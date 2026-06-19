from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from causal.experiments.config import CellSpec
from causal.experiments.run_grid import execute_cell_stage1


def _cell(*, seed: int) -> CellSpec:
    # Minimal cell for determinism checks (3-node chain).
    return CellSpec(
        experiment_id="test",
        dgp="G3-chain",
        nodes=3,
        edges=((0, 1), (1, 2)),
        n=12,
        seed=seed,
        target="x2",
        config_hash="sha256:test",
        run_id=f"run_{seed}",
        cell_dir_name=f"run_{seed}",
        graph_type="continuous",
        example_split="median",
    )


def _assert_frames_close(a: pd.DataFrame, b: pd.DataFrame) -> None:
    assert list(a.columns) == list(b.columns)
    assert a.shape == b.shape
    assert np.allclose(a.to_numpy(), b.to_numpy(), atol=1e-9, rtol=1e-9)


def _assert_frames_different(a: pd.DataFrame, b: pd.DataFrame) -> None:
    assert a.shape == b.shape
    assert not np.allclose(a.to_numpy(), b.to_numpy(), atol=1e-12, rtol=1e-12)


@pytest.mark.parametrize("graph_type", ["continuous", "discrete"])
def test_stage1_same_seed_reproducible(tmp_path: Path, graph_type: str) -> None:
    c1 = _cell(seed=42)
    c2 = _cell(seed=42)

    out1 = execute_cell_stage1(c1, tmp_path / "a", graph_type=graph_type)
    out2 = execute_cell_stage1(c2, tmp_path / "b", graph_type=graph_type)

    assert out1.data_path.is_file()
    assert out2.data_path.is_file()

    df1 = pd.read_csv(out1.data_path)
    df2 = pd.read_csv(out2.data_path)
    _assert_frames_close(df1, df2)


@pytest.mark.parametrize("graph_type", ["continuous", "discrete"])
def test_stage1_different_seed_differs(tmp_path: Path, graph_type: str) -> None:
    c1 = _cell(seed=42)
    c2 = _cell(seed=43)

    out1 = execute_cell_stage1(c1, tmp_path / "a", graph_type=graph_type)
    out2 = execute_cell_stage1(c2, tmp_path / "b", graph_type=graph_type)

    df1 = pd.read_csv(out1.data_path)
    df2 = pd.read_csv(out2.data_path)
    _assert_frames_different(df1, df2)


def test_stage1_smoke_writes_csv(tmp_path: Path) -> None:
    cell = _cell(seed=7)
    out = execute_cell_stage1(cell, tmp_path / "cell", graph_type="continuous")
    assert out.data_path.exists()
    df = pd.read_csv(out.data_path)
    assert df.shape == (cell.n, cell.nodes)

