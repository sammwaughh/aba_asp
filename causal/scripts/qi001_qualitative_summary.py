"""Generate the QI-001 qualitative summary Markdown report.

This is reporting infrastructure, distinct from the human-written experiment
record at ``docs/experiments/qualitative/QI-001.md``. The human record explains
the investigation; this generated summary collects per-cell inputs and (once a
grid run exists) per-cell learned-rule artefacts and metrics.

Scope: parent-set recovery via ABA Learning. This is NOT full Russo-style Causal
ABA: no graph recovery, no d-separation, no stable-extension-as-DAG machinery.

Modes:
- pending-run (no grid artefacts yet): lists all planned cells with fixture
  tables, expected parents, examples, and expected predicate encoding;
- post-run (grid artefacts present under
  ``causal/outputs/aba_learning/grid/<experiment>/cells/<run_id>/``): adds
  learned delta rules, target-rule bodies, recovered base variables, metrics,
  and a recovery classification per cell.

Usage (Prolog-free; does not run ABA Learning):
    python causal/scripts/qi001_qualitative_summary.py --experiment QI001_motifs_modes
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Ensure the repo root is importable when run as a plain script.
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

# Motif name -> expected parents of x2 (cross-checked against fixture edges).
_MOTIF_PARENTS: dict[str, set[str]] = {
    "chain": {"x1"},
    "fork": {"x0"},
    "collider": {"x0", "x1"},
}

# Data-mode tag -> human description of the expected BK predicate encoding.
_MODE_ENCODING: dict[str, str] = {
    "binary": "bare predicates, e.g. `x0(A)`",
    "cat3": "`_val_` predicates, e.g. `x0_val_2(A)`",
    "cont3": "`_bin` predicates, e.g. `x0_bin2(A)`",
}

_MODE_LABEL: dict[str, str] = {
    "binary": "binary 0/1",
    "cat3": "categorical (3 values)",
    "cont3": "continuous (3 uniform bins)",
}

_TARGET = "x2"

# Outcomes that mean the learner ran but produced no usable solution.
_NO_SOLUTION_OUTCOMES = {
    "completed_no_solution",
    "completed_empty_delta",
    "skipped",
    "timeout",
}


def parse_source_id(source: str) -> tuple[str, str]:
    """Split a ``qi001_<motif>_<mode>`` source id into (motif, mode tag).

    Falls back to ("unknown", "unknown") for ids that do not match the pattern.
    """
    parts = source.split("_")
    if len(parts) >= 3 and parts[0] == "qi001":
        motif = parts[1]
        mode = "_".join(parts[2:])
        return motif, mode
    return "unknown", "unknown"


def classify_recovery(
    *,
    metrics_present: bool,
    outcome: str | None,
    n_target_rules: int,
    recovered: set[str],
    expected: set[str],
) -> str:
    """Classify parent-set recovery for one cell.

    ``recovered`` is the set of base body variables (e.g. {x0, x1}) cited by the
    x2-headed delta rules, with the target itself removed. ``expected`` is the
    true parent set of x2.
    """
    if not metrics_present:
        return "no_output_yet"
    if outcome == "error":
        return "parser_or_metric_failure"
    if outcome in _NO_SOLUTION_OUTCOMES:
        return "no_solution"
    if outcome != "solved":
        return "parser_or_metric_failure"

    # outcome == "solved"
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
    if not values:
        return "{}"
    return "{" + ", ".join(sorted(values)) + "}"


def _fmt_examples(atoms: tuple[str, ...]) -> str:
    return ", ".join(f"`{a}`" for a in atoms) if atoms else "(none)"


def _fmt_edges(edges: tuple[tuple[int, int], ...]) -> str:
    return ", ".join(f"x{s} -> x{t}" for s, t in edges) if edges else "(none)"


def _fixture_table_md(fx: HandcraftedFixture) -> str:
    """Render the tiny fixture table as Markdown with a 1-based sample_id column."""
    cols = list(fx.df.columns)
    header = "| sample_id | " + " | ".join(cols) + " |"
    sep = "| --- | " + " | ".join("---" for _ in cols) + " |"
    lines = [header, sep]
    for i, (_, row) in enumerate(fx.df.iterrows()):
        cells = [str(i + 1)] + [str(row[c]) for c in cols]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def _fmt_metric(value: Any) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


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


def render_pending_block(
    cell: CellSpec, fx: HandcraftedFixture, motif: str, mode: str, expected: set[str]
) -> str:
    lines: list[str] = []
    lines.append(f"### {cell.dgp}")
    lines.append("")
    lines.append(f"- Source id: `{cell.dgp}`")
    lines.append(f"- Motif: {motif}")
    lines.append(f"- Data mode: {_MODE_LABEL.get(mode, mode)}")
    lines.append(f"- Graph edges: {_fmt_edges(fx.edges)}")
    lines.append(f"- Target: `{cell.target}`")
    lines.append(f"- Expected parents of `x2`: {_fmt_set(expected)}")
    lines.append(f"- Positive examples: {_fmt_examples(fx.pos_examples)}")
    lines.append(f"- Negative examples: {_fmt_examples(fx.neg_examples)}")
    lines.append(f"- Expected predicate encoding: {_MODE_ENCODING.get(mode, 'unknown')}")
    lines.append(f"- Run status: pending (run_id `{cell.run_id}`)")
    lines.append("")
    lines.append("Fixture table:")
    lines.append("")
    lines.append(_fixture_table_md(fx))
    lines.append("")
    lines.append("Interpretation notes:")
    lines.append("")
    lines.append("```text")
    lines.append("")
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def render_postrun_block(
    cell: CellSpec,
    fx: HandcraftedFixture,
    motif: str,
    mode: str,
    expected: set[str],
    run_dir: Path,
    metrics: dict[str, Any],
) -> str:
    lines: list[str] = []
    lines.append(f"### {cell.dgp}")
    lines.append("")
    lines.append(f"- Source id: `{cell.dgp}`")
    lines.append(f"- Motif: {motif}")
    lines.append(f"- Data mode: {_MODE_LABEL.get(mode, mode)}")
    lines.append(f"- Graph edges: {_fmt_edges(fx.edges)}")
    lines.append(f"- Target: `{cell.target}`")
    lines.append(f"- Expected parents of `x2`: {_fmt_set(expected)}")
    lines.append(f"- Run directory: `{_relpath(run_dir)}`")

    # Artefact paths (only if present).
    artefacts = {
        "data.csv": run_dir / "data.csv",
        "bk.aba": run_dir / "bk.aba",
        "bk.sol.aba": run_dir / "bk.sol.aba",
        "metrics.json": run_dir / "metrics.json",
    }
    for label, path in artefacts.items():
        if path.is_file():
            lines.append(f"- {label}: `{_relpath(path)}`")

    outcome = metrics.get("outcome")
    lines.append(f"- Outcome: `{outcome}`")

    # Learned rules: reuse metrics parsers (graceful on missing/garbled files).
    sol_path = run_dir / "bk.sol.aba"
    delta_rules: list[str] = []
    target_rules: list[str] = []
    recovered: set[str] = set()
    parse_failed = False
    try:
        if sol_path.is_file():
            delta_rules = parse_delta_rules(sol_path)
            target_rules = target_rule_filter(_TARGET, delta_rules)
            for rule in target_rules:
                recovered |= _rule_body_var_set(rule)
            recovered.discard(_TARGET)
    except Exception:  # noqa: BLE001 - degrade gracefully per cell
        parse_failed = True

    classification = classify_recovery(
        metrics_present=True,
        outcome=outcome if not parse_failed else "error",
        n_target_rules=len(target_rules),
        recovered=recovered,
        expected=expected,
    )

    lines.append(f"- Recovered body variables: {_fmt_set(recovered)}")
    lines.append(f"- Recovery classification: `{classification}`")
    lines.append(
        "- body-parent P/R/F1: "
        f"{_fmt_metric(metrics.get('body_parent_precision'))} / "
        f"{_fmt_metric(metrics.get('body_parent_recall'))} / "
        f"{_fmt_metric(metrics.get('body_parent_f1'))}"
    )
    lines.append(
        "- Python coverage (acc/pos/neg): "
        f"{_fmt_metric(metrics.get('cov_py_accuracy'))} / "
        f"{_fmt_metric(metrics.get('cov_py_pos'))} / "
        f"{_fmt_metric(metrics.get('cov_py_neg'))}"
    )
    if metrics.get("cov_pl_accuracy") is not None:
        lines.append(
            "- Prolog-aware coverage (acc/pos/neg): "
            f"{_fmt_metric(metrics.get('cov_pl_accuracy'))} / "
            f"{_fmt_metric(metrics.get('cov_pl_pos'))} / "
            f"{_fmt_metric(metrics.get('cov_pl_neg'))}"
        )
    lines.append(
        "- assumptions / contraries: "
        f"{_fmt_metric(metrics.get('n_assumptions'))} / "
        f"{_fmt_metric(metrics.get('n_contraries'))}"
    )
    lines.append(f"- delta rules ({len(delta_rules)}):")
    lines.append("")
    lines.append("```prolog")
    if delta_rules:
        lines.extend(delta_rules)
    else:
        lines.append("% (no delta rules)")
    lines.append("```")
    lines.append("")
    lines.append(f"x2 target rules ({len(target_rules)}):")
    lines.append("")
    lines.append("```prolog")
    if target_rules:
        lines.extend(target_rules)
    else:
        lines.append("% (no x2-headed target rules)")
    lines.append("```")
    lines.append("")
    lines.append("Interpretation notes:")
    lines.append("")
    lines.append("```text")
    lines.append("")
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def build_summary(experiment_id: str, config_path: Path) -> tuple[str, int, int]:
    """Build the Markdown summary string. Returns (markdown, n_cells, n_with_artefacts)."""
    cfg = load_config(config_path)
    cells = expand_cells(cfg, config_path=config_path)
    out_root = grid_root() / experiment_id

    blocks: list[str] = []
    n_with_artefacts = 0
    for cell in cells:
        source = cell.handcrafted_source
        if source is None:
            raise ValueError(f"cell {cell.run_id} has no handcrafted_source")
        fx = load_handcrafted(source)
        motif, mode = parse_source_id(source)
        expected = set(fx.ground_truth().parents_of(_TARGET))
        # Cross-check the parsed-motif parent set against fixture edges.
        if motif in _MOTIF_PARENTS and _MOTIF_PARENTS[motif] != expected:
            raise ValueError(
                f"motif/edge mismatch for {source}: id implies "
                f"{_MOTIF_PARENTS[motif]} but edges give {expected}"
            )

        run_dir = out_root / "cells" / cell.run_id
        metrics = _read_metrics(run_dir / "metrics.json")
        if metrics is None:
            blocks.append(render_pending_block(cell, fx, motif, mode, expected))
        else:
            n_with_artefacts += 1
            blocks.append(
                render_postrun_block(cell, fx, motif, mode, expected, run_dir, metrics)
            )

    n_cells = len(cells)
    if n_with_artefacts == 0:
        mode_line = "pending run (no grid artefacts found)"
    elif n_with_artefacts < n_cells:
        mode_line = f"partial run ({n_with_artefacts}/{n_cells} cells have artefacts)"
    else:
        mode_line = "complete run (all cells have artefacts)"

    header: list[str] = []
    header.append(f"# QI-001 generated summary: {experiment_id}")
    header.append("")
    header.append(
        "Generated artefact-collecting summary (distinct from the human-written "
        "record `docs/experiments/qualitative/QI-001.md`). Do not edit by hand; "
        "regenerate with the command below."
    )
    header.append("")
    header.append(
        "Scope: parent-set recovery via ABA Learning. This is NOT full Russo-style "
        "Causal ABA and makes no graph-recovery, d-separation, or "
        "stable-extension-as-DAG claims."
    )
    header.append("")
    header.append(f"- Experiment: `{experiment_id}`")
    header.append(f"- Config: `{_relpath(config_path)}`")
    header.append(f"- Output root: `{_relpath(out_root)}`")
    header.append(f"- Status: {mode_line}")
    header.append(f"- Cells: {n_cells}")
    header.append(f"- Generated at: {datetime.now(timezone.utc).isoformat()}")
    header.append("")
    header.append(
        "Recovery classifications: `exact_parent_recovery`, `parent_subset`, "
        "`parent_superset`, `non_parent_or_proxy`, `mixed_parent_and_non_parent`, "
        "`rote_or_sample_specific`, `no_solution`, `no_output_yet`, "
        "`parser_or_metric_failure`."
    )
    header.append("")
    header.append("## Cells")
    header.append("")

    markdown = "\n".join(header) + "\n".join(blocks)
    return markdown, n_cells, n_with_artefacts


def default_output_path(experiment_id: str) -> Path:
    if experiment_id == "QI001_motifs_modes":
        return repo_root() / "docs" / "experiments" / "qualitative" / "QI-001_summary.md"
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
        description="Generate the QI-001 qualitative summary Markdown report"
    )
    p.add_argument("--experiment", default="QI001_motifs_modes", help="experiment id")
    p.add_argument(
        "--config",
        type=Path,
        default=None,
        help="path to experiment YAML (default: causal/configs/experiments/<experiment>.yaml)",
    )
    p.add_argument(
        "--output",
        type=Path,
        default=None,
        help="output Markdown path (default: docs/experiments/qualitative/QI-001_summary.md)",
    )
    args = p.parse_args(argv)

    config_path = (
        Path(args.config) if args.config is not None else default_config_path(args.experiment)
    )
    output_path = (
        Path(args.output) if args.output is not None else default_output_path(args.experiment)
    )

    # Guard against clobbering the human-written record.
    human_record = repo_root() / "docs" / "experiments" / "qualitative" / "QI-001.md"
    if output_path.resolve() == human_record.resolve():
        raise SystemExit(
            "refusing to overwrite the human-written experiment record "
            f"{human_record}; choose a different --output"
        )

    markdown, n_cells, n_with = build_summary(args.experiment, config_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")

    print(f"wrote {output_path}")
    print(f"{n_cells} cells: {n_cells - n_with} pending, {n_with} with artefacts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
