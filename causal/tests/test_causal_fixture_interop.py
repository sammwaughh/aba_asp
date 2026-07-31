from __future__ import annotations

from pathlib import Path

from causal.fixtures.interop import (
    bif_text,
    export_bif,
    to_pgmpy_model,
    validate_bif_text,
)
from causal.fixtures.io import default_diamond_spec_path, load_fixture
from causal.tests.fixture_test_utils import write_root_stochastic_deterministic_and


def test_diamond_pgmpy_and_bif_round_trip(tmp_path: Path) -> None:
    fixture = load_fixture(default_diamond_spec_path()).fixture
    model = to_pgmpy_model(fixture)
    assert model.check_model()
    assert set(model.nodes()) == set(fixture.variable_names)
    assert set(model.edges()) == set(fixture.edges)

    text_report = validate_bif_text(fixture, bif_text(fixture))
    assert text_report.ok
    assert text_report.max_absolute_probability_error <= 1e-12

    path = tmp_path / "diamond.bif"
    file_report = export_bif(fixture, path)
    assert path.is_file()
    assert file_report.ok
    assert "network m13_bucket3_binary_diamond" in path.read_text(encoding="utf-8")


def test_asymmetric_cpt_preserves_parent_and_configuration_order(tmp_path: Path) -> None:
    spec = tmp_path / "asymmetric.yaml"
    spec.write_text(
        """\
schema_version: 1
id: asymmetric_parent_order
variables:
  - {name: a, states: [0, 1]}
  - {name: b, states: [0, 1]}
  - {name: c, states: [0, 1]}
graph:
  edges: [[a, c], [b, c]]
mechanisms:
  a:
    parents: []
    cpt: [{when: {}, probabilities: ["1/2", "1/2"]}]
  b:
    parents: []
    cpt: [{when: {}, probabilities: ["1/2", "1/2"]}]
  c:
    parents: [a, b]
    cpt:
      - {when: {a: 0, b: 0}, probabilities: ["9/10", "1/10"]}
      - {when: {a: 0, b: 1}, probabilities: ["4/5", "1/5"]}
      - {when: {a: 1, b: 0}, probabilities: ["7/10", "3/10"]}
      - {when: {a: 1, b: 1}, probabilities: ["3/5", "2/5"]}
assumptions:
  causal_sufficiency:
    declared: true
    exogenous_noise: mutually_independent_private_exogenous_noise
  observational_sampling: {regime: observational_iid}
""",
        encoding="utf-8",
    )
    fixture = load_fixture(spec).fixture
    model = to_pgmpy_model(fixture)
    cpd = model.get_cpds("c")
    assert tuple(cpd.variables[1:]) == ("a", "b")
    assert cpd.get_value(c="1", a="0", b="1") == 0.2
    assert cpd.get_value(c="1", a="1", b="0") == 0.3

    report = export_bif(fixture, tmp_path / "asymmetric.bif")
    assert report.ok


def test_isolated_variables_survive_bif_export(tmp_path: Path) -> None:
    spec = tmp_path / "isolated.yaml"
    spec.write_text(
        """\
schema_version: 1
id: isolated_roots
variables:
  - {name: a, states: [0, 1]}
  - {name: b, states: [0, 1]}
graph: {edges: []}
mechanisms:
  a:
    parents: []
    cpt: [{when: {}, probabilities: ["1/2", "1/2"]}]
  b:
    parents: []
    cpt: [{when: {}, probabilities: ["1/4", "3/4"]}]
assumptions:
  causal_sufficiency:
    declared: true
    exogenous_noise: mutually_independent_private_exogenous_noise
  observational_sampling: {regime: observational_iid}
""",
        encoding="utf-8",
    )
    fixture = load_fixture(spec).fixture
    model = to_pgmpy_model(fixture)
    assert set(model.nodes()) == {"a", "b"}
    assert not model.edges()
    assert export_bif(fixture, tmp_path / "isolated.bif").ok


def test_zero_one_deterministic_cpt_survives_bif_round_trip(tmp_path: Path) -> None:
    fixture = load_fixture(write_root_stochastic_deterministic_and(tmp_path)).fixture
    model = to_pgmpy_model(fixture)
    cpd = model.get_cpds("x2")

    assert cpd.get_value(x2="0", x0="1", x1="1") == 0.0
    assert cpd.get_value(x2="1", x0="1", x1="1") == 1.0
    assert cpd.get_value(x2="0", x0="1", x1="0") == 1.0
    assert export_bif(fixture, tmp_path / "deterministic_and.bif").ok
