"""Prolog-free tests for QI-001 handcrafted fixtures and config.

These tests validate controlled data generation, BK encoding, target exclusion,
and config expansion only. They do NOT run ABA Learning (no swipl/clingo):
``execute_cell_stage2`` performs BK generation + example building but stops
before the Prolog stage.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from causal.experiments.config import CellSpec, expand_cells, load_config
from causal.experiments.handcrafted import load_handcrafted, normalize_source
from causal.experiments.handcrafted_qi001 import QI001_ALIASES, QI001_BUILDERS
from causal.experiments.run_grid import execute_cell_stage2

_BINARY_IDS = ("qi001_chain_binary", "qi001_fork_binary", "qi001_collider_binary")
_CAT3_IDS = ("qi001_chain_cat3", "qi001_fork_cat3", "qi001_collider_cat3")
_CONT3_IDS = ("qi001_chain_cont3", "qi001_fork_cont3", "qi001_collider_cont3")
_ALL_IDS = _BINARY_IDS + _CAT3_IDS + _CONT3_IDS

_CONFIG_PATH = _REPO_ROOT / "causal/configs/experiments/QI001_motifs_modes.yaml"


def _expected_parents(source: str) -> set[str]:
    if "chain" in source:
        return {"x1"}
    if "fork" in source:
        return {"x0"}
    if "collider" in source:
        return {"x0", "x1"}
    raise AssertionError(f"unknown motif in source {source!r}")


def _cell_for(source: str) -> CellSpec:
    fx = load_handcrafted(source)
    return CellSpec(
        experiment_id="QI001_motifs_modes",
        dgp=source,
        nodes=fx.nodes,
        edges=fx.edges,
        n=len(fx.df),
        seed=0,
        target="x2",
        config_hash="sha256:test",
        run_id=f"run_{source}",
        graph_type="handcrafted_table",
        example_split="handcrafted",
        handcrafted_source=source,
    )


def _bk_text(source: str, tmp_path: Path) -> str:
    cell = _cell_for(source)
    out = execute_cell_stage2(
        cell,
        tmp_path / source,
        graph_type="handcrafted_table",
        bins=3,
        bin_strategy="uniform",
        example_split="handcrafted",
    )
    assert out.outcome == "ok", f"{source} stage2 outcome={out.outcome}"
    assert out.bk_path is not None and out.bk_path.is_file()
    return out.bk_path.read_text(encoding="utf-8")


def test_qi001_module_registers_nine_fixtures() -> None:
    assert len(QI001_BUILDERS) == 9
    assert set(QI001_BUILDERS) == set(_ALL_IDS)
    assert set(QI001_ALIASES) == set(_ALL_IDS)


@pytest.mark.parametrize("source", _ALL_IDS)
def test_all_fixtures_load(source: str) -> None:
    fx = load_handcrafted(source)
    assert fx.key == source


@pytest.mark.parametrize("source", _ALL_IDS)
def test_aliases_normalise(source: str) -> None:
    assert normalize_source(source) == source


@pytest.mark.parametrize("source", _ALL_IDS)
def test_default_target_is_x2(source: str) -> None:
    assert load_handcrafted(source).default_target == "x2"


@pytest.mark.parametrize("source", _ALL_IDS)
def test_nodes_is_three(source: str) -> None:
    assert load_handcrafted(source).nodes == 3


@pytest.mark.parametrize("source", _ALL_IDS)
def test_true_parent_sets(source: str) -> None:
    parents = load_handcrafted(source).ground_truth().parents_of("x2")
    assert set(parents) == _expected_parents(source)


@pytest.mark.parametrize("source", _ALL_IDS)
def test_examples_non_empty(source: str) -> None:
    fx = load_handcrafted(source)
    assert len(fx.pos_examples) > 0
    assert len(fx.neg_examples) > 0
    for atom in fx.pos_examples + fx.neg_examples:
        assert atom.startswith("x2(")


@pytest.mark.parametrize("source", _ALL_IDS)
def test_no_fixture_uses_binary_var_type(source: str) -> None:
    assert "binary" not in load_handcrafted(source).var_types.values()


@pytest.mark.parametrize("source", _BINARY_IDS)
def test_binary_fixtures_emit_bare_predicates(source: str, tmp_path: Path) -> None:
    text = _bk_text(source, tmp_path)
    assert "x0(A) :-" in text
    assert "x1(A) :-" in text
    assert "x0_val_" not in text
    assert "x1_val_" not in text
    assert "x0_bin" not in text
    assert "x1_bin" not in text


@pytest.mark.parametrize("source", _CAT3_IDS)
def test_cat3_fixtures_emit_val_predicates(source: str, tmp_path: Path) -> None:
    text = _bk_text(source, tmp_path)
    assert "x0_val_" in text
    assert "x1_val_" in text
    # No bare or binned predicates for the non-target columns.
    assert "x0_bin" not in text
    assert "x1_bin" not in text


@pytest.mark.parametrize("source", _CONT3_IDS)
def test_cont3_fixtures_emit_bin_predicates(source: str, tmp_path: Path) -> None:
    text = _bk_text(source, tmp_path)
    assert "x0_bin" in text
    assert "x1_bin" in text
    assert "bins=3, strategy=uniform" in text


@pytest.mark.parametrize("source", _ALL_IDS)
def test_target_x2_excluded_from_bk(source: str, tmp_path: Path) -> None:
    text = _bk_text(source, tmp_path)
    assert "Skipping excluded variable: x2" in text
    assert "x2(A) :-" not in text
    assert "x2_val_" not in text
    assert "x2_bin" not in text


def test_config_expands_to_nine_cells_all_x2() -> None:
    cfg = load_config(_CONFIG_PATH)
    cells = expand_cells(cfg, config_path=_CONFIG_PATH)
    assert len(cells) == 9
    assert all(c.target == "x2" for c in cells)
    assert {c.dgp for c in cells} == set(_ALL_IDS)
