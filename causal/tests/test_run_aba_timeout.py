"""Subprocess timeout wiring for run_prolog_aba_asp."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from causal.run_aba_asp import ABASPRunner


def test_run_prolog_aba_asp_passes_timeout_to_communicate(tmp_path: Path) -> None:
    bk = tmp_path / "bk.aba"
    bk.write_text("% stub\n", encoding="utf-8")
    runner = ABASPRunner()
    runner.prolog_available = True

    proc = MagicMock()
    proc.communicate.return_value = ("done", "")
    proc.returncode = 0

    with patch("causal.run_aba_asp.subprocess.Popen", return_value=proc) as popen:
        with patch.object(runner, "_check_prolog_available", return_value=True):
            runner.run_prolog_aba_asp(
                bk,
                positive_examples=["x0(1)"],
                negative_examples=["x0(2)"],
                timeout_s=120.0,
            )

    proc.communicate.assert_called_once_with(timeout=120.0)
    assert popen.called
