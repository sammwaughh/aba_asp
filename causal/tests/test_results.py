"""Tests for per-cell metrics shards and results concatenation."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import pandas as pd
import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from causal.experiments.results import (
    concat_shards,
    enforce_results_dtypes,
    load_metrics_parquet_shard,
    write_cell_metrics,
    write_results_parquet,
)
from causal.metrics import RESULT_PARQUET_COLUMNS

pytest.importorskip("pyarrow")


def _panels_equal(a: dict, b: dict) -> bool:
    for col in RESULT_PARQUET_COLUMNS:
        va, vb = a[col], b[col]
        if isinstance(va, float) and isinstance(vb, float):
            if math.isnan(va) and math.isnan(vb):
                continue
        if va != vb:
            return False
    return True


def _synthetic_panel(*, run_id: str, seed: int) -> dict:
    """Minimal valid panel row for shard tests."""
    nan = math.nan
    base = {
        "experiment_id": "E_test",
        "dgp": "G3-chain",
        "graph_type": "continuous",
        "target": "x2",
        "n": 25,
        "seed": seed,
        "config_hash": "sha256:test",
        "run_id": run_id,
        "outcome": "skipped",
        "failure_reason": "empty E+ or E-",
        "wall_clock_s": 0.0,
        "folding_tokens_used": 0,
        "n_delta_rules": 0,
        "n_target_rules": 0,
        "n_assumptions": 0,
        "n_contraries": 0,
        "n_trivial_target_rules": 0,
        "n_nontrivial_target_rules": 0,
        "max_body_length": 0,
        "mean_body_length": nan,
        "body_parent_precision": nan,
        "body_parent_recall": nan,
        "body_parent_f1": nan,
        "offgraph_rate": nan,
        "ancestor_only_rate": nan,
        "cov_py_accuracy": nan,
        "cov_py_pos": nan,
        "cov_py_neg": nan,
        "cov_py_tp": 0,
        "cov_py_fp": 0,
        "cov_py_tn": 0,
        "cov_py_fn": 0,
        "cov_pl_accuracy": nan,
        "cov_pl_pos": nan,
        "cov_pl_neg": nan,
        "cov_pl_tp": 0,
        "cov_pl_fp": 0,
        "cov_pl_tn": 0,
        "cov_pl_fn": 0,
        "cov_gap_accuracy": nan,
        "cov_gap_pos": nan,
        "cov_gap_neg": nan,
        "skel_precision": nan,
        "skel_recall": nan,
        "skel_f1": nan,
        "dir_d1_precision": nan,
        "dir_d1_recall": nan,
        "dir_d1_f1": nan,
        "dir_d2_precision": nan,
        "dir_d2_recall": nan,
        "dir_d2_f1": nan,
        "bridge_mode": None,
        "shd": None,
        "dir_edge_precision": nan,
        "dir_edge_recall": nan,
        "dir_edge_f1": nan,
        "runtime_s_bridge": nan,
        "parser_unread_lines": 0,
        "sol_file_bytes": 0,
    }
    return base


def test_parquet_shard_round_trip_no_dtype_drift(tmp_path: Path) -> None:
    panel = _synthetic_panel(run_id="r0", seed=0)
    panel["body_parent_f1_nan_reason"] = "no_nontrivial_target_rules"
    run_dir = tmp_path / "cell_a"
    _, parquet_path = write_cell_metrics(run_dir, panel)
    loaded = load_metrics_parquet_shard(parquet_path)
    assert _panels_equal(panel, loaded)
    shard = pd.read_parquet(parquet_path, engine="pyarrow")
    assert not any(shard[c].dtype == object for c in shard.columns)
    assert list(shard.columns) == list(RESULT_PARQUET_COLUMNS)


def test_concat_three_shards(tmp_path: Path) -> None:
    exp_dir = tmp_path / "E_test"
    cells = exp_dir / "cells"
    for i, rid in enumerate(("r0", "r1", "r2")):
        run_dir = cells / rid
        write_cell_metrics(run_dir, _synthetic_panel(run_id=rid, seed=i))

    df = concat_shards(exp_dir)
    assert len(df) == 3
    assert set(df["run_id"]) == {"r0", "r1", "r2"}
    assert not any(df[c].dtype == object for c in df.columns)

    out = write_results_parquet(exp_dir)
    assert out.is_file()
    reread = pd.read_parquet(out, engine="pyarrow")
    assert len(reread) == 3


def test_metrics_json_has_parquet_columns(tmp_path: Path) -> None:
    panel = _synthetic_panel(run_id="json_test", seed=1)
    json_path, _ = write_cell_metrics(tmp_path / "cell", panel)
    doc = json.loads(json_path.read_text(encoding="utf-8"))
    for col in RESULT_PARQUET_COLUMNS:
        assert col in doc
