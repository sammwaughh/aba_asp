"""Prolog-free tests for the M1.2 side-car summary module.

Fabricates a cell directory (metrics.json + prolog.stdout with a listing(lopt/1)
block + bk.aba/bk.sol.aba) and asserts the summary computes framework-scope vars,
the covers/rejects flags, trace-line count, effective-option provenance, and the
exact-match check. No swipl/clingo.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from causal.experiments.m12_summary import (
    _canonicalize,
    exact_match,
    m12_delta_rules,
    parse_lopt_block,
    summarize_arm,
    summarize_cell,
)

# stdout with TWO lopt listings: the load-time defaults (cautious) and the
# in-run effective block (brave) after "Current learning options:". The parser
# must return the effective block.
_STDOUT = """\
:- dynamic lopt/1.

lopt(learning_mode(cautious)).
lopt(folding_mode(nd)).

Some other engine chatter here.

Current learning options:
:- dynamic lopt/1.

lopt(learning_mode(brave)).
lopt(folding_mode(nd)).
lopt(folding_steps(10)).
lopt(folding_selection(any)).
lopt(folding_space(all)).
lopt(asm_intro(relto)).
lopt(check_ic).

Starting RoLe...
"""


def _write_cell(cell_dir: Path, *, target: str, learned_rule: str) -> None:
    cell_dir.mkdir(parents=True, exist_ok=True)
    bk_lines = [
        "% Feature predicates for variable: x0",
        "x0_val_0(A) :- A=1.",
        "x0_val_1(A) :- A=2.",
        "% Feature predicates for variable: x1",
        "x1_val_2(A) :- A=3.",
    ]
    (cell_dir / "bk.aba").write_text("\n".join(bk_lines) + "\n", encoding="utf-8")
    (cell_dir / "bk.sol.aba").write_text(
        "\n".join(bk_lines + [learned_rule]) + "\n", encoding="utf-8"
    )
    (cell_dir / "prolog.stdout").write_text(_STDOUT, encoding="utf-8")
    metrics = {
        "dgp": "m12_sep",
        "target": target,
        "outcome": "solved",
        "n_delta_rules": 1,
        "n_target_rules": 1,
        "n_assumptions": 0,
        "n_contraries": 0,
        "max_body_length": 1,
        "mean_body_length": 1.0,
        "cov_py_pos": 1.0,
        "cov_py_neg": 1.0,
    }
    (cell_dir / "metrics.json").write_text(json.dumps(metrics), encoding="utf-8")


def test_parse_lopt_block_takes_effective_block() -> None:
    opts = parse_lopt_block(_STDOUT)
    assert opts["learning_mode"] == "brave"  # effective, not the default cautious
    assert opts["folding_mode"] == "nd"
    assert opts["folding_steps"] == "10"
    assert opts["folding_selection"] == "any"
    assert opts["folding_space"] == "all"
    assert opts["asm_intro"] == "relto"
    assert "check_ic" in opts and opts["check_ic"] == ""


def test_parse_lopt_block_absent_returns_empty() -> None:
    assert parse_lopt_block("no options here") == {}


def test_summarize_cell_computes_detectors(tmp_path: Path) -> None:
    cell_dir = tmp_path / "cell0"
    _write_cell(cell_dir, target="x2", learned_rule="x2(A) :- x1_val_2(A).")

    summary = summarize_cell(cell_dir, "M12_ecai2024")
    assert summary is not None
    assert summary.fixture == "m12_sep"
    assert summary.target == "x2"
    assert summary.outcome == "solved"
    assert summary.exact_match is True
    assert summary.covers_all_pos is True
    assert summary.rejects_all_neg is True
    assert summary.body_scope_vars == ("x1",)
    assert summary.framework_scope_vars == ("x1",)
    assert summary.n_delta_rules == 1
    assert summary.trace_line_count == len(_STDOUT.splitlines())
    assert summary.effective_options["learning_mode"] == "brave"
    assert "check_ic" in summary.effective_options
    assert summary.learned_target_rules == ("x2(A) :- x1_val_2(A).",)


def test_summarize_cell_detects_non_match(tmp_path: Path) -> None:
    cell_dir = tmp_path / "cell1"
    # Learn the wrong parent (x0) -> not the locked expected x1 rule.
    _write_cell(cell_dir, target="x2", learned_rule="x2(A) :- x0_val_1(A).")
    summary = summarize_cell(cell_dir, "M12_ecai2024")
    assert summary is not None
    assert summary.exact_match is False
    assert summary.body_scope_vars == ("x0",)


def test_exact_match_normalizes_literal_order() -> None:
    # Conjunctive rule with body literals in reversed order still matches.
    delta = ["x2(A) :- x1_val_2(A), x0_val_2(A)."]
    assert exact_match("m12_conj", "x2", delta) is True


def test_exact_match_disj_requires_both_rules() -> None:
    one = ["x2(A) :- x0_val_2(A)."]
    both = ["x2(A) :- x0_val_2(A).", "x2(A) :- x1_val_2(A)."]
    assert exact_match("m12_disj", "x2", one) is False
    assert exact_match("m12_disj", "x2", both) is True


def test_summarize_arm_missing_dir_is_empty(tmp_path: Path) -> None:
    assert summarize_arm("M12_ecai2024", root=tmp_path) == []


def test_canonicalize_ignores_variable_names() -> None:
    # The engine echoes BK feature rules with renamed variables (X -> A).
    assert _canonicalize("x1_val_2(X) :- X=3.") == _canonicalize("x1_val_2(A) :- A=3.")
    # Distinct variables stay distinct.
    assert _canonicalize("f(X,Y).") != _canonicalize("f(X,X).")


def test_m12_delta_excludes_echoed_bk_rules(tmp_path: Path) -> None:
    """Echoed feature/domain BK clauses must NOT count as learned delta rules."""
    cell = tmp_path / "cell"
    cell.mkdir()
    bk = [
        "x1_val_2(A) :- A=3.",
        "domain(default).",
        "domain(1).",
    ]
    sol = [
        # feature rule echoed with A -> B (must be subtracted):
        "x1_val_2(B) :- B=3.",
        "domain(default).",
        "domain(1).",
        # a genuinely learned rule:
        "x2(A) :- x1_val_2(A).",
    ]
    (cell / "bk.aba").write_text("\n".join(bk) + "\n", encoding="utf-8")
    (cell / "bk.sol.aba").write_text("\n".join(sol) + "\n", encoding="utf-8")

    delta = m12_delta_rules(cell / "bk.sol.aba")
    assert "x2(A) :- x1_val_2(A)." in delta
    assert not any("domain" in r for r in delta)
    assert not any(r.startswith("x1_val_2") for r in delta)
