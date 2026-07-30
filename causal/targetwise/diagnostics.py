"""Compact diagnostics for target-wise causal-fixture learning runs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

from causal.metrics import body_vars, parse_delta_rules, target_rule_filter
from causal.targetwise.semantics import ArtifactIntegrityCheckResult


TARGETWISE_RESULT_COLUMNS: tuple[str, ...] = (
    "experiment_id",
    "fixture_id",
    "configuration_id",
    "configuration_hash",
    "sample_name",
    "target",
    "n",
    "seed",
    "config_hash",
    "prolog_config_hash",
    "run_id",
    "outcome",
    "failure_reason",
    "aba_learning_runtime_s",
    "n_delta_rules",
    "n_target_rules",
    "n_assumptions",
    "n_contraries",
    "delta_rules_json",
    "target_rules_json",
    "assumptions_json",
    "contraries_json",
    "body_variables_json",
    "body_lengths_json",
    "max_body_length",
    "mean_body_length",
    "artifact_check_status",
    "artifact_check_failure_reason",
    "artifact_check_runtime_s",
    "parser_unread_lines",
    "solution_file_bytes",
    "solution_asp_file_bytes",
    "solution_check_asp_file_bytes",
)

_STRING_COLUMNS = frozenset(
    {
        "experiment_id",
        "fixture_id",
        "configuration_id",
        "configuration_hash",
        "sample_name",
        "target",
        "config_hash",
        "prolog_config_hash",
        "run_id",
        "outcome",
        "delta_rules_json",
        "target_rules_json",
        "assumptions_json",
        "contraries_json",
        "body_variables_json",
        "body_lengths_json",
        "artifact_check_status",
    }
)
_NULLABLE_STRING_COLUMNS = frozenset(
    {"failure_reason", "artifact_check_failure_reason"}
)
_INTEGER_COLUMNS = frozenset(
    {
        "n",
        "seed",
        "n_delta_rules",
        "n_target_rules",
        "n_assumptions",
        "n_contraries",
        "max_body_length",
        "parser_unread_lines",
        "solution_file_bytes",
        "solution_asp_file_bytes",
        "solution_check_asp_file_bytes",
    }
)
_FLOAT_COLUMNS = frozenset(
    {
        "aba_learning_runtime_s",
        "mean_body_length",
        "artifact_check_runtime_s",
    }
)


def _parse_rule_lines(text: str) -> list[str]:
    parsed: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("%"):
            continue
        if ":-" in line or line.endswith("."):
            parsed.append(line)
    return parsed


def _count_parser_unread_lines(solution_path: Path | None) -> int:
    if solution_path is None or not Path(solution_path).is_file():
        return 0
    text = Path(solution_path).read_text(encoding="utf-8")
    parsed = set(_parse_rule_lines(text))
    return sum(
        1
        for raw in text.splitlines()
        if (line := raw.strip()) and not line.startswith("%") and line not in parsed
    )


def _split_body_literals(rule: str) -> list[str]:
    if ":-" not in rule:
        return []
    body = rule.split(":-", 1)[1].strip().rstrip(".")
    if not body:
        return []
    literals: list[str] = []
    start = 0
    depth = 0
    for index, character in enumerate(body):
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
        elif character == "," and depth == 0:
            literals.append(body[start:index].strip())
            start = index + 1
    literals.append(body[start:].strip())
    return [literal for literal in literals if literal]


def build_targetwise_diagnostics(
    *,
    experiment_id: str,
    fixture_id: str,
    configuration_id: str,
    configuration_hash: str,
    sample_name: str,
    target: str,
    n: int,
    seed: int,
    config_hash: str,
    prolog_config_hash: str,
    run_id: str,
    outcome: str,
    failure_reason: str | None,
    aba_learning_runtime_s: float,
    solution_path: Path | None,
    solution_asp_path: Path | None,
    solution_check_asp_path: Path | None,
    artifact_integrity_check: ArtifactIntegrityCheckResult,
    provenance: Mapping[str, Any],
) -> dict[str, Any]:
    """Build the complete target-wise diagnostics document."""

    learned = (
        parse_delta_rules(solution_path)
        if solution_path is not None and Path(solution_path).is_file()
        else []
    )
    target_rules = target_rule_filter(target, learned)
    assumptions = [rule for rule in learned if rule.startswith("assumption(")]
    contraries = [rule for rule in learned if rule.startswith("contrary(")]

    body_details: list[dict[str, Any]] = []
    all_body_variables: set[str] = set()
    body_lengths: list[int] = []
    for rule in target_rules:
        literals = _split_body_literals(rule)
        variables = sorted(body_vars(" ".join(literals)))
        all_body_variables.update(variables)
        body_lengths.append(len(literals))
        body_details.append(
            {
                "rule": rule,
                "body_literals": literals,
                "body_variables": variables,
                "body_length": len(literals),
            }
        )

    solution_bytes = (
        Path(solution_path).stat().st_size
        if solution_path is not None and Path(solution_path).is_file()
        else 0
    )
    solution_asp_bytes = (
        Path(solution_asp_path).stat().st_size
        if solution_asp_path is not None and Path(solution_asp_path).is_file()
        else 0
    )
    solution_check_asp_bytes = (
        Path(solution_check_asp_path).stat().st_size
        if solution_check_asp_path is not None
        and Path(solution_check_asp_path).is_file()
        else 0
    )

    return {
        "targetwise_metrics_schema_version": 2,
        "experiment_id": experiment_id,
        "fixture_id": fixture_id,
        "configuration_id": configuration_id,
        "configuration_hash": configuration_hash,
        "sample_name": sample_name,
        "target": target,
        "n": n,
        "seed": seed,
        "config_hash": config_hash,
        "prolog_config_hash": prolog_config_hash,
        "run_id": run_id,
        "outcome": outcome,
        "failure_reason": failure_reason,
        "aba_learning_runtime_s": aba_learning_runtime_s,
        "n_delta_rules": len(learned),
        "n_target_rules": len(target_rules),
        "n_assumptions": len(assumptions),
        "n_contraries": len(contraries),
        "delta_rules": learned,
        "target_rules": target_rules,
        "assumptions": assumptions,
        "contraries": contraries,
        "body_variables": sorted(all_body_variables),
        "body_lengths": body_lengths,
        "max_body_length": max(body_lengths, default=0),
        "mean_body_length": (
            sum(body_lengths) / len(body_lengths) if body_lengths else None
        ),
        "target_rule_body_details": body_details,
        "artifact_check_status": artifact_integrity_check.status,
        "artifact_check_failure_reason": artifact_integrity_check.failure_reason,
        "artifact_check_runtime_s": artifact_integrity_check.runtime_s,
        "artifact_integrity_check": artifact_integrity_check.as_dict(),
        "parser_unread_lines": _count_parser_unread_lines(solution_path),
        "solution_file_bytes": solution_bytes,
        "solution_asp_file_bytes": solution_asp_bytes,
        "solution_check_asp_file_bytes": solution_check_asp_bytes,
        "solution_path": str(solution_path) if solution_path is not None else None,
        "solution_asp_path": (
            str(solution_asp_path) if solution_asp_path is not None else None
        ),
        "solution_check_asp_path": (
            str(solution_check_asp_path)
            if solution_check_asp_path is not None
            else None
        ),
        "provenance": dict(provenance),
    }


def _json_list(value: Sequence[Any]) -> str:
    return json.dumps(list(value), separators=(",", ":"), ensure_ascii=True)


def diagnostics_to_parquet_row(metrics: Mapping[str, Any]) -> dict[str, Any]:
    """Flatten retained diagnostics into one aggregation-safe Parquet row."""

    row = {
        key: metrics[key]
        for key in TARGETWISE_RESULT_COLUMNS
        if key
        not in {
            "delta_rules_json",
            "target_rules_json",
            "assumptions_json",
            "contraries_json",
            "body_variables_json",
            "body_lengths_json",
        }
    }
    row.update(
        {
            "delta_rules_json": _json_list(metrics["delta_rules"]),
            "target_rules_json": _json_list(metrics["target_rules"]),
            "assumptions_json": _json_list(metrics["assumptions"]),
            "contraries_json": _json_list(metrics["contraries"]),
            "body_variables_json": _json_list(metrics["body_variables"]),
            "body_lengths_json": _json_list(metrics["body_lengths"]),
        }
    )
    return row


def diagnostics_dataframe(rows: Sequence[Mapping[str, Any]]) -> pd.DataFrame:
    """Create a typed DataFrame containing only approved target-wise fields."""

    frame = pd.DataFrame(
        [diagnostics_to_parquet_row(row) for row in rows],
        columns=list(TARGETWISE_RESULT_COLUMNS),
    )
    for column in _STRING_COLUMNS | _NULLABLE_STRING_COLUMNS:
        frame[column] = frame[column].astype("string")
    for column in _INTEGER_COLUMNS:
        frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0)
        frame[column] = frame[column].astype("int64")
    for column in _FLOAT_COLUMNS:
        frame[column] = pd.to_numeric(frame[column], errors="coerce").astype("float64")
    object_columns = [
        column for column in frame.columns if frame[column].dtype == object
    ]
    if object_columns:
        raise TypeError(f"object-typed target-wise columns: {object_columns}")
    return frame


def write_targetwise_metrics(
    cell_directory: Path,
    metrics: Mapping[str, Any],
) -> tuple[Path, Path]:
    """Write one inspectable JSON document and one typed Parquet shard."""

    cell_directory = Path(cell_directory)
    cell_directory.mkdir(parents=True, exist_ok=True)
    json_path = cell_directory / "metrics.json"
    parquet_path = cell_directory / "metrics.parquet"
    json_path.write_text(
        json.dumps(metrics, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    diagnostics_dataframe([metrics]).to_parquet(
        parquet_path,
        index=False,
        engine="pyarrow",
    )
    return json_path, parquet_path


def write_targetwise_results(collection_directory: Path) -> Path:
    """Concatenate target shards into the compact collection result table."""

    collection_directory = Path(collection_directory)
    shard_paths = sorted((collection_directory / "cells").glob("target-*/metrics.json"))
    rows = [json.loads(path.read_text(encoding="utf-8")) for path in shard_paths]
    output = collection_directory / "results.parquet"
    diagnostics_dataframe(rows).to_parquet(output, index=False, engine="pyarrow")
    return output
