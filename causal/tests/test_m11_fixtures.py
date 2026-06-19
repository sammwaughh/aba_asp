"""Prolog-free Stage-0 validation for the m1.1 parent-position fixtures.

Validates the eight metamorphic chain fixtures (2 encodings x cells A/B/C/D)
described in ``docs/research/milestone_plans/milestone1_part1_parent_position.md``
before any ABA Learning run. No swipl/clingo: ``execute_cell_stage2`` stops
before Prolog, so BK-dependent checks use the actually generated ``bk.aba``.
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
from causal.experiments.handcrafted_m11 import (
    M11_ALIASES,
    M11_BUILDERS,
    M11_CELLS,
    M11_META_BY_KEY,
    bk_predictor_order,
    is_pi_pair,
    is_sigma_pair,
    predictor_columns,
    structural_checks,
)
from causal.experiments.run_grid import execute_cell_stage2

_BINARY_IDS = ("m11_binary_A", "m11_binary_B", "m11_binary_C", "m11_binary_D")
_CAT3_IDS = ("m11_cat3_A", "m11_cat3_B", "m11_cat3_C", "m11_cat3_D")
_ALL_IDS = _BINARY_IDS + _CAT3_IDS

_CONFIG_PATH = _REPO_ROOT / "causal/configs/experiments/M11_parent_position.yaml"


def _cell_for(source: str) -> CellSpec:
    fx = load_handcrafted(source)
    return CellSpec(
        experiment_id="M11_parent_position",
        dgp=source,
        nodes=fx.nodes,
        edges=fx.edges,
        n=len(fx.df),
        seed=0,
        target="x2",
        config_hash="sha256:test",
        run_id=f"run_{source}",
        cell_dir_name=f"run_{source}",
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


# --- Registration / loading -------------------------------------------------


def test_module_registers_eight_fixtures() -> None:
    assert len(M11_BUILDERS) == 8
    assert set(M11_BUILDERS) == set(_ALL_IDS)
    assert set(M11_ALIASES) == set(_ALL_IDS)
    assert {m.key for m in M11_CELLS} == set(_ALL_IDS)


@pytest.mark.parametrize("source", _ALL_IDS)
def test_all_fixtures_load(source: str) -> None:
    assert load_handcrafted(source).key == source
    assert normalize_source(source) == source


# --- Row count / factorial / target mechanism -------------------------------


@pytest.mark.parametrize("source", _BINARY_IDS)
def test_binary_row_count_and_full_factorial(source: str) -> None:
    fx = load_handcrafted(source)
    # Minimal complete factorial: one row per (x0, x1) assignment.
    assert len(fx.df) == 4
    combos = list(zip(fx.df["x0"], fx.df["x1"]))
    for combo in itertools.product((0, 1), (0, 1)):
        assert combos.count(combo) == 1


@pytest.mark.parametrize("source", _CAT3_IDS)
def test_cat3_row_count_and_full_factorial(source: str) -> None:
    fx = load_handcrafted(source)
    # Minimal complete factorial: one row per (x0, x1) assignment.
    assert len(fx.df) == 9
    combos = list(zip(fx.df["x0"], fx.df["x1"]))
    for combo in itertools.product((0, 1, 2), (0, 1, 2)):
        assert combos.count(combo) == 1


@pytest.mark.parametrize("source", _ALL_IDS)
def test_x2_equals_designated_parent(source: str) -> None:
    fx = load_handcrafted(source)
    parent = M11_META_BY_KEY[source].parent
    assert all(
        int(fx.df["x2"].iloc[i]) == int(fx.df[parent].iloc[i]) for i in range(len(fx.df))
    )
    assert set(fx.ground_truth().parents_of("x2")) == {parent}


@pytest.mark.parametrize("source", _ALL_IDS)
def test_positive_class_definition(source: str) -> None:
    fx = load_handcrafted(source)
    threshold = 1 if "binary" in source else 2
    expected_pos = {f"x2({i + 1})" for i, v in enumerate(fx.df["x2"]) if int(v) == threshold}
    expected_neg = {f"x2({i + 1})" for i, v in enumerate(fx.df["x2"]) if int(v) != threshold}
    assert set(fx.pos_examples) == expected_pos
    assert set(fx.neg_examples) == expected_neg
    # Examples partition all rows exactly.
    assert len(fx.pos_examples) + len(fx.neg_examples) == len(fx.df)
    assert not (set(fx.pos_examples) & set(fx.neg_examples))


# --- Requested vs table order ----------------------------------------------


@pytest.mark.parametrize("source", _ALL_IDS)
def test_requested_order_equals_table_order(source: str) -> None:
    fx = load_handcrafted(source)
    meta = M11_META_BY_KEY[source]
    assert tuple(predictor_columns(fx)) == meta.requested_order
    assert list(fx.df.columns)[-1] == "x2"  # target kept last


# --- One-literal separator properties ---------------------------------------


@pytest.mark.parametrize("source", _ALL_IDS)
def test_separator_properties(source: str) -> None:
    checks = structural_checks(source)
    assert checks["parent_is_zero_error_separator"], source
    assert checks["non_parent_has_no_separator"], source


@pytest.mark.parametrize("source", _ALL_IDS)
def test_all_structural_checks_pass(source: str) -> None:
    checks = structural_checks(source)
    failed = [name for name, ok in checks.items() if not ok]
    assert not failed, f"{source} failed structural checks: {failed}"


# --- sigma / pi orbit relations ---------------------------------------------


@pytest.mark.parametrize("encoding", ("binary", "cat3"))
def test_sigma_pairs_exact(encoding: str) -> None:
    a = load_handcrafted(f"m11_{encoding}_A")
    b = load_handcrafted(f"m11_{encoding}_B")
    c = load_handcrafted(f"m11_{encoding}_C")
    d = load_handcrafted(f"m11_{encoding}_D")
    # A/B and D/C are exact sigma-pairs.
    assert is_sigma_pair(a, b)
    assert is_sigma_pair(d, c)


@pytest.mark.parametrize("encoding", ("binary", "cat3"))
def test_pi_pairs_exact(encoding: str) -> None:
    a = load_handcrafted(f"m11_{encoding}_A")
    b = load_handcrafted(f"m11_{encoding}_B")
    c = load_handcrafted(f"m11_{encoding}_C")
    d = load_handcrafted(f"m11_{encoding}_D")
    # A/D and B/C are exact pi-pairs.
    assert is_pi_pair(a, d)
    assert is_pi_pair(b, c)


@pytest.mark.parametrize("encoding", ("binary", "cat3"))
def test_square_commutes(encoding: str) -> None:
    """sigma(pi(A)) == pi(sigma(A)) == C (the transformation square closes)."""
    from causal.experiments.handcrafted_m11 import (
        apply_pi,
        apply_sigma,
        fixtures_equal_ignoring_key,
    )

    a = load_handcrafted(f"m11_{encoding}_A")
    c = load_handcrafted(f"m11_{encoding}_C")
    assert fixtures_equal_ignoring_key(apply_sigma(apply_pi(a)), c)
    assert fixtures_equal_ignoring_key(apply_pi(apply_sigma(a)), c)


@pytest.mark.parametrize("encoding", ("binary", "cat3"))
def test_sigma_pairs_share_examples(encoding: str) -> None:
    """A sigma-pair must have identical examples and identical row values."""
    a = load_handcrafted(f"m11_{encoding}_A")
    b = load_handcrafted(f"m11_{encoding}_B")
    assert a.pos_examples == b.pos_examples
    assert a.neg_examples == b.neg_examples
    # Same data, only column order differs.
    cols = sorted(a.df.columns)
    assert a.df[cols].reset_index(drop=True).equals(b.df[cols].reset_index(drop=True))


# --- BK-level checks (generated, Prolog-free) -------------------------------


@pytest.mark.parametrize("source", _BINARY_IDS)
def test_binary_fixtures_emit_bare_predicates(source: str, tmp_path: Path) -> None:
    text = _bk_text(source, tmp_path)
    assert "x0(A) :-" in text
    assert "x1(A) :-" in text
    assert "x0_val_" not in text
    assert "x1_val_" not in text


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


@pytest.mark.parametrize("source", _ALL_IDS)
def test_bk_order_matches_requested_order(source: str, tmp_path: Path) -> None:
    text = _bk_text(source, tmp_path)
    meta = M11_META_BY_KEY[source]
    assert bk_predictor_order(text) == list(meta.requested_order)


# --- Config expansion -------------------------------------------------------


def test_config_expands_to_eight_cells_all_x2() -> None:
    cfg = load_config(_CONFIG_PATH)
    cells = expand_cells(cfg, config_path=_CONFIG_PATH)
    assert len(cells) == 8
    assert all(c.target == "x2" for c in cells)
    assert {c.dgp for c in cells} == set(_ALL_IDS)
