"""Per-cell metrics shards and experiment-level ``results.parquet`` (INFRA.md §5)."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Mapping

import numpy as np
import pandas as pd

from causal.metrics import RESULT_PARQUET_COLUMNS

# Pinned dtypes for Parquet I/O (no object columns).
_STRING_COLS: frozenset[str] = frozenset(
    {
        "experiment_id",
        "dgp",
        "graph_type",
        "target",
        "config_hash",
        "run_id",
        "outcome",
    }
)
_NULLABLE_STRING_COLS: frozenset[str] = frozenset({"failure_reason", "bridge_mode"})
_INT_COLS: frozenset[str] = frozenset(
    {
        "n",
        "seed",
        "folding_tokens_used",
        "n_delta_rules",
        "n_target_rules",
        "n_assumptions",
        "n_contraries",
        "n_trivial_target_rules",
        "n_nontrivial_target_rules",
        "max_body_length",
        "cov_py_tp",
        "cov_py_fp",
        "cov_py_tn",
        "cov_py_fn",
        "cov_pl_tp",
        "cov_pl_fp",
        "cov_pl_tn",
        "cov_pl_fn",
        "parser_unread_lines",
        "sol_file_bytes",
    }
)
_NULLABLE_INT_COLS: frozenset[str] = frozenset({"shd"})
_FLOAT_COLS: frozenset[str] = frozenset(
    col
    for col in RESULT_PARQUET_COLUMNS
    if col
    not in (
        _STRING_COLS | _NULLABLE_STRING_COLS | _INT_COLS | _NULLABLE_INT_COLS
    )
)


def _is_nan(value: Any) -> bool:
    """True if ``value`` is a float NaN."""
    return isinstance(value, float) and math.isnan(value)


def _parquet_scalar(col: str, value: Any) -> Any:
    """Coerce one panel value to the pinned Parquet dtype for column ``col``.

    Nullable string/int columns map missing values to ``pd.NA``; plain int
    columns default missing to 0 and float columns to NaN.
    """
    if col in _NULLABLE_STRING_COLS:
        if value is None or _is_nan(value):
            return pd.NA
        return str(value)
    if col in _STRING_COLS:
        return str(value)
    if col in _NULLABLE_INT_COLS:
        if value is None or _is_nan(value):
            return pd.NA
        return int(value)
    if col in _INT_COLS:
        if value is None or _is_nan(value):
            return 0
        return int(value)
    if col in _FLOAT_COLS:
        if value is None or _is_nan(value):
            return np.nan
        return float(value)
    raise KeyError(f"unknown parquet column: {col}")


def panel_to_parquet_row(panel: Mapping[str, Any]) -> dict[str, Any]:
    """Extract a typed row dict for Parquet from a compute_cell_metrics panel."""
    return {col: _parquet_scalar(col, panel[col]) for col in RESULT_PARQUET_COLUMNS}


def metrics_row_to_dataframe(row: Mapping[str, Any]) -> pd.DataFrame:
    """Build a single-row DataFrame with pinned dtypes."""
    data = panel_to_parquet_row(row)
    df = pd.DataFrame([data], columns=list(RESULT_PARQUET_COLUMNS))
    return enforce_results_dtypes(df)


def enforce_results_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Cast columns to pinned dtypes; reject object columns."""
    out = df.copy()
    for col in RESULT_PARQUET_COLUMNS:
        if col not in out.columns:
            out[col] = pd.NA
    out = out[list(RESULT_PARQUET_COLUMNS)]
    for col in _STRING_COLS | _NULLABLE_STRING_COLS:
        out[col] = out[col].astype("string")
    for col in _INT_COLS:
        out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0).astype("int64")
    for col in _NULLABLE_INT_COLS:
        out[col] = pd.to_numeric(out[col], errors="coerce").astype("Int64")
    for col in _FLOAT_COLS:
        out[col] = pd.to_numeric(out[col], errors="coerce").astype("float64")
    object_cols = [c for c in out.columns if out[c].dtype == object]
    if object_cols:
        raise TypeError(f"object-typed columns not allowed: {object_cols}")
    return out


def parquet_row_to_panel(row: pd.Series) -> dict[str, Any]:
    """Convert a Parquet row back to a metrics dict (Parquet columns only)."""
    panel: dict[str, Any] = {}
    for col in RESULT_PARQUET_COLUMNS:
        val = row[col]
        if col in _NULLABLE_STRING_COLS:
            panel[col] = None if pd.isna(val) else str(val)
            continue
        if col in _NULLABLE_INT_COLS:
            panel[col] = None if pd.isna(val) else int(val)
            continue
        if col in _STRING_COLS:
            panel[col] = str(val)
            continue
        if col in _INT_COLS:
            panel[col] = int(val)
            continue
        if col in _FLOAT_COLS:
            panel[col] = math.nan if pd.isna(val) else float(val)
            continue
    return panel


def _panel_for_json(panel: Mapping[str, Any]) -> dict[str, Any]:
    """JSON document: Parquet columns plus ``*_nan_reason`` keys when present."""
    doc: dict[str, Any] = {}
    for col in RESULT_PARQUET_COLUMNS:
        val = panel[col]
        if _is_nan(val):
            doc[col] = None
        else:
            doc[col] = val
    for key, val in panel.items():
        if key.endswith("_nan_reason"):
            doc[key] = val
    return doc


def write_cell_metrics(
    run_dir: Path,
    panel: Mapping[str, Any],
    *,
    context: Mapping[str, Any] | None = None,
) -> tuple[Path, Path]:
    """Write ``metrics.json`` and per-cell ``metrics.parquet`` shard."""
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    json_path = run_dir / "metrics.json"
    parquet_path = run_dir / "metrics.parquet"

    json_doc = _panel_for_json(panel)
    if context is not None:
        json_doc["context"] = dict(context)
    json_path.write_text(
        json.dumps(json_doc, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    df = metrics_row_to_dataframe(panel)
    df.to_parquet(parquet_path, index=False, engine="pyarrow")
    return json_path, parquet_path


def load_metrics_parquet_shard(path: Path) -> dict[str, Any]:
    """Load a single-cell Parquet shard as a metrics dict."""
    df = pd.read_parquet(path, engine="pyarrow")
    if len(df) != 1:
        raise ValueError(f"expected 1 row in shard {path}, got {len(df)}")
    df = enforce_results_dtypes(df)
    return parquet_row_to_panel(df.iloc[0])


def concat_shards(experiment_dir: Path) -> pd.DataFrame:
    """Concatenate all per-cell ``cells/<run_id>/metrics.parquet`` shards."""
    experiment_dir = Path(experiment_dir)
    cells_dir = experiment_dir / "cells"
    shard_paths = sorted(cells_dir.glob("*/metrics.parquet"))
    if not shard_paths:
        return enforce_results_dtypes(
            pd.DataFrame(columns=list(RESULT_PARQUET_COLUMNS))
        )
    frames = [pd.read_parquet(p, engine="pyarrow") for p in shard_paths]
    df = pd.concat(frames, ignore_index=True)
    return enforce_results_dtypes(df)


def write_results_parquet(experiment_dir: Path) -> Path:
    """Concatenate shards and write ``results.parquet`` at the experiment root."""
    experiment_dir = Path(experiment_dir)
    df = concat_shards(experiment_dir)
    out = experiment_dir / "results.parquet"
    df.to_parquet(out, index=False, engine="pyarrow")
    return out
