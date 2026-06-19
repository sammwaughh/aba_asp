from __future__ import annotations

import argparse
import json
import logging
import multiprocessing
import shutil
import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

import numpy as np
import pandas as pd

# Ensure ArgCausalDisco is importable when running from repo root.
_THIS_DIR = Path(__file__).resolve().parent
from causal.experiments.paths import grid_root, repo_root

_REPO_ROOT = repo_root()
# ArgCausalDisco is a sibling directory of the repo root in this workspace.
# To import `ArgCausalDisco.*`, sys.path must include the directory that contains
# the `ArgCausalDisco/` folder (i.e. the parent of repo root).
_WORKSPACE_ROOT = _REPO_ROOT.parent
_ARGCAUSALDISCO_ROOT = _WORKSPACE_ROOT / "ArgCausalDisco"
for _p in (_REPO_ROOT, _WORKSPACE_ROOT, _ARGCAUSALDISCO_ROOT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from ArgCausalDisco.utils.data_utils import (  # type: ignore  # noqa: E402
    simulate_discrete_data,
    simulate_linear_continuous_data,
)

from causal.argcausaldisco_integration import (
    generate_aba_background_knowledge,
    pick_target_variable,
)
from causal.experiments.config import CellSpec, ExperimentConfig, expand_cells, load_config
from causal.experiments.dgp import get_dgp
from causal.experiments.handcrafted import load_handcrafted
from causal.metrics import GroundTruth
from causal.experiments.manifest import close_manifest, open_manifest
from causal.experiments.results import write_cell_metrics, write_results_parquet
from causal.metrics import CellInputs, compute_cell_metrics, outcome_classifier, parse_folding_tokens_used
from causal.run_aba_asp import ABASPRunner

_GRID_ROOT = grid_root()
_RUN_LOGGER = logging.getLogger("causal.experiments.run_grid")


GraphType = Literal["discrete", "continuous", "handcrafted_table"]


def ground_truth_for_cell(cell: CellSpec) -> GroundTruth:
    """Ground truth for a cell (zoo DGP or handcrafted / config edges)."""
    try:
        return get_dgp(cell.dgp).ground_truth()
    except KeyError:
        names = tuple(f"x{i}" for i in range(cell.nodes))
        edge_names = frozenset((f"x{s}", f"x{t}") for s, t in cell.edges)
        return GroundTruth(nodes=names, edges=edge_names)


@dataclass(frozen=True)
class Stage1Artefacts:
    """Artefacts produced by execute_cell stage 1 only."""

    data_path: Path
    df: pd.DataFrame


def execute_cell_stage1(
    cell: CellSpec,
    run_dir: Path,
    *,
    graph_type: GraphType,
    noise_type: str = "gaussian",
) -> Stage1Artefacts:
    """Stage 1 of execute_cell: simulate and write `data.csv` (INFRA.md §4.3)."""
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)

    # Explicit per-cell RNG construction (even if simulator uses seed int).
    _ = np.random.RandomState(cell.seed)

    edges_set = set(cell.edges)
    if graph_type == "handcrafted_table":
        source = cell.handcrafted_source
        if source is None:
            raise ValueError(f"handcrafted cell {cell.run_id} missing handcrafted_source")
        fx = load_handcrafted(source)
        df = fx.df.copy()
        data_path = run_dir / "data.csv"
        df.to_csv(data_path, index=False)
        return Stage1Artefacts(data_path=data_path, df=df)

    if graph_type == "discrete":
        data = simulate_discrete_data(
            num_of_nodes=cell.nodes,
            sample_size=cell.n,
            truth_DAG_directed_edges=edges_set,
            random_seed=cell.seed,
        )
    elif graph_type == "continuous":
        data = simulate_linear_continuous_data(
            num_of_nodes=cell.nodes,
            sample_size=cell.n,
            truth_DAG_directed_edges=edges_set,
            noise_type=noise_type,
            random_seed=cell.seed,
        )
    else:  # pragma: no cover
        raise ValueError(f"Unknown graph_type: {graph_type}")

    cols = [f"x{i}" for i in range(cell.nodes)]
    df = pd.DataFrame(data, columns=cols)
    data_path = run_dir / "data.csv"
    df.to_csv(data_path, index=False)
    return Stage1Artefacts(data_path=data_path, df=df)


@dataclass(frozen=True)
class Stage2Artefacts:
    """Artefacts produced by execute_cell stage 2 (stage 1 + BK + examples)."""

    data_path: Path
    bk_path: Path | None
    data_binned_path: Path | None
    pos_examples: tuple[str, ...]
    neg_examples: tuple[str, ...]
    outcome: str  # solved|... exists later; stage2 uses 'skipped' or 'ok'
    failure_reason: str | None


def _median_examples(df: pd.DataFrame, *, target: str) -> tuple[list[str], list[str]]:
    """Split samples into E+/E- by a median threshold on the target column.

    Samples with ``target >= median`` become positive example atoms
    (``target(i)``, 1-indexed); the rest become negative atoms. Used for the
    continuous regime.
    """
    median_val = float(df[target].median())
    pos = [f"{target}({i + 1})" for i in df.index if float(df[target].iloc[i]) >= median_val]
    neg = [f"{target}({i + 1})" for i in df.index if float(df[target].iloc[i]) < median_val]
    return pos, neg


def _examples_for_cell(
    df: pd.DataFrame,
    *,
    cell: CellSpec,
    graph_type: GraphType,
    example_split: str,
) -> tuple[list[str], list[str]]:
    """Build the positive/negative example atoms for a cell.

    Dispatches on ``graph_type``: continuous uses a median split, discrete uses
    ``pick_target_variable``, and handcrafted tables return the fixture's fixed
    examples. Returns ``(pos_atoms, neg_atoms)``.
    """
    target = cell.target
    if graph_type == "continuous":
        if example_split != "median":
            raise NotImplementedError(
                f"example_split={example_split!r} is not supported for continuous "
                "data; use 'median'"
            )
        return _median_examples(df, target=target)

    if graph_type == "handcrafted_table":
        source = cell.handcrafted_source
        if source is None:
            raise ValueError("handcrafted_table requires handcrafted_source on cell")
        fx = load_handcrafted(source)
        if target != fx.default_target:
            raise ValueError(
                f"handcrafted fixture {source!r} only supports target {fx.default_target}"
            )
        return list(fx.pos_examples), list(fx.neg_examples)

    if graph_type == "discrete":
        if example_split not in ("median", "pick_target_variable"):
            raise NotImplementedError(
                f"example_split={example_split!r} is not supported for discrete "
                "data; use 'pick_target_variable' or 'median'"
            )
        picked, pos, neg = pick_target_variable(df, target)
        if picked != target:
            raise ValueError(f"pick_target_variable returned {picked}, expected {target}")
        return pos, neg

    raise ValueError(f"unsupported graph_type for examples: {graph_type}")


def execute_cell_stage2(
    cell: CellSpec,
    run_dir: Path,
    *,
    graph_type: GraphType,
    bins: int = 2,
    bin_strategy: str = "quantile",
    example_split: str = "median",
    noise_type: str = "gaussian",
) -> Stage2Artefacts:
    """Stage 2 of execute_cell: BK generation + E+/E- builders (INFRA.md §4.3)."""
    stage1 = execute_cell_stage1(cell, run_dir, graph_type=graph_type, noise_type=noise_type)

    # Build examples first so we can skip without producing BK when split is empty.
    pos, neg = _examples_for_cell(
        stage1.df,
        cell=cell,
        graph_type=graph_type,
        example_split=example_split,
    )
    if not pos or not neg:
        return Stage2Artefacts(
            data_path=stage1.data_path,
            bk_path=None,
            data_binned_path=None,
            pos_examples=tuple(pos),
            neg_examples=tuple(neg),
            outcome="skipped",
            failure_reason="empty E+ or E-",
        )

    if graph_type == "handcrafted_table":
        fx = load_handcrafted(cell.handcrafted_source or "")
        var_types = dict(fx.var_types)
    else:
        var_types = {
            f"x{i}": ("continuous" if graph_type == "continuous" else "categorical")
            for i in range(cell.nodes)
        }
    name = cell.run_id
    bk_generated = generate_aba_background_knowledge(
        stage1.df,
        var_types=var_types,
        name=name,
        output_dir=Path(run_dir),
        exclude_cols=[cell.target],
        continuous_bins=bins,
        bin_strategy=bin_strategy,
    )

    # Normalise filenames to the runner's artefact layout.
    bk_path = Path(run_dir) / "bk.aba"
    bk_generated.replace(bk_path)

    binned_src = Path(run_dir) / f"{name}.binned.csv"
    binned_dst = Path(run_dir) / "data.binned.csv"
    if graph_type == "continuous" and binned_src.exists():
        binned_src.replace(binned_dst)
        data_binned_path: Path | None = binned_dst
    else:
        data_binned_path = None

    return Stage2Artefacts(
        data_path=stage1.data_path,
        bk_path=bk_path,
        data_binned_path=data_binned_path,
        pos_examples=tuple(pos),
        neg_examples=tuple(neg),
        outcome="ok",
        failure_reason=None,
    )


@dataclass(frozen=True)
class Stage3Artefacts:
    """Artefacts produced by execute_cell stage 3 (Prolog + classification)."""

    data_path: Path
    data_binned_path: Path | None
    bk_path: Path | None
    sol_path: Path | None
    pos_examples: tuple[str, ...]
    neg_examples: tuple[str, ...]
    prolog_stdout: str
    prolog_stderr: str
    wall_clock_s: float
    folding_tokens_used: int
    outcome: str  # one of the METRICS categories
    failure_reason: str | None


def _sol_candidate_paths(bk_path: Path) -> list[Path]:
    """Candidate solution paths for a BK file (cell-local first, then shared root)."""
    from causal.argcausaldisco_integration import ABA_ASP_ROOT

    base = bk_path.stem
    run_dir = Path(bk_path).parent
    return [
        run_dir / f"{base}.bk.sol.aba",
        run_dir / f"{base}.sol.aba",
        run_dir / "bk.sol.aba",
        ABA_ASP_ROOT / f"{base}.bk.sol.aba",
        ABA_ASP_ROOT / f"{base}.sol.aba",
    ]


def _extract_sol_path(bk_path: Path) -> Path | None:
    """Locate the produced solution file (prefer per-cell ``run_dir``)."""
    for c in _sol_candidate_paths(bk_path):
        if c.is_file():
            return c
    return None


def _relocate_sol_artefacts(bk_path: Path) -> None:
    """Copy solution files from shared ``ABA_ASP_ROOT`` into the cell directory.

    ABA-ASP may write ``{stem}.bk.sol.aba`` under the repo root; parallel workers
    would otherwise race on the same basename. After relocation, each cell reads
    only files under ``cells/<run_id>/``.
    """
    from causal.argcausaldisco_integration import ABA_ASP_ROOT

    run_dir = Path(bk_path).parent
    base = bk_path.stem
    shared_names = (f"{base}.bk.sol.aba", f"{base}.sol.aba")
    for name in shared_names:
        src = ABA_ASP_ROOT / name
        if not src.is_file():
            continue
        dest = run_dir / name
        if src.resolve() != dest.resolve():
            shutil.copy2(src, dest)
            try:
                src.unlink()
            except OSError:
                pass
    canonical = run_dir / "bk.sol.aba"
    primary = run_dir / f"{base}.bk.sol.aba"
    if primary.is_file() and not canonical.exists():
        shutil.copy2(primary, canonical)


def execute_cell_stage3(
    cell: CellSpec,
    stage2: Stage2Artefacts,
    run_dir: Path,
    *,
    folding_steps: int = 15,
    folding_mode: str = "nd",
    prolog_timeout_s: float = 120.0,
) -> Stage3Artefacts:
    """Stage 3 of execute_cell: run Prolog learning + outcome classification."""
    run_dir = Path(run_dir)

    if stage2.outcome != "ok":
        # Skip Prolog; propagate the earlier skip.
        return Stage3Artefacts(
            data_path=stage2.data_path,
            data_binned_path=stage2.data_binned_path,
            bk_path=stage2.bk_path,
            sol_path=None,
            pos_examples=stage2.pos_examples,
            neg_examples=stage2.neg_examples,
            prolog_stdout="",
            prolog_stderr="",
            wall_clock_s=0.0,
            folding_tokens_used=0,
            outcome=stage2.outcome,
            failure_reason=stage2.failure_reason,
        )

    if stage2.bk_path is None:
        raise ValueError("stage2 outcome=ok requires bk_path")

    prolog_out = run_dir / "prolog.stdout"
    prolog_err = run_dir / "prolog.stderr"
    prolog_out.parent.mkdir(parents=True, exist_ok=True)

    runner = ABASPRunner()
    if not runner.prolog_available:
        raise RuntimeError("SWI-Prolog not available; cannot run stage 3")

    # Invoke ABA-ASP via Prolog.
    learning_options = {
        "folding_steps": str(folding_steps),
        "folding_mode": folding_mode,
    }

    import time

    t0 = time.monotonic()
    try:
        result = runner.run_prolog_aba_asp(
            stage2.bk_path,
            positive_examples=list(stage2.pos_examples),
            negative_examples=list(stage2.neg_examples),
            learning_options=learning_options,
            timeout_s=prolog_timeout_s,
        )
    except TimeoutError as e:
        t1 = time.monotonic()
        wall = t1 - t0
        prolog_out.write_text("", encoding="utf-8")
        prolog_err.write_text(str(e), encoding="utf-8")
        return Stage3Artefacts(
            data_path=stage2.data_path,
            data_binned_path=stage2.data_binned_path,
            bk_path=stage2.bk_path,
            sol_path=None,
            pos_examples=stage2.pos_examples,
            neg_examples=stage2.neg_examples,
            prolog_stdout="",
            prolog_stderr=str(e),
            wall_clock_s=wall,
            folding_tokens_used=0,
            outcome="timeout",
            failure_reason=str(e),
        )
    t1 = time.monotonic()

    stdout = result.get("stdout", "") or ""
    stderr = result.get("stderr", "") or ""

    prolog_out.write_text(stdout, encoding="utf-8")
    prolog_err.write_text(stderr, encoding="utf-8")

    _relocate_sol_artefacts(stage2.bk_path)
    sol_path = _extract_sol_path(stage2.bk_path)

    # Learned delta rules (used by outcome_classifier).
    from causal.argcausaldisco_integration import _extract_learned_rules

    learned_rules = _extract_learned_rules(stage2.bk_path)

    examples_ok = bool(stage2.pos_examples) and bool(stage2.neg_examples)
    outcome, failure_reason = outcome_classifier(
        stdout=stdout,
        sol_path=sol_path,
        learned_rules=learned_rules,
        wall_clock_s=t1 - t0,
        timeout_s=prolog_timeout_s,
        examples_ok=examples_ok,
    )

    folding_tokens_used = parse_folding_tokens_used(stdout)

    return Stage3Artefacts(
        data_path=stage2.data_path,
        data_binned_path=stage2.data_binned_path,
        bk_path=stage2.bk_path,
        sol_path=sol_path,
        pos_examples=stage2.pos_examples,
        neg_examples=stage2.neg_examples,
        prolog_stdout=stdout,
        prolog_stderr=stderr,
        wall_clock_s=t1 - t0,
        folding_tokens_used=folding_tokens_used,
        outcome=outcome,
        failure_reason=failure_reason,
    )


@dataclass(frozen=True)
class CellRunArtefacts:
    """Full cell run: stages 1–3 artefacts plus written metrics."""

    data_path: Path
    data_binned_path: Path | None
    bk_path: Path | None
    sol_path: Path | None
    pos_examples: tuple[str, ...]
    neg_examples: tuple[str, ...]
    prolog_stdout: str
    prolog_stderr: str
    wall_clock_s: float
    folding_tokens_used: int
    outcome: str
    failure_reason: str | None
    metrics: dict
    metrics_json_path: Path
    metrics_parquet_path: Path


def execute_cell_stage4(
    cell: CellSpec,
    stage3: Stage3Artefacts,
    run_dir: Path,
    *,
    graph_type: GraphType,
    query_timeout_s: float = 5.0,
    skip_prolog_coverage: bool = False,
) -> CellRunArtefacts:
    """Stage 4: compute metrics panel and write per-cell JSON + Parquet shard."""
    run_dir = Path(run_dir)
    gt = ground_truth_for_cell(cell)
    bk_path = stage3.bk_path if stage3.bk_path is not None else run_dir / "bk.aba"

    inp = CellInputs(
        experiment_id=cell.experiment_id,
        dgp=cell.dgp,
        graph_type=graph_type,
        target=cell.target,
        n=cell.n,
        seed=cell.seed,
        config_hash=cell.config_hash,
        run_id=cell.run_id,
        bk_path=Path(bk_path),
        sol_path=stage3.sol_path,
        pos_examples=stage3.pos_examples,
        neg_examples=stage3.neg_examples,
        ground_truth=gt,
        wall_clock_s=stage3.wall_clock_s,
        outcome=stage3.outcome,
        failure_reason=stage3.failure_reason,
        folding_tokens_used=stage3.folding_tokens_used,
        query_timeout_s=query_timeout_s,
        skip_prolog_coverage=skip_prolog_coverage,
    )
    panel = compute_cell_metrics(inp)
    metrics_json_path, metrics_parquet_path = write_cell_metrics(run_dir, panel)

    return CellRunArtefacts(
        data_path=stage3.data_path,
        data_binned_path=stage3.data_binned_path,
        bk_path=stage3.bk_path,
        sol_path=stage3.sol_path,
        pos_examples=stage3.pos_examples,
        neg_examples=stage3.neg_examples,
        prolog_stdout=stage3.prolog_stdout,
        prolog_stderr=stage3.prolog_stderr,
        wall_clock_s=stage3.wall_clock_s,
        folding_tokens_used=stage3.folding_tokens_used,
        outcome=stage3.outcome,
        failure_reason=stage3.failure_reason,
        metrics=panel,
        metrics_json_path=metrics_json_path,
        metrics_parquet_path=metrics_parquet_path,
    )


def execute_cell(
    cell: CellSpec,
    run_dir: Path,
    *,
    graph_type: GraphType | None = None,
    bins: int = 2,
    bin_strategy: str = "quantile",
    example_split: str | None = None,
    folding_steps: int = 15,
    folding_mode: str = "nd",
    prolog_timeout_s: float = 120.0,
    noise_type: str = "gaussian",
    query_timeout_s: float = 5.0,
    skip_prolog_coverage: bool = False,
) -> CellRunArtefacts:
    """Convenience: stages 1→2→3→4 for a single learning cell."""
    resolved_graph_type: GraphType = graph_type or cell.graph_type  # type: ignore[assignment]
    resolved_example_split = (
        example_split if example_split is not None else cell.example_split
    )
    stage2 = execute_cell_stage2(
        cell,
        run_dir,
        graph_type=resolved_graph_type,
        bins=bins,
        bin_strategy=bin_strategy,
        example_split=resolved_example_split,
        noise_type=noise_type,
    )
    stage3 = execute_cell_stage3(
        cell,
        stage2,
        run_dir,
        folding_steps=folding_steps,
        folding_mode=folding_mode,
        prolog_timeout_s=prolog_timeout_s,
    )
    return execute_cell_stage4(
        cell,
        stage3,
        run_dir,
        graph_type=resolved_graph_type,
        query_timeout_s=query_timeout_s,
        skip_prolog_coverage=skip_prolog_coverage,
    )


@dataclass(frozen=True)
class RunOptions:
    """CLI options for ``run_experiment`` (INFRA.md §4.1)."""

    config_path: Path
    dry_run: bool = False
    limit: int | None = None
    only_target: str | None = None
    only_dgp: str | None = None
    force: bool = False
    no_resume: bool = False
    workers: int = 1
    log_level: str = "INFO"
    skip_prolog_coverage: bool = False


def grid_out_root(experiment_id: str) -> Path:
    """Return the output directory for an experiment's grid run."""
    return _GRID_ROOT / experiment_id


def filter_cells(
    cells: list[CellSpec],
    *,
    only_target: str | None = None,
    only_dgp: str | None = None,
) -> list[CellSpec]:
    """Subset ``cells`` to a single target and/or DGP (``--only-*`` CLI flags)."""
    out = cells
    if only_dgp is not None:
        out = [c for c in out if c.dgp == only_dgp]
    if only_target is not None:
        out = [c for c in out if c.target == only_target]
    return out


def cell_is_done(run_dir: Path, *, config_hash: str | None = None) -> bool:
    """True when ``metrics.json`` exists, parses, and matches ``config_hash`` if given."""
    path = Path(run_dir) / "metrics.json"
    if not path.is_file():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    if config_hash is not None:
        stored = data.get("config_hash")
        if stored != config_hash:
            return False
    return True


def _execute_kwargs(cfg: ExperimentConfig) -> dict[str, Any]:
    """Extract the ``execute_cell`` keyword arguments from a config's defaults."""
    d = cfg.defaults
    return {
        "bins": int(d.get("bins", 2)),
        "bin_strategy": str(d.get("bin_strategy", "quantile")),
        "example_split": str(d.get("example_split", "median")),
        "folding_steps": int(d.get("folding_steps", 15)),
        "folding_mode": str(d.get("folding_mode", "nd")),
        "prolog_timeout_s": float(d.get("prolog_timeout_s", 120.0)),
        "query_timeout_s": float(d.get("query_timeout_s", 5.0)),
        "noise_type": str(d.get("noise_type", "gaussian")),
    }


@dataclass(frozen=True)
class CellJobResult:
    """Outcome of one grid cell (serial or parallel worker)."""

    run_id: str
    dgp: str
    target: str
    seed: int
    outcome: str
    failure_reason: str | None


def write_outcome_shard(
    cell: CellSpec,
    run_dir: Path,
    *,
    graph_type: GraphType,
    outcome: str,
    failure_reason: str | None,
    wall_clock_s: float = 0.0,
    bk_path: Path | None = None,
    sol_path: Path | None = None,
    pos_examples: tuple[str, ...] = (),
    neg_examples: tuple[str, ...] = (),
    folding_tokens_used: int = 0,
    query_timeout_s: float = 5.0,
    skip_prolog_coverage: bool = False,
) -> tuple[Path, Path]:
    """Write metrics artefacts for timeout/error outcomes (INFRA.md §4.6)."""
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    gt = ground_truth_for_cell(cell)
    resolved_bk = Path(bk_path if bk_path is not None else run_dir / "bk.aba")
    if not resolved_bk.is_file():
        resolved_bk.write_text("", encoding="utf-8")
    inp = CellInputs(
        experiment_id=cell.experiment_id,
        dgp=cell.dgp,
        graph_type=graph_type,
        target=cell.target,
        n=cell.n,
        seed=cell.seed,
        config_hash=cell.config_hash,
        run_id=cell.run_id,
        bk_path=resolved_bk,
        sol_path=sol_path,
        pos_examples=pos_examples,
        neg_examples=neg_examples,
        ground_truth=gt,
        wall_clock_s=wall_clock_s,
        outcome=outcome,
        failure_reason=failure_reason,
        folding_tokens_used=folding_tokens_used,
        query_timeout_s=query_timeout_s,
        skip_prolog_coverage=skip_prolog_coverage,
    )
    panel = compute_cell_metrics(inp)
    return write_cell_metrics(run_dir, panel)


def _metrics_write_kwargs(
    exec_kwargs: dict[str, Any],
    *,
    skip_prolog_coverage: bool,
) -> dict[str, Any]:
    """Subset of kwargs needed when writing timeout/error metric shards."""
    return {
        "query_timeout_s": float(exec_kwargs.get("query_timeout_s", 5.0)),
        "skip_prolog_coverage": skip_prolog_coverage,
    }


def _run_single_cell(
    cell: CellSpec,
    run_dir: Path,
    *,
    exec_kwargs: dict[str, Any],
    skip_prolog_coverage: bool,
) -> CellJobResult:
    """Execute one cell (used serially and from process workers)."""
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    cell_graph_type: GraphType = cell.graph_type  # type: ignore[assignment]
    run_kw = {**exec_kwargs, "skip_prolog_coverage": skip_prolog_coverage}
    shard_kw = _metrics_write_kwargs(
        exec_kwargs, skip_prolog_coverage=skip_prolog_coverage
    )
    try:
        result = execute_cell(cell, run_dir, **run_kw)
        return CellJobResult(
            run_id=cell.run_id,
            dgp=cell.dgp,
            target=cell.target,
            seed=cell.seed,
            outcome=result.outcome,
            failure_reason=result.failure_reason,
        )
    except TimeoutError as e:
        wall = float(exec_kwargs.get("prolog_timeout_s", 120.0))
        write_outcome_shard(
            cell,
            run_dir,
            graph_type=cell_graph_type,
            outcome="timeout",
            failure_reason=str(e),
            wall_clock_s=wall,
            **shard_kw,
        )
        return CellJobResult(
            run_id=cell.run_id,
            dgp=cell.dgp,
            target=cell.target,
            seed=cell.seed,
            outcome="timeout",
            failure_reason=str(e),
        )
    except Exception as e:
        write_outcome_shard(
            cell,
            run_dir,
            graph_type=cell_graph_type,
            outcome="error",
            failure_reason=repr(e),
            **shard_kw,
        )
        return CellJobResult(
            run_id=cell.run_id,
            dgp=cell.dgp,
            target=cell.target,
            seed=cell.seed,
            outcome="error",
            failure_reason=repr(e),
        )


def _cell_spec_from_dict(data: dict[str, Any]) -> CellSpec:
    """Rebuild a ``CellSpec`` from its ``asdict`` form (used by process workers)."""
    edges_raw = data["edges"]
    edges = tuple(tuple(e) for e in edges_raw)
    return CellSpec(
        experiment_id=str(data["experiment_id"]),
        dgp=str(data["dgp"]),
        nodes=int(data["nodes"]),
        edges=edges,
        n=int(data["n"]),
        seed=int(data["seed"]),
        target=str(data["target"]),
        config_hash=str(data["config_hash"]),
        run_id=str(data["run_id"]),
        cell_dir_name=str(data["cell_dir_name"]),
        graph_type=str(data["graph_type"]),
        example_split=str(data["example_split"]),
        handcrafted_source=data.get("handcrafted_source"),
    )


def _grid_worker_run_cell(payload: dict[str, Any]) -> CellJobResult:
    """Process-pool entry point (picklable; macOS spawn-safe)."""
    cell = _cell_spec_from_dict(payload["cell"])
    return _run_single_cell(
        cell,
        Path(payload["run_dir"]),
        exec_kwargs=payload["exec_kwargs"],
        skip_prolog_coverage=bool(payload["skip_prolog_coverage"]),
    )


def _log_cell_result(result: CellJobResult) -> None:
    """Log a finished cell: WARN for any non-solved outcome, INFO otherwise."""
    if result.outcome != "solved":
        _RUN_LOGGER.warning(
            "finish %s %s target=%s seed=%s outcome=%s reason=%s",
            result.dgp,
            result.run_id,
            result.target,
            result.seed,
            result.outcome,
            result.failure_reason,
        )
    else:
        _RUN_LOGGER.info(
            "finish %s %s target=%s seed=%s outcome=%s",
            result.dgp,
            result.run_id,
            result.target,
            result.seed,
            result.outcome,
        )


def setup_run_logging(out_root: Path, *, log_level: str) -> None:
    """Configure file logging to ``run.log`` (INFRA.md §11)."""
    out_root = Path(out_root)
    out_root.mkdir(parents=True, exist_ok=True)
    log_path = out_root / "run.log"

    level = getattr(logging, log_level.upper(), logging.INFO)
    _RUN_LOGGER.setLevel(level)
    _RUN_LOGGER.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    file_handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    _RUN_LOGGER.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(level)
    _RUN_LOGGER.addHandler(stream_handler)

    started = datetime.now(timezone.utc).isoformat()
    _RUN_LOGGER.info("=== grid run started at %s ===", started)


def run_experiment(opts: RunOptions) -> int:
    """Run (or dry-run) an experiment grid."""
    config_path = Path(opts.config_path).resolve()
    cfg = load_config(config_path)
    cells = expand_cells(cfg, config_path=config_path)
    cells = filter_cells(
        cells, only_target=opts.only_target, only_dgp=opts.only_dgp
    )

    if opts.dry_run:
        print(f"{len(cells)} cells planned for {cfg.experiment_id}")
        return 0

    out_root = grid_out_root(cfg.experiment_id)
    setup_run_logging(out_root, log_level=opts.log_level)
    workers = max(1, int(opts.workers))
    if workers > 1:
        _RUN_LOGGER.info(
            "parallel mode: workers=%s (cells run in separate processes; "
            "per-cell wall-clock order is not deterministic)",
            workers,
        )
    if opts.skip_prolog_coverage:
        _RUN_LOGGER.warning(
            "--skip-prolog-coverage: cov_pl_* / cov_gap_* will be NaN "
            "(one SWI-Prolog pass per cell only)"
        )
    open_manifest(
        out_root,
        cfg=cfg,
        config_path=config_path,
        n_cells_planned=len(cells),
        repo_root=_REPO_ROOT,
    )

    exec_kwargs = _execute_kwargs(cfg)
    outcome_counts: Counter[str] = Counter()
    n_completed = 0
    n_skipped = 0
    to_run = cells if opts.limit is None else cells[: opts.limit]
    pending: list[tuple[CellSpec, Path]] = []
    for cell in to_run:
        run_dir = out_root / "cells" / cell.cell_dir_name
        if cell_is_done(run_dir, config_hash=cell.config_hash) and not opts.no_resume:
            n_skipped += 1
            _RUN_LOGGER.info(
                "skip %s dir=%s target=%s seed=%s (resume)",
                cell.dgp,
                cell.cell_dir_name,
                cell.target,
                cell.seed,
            )
            continue
        pending.append((cell, run_dir))

    job_payloads = [
        {
            "cell": asdict(cell),
            "run_dir": str(run_dir),
            "exec_kwargs": exec_kwargs,
            "skip_prolog_coverage": opts.skip_prolog_coverage,
        }
        for cell, run_dir in pending
    ]

    for cell, run_dir in pending:
        _RUN_LOGGER.info(
            "start %s dir=%s run_id=%s target=%s seed=%s n=%s",
            cell.dgp,
            cell.cell_dir_name,
            cell.run_id,
            cell.target,
            cell.seed,
            cell.n,
        )

    if workers <= 1:
        for cell, run_dir in pending:
            job_result = _run_single_cell(
                cell,
                run_dir,
                exec_kwargs=exec_kwargs,
                skip_prolog_coverage=opts.skip_prolog_coverage,
            )
            n_completed += 1
            outcome_counts[job_result.outcome] += 1
            _log_cell_result(job_result)
    else:
        ctx = multiprocessing.get_context("spawn")
        with ProcessPoolExecutor(max_workers=workers, mp_context=ctx) as pool:
            futures = {
                pool.submit(_grid_worker_run_cell, payload): payload
                for payload in job_payloads
            }
            for fut in as_completed(futures):
                job_result = fut.result()
                n_completed += 1
                outcome_counts[job_result.outcome] += 1
                _log_cell_result(job_result)

    write_results_parquet(out_root)
    close_manifest(
        out_root,
        n_cells_completed=n_completed,
        n_cells_skipped=n_skipped,
        outcome_counts=dict(outcome_counts),
    )
    _RUN_LOGGER.info(
        "done: completed=%s skipped=%s outcomes=%s",
        n_completed,
        n_skipped,
        dict(outcome_counts),
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="ABA-ASP experiment grid runner")
    p.add_argument(
        "--config",
        required=True,
        type=Path,
        help="Path to experiment YAML config",
    )
    p.add_argument("--dry-run", action="store_true", help="Print cell count and exit")
    p.add_argument("--limit", type=int, default=None, metavar="N")
    p.add_argument("--only-target", type=str, default=None, metavar="x2")
    p.add_argument("--only-dgp", type=str, default=None, metavar="G3-chain")
    p.add_argument(
        "--force",
        action="store_true",
        help="Reserved flag; currently a no-op (the runner does not refuse a dirty tree).",
    )
    p.add_argument(
        "--no-resume",
        action="store_true",
        help="Re-run cells even when metrics.json exists",
    )
    p.add_argument(
        "--workers",
        type=int,
        default=1,
        metavar="N",
        help="Process pool size for parallel cells (default 1 = serial)",
    )
    p.add_argument(
        "--skip-prolog-coverage",
        action="store_true",
        help="Skip prolog_aware_coverage (second SWI-Prolog pass per cell)",
    )
    p.add_argument("--log-level", type=str, default="INFO")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    opts = RunOptions(
        config_path=args.config,
        dry_run=args.dry_run,
        limit=args.limit,
        only_target=args.only_target,
        only_dgp=args.only_dgp,
        force=args.force,
        no_resume=args.no_resume,
        workers=args.workers,
        log_level=args.log_level,
        skip_prolog_coverage=args.skip_prolog_coverage,
    )
    return run_experiment(opts)


if __name__ == "__main__":
    raise SystemExit(main())

