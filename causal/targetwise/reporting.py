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
        "configuration_id": config.configuration_id,
        "configuration_hash": config.configuration_hash,
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
        "artifact_check_status": metrics["artifact_check_status"],
        "artifact_check_failure_reason": metrics["artifact_check_failure_reason"],
        "artifact_check_runtime_s": metrics["artifact_check_runtime_s"],
        "integrity": {
            "parser_unread_lines": metrics["parser_unread_lines"],
            "solution_file_bytes": metrics["solution_file_bytes"],
            "solution_asp_file_bytes": metrics["solution_asp_file_bytes"],
            "solution_check_asp_file_bytes": metrics[
                "solution_check_asp_file_bytes"
            ],
        },
        "artefacts": {
            "data": str(cell_paths.data_path),
            "background_knowledge": str(cell_paths.bk_path),
            "examples": str(cell_paths.examples_path),
            "task_manifest": str(cell_paths.task_manifest_path),
            "solution": metrics["solution_path"],
            "solution_asp": metrics["solution_asp_path"],
            "solution_check_asp": metrics["solution_check_asp_path"],
            "delta": metrics["delta_path"],
            "prolog_stdout": str(cell_paths.output_dir / "prolog.stdout"),
            "prolog_stderr": str(cell_paths.output_dir / "prolog.stderr"),
            "metrics": str(cell_paths.metrics_json_path),
        },
        "learner": {
            "configuration_id": config.configuration_id,
            "configuration_hash": config.configuration_hash,
            "prolog_config": str(config.prolog_config),
            "prolog_config_sha256": config.prolog_config_hash,
            "learning_mode": config.learning_mode,
            "config_hash": config.config_hash,
        },
        "boundary": (
            "The artefact audit executes the learner-produced .sol_chk.asp file. "
            "That file already contains the final framework serialization and the "
            "joint E+/E- integrity constraints emitted under check_ic. The audit "
            "checks final-file satisfiability; it is not a new coverage metric, an "
            "independent per-example acceptance table, or a graph decoder."
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
    check_reason = summary["artifact_check_failure_reason"] or "none"
    lines = [
        f"# Target-wise cell: {task.target}",
        "",
        f"- **Fixture:** `{bundle.fixture_id}`",
        f"- **Configuration:** `{config.configuration_id}`",
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
            "## Final-artefact integrity audit",
            "",
            f"- **Status:** `{summary['artifact_check_status']}`",
            f"- **Runtime:** {summary['artifact_check_runtime_s']:.6f} seconds",
            f"- **Failure reason:** {check_reason}",
            "",
            (
                "Clingo is run directly on the learner-produced `.sol_chk.asp`. "
                "A `SAT` result confirms that this final serialized checked "
                "artefact has a witnessing stable model. Because the learner "
                "already applies the corresponding joint condition internally, "
                "this is an artefact-integrity audit rather than an additional "
                "learner-performance or coverage metric."
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
            f"- **Checked ASP solution bytes:** "
            f"{summary['integrity']['solution_check_asp_file_bytes']}",
            "",
            "## Artefacts",
            "",
            f"- Input table: `{cell_paths.data_path}`",
            f"- Background knowledge: `{cell_paths.bk_path}`",
            f"- Positive/negative examples: `{cell_paths.examples_path}`",
            f"- Task manifest: `{cell_paths.task_manifest_path}`",
            f"- Raw learner output: `{cell_paths.output_dir}`",
            f"- Checked ASP artefact: "
            f"`{summary['artefacts']['solution_check_asp'] or 'missing'}`",
            f"- Learned delta: `{summary['artefacts']['delta'] or 'missing'}`",
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
        "summary_schema_version": 4,
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
        "configuration": {
            "id": config.configuration_id,
            "hash": config.configuration_hash,
            "manifest": str(paths.configuration_manifest_path),
        },
        "learner": {
            "prolog_config": str(config.prolog_config),
            "prolog_config_sha256": config.prolog_config_hash,
            "learning_mode": config.learning_mode,
            "config_hash": config.config_hash,
        },
        "targets": list(cells),
        "boundary": (
            "Target outputs are retained separately. The post-run Clingo invocation "
            "executes each learner-produced .sol_chk.asp only as a final-artefact "
            "integrity audit; it is not counted as a separate coverage metric. No "
            "per-example coverage panel, parent-set score, union-of-rules graph "
            "decoder, CPDAG construction, or graph-level recovery claim is applied."
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
        f"- **Configuration:** `{config.configuration_id}`",
        f"- **Configuration hash:** `{config.configuration_hash}`",
        f"- **Sample hash:** `{bundle.sample_hash}`",
        f"- **Encoding:** `{config.encoding_type}` / `{config.example_policy}`",
        f"- **Learner configuration:** `{config.prolog_config}`",
        f"- **Learning mode:** `{config.learning_mode}`",
        f"- **Targets:** {len(cells)}",
        "",
        "| target | E+ | E- | outcome | delta rules | target rules | assumptions | contraries | body variables | body lengths | artefact audit | ABA runtime (s) | audit runtime (s) |",
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
            f"{cell['artifact_check_status']} | "
            f"{cell['aba_learning_runtime_s']:.6f} | "
            f"{cell['artifact_check_runtime_s']:.6f} |"
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
