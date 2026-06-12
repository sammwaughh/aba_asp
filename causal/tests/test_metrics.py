"""Unit tests for causal.metrics (Prolog-free paths)."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import pandas as pd
import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from causal.argcausaldisco_integration import _extract_learned_rules
from causal.metrics import (
    CellInputs,
    GroundTruth,
    RESULT_PARQUET_COLUMNS,
    abaf_structure_counts,
    body_level_stats,
    body_vars,
    compute_cell_metrics,
    outcome_classifier,
    parse_bk_feature_map,
    parse_delta_rules,
    python_horn_coverage,
    target_rule_filter,
    triviality_counts,
    variable_level_stats,
)
from causal.test_aba_learning import (
    _abaf_component_stats,
    _example_coverage_report,
    _median_pos_neg_examples,
    _summarize_target_rule_triviality,
)

_FIXTURE_SOL = (
    _REPO_ROOT
    / "causal"
    / "outputs"
    / "aba_learning"
    / "TestMinimalContinuousData"
    / "cont_collider_8_x2.bk.sol.aba"
)
_FIXTURE_BK = _FIXTURE_SOL.with_name("cont_collider_8_x2.bk.aba")
_CONFOUNDER_SOL = (
    _REPO_ROOT
    / "causal"
    / "outputs"
    / "aba_learning"
    / "TestMinimalContinuousData"
    / "cont_confounder_6_x0.bk.sol.aba"
)
_CONFOUNDER_BK = _CONFOUNDER_SOL.with_name("cont_confounder_6_x0.bk.aba")
_ASSUMPTION_SOL = (
    _REPO_ROOT
    / "causal"
    / "outputs"
    / "aba_learning"
    / "TestAssumptionIntroduction"
    / "exception_5.bk.sol.aba"
)
_ASSUMPTION_BK = _ASSUMPTION_SOL.with_name("exception_5.bk.aba")


def _gt_chain() -> GroundTruth:
    return GroundTruth(
        nodes=("x0", "x1", "x2"),
        edges=frozenset({("x0", "x1"), ("x1", "x2")}),
    )


def _gt_fork() -> GroundTruth:
    return GroundTruth(
        nodes=("x0", "x1", "x2"),
        edges=frozenset({("x0", "x1"), ("x0", "x2")}),
    )


def _gt_collider() -> GroundTruth:
    return GroundTruth(
        nodes=("x0", "x1", "x2"),
        edges=frozenset({("x0", "x2"), ("x1", "x2")}),
    )


class TestGroundTruthParents:
    def test_chain_parents(self) -> None:
        gt = _gt_chain()
        assert gt.parents_of("x0") == frozenset()
        assert gt.parents_of("x1") == frozenset({"x0"})
        assert gt.parents_of("x2") == frozenset({"x1"})

    def test_fork_parents(self) -> None:
        gt = _gt_fork()
        assert gt.parents_of("x2") == frozenset({"x0"})
        assert gt.parents_of("x1") == frozenset({"x0"})

    def test_collider_parents(self) -> None:
        gt = _gt_collider()
        assert gt.parents_of("x2") == frozenset({"x0", "x1"})


class TestGroundTruthAncestors:
    def test_chain_ancestors(self) -> None:
        gt = _gt_chain()
        assert gt.ancestors_of("x2") == frozenset({"x0", "x1"})
        assert gt.ancestors_of("x1") == frozenset({"x0"})
        assert gt.ancestors_of("x0") == frozenset()

    def test_fork_ancestors(self) -> None:
        gt = _gt_fork()
        assert gt.ancestors_of("x2") == frozenset({"x0"})
        assert gt.ancestors_of("x1") == frozenset({"x0"})

    def test_collider_ancestors(self) -> None:
        gt = _gt_collider()
        assert gt.ancestors_of("x2") == frozenset({"x0", "x1"})


class TestBodyVars:
    def test_x0_bin0(self) -> None:
        assert body_vars("x0_bin0(A)") == frozenset({"x0"})

    def test_x1_val_3(self) -> None:
        assert body_vars("x1_val_3(A)") == frozenset({"x1"})

    def test_x10_bin0_digit_boundary(self) -> None:
        assert body_vars("x10_bin0(A)") == frozenset({"x10"})

    def test_plain_variable(self) -> None:
        assert body_vars("x2(A)") == frozenset({"x2"})

    def test_rule_with_multiple_literals(self) -> None:
        assert body_vars("x2(A) :- x0_bin0(A), x1_val_1(A).") == frozenset(
            {"x0", "x1", "x2"}
        )


@pytest.mark.skipif(not _FIXTURE_SOL.is_file(), reason="fixture sol file missing")
class TestParseDeltaRules:
    def test_matches_legacy_extract(self) -> None:
        legacy = _extract_learned_rules(_FIXTURE_BK)
        assert parse_delta_rules(_FIXTURE_SOL) == legacy

    def test_collider_fixture_has_one_delta_rule(self) -> None:
        learned = parse_delta_rules(_FIXTURE_SOL)
        assert learned == ["x2(A) :- x0_bin0(A)."]


def _legacy_triviality_tuple(target: str, learned: list[str]) -> tuple[int, int, int]:
    n_target, n_trivial, n_nontrivial = _summarize_target_rule_triviality(target, learned)
    return n_target, n_trivial, n_nontrivial


def _triviality_tuple(target: str, learned: list[str]) -> tuple[int, int, int]:
    counts = triviality_counts(target, learned)
    return (
        int(counts["n_target_rules"]),
        int(counts["n_trivial_target_rules"]),
        int(counts["n_nontrivial_target_rules"]),
    )


class TestTrivialityCounts:
    def test_all_trivial(self) -> None:
        learned = [
            "x2(A) :- x2_bin0(A).",
            "x2(A) :- x2_bin1(A), x2_bin0(A).",
        ]
        assert _triviality_tuple("x2", learned) == (2, 2, 0)
        assert target_rule_filter("x2", learned) == learned

    def test_mixed_trivial_and_nontrivial(self) -> None:
        learned = [
            "x2(A) :- x2_bin0(A).",
            "x2(A) :- x0_bin0(A).",
            "x0(A) :- x1_bin0(A).",
        ]
        assert _triviality_tuple("x2", learned) == (2, 1, 1)
        counts = triviality_counts("x2", learned)
        assert counts["max_body_length"] == 1
        assert counts["mean_body_length"] == 1.0

    def test_no_target_rules(self) -> None:
        learned = ["x0(A) :- x1_bin0(A)."]
        counts = triviality_counts("x2", learned)
        assert counts["n_target_rules"] == 0
        assert counts["n_trivial_target_rules"] == 0
        assert counts["n_nontrivial_target_rules"] == 0
        assert counts["max_body_length"] == 0
        assert counts["mean_body_length"] != counts["mean_body_length"]  # NaN


@pytest.mark.skipif(
    not _CONFOUNDER_SOL.is_file(), reason="cont_confounder_6_x0 fixture missing"
)
class TestTrivialityFixtureConfounder:
    def test_matches_legacy_on_cont_confounder_6_x0(self) -> None:
        learned = parse_delta_rules(_CONFOUNDER_SOL)
        assert _triviality_tuple("x0", learned) == _legacy_triviality_tuple(
            "x0", learned
        )
        assert learned == ["x0(A) :- x1_bin0(A)."]


@pytest.mark.skipif(
    not _ASSUMPTION_SOL.is_file(), reason="exception_5 assumption fixture missing"
)
class TestAbafStructureCounts:
    def test_assumption_laden_exception_5(self) -> None:
        learned = parse_delta_rules(_ASSUMPTION_SOL)
        legacy = _abaf_component_stats(learned)
        ours = abaf_structure_counts(learned)
        assert {k: ours[k] for k in legacy} == legacy
        assert ours["n_delta_rules"] == len(learned)
        assert ours["assumptions"] == 1
        assert ours["alpha_mentions"] == 4

    def test_zero_abaf_on_confounder_fixture(self) -> None:
        """cont_confounder_6_x0 has no assumptions; validates pipeline on that path."""
        learned = parse_delta_rules(_CONFOUNDER_SOL)
        legacy = _abaf_component_stats(learned)
        ours = abaf_structure_counts(learned)
        assert {k: ours[k] for k in legacy} == legacy
        assert ours == {
            "n_delta_rules": 1,
            "assumptions": 0,
            "contraries": 0,
            "alpha_mentions": 0,
            "c_alpha_mentions": 0,
        }


class TestBodyLevelStatsMicroExample:
    """METRICS.md §6 worked examples on G3-fork."""

    def test_x2_perfect_parent_match(self) -> None:
        gt = _gt_fork()
        learned = ["x2(A) :- x0_bin0(A)."]
        stats = body_level_stats("x2", learned, gt)
        assert stats["body_parent_precision"] == 1.0
        assert stats["body_parent_recall"] == 1.0
        assert stats["body_parent_f1"] == 1.0
        assert stats["offgraph_rate"] == 0.0
        assert stats["ancestor_only_rate"] == 0.0
        assert stats["degenerate_hit"] == 0
        assert stats["mass_balance_ok"] is True

    def test_x0_offgraph(self) -> None:
        gt = _gt_fork()
        learned = ["x0(A) :- x1_bin0(A)."]
        stats = body_level_stats("x0", learned, gt)
        assert stats["body_parent_precision"] == 0.0
        assert math.isnan(stats["body_parent_recall"])
        assert math.isnan(stats["body_parent_f1"])
        assert stats["offgraph_rate"] == 1.0
        assert stats["ancestor_only_rate"] == 0.0
        assert stats["mass_balance_ok"] is True


class TestBodyLevelStatsEdgeCases:
    def test_recall_nan_when_no_parents(self) -> None:
        gt = _gt_fork()
        learned = ["x0(A) :- x1_bin0(A)."]
        stats = body_level_stats("x0", learned, gt)
        assert gt.parents_of("x0") == frozenset()
        assert math.isnan(stats["body_parent_recall"])

    def test_mass_balance_synthetic_mix(self) -> None:
        gt = GroundTruth(
            nodes=("x0", "x1", "x2"),
            edges=frozenset({("x0", "x2"), ("x1", "x2")}),
        )
        learned = [
            "x2(A) :- x0_bin0(A).",
            "x2(A) :- x1_bin0(A).",
            "x2(A) :- x2_bin0(A).",
        ]
        stats = body_level_stats("x2", learned, gt)
        assert stats["mass_balance_ok"] is True
        assert stats["degenerate_hit"] == 0


class TestVariableLevelStats:
    """Variable-level set comparison + clean_recovery (METRICS.md §3.4b)."""

    def test_exact_recovery_fork(self) -> None:
        gt = _gt_fork()  # parents(x2) = {x0}
        learned = ["x2(A) :- x0_bin0(A)."]
        stats = variable_level_stats("x2", learned, gt)
        assert stats["var_parent_precision"] == 1.0
        assert stats["var_parent_recall"] == 1.0
        assert stats["var_parent_jaccard"] == 1.0
        assert stats["clean_recovery"] == 1

    def test_ancestor_proxy_chain_is_not_clean(self) -> None:
        gt = _gt_chain()  # parents(x2) = {x1}; x0 is a strict ancestor
        learned = ["x2(A) :- x0_bin0(A)."]
        stats = variable_level_stats("x2", learned, gt)
        assert stats["var_parent_precision"] == 0.0
        assert stats["var_parent_recall"] == 0.0
        assert stats["var_parent_jaccard"] == 0.0
        assert stats["clean_recovery"] == 0

    def test_parent_subset_collider(self) -> None:
        gt = _gt_collider()  # parents(x2) = {x0, x1}
        learned = ["x2(A) :- x0_bin0(A)."]
        stats = variable_level_stats("x2", learned, gt)
        assert stats["var_parent_precision"] == 1.0
        assert stats["var_parent_recall"] == 0.5
        assert stats["var_parent_jaccard"] == 0.5
        assert stats["clean_recovery"] == 0

    def test_parent_superset_chain_contaminated(self) -> None:
        gt = _gt_chain()  # parents(x2) = {x1}
        learned = ["x2(A) :- x1_bin0(A).", "x2(A) :- x0_bin0(A)."]
        stats = variable_level_stats("x2", learned, gt)
        # recovered = {x0, x1}; only x1 is a parent.
        assert stats["var_parent_precision"] == 0.5
        assert stats["var_parent_recall"] == 1.0
        assert stats["var_parent_jaccard"] == 0.5
        assert stats["clean_recovery"] == 0

    def test_empty_recovered_set(self) -> None:
        gt = _gt_fork()
        stats = variable_level_stats("x2", [], gt)
        assert math.isnan(stats["var_parent_precision"])
        assert stats["var_parent_recall"] == 0.0
        assert stats["var_parent_jaccard"] == 0.0
        assert stats["clean_recovery"] == 0

    def test_root_target_recall_nan(self) -> None:
        gt = _gt_chain()  # parents(x0) = {}
        learned = ["x0(A) :- x1_bin0(A)."]
        stats = variable_level_stats("x0", learned, gt)
        assert math.isnan(stats["var_parent_recall"])
        assert stats["clean_recovery"] == 0


@pytest.mark.skipif(not _FIXTURE_SOL.is_file(), reason="collider fixture missing")
class TestPythonHornCoverage:
    def test_matches_legacy_on_cont_collider_8_x2(self) -> None:
        learned = parse_delta_rules(_FIXTURE_SOL)
        df = pd.read_csv(
            _FIXTURE_SOL.parent / "cont_collider_8_x2.csv"
        )
        pos, neg = _median_pos_neg_examples(df, "x2")
        legacy = _example_coverage_report(
            target="x2",
            bk_path=_FIXTURE_BK,
            learned_rules=learned,
            pos_examples=pos,
            neg_examples=neg,
        )
        ours = python_horn_coverage(_FIXTURE_BK, learned, pos, neg, target="x2")
        assert ours["cov_py_tp"] + ours["cov_py_fn"] == len(pos)
        assert ours["cov_py_tn"] + ours["cov_py_fp"] == len(neg)
        assert ours["cov_py_tp"] == legacy["TP"]
        assert ours["cov_py_fn"] == legacy["FN"]
        assert ours["cov_py_tn"] == legacy["TN"]
        assert ours["cov_py_fp"] == legacy["FP"]
        assert ours["cov_py_accuracy"] == legacy["acc"]
        assert ours["cov_py_pos"] == legacy["pos_cov"]
        assert ours["cov_py_neg"] == legacy["neg_cov"]

    def test_parse_bk_feature_map_nonempty(self) -> None:
        fmap = parse_bk_feature_map(_FIXTURE_BK)
        assert 1 in fmap
        assert any(p.startswith("x0_bin") for p in fmap[1])


def _collider_gt() -> GroundTruth:
    return GroundTruth(
        nodes=("x0", "x1", "x2"),
        edges=frozenset({("x0", "x2"), ("x1", "x2")}),
    )


def _collider_cell_inputs(
    *,
    outcome: str = "solved",
    failure_reason: str | None = None,
    sol_path: Path | None = None,
) -> CellInputs:
    df = pd.read_csv(_FIXTURE_SOL.parent / "cont_collider_8_x2.csv")
    pos, neg = _median_pos_neg_examples(df, "x2")
    return CellInputs(
        experiment_id="test_fixture",
        dgp="G3-collider",
        graph_type="continuous",
        target="x2",
        n=8,
        seed=0,
        config_hash="fixture",
        run_id="test_fixture_G3-collider_x2_s0",
        bk_path=_FIXTURE_BK,
        sol_path=sol_path if sol_path is not None else _FIXTURE_SOL,
        pos_examples=tuple(pos),
        neg_examples=tuple(neg),
        ground_truth=_collider_gt(),
        wall_clock_s=12.5,
        outcome=outcome,
        failure_reason=failure_reason,
        folding_tokens_used=10,
    )


def _assert_nan_has_reason(panel: dict, key: str) -> None:
    assert math.isnan(panel[key])
    assert f"{key}_nan_reason" in panel
    assert panel[f"{key}_nan_reason"]


class TestOutcomeClassifier:
    def test_skipped(self) -> None:
        outcome, reason = outcome_classifier("", None, [], 1.0, 120.0, False)
        assert outcome == "skipped"
        assert reason == "empty E+ or E-"

    def test_timeout(self) -> None:
        outcome, reason = outcome_classifier("", None, [], 130.0, 120.0, True)
        assert outcome == "timeout"
        assert reason is not None

    def test_solved(self) -> None:
        learned = ["x2(A) :- x0_bin0(A)."]
        outcome, reason = outcome_classifier(
            "ok", _FIXTURE_SOL, learned, 10.0, 120.0, True
        )
        assert outcome == "solved"
        assert reason is None

    def test_completed_no_solution(self) -> None:
        stdout = "Running...\n* No solution found!\n"
        outcome, reason = outcome_classifier(stdout, None, [], 5.0, 120.0, True)
        assert outcome == "completed_no_solution"
        assert reason is not None

    def test_completed_empty_delta(self, tmp_path: Path) -> None:
        sol = tmp_path / "empty.bk.sol.aba"
        bk = tmp_path / "empty.bk.aba"
        bk.write_text("x0(A) :- A=1.\n", encoding="utf-8")
        sol.write_text("x0(A) :- A=1.\n", encoding="utf-8")
        outcome, reason = outcome_classifier("", sol, [], 5.0, 120.0, True)
        assert outcome == "completed_empty_delta"
        assert reason is not None

    def test_error(self) -> None:
        outcome, reason = outcome_classifier("crash", None, [], 5.0, 120.0, True)
        assert outcome == "error"
        assert reason is not None


@pytest.mark.skipif(not _FIXTURE_SOL.is_file(), reason="collider fixture missing")
class TestComputeCellMetrics:
    def test_all_parquet_columns_present(self) -> None:
        panel = compute_cell_metrics(_collider_cell_inputs())
        for col in RESULT_PARQUET_COLUMNS:
            assert col in panel, f"missing column {col}"

    def test_identity_check(self) -> None:
        inp = _collider_cell_inputs()
        first = compute_cell_metrics(inp)
        second = compute_cell_metrics(inp)
        assert first == second

    def test_fork_microexample_f1_via_full_panel(self) -> None:
        gt = _gt_fork()
        learned = ["x2(A) :- x0_bin0(A)."]
        inp = CellInputs(
            experiment_id="micro",
            dgp="G3-fork",
            graph_type="continuous",
            target="x2",
            n=8,
            seed=0,
            config_hash="micro",
            run_id="micro",
            bk_path=_FIXTURE_BK,
            sol_path=_FIXTURE_SOL,
            pos_examples=("x2(1)", "x2(2)"),
            neg_examples=("x2(3)", "x2(4)"),
            ground_truth=gt,
            wall_clock_s=1.0,
            outcome="solved",
            failure_reason=None,
            folding_tokens_used=0,
        )
        panel = compute_cell_metrics(inp)
        assert panel["body_parent_f1"] == 1.0

    def test_collider_fixture_solved_f1(self) -> None:
        learned = parse_delta_rules(_FIXTURE_SOL)
        outcome, failure_reason = outcome_classifier(
            "", _FIXTURE_SOL, learned, 12.5, 120.0, True
        )
        inp = _collider_cell_inputs(outcome=outcome, failure_reason=failure_reason)
        panel = compute_cell_metrics(inp)
        assert panel["outcome"] == "solved"
        assert panel["failure_reason"] is None
        assert panel["body_parent_precision"] == 1.0
        assert panel["body_parent_recall"] == 0.5
        assert panel["body_parent_f1"] == pytest.approx(2.0 / 3.0)
        assert panel["n_nontrivial_target_rules"] == 1
        # Variable-level: recovered {x0}, parents {x0, x1} -> subset, not clean.
        assert panel["var_parent_precision"] == 1.0
        assert panel["var_parent_recall"] == 0.5
        assert panel["clean_recovery"] == 0

    @pytest.mark.skipif(
        not _CONFOUNDER_SOL.is_file(), reason="confounder fixture missing"
    )
    def test_nan_reasons_recorded_for_deferred_and_empty_parents(self) -> None:
        learned = parse_delta_rules(_CONFOUNDER_SOL)
        outcome, failure_reason = outcome_classifier(
            "", _CONFOUNDER_SOL, learned, 1.0, 120.0, True
        )
        gt = GroundTruth(
            nodes=("x0", "x1", "x2"),
            edges=frozenset({("x0", "x1"), ("x0", "x2")}),
        )
        inp = CellInputs(
            experiment_id="nan_test",
            dgp="G3-confounder",
            graph_type="continuous",
            target="x0",
            n=6,
            seed=0,
            config_hash="x",
            run_id="nan_test",
            bk_path=_CONFOUNDER_BK,
            sol_path=_CONFOUNDER_SOL,
            pos_examples=("x0(1)", "x0(2)", "x0(3)"),
            neg_examples=("x0(4)", "x0(5)", "x0(6)"),
            ground_truth=gt,
            wall_clock_s=1.0,
            outcome=outcome,
            failure_reason=failure_reason,
            folding_tokens_used=0,
        )
        panel = compute_cell_metrics(inp)
        _assert_nan_has_reason(panel, "body_parent_recall")
        # Prolog-aware coverage is implemented; it should produce a real value.
        assert 0.0 <= panel["cov_pl_accuracy"] <= 1.0
        assert panel["cov_pl_tp"] + panel["cov_pl_fn"] == len(inp.pos_examples)
        _assert_nan_has_reason(panel, "skel_precision")

    def test_non_solved_uses_empty_delta_for_coverage(self) -> None:
        inp = _collider_cell_inputs(
            outcome="completed_no_solution",
            failure_reason="Prolog reported no solution",
            sol_path=None,
        )
        panel = compute_cell_metrics(inp)
        assert panel["n_delta_rules"] == 0
        assert panel["cov_py_pos"] == 0.0
        assert panel["cov_py_tp"] == 0
