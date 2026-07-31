"""Validated model objects for exact finite-discrete causal BNs."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import re
from typing import Mapping, TypeAlias


StateValue: TypeAlias = int | str

_IDENTIFIER_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")
_FIXTURE_ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")

POSITIVE_STOCHASTIC_REGIME = "positive_stochastic"
ROOT_STOCHASTIC_DETERMINISTIC_NONROOTS_REGIME = (
    "root_stochastic_deterministic_nonroots"
)


def point_mass_index(probabilities: tuple[Fraction, ...]) -> int | None:
    """Return the certain-state index for a point mass, otherwise ``None``."""

    ones = [index for index, probability in enumerate(probabilities) if probability == 1]
    if len(ones) != 1:
        return None
    if any(
        probability not in {Fraction(0, 1), Fraction(1, 1)}
        for probability in probabilities
    ):
        return None
    return ones[0]


class FixtureValidationError(ValueError):
    """Raised when a causal fixture definition is internally inconsistent."""


@dataclass(frozen=True)
class Variable:
    """One observed finite-discrete variable and its declared state order."""

    name: str
    states: tuple[StateValue, ...]


@dataclass(frozen=True)
class CPTRow:
    """One exact conditional-probability row.

    ``when`` follows the mechanism's declared parent order and
    ``probabilities`` follows the child variable's declared state order.
    """

    when: tuple[tuple[str, StateValue], ...]
    probabilities: tuple[Fraction, ...]


@dataclass(frozen=True)
class Mechanism:
    """The ordered parents and complete CPT for one variable."""

    variable: str
    parents: tuple[str, ...]
    rows: tuple[CPTRow, ...]

    @property
    def deterministic(self) -> bool:
        return all(point_mass_index(row.probabilities) is not None for row in self.rows)

    def distribution(
        self, parent_assignment: Mapping[str, StateValue]
    ) -> tuple[Fraction, ...]:
        key = tuple((parent, parent_assignment[parent]) for parent in self.parents)
        for row in self.rows:
            if row.when == key:
                return row.probabilities
        raise KeyError(
            f"no CPT row for {self.variable!r} with parent assignment {dict(key)!r}"
        )


@dataclass(frozen=True)
class CausalAssumptions:
    """Declared causal and sampling semantics not inferable from a BIF alone."""

    causal_sufficiency_declared: bool
    exogenous_noise: str
    sampling_regime: str
    mechanism_regime: str = POSITIVE_STOCHASTIC_REGIME


def _deterministic_topological_order(
    nodes: tuple[str, ...], edges: tuple[tuple[str, str], ...]
) -> tuple[str, ...]:
    """Return a topological order, breaking ties by declared variable order."""
    index = {node: i for i, node in enumerate(nodes)}
    children: dict[str, list[str]] = {node: [] for node in nodes}
    indegree = {node: 0 for node in nodes}
    for source, target in edges:
        children[source].append(target)
        indegree[target] += 1

    ready = [node for node in nodes if indegree[node] == 0]
    order: list[str] = []
    while ready:
        ready.sort(key=index.__getitem__)
        node = ready.pop(0)
        order.append(node)
        for child in sorted(children[node], key=index.__getitem__):
            indegree[child] -= 1
            if indegree[child] == 0:
                ready.append(child)

    if len(order) != len(nodes):
        raise FixtureValidationError("graph.edges must define an acyclic graph")
    return tuple(order)


@dataclass(frozen=True)
class CausalFixture:
    """An exact finite-discrete causal Bayesian network.

    Schema version 1 preserves the original strictly positive stochastic
    regime. Schema version 2 represents non-degenerate stochastic roots and
    deterministic non-root structural functions explicitly.
    """

    schema_version: int
    fixture_id: str
    title: str
    description: str
    variables: tuple[Variable, ...]
    edges: tuple[tuple[str, str], ...]
    mechanisms: tuple[Mechanism, ...]
    assumptions: CausalAssumptions

    def __post_init__(self) -> None:
        self.validate()

    @property
    def variable_names(self) -> tuple[str, ...]:
        return tuple(variable.name for variable in self.variables)

    @property
    def topological_order(self) -> tuple[str, ...]:
        return _deterministic_topological_order(self.variable_names, self.edges)

    def variable(self, name: str) -> Variable:
        for variable in self.variables:
            if variable.name == name:
                return variable
        raise KeyError(name)

    def states_of(self, name: str) -> tuple[StateValue, ...]:
        return self.variable(name).states

    def mechanism_for(self, name: str) -> Mechanism:
        for mechanism in self.mechanisms:
            if mechanism.variable == name:
                return mechanism
        raise KeyError(name)

    def parents_of(self, name: str) -> tuple[str, ...]:
        return self.mechanism_for(name).parents

    def children_of(self, name: str) -> tuple[str, ...]:
        node_index = {node: i for i, node in enumerate(self.variable_names)}
        return tuple(
            sorted(
                (target for source, target in self.edges if source == name),
                key=node_index.__getitem__,
            )
        )

    @property
    def root_names(self) -> tuple[str, ...]:
        return tuple(name for name in self.variable_names if not self.parents_of(name))

    @property
    def deterministic_variables(self) -> tuple[str, ...]:
        return tuple(
            name for name in self.variable_names if self.mechanism_for(name).deterministic
        )

    @property
    def stochastic_variables(self) -> tuple[str, ...]:
        deterministic = set(self.deterministic_variables)
        return tuple(name for name in self.variable_names if name not in deterministic)

    def conditional_distribution(
        self, variable: str, parent_assignment: Mapping[str, StateValue]
    ) -> tuple[Fraction, ...]:
        return self.mechanism_for(variable).distribution(parent_assignment)

    def conditional_probability(
        self,
        variable: str,
        value: StateValue,
        parent_assignment: Mapping[str, StateValue],
    ) -> Fraction:
        states = self.states_of(variable)
        try:
            state_index = states.index(value)
        except ValueError as exc:
            raise KeyError(f"unknown state {value!r} for variable {variable!r}") from exc
        return self.conditional_distribution(variable, parent_assignment)[state_index]

    def validate(self) -> None:
        if self.schema_version not in {1, 2}:
            raise FixtureValidationError(
                f"unsupported fixture schema_version: {self.schema_version!r}"
            )
        expected_regime = (
            POSITIVE_STOCHASTIC_REGIME
            if self.schema_version == 1
            else ROOT_STOCHASTIC_DETERMINISTIC_NONROOTS_REGIME
        )
        if self.assumptions.mechanism_regime != expected_regime:
            raise FixtureValidationError(
                f"schema_version {self.schema_version} requires "
                f"assumptions.mechanism_regime={expected_regime!r}"
            )
        if not _FIXTURE_ID_RE.fullmatch(self.fixture_id):
            raise FixtureValidationError(
                "id must start with a letter and contain only letters, digits, '_', or '-'"
            )
        if not self.variables:
            raise FixtureValidationError("variables must be non-empty")

        names = self.variable_names
        if len(set(names)) != len(names):
            raise FixtureValidationError("variable names must be unique")
        for variable in self.variables:
            if not _IDENTIFIER_RE.fullmatch(variable.name):
                raise FixtureValidationError(
                    f"invalid variable name {variable.name!r}; use a BIF-safe identifier"
                )
            if len(variable.states) < 2:
                raise FixtureValidationError(
                    f"variables.{variable.name}.states must contain at least two states"
                )
            for state in variable.states:
                if isinstance(state, bool) or not isinstance(state, (int, str)):
                    raise FixtureValidationError(
                        f"state {state!r} for {variable.name!r} must be an int or string"
                    )
                if isinstance(state, str) and not state:
                    raise FixtureValidationError(
                        f"states for {variable.name!r} may not contain an empty string"
                    )
            if len(set(variable.states)) != len(variable.states):
                raise FixtureValidationError(
                    f"states for {variable.name!r} must be unique"
                )
            if len({type(state) for state in variable.states}) != 1:
                raise FixtureValidationError(
                    f"states for {variable.name!r} must use one homogeneous type "
                    "so CSV round trips preserve the domain"
                )
            if len({str(state) for state in variable.states}) != len(variable.states):
                raise FixtureValidationError(
                    f"states for {variable.name!r} must have unique string forms for BIF export"
                )

        node_set = set(names)
        if len(set(self.edges)) != len(self.edges):
            raise FixtureValidationError("graph.edges must not contain duplicates")
        for source, target in self.edges:
            if source not in node_set or target not in node_set:
                raise FixtureValidationError(
                    f"graph edge ({source!r}, {target!r}) names an unknown variable"
                )
            if source == target:
                raise FixtureValidationError(
                    f"graph edge ({source!r}, {target!r}) is a self-loop"
                )
        _deterministic_topological_order(names, self.edges)

        mechanisms_by_variable = {
            mechanism.variable: mechanism for mechanism in self.mechanisms
        }
        if len(mechanisms_by_variable) != len(self.mechanisms):
            raise FixtureValidationError("mechanisms must contain each variable once")
        if set(mechanisms_by_variable) != node_set:
            missing = sorted(node_set - set(mechanisms_by_variable))
            extra = sorted(set(mechanisms_by_variable) - node_set)
            raise FixtureValidationError(
                f"mechanisms must match variables exactly; missing={missing}, extra={extra}"
            )

        for variable in self.variables:
            mechanism = mechanisms_by_variable[variable.name]
            expected_parents = tuple(
                node for node in names if (node, variable.name) in set(self.edges)
            )
            if mechanism.parents != expected_parents:
                raise FixtureValidationError(
                    f"mechanisms.{variable.name}.parents must equal graph parents in "
                    f"declared variable order: expected {expected_parents}, got {mechanism.parents}"
                )
            if len(set(mechanism.parents)) != len(mechanism.parents):
                raise FixtureValidationError(
                    f"mechanisms.{variable.name}.parents must be unique"
                )

            expected_parent_values = tuple(
                product(*(self.states_of(parent) for parent in mechanism.parents))
            )
            expected_keys = {
                tuple(zip(mechanism.parents, values))
                for values in expected_parent_values
            }
            actual_keys = [row.when for row in mechanism.rows]
            if len(set(actual_keys)) != len(actual_keys):
                raise FixtureValidationError(
                    f"mechanisms.{variable.name}.cpt contains duplicate parent assignments"
                )
            if set(actual_keys) != expected_keys:
                missing = expected_keys - set(actual_keys)
                extra = set(actual_keys) - expected_keys
                raise FixtureValidationError(
                    f"mechanisms.{variable.name}.cpt must cover every parent assignment "
                    f"exactly once; missing={sorted(map(str, missing))}, "
                    f"extra={sorted(map(str, extra))}"
                )

            for row in mechanism.rows:
                if tuple(parent for parent, _ in row.when) != mechanism.parents:
                    raise FixtureValidationError(
                        f"mechanisms.{variable.name}.cpt parent order must be {mechanism.parents}"
                    )
                if len(row.probabilities) != len(variable.states):
                    raise FixtureValidationError(
                        f"mechanisms.{variable.name}.cpt probability vector must have "
                        f"{len(variable.states)} entries"
                    )
                if any(
                    not isinstance(probability, Fraction)
                    for probability in row.probabilities
                ):
                    raise FixtureValidationError(
                        f"mechanisms.{variable.name}.cpt probabilities must be "
                        "fractions.Fraction values"
                    )
                if any(probability < 0 for probability in row.probabilities):
                    raise FixtureValidationError(
                        f"mechanisms.{variable.name}.cpt probabilities must be non-negative"
                    )
                if sum(row.probabilities, Fraction(0, 1)) != Fraction(1, 1):
                    raise FixtureValidationError(
                        f"mechanisms.{variable.name}.cpt probabilities must sum exactly to one"
                    )

                if self.schema_version == 1 and any(
                    probability == 0 for probability in row.probabilities
                ):
                    raise FixtureValidationError(
                        f"mechanisms.{variable.name}.cpt probabilities must all be "
                        "strictly positive under schema_version 1"
                    )

            if self.schema_version == 2:
                if mechanism.parents:
                    if not mechanism.deterministic:
                        raise FixtureValidationError(
                            f"mechanisms.{variable.name} must be deterministic under "
                            f"{ROOT_STOCHASTIC_DETERMINISTIC_NONROOTS_REGIME!r}"
                        )
                else:
                    root_distribution = mechanism.rows[0].probabilities
                    if any(probability <= 0 for probability in root_distribution):
                        raise FixtureValidationError(
                            f"root mechanism {variable.name!r} must assign strictly "
                            "positive probability to every state"
                        )
                    if mechanism.deterministic:
                        raise FixtureValidationError(
                            f"root mechanism {variable.name!r} must be non-degenerate"
                        )

        if self.assumptions.causal_sufficiency_declared:
            expected_noise = (
                "mutually_independent_private_exogenous_noise"
                if self.schema_version == 1
                else "mutually_independent_root_exogenous_noise"
            )
            if self.assumptions.exogenous_noise != expected_noise:
                raise FixtureValidationError(
                    "causal sufficiency may be declared only with "
                    f"exogenous_noise={expected_noise!r}"
                )
        if self.assumptions.sampling_regime != "observational_iid":
            raise FixtureValidationError(
                "sampling regime for this fixture model must be 'observational_iid'"
            )
