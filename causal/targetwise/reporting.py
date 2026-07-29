"""Inspectable per-target and collection reports for target-wise runs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from causal.fixtures.artifacts import write_text_once
from causal.targetwise.bundle import LoadedCausalFixtureBundle
from causal.targetwise.config import TargetwiseRunConfig
from causal.targetwise.encoding import BinaryTargetTask
from causal.targetwise.paths import TargetCellPaths, TargetwiseCollectionPaths


def build_target_summary(
    *,
    bundle: LoadedCausalFixtureBundle,
    config: TargetwiseRunConfig,
    task: BinaryTargetTask,
    cell_paths: TargetCellPaths,
    metrics: Mapping[str, Any],
) -> dict[str, Any]:
    """Select the retained diagnostics for one target and its report paths."""

    return {
        "target": task.target,
        "predictor_order": list(task.predictor_order),
        "n_positive": task.n_positive,
        "n_negative": task.n_negative,
        "outcome": metrics["outcome"],
        "failure_reason": metrics["failure_reason"],
        "aba_learning_runtime_s": metrics["aba_learning_runtime_s"],
        "n_delta_rules": metrics["n_delta_rules"],
        "n_target_rules": metrics["n_target_rules"],
        "n_assumptions": metrics["n_assumptions"],
        "n_contraries": metrics["n_contraries"],
        "delta_rules": list(metrics["delta_rules"]),
        "target_rules": list(metrics["target_rules"]),
        "assumptions": list(metrics["assumptions"]),
        "contraries": list(metrics["contraries"]),
        "body_variables": list(metrics["body_variables"]),
        "body_lengths": list(metrics["body_lengths"]),
        "max_body_length": metrics["max_body_length"],
        "mean_body_length": metrics["mean_body_length"],
        "target_rule_body_details": list(metrics["target_rule_body_details"]),
        "joint_brave_status": metrics["joint_brave_status"],
        "joint_brave_failure_reason": metrics["joint_brave_failure_reason"],
        "joint_brave_runtime_s": metrics["joint_brave_runtime_s"],
        "integrity": {
            "parser_unread_lines": metrics["parser_unread_lines"],
            "solution_file_bytes": metrics["solution_file_bytes"],
            "solution_asp_file_bytes": metrics["solution_asp_file_bytes"],
        },
        "artefacts": {
            "data": str(cell_paths.data_path),
            "background_knowledge": str(cell_paths.bk_path),
            "examples": str(cell_paths.examples_path),
            "task_manifest": str(cell_paths.task_manifest_path),
            "solution": metrics["solution_path"],
            "solution_asp": metrics["solution_asp_path"],
            "prolog_stdout": str(cell_paths.output_dir / "prolog.stdout"),
            "prolog_stderr": str(cell_paths.output_dir / "prolog.stderr"),
            "metrics": str(cell_paths.metrics_json_path),
        },
        "learner": {
            "prolog_config": str(config.prolog_config),
            "prolog_config_sha256": config.prolog_config_hash,
            "learning_mode": config.learning_mode,
            "config_hash": config.config_hash,
        },
        "boundary": (
            "The joint brave result asks only whether at least one stable model "
            "simultaneously contains every E+ atom and no E- atom. It is not an "
            "independent per-example acceptance table and does not interpret learned "
            "rule bodies as causal parents or decode a graph."
        ),
    }


def _rules_or_comment(rules: Sequence[str]) -> list[str]:
    return list(rules) if rules else ["% (none)"]


def _component_lines(label: str, rules: Sequence[str]) -> list[str]:
    lines = [f"### {label}", "", "```prolog"]
    lines.extend(_rules_or_comment(rules))
    lines.extend(["```", ""])
    return lines


def write_target_report(
    *,
    bundle: LoadedCausalFixtureBundle,
    config: TargetwiseRunConfig,
    task: BinaryTargetTask,
    cell_paths: TargetCellPaths,
    metrics: Mapping[str, Any],
) -> dict[str, Any]:
    """Write one concise Markdown report and return its summary document."""

    summary = build_target_summary(
        bundle=bundle,
        config=config,
        task=task,
        cell_paths=cell_paths,
        metrics=metrics,
    )
    check_reason = summary["joint_brave_failure_reason"] or "none"
    lines = [
        f"# Target-wise cell: {task.target}",
        "",
        f"- **Fixture:** `{bundle.fixture_id}`",
        f"- **Sample:** `{bundle.sample_name}` (n={bundle.n}, seed={bundle.seed})",
        f"- **Target:** `{task.target}`",
        f"- **Predictor order:** `{', '.join(task.predictor_order)}`",
        f"- **Examples:** E+={task.n_positive}, E-={task.n_negative}",
        f"- **Outcome:** `{summary['outcome']}`",
        f"- **Failure reason:** {summary['failure_reason'] or 'none'}",
        f"- **ABA Learning runtime:** "
        f"{summary['aba_learning_runtime_s']:.6f} seconds",
        f"- **Delta / target rules:** "
        f"{summary['n_delta_rules']} / {summary['n_target_rules']}",
        f"- **Assumptions / contraries:** "
        f"{summary['n_assumptions']} / {summary['n_contraries']}",
        f"- **Target-body variables:** "
        f"`{', '.join(summary['body_variables']) or 'none'}`",
        f"- **Target-body lengths:** " f"`{summary['body_lengths'] or 'none'}`",
        "",
        "## Learned rules",
        "",
        "### Complete learned delta",
        "",
        "```prolog",
        *_rules_or_comment(summary["delta_rules"]),
        "```",
        "",
        "### Target rules",
        "",
        "```prolog",
        *_rules_or_comment(summary["target_rules"]),
        "```",
        "",
        "## ABA components",
        "",
        *_component_lines("Assumptions", summary["assumptions"]),
        *_component_lines("Contraries", summary["contraries"]),
        "## Target-rule bodies",
        "",
        "| rule | body literals | body variables | length |",
        "|---|---|---|---:|",
    ]
    if summary["target_rule_body_details"]:
        for detail in summary["target_rule_body_details"]:
            lines.append(
                f"| `{detail['rule']}` | "
                f"`{', '.join(detail['body_literals']) or 'none'}` | "
                f"`{', '.join(detail['body_variables']) or 'none'}` | "
                f"{detail['body_length']} |"
            )
    else:
        lines.append("| none | none | none | 0 |")

    lines.extend(
        [
            "",
            "## Joint brave-task check",
            "",
            f"- **Status:** `{summary['joint_brave_status']}`",
            f"- **Runtime:** {summary['joint_brave_runtime_s']:.6f} seconds",
            f"- **Failure reason:** {check_reason}",
            "",
            (
                "Question checked: does the final serialized learned ABA framework "
                "have at least one stable model that simultaneously accepts every "
                "positive example and rejects every negative example?"
            ),
            "",
            "## Solution integrity",
            "",
            f"- **Parser-unread lines:** "
            f"{summary['integrity']['parser_unread_lines']}",
            f"- **ABA solution bytes:** "
            f"{summary['integrity']['solution_file_bytes']}",
            f"- **ASP solution bytes:** "
            f"{summary['integrity']['solution_asp_file_bytes']}",
            "",
            "## Artefacts",
            "",
            f"- Input table: `{cell_paths.data_path}`",
            f"- Background knowledge: `{cell_paths.bk_path}`",
            f"- Positive/negative examples: `{cell_paths.examples_path}`",
            f"- Task manifest: `{cell_paths.task_manifest_path}`",
            f"- Raw learner output: `{cell_paths.output_dir}`",
            f"- Metrics: `{cell_paths.metrics_json_path}`",
            "",
            "## Interpretation boundary",
            "",
            summary["boundary"],
            "",
        ]
    )
    write_text_once(cell_paths.report_path, "\n".join(lines))
    return summary


def write_collection_summary(
    *,
    bundle: LoadedCausalFixtureBundle,
    config: TargetwiseRunConfig,
    paths: TargetwiseCollectionPaths,
    cells: Sequence[Mapping[str, Any]],
) -> tuple[Path, Path]:
    """Write Markdown and JSON summaries across every target."""

    document = {
        "summary_schema_version": 2,
        "fixture": {
            "id": bundle.fixture_id,
            "semantic_hash": bundle.semantic_hash,
        },
        "sample": {
            "name": bundle.sample_name,
            "n": bundle.n,
            "seed": bundle.seed,
            "csv_sha256": bundle.sample_hash,
        },
        "encoding": {
            "type": config.encoding_type,
            "example_policy": config.example_policy,
        },
        "learner": {
            "prolog_config": str(config.prolog_config),
            "prolog_config_sha256": config.prolog_config_hash,
            "learning_mode": config.learning_mode,
            "config_hash": config.config_hash,
        },
        "targets": list(cells),
        "boundary": (
            "Target outputs are retained separately. Joint brave checks are one "
            "witness-existence query per target. No per-example coverage panel, "
            "parent-set score, union-of-rules graph decoder, CPDAG construction, "
            "or graph-level recovery claim is applied."
        ),
    }
    write_text_once(
        paths.summary_json_path,
        json.dumps(document, indent=2, sort_keys=True) + "\n",
    )

    lines = [
        f"# Target-complete collection: {bundle.fixture_id} / {bundle.sample_name}",
        "",
        f"- **Sample:** n={bundle.n}, seed={bundle.seed}",
        f"- **Sample hash:** `{bundle.sample_hash}`",
        f"- **Encoding:** `{config.encoding_type}` / `{config.example_policy}`",
        f"- **Learner configuration:** `{config.prolog_config}`",
        f"- **Learning mode:** `{config.learning_mode}`",
        f"- **Targets:** {len(cells)}",
        "",
        "| target | E+ | E- | outcome | delta rules | target rules | assumptions | contraries | body variables | body lengths | joint witness | ABA runtime (s) | check runtime (s) |",
        "|---|---:|---:|---|---:|---:|---:|---:|---|---|---|---:|---:|",
    ]
    for cell in cells:
        lines.append(
            f"| {cell['target']} | {cell['n_positive']} | {cell['n_negative']} | "
            f"{cell['outcome']} | {cell['n_delta_rules']} | "
            f"{cell['n_target_rules']} | {cell['n_assumptions']} | "
            f"{cell['n_contraries']} | "
            f"{', '.join(cell['body_variables']) or 'none'} | "
            f"{cell['body_lengths'] or 'none'} | "
            f"{cell['joint_brave_status']} | "
            f"{cell['aba_learning_runtime_s']:.6f} | "
            f"{cell['joint_brave_runtime_s']:.6f} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            document["boundary"],
            "",
        ]
    )
    write_text_once(paths.summary_markdown_path, "\n".join(lines))
    return paths.summary_markdown_path, paths.summary_json_path
