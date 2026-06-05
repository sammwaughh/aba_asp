"""Tests for execute_cell stage 4 (metrics artefacts)."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pandas as pd
import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from causal.experiments.config import CellSpec
from causal.experiments.run_grid import Stage2Artefacts, Stage3Artefacts, execute_cell_stage4
from causal.metrics import RESULT_PARQUET_COLUMNS
from causal.run_aba_asp import SWIPL_PATH
from causal.test_aba_learning import _median_pos_neg_examples

pytest.importorskip("pyarrow")

_FIX_DIR = (
    _REPO_ROOT
    / "causal"
    / "outputs"
    / "aba_learning"
    / "TestMinimalContinuousData"
)
_DATA_CSV = _FIX_DIR / "cont_collider_8_x2.csv"
_BK = _FIX_DIR / "cont_collider_8_x2.bk.aba"

requires_fixture = pytest.mark.skipif(
    not _BK.is_file(), reason="cont_collider_8_x2 fixture bk.aba missing"
)
requires_prolog = pytest.mark.skipif(not SWIPL_PATH, reason="swipl not available")


@requires_fixture
@requires_prolog
def test_stage4_writes_metrics_json_and_parquet(tmp_path: Path) -> None:
    from causal.experiments.run_grid import execute_cell_stage3

    df = pd.read_csv(_DATA_CSV)
    pos, neg = _median_pos_neg_examples(df, "x2")
    run_dir = tmp_path / "cell"
    run_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(_BK, run_dir / "bk.aba")
    shutil.copy2(_DATA_CSV, run_dir / "data.csv")
    binned_src = _FIX_DIR / "cont_collider_8_x2.binned.csv"
    if binned_src.is_file():
        shutil.copy2(binned_src, run_dir / "data.binned.csv")

    cell = CellSpec(
        experiment_id="E_fixture",
        dgp="G3-collider",
        nodes=3,
        edges=((0, 2), (1, 2)),
        n=8,
        seed=0,
        target="x2",
        config_hash="sha256:fixture",
        run_id="fixture_stage4",
        graph_type="continuous",
        example_split="median",
    )
    stage2 = Stage2Artefacts(
        data_path=run_dir / "data.csv",
        bk_path=run_dir / "bk.aba",
        data_binned_path=run_dir / "data.binned.csv"
        if (run_dir / "data.binned.csv").exists()
        else None,
        pos_examples=tuple(pos),
        neg_examples=tuple(neg),
        outcome="ok",
        failure_reason=None,
    )
    stage3 = execute_cell_stage3(cell, stage2, run_dir, prolog_timeout_s=120.0)
    result = execute_cell_stage4(cell, stage3, run_dir, graph_type="continuous")

    assert result.metrics_json_path.is_file()
    assert result.metrics_parquet_path.is_file()
    doc = json.loads(result.metrics_json_path.read_text(encoding="utf-8"))
    for col in RESULT_PARQUET_COLUMNS:
        assert col in doc
    shard = pd.read_parquet(result.metrics_parquet_path, engine="pyarrow")
    assert len(shard) == 1
    assert not any(shard[c].dtype == object for c in shard.columns)
