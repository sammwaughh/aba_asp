"""Exact population, conditional-independence, MEC, and CPDAG analysis."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from fractions import Fraction
import io
from itertools import combinations, product
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from causal.fixtures.artifacts import (
    FIXTURE_TOOLKIT_VERSION,
    file_sha256,
    write_text_once,
)
from causal.fixtures.io import LoadedFixture
from causal.fixtures.model import CausalFixture, StateValue


class MECEnumerationError(ValueError):
    """Raised when exact MEC enumeration exceeds its explicit small-graph bound."""


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


@dataclass(frozen=True)
class PopulationRow:
    assignment: tuple[StateValue, ...]
    probability: Fraction


@dataclass(frozen=True)
class ExactPopulation:
    """A canonical exact joint distribution in declared variable order."""

    variables: tuple[str, ...]
    states: tuple[tuple[StateValue, ...], ...]
    rows: tuple[PopulationRow, ...]

    @property
    def total_probability(self) -> Fraction:
        return sum((row.probability for row in self.rows), Fraction(0, 1))

    def mass(self, constraints: Mapping[str, StateValue]) -> Fraction:
        unknown = set(constraints) - set(self.variables)
        if unknown:
            raise KeyError(f"unknown variables in marginal query: {sorted(unknown)}")
        indices = {name: i for i, name in enumerate(self.variables)}
        return sum(
            (
                row.probability
                for row in self.rows
                if all(row.assignment[indices[name]] == value for name, value in constraints.items())
            ),
            Fraction(0, 1),
        )

    def assignment_mapping(self, row: PopulationRow) -> dict[str, StateValue]:
        return dict(zip(self.variables, row.assignment))


@dataclass(frozen=True)
class CIWitness:
    conditioning_assignment: tuple[tuple[str, StateValue], ...]
    x_value: StateValue
    y_value: StateValue
    p_xy_s: Fraction
    p_s: Fraction
    p_x_s: Fraction
    p_y_s: Fraction
    lhs: Fraction
    rhs: Fraction

    @property
    def difference(self) -> Fraction:
        return self.lhs - self.rhs


@dataclass(frozen=True)
class CIQueryResult:
    x: str
    y: str
    conditioning: tuple[str, ...]
    graph_d_separated: bool
    population_independent: bool
    witness: CIWitness | None


@dataclass(frozen=True)
class EdgeActivityResult:
    parent: str
    child: str
    active: bool
    witness_other_parents: tuple[tuple[str, StateValue], ...] | None
    parent_state_a: StateValue | None
    parent_state_b: StateValue | None
    distribution_a: tuple[Fraction, ...] | None
    distribution_b: tuple[Fraction, ...] | None


@dataclass(frozen=True)
class MECResult:
    members: tuple[tuple[tuple[str, str], ...], ...]
    cpdag_directed: tuple[tuple[str, str], ...]
    cpdag_undirected: tuple[tuple[str, str], ...]


def derive_population(fixture: CausalFixture) -> ExactPopulation:
    """Derive the full exact joint by Bayesian-network factorisation."""
    variables = fixture.variable_names
    states = tuple(fixture.states_of(variable) for variable in variables)
    rows: list[PopulationRow] = []
    for values in product(*states):
        assignment = dict(zip(variables, values))
        probability = Fraction(1, 1)
        for variable in fixture.topological_order:
            mechanism = fixture.mechanism_for(variable)
            parent_assignment = {
                parent: assignment[parent] for parent in mechanism.parents
            }
            probability *= fixture.conditional_probability(
                variable, assignment[variable], parent_assignment
            )
        rows.append(PopulationRow(assignment=tuple(values), probability=probability))
    population = ExactPopulation(variables=variables, states=states, rows=tuple(rows))
    if population.total_probability != Fraction(1, 1):
        raise AssertionError(
            "validated CPTs produced a non-normalized joint distribution: "
            f"{population.total_probability}"
        )
    return population


def _all_conditioning_sets(nodes: tuple[str, ...]) -> Iterable[tuple[str, ...]]:
    for size in range(len(nodes) + 1):
        yield from combinations(nodes, size)


def _ancestors(
    nodes: set[str], edges: tuple[tuple[str, str], ...]
) -> set[str]:
    result = set(nodes)
    changed = True
    while changed:
        changed = False
        for parent, child in edges:
            if child in result and parent not in result:
                result.add(parent)
                changed = True
    return result


def graph_d_separated(
    fixture: CausalFixture,
    x: str,
    y: str,
    conditioning: tuple[str, ...],
) -> bool:
    """Test d-separation by ancestral moralisation."""
    node_set = set(fixture.variable_names)
    if x not in node_set or y not in node_set:
        raise KeyError(f"unknown d-separation endpoint: {x!r}, {y!r}")
    if x == y:
        raise ValueError("d-separation endpoints must be different")
    condition_set = set(conditioning)
    if len(condition_set) != len(conditioning):
        raise ValueError("conditioning set must not contain duplicate variables")
    if not condition_set <= node_set:
        raise KeyError(f"unknown conditioning variables: {sorted(condition_set - node_set)}")
    if x in condition_set or y in condition_set:
        raise ValueError("conditioning set must exclude the query endpoints")

    ancestral_nodes = _ancestors({x, y} | condition_set, fixture.edges)
    adjacency: dict[str, set[str]] = {node: set() for node in ancestral_nodes}
    for source, target in fixture.edges:
        if source in ancestral_nodes and target in ancestral_nodes:
            adjacency[source].add(target)
            adjacency[target].add(source)

    for child in ancestral_nodes:
        parents = [
            parent
            for parent, target in fixture.edges
            if target == child and parent in ancestral_nodes
        ]
        for left, right in combinations(parents, 2):
            adjacency[left].add(right)
            adjacency[right].add(left)

    visited = set(condition_set)
    frontier = [x]
    while frontier:
        node = frontier.pop()
        if node == y:
            return False
        if node in visited:
            continue
        visited.add(node)
        frontier.extend(neighbour for neighbour in adjacency[node] if neighbour not in visited)
    return True


def check_population_ci(
    fixture: CausalFixture,
    population: ExactPopulation,
    x: str,
    y: str,
    conditioning: tuple[str, ...],
) -> tuple[bool, CIWitness | None]:
    """Check finite categorical CI using exact unnormalised masses.

    For every state assignment ``x, y, s``, conditional independence is
    equivalent to ``P(x,y,s)P(s) = P(x,s)P(y,s)``.
    """
    node_set = set(fixture.variable_names)
    if x not in node_set or y not in node_set:
        raise KeyError(f"unknown conditional-independence endpoint: {x!r}, {y!r}")
    if x == y:
        raise ValueError("conditional-independence endpoints must be different")
    condition_set = set(conditioning)
    if len(condition_set) != len(conditioning):
        raise ValueError("conditioning set must not contain duplicate variables")
    if not condition_set <= node_set:
        raise KeyError(f"unknown conditioning variables: {sorted(condition_set - node_set)}")
    if x in condition_set or y in condition_set:
        raise ValueError("conditioning set must exclude the query endpoints")
    condition_domains = [fixture.states_of(variable) for variable in conditioning]
    for condition_values in product(*condition_domains):
        condition_assignment = dict(zip(conditioning, condition_values))
        p_s = population.mass(condition_assignment)
        for x_value in fixture.states_of(x):
            for y_value in fixture.states_of(y):
                joint_constraints = {
                    **condition_assignment,
                    x: x_value,
                    y: y_value,
                }
                x_constraints = {**condition_assignment, x: x_value}
                y_constraints = {**condition_assignment, y: y_value}
                p_xy_s = population.mass(joint_constraints)
                p_x_s = population.mass(x_constraints)
                p_y_s = population.mass(y_constraints)
                lhs = p_xy_s * p_s
                rhs = p_x_s * p_y_s
                if lhs != rhs:
                    return False, CIWitness(
                        conditioning_assignment=tuple(
                            (variable, condition_assignment[variable])
                            for variable in conditioning
                        ),
                        x_value=x_value,
                        y_value=y_value,
                        p_xy_s=p_xy_s,
                        p_s=p_s,
                        p_x_s=p_x_s,
                        p_y_s=p_y_s,
                        lhs=lhs,
                        rhs=rhs,
                    )
    return True, None


def audit_conditional_independences(
    fixture: CausalFixture, population: ExactPopulation
) -> tuple[CIQueryResult, ...]:
    """Audit every singleton pair and every subset of remaining variables."""
    results: list[CIQueryResult] = []
    variables = fixture.variable_names
    for x_index, x in enumerate(variables):
        for y in variables[x_index + 1 :]:
            remaining = tuple(variable for variable in variables if variable not in {x, y})
            for conditioning in _all_conditioning_sets(remaining):
                independent, witness = check_population_ci(
                    fixture, population, x, y, conditioning
                )
                results.append(
                    CIQueryResult(
                        x=x,
                        y=y,
                        conditioning=conditioning,
                        graph_d_separated=graph_d_separated(
                            fixture, x, y, conditioning
                        ),
                        population_independent=independent,
                        witness=witness,
                    )
                )
    return tuple(results)


def audit_edge_activity(fixture: CausalFixture) -> tuple[EdgeActivityResult, ...]:
    """Check whether each declared parent can change its child's CPT."""
    results: list[EdgeActivityResult] = []
    for parent, child in fixture.edges:
        mechanism = fixture.mechanism_for(child)
        other_parents = tuple(node for node in mechanism.parents if node != parent)
        other_domains = [fixture.states_of(node) for node in other_parents]
        witness: EdgeActivityResult | None = None
        for other_values in product(*other_domains):
            other_assignment = dict(zip(other_parents, other_values))
            for state_a, state_b in combinations(fixture.states_of(parent), 2):
                assignment_a = {**other_assignment, parent: state_a}
                assignment_b = {**other_assignment, parent: state_b}
                distribution_a = mechanism.distribution(assignment_a)
                distribution_b = mechanism.distribution(assignment_b)
                if distribution_a != distribution_b:
                    witness = EdgeActivityResult(
                        parent=parent,
                        child=child,
                        active=True,
                        witness_other_parents=tuple(
                            (node, other_assignment[node]) for node in other_parents
                        ),
                        parent_state_a=state_a,
                        parent_state_b=state_b,
                        distribution_a=distribution_a,
                        distribution_b=distribution_b,
                    )
                    break
            if witness is not None:
                break
        if witness is None:
            witness = EdgeActivityResult(
                parent=parent,
                child=child,
                active=False,
                witness_other_parents=None,
                parent_state_a=None,
                parent_state_b=None,
                distribution_a=None,
                distribution_b=None,
            )
        results.append(witness)
    return tuple(results)


def _edge_sort_key(
    edge: tuple[str, str], node_index: Mapping[str, int]
) -> tuple[int, int]:
    return node_index[edge[0]], node_index[edge[1]]


def skeleton_edges(fixture: CausalFixture) -> tuple[tuple[str, str], ...]:
    index = {node: i for i, node in enumerate(fixture.variable_names)}
    skeleton = {
        (source, target) if index[source] < index[target] else (target, source)
        for source, target in fixture.edges
    }
    return tuple(sorted(skeleton, key=lambda edge: _edge_sort_key(edge, index)))


def unshielded_colliders(
    nodes: tuple[str, ...], edges: tuple[tuple[str, str], ...]
) -> tuple[tuple[str, str, str], ...]:
    index = {node: i for i, node in enumerate(nodes)}
    adjacency = {frozenset(edge) for edge in edges}
    colliders: set[tuple[str, str, str]] = set()
    for center in nodes:
        parents = [source for source, target in edges if target == center]
        for left, right in combinations(parents, 2):
            if frozenset((left, right)) in adjacency:
                continue
            if index[left] > index[right]:
                left, right = right, left
            colliders.add((left, center, right))
    return tuple(
        sorted(
            colliders,
            key=lambda collider: (
                index[collider[1]],
                index[collider[0]],
                index[collider[2]],
            ),
        )
    )


def _is_acyclic(
    nodes: tuple[str, ...], edges: tuple[tuple[str, str], ...]
) -> bool:
    indegree = {node: 0 for node in nodes}
    children: dict[str, list[str]] = {node: [] for node in nodes}
    for source, target in edges:
        indegree[target] += 1
        children[source].append(target)
    frontier = [node for node in nodes if indegree[node] == 0]
    seen = 0
    while frontier:
        node = frontier.pop()
        seen += 1
        for child in children[node]:
            indegree[child] -= 1
            if indegree[child] == 0:
                frontier.append(child)
    return seen == len(nodes)


def enumerate_markov_equivalence_class(
    fixture: CausalFixture, *, max_edges: int = 16
) -> MECResult:
    """Enumerate the exact MEC for a bounded small DAG and derive its CPDAG."""
    skeleton = skeleton_edges(fixture)
    if len(skeleton) > max_edges:
        raise MECEnumerationError(
            f"exact MEC enumeration needs 2^{len(skeleton)} orientations; "
            f"configured max_edges is {max_edges}"
        )
    nodes = fixture.variable_names
    node_index = {node: i for i, node in enumerate(nodes)}
    target_colliders = set(unshielded_colliders(nodes, fixture.edges))
    members: list[tuple[tuple[str, str], ...]] = []
    for mask in range(1 << len(skeleton)):
        candidate: list[tuple[str, str]] = []
        for bit, (left, right) in enumerate(skeleton):
            candidate.append((right, left) if mask & (1 << bit) else (left, right))
        candidate_tuple = tuple(
            sorted(candidate, key=lambda edge: _edge_sort_key(edge, node_index))
        )
        if not _is_acyclic(nodes, candidate_tuple):
            continue
        if set(unshielded_colliders(nodes, candidate_tuple)) != target_colliders:
            continue
        members.append(candidate_tuple)

    generating_edges = tuple(
        sorted(fixture.edges, key=lambda edge: _edge_sort_key(edge, node_index))
    )
    if generating_edges not in members:
        raise AssertionError("MEC enumeration omitted the generating DAG")

    directed: list[tuple[str, str]] = []
    undirected: list[tuple[str, str]] = []
    for left, right in skeleton:
        if all((left, right) in member for member in members):
            directed.append((left, right))
        elif all((right, left) in member for member in members):
            directed.append((right, left))
        else:
            undirected.append((left, right))
    return MECResult(
        members=tuple(members),
        cpdag_directed=tuple(
            sorted(directed, key=lambda edge: _edge_sort_key(edge, node_index))
        ),
        cpdag_undirected=tuple(
            sorted(undirected, key=lambda edge: _edge_sort_key(edge, node_index))
        ),
    )


def _node_roles(
    nodes: tuple[str, ...], edges: tuple[tuple[str, str], ...]
) -> dict[str, str]:
    result: dict[str, str] = {}
    for node in nodes:
        has_parent = any(target == node for _, target in edges)
        has_child = any(source == node for source, _ in edges)
        if not has_parent and not has_child:
            result[node] = "isolated"
        elif not has_parent:
            result[node] = "source"
        elif not has_child:
            result[node] = "sink"
        else:
            result[node] = "internal"
    return result


def _ci_statement(result: CIQueryResult) -> dict[str, Any]:
    return {
        "x": result.x,
        "y": result.y,
        "conditioning": list(result.conditioning),
    }


def _witness_document(witness: CIWitness | None) -> dict[str, Any] | None:
    if witness is None:
        return None
    return {
        "conditioning_assignment": [list(item) for item in witness.conditioning_assignment],
        "x_value": witness.x_value,
        "y_value": witness.y_value,
        "p_xy_s": fraction_text(witness.p_xy_s),
        "p_s": fraction_text(witness.p_s),
        "p_x_s": fraction_text(witness.p_x_s),
        "p_y_s": fraction_text(witness.p_y_s),
        "lhs_p_xy_s_times_p_s": fraction_text(witness.lhs),
        "rhs_p_x_s_times_p_y_s": fraction_text(witness.rhs),
        "difference": fraction_text(witness.difference),
    }


def _ci_query_document(result: CIQueryResult) -> dict[str, Any]:
    return {
        **_ci_statement(result),
        "graph_d_separated": result.graph_d_separated,
        "population_independent": result.population_independent,
        "dependence_witness": _witness_document(result.witness),
    }


def _edge_activity_document(result: EdgeActivityResult) -> dict[str, Any]:
    document: dict[str, Any] = {
        "edge": [result.parent, result.child],
        "active": result.active,
    }
    if result.active:
        document["witness"] = {
            "other_parent_assignment": [
                list(item) for item in (result.witness_other_parents or ())
            ],
            "parent_states_compared": [result.parent_state_a, result.parent_state_b],
            "conditional_distribution_a": [
                fraction_text(value) for value in (result.distribution_a or ())
            ],
            "conditional_distribution_b": [
                fraction_text(value) for value in (result.distribution_b or ())
            ],
        }
    else:
        document["witness"] = None
    return document


def build_certificate(
    loaded: LoadedFixture, *, max_mec_edges: int = 16
) -> tuple[ExactPopulation, dict[str, Any]]:
    """Build a complete exact population certificate for one loaded fixture."""
    fixture = loaded.fixture
    population = derive_population(fixture)
    queries = audit_conditional_independences(fixture, population)
    edge_activity = audit_edge_activity(fixture)
    mec = enumerate_markov_equivalence_class(fixture, max_edges=max_mec_edges)

    graph_implied = tuple(result for result in queries if result.graph_d_separated)
    population_independent = tuple(
        result for result in queries if result.population_independent
    )
    markov_violations = tuple(
        result
        for result in queries
        if result.graph_d_separated and not result.population_independent
    )
    extra_independences = tuple(
        result
        for result in queries
        if result.population_independent and not result.graph_d_separated
    )
    if markov_violations:
        raise AssertionError(
            "a population derived from validated DAG factorisation violated a "
            "graph-implied conditional independence; this indicates an analyser bug"
        )
    faithful = not markov_violations and not extra_independences

    member_roles = [_node_roles(fixture.variable_names, member) for member in mec.members]
    possible_roles = {
        node: sorted({roles[node] for roles in member_roles})
        for node in fixture.variable_names
    }
    invariant_roles = {
        node: roles[0]
        for node, roles in possible_roles.items()
        if len(roles) == 1
    }

    minimum_row = min(population.rows, key=lambda row: row.probability)
    certificate: dict[str, Any] = {
        "certificate_schema_version": 1,
        "generator": {
            "fixture_toolkit_version": FIXTURE_TOOLKIT_VERSION,
            "implementation_modules": {
                "causal.fixtures.analysis": file_sha256(Path(__file__)),
                "causal.fixtures.io": file_sha256(Path(__file__).with_name("io.py")),
                "causal.fixtures.model": file_sha256(
                    Path(__file__).with_name("model.py")
                ),
            },
            "algorithms": {
                "population": "exact DAG factorisation",
                "conditional_independence": "exact finite-categorical cross-product identity",
                "d_separation": "ancestral moralisation",
                "mec": "bounded exhaustive skeleton orientation",
                "cpdag": "orientation invariance across enumerated MEC",
            },
        },
        "fixture": {
            "id": fixture.fixture_id,
            "source_path": str(loaded.source_path),
            "source_hash": loaded.source_hash,
            "source_hash_basis": "exact UTF-8 source-file bytes",
            "document_hash": loaded.document_hash,
            "document_hash_basis": "canonical parsed YAML document",
            "semantic_hash": loaded.semantic_hash,
        },
        "scope": {
            "distribution_level": "exact_population",
            "arithmetic": "fractions.Fraction exact rationals",
            "ci_audit": (
                "every unordered singleton variable pair and every subset of the "
                "remaining variables"
            ),
            "ci_identity": "P(x,y,s)P(s) = P(x,s)P(y,s)",
            "faithfulness_scope": "ordinary observational DAG faithfulness",
            "learner_visible": False,
        },
        "graph": {
            "variables": list(fixture.variable_names),
            "state_orders": {
                variable: list(fixture.states_of(variable))
                for variable in fixture.variable_names
            },
            "edges": [list(edge) for edge in fixture.edges],
            "topological_order": list(fixture.topological_order),
            "skeleton": [list(edge) for edge in skeleton_edges(fixture)],
            "unshielded_colliders": [
                list(collider)
                for collider in unshielded_colliders(
                    fixture.variable_names, fixture.edges
                )
            ],
            "generating_dag_roles": _node_roles(
                fixture.variable_names, fixture.edges
            ),
            "markov_equivalence_class": {
                "method": "exact orientation enumeration by skeleton and unshielded colliders",
                "size": len(mec.members),
                "members": [
                    {"edges": [list(edge) for edge in member]}
                    for member in mec.members
                ],
            },
            "cpdag": {
                "kind": "graph-theoretic essential graph of the generating DAG MEC",
                "directed_edges": [list(edge) for edge in mec.cpdag_directed],
                "undirected_edges": [list(edge) for edge in mec.cpdag_undirected],
                "observational_recovery_scope": (
                    "this CPDAG is the population-level CI recovery target only under "
                    "causal sufficiency, the causal Markov condition, and ordinary "
                    "faithfulness"
                ),
                "identified_by_this_population_ci_structure": (
                    faithful and fixture.assumptions.causal_sufficiency_declared
                ),
            },
            "roles_across_mec": {
                "possible": possible_roles,
                "invariant": invariant_roles,
            },
        },
        "mechanisms": {
            "strictly_positive_local_probabilities": all(
                probability > 0
                for mechanism in fixture.mechanisms
                for row in mechanism.rows
                for probability in row.probabilities
            ),
            "edge_activity": [
                _edge_activity_document(result) for result in edge_activity
            ],
            "all_edges_active": all(result.active for result in edge_activity),
            "interpretation": (
                "all edges active is a local mechanism/minimality check; it is not "
                "by itself a faithfulness proof"
            ),
        },
        "population": {
            "number_of_joint_states": len(population.rows),
            "normalised": population.total_probability == Fraction(1, 1),
            "total_probability": fraction_text(population.total_probability),
            "full_support": all(row.probability > 0 for row in population.rows),
            "minimum_joint_probability": fraction_text(minimum_row.probability),
            "minimum_joint_probability_assignment": dict(
                zip(fixture.variable_names, minimum_row.assignment)
            ),
        },
        "assumptions_and_results": {
            "causal_sufficiency": {
                "status": (
                    "declared_satisfied_by_fixture_design"
                    if fixture.assumptions.causal_sufficiency_declared
                    else "not_declared"
                ),
                "exogenous_noise": fixture.assumptions.exogenous_noise,
                "basis": (
                    "the fixture declares one mutually independent private exogenous "
                    "noise variable per observed node; this is not inferred from the "
                    "CPTs or observational population"
                ),
                "observationally_testable_from_joint_distribution": False,
            },
            "causal_markov_condition": {
                "status": "verified",
                "factorisation_basis": (
                    "the joint was derived as the product of the validated local "
                    "CPTs over the DAG"
                ),
                "exact_graph_implied_ci_violations": len(markov_violations),
            },
            "ordinary_faithfulness": {
                "status": "verified_exactly" if faithful else "not_satisfied",
                "faithful": faithful,
                "basis": (
                    "the exact population CI set equals the graph d-separation set "
                    "over the exhaustive singleton-pair audit"
                ),
                "why_singleton_audit_is_sufficient": (
                    "DAG factorisation establishes the global Markov direction. A DAG "
                    "d-separates two variable sets exactly when it d-separates every "
                    "cross-pair, while probabilistic setwise conditional independence "
                    "implies every cross-pair conditional independence by decomposition. "
                    "Therefore any extra setwise population independence would yield an "
                    "extra singleton-pair independence detected by this audit."
                ),
            },
            "sampling_regime": fixture.assumptions.sampling_regime,
        },
        "conditional_independence_audit": {
            "query_count": len(queries),
            "graph_implied_independence_count": len(graph_implied),
            "population_independence_count": len(population_independent),
            "graph_implied_independences": [
                _ci_statement(result) for result in graph_implied
            ],
            "population_independences": [
                _ci_statement(result) for result in population_independent
            ],
            "markov_violations": [
                _ci_query_document(result) for result in markov_violations
            ],
            "extra_independences": [
                _ci_query_document(result) for result in extra_independences
            ],
            "queries": [_ci_query_document(result) for result in queries],
        },
    }
    return population, certificate


def write_population_csv(population: ExactPopulation, path: Path | str) -> Path:
    destination = Path(path)
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(
        [*population.variables, "probability_exact", "probability_decimal"]
    )
    for row in population.rows:
        writer.writerow(
            [
                *row.assignment,
                fraction_text(row.probability),
                format(float(row.probability), ".12g"),
            ]
        )
    return write_text_once(destination, buffer.getvalue())


def write_certificate_json(certificate: Mapping[str, Any], path: Path | str) -> Path:
    destination = Path(path)
    return write_text_once(
        destination, json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    )
