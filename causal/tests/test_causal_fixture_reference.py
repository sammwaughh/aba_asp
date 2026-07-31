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
            "x0": [0, 0, 1],
            "x1": [0, 1, 0],
            "x2": [0, 0, 0],
        }
    )
    document = build_mechanism_reference(
        loaded, population, sample=sample, sample_name="manual_n3"
    )

    assert document["sample"] == {"available": True, "name": "manual_n3", "n": 3}
    assert document["encoding_reference"]["compatible"] is True

    root = _target(document, "x0")
    assert root["reference_status"] == "no_observed_parent_deterministic_rule"
    assert root["canonical_positive_rules"]["formal"] == []
    assert root["root_distribution"] == [
        {"state": 0, "probability": "1/5"},
        {"state": 1, "probability": "4/5"},
    ]

    child = _target(document, "x2")
    rule = "x2(A) :- x0_val_1(A), x1_val_1(A)."
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
  - {name: x0, states: [0, 1]}
  - {name: x1, states: [0, 1]}
  - {name: x2, states: [0, 1]}
graph:
  edges: [[x0, x1], [x0, x2], [x1, x2]]
mechanisms:
  x0:
    parents: []
    cpt: [{when: {}, probabilities: ["1/2", "1/2"]}]
  x1:
    parents: [x0]
    cpt:
      - {when: {x0: 0}, probabilities: [1, 0]}
      - {when: {x0: 1}, probabilities: [0, 1]}
  x2:
    parents: [x0, x1]
    cpt:
      - {when: {x0: 0, x1: 0}, probabilities: [1, 0]}
      - {when: {x0: 0, x1: 1}, probabilities: [1, 0]}
      - {when: {x0: 1, x1: 0}, probabilities: [1, 0]}
      - {when: {x0: 1, x1: 1}, probabilities: [0, 1]}
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
    child = _target(document, "x2")
    table = {tuple(row["when"].values()): row for row in child["deterministic_truth_table"]}

    assert table[(0, 0)]["population_supported"] is True
    assert table[(1, 1)]["population_supported"] is True
    assert table[(0, 1)]["population_supported"] is False
    assert table[(1, 0)]["population_supported"] is False
