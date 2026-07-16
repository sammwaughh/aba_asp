"""Smoke tests for M12x H* summary (requires completed grid outputs)."""

from __future__ import annotations

from pathlib import Path

import pytest

from causal.experiments.m12x_summary import (
    ARMS,
    HSTAR,
    summarize_arm,
    write_summary,
)
from causal.experiments.paths import grid_root


def test_hstar_covers_eleven_cells() -> None:
    assert len(HSTAR) == 11


@pytest.mark.parametrize("arm", ARMS)
def test_summarize_arm_has_eleven_cells_if_run(arm: str) -> None:
    cells = grid_root() / arm / "cells"
    if not cells.is_dir():
        pytest.skip(f"{arm} not run yet")
    rows = summarize_arm(arm)
    assert len(rows) == 11
    assert all(r.outcome == "solved" for r in rows)


def test_write_summary_smoke(tmp_path: Path) -> None:
    # Use real outputs if present; otherwise skip.
    if not (grid_root() / "M12x_ecai2024" / "cells").is_dir():
        pytest.skip("M12x not run")
    rows = {arm: summarize_arm(arm) for arm in ARMS}
    md, js, reports = write_summary(rows, root=tmp_path)
    assert md.is_file() and js.is_file()
    assert (reports / "README.md").is_file()
    assert len(list(reports.glob("*/*.md"))) == 22
