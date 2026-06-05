"""CLI and lifecycle tests for run_grid."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from concurrent.futures import Future

from causal.experiments.run_grid import (
    RunOptions,
    cell_is_done,
    grid_out_root,
    main,
    run_experiment,
    write_outcome_shard,
)
from causal.metrics import RESULT_PARQUET_COLUMNS

pytest.importorskip("pyarrow")


def _write_multi_stub(tmp_path: Path) -> Path:
    p = tmp_path / "E00_multi_stub.yaml"
    p.write_text(
        "\n".join(
            [
                "experiment_id: E00_multi_stub",
                "description: stub",
                "defaults:",
                "  graph_type: continuous",
                "  bins: 2",
                "  folding_steps: 15",
                "  prolog_timeout_s: 120",
                "  query_timeout_s: 5",
                "dgps:",
                "  - id: G3-chain",
                "    nodes: 3",
                "    edges: [[0,1],[1,2]]",
                "  - id: G3-fork",
                "    nodes: 3",
                "    edges: [[0,1],[0,2]]",
                "  - id: G3-collider",
                "    nodes: 3",
                "    edges: [[0,2],[1,2]]",
                "  - id: G4-forkchain",
                "    nodes: 4",
                "    edges: [[0,1],[0,2],[2,3]]",
                "  - id: G4-hub",
                "    nodes: 4",
                "    edges: [[0,1],[0,2],[0,3]]",
                "grid:",
                "  n: [25]",
                "  seed: { range: [0, 30] }",
                "  target: all",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return p


def test_dry_run_multi_stub_cell_count(capsys, tmp_path: Path) -> None:
    cfg_path = _write_multi_stub(tmp_path)
    code = main(["--config", str(cfg_path), "--dry-run"])
    captured = capsys.readouterr().out
    assert code == 0
    assert "510 cells planned" in captured


def test_limit_one_writes_single_cell_artefacts(tmp_path: Path, monkeypatch) -> None:
    cfg_path = _write_multi_stub(tmp_path)
    out_root = tmp_path / "grid" / "E00_multi_stub"
    monkeypatch.setattr(
        "causal.experiments.run_grid._GRID_ROOT",
        tmp_path / "grid",
    )

    call_count = 0

    def _fake_execute_cell(cell, run_dir, **kwargs):
        nonlocal call_count
        call_count += 1
        write_outcome_shard(
            cell,
            run_dir,
            graph_type="continuous",
            outcome="skipped",
            failure_reason="test stub",
        )
        from causal.experiments.run_grid import CellRunArtefacts

        mj = run_dir / "metrics.json"
        mp = run_dir / "metrics.parquet"
        return CellRunArtefacts(
            data_path=run_dir / "data.csv",
            data_binned_path=None,
            bk_path=None,
            sol_path=None,
            pos_examples=(),
            neg_examples=(),
            prolog_stdout="",
            prolog_stderr="",
            wall_clock_s=0.0,
            folding_tokens_used=0,
            outcome="skipped",
            failure_reason="test stub",
            metrics=json.loads(mj.read_text(encoding="utf-8")),
            metrics_json_path=mj,
            metrics_parquet_path=mp,
        )

    with patch("causal.experiments.run_grid.execute_cell", side_effect=_fake_execute_cell):
        code = run_experiment(
            RunOptions(config_path=cfg_path, limit=1, log_level="WARNING")
        )

    assert code == 0
    assert call_count == 1
    shards = list((out_root / "cells").glob("*/metrics.json"))
    assert len(shards) == 1
    assert (out_root / "results.parquet").is_file()


def test_resume_skips_second_run_zero_execute_calls(tmp_path: Path, monkeypatch) -> None:
    cfg_path = _write_multi_stub(tmp_path)
    monkeypatch.setattr(
        "causal.experiments.run_grid._GRID_ROOT",
        tmp_path / "grid",
    )

    call_count = 0

    def _fake_execute_cell(cell, run_dir, **kwargs):
        nonlocal call_count
        call_count += 1
        write_outcome_shard(
            cell,
            run_dir,
            graph_type="continuous",
            outcome="solved",
            failure_reason=None,
        )
        from causal.experiments.run_grid import CellRunArtefacts

        mj = run_dir / "metrics.json"
        mp = run_dir / "metrics.parquet"
        return CellRunArtefacts(
            data_path=run_dir / "data.csv",
            data_binned_path=None,
            bk_path=None,
            sol_path=None,
            pos_examples=(),
            neg_examples=(),
            prolog_stdout="",
            prolog_stderr="",
            wall_clock_s=1.0,
            folding_tokens_used=0,
            outcome="solved",
            failure_reason=None,
            metrics=json.loads(mj.read_text(encoding="utf-8")),
            metrics_json_path=mj,
            metrics_parquet_path=mp,
        )

    opts = RunOptions(config_path=cfg_path, limit=1, log_level="WARNING")
    with patch("causal.experiments.run_grid.execute_cell", side_effect=_fake_execute_cell):
        run_experiment(opts)
        first_calls = call_count
        run_experiment(opts)
        second_calls = call_count

    assert first_calls == 1
    assert second_calls == 1


def test_timeout_error_writes_timeout_outcome_shard(tmp_path: Path, monkeypatch) -> None:
    cfg_path = _write_multi_stub(tmp_path)
    monkeypatch.setattr(
        "causal.experiments.run_grid._GRID_ROOT",
        tmp_path / "grid",
    )

    def _timeout(*_a, **_k):
        raise TimeoutError("prolog wall clock exceeded")

    with patch("causal.experiments.run_grid.execute_cell", side_effect=_timeout):
        run_experiment(
            RunOptions(config_path=cfg_path, limit=1, log_level="WARNING")
        )

    out_root = tmp_path / "grid" / "E00_multi_stub"
    doc = json.loads(list((out_root / "cells").glob("*/metrics.json"))[0].read_text())
    assert doc["outcome"] == "timeout"
    assert "wall clock" in doc["failure_reason"]


def test_exception_writes_error_outcome_shard(tmp_path: Path, monkeypatch) -> None:
    cfg_path = _write_multi_stub(tmp_path)
    monkeypatch.setattr(
        "causal.experiments.run_grid._GRID_ROOT",
        tmp_path / "grid",
    )

    def _boom(*_a, **_k):
        raise RuntimeError("simulator failed")

    with patch("causal.experiments.run_grid.execute_cell", side_effect=_boom):
        run_experiment(
            RunOptions(config_path=cfg_path, limit=1, log_level="WARNING")
        )

    out_root = tmp_path / "grid" / "E00_multi_stub"
    metrics_paths = list((out_root / "cells").glob("*/metrics.json"))
    assert len(metrics_paths) == 1
    doc = json.loads(metrics_paths[0].read_text(encoding="utf-8"))
    assert doc["outcome"] == "error"
    assert "simulator failed" in doc["failure_reason"]
    for col in RESULT_PARQUET_COLUMNS:
        assert col in doc


def test_cell_is_done_requires_valid_json(tmp_path: Path) -> None:
    run_dir = tmp_path / "cell"
    run_dir.mkdir()
    assert not cell_is_done(run_dir)
    (run_dir / "metrics.json").write_text("{not json", encoding="utf-8")
    assert not cell_is_done(run_dir)
    (run_dir / "metrics.json").write_text('{"outcome": "solved"}', encoding="utf-8")
    assert cell_is_done(run_dir)


def test_run_log_created(tmp_path: Path, monkeypatch) -> None:
    cfg_path = _write_multi_stub(tmp_path)
    monkeypatch.setattr(
        "causal.experiments.run_grid._GRID_ROOT",
        tmp_path / "grid",
    )

    with patch(
        "causal.experiments.run_grid.execute_cell",
        side_effect=RuntimeError("fail"),
    ):
        run_experiment(
            RunOptions(config_path=cfg_path, limit=1, log_level="INFO")
        )

    log_path = tmp_path / "grid" / "E00_multi_stub" / "run.log"
    text = log_path.read_text(encoding="utf-8")
    assert log_path.is_file()
    assert "grid run started" in text
    assert "outcome=error" in text


def _fake_cell_run(cell, run_dir, **kwargs):
    write_outcome_shard(
        cell,
        run_dir,
        graph_type="continuous",
        outcome="solved",
        failure_reason=None,
        query_timeout_s=float(kwargs.get("query_timeout_s", 5.0)),
        skip_prolog_coverage=bool(kwargs.get("skip_prolog_coverage", False)),
    )
    from causal.experiments.run_grid import CellRunArtefacts

    mj = run_dir / "metrics.json"
    mp = run_dir / "metrics.parquet"
    return CellRunArtefacts(
        data_path=run_dir / "data.csv",
        data_binned_path=None,
        bk_path=None,
        sol_path=None,
        pos_examples=(),
        neg_examples=(),
        prolog_stdout="",
        prolog_stderr="",
        wall_clock_s=1.0,
        folding_tokens_used=0,
        outcome="solved",
        failure_reason=None,
        metrics=json.loads(mj.read_text(encoding="utf-8")),
        metrics_json_path=mj,
        metrics_parquet_path=mp,
    )


class _SyncProcessPool:
    """Run pool tasks in-process (for parallel worker tests without fork bombs)."""

    def __init__(self, max_workers=None, mp_context=None):
        self.max_workers = max_workers

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def submit(self, fn, payload):
        fut: Future = Future()
        try:
            fut.set_result(fn(payload))
        except Exception as e:
            fut.set_exception(e)
        return fut


def test_workers_two_limit_four_then_resume(tmp_path: Path, monkeypatch) -> None:
    cfg_path = _write_multi_stub(tmp_path)
    monkeypatch.setattr(
        "causal.experiments.run_grid._GRID_ROOT",
        tmp_path / "grid",
    )
    monkeypatch.setattr(
        "causal.experiments.run_grid.ProcessPoolExecutor",
        _SyncProcessPool,
    )

    call_count = 0

    def _fake_execute(cell, run_dir, **kwargs):
        nonlocal call_count
        call_count += 1
        return _fake_cell_run(cell, run_dir, **kwargs)

    opts = RunOptions(
        config_path=cfg_path,
        limit=4,
        workers=2,
        log_level="WARNING",
    )
    with patch("causal.experiments.run_grid.execute_cell", side_effect=_fake_execute):
        run_experiment(opts)
        assert call_count == 4
        first_calls = call_count
        run_experiment(opts)
        assert call_count == first_calls

    out_root = tmp_path / "grid" / "E00_multi_stub"
    assert len(list((out_root / "cells").glob("*/metrics.json"))) == 4


def test_skip_prolog_coverage_sets_nan_reason(tmp_path: Path, monkeypatch) -> None:
    cfg_path = _write_multi_stub(tmp_path)
    monkeypatch.setattr(
        "causal.experiments.run_grid._GRID_ROOT",
        tmp_path / "grid",
    )

    with patch(
        "causal.experiments.run_grid.execute_cell",
        side_effect=_fake_cell_run,
    ):
        run_experiment(
            RunOptions(
                config_path=cfg_path,
                limit=1,
                skip_prolog_coverage=True,
                log_level="WARNING",
            )
        )

    doc = json.loads(
        list((tmp_path / "grid" / "E00_multi_stub" / "cells").glob("*/metrics.json"))[
            0
        ].read_text(encoding="utf-8")
    )
    assert doc.get("cov_pl_accuracy_nan_reason") == "grid_skip_prolog_coverage"


def test_grid_out_root_under_repo() -> None:
    root = grid_out_root("E00_multi_stub")
    from causal.experiments.paths import repo_root

    rr = repo_root().resolve()
    assert rr in root.resolve().parents
    assert root.resolve() == (rr / "causal" / "outputs" / "aba_learning" / "grid" / "E00_multi_stub").resolve()
