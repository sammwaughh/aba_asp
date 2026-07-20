"""M12x side-car: \(\mathcal{H}^\star\) matrix + per-cell inspection artefacts.

Reads ``M12x_{ecai2024,aamas2025}/cells/{dgp}__target-{t}/`` and writes:

- ``causal/outputs/aba_learning/grid/M12x_summary.md``
- ``causal/outputs/aba_learning/grid/M12x_summary.json``
- ``causal/outputs/aba_learning/grid/M12x_cell_reports/{arm}/{cell}.md``

Acceptance remains inspection-first (Approach); ``exact_hstar`` is a detector only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

_THIS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _THIS_DIR.parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from causal.experiments.m12_summary import (
    _asp_fractions_for_cell,
    _find_sol_path,
    _normalize_rule,
    body_scope_vars,
    framework_scope_vars,
    m12_delta_rules,
    parse_lopt_block,
)
from causal.experiments.paths import grid_root
from causal.metrics import target_rule_filter

ARMS: tuple[str, ...] = ("M12x_ecai2024", "M12x_aamas2025")

# Reference \(\mathcal{H}_t^\star\) from mechanism cards (normalized via _normalize_rule).
HSTAR: dict[tuple[str, str], frozenset[str]] = {
    ("m12_u1_separator_copy", "x2"): frozenset(
        {"x2(A):-x1_val_1(A)", "x2(A):-x1_val_2(A)"}
    ),
    ("m12_u2_collider_min", "x2"): frozenset(
        {
            "x2(A):-x0_val_1(A),x1_val_1(A)",
            "x2(A):-x0_val_1(A),x1_val_2(A)",
            "x2(A):-x0_val_2(A),x1_val_1(A)",
            "x2(A):-x0_val_2(A),x1_val_2(A)",
        }
    ),
    ("m12_u3_collider_max", "x2"): frozenset(
        {
            "x2(A):-x0_val_1(A)",
            "x2(A):-x0_val_2(A)",
            "x2(A):-x1_val_1(A)",
            "x2(A):-x1_val_2(A)",
        }
    ),
    ("m12_u4_fork_double_copy", "x1"): frozenset(
        {"x1(A):-x0_val_0(A)", "x1(A):-x0_val_1(A)"}
    ),
    ("m12_u4_fork_double_copy", "x2"): frozenset(
        {"x2(A):-x0_val_1(A)", "x2(A):-x0_val_2(A)"}
    ),
    # U5/x1: no parent-aligned perfect H* (descendant is unique perfect separator).
    ("m12_u5_chain_double_copy", "x1"): frozenset(),
    ("m12_u5_chain_double_copy", "x2"): frozenset(
        {"x2(A):-x1_val_1(A)", "x2(A):-x1_val_2(A)"}
    ),
    ("m12_u6_g1_and_cone", "x2"): frozenset(
        {
            "x2(A):-x0_val_1(A),x1_val_1(A)",
            "x2(A):-x0_val_1(A),x1_val_2(A)",
            "x2(A):-x0_val_2(A),x1_val_1(A)",
            "x2(A):-x0_val_2(A),x1_val_2(A)",
        }
    ),
    ("m12_u6_g1_and_cone", "x3"): frozenset(
        {
            "x3(A):-x1_val_1(A),x2_val_0(A)",
            "x3(A):-x1_val_2(A),x2_val_0(A)",
            "x3(A):-x1_val_2(A),x2_val_1(A)",
        }
    ),
    ("m12_u7_g1_or_cone", "x3"): frozenset(
        {
            "x3(A):-x1_val_1(A),x2_val_2(A)",
            "x3(A):-x1_val_2(A),x2_val_0(A)",
            "x3(A):-x1_val_0(A),x2_val_1(A)",
        }
    ),
}

# Structural sets for citation flags (from mechanism cards).
STRUCT: dict[tuple[str, str], dict[str, frozenset[str]]] = {
    ("m12_u1_separator_copy", "x2"): {
        "ancestors": frozenset({"x1"}),
        "other_distractors": frozenset({"x0"}),
        "descendants": frozenset(),
    },
    ("m12_u2_collider_min", "x2"): {
        "ancestors": frozenset({"x0", "x1"}),
        "other_distractors": frozenset(),
        "descendants": frozenset(),
    },
    ("m12_u3_collider_max", "x2"): {
        "ancestors": frozenset({"x0", "x1"}),
        "other_distractors": frozenset(),
        "descendants": frozenset(),
    },
    ("m12_u4_fork_double_copy", "x1"): {
        "ancestors": frozenset({"x0"}),
        "other_distractors": frozenset({"x2"}),
        "descendants": frozenset(),
    },
    ("m12_u4_fork_double_copy", "x2"): {
        "ancestors": frozenset({"x0"}),
        "other_distractors": frozenset({"x1"}),
        "descendants": frozenset(),
    },
    ("m12_u5_chain_double_copy", "x1"): {
        "ancestors": frozenset({"x0"}),
        "other_distractors": frozenset(),
        "descendants": frozenset({"x2"}),
    },
    ("m12_u5_chain_double_copy", "x2"): {
        "ancestors": frozenset({"x0", "x1"}),
        "other_distractors": frozenset(),
        "descendants": frozenset(),
    },
    ("m12_u6_g1_and_cone", "x2"): {
        "ancestors": frozenset({"x0", "x1"}),
        "other_distractors": frozenset(),
        "descendants": frozenset({"x3"}),
    },
    ("m12_u6_g1_and_cone", "x3"): {
        "ancestors": frozenset({"x0", "x1", "x2"}),
        "other_distractors": frozenset(),
        "descendants": frozenset(),
    },
    ("m12_u7_g1_or_cone", "x3"): {
        "ancestors": frozenset({"x0", "x1", "x2"}),
        "other_distractors": frozenset(),
        "descendants": frozenset(),
    },
}

# Preferred parents (for parent-vs-ancestor notes).
PARENTS: dict[tuple[str, str], frozenset[str]] = {
    ("m12_u1_separator_copy", "x2"): frozenset({"x1"}),
    ("m12_u2_collider_min", "x2"): frozenset({"x0", "x1"}),
    ("m12_u3_collider_max", "x2"): frozenset({"x0", "x1"}),
    ("m12_u4_fork_double_copy", "x1"): frozenset({"x0"}),
    ("m12_u4_fork_double_copy", "x2"): frozenset({"x0"}),
    ("m12_u5_chain_double_copy", "x1"): frozenset({"x0"}),
    ("m12_u5_chain_double_copy", "x2"): frozenset({"x1"}),
    ("m12_u6_g1_and_cone", "x2"): frozenset({"x0", "x1"}),
    ("m12_u6_g1_and_cone", "x3"): frozenset({"x1", "x2"}),
    ("m12_u7_g1_or_cone", "x3"): frozenset({"x1", "x2"}),
}

_CELL_DIR_RE = re.compile(r"^(?P<dgp>.+)__target-(?P<target>x\d+)$")
_ALPHA_RE = re.compile(r"\balpha_\d+\b")


@dataclass(frozen=True)
class M12xCellSummary:
    arm: str
    fixture: str
    target: str
    cell_dir_name: str
    outcome: str
    exact_hstar: bool
    cites_descendant: bool
    cites_other_distractor: bool
    cites_non_parent_ancestor: bool
    uses_assumptions_in_target_rules: bool
    body_scope_vars: tuple[str, ...]
    framework_scope_vars: tuple[str, ...]
    pos_covered: str
    neg_rejected: str
    n_delta_rules: int
    n_target_rules: int
    n_assumptions: int
    n_contraries: int
    max_body_length: int
    mean_body_length: float | None
    trace_line_count: int
    hstar_rules: tuple[str, ...]
    learned_target_rules: tuple[str, ...]
    flags: tuple[str, ...]
    judgment_sketch: str


def _hstar_pretty(key: tuple[str, str]) -> tuple[str, ...]:
    rules = sorted(HSTAR[key])
    # Un-normalize for display: insert spaces around :- and commas.
    out: list[str] = []
    for r in rules:
        if ":-" not in r:
            out.append(r + ".")
            continue
        head, body = r.split(":-", 1)
        lits = body.split(",") if body else []
        out.append(f"{head} :- {', '.join(lits)}.")
    return tuple(out)


def _flags_and_judgment(
    *,
    key: tuple[str, str],
    body_vars_set: frozenset[str],
    target_rules: list[str],
    exact: bool,
) -> tuple[tuple[str, ...], str]:
    st = STRUCT[key]
    parents = PARENTS[key]
    flags: list[str] = []
    if exact:
        flags.append("exact_hstar")
    cites_desc = bool(body_vars_set & st["descendants"])
    cites_dist = bool(body_vars_set & st["other_distractors"])
    cites_non_parent_anc = bool(body_vars_set & (st["ancestors"] - parents))
    uses_asm = any(_ALPHA_RE.search(r) for r in target_rules)
    if cites_desc:
        flags.append("cites_descendant")
    if cites_dist:
        flags.append("cites_other_distractor")
    if cites_non_parent_anc:
        flags.append("cites_non_parent_ancestor")
    if uses_asm:
        flags.append("uses_assumptions_in_target_rules")
    if not body_vars_set & st["ancestors"] and body_vars_set:
        flags.append("no_ancestor_in_body")
    if not flags:
        flags.append("other_divergence")

    if exact:
        sketch = "exact match to intended H*"
    elif cites_desc and cites_dist:
        sketch = "cites descendant and other distractor"
    elif cites_desc:
        sketch = "cites descendant (explicit failure mode)"
    elif cites_dist:
        sketch = "cites sibling/isolated distractor"
    elif cites_non_parent_anc and not (body_vars_set & parents):
        sketch = "grandparent/ancestor without preferred parent"
    elif uses_asm:
        sketch = "assumption-mediated; not exact H*"
    else:
        sketch = "diverges from H* (see rules)"
    return tuple(flags), sketch


def summarize_cell(cell_dir: Path, arm: str) -> M12xCellSummary | None:
    metrics_path = cell_dir / "metrics.json"
    if not metrics_path.is_file():
        return None
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    fixture = str(metrics.get("dgp", ""))
    target = str(metrics.get("target", ""))
    key = (fixture, target)
    if key not in HSTAR:
        return None

    stdout_path = cell_dir / "prolog.stdout"
    stdout = stdout_path.read_text(encoding="utf-8") if stdout_path.is_file() else ""
    sol_path = _find_sol_path(cell_dir)
    delta = m12_delta_rules(sol_path) if sol_path is not None else []
    target_rules = target_rule_filter(target, delta)
    learned_norm = {_normalize_rule(r) for r in target_rules}
    hstar = HSTAR[key]
    exact = learned_norm == set(hstar)
    body = body_scope_vars(target, delta)
    st = STRUCT[key]
    parents = PARENTS[key]
    flags, sketch = _flags_and_judgment(
        key=key,
        body_vars_set=body,
        target_rules=target_rules,
        exact=exact,
    )
    pos_covered, neg_rejected = _asp_fractions_for_cell(cell_dir, metrics, target)
    mean_bl = metrics.get("mean_body_length")
    return M12xCellSummary(
        arm=arm,
        fixture=fixture,
        target=target,
        cell_dir_name=cell_dir.name,
        outcome=str(metrics.get("outcome", "")),
        exact_hstar=exact,
        cites_descendant=bool(body & st["descendants"]),
        cites_other_distractor=bool(body & st["other_distractors"]),
        cites_non_parent_ancestor=bool(body & (st["ancestors"] - parents)),
        uses_assumptions_in_target_rules=any(_ALPHA_RE.search(r) for r in target_rules),
        body_scope_vars=tuple(sorted(body)),
        framework_scope_vars=tuple(sorted(framework_scope_vars(target, delta))),
        pos_covered=pos_covered,
        neg_rejected=neg_rejected,
        n_delta_rules=int(metrics.get("n_delta_rules", 0) or 0),
        n_target_rules=int(metrics.get("n_target_rules", 0) or len(target_rules)),
        n_assumptions=int(metrics.get("n_assumptions", 0) or 0),
        n_contraries=int(metrics.get("n_contraries", 0) or 0),
        max_body_length=int(metrics.get("max_body_length", 0) or 0),
        mean_body_length=(float(mean_bl) if mean_bl is not None else None),
        trace_line_count=len(stdout.splitlines()),
        hstar_rules=_hstar_pretty(key),
        learned_target_rules=tuple(target_rules),
        flags=flags,
        judgment_sketch=sketch,
    )


def summarize_arm(arm: str, *, root: Path | None = None) -> list[M12xCellSummary]:
    root = root or grid_root()
    cells_dir = root / arm / "cells"
    if not cells_dir.is_dir():
        return []
    out: list[M12xCellSummary] = []
    for cell_dir in sorted(cells_dir.iterdir()):
        if not cell_dir.is_dir():
            continue
        if _CELL_DIR_RE.match(cell_dir.name) is None:
            continue
        summary = summarize_cell(cell_dir, arm)
        if summary is not None:
            out.append(summary)
    return out


def build_markdown(rows_by_arm: dict[str, list[M12xCellSummary]]) -> str:
    lines: list[str] = [
        "# M12x summary matrix (\(\mathcal{H}^\star\) vs learned)",
        "",
        "Detectors only; acceptance remains inspection-first against mechanism cards.",
        "Generated by `python -m causal.experiments.m12x_summary`.",
        "",
        "Flag legend: `exact_hstar` · `cites_descendant` · "
        "`cites_other_distractor` · `cites_non_parent_ancestor` · "
        "`uses_assumptions_in_target_rules` · `other_divergence`.",
        "",
    ]
    for arm in ARMS:
        rows = rows_by_arm.get(arm, [])
        lines.append(f"## {arm}")
        lines.append("")
        if not rows:
            lines.append("_No cells found._")
            lines.append("")
            continue
        n_exact = sum(1 for r in rows if r.exact_hstar)
        n_desc = sum(1 for r in rows if r.cites_descendant)
        n_dist = sum(1 for r in rows if r.cites_other_distractor)
        lines.append(
            f"Cells: {len(rows)}; exact \(\mathcal{{H}}^\star\): {n_exact}; "
            f"cites descendant: {n_desc}; "
            f"cites other distractor: {n_dist}."
        )
        lines.append("")
        lines.append(
            "| fixture | target | outcome | exact | desc | distractor | "
            "body vars | pos | neg | asm | flags | sketch |"
        )
        lines.append(
            "|---|---|---|:-:|:-:|:-:|---|:-:|:-:|--:|---|---|"
        )
        for r in rows:
            lines.append(
                f"| {r.fixture} | {r.target} | {r.outcome} | "
                f"{'Y' if r.exact_hstar else 'N'} | "
                f"{'Y' if r.cites_descendant else 'N'} | "
                f"{'Y' if r.cites_other_distractor else 'N'} | "
                f"{{{', '.join(r.body_scope_vars)}}} | "
                f"{r.pos_covered} | {r.neg_rejected} | {r.n_assumptions} | "
                f"{', '.join(r.flags)} | {r.judgment_sketch} |"
            )
        lines.append("")
        lines.append("### Learned vs \(\mathcal{H}^\star\) (compact)")
        lines.append("")
        for r in rows:
            lines.append(f"#### `{r.cell_dir_name}`")
            lines.append("")
            lines.append("\(\mathcal{H}^\star\):")
            lines.append("")
            lines.append("```prolog")
            lines.extend(r.hstar_rules)
            lines.append("```")
            lines.append("")
            lines.append("Learned target rules:")
            lines.append("")
            lines.append("```prolog")
            lines.extend(r.learned_target_rules or ["% (none)"])
            lines.append("```")
            lines.append("")
    return "\n".join(lines) + "\n"


def write_cell_report(row: M12xCellSummary, *, reports_root: Path) -> Path:
    arm_dir = reports_root / row.arm
    arm_dir.mkdir(parents=True, exist_ok=True)
    path = arm_dir / f"{row.cell_dir_name}.md"
    st = STRUCT[(row.fixture, row.target)]
    lines = [
        f"# {row.arm} / {row.cell_dir_name}",
        "",
        f"- **Outcome:** {row.outcome}",
        f"- **Judgment sketch:** {row.judgment_sketch}",
        f"- **Flags:** {', '.join(row.flags)}",
        f"- **Body-scope vars:** {{{', '.join(row.body_scope_vars)}}}",
        f"- **Framework-scope vars:** {{{', '.join(row.framework_scope_vars)}}}",
        f"- **ASP coverage:** pos {row.pos_covered}, neg {row.neg_rejected}",
        f"- **Complexity:** Δrules={row.n_delta_rules}, target_rules={row.n_target_rules}, "
        f"asm={row.n_assumptions}, contr={row.n_contraries}, "
        f"max_body={row.max_body_length}, trace_lines={row.trace_line_count}",
        "",
        "## Structural sets (card)",
        "",
        f"- Ancestors: {{{', '.join(sorted(st['ancestors']))}}}",
        f"- Other distractors: {{{', '.join(sorted(st['other_distractors'])) or '∅'}}}",
        f"- Descendants (in BK): {{{', '.join(sorted(st['descendants'])) or '∅'}}}",
        "",
        "## \(\mathcal{H}^\star\)",
        "",
        "```prolog",
        *row.hstar_rules,
        "```",
        "",
        "## Learned target rules",
        "",
        "```prolog",
        *(row.learned_target_rules or ["% (none)"]),
        "```",
        "",
        "## Runner artefacts",
        "",
        f"- `causal/outputs/aba_learning/grid/{row.arm}/cells/{row.cell_dir_name}/`",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_summary(
    rows_by_arm: dict[str, list[M12xCellSummary]], *, root: Path | None = None
) -> tuple[Path, Path, Path]:
    root = root or grid_root()
    root.mkdir(parents=True, exist_ok=True)
    md_path = root / "M12x_summary.md"
    json_path = root / "M12x_summary.json"
    reports_root = root / "M12x_cell_reports"
    md_path.write_text(build_markdown(rows_by_arm), encoding="utf-8")
    doc: dict[str, Any] = {
        arm: [asdict(r) for r in rows] for arm, rows in rows_by_arm.items()
    }
    json_path.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    n_reports = 0
    for rows in rows_by_arm.values():
        for r in rows:
            write_cell_report(r, reports_root=reports_root)
            n_reports += 1
    # Index for cell reports
    index_lines = [
        "# M12x per-cell inspection reports",
        "",
        f"{n_reports} cells. Generated by `python -m causal.experiments.m12x_summary`.",
        "",
    ]
    for arm in ARMS:
        index_lines.append(f"## {arm}")
        index_lines.append("")
        for r in rows_by_arm.get(arm, []):
            index_lines.append(f"- [{r.cell_dir_name}]({arm}/{r.cell_dir_name}.md) — {r.judgment_sketch}")
        index_lines.append("")
    (reports_root / "README.md").write_text("\n".join(index_lines), encoding="utf-8")
    return md_path, json_path, reports_root


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="M12x \(\mathcal{H}^\star\) summary matrix")
    p.add_argument("--only", type=str, default=None, metavar="ARM")
    args = p.parse_args(argv)
    arms = (args.only,) if args.only else ARMS
    rows_by_arm = {arm: summarize_arm(arm) for arm in arms}
    md_path, json_path, reports = write_summary(rows_by_arm)
    total = sum(len(v) for v in rows_by_arm.values())
    print(f"wrote {md_path}")
    print(f"wrote {json_path}")
    print(f"wrote {reports}/ ({total} cell reports)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
