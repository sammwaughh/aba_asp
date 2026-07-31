from __future__ import annotations

from pathlib import Path

import pandas as pd

from causal.fixtures.analysis import derive_population
from causal.fixtures.io import load_fixture
from causal.fixtures.reference import build_mechanism_reference
from causal.tests.fixture_test_utils import write_root_stochastic_deterministic_and


def _target(document, name: str):
    return next(target for target in document["targets"] if target["target"] == name)


def test_reference_separates_roots_truth_table_population_and_sample(
    tmp_path: Path,
) -> None:
    loaded = load_fixture(write_root_stochastic_deterministic_and(tmp_path))
    population = derive_population(loaded.fixture)
    sample = pd.DataFrame(
        {
            "a": [0, 0, 1],
            "b": [0, 1, 0],
            "c": [0, 0, 0],
        }
    )
    document = build_mechanism_reference(
        loaded, population, sample=sample, sample_name="manual_n3"
    )

    assert document["sample"] == {"available": True, "name": "manual_n3", "n": 3}
    assert document["encoding_reference"]["compatible"] is True

    root = _target(document, "a")
    assert root["reference_status"] == "no_observed_parent_deterministic_rule"
    assert root["canonical_positive_rules"]["formal"] == []
    assert root["root_distribution"] == [
        {"state": 0, "probability": "1/5"},
        {"state": 1, "probability": "4/5"},
    ]

    child = _target(document, "c")
    rule = "c(A) :- a_val_1(A), b_val_1(A)."
    assert child["reference_status"] == "available"
    assert len(child["deterministic_truth_table"]) == 4
    assert child["canonical_positive_rules"]["formal"] == [rule]
    assert child["canonical_positive_rules"]["population_supported"] == [rule]
    assert child["canonical_positive_rules"]["sample_observed"] == []


def test_reference_marks_formal_parent_configurations_outside_population_support(
    tmp_path: Path,
) -> None:
    path = tmp_path / "deterministic_redundant_parents.yaml"
    path.write_text(
        """\
schema_version: 2
id: test_deterministic_redundant_parents
variables:
  - {name: a, states: [0, 1]}
  - {name: b, states: [0, 1]}
  - {name: c, states: [0, 1]}
graph:
  edges: [[a, b], [a, c], [b, c]]
mechanisms:
  a:
    parents: []
    cpt: [{when: {}, probabilities: ["1/2", "1/2"]}]
  b:
    parents: [a]
    cpt:
      - {when: {a: 0}, probabilities: [1, 0]}
      - {when: {a: 1}, probabilities: [0, 1]}
  c:
    parents: [a, b]
    cpt:
      - {when: {a: 0, b: 0}, probabilities: [1, 0]}
      - {when: {a: 0, b: 1}, probabilities: [1, 0]}
      - {when: {a: 1, b: 0}, probabilities: [1, 0]}
      - {when: {a: 1, b: 1}, probabilities: [0, 1]}
assumptions:
  mechanism_regime: root_stochastic_deterministic_nonroots
  causal_sufficiency:
    declared: true
    exogenous_noise: mutually_independent_root_exogenous_noise
  observational_sampling: {regime: observational_iid}
""",
        encoding="utf-8",
    )
    loaded = load_fixture(path)
    document = build_mechanism_reference(loaded, derive_population(loaded.fixture))
    child = _target(document, "c")
    table = {tuple(row["when"].values()): row for row in child["deterministic_truth_table"]}

    assert table[(0, 0)]["population_supported"] is True
    assert table[(1, 1)]["population_supported"] is True
    assert table[(0, 1)]["population_supported"] is False
    assert table[(1, 0)]["population_supported"] is False
