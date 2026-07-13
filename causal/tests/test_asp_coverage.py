"""Tests for ASP answer-set coverage (brave entailment on bk.sol.asp)."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from causal.asp_coverage import (
    asp_answer_set_coverage,
    atom_bravely_entailed,
    clingo_available,
    resolve_sol_asp_path,
)

requires_clingo = pytest.mark.skipif(
    not clingo_available(), reason="clingo not available on PATH"
)


@requires_clingo
def test_assumption_bearing_sep_like_coverage(tmp_path: Path) -> None:
    """ECAI-sep style: alphas + contraries → pos covered, negs rejected."""
    asp = tmp_path / "bk.sol.asp"
    asp.write_text(
        "\n".join(
            [
                "x0_val_0(A) :- A=1.",
                "x0_val_0(A) :- A=2.",
                "x0_val_0(A) :- A=3.",
                "x0_val_1(A) :- A=4.",
                "x0_val_1(A) :- A=5.",
                "x0_val_1(A) :- A=6.",
                "x0_val_2(A) :- A=7.",
                "x0_val_2(A) :- A=8.",
                "x0_val_2(A) :- A=9.",
                "x1_val_0(A) :- A=1.",
                "x1_val_1(A) :- A=2.",
                "x1_val_2(A) :- A=3.",
                "x1_val_0(A) :- A=4.",
                "x1_val_1(A) :- A=5.",
                "x1_val_2(A) :- A=6.",
                "x1_val_0(A) :- A=7.",
                "x1_val_1(A) :- A=8.",
                "x1_val_2(A) :- A=9.",
                "x2(A) :- alpha_1(A), x0_val_0(A).",
                "x2(A) :- alpha_2(A), x0_val_1(A).",
                "x2(A) :- alpha_3(A), x0_val_2(A).",
                "c_alpha_1(A) :- x1_val_0(A).",
                "c_alpha_1(A) :- x1_val_1(A).",
                "c_alpha_2(A) :- x1_val_0(A).",
                "c_alpha_2(A) :- x1_val_1(A).",
                "c_alpha_3(A) :- x1_val_0(A).",
                "c_alpha_3(A) :- x1_val_1(A).",
                "alpha_1(A) :- not c_alpha_1(A), x0_val_0(A).",
                "alpha_2(A) :- not c_alpha_2(A), x0_val_1(A).",
                "alpha_3(A) :- not c_alpha_3(A), x0_val_2(A).",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    pos = ["x2(3)", "x2(6)", "x2(9)"]
    neg = ["x2(1)", "x2(2)", "x2(4)", "x2(5)", "x2(7)", "x2(8)"]
    cov = asp_answer_set_coverage(asp, pos, neg)
    assert cov["cov_asp_tp"] == 3
    assert cov["cov_asp_fn"] == 0
    assert cov["cov_asp_tn"] == 6
    assert cov["cov_asp_fp"] == 0
    assert cov["cov_asp_n_pos"] == 3
    assert cov["cov_asp_n_neg"] == 6
    assert cov["cov_asp_pos"] == 1.0
    assert cov["cov_asp_neg"] == 1.0


@requires_clingo
def test_assumption_free_singleton_coverage(tmp_path: Path) -> None:
    asp = tmp_path / "bk.sol.asp"
    asp.write_text(
        "\n".join(
            [
                "x0_val_2(A) :- A=3.",
                "x0_val_0(A) :- A=1.",
                "x0_val_1(A) :- A=2.",
                "x2(A) :- x0_val_2(A).",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    pos = ["x2(3)"]
    neg = ["x2(1)", "x2(2)"]
    cov = asp_answer_set_coverage(asp, pos, neg)
    assert cov["cov_asp_tp"] == 1
    assert cov["cov_asp_tn"] == 2
    assert cov["cov_asp_pos"] == 1.0
    assert cov["cov_asp_neg"] == 1.0
    assert atom_bravely_entailed(asp, "x2(3)") is True
    assert atom_bravely_entailed(asp, "x2(1)") is False


def test_missing_sol_asp_returns_nan() -> None:
    cov = asp_answer_set_coverage(None, ["x2(1)"], ["x2(2)"])
    assert math.isnan(float(cov["cov_asp_pos"]))
    assert cov["_cov_asp_nan_reason"] == "sol_asp_missing"
    assert cov["cov_asp_n_pos"] == 1
    assert cov["cov_asp_n_neg"] == 1


def test_resolve_sol_asp_path(tmp_path: Path) -> None:
    (tmp_path / "bk.aba").write_text("x0_val_0(A) :- A=1.\n", encoding="utf-8")
    assert resolve_sol_asp_path(tmp_path / "bk.aba", tmp_path / "bk.sol.aba") is None
    asp = tmp_path / "bk.sol.asp"
    asp.write_text("x2(A) :- x0_val_0(A).\n", encoding="utf-8")
    assert resolve_sol_asp_path(tmp_path / "bk.aba", tmp_path / "bk.sol.aba") == asp
