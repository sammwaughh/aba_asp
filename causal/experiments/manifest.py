from __future__ import annotations

import json
import os
import platform
import socket
import subprocess
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from causal.experiments.config import ExperimentConfig, config_hash_from_path
from causal.run_aba_asp import SWIPL_PATH


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _git_commit(repo_root: Path) -> tuple[str | None, bool]:
    """Return (commit, dirty). If git unavailable, returns (None, False)."""
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=str(repo_root), text=True
        ).strip()
        status = subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=str(repo_root), text=True
        )
        dirty = bool(status.strip())
        return commit, dirty
    except Exception:
        return None, False


def _swipl_version() -> str | None:
    if not SWIPL_PATH:
        return None
    try:
        out = subprocess.check_output([SWIPL_PATH, "--version"], text=True, timeout=5).strip()
        return out
    except Exception:
        return None


def open_manifest(
    out_root: Path,
    *,
    cfg: ExperimentConfig,
    config_path: Path,
    n_cells_planned: int,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    """Create and write `manifest.json` (INFRA.md §6)."""
    out_root = Path(out_root)
    out_root.mkdir(parents=True, exist_ok=True)

    config_path = Path(config_path)
    repo_root = Path(repo_root) if repo_root is not None else config_path.parent.parent.parent.parent

    config_hash = config_hash_from_path(config_path)
    commit, dirty = _git_commit(repo_root)

    manifest: dict[str, Any] = {
        "experiment_id": cfg.experiment_id,
        "config_path": str(config_path),
        "config_hash": config_hash,
        "code_commit": commit,
        "code_dirty": dirty,
        "python": platform.python_version(),
        "swipl": _swipl_version(),
        "aba_asp_version": None,
        "argcausaldisco_commit": None,
        "started_at": _iso_now(),
        "finished_at": None,
        "n_cells_planned": int(n_cells_planned),
        "n_cells_completed": 0,
        "n_cells_skipped": 0,
        "outcome_counts": {},
        "host": socket.gethostname(),
        "platform": platform.platform(),
        "pid": os.getpid(),
        # helpful for debugging; keep the parsed structure, but this isn't part of the audit minimum
        "config_defaults": dict(cfg.defaults),
        "dgps": [asdict(d) for d in cfg.dgps],
    }

    (out_root / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def close_manifest(
    out_root: Path,
    *,
    n_cells_completed: int,
    n_cells_skipped: int,
    outcome_counts: Mapping[str, int],
) -> dict[str, Any]:
    """Update and write final `manifest.json`."""
    out_root = Path(out_root)
    path = out_root / "manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))

    manifest["finished_at"] = _iso_now()
    manifest["n_cells_completed"] = int(n_cells_completed)
    manifest["n_cells_skipped"] = int(n_cells_skipped)
    manifest["outcome_counts"] = dict(outcome_counts)

    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest

