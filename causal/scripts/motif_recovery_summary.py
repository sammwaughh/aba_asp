"""Generate a generalized motif parent-recovery summary Markdown report.

This is the experiment-agnostic successor to
``causal/scripts/qi001_qualitative_summary.py`` (which stays as-is for QI-001
reproducibility). It works for any ``handcrafted_table`` experiment whose
fixtures encode a ground-truth graph, and in particular handles QI-003's
parent-position variants by deriving the expected parents of ``x2`` directly
from each fixture's edges (no hard-coded motif->parent map).

Scope: parent-set recovery via ABA Learning. NOT Russo-style Causal ABA: no
graph recovery, no d-separation, no stable-extension-as-DAG machinery.

Reporting choices (see METRICS.md): leads with the variable-level set metrics
and ``clean_recovery``; reports ``ancestor_only_rate`` and ``body_parent_recall``
as the proxy/parent diagnostics; reports the folding budget and assumption
counts. It deliberately does NOT print ``body_parent_f1`` (rule-level/lenient;
retained in the schema only for cross-experiment stability).

Modes:
- pending-run (no grid artefacts): lists planned cells, expected parents, examples;
- post-run (metrics.json present): adds learned rules, recovered variables, the
  variable-level metrics, and a clean-recovery aggregate.

Usage (Prolog-free; does not run ABA Learning):
    python causal/scripts/motif_recovery_summary.py --experiment QI002_minimal_motifs
    python causal/scripts/motif_recovery_summary.py --experiment QI003_scaled_motifs
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_THIS = Path(__file__).resolve()
_REPO_ROOT = _THIS.parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from causal.experiments.config import CellSpec, expand_cells, load_config
from causal.experiments.handcrafted import HandcraftedFixture, load_handcrafted
from causal.experiments.paths import grid_root, repo_root
from causal.metrics import (
    _rule_body_var_set,
    parse_delta_rules,
    target_rule_filter,
)

_TARGET = "x2"

_MODE_LABEL: dict[str, str] = {
    "binary": "binary 0/1",
    "cat3": "categorical (3 values)",
    "cont3": "continuous (3 uniform bins)",
}

# Outcomes meaning the learner ran but produced no usable solution.
_NO_SOLUTION_OUTCOMES = {
    "completed_no_solution",
    "completed_empty_delta",
    "skipped",
    "timeout",
}

# Human-written experiment records use the form ``QI-002`` / ``M11``.
_HUMAN_RECORD_RE = re.compile(r"^[A-Z]{2}-\d+$")


def parse_mode(dgp: str) -> str:
    """Infer the data-mode tag from a fixture/dgp id by trailing token."""
    for tag in ("binary", "cat3", "cont3"):
        if dgp.endswith(f"_{tag}"):
            return tag
    return "unknown"


def classify_recovery(
    *,
    metrics_present: bool,
    outcome: str | None,
    n_target_rules: int,
    recovered: set[str],
    expected: set[str],
) -> str:
    """Classify parent-set recovery for one cell (parents derived from edges)."""
    if not metrics_present:
        return "no_output_yet"
    if outcome == "error":
        return "parser_or_metric_failure"
    if outcome in _NO_SOLUTION_OUTCOMES:
        return "no_solution"
    if outcome != "solved":
        return "parser_or_metric_failure"
    if n_target_rules == 0:
        return "parser_or_metric_failure"
    if not recovered:
        return "rote_or_sample_specific"
    if recovered == expected:
        return "exact_parent_recovery"
    if recovered < expected:
        return "parent_subset"
    if expected < recovered:
        return "parent_superset"
    if recovered & expected:
        return "mixed_parent_and_non_parent"
    return "non_parent_or_proxy"


def _fmt_set(values: set[str]) -> str:
    return "{" + ", ".join(sorted(values)) + "}" if values else "{}"


def _fmt_examples(atoms: tuple[str, ...]) -> str:
    if not atoms:
        return "(none)"
    if len(atoms) > 12:
        head = ", ".join(f"`{a}`" for a in atoms[:12])
        return f"{head}, ... ({len(atoms)} total)"
    return ", ".join(f"`{a}`" for a in atoms)


def _fmt_edges(edges: tuple[tuple[int, int], ...]) -> str:
    return ", ".join(f"x{s} -> x{t}" for s, t in edges) if edges else "(none)"


def _fmt_metric(value: Any) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


def _fixture_table_md(fx: HandcraftedFixture) -> str:
    cols = list(fx.df.columns)
    header = "| sample_id | " + " | ".join(cols) + " |"
    sep = "| --- | " + " | ".join("---" for _ in cols) + " |"
    lines = [header, sep]
    for i, (_, row) in enumerate(fx.df.iterrows()):
        cells = [str(i + 1)] + [str(row[c]) for c in cols]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def _read_metrics(metrics_path: Path) -> dict[str, Any] | None:
    if not metrics_path.is_file():
        return None
    try:
        return json.loads(metrics_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _relpath(path: Path) -> str:
    try:
        return str(path.relative_to(repo_root()))
    except ValueError:
        return str(path)


def _recovered_from_rules(run_dir: Path) -> tuple[list[str], list[str], set[str], bool]:
    """Return (delta_rules, target_rules, recovered_vars, parse_failed)."""
    sol_path = run_dir / "bk.sol.aba"
    delta_rules: list[str] = []
    target_rules: list[str] = []
    recovered: set[str] = set()
    try:
        if sol_path.is_file():
            delta_rules = parse_delta_rules(sol_path)
            target_rules = target_rule_filter(_TARGET, delta_rules)
            for rule in target_rules:
                recovered |= _rule_body_var_set(rule)
            recovered.discard(_TARGET)
    except Exception:  # noqa: BLE001 - degrade gracefully per cell
        return delta_rules, target_rules, recovered, True
    return delta_rules, target_rules, recovered, False


def render_pending_block(
    cell: CellSpec, fx: HandcraftedFixture, mode: str, expected: set[str]
) -> str:
    lines = [
        f"### {cell.dgp}",
        "",
        f"- Source id: `{cell.dgp}`",
        f"- Data mode: {_MODE_LABEL.get(mode, mode)}",
        f"- Graph edges: {_fmt_edges(fx.edges)}",
        f"- Expected parents of `x2` (from edges): {_fmt_set(expected)}",
        f"- Rows: {len(fx.df)}",
        f"- Positive examples: {_fmt_examples(fx.pos_examples)}",
        f"- Negative examples: {_fmt_examples(fx.neg_examples)}",
        f"- Run status: pending (run_id `{cell.run_id}`)",
        "",
    ]
    if len(fx.df) <= 20:
        lines += ["Fixture table:", "", _fixture_table_md(fx), ""]
    return "\n".join(lines)


def render_postrun_block(
    cell: CellSpec,
    fx: HandcraftedFixture,
    mode: str,
    expected: set[str],
    run_dir: Path,
    metrics: dict[str, Any],
) -> tuple[str, str | None, int | None]:
    """Render one solved/failed cell. Returns (markdown, mode, clean_recovery)."""
    delta_rules, target_rules, recovered, parse_failed = _recovered_from_rules(run_dir)
    outcome = metrics.get("outcome")
    classification = classify_recovery(
        metrics_present=True,
        outcome=outcome if not parse_failed else "error",
        n_target_rules=len(target_rules),
        recovered=recovered,
        expected=expected,
    )
    clean = metrics.get("clean_recovery")

    lines = [
        f"### {cell.dgp}",
        "",
        f"- Source id: `{cell.dgp}`",
        f"- Data mode: {_MODE_LABEL.get(mode, mode)}",
        f"- Graph edges: {_fmt_edges(fx.edges)}",
        f"- Expected parents of `x2` (from edges): {_fmt_set(expected)}",
        f"- Rows: {len(fx.df)}",
        f"- Run directory: `{_relpath(run_dir)}`",
        f"- Outcome: `{outcome}`",
        f"- Recovered body variables: {_fmt_set(recovered)}",
        f"- Recovery classification: `{classification}`",
        f"- clean_recovery: `{_fmt_metric(clean)}`",
        (
            "- variable-level P/R/Jaccard: "
            f"{_fmt_metric(metrics.get('var_parent_precision'))} / "
            f"{_fmt_metric(metrics.get('var_parent_recall'))} / "
            f"{_fmt_metric(metrics.get('var_parent_jaccard'))}"
        ),
        (
            "- ancestor_only_rate / body_parent_recall: "
            f"{_fmt_metric(metrics.get('ancestor_only_rate'))} / "
            f"{_fmt_metric(metrics.get('body_parent_recall'))}"
        ),
        (
            "- Prolog-aware coverage (acc/pos/neg): "
            f"{_fmt_metric(metrics.get('cov_pl_accuracy'))} / "
            f"{_fmt_metric(metrics.get('cov_pl_pos'))} / "
            f"{_fmt_metric(metrics.get('cov_pl_neg'))}"
        ),
        (
            "- assumptions / contraries / folding_tokens: "
            f"{_fmt_metric(metrics.get('n_assumptions'))} / "
            f"{_fmt_metric(metrics.get('n_contraries'))} / "
            f"{_fmt_metric(metrics.get('folding_tokens_used'))}"
        ),
        "",
        f"x2 target rules ({len(target_rules)}):",
        "",
        "```prolog",
    ]
    lines.extend(target_rules if target_rules else ["% (no x2-headed target rules)"])
    lines += ["```", ""]

    clean_int = int(clean) if isinstance(clean, (int, float)) else None
    return "\n".join(lines), mode, clean_int


def _aggregate_block(
    rows: list[tuple[str, str | None, int | None]],
) -> str:
    """Build the clean-recovery aggregate (overall + per mode), over solved cells."""
    solved = [(mode, clean) for _dgp, mode, clean in rows if clean is not None]
    lines = ["## Aggregate (clean_recovery over cells with metrics)", ""]
    if not solved:
        lines += ["No cells with metrics yet.", ""]
        return "\n".join(lines)

    overall = sum(c for _m, c in solved) / len(solved)
    lines.append(f"- Overall clean-recovery rate: {overall:.3f} ({len(solved)} cells)")
    by_mode: dict[str, list[int]] = {}
    for mode, clean in solved:
        by_mode.setdefault(mode or "unknown", []).append(clean)
    for mode in sorted(by_mode):
        vals = by_mode[mode]
        lines.append(
            f"- {_MODE_LABEL.get(mode, mode)}: "
            f"{sum(vals) / len(vals):.3f} ({sum(vals)}/{len(vals)})"
        )
    lines.append("")
    return "\n".join(lines)


def build_summary(experiment_id: str, config_path: Path) -> tuple[str, int, int]:
    cfg = load_config(config_path)
    cells = expand_cells(cfg, config_path=config_path)
    out_root = grid_root() / experiment_id

    blocks: list[str] = []
    agg_rows: list[tuple[str, str | None, int | None]] = []
    n_with_artefacts = 0
    for cell in cells:
        source = cell.handcrafted_source
        if source is None:
            raise ValueError(f"cell {cell.run_id} has no handcrafted_source")
        fx = load_handcrafted(source)
        mode = parse_mode(source)
        expected = set(fx.ground_truth().parents_of(_TARGET))

        run_dir = out_root / "cells" / cell.run_id
        metrics = _read_metrics(run_dir / "metrics.json")
        if metrics is None:
            blocks.append(render_pending_block(cell, fx, mode, expected))
            agg_rows.append((cell.dgp, mode, None))
        else:
            n_with_artefacts += 1
            block, mode_tag, clean = render_postrun_block(
                cell, fx, mode, expected, run_dir, metrics
            )
            blocks.append(block)
            agg_rows.append((cell.dgp, mode_tag, clean))

    n_cells = len(cells)
    if n_with_artefacts == 0:
        status = "pending run (no grid artefacts found)"
    elif n_with_artefacts < n_cells:
        status = f"partial run ({n_with_artefacts}/{n_cells} cells have artefacts)"
    else:
        status = "complete run (all cells have artefacts)"

    header = [
        f"# Motif recovery summary: {experiment_id}",
        "",
        "Generated artefact-collecting summary. Do not edit by hand; regenerate "
        "with `causal/scripts/motif_recovery_summary.py`.",
        "",
        "Scope: parent-set recovery via ABA Learning. NOT Russo-style Causal ABA "
        "(no graph recovery, d-separation, or stable-extension-as-DAG claims). "
        "Expected parents are derived from each fixture's ground-truth edges, so "
        "parent-position variants are handled correctly. `body_parent_f1` is "
        "intentionally omitted (see METRICS.md).",
        "",
        f"- Experiment: `{experiment_id}`",
        f"- Config: `{_relpath(config_path)}`",
        f"- Output root: `{_relpath(out_root)}`",
        f"- Status: {status}",
        f"- Cells: {n_cells}",
        f"- Generated at: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Recovery classifications: `exact_parent_recovery`, `parent_subset`, "
        "`parent_superset`, `non_parent_or_proxy`, `mixed_parent_and_non_parent`, "
        "`rote_or_sample_specific`, `no_solution`, `no_output_yet`, "
        "`parser_or_metric_failure`.",
        "",
    ]
    markdown = (
        "\n".join(header)
        + _aggregate_block(agg_rows)
        + "\n## Cells\n\n"
        + "\n".join(blocks)
    )
    return markdown, n_cells, n_with_artefacts


def default_output_path(experiment_id: str) -> Path:
    return (
        repo_root()
        / "docs"
        / "experiments"
        / "qualitative"
        / f"{experiment_id}_summary.md"
    )


def default_config_path(experiment_id: str) -> Path:
    return repo_root() / "causal" / "configs" / "experiments" / f"{experiment_id}.yaml"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Generate a generalized motif parent-recovery summary"
    )
    p.add_argument("--experiment", required=True, help="experiment id")
    p.add_argument("--config", type=Path, default=None)
    p.add_argument("--output", type=Path, default=None)
    args = p.parse_args(argv)

    config_path = (
        Path(args.config)
        if args.config is not None
        else default_config_path(args.experiment)
    )
    output_path = (
        Path(args.output)
        if args.output is not None
        else default_output_path(args.experiment)
    )

    # Guard against clobbering a human-written experiment record (e.g. QI-002.md).
    if _HUMAN_RECORD_RE.match(output_path.stem):
        raise SystemExit(
            f"refusing to overwrite human-written record {output_path.name}; "
            "choose a different --output (summaries use the *_summary.md suffix)"
        )

    markdown, n_cells, n_with = build_summary(args.experiment, config_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")

    print(f"wrote {output_path}")
    print(f"{n_cells} cells: {n_cells - n_with} pending, {n_with} with artefacts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
