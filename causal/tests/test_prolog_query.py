"""Tests for Prolog-aware example coverage queries."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from unittest import mock

import pandas as pd
import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from causal.run_aba_asp import (
    SWIPL_PATH,
    _build_batch_query_script,
    _run_prolog_script,
    query_examples,
)
from causal.test_aba_learning import _median_pos_neg_examples
from causal.metrics import (
    CellInputs,
    GroundTruth,
    compute_cell_metrics,
    parse_delta_rules,
)

pytestmark = pytest.mark.skipif(
    not SWIPL_PATH, reason="SWI-Prolog (swipl) not available on PATH"
)

_FIXTURE_SOL = (
    _REPO_ROOT
    / "causal"
    / "outputs"
    / "aba_learning"
    / "TestMinimalContinuousData"
    / "cont_collider_8_x2.bk.sol.aba"
)

requires_fixture = pytest.mark.skipif(
    not _FIXTURE_SOL.is_file(), reason="cont_collider_8_x2 fixture missing"
)

_EXCEPTION_SOL = (
    _REPO_ROOT
    / "causal"
    / "outputs"
    / "aba_learning"
    / "TestAssumptionIntroduction"
    / "exception_5.bk.sol.aba"
)
_EXCEPTION_BK = _EXCEPTION_SOL.with_name("exception_5.bk.aba")

requires_exception_fixture = pytest.mark.skipif(
    not _EXCEPTION_SOL.is_file(), reason="exception_5 fixture missing"
)


@pytest.fixture
def collider_examples() -> tuple[list[str], list[str]]:
    df = pd.read_csv(_FIXTURE_SOL.parent / "cont_collider_8_x2.csv")
    pos, neg = _median_pos_neg_examples(df, "x2")
    return pos, neg


@requires_fixture
class TestQueryExamples:
    def test_callable_returns_dict(self, collider_examples: tuple[list[str], list[str]]) -> None:
        pos, neg = collider_examples
        examples = pos[:2] + neg[:2]
        results = query_examples(_FIXTURE_SOL, examples, timeout_s=5.0)
        assert isinstance(results, dict)
        assert set(results.keys()) == set(examples)
        assert all(isinstance(v, bool) for v in results.values())

    def test_collider_sol_matches_known_semantics(
        self, collider_examples: tuple[list[str], list[str]]
    ) -> None:
        pos, neg = collider_examples
        results = query_examples(_FIXTURE_SOL, pos + neg, timeout_s=5.0)
        for atom in pos:
            assert results[atom] is True, atom
        for atom in neg:
            assert results[atom] is False, atom

    def test_x2_1_and_x2_5_specifically(self) -> None:
        results = query_examples(_FIXTURE_SOL, ["x2(1)", "x2(5)"], timeout_s=5.0)
        assert results["x2(1)"] is False
        assert results["x2(5)"] is True

    def test_empty_examples(self) -> None:
        assert query_examples(_FIXTURE_SOL, [], timeout_s=5.0) == {}

    def test_invalid_example_rejected(self) -> None:
        with pytest.raises(ValueError, match="Invalid example atom"):
            query_examples(_FIXTURE_SOL, ["not an atom"], timeout_s=5.0)

    def test_subprocess_timeout_returns_false(self, collider_examples: tuple[list[str], list[str]]) -> None:
        pos, _neg = collider_examples
        with mock.patch(
            "causal.run_aba_asp._run_prolog_script",
            side_effect=subprocess.TimeoutExpired(cmd="swipl", timeout=0.01),
        ):
            results = query_examples(_FIXTURE_SOL, pos[:1], timeout_s=5.0)
        assert results[pos[0]] is False

    def test_batch_script_uses_call_with_time_limit(self) -> None:
        script = _build_batch_query_script(_FIXTURE_SOL, ["x2(3)"], timeout_s=0.5)
        assert "call_with_time_limit" in script
        assert "time_limit_exceeded" in script

    def test_hung_prolog_subprocess_times_out(self, tmp_path: Path) -> None:
        hang_script = ":- initialization(main, main).\nmain :- between(1, 1000000000, _), fail.\n"
        with pytest.raises(subprocess.TimeoutExpired):
            _run_prolog_script(hang_script, cwd=tmp_path, timeout_s=0.3)


@requires_fixture
class TestPrologAwareCoverageWiring:
    def test_gap_pos_zero_on_cont_collider_8_x2(self, collider_examples: tuple[list[str], list[str]]) -> None:
        pos, neg = collider_examples
        learned = parse_delta_rules(_FIXTURE_SOL)
        inp = CellInputs(
            experiment_id="A06",
            dgp="G3-collider",
            graph_type="continuous",
            target="x2",
            n=8,
            seed=0,
            config_hash="fixture",
            run_id="fixture",
            bk_path=_FIXTURE_SOL.with_name("cont_collider_8_x2.bk.aba"),
            sol_path=_FIXTURE_SOL,
            pos_examples=tuple(pos),
            neg_examples=tuple(neg),
            ground_truth=GroundTruth(
                nodes=("x0", "x1", "x2"),
                edges=frozenset({("x0", "x2"), ("x1", "x2")}),
            ),
            wall_clock_s=1.0,
            outcome="solved",
            failure_reason=None,
            folding_tokens_used=0,
        )
        panel = compute_cell_metrics(inp)
        assert panel["cov_pl_tp"] + panel["cov_pl_fn"] == len(pos)
        assert panel["cov_gap_pos"] == pytest.approx(0.0)


@requires_exception_fixture
class TestPrologAwareCoverageAssumptions:
    def test_gap_pos_nonzero_on_exception_5(self) -> None:
        pos = ["x2(1)", "x2(2)"]
        neg = ["x2(3)", "x2(4)", "x2(5)"]
        inp = CellInputs(
            experiment_id="A06",
            dgp="H-exception-5",
            graph_type="handcrafted_table",
            target="x2",
            n=5,
            seed=0,
            config_hash="fixture",
            run_id="fixture",
            bk_path=_EXCEPTION_BK,
            sol_path=_EXCEPTION_SOL,
            pos_examples=tuple(pos),
            neg_examples=tuple(neg),
            ground_truth=GroundTruth(
                nodes=("x0", "x1", "x2"),
                edges=frozenset({("x0", "x2")}),
            ),
            wall_clock_s=1.0,
            outcome="solved",
            failure_reason=None,
            folding_tokens_used=0,
        )
        panel = compute_cell_metrics(inp)
        assert panel["cov_pl_tp"] + panel["cov_pl_fn"] == len(pos)
        assert panel["cov_gap_pos"] != 0.0
