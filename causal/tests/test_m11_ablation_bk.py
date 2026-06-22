"""Tests for m1.1 ablation BK interventions (Prolog-free)."""

from __future__ import annotations

from pathlib import Path

import pytest

from causal.experiments.m11_ablation_bk import (
    bk_rule_multiset,
    block_order_from_source,
    build_intervened_bk,
    parse_bk_lines,
    prepend_bk_rules,
    read_bk_text,
    reorder_bk_blocks_from,
    rule_multiset,
)

_REPO = Path(__file__).resolve().parents[2]
_GRID = _REPO / "causal/outputs/aba_learning/grid/M11_parent_position/cells"
_CAT3_A = _GRID / "m11_cat3_A/bk.aba"
_CAT3_B = _GRID / "m11_cat3_B/bk.aba"


@pytest.fixture
def bk_a() -> str:
    if not _CAT3_A.is_file():
        pytest.skip("m11 cat3 A grid artefact missing")
    return read_bk_text(_CAT3_A)


@pytest.fixture
def bk_b() -> str:
    if not _CAT3_B.is_file():
        pytest.skip("m11 cat3 B grid artefact missing")
    return read_bk_text(_CAT3_B)


def test_block_order_from_b_vs_a(bk_a: str, bk_b: str) -> None:
    assert block_order_from_source(bk_a) == ("x0", "x1")
    assert block_order_from_source(bk_b) == ("x1", "x0")


def test_reorder_preserves_multiset(bk_a: str, bk_b: str) -> None:
    flipped = reorder_bk_blocks_from(bk_b, bk_a)
    assert bk_rule_multiset(bk_a, flipped)
    assert block_order_from_source(flipped) == ("x1", "x0")


def test_reorder_matches_b_block_order(bk_a: str, bk_b: str) -> None:
    flipped = reorder_bk_blocks_from(bk_b, bk_a)
    assert block_order_from_source(flipped) == block_order_from_source(bk_b)


def test_prepend_adds_rule_at_top(bk_a: str) -> None:
    extra = "x1_val_2(A) :- A=3."
    out = prepend_bk_rules(bk_a, [extra])
    rules = [ln.rule_key for ln in parse_bk_lines(out) if ln.is_rule]
    assert rules[0] == extra
    assert len(rules) == len(rule_multiset(parse_bk_lines(bk_a))) + 1


def test_build_intervened_block_order_from(bk_a: str, bk_b: str) -> None:
    out = build_intervened_bk(bk_a, mode="block_order_from", source_text=bk_b)
    assert bk_rule_multiset(bk_a, out)


def test_build_intervened_prepend(bk_a: str) -> None:
    out = build_intervened_bk(
        bk_a,
        mode="prepend_rules",
        prepend_rules=["x1_val_2(A) :- A=3."],
    )
    assert "x1_val_2(A) :- A=3." in out.splitlines()[2]
