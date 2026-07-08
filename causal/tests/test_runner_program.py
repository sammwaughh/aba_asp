"""Prolog-free tests for the generated ABA-ASP learning program builder.

``_build_learning_program`` is pure (returns the program text). These tests lock
the load ordering and the ``prolog_config`` branch: with a config the program
consults it verbatim and omits the ``set_lopt`` folding directives; without one
it emits them (legacy behaviour). No swipl is invoked.
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from causal.run_aba_asp import _build_learning_program

_ABA_ASP = _REPO_ROOT
_BK = _REPO_ROOT / "examples" / "aacbr2.bk.aba"  # any existing .aba path; stem used


def _program(**kwargs) -> str:
    return _build_learning_program(
        _ABA_ASP,
        _BK,
        ["x2(3)", "x2(6)"],
        ["x2(1)"],
        **kwargs,
    )


def test_legacy_emits_set_lopt_and_no_config() -> None:
    prog = _program(learning_options={"folding_mode": "nd", "folding_steps": "15"})
    assert "set_lopt(folding_mode(nd))" in prog
    assert "set_lopt(folding_steps(15))" in prog
    # No verbatim config consult in legacy mode (only aba_asp.pl + BK).
    assert prog.count(":- consult(") == 2  # aba_asp.pl + predicate file


def test_prolog_config_consulted_verbatim_and_no_set_lopt() -> None:
    config = _REPO_ROOT / "configs" / "ecai2024_config.pl"
    prog = _program(
        learning_options={"folding_mode": "nd", "folding_steps": "15"},
        prolog_config=config,
    )
    # Config consulted verbatim; folding set_lopt directives suppressed.
    assert "ecai2024_config.pl" in prog
    assert "set_lopt(folding_mode" not in prog
    assert "set_lopt(folding_steps" not in prog
    assert prog.count(":- consult(") == 3  # aba_asp.pl + config + predicate file


def test_load_ordering_aba_asp_then_config_then_bk() -> None:
    config = _REPO_ROOT / "configs" / "aamas2025_config.pl"
    prog = _program(prolog_config=config)
    i_engine = prog.index("aba_asp.pl")
    i_config = prog.index("aamas2025_config.pl")
    i_bk = prog.index(_BK.stem)  # BK consult uses the resolved path; stem appears
    i_run = prog.index("aba_asp(")
    # Engine defaults load first, then the config overrides, then BK, then run.
    assert i_engine < i_config < i_bk < i_run


def test_examples_are_embedded() -> None:
    prog = _program()
    assert "[x2(3), x2(6)]" in prog
    assert "[x2(1)]" in prog
