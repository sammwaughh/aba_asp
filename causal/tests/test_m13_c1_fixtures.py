"""Stage-0 invariants for M13-C1 causal-role underdetermination."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from causal.experiments.config import CellSpec, expand_cells, load_config
from causal.experiments.handcrafted import load_handcrafted
from causal.experiments.handcrafted_m13 import M13_BUILDERS
from causal.experiments.run_grid import execute_cell_stage2

_SOURCES: tuple[str, str] = ("m13_c1_parent_x0", "m13_c1_parent_x1")
_EXPECTED_TABLE = pd.DataFrame(
    {
        "x0": [0, 1, 2],
        "x1": [0, 1, 2],
        "x2": [0, 1, 2],
    }
)
_CONFIG_DIR = Path(__file__).resolve().parents[1] / "configs" / "experiments"
_CONFIGS = (
    _CONFIG_DIR / "M13_c1_role_equivalence_ecai2024.yaml",
    _CONFIG_DIR / "M13_c1_role_equivalence_aamas2025.yaml",
)


def _fixture(source: str):
    return load_handcrafted(source)


def _cell(source: str) -> CellSpec:
    fx = _fixture(source)
    return CellSpec(
        experiment_id="M13_c1_stage0",
        dgp=source,
        nodes=fx.nodes,
        edges=fx.edges,
        n=len(fx.df),
        seed=None,
        target="x2",
        config_hash="sha256:test",
        run_id=f"run_{source}",
        cell_dir_name=source,
        graph_type="handcrafted_table",
        example_split="handcrafted",
        handcrafted_source=source,
    )


def test_registry_contains_both_c1_models() -> None:
    assert set(M13_BUILDERS) == set(_SOURCES)
    for source in _SOURCES:
        assert _fixture(source).key == source


@pytest.mark.parametrize("source", _SOURCES)
def test_shared_table_and_examples(source: str) -> None:
    fx = _fixture(source)
    pd.testing.assert_frame_equal(fx.df, _EXPECTED_TABLE)
    assert tuple(fx.df.columns) == ("x0", "x1", "x2")
    assert fx.resolved_learning_targets() == ("x2",)
    assert fx.examples_for_target("x2") == (
        ("x2(2)", "x2(3)"),
        ("x2(1)",),
    )


def test_models_reverse_parent_and_sibling_roles() -> None:
    g0 = _fixture("m13_c1_parent_x0")
    g1 = _fixture("m13_c1_parent_x1")

    assert g0.edges == ((0, 1), (0, 2))
    assert g1.edges == ((1, 0), (1, 2))
    assert g0.ground_truth().parents_of("x2") == frozenset({"x0"})
    assert g1.ground_truth().parents_of("x2") == frozenset({"x1"})

    # Both causal interpretations generate the same observational table.
    assert (g0.df["x1"] == g0.df["x0"]).all()
    assert (g0.df["x2"] == g0.df["x0"]).all()
    assert (g1.df["x0"] == g1.df["x1"]).all()
    assert (g1.df["x2"] == g1.df["x1"]).all()


def test_stage2_learner_inputs_are_identical(tmp_path: Path) -> None:
    artefacts = {}
    for source in _SOURCES:
        out = execute_cell_stage2(
            _cell(source),
            tmp_path / source,
            graph_type="handcrafted_table",
            bins=3,
            bin_strategy="uniform",
            example_split="handcrafted",
        )
        assert out.outcome == "ok", (out.outcome, out.failure_reason)
        assert out.bk_path is not None
        artefacts[source] = out

    g0 = artefacts["m13_c1_parent_x0"]
    g1 = artefacts["m13_c1_parent_x1"]
    assert g0.data_path.read_bytes() == g1.data_path.read_bytes()
    assert g0.bk_path is not None and g1.bk_path is not None
    assert g0.bk_path.read_bytes() == g1.bk_path.read_bytes()
    assert g0.pos_examples == g1.pos_examples == ("x2(2)", "x2(3)")
    assert g0.neg_examples == g1.neg_examples == ("x2(1)",)

    bk = g0.bk_path.read_text(encoding="utf-8")
    assert bk.index("Feature predicates for variable: x0") < bk.index(
        "Feature predicates for variable: x1"
    )
    assert "x0_val_" in bk
    assert "x1_val_" in bk
    assert "x2_val_" not in bk
    assert "Skipping excluded variable: x2" in bk


@pytest.mark.parametrize("config_path", _CONFIGS)
def test_configs_expand_to_the_input_equivalent_pair(config_path: Path) -> None:
    cfg = load_config(config_path)
    cells = expand_cells(cfg, config_path=config_path)
    assert len(cells) == 2
    assert [cell.dgp for cell in cells] == list(_SOURCES)
    assert [cell.handcrafted_source for cell in cells] == list(_SOURCES)
    assert [cell.target for cell in cells] == ["x2", "x2"]
    assert [cell.edges for cell in cells] == [
        ((0, 1), (0, 2)),
        ((1, 0), (1, 2)),
    ]
