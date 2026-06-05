"""Project path helpers (single source of truth).

This module defines where the repository root and grid output root live.
"""

from __future__ import annotations

from pathlib import Path


def repo_root() -> Path:
    """Return the `aba_asp` repository root directory."""
    # `causal/experiments/paths.py` -> parents[2] is `aba_asp`
    return Path(__file__).resolve().parents[2]


def grid_root() -> Path:
    """Return `.../causal/outputs/aba_learning/grid` under the repo root."""
    return repo_root() / "causal" / "outputs" / "aba_learning" / "grid"

