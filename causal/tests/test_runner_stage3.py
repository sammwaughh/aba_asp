from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from causal.experiments.config import CellSpec
from causal.experiments.run_grid import Stage2Artefacts, execute_cell_stage3
from causal.metrics import parse_folding_tokens_used
from causal.run_aba_asp import ABASPRunner, SWIPL_PATH
from causal.test_aba_learning import _median_pos_neg_examples

_FIX_DIR = (
    _REPO_ROOT
    / "causal"
    / "outputs"
    / "aba_learning"
    / "TestMinimalContinuousData"
)
_DATA_CSV = _FIX_DIR / "cont_collider_8_x2.csv"
_BK_SOL = _FIX_DIR / "cont_collider_8_x2.bk.sol.aba"
_BK = _FIX_DIR / "cont_collider_8_x2.bk.aba"

requires_fixture = pytest.mark.skipif(
    not _BK.is_file(), reason="cont_collider_8_x2 fixture bk.aba missing"
)
requires_prolog = pytest.mark.skipif(
    not SWIPL_PATH, reason="swipl not available"
)


@requires_fixture
@requires_prolog
def test_stage3_smoke_solved_cont_collider_8_x2(tmp_path: Path) -> None:
    # Compute median E+/E- from the fixture CSV.
    import pandas as pd

    df = pd.read_csv(_DATA_CSV)
    pos, neg = _median_pos_neg_examples(df, "x2")
    assert pos and neg

    run_dir = tmp_path / "cell"
    run_dir.mkdir(parents=True, exist_ok=True)

    # Copy fixture BK into the runner layout (run_dir/bk.aba).
    shutil.copy2(_BK, run_dir / "bk.aba")
    shutil.copy2(_DATA_CSV, run_dir / "data.csv")
    # Copy binned CSV if present (continuous).
    binned_src = _FIX_DIR / "cont_collider_8_x2.binned.csv"
    binned_path = shutil.copy2(binned_src, run_dir / "data.binned.csv") if binned_src.is_file() else None

    cell = CellSpec(
        experiment_id="E_fixture",
        dgp="G3-collider",
        nodes=3,
        edges=((0, 2), (1, 2)),
        n=8,
        seed=0,
        target="x2",
        config_hash="sha256:fixture",
        run_id="fixture",
        graph_type="continuous",
        example_split="median",
    )

    stage2 = Stage2Artefacts(
        data_path=run_dir / "data.csv",
        bk_path=run_dir / "bk.aba",
        data_binned_path=run_dir / "data.binned.csv" if (run_dir / "data.binned.csv").exists() else None,
        pos_examples=tuple(pos),
        neg_examples=tuple(neg),
        outcome="ok",
        failure_reason=None,
    )

    # Run Prolog stage.
    stage3 = execute_cell_stage3(
        cell,
        stage2,
        run_dir,
        folding_steps=15,
        folding_mode="nd",
        prolog_timeout_s=120.0,
    )

    assert stage3.outcome == "solved"
    assert stage3.sol_path is not None and stage3.sol_path.is_file()
    assert stage3.wall_clock_s > 0.0
    assert stage3.folding_tokens_used >= 0

    # Verify prolog stdout/stderr are written verbatim.
    stdout_file = run_dir / "prolog.stdout"
    stderr_file = run_dir / "prolog.stderr"
    assert stdout_file.is_file()
    assert stderr_file.is_file()
    assert stdout_file.read_text(encoding="utf-8") == stage3.prolog_stdout
    assert stderr_file.read_text(encoding="utf-8") == stage3.prolog_stderr

    # Folding token parsing sanity (should match the stored value).
    assert parse_folding_tokens_used(stage3.prolog_stdout) == stage3.folding_tokens_used

