"""Prolog-free tests for QI-002 minimal truth-table fixtures and config.

Validate complete-factorial construction, the "parent is the unique perfect
separator" property, BK encoding, target exclusion, and config expansion. No
ABA Learning (no swipl/clingo): ``execute_cell_stage2`` stops before Prolog.
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from causal.experiments.config import CellSpec, expand_cells, load_config
from causal.experiments.handcrafted import load_handcrafted, normalize_source
from causal.experiments.handcrafted_qi002 import QI002_ALIASES, QI002_BUILDERS
from causal.experiments.run_grid import execute_cell_stage2

_BINARY_IDS = ("qi002_chain_binary", "qi002_fork_binary", "qi002_collider_binary")
_CAT3_IDS = ("qi002_chain_cat3", "qi002_fork_cat3", "qi002_collider_cat3")
_ALL_IDS = _BINARY_IDS + _CAT3_IDS

_CONFIG_PATH = _REPO_ROOT / "causal/configs/experiments/QI002_minimal_motifs.yaml"


def _expected_parents(source: str) -> set[str]:
    if "chain" in source:
        return {"x1"}
    if "fork" in source:
        return {"x0"}
    if "collider" in source:
        return {"x0", "x1"}
    raise AssertionError(f"unknown motif in source {source!r}")


def _positive_mask(source: str) -> list[bool]:
    fx = load_handcrafted(source)
    threshold = 1 if "binary" in source else 2
    return [int(v) == threshold for v in fx.df["x2"]]


def _cell_for(source: str) -> CellSpec:
    fx = load_handcrafted(source)
    return CellSpec(
        experiment_id="QI002_minimal_motifs",
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


def test_module_registers_six_fixtures() -> None:
    assert len(QI002_BUILDERS) == 6
    assert set(QI002_BUILDERS) == set(_ALL_IDS)
    assert set(QI002_ALIASES) == set(_ALL_IDS)


@pytest.mark.parametrize("source", _ALL_IDS)
def test_all_fixtures_load(source: str) -> None:
    assert load_handcrafted(source).key == source
    assert normalize_source(source) == source


@pytest.mark.parametrize("source", _ALL_IDS)
def test_nodes_target_parents(source: str) -> None:
    fx = load_handcrafted(source)
    assert fx.nodes == 3
    assert fx.default_target == "x2"
    assert set(fx.ground_truth().parents_of("x2")) == _expected_parents(source)


@pytest.mark.parametrize("source", _BINARY_IDS)
def test_binary_row_count_and_full_factorial(source: str) -> None:
    fx = load_handcrafted(source)
    assert len(fx.df) == 8
    combos = list(zip(fx.df["x0"], fx.df["x1"]))
    # All 4 (x0, x1) combinations present, each exactly twice.
    for combo in itertools.product((0, 1), (0, 1)):
        assert combos.count(combo) == 2


@pytest.mark.parametrize("source", _CAT3_IDS)
def test_cat3_row_count_and_full_factorial(source: str) -> None:
    fx = load_handcrafted(source)
    assert len(fx.df) == 18
    combos = list(zip(fx.df["x0"], fx.df["x1"]))
    for combo in itertools.product((0, 1, 2), (0, 1, 2)):
        assert combos.count(combo) == 2


@pytest.mark.parametrize("source", _ALL_IDS)
def test_parent_is_unique_perfect_separator(source: str) -> None:
    """The true parent(s) perfectly separate positives; non-parents do not.

    A single non-parent column must fail to separate (proving the parent is the
    unique perfect single-column rule); collider needs both parents so neither
    single column separates.
    """
    fx = load_handcrafted(source)
    pos = _positive_mask(source)
    parents = _expected_parents(source)

    def column_separates(col: str) -> bool:
        # A column "separates" if its value-set partitions pos vs neg perfectly:
        # no value appears in both a positive and a negative row.
        by_value: dict[int, set[bool]] = {}
        for val, is_pos in zip(fx.df[col], pos):
            by_value.setdefault(int(val), set()).add(is_pos)
        return all(len(labels) == 1 for labels in by_value.values())

    if parents == {"x0", "x1"}:
        # collider: neither single column perfectly separates.
        assert not column_separates("x0")
        assert not column_separates("x1")
    else:
        parent = next(iter(parents))
        non_parent = "x1" if parent == "x0" else "x0"
        assert column_separates(parent)
        assert not column_separates(non_parent)


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


@pytest.mark.parametrize("source", _CAT3_IDS)
def test_cat3_fixtures_emit_val_predicates(source: str, tmp_path: Path) -> None:
    text = _bk_text(source, tmp_path)
    assert "x0_val_" in text
    assert "x1_val_" in text
    assert "x0_bin" not in text


@pytest.mark.parametrize("source", _ALL_IDS)
def test_target_x2_excluded_from_bk(source: str, tmp_path: Path) -> None:
    text = _bk_text(source, tmp_path)
    assert "Skipping excluded variable: x2" in text
    assert "x2(A) :-" not in text
    assert "x2_val_" not in text


def test_config_expands_to_six_cells_all_x2() -> None:
    cfg = load_config(_CONFIG_PATH)
    cells = expand_cells(cfg, config_path=_CONFIG_PATH)
    assert len(cells) == 6
    assert all(c.target == "x2" for c in cells)
    assert {c.dgp for c in cells} == set(_ALL_IDS)
