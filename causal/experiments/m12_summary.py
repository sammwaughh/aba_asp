"""M1.2 side-car summary: expected-vs-learned matrix + extra divergence detectors.

Localized to M1.2 so the shared results schema (``causal/metrics.py``
``RESULT_PARQUET_COLUMNS``) stays the primary store. Reads each cell's
``metrics.json``, ``prolog.stdout``, and solution files for the two published
arms and emits, per (arm, fixture) cell, the objective signals the plan lists in
Section 5 that are not in the shared parquet narrative alone:

- body-scope parent variable set (base vars in learned target-rule bodies) and
  framework-scope variable set (base vars anywhere in the learned delta,
  contraries included);
- ``pos_covered`` / ``neg_rejected`` as ``k/n`` fractions from **ASP answer-set
  coverage** (brave entailment on ``bk.sol.asp`` via clingo; ``cov_asp_*`` in
  ``metrics.json``, recomputed from the cell ASP file when those keys are absent);
- framework complexity (delta rules / assumptions / contraries / body length);
- trace-line count of ``prolog.stdout`` (reproducible runtime proxy);
- effective-configuration provenance (the ``Current learning options:`` /
  ``listing(lopt/1)`` block the engine prints);
- an exact-match check of the learned target rules against the locked expected
  output per fixture.

The categorical, table-relative "outcome class" is deliberately NOT assigned
here: it is a Stage-3 qualitative judgement (metrics are detectors only).

CLI::

    python -m causal.experiments.m12_summary [--only M12_ecai2024]

writes ``causal/outputs/aba_learning/grid/M12_summary.md`` and ``.json``.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

_THIS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _THIS_DIR.parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from causal.asp_coverage import asp_answer_set_coverage, resolve_sol_asp_path
from causal.experiments.paths import grid_root
from causal.metrics import (
    _PER_SAMPLE_INDICATOR_RE,
    _parse_rule_lines,
    body_vars,
    target_rule_filter,
)

import re as _re

# Prolog variable token: leading uppercase letter or underscore.
_VAR_RE = _re.compile(r"\b[A-Z_][A-Za-z0-9_]*\b")

ARMS: tuple[str, ...] = ("M12_ecai2024", "M12_aamas2025")

# Locked expected target-rule sets per fixture (mirrors the M1.2 record). Each
# entry is a set of normalized "head:-body" strings (see ``_normalize_rule``).
EXPECTED: dict[str, frozenset[str]] = {
    "m12_sep": frozenset({"x2(A):-x1_val_2(A)"}),
    "m12_conj": frozenset({"x2(A):-x0_val_2(A),x1_val_2(A)"}),
    "m12_disj": frozenset({"x2(A):-x0_val_2(A)", "x2(A):-x1_val_2(A)"}),
    "m12_fork": frozenset({"x2(A):-x0_val_2(A)"}),
    "m12_chain": frozenset({"x2(A):-x1_val_2(A)"}),
}

_LOPT_MARKER = "Current learning options:"


def parse_lopt_block(stdout: str) -> dict[str, str]:
    """Parse the effective ``listing(lopt/1)`` block printed by ``aba_asp/...``.

    Returns a mapping option-name -> inner argument text, e.g.
    ``{"learning_mode": "brave", "folding_mode": "nd", "check_ic": ""}``. Reads
    the block that follows the in-run ``Current learning options:`` marker (the
    effective options, after any consulted config), not the load-time default
    listing. ``check_ic`` (0-ary) maps to an empty string.
    """
    lines = stdout.splitlines()
    try:
        start = next(i for i, ln in enumerate(lines) if _LOPT_MARKER in ln)
    except StopIteration:
        return {}

    opts: dict[str, str] = {}
    for ln in lines[start + 1 :]:
        s = ln.strip()
        if not s.startswith("lopt("):
            # listing/1 emits a blank line and a ':- dynamic lopt/1.' header;
            # stop once we have started collecting and hit a non-lopt line.
            if opts and s and not s.startswith(":-"):
                break
            continue
        inner = s[len("lopt(") :].rstrip(".").rstrip()
        if inner.endswith(")"):
            inner = inner[:-1]
        # inner is now e.g. "learning_mode(brave)" or "check_ic".
        if "(" in inner:
            name, arg = inner.split("(", 1)
            opts[name.strip()] = arg[:-1] if arg.endswith(")") else arg
        else:
            opts[inner.strip()] = ""
    return opts


def _normalize_rule(rule: str) -> str:
    """Normalize a target rule to ``head:-l1,l2`` (spaces removed, body sorted)."""
    r = rule.strip().rstrip(".")
    r = "".join(r.split())
    if ":-" not in r:
        return r
    head, body = r.split(":-", 1)
    literals = [lit for lit in _split_top_level(body) if lit]
    return f"{head}:-{','.join(sorted(literals))}"


def _split_top_level(body: str) -> list[str]:
    """Split a rule body on top-level commas (commas outside parentheses)."""
    out: list[str] = []
    depth = 0
    current = ""
    for ch in body:
        if ch == "(":
            depth += 1
            current += ch
        elif ch == ")":
            depth -= 1
            current += ch
        elif ch == "," and depth == 0:
            out.append(current)
            current = ""
        else:
            current += ch
    if current:
        out.append(current)
    return out


def body_scope_vars(target: str, delta: list[str]) -> frozenset[str]:
    """Base variables cited in learned target-rule bodies (excludes the target)."""
    acc: set[str] = set()
    for rule in target_rule_filter(target, delta):
        if ":-" in rule:
            acc |= body_vars(rule.split(":-", 1)[1])
    acc.discard(target)
    return frozenset(acc)


def framework_scope_vars(target: str, delta: list[str]) -> frozenset[str]:
    """Base variables anywhere in the learned delta (heads, bodies, contraries)."""
    acc: set[str] = set()
    for rule in delta:
        acc |= body_vars(rule)
    acc.discard(target)
    return frozenset(acc)


def _learned_target_rules_normalized(target: str, delta: list[str]) -> set[str]:
    return {_normalize_rule(r) for r in target_rule_filter(target, delta)}


def exact_match(fixture: str, target: str, delta: list[str]) -> bool:
    """True iff the learned target rules equal the locked expected set exactly."""
    expected = EXPECTED.get(fixture)
    if expected is None:
        return False
    return _learned_target_rules_normalized(target, delta) == set(expected)


def _canonicalize(rule: str) -> str:
    """Canonicalize a rule: strip spaces and rename variables by appearance order.

    Makes BK subtraction robust to the engine echoing BK clauses into the
    solution with renamed variables (e.g. a feature rule ``xi_val_v(X) :- X=id``
    written back as ``xi_val_v(A) :- A=id``). Distinct variables stay distinct.
    """
    r = "".join(rule.strip().rstrip(".").split())
    mapping: dict[str, str] = {}

    def _sub(match: "_re.Match[str]") -> str:
        name = match.group(0)
        if name not in mapping:
            mapping[name] = f"_V{len(mapping)}"
        return mapping[name]

    return _VAR_RE.sub(_sub, r)


def m12_delta_rules(sol_path: Path) -> list[str]:
    """Learned δ-rules = solution minus BK, matched under variable canonicalization.

    Reads the cell's ``bk.aba`` (always ``sol_path.parent/bk.aba`` in the grid
    layout) and subtracts BK clauses by canonical form, then drops per-sample
    indicator facts. Returns the original solution-rule text of the survivors.
    """
    sol_path = Path(sol_path)
    if not sol_path.is_file():
        return []
    bk_path = sol_path.parent / "bk.aba"
    sol_rules = _parse_rule_lines(sol_path.read_text(encoding="utf-8"))
    bk_rules = (
        _parse_rule_lines(bk_path.read_text(encoding="utf-8")) if bk_path.is_file() else []
    )
    bk_canon = {_canonicalize(r) for r in bk_rules}
    learned = [r for r in sol_rules if _canonicalize(r) not in bk_canon]
    return [r for r in learned if not _PER_SAMPLE_INDICATOR_RE.match(r)]


def _find_sol_path(cell_dir: Path) -> Path | None:
    """Locate the cell's solution file (canonical ``bk.sol.aba`` preferred)."""
    canonical = cell_dir / "bk.sol.aba"
    if canonical.is_file():
        return canonical
    candidates = sorted(cell_dir.glob("*.sol.aba"))
    return candidates[0] if candidates else None


@dataclass(frozen=True)
class CellSummary:
    arm: str
    fixture: str
    target: str
    outcome: str
    exact_match: bool
    pos_covered: str  # "k/n" or "?"
    neg_rejected: str  # "k/n" or "?"
    body_scope_vars: tuple[str, ...]
    framework_scope_vars: tuple[str, ...]
    n_delta_rules: int
    n_target_rules: int
    n_assumptions: int
    n_contraries: int
    max_body_length: int
    mean_body_length: float | None
    trace_line_count: int
    effective_options: dict[str, str]
    learned_target_rules: tuple[str, ...]


def _as_bool_flag(value: Any) -> bool | None:
    """1.0 -> True, 0.0..<1 -> False, None/NaN -> None."""
    if value is None:
        return None
    try:
        return float(value) >= 1.0
    except (TypeError, ValueError):
        return None


def _format_fraction(k: Any, n: Any) -> str:
    """Format coverage as ``k/n``, or ``?`` if unavailable."""
    try:
        ki = int(k)
        ni = int(n)
    except (TypeError, ValueError):
        return "?"
    if ni < 0 or ki < 0:
        return "?"
    return f"{ki}/{ni}"


def _examples_from_data_csv(cell_dir: Path, target: str) -> tuple[list[str], list[str]]:
    """Rebuild E+/E− from ``data.csv`` (positive class ``target == 2``)."""
    data_path = cell_dir / "data.csv"
    if not data_path.is_file():
        return [], []
    try:
        import pandas as pd
    except ImportError:
        return [], []
    df = pd.read_csv(data_path)
    if target not in df.columns:
        return [], []
    pos = [
        f"{target}({i + 1})"
        for i, v in enumerate(df[target].tolist())
        if int(v) == 2
    ]
    neg = [
        f"{target}({i + 1})"
        for i, v in enumerate(df[target].tolist())
        if int(v) != 2
    ]
    return pos, neg


def _asp_fractions_for_cell(
    cell_dir: Path, metrics: dict[str, Any], target: str
) -> tuple[str, str]:
    """Return ``(pos_covered, neg_rejected)`` as ``k/n`` strings from ASP coverage."""
    # Prefer counts written by compute_cell_metrics.
    if "cov_asp_tp" in metrics and "cov_asp_n_pos" in metrics:
        pos_rate = metrics.get("cov_asp_pos")
        if isinstance(pos_rate, float) and math.isnan(pos_rate):
            pass
        else:
            return (
                _format_fraction(metrics.get("cov_asp_tp"), metrics.get("cov_asp_n_pos")),
                _format_fraction(metrics.get("cov_asp_tn"), metrics.get("cov_asp_n_neg")),
            )

    sol_asp = resolve_sol_asp_path(cell_dir / "bk.aba", cell_dir / "bk.sol.aba")
    if sol_asp is None:
        return "?", "?"
    pos, neg = _examples_from_data_csv(cell_dir, target)
    if not pos and not neg:
        return "?", "?"
    cov = asp_answer_set_coverage(sol_asp, pos, neg)
    if isinstance(cov.get("cov_asp_pos"), float) and math.isnan(float(cov["cov_asp_pos"])):
        return "?", "?"
    return (
        _format_fraction(cov.get("cov_asp_tp"), cov.get("cov_asp_n_pos")),
        _format_fraction(cov.get("cov_asp_tn"), cov.get("cov_asp_n_neg")),
    )


def summarize_cell(cell_dir: Path, arm: str) -> CellSummary | None:
    """Build a ``CellSummary`` from one cell directory, or ``None`` if unreadable."""
    metrics_path = cell_dir / "metrics.json"
    if not metrics_path.is_file():
        return None
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))

    fixture = str(metrics.get("dgp", ""))
    target = str(metrics.get("target", ""))
    outcome = str(metrics.get("outcome", ""))

    stdout_path = cell_dir / "prolog.stdout"
    stdout = stdout_path.read_text(encoding="utf-8") if stdout_path.is_file() else ""
    trace_line_count = len(stdout.splitlines())
    effective_options = parse_lopt_block(stdout)

    sol_path = _find_sol_path(cell_dir)
    delta = m12_delta_rules(sol_path) if sol_path is not None else []
    target_rules = target_rule_filter(target, delta)

    pos_covered, neg_rejected = _asp_fractions_for_cell(cell_dir, metrics, target)

    mean_bl = metrics.get("mean_body_length")
    return CellSummary(
        arm=arm,
        fixture=fixture,
        target=target,
        outcome=outcome,
        exact_match=exact_match(fixture, target, delta),
        pos_covered=pos_covered,
        neg_rejected=neg_rejected,
        body_scope_vars=tuple(sorted(body_scope_vars(target, delta))),
        framework_scope_vars=tuple(sorted(framework_scope_vars(target, delta))),
        n_delta_rules=int(metrics.get("n_delta_rules", 0) or 0),
        n_target_rules=int(metrics.get("n_target_rules", 0) or 0),
        n_assumptions=int(metrics.get("n_assumptions", 0) or 0),
        n_contraries=int(metrics.get("n_contraries", 0) or 0),
        max_body_length=int(metrics.get("max_body_length", 0) or 0),
        mean_body_length=(float(mean_bl) if mean_bl is not None else None),
        trace_line_count=trace_line_count,
        effective_options=effective_options,
        learned_target_rules=tuple(target_rules),
    )


def summarize_arm(arm: str, *, root: Path | None = None) -> list[CellSummary]:
    """Summarize the locked five-fixture cells of one arm's grid output directory."""
    root = root or grid_root()
    cells_dir = root / arm / "cells"
    if not cells_dir.is_dir():
        return []
    out: list[CellSummary] = []
    for fixture in sorted(EXPECTED):
        cell_dir = cells_dir / fixture
        if not cell_dir.is_dir():
            continue
        summary = summarize_cell(cell_dir, arm)
        if summary is not None:
            out.append(summary)
    return out


def _fmt_opts(opts: dict[str, str]) -> str:
    if not opts:
        return "-"
    parts = []
    for k in sorted(opts):
        v = opts[k]
        parts.append(k if v == "" else f"{k}={v}")
    return "; ".join(parts)


def build_markdown(rows_by_arm: dict[str, list[CellSummary]]) -> str:
    """Render the M1.2 side-car matrix as markdown."""
    lines: list[str] = []
    lines.append("# M1.2 side-car summary (expected-vs-learned detectors)")
    lines.append("")
    lines.append(
        "Objective divergence detectors only; the categorical outcome class is a "
        "Stage-3 qualitative judgement. ``pos_covered`` / ``neg_rejected`` are "
        "ASP answer-set coverage fractions (brave entailment on ``bk.sol.asp``). "
        "Generated by `python -m causal.experiments.m12_summary`."
    )
    lines.append("")
    for arm in ARMS:
        rows = rows_by_arm.get(arm, [])
        lines.append(f"## {arm}")
        lines.append("")
        if not rows:
            lines.append("_No cells found (arm not yet run)._")
            lines.append("")
            continue
        lines.append(
            "| fixture | target | outcome | exact | pos_covered | neg_rejected "
            "| body-scope vars | framework-scope vars | Δrules | asm | contr | "
            "max &#124; mean body | trace lines |"
        )
        lines.append(
            "|---|---|---|:-:|:-:|:-:|---|---|--:|--:|--:|---|---|--:|"
        )
        for r in rows:
            mean_bl = "-" if r.mean_body_length is None else f"{r.mean_body_length:.2f}"
            lines.append(
                f"| {r.fixture} | {r.target} | {r.outcome} | "
                f"{'Y' if r.exact_match else 'N'} | "
                f"{r.pos_covered} | {r.neg_rejected} | "
                f"{{{', '.join(r.body_scope_vars)}}} | "
                f"{{{', '.join(r.framework_scope_vars)}}} | "
                f"{r.n_delta_rules} | {r.n_assumptions} | {r.n_contraries} | "
                f"{r.max_body_length} &#124; {mean_bl} | {r.trace_line_count} |"
            )
        lines.append("")
        # Effective-options provenance (one line per distinct option set).
        lines.append("Effective options (from `listing(lopt/1)`):")
        lines.append("")
        for r in rows:
            lines.append(f"- `{r.fixture}`: {_fmt_opts(r.effective_options)}")
        lines.append("")
    return "\n".join(lines) + "\n"


def write_summary(rows_by_arm: dict[str, list[CellSummary]], *, root: Path | None = None) -> tuple[Path, Path]:
    """Write ``M12_summary.md`` and ``M12_summary.json`` under the grid root."""
    root = root or grid_root()
    root.mkdir(parents=True, exist_ok=True)
    md_path = root / "M12_summary.md"
    json_path = root / "M12_summary.json"
    md_path.write_text(build_markdown(rows_by_arm), encoding="utf-8")
    doc = {arm: [asdict(r) for r in rows] for arm, rows in rows_by_arm.items()}
    json_path.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return md_path, json_path


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="M1.2 side-car summary generator")
    p.add_argument(
        "--only",
        type=str,
        default=None,
        metavar="ARM",
        help="Summarize a single arm (e.g. M12_ecai2024) instead of both arms",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    arms = (args.only,) if args.only else ARMS
    rows_by_arm = {arm: summarize_arm(arm) for arm in arms}
    md_path, json_path = write_summary(rows_by_arm)
    total = sum(len(v) for v in rows_by_arm.values())
    print(f"wrote {md_path} and {json_path} ({total} cells across {len(arms)} arm(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
