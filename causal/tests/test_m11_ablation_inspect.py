"""Tests for m1.1 ablation trace inspector (Prolog-free)."""

from __future__ import annotations

from pathlib import Path

import pytest

from causal.experiments.m11_ablation_inspect import (
    AblationExpected,
    compare_to_expected,
    parse_trace_observables,
)

_REPO = Path(__file__).resolve().parents[2]
_CAT3_A_STDOUT = (
    _REPO
    / "causal/outputs/aba_learning/grid/M11_parent_position/cells/m11_cat3_A/prolog.stdout"
)
_CAT3_B_STDOUT = (
    _REPO
    / "causal/outputs/aba_learning/grid/M11_parent_position/cells/m11_cat3_B/prolog.stdout"
)

_SNIPPET_A = """
 begin nd folding
 1: folding [A=3] with x0_val_0(_5226): x0_val_0(A) <- [A=3]
gen2: extended ABA does not entail <E+,E-> - looking for assumption relative to
gen2: generating NEW assumption: alpha_1(A)
ABA size (rules): 27
Writing solution no. 1
"""

_SNIPPET_B = """
 begin nd folding
 1: folding [A=3] with x1_val_2(_5226): x1_val_2(A) <- [A=3]
gen2: extended ABA entails <E+,E-> - using folding
ABA size (rules): 19
Writing solution no. 1
"""


def test_parse_cat3_a_snippet() -> None:
    obs = parse_trace_observables(_SNIPPET_A)
    assert obs.first_fold_pred == "x0_val_0"
    assert obs.entailment == "fail"
    assert obs.aba_rules == 27
    assert obs.n_assumptions >= 1
    assert obs.outcome == "solved"


def test_parse_cat3_b_snippet() -> None:
    obs = parse_trace_observables(_SNIPPET_B)
    assert obs.first_fold_pred == "x1_val_2"
    assert obs.entailment == "pass"
    assert obs.aba_rules == 19
    assert obs.n_assumptions == 0


def test_compare_expected_pass() -> None:
    obs = parse_trace_observables(_SNIPPET_B)
    exp = AblationExpected(
        first_fold_pred="x1_val_2",
        entailment="pass",
        max_trace_lines=80,
        max_aba_rules=22,
    )
    summary = compare_to_expected("ABL-101", obs, ["x2(A)<-x1_val_2(A)"], exp)
    assert summary.verdict == "pass"


def test_compare_expected_fail_entailment() -> None:
    obs = parse_trace_observables(_SNIPPET_A)
    exp = AblationExpected(
        first_fold_pred="x1_val_2",
        entailment="pass",
    )
    summary = compare_to_expected("ABL-101", obs, [], exp)
    assert summary.verdict == "fail"
    assert any("first_fold_pred" in m for m in summary.mismatches)


@pytest.mark.skipif(not _CAT3_A_STDOUT.is_file(), reason="grid artefact missing")
def test_parse_real_cat3_a_trace() -> None:
    text = _CAT3_A_STDOUT.read_text(encoding="utf-8")
    obs = parse_trace_observables(text)
    assert obs.first_fold_pred == "x0_val_0"
    assert obs.entailment == "fail"
    assert obs.trace_lines > 100


@pytest.mark.skipif(not _CAT3_B_STDOUT.is_file(), reason="grid artefact missing")
def test_parse_real_cat3_b_trace() -> None:
    text = _CAT3_B_STDOUT.read_text(encoding="utf-8")
    obs = parse_trace_observables(text)
    assert obs.first_fold_pred == "x1_val_2"
    assert obs.entailment == "pass"
    assert obs.trace_lines < 80
