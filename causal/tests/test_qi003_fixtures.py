"""Prolog-free tests for QI-003 scaled noisy fixtures and config.

Validate n=100 generation, parent-position controls (the true parent sits in the
asserted column), chain non-collinearity, populated continuous bins, BK encoding,
target exclusion, and config expansion. No ABA Learning (no swipl/clingo).
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from causal.experiments.config import CellSpec, expand_cells, load_config
from causal.experiments.handcrafted import load_handcrafted, normalize_source
from causal.experiments.handcrafted_qi003 import QI003_ALIASES, QI003_BUILDERS
from causal.experiments.run_grid import execute_cell_stage2
from aba_asp.utils.data_utils import bin_continuous_variable

_CHAIN_IDS = ("qi003_chain_x1parent", "qi003_chain_x0parent")
_FORK_IDS = ("qi003_fork_x0parent", "qi003_fork_x1parent")
_COLLIDER_IDS = ("qi003_collider",)
_MODES = ("binary", "cat3", "cont3")

_ALL_IDS = tuple(
    f"{base}_{mode}"
    for base in (_CHAIN_IDS + _FORK_IDS + _COLLIDER_IDS)
    for mode in _MODES
)
_CONT3_IDS = tuple(s for s in _ALL_IDS if s.endswith("cont3"))
_BINARY_IDS = tuple(s for s in _ALL_IDS if s.endswith("binary"))
_CAT3_IDS = tuple(s for s in _ALL_IDS if s.endswith("cat3"))

_CONFIG_PATH = _REPO_ROOT / "causal/configs/experiments/QI003_scaled_motifs.yaml"


def _expected_parents(source: str) -> set[str]:
    if "chain_x1parent" in source:
        return {"x1"}
    if "chain_x0parent" in source:
        return {"x0"}
    if "fork_x0parent" in source:
        return {"x0"}
    if "fork_x1parent" in source:
        return {"x1"}
    if "collider" in source:
        return {"x0", "x1"}
    raise AssertionError(f"unknown structural config in source {source!r}")


def _cell_for(source: str) -> CellSpec:
    fx = load_handcrafted(source)
    return CellSpec(
        experiment_id="QI003_scaled_motifs",
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


def test_module_registers_fifteen_fixtures() -> None:
    assert len(QI003_BUILDERS) == 15
    assert set(QI003_BUILDERS) == set(_ALL_IDS)
    assert set(QI003_ALIASES) == set(_ALL_IDS)


@pytest.mark.parametrize("source", _ALL_IDS)
def test_all_fixtures_load(source: str) -> None:
    assert load_handcrafted(source).key == source
    assert normalize_source(source) == source


@pytest.mark.parametrize("source", _ALL_IDS)
def test_hundred_rows_nodes_target(source: str) -> None:
    fx = load_handcrafted(source)
    assert len(fx.df) == 100
    assert fx.nodes == 3
    assert fx.default_target == "x2"


@pytest.mark.parametrize("source", _ALL_IDS)
def test_parent_in_asserted_column(source: str) -> None:
    parents = load_handcrafted(source).ground_truth().parents_of("x2")
    assert set(parents) == _expected_parents(source)


@pytest.mark.parametrize("source", _ALL_IDS)
def test_examples_non_empty_both_classes(source: str) -> None:
    fx = load_handcrafted(source)
    assert len(fx.pos_examples) > 0
    assert len(fx.neg_examples) > 0
    for atom in fx.pos_examples + fx.neg_examples:
        assert atom.startswith("x2(")


@pytest.mark.parametrize("source", [s for s in _ALL_IDS if "chain" in s])
def test_chain_parent_not_collinear_with_ancestor(source: str) -> None:
    """In a chain, the parent (intermediate) must NOT equal its ancestor (root),
    otherwise parent vs ancestor is undecidable (the QI-001 cont3 degeneracy)."""
    fx = load_handcrafted(source)
    parent = next(iter(_expected_parents(source)))
    ancestor = "x1" if parent == "x0" else "x0"
    p = fx.df[parent].to_numpy()
    a = fx.df[ancestor].to_numpy()
    assert not np.array_equal(p, a)
    if fx.var_types[parent] == "continuous":
        assert abs(float(np.corrcoef(p, a)[0, 1])) < 0.99
    else:
        disagree = float(np.mean(p != a))
        assert disagree > 0.05


@pytest.mark.parametrize("source", _CONT3_IDS)
def test_continuous_bins_populated(source: str) -> None:
    fx = load_handcrafted(source)
    for col in ("x0", "x1"):
        binned, _ = bin_continuous_variable(fx.df[col].to_numpy(), 3, "uniform")
        counts = Counter(binned.tolist())
        for b in (0, 1, 2):
            assert counts.get(b, 0) >= 1, f"{source} {col} bin {b} empty"


@pytest.mark.parametrize("source", _BINARY_IDS)
def test_binary_fixtures_emit_bare_predicates(source: str, tmp_path: Path) -> None:
    text = _bk_text(source, tmp_path)
    assert "x0(A) :-" in text
    assert "x1(A) :-" in text
    assert "x0_val_" not in text
    assert "x0_bin" not in text


@pytest.mark.parametrize("source", _CAT3_IDS)
def test_cat3_fixtures_emit_val_predicates(source: str, tmp_path: Path) -> None:
    text = _bk_text(source, tmp_path)
    assert "x0_val_" in text
    assert "x1_val_" in text
    assert "x0_bin" not in text


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


def test_config_expands_to_fifteen_cells_all_x2() -> None:
    cfg = load_config(_CONFIG_PATH)
    cells = expand_cells(cfg, config_path=_CONFIG_PATH)
    assert len(cells) == 15
    assert all(c.target == "x2" for c in cells)
    assert {c.dgp for c in cells} == set(_ALL_IDS)
