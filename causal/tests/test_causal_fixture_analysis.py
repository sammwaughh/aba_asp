from __future__ import annotations

from fractions import Fraction
from pathlib import Path

import pytest

from causal.fixtures.analysis import (
    MECEnumerationError,
    build_certificate,
    derive_population,
    enumerate_markov_equivalence_class,
    graph_d_separated,
)
from causal.fixtures.io import default_diamond_spec_path, load_fixture
from causal.tests.fixture_test_utils import write_root_stochastic_deterministic_and


EXPECTED_DIAMOND_JOINT = {
    (0, 0, 0, 0): Fraction(49, 250),
    (0, 0, 0, 1): Fraction(49, 1000),
    (0, 0, 1, 0): Fraction(147, 4000),
    (0, 0, 1, 1): Fraction(273, 4000),
    (0, 1, 0, 0): Fraction(147, 4000),
    (0, 1, 0, 1): Fraction(273, 4000),
    (0, 1, 1, 0): Fraction(9, 1000),
    (0, 1, 1, 1): Fraction(9, 250),
    (1, 0, 0, 0): Fraction(9, 250),
    (1, 0, 0, 1): Fraction(9, 1000),
    (1, 0, 1, 0): Fraction(147, 4000),
    (1, 0, 1, 1): Fraction(273, 4000),
    (1, 1, 0, 0): Fraction(147, 4000),
    (1, 1, 0, 1): Fraction(273, 4000),
    (1, 1, 1, 0): Fraction(49, 1000),
    (1, 1, 1, 1): Fraction(49, 250),
}


def test_exact_diamond_population_matches_approved_table() -> None:
    fixture = load_fixture(default_diamond_spec_path()).fixture
    population = derive_population(fixture)
    observed = {row.assignment: row.probability for row in population.rows}

    assert observed == EXPECTED_DIAMOND_JOINT
    assert population.total_probability == 1
    assert min(observed.values()) == Fraction(9, 1000)


def test_diamond_certificate_faithfulness_mec_and_cpdag() -> None:
    loaded = load_fixture(default_diamond_spec_path())
    _, certificate = build_certificate(loaded)
    audit = certificate["conditional_independence_audit"]

    assert audit["query_count"] == 24
    assert audit["population_independences"] == [
        {"x": "x0", "y": "x3", "conditioning": ["x1", "x2"]},
        {"x": "x1", "y": "x2", "conditioning": ["x0"]},
    ]
    assert audit["population_independences"] == audit["graph_implied_independences"]
    assert audit["markov_violations"] == []
    assert audit["extra_independences"] == []
    assert certificate["assumptions_and_results"]["causal_markov_condition"][
        "status"
    ] == "verified"
    faithfulness = certificate["assumptions_and_results"]["ordinary_faithfulness"]
    assert faithfulness["status"] == "verified_exactly"
    assert faithfulness["faithful"] is True
    assert "global Markov" in faithfulness["why_singleton_audit_is_sufficient"]
    assert "decomposition" in faithfulness["why_singleton_audit_is_sufficient"]

    graph = certificate["graph"]
    assert graph["markov_equivalence_class"]["size"] == 3
    assert graph["cpdag"]["directed_edges"] == [
        ["x1", "x3"],
        ["x2", "x3"],
    ]
    assert graph["cpdag"]["undirected_edges"] == [
        ["x0", "x1"],
        ["x0", "x2"],
    ]
    assert graph["cpdag"]["identified_by_this_population_ci_structure"] is True
    assert graph["roles_across_mec"]["invariant"] == {"x3": "sink"}
    assert certificate["mechanisms"]["all_edges_active"] is True
    assert certificate["population"]["full_support"] is True


def test_graph_d_separation_matches_diamond_reference() -> None:
    fixture = load_fixture(default_diamond_spec_path()).fixture
    assert graph_d_separated(fixture, "x1", "x2", ("x0",))
    assert not graph_d_separated(fixture, "x1", "x2", ())
    assert not graph_d_separated(fixture, "x1", "x2", ("x3",))
    assert graph_d_separated(fixture, "x0", "x3", ("x1", "x2"))
    with pytest.raises(ValueError, match="duplicate"):
        graph_d_separated(fixture, "x0", "x3", ("x1", "x1"))


def test_mec_members_are_exactly_the_three_expected_dags() -> None:
    fixture = load_fixture(default_diamond_spec_path()).fixture
    mec = enumerate_markov_equivalence_class(fixture)
    observed = {frozenset(member) for member in mec.members}
    common = {("x1", "x3"), ("x2", "x3")}
    expected = {
        frozenset(common | {("x0", "x1"), ("x0", "x2")}),
        frozenset(common | {("x1", "x0"), ("x0", "x2")}),
        frozenset(common | {("x2", "x0"), ("x0", "x1")}),
    }
    assert observed == expected


def test_mec_enumeration_has_an_explicit_complexity_bound() -> None:
    fixture = load_fixture(default_diamond_spec_path()).fixture
    with pytest.raises(MECEnumerationError, match="configured max_edges"):
        enumerate_markov_equivalence_class(fixture, max_edges=3)


def test_positive_active_noisy_xor_is_not_mistaken_for_faithfulness(
    tmp_path: Path,
) -> None:
    path = tmp_path / "noisy_xor.yaml"
    path.write_text(
        """\
schema_version: 1
id: noisy_xor
variables:
  - {name: x0, states: [0, 1]}
  - {name: x1, states: [0, 1]}
  - {name: y, states: [0, 1]}
graph:
  edges: [[x0, y], [x1, y]]
mechanisms:
  x0:
    parents: []
    cpt: [{when: {}, probabilities: ["1/2", "1/2"]}]
  x1:
    parents: []
    cpt: [{when: {}, probabilities: ["1/2", "1/2"]}]
  y:
    parents: [x0, x1]
    cpt:
      - {when: {x0: 0, x1: 0}, probabilities: ["9/10", "1/10"]}
      - {when: {x0: 0, x1: 1}, probabilities: ["1/10", "9/10"]}
      - {when: {x0: 1, x1: 0}, probabilities: ["1/10", "9/10"]}
      - {when: {x0: 1, x1: 1}, probabilities: ["9/10", "1/10"]}
assumptions:
  causal_sufficiency:
    declared: true
    exogenous_noise: mutually_independent_private_exogenous_noise
  observational_sampling: {regime: observational_iid}
""",
        encoding="utf-8",
    )
    _, certificate = build_certificate(load_fixture(path))

    assert certificate["mechanisms"]["all_edges_active"] is True
    assert certificate["population"]["full_support"] is True
    assert certificate["conditional_independence_audit"]["markov_violations"] == []
    extras = certificate["conditional_independence_audit"]["extra_independences"]
    assert {(item["x"], item["y"], tuple(item["conditioning"])) for item in extras} == {
        ("x0", "y", ()),
        ("x1", "y", ()),
    }
    assert certificate["assumptions_and_results"]["ordinary_faithfulness"][
        "faithful"
    ] is False


def test_inactive_edge_is_reported_separately_from_faithfulness(
    tmp_path: Path,
) -> None:
    path = tmp_path / "inactive_edge.yaml"
    path.write_text(
        """\
schema_version: 1
id: inactive_edge
variables:
  - {name: x, states: [0, 1]}
  - {name: y, states: [0, 1]}
graph: {edges: [[x, y]]}
mechanisms:
  x:
    parents: []
    cpt: [{when: {}, probabilities: ["1/2", "1/2"]}]
  y:
    parents: [x]
    cpt:
      - {when: {x: 0}, probabilities: ["3/5", "2/5"]}
      - {when: {x: 1}, probabilities: ["3/5", "2/5"]}
assumptions:
  causal_sufficiency:
    declared: true
    exogenous_noise: mutually_independent_private_exogenous_noise
  observational_sampling: {regime: observational_iid}
""",
        encoding="utf-8",
    )
    _, certificate = build_certificate(load_fixture(path))
    assert certificate["mechanisms"]["all_edges_active"] is False
    assert certificate["mechanisms"]["edge_activity"] == [
        {"edge": ["x", "y"], "active": False, "witness": None}
    ]
    assert certificate["assumptions_and_results"]["ordinary_faithfulness"][
        "faithful"
    ] is False


def test_exact_ci_audit_supports_nonbinary_finite_variables(tmp_path: Path) -> None:
    path = tmp_path / "ternary_independent_roots.yaml"
    path.write_text(
        """\
schema_version: 1
id: ternary_independent_roots
variables:
  - {name: x, states: [0, 1, 2]}
  - {name: y, states: [low, high]}
graph: {edges: []}
mechanisms:
  x:
    parents: []
    cpt: [{when: {}, probabilities: ["1/6", "1/3", "1/2"]}]
  y:
    parents: []
    cpt: [{when: {}, probabilities: ["2/5", "3/5"]}]
assumptions:
  causal_sufficiency:
    declared: true
    exogenous_noise: mutually_independent_private_exogenous_noise
  observational_sampling: {regime: observational_iid}
""",
        encoding="utf-8",
    )
    population, certificate = build_certificate(load_fixture(path))
    assert len(population.rows) == 6
    assert population.total_probability == 1
    audit = certificate["conditional_independence_audit"]
    assert audit["query_count"] == 1
    assert audit["population_independences"] == [
        {"x": "x", "y": "y", "conditioning": []}
    ]
    assert certificate["assumptions_and_results"]["ordinary_faithfulness"][
        "faithful"
    ] is True


def test_deterministic_and_population_support_and_faithfulness(
    tmp_path: Path,
) -> None:
    loaded = load_fixture(write_root_stochastic_deterministic_and(tmp_path))
    population, certificate = build_certificate(loaded)

    support = {
        row.assignment: row.probability
        for row in population.rows
        if row.probability > 0
    }
    assert support == {
        (0, 0, 0): Fraction(3, 50),
        (0, 1, 0): Fraction(7, 50),
        (1, 0, 0): Fraction(6, 25),
        (1, 1, 1): Fraction(14, 25),
    }
    assert certificate["population"]["support_size"] == 4
    assert certificate["population"]["structural_zero_count"] == 4
    assert certificate["population"]["full_support"] is False
    assert certificate["mechanisms"]["randomness_confined_to_roots"] is True
    assert certificate["mechanisms"]["stochastic_variables"] == ["x0", "x1"]
    assert certificate["mechanisms"]["deterministic_variables"] == ["x2"]
    assert certificate["conditional_independence_audit"][
        "population_independences"
    ] == [{"x": "x0", "y": "x1", "conditioning": []}]
    assert certificate["assumptions_and_results"]["ordinary_faithfulness"][
        "faithful"
    ] is True
    assert certificate["graph"]["markov_equivalence_class"]["size"] == 1
