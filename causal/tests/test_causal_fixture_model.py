from __future__ import annotations

from fractions import Fraction
from dataclasses import replace
from pathlib import Path

import pytest
import yaml

from causal.fixtures.io import default_diamond_spec_path, load_fixture
from causal.fixtures.model import FixtureValidationError
from causal.tests.fixture_test_utils import write_root_stochastic_deterministic_and


def _mutated_spec(tmp_path: Path, mutate) -> Path:
    raw = yaml.safe_load(default_diamond_spec_path().read_text(encoding="utf-8"))
    mutate(raw)
    path = tmp_path / "fixture.yaml"
    path.write_text(yaml.safe_dump(raw, sort_keys=False), encoding="utf-8")
    return path


def test_loads_approved_binary_diamond_exactly() -> None:
    loaded = load_fixture(default_diamond_spec_path())
    fixture = loaded.fixture

    assert fixture.fixture_id == "m13_bucket3_binary_diamond"
    assert fixture.variable_names == ("x0", "x1", "x2", "x3")
    assert fixture.topological_order == ("x0", "x1", "x2", "x3")
    assert fixture.edges == (
        ("x0", "x1"),
        ("x0", "x2"),
        ("x1", "x3"),
        ("x2", "x3"),
    )
    assert fixture.parents_of("x3") == ("x1", "x2")
    assert fixture.conditional_distribution("x3", {"x1": 1, "x2": 0}) == (
        Fraction(7, 20),
        Fraction(13, 20),
    )
    assert loaded.source_hash.startswith("sha256:")
    assert loaded.document_hash.startswith("sha256:")
    assert loaded.semantic_hash == (
        "sha256:6650750a67109c41e3458bfde52b38634e905ee6d24b3ff6e5bc3e9b818ee299"
    )


def test_yaml_floats_are_rejected_to_preserve_exactness(tmp_path: Path) -> None:
    path = _mutated_spec(
        tmp_path,
        lambda raw: raw["mechanisms"]["x0"]["cpt"][0].update(
            {"probabilities": [0.5, 0.5]}
        ),
    )
    with pytest.raises(FixtureValidationError, match="not a float"):
        load_fixture(path)


def test_cpt_must_cover_every_parent_assignment(tmp_path: Path) -> None:
    path = _mutated_spec(
        tmp_path,
        lambda raw: raw["mechanisms"]["x3"]["cpt"].pop(),
    )
    with pytest.raises(FixtureValidationError, match="cover every parent assignment"):
        load_fixture(path)


def test_parent_order_is_canonical_and_explicit(tmp_path: Path) -> None:
    path = _mutated_spec(
        tmp_path,
        lambda raw: raw["mechanisms"]["x3"].update({"parents": ["x2", "x1"]}),
    )
    with pytest.raises(FixtureValidationError, match="declared variable order"):
        load_fixture(path)


def test_graph_must_be_acyclic(tmp_path: Path) -> None:
    path = _mutated_spec(
        tmp_path,
        lambda raw: raw["graph"]["edges"].append(["x3", "x0"]),
    )
    with pytest.raises(FixtureValidationError, match="acyclic"):
        load_fixture(path)


def test_semantic_hash_ignores_descriptive_metadata(tmp_path: Path) -> None:
    original = load_fixture(default_diamond_spec_path())

    def mutate(raw) -> None:
        raw["title"] = "A different descriptive title"
        raw["metadata"]["note"] = "not part of the scientific model"

    changed = load_fixture(_mutated_spec(tmp_path, mutate))
    assert changed.source_hash != original.source_hash
    assert changed.document_hash != original.document_hash
    assert changed.semantic_hash == original.semantic_hash


def test_source_hash_tracks_bytes_but_document_hash_ignores_formatting(
    tmp_path: Path,
) -> None:
    original = load_fixture(default_diamond_spec_path())
    path = tmp_path / "fixture.yaml"
    path.write_text(
        "# formatting-only comment\n"
        + default_diamond_spec_path().read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    reformatted = load_fixture(path)
    assert reformatted.source_hash != original.source_hash
    assert reformatted.document_hash == original.document_hash
    assert reformatted.semantic_hash == original.semantic_hash


def test_direct_model_construction_cannot_bypass_exact_fraction_invariant() -> None:
    fixture = load_fixture(default_diamond_spec_path()).fixture
    root = fixture.mechanism_for("x0")
    float_root = replace(
        root,
        rows=(replace(root.rows[0], probabilities=(0.5, 0.5)),),
    )
    mechanisms = tuple(
        float_root if mechanism.variable == "x0" else mechanism
        for mechanism in fixture.mechanisms
    )
    with pytest.raises(FixtureValidationError, match="fractions.Fraction"):
        replace(fixture, mechanisms=mechanisms)


def test_mixed_state_types_are_rejected_for_type_safe_csv_round_trips(
    tmp_path: Path,
) -> None:
    path = _mutated_spec(
        tmp_path,
        lambda raw: raw["variables"][0].update({"states": [0, "one"]}),
    )
    with pytest.raises(FixtureValidationError, match="homogeneous type"):
        load_fixture(path)


def test_schema2_accepts_stochastic_roots_and_deterministic_nonroots(
    tmp_path: Path,
) -> None:
    loaded = load_fixture(write_root_stochastic_deterministic_and(tmp_path))
    fixture = loaded.fixture

    assert fixture.schema_version == 2
    assert (
        fixture.assumptions.mechanism_regime
        == "root_stochastic_deterministic_nonroots"
    )
    assert fixture.root_names == ("a", "b")
    assert fixture.stochastic_variables == ("a", "b")
    assert fixture.deterministic_variables == ("c",)


def test_schema1_remains_strictly_positive(tmp_path: Path) -> None:
    path = _mutated_spec(
        tmp_path,
        lambda raw: raw["mechanisms"]["x0"]["cpt"][0].update(
            {"probabilities": [1, 0]}
        ),
    )
    with pytest.raises(FixtureValidationError, match="strictly positive"):
        load_fixture(path)


def test_schema2_requires_explicit_mechanism_regime(tmp_path: Path) -> None:
    path = write_root_stochastic_deterministic_and(tmp_path)
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    del raw["assumptions"]["mechanism_regime"]
    path.write_text(yaml.safe_dump(raw, sort_keys=False), encoding="utf-8")

    with pytest.raises(FixtureValidationError, match="mechanism_regime"):
        load_fixture(path)


def test_schema2_rejects_degenerate_roots(tmp_path: Path) -> None:
    path = write_root_stochastic_deterministic_and(tmp_path)
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    raw["mechanisms"]["a"]["cpt"][0]["probabilities"] = [0, 1]
    path.write_text(yaml.safe_dump(raw, sort_keys=False), encoding="utf-8")

    with pytest.raises(FixtureValidationError, match="root mechanism.*strictly positive"):
        load_fixture(path)


def test_schema2_rejects_stochastic_nonroot_mechanisms(tmp_path: Path) -> None:
    path = write_root_stochastic_deterministic_and(tmp_path)
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    raw["mechanisms"]["c"]["cpt"][0]["probabilities"] = ["1/2", "1/2"]
    path.write_text(yaml.safe_dump(raw, sort_keys=False), encoding="utf-8")

    with pytest.raises(FixtureValidationError, match="c must be deterministic"):
        load_fixture(path)


def test_schema2_rejects_negative_probabilities(tmp_path: Path) -> None:
    path = write_root_stochastic_deterministic_and(tmp_path)
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    raw["mechanisms"]["c"]["cpt"][0]["probabilities"] = [-1, 2]
    path.write_text(yaml.safe_dump(raw, sort_keys=False), encoding="utf-8")

    with pytest.raises(FixtureValidationError, match="non-negative"):
        load_fixture(path)
