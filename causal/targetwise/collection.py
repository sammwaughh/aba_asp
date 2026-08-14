"""Preparation and serial execution of all-target ABA Learning collections."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import tempfile
import time
from typing import Any, Callable, Mapping, Sequence

from causal.fixtures.artifacts import (
    ArtifactConflictError,
    file_sha256,
    sha256_bytes,
    write_bytes_once,
    write_text_once,
)
from causal.metrics import (
    outcome_classifier,
    parse_delta_rules,
)
from causal.run_aba_asp import ABASPRunner
from causal.targetwise.bundle import (
    LoadedCausalFixtureBundle,
    load_causal_fixture_bundle,
)
from causal.targetwise.config import TargetwiseRunConfig
from causal.targetwise.diagnostics import (
    build_targetwise_diagnostics,
    write_targetwise_metrics,
    write_targetwise_results,
)
from causal.targetwise.encoding import (
    BinaryTargetTask,
    PREDICTOR_POLICY_ORACLE_PARENTS,
    build_binary_target_task,
)
from causal.targetwise.paths import TargetwiseCollectionPaths
from causal.targetwise.reporting import (
    write_collection_summary,
    write_target_report,
)
from causal.targetwise.semantics import (
    ArtifactIntegrityCheckResult,
    final_artifact_integrity_check,
    resolve_solution_asp_path,
    resolve_solution_check_asp_path,
    unavailable_artifact_integrity_check,
)


TARGETWISE_RUNNER_VERSION = 5


@dataclass(frozen=True)
class PreparedTargetwiseCollection:
    config: TargetwiseRunConfig
    bundle: LoadedCausalFixtureBundle
    paths: TargetwiseCollectionPaths
    tasks: Mapping[str, BinaryTargetTask]


def _encoding_document(config: TargetwiseRunConfig) -> dict[str, str]:
    return {
        "type": config.encoding_type,
        "example_policy": config.example_policy,
        "predictor_policy": config.predictor_policy,
    }


def _task_boundaries(config: TargetwiseRunConfig) -> list[str]:
    if config.predictor_policy == PREDICTOR_POLICY_ORACLE_PARENTS:
        return [
            "the same frozen data table is used for every target",
            "the target column is excluded from learner-visible feature BK",
            (
                "learner-visible feature BK is restricted to the fixture-graph "
                "parents of the target (oracle parent mask)"
            ),
            (
                "graph edges are not serialized as ABA facts; this is a "
                "predictor mask, not Russo-style Causal ABA"
            ),
            "this task is target-wise ABA Learning, not Russo-style Causal ABA",
            "no learned-rule-to-graph decoder is applied",
        ]
    return [
        "the same frozen data table is used for every target",
        "the target column is excluded from learner-visible feature BK",
        "no graph, parent-set, CPDAG, or causal-role metadata is learner-visible",
        "this task is target-wise ABA Learning, not Russo-style Causal ABA",
        "no learned-rule-to-graph decoder is applied",
    ]


def _selected_targets(
    bundle: LoadedCausalFixtureBundle,
    targets: Sequence[str] | None,
) -> tuple[str, ...]:
    if targets is None:
        return bundle.variables
    requested = [target.strip() for target in targets if str(target).strip()]
    if not requested:
        raise ValueError("targets must be a non-empty subset of fixture variables")
    unknown = [target for target in requested if target not in bundle.variables]
    if unknown:
        raise ValueError(
            f"unknown targets {unknown!r}; expected a subset of {bundle.variables!r}"
        )
    wanted = set(requested)
    return tuple(variable for variable in bundle.variables if variable in wanted)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _git_state() -> tuple[str | None, bool | None]:
    try:
        root = Path(__file__).resolve().parents[2]
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        dirty = bool(
            subprocess.check_output(
                ["git", "status", "--porcelain"],
                cwd=root,
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
        )
        return commit, dirty
    except Exception:
        return None, None


def _atomic_json_write(path: Path, document: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(document, indent=2, sort_keys=True) + "\n"
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
        temporary = Path(handle.name)
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _append_log(path: Path, message: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"{_now()} {message}\n")


def _run_id(
    *,
    bundle: LoadedCausalFixtureBundle,
    config: TargetwiseRunConfig,
    target: str,
) -> str:
    payload = (
        f"{bundle.fixture_id}|{config.configuration_id}|"
        f"{config.configuration_hash}|{bundle.sample_name}|{bundle.sample_hash}|"
        f"{target}|{config.config_hash}|{config.prolog_config_hash}"
    )
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:12]


def _task_manifest(
    *,
    bundle: LoadedCausalFixtureBundle,
    config: TargetwiseRunConfig,
    task: BinaryTargetTask,
    examples_hash: str,
    bk_hash: str,
) -> dict[str, Any]:
    parents = [source for source, target in bundle.edges if target == task.target]
    return {
        "task_manifest_schema_version": 5,
        "targetwise_runner_version": TARGETWISE_RUNNER_VERSION,
        "configuration": {
            "id": config.configuration_id,
            "hash": config.configuration_hash,
        },
        "fixture": {
            "id": bundle.fixture_id,
            "directory": str(bundle.fixture_directory),
            "source_hash": bundle.source_hash,
            "document_hash": bundle.document_hash,
            "semantic_hash": bundle.semantic_hash,
            "fixture_manifest_sha256": bundle.fixture_manifest_hash,
        },
        "sample": {
            "name": bundle.sample_name,
            "source_csv": str(bundle.sample_path),
            "source_manifest": str(bundle.sample_manifest_path),
            "n": bundle.n,
            "seed": bundle.seed,
            "csv_sha256": bundle.sample_hash,
            "sample_manifest_sha256": bundle.sample_manifest_hash,
            "target_free_source": True,
        },
        "task": {
            "target": task.target,
            "predictor_order": list(task.predictor_order),
            "predictor_policy": config.predictor_policy,
            "encoding": config.encoding_type,
            "example_policy": config.example_policy,
            "positive_value": 1,
            "negative_value": 0,
            "n_positive": task.n_positive,
            "n_negative": task.n_negative,
            "feature_clause_count": task.feature_clause_count,
        },
        "learner": {
            "prolog_config": str(config.prolog_config),
            "prolog_config_sha256": config.prolog_config_hash,
            "learning_mode": config.learning_mode,
            "prolog_timeout_s": config.prolog_timeout_s,
            "joint_check_timeout_s": config.joint_check_timeout_s,
            "run_config_path": str(config.config_path),
            "run_config_hash": config.config_hash,
        },
        "input_provenance": {
            "frozen_table_copy": "data.csv",
            "data_sha256": bundle.sample_hash,
            "note": (
                "data.csv is retained for inspection and provenance; the ABA "
                "engine does not read it directly"
            ),
        },
        "learner_visible": {
            "files": ["bk.aba", "examples.json"],
            "background_knowledge_sha256": bk_hash,
            "examples_sha256": examples_hash,
            "delivery": {
                "background_knowledge": "consulted by the ABA engine",
                "examples": (
                    "positive_examples and negative_examples arrays passed to "
                    "the ABA engine; examples.json is their frozen record"
                ),
            },
        },
        "evaluator_only": {
            "generating_edges": [list(edge) for edge in bundle.edges],
            "generating_parents_of_target": parents,
            "not_serialized_into_background_knowledge_or_examples": True,
        },
        "output_contract": {
            "solution_aba": "output/bk.sol.aba",
            "solution_asp": "output/bk.sol.asp",
            "solution_check_asp": "output/bk.sol_chk.asp",
            "learned_delta": "output/delta.aba",
            "temporary_execution_stem_exposed": False,
        },
        "boundaries": _task_boundaries(config),
    }


def _base_manifest(
    prepared: PreparedTargetwiseCollection,
    *,
    status: str,
) -> dict[str, Any]:
    config = prepared.config
    bundle = prepared.bundle
    code_commit, code_dirty = _git_state()
    targets: list[dict[str, Any]] = []
    for target, task in prepared.tasks.items():
        cell = prepared.paths.cell(target)
        targets.append(
            {
                "target": target,
                "predictor_order": list(task.predictor_order),
                "n_positive": task.n_positive,
                "n_negative": task.n_negative,
                "cell_directory": str(cell.root),
                "data_sha256": file_sha256(cell.data_path),
                "background_knowledge_sha256": file_sha256(cell.bk_path),
                "examples_sha256": file_sha256(cell.examples_path),
                "task_manifest_sha256": file_sha256(cell.task_manifest_path),
                "outcome": None,
                "failure_reason": None,
                "artifact_check_status": None,
            }
        )
    return {
        "targetwise_manifest_schema_version": 3,
        "targetwise_runner_version": TARGETWISE_RUNNER_VERSION,
        "status": status,
        "fixture": {
            "id": bundle.fixture_id,
            "directory": str(bundle.fixture_directory),
            "semantic_hash": bundle.semantic_hash,
            "fixture_manifest_sha256": bundle.fixture_manifest_hash,
        },
        "sample": {
            "name": bundle.sample_name,
            "source_csv": str(bundle.sample_path),
            "n": bundle.n,
            "seed": bundle.seed,
            "csv_sha256": bundle.sample_hash,
            "sample_manifest_sha256": bundle.sample_manifest_hash,
        },
        "encoding": _encoding_document(config),
        "configuration": {
            "id": config.configuration_id,
            "hash": config.configuration_hash,
            "manifest": str(prepared.paths.configuration_manifest_path),
        },
        "learner": {
            "prolog_config": str(config.prolog_config),
            "prolog_config_sha256": config.prolog_config_hash,
            "learning_mode": config.learning_mode,
            "prolog_timeout_s": config.prolog_timeout_s,
            "joint_check_timeout_s": config.joint_check_timeout_s,
        },
        "run_config": {
            "path": str(config.config_path),
            "hash": config.config_hash,
        },
        "runtime": {
            "python": platform.python_version(),
            "code_commit": code_commit,
            "code_dirty": code_dirty,
        },
        "target_order": list(bundle.variables),
        "targets": targets,
        "started_at": None,
        "finished_at": None,
        "outcome_counts": {},
        "output_directory": str(prepared.paths.root),
        "boundaries": [
            "all target cells use one byte-identical frozen sample",
            "generating graph metadata is evaluator-only",
            "no cross-target graph decoder is run",
        ],
    }


def _guard_existing_manifest(
    path: Path,
    *,
    config: TargetwiseRunConfig,
    bundle: LoadedCausalFixtureBundle,
) -> Mapping[str, Any] | None:
    if not path.is_file():
        return None
    try:
        existing = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ArtifactConflictError(
            f"cannot validate existing target-wise manifest: {path}"
        ) from exc
    if (
        existing.get("run_config", {}).get("hash") != config.config_hash
        or existing.get("configuration", {}).get("id") != config.configuration_id
        or existing.get("configuration", {}).get("hash") != config.configuration_hash
        or existing.get("sample", {}).get("csv_sha256") != bundle.sample_hash
        or existing.get("fixture", {}).get("semantic_hash") != bundle.semantic_hash
        or existing.get("learner", {}).get("prolog_config_sha256")
        != config.prolog_config_hash
    ):
        raise ArtifactConflictError(
            "the fixture/configuration/sample output directory already belongs "
            f"to a different target-wise run configuration: {path.parent}"
        )
    return existing


def _configuration_manifest_document(
    *,
    config: TargetwiseRunConfig,
    bundle: LoadedCausalFixtureBundle,
) -> dict[str, Any]:
    return {
        "targetwise_configuration_manifest_schema_version": 1,
        "targetwise_runner_version": TARGETWISE_RUNNER_VERSION,
        "fixture": {
            "id": bundle.fixture_id,
            "semantic_hash": bundle.semantic_hash,
        },
        "configuration": {
            "id": config.configuration_id,
            "hash": config.configuration_hash,
        },
        "encoding": _encoding_document(config),
        "learner": {
            "prolog_config": str(config.prolog_config),
            "prolog_config_sha256": config.prolog_config_hash,
            "learning_mode": config.learning_mode,
            "prolog_timeout_s": config.prolog_timeout_s,
            "joint_check_timeout_s": config.joint_check_timeout_s,
        },
        "boundary": (
            "This manifest pins the non-sample target-wise execution contract "
            "shared by all sample collections in this configuration directory."
        ),
    }


def _guard_configuration_manifest(
    path: Path,
    *,
    config: TargetwiseRunConfig,
    bundle: LoadedCausalFixtureBundle,
) -> None:
    expected = _configuration_manifest_document(config=config, bundle=bundle)
    if path.is_file():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ArtifactConflictError(
                f"cannot validate target-wise configuration manifest: {path}"
            ) from exc
        if existing != expected:
            raise ArtifactConflictError(
                "configuration directory is already pinned to a different "
                f"target-wise execution contract: {path.parent}"
            )
        return
    write_text_once(
        path,
        json.dumps(expected, indent=2, sort_keys=True) + "\n",
    )


def prepare_collection(
    config: TargetwiseRunConfig,
    *,
    output_root: Path | str | None = None,
) -> PreparedTargetwiseCollection:
    """Write and freeze every target's task inputs and provenance artefacts."""

    bundle = load_causal_fixture_bundle(
        config.fixture_directory,
        config.sample,
    )
    paths = TargetwiseCollectionPaths.for_bundle(
        fixture_id=bundle.fixture_id,
        configuration_id=config.configuration_id,
        sample_name=bundle.sample_name,
        output_root=output_root,
    )
    _guard_configuration_manifest(
        paths.configuration_manifest_path,
        config=config,
        bundle=bundle,
    )
    existing_manifest = _guard_existing_manifest(
        paths.manifest_path,
        config=config,
        bundle=bundle,
    )

    tasks: dict[str, BinaryTargetTask] = {}
    for target in bundle.variables:
        task = build_binary_target_task(
            bundle,
            target,
            predictor_policy=config.predictor_policy,
        )
        tasks[target] = task
        cell = paths.cell(target)
        examples_text = (
            json.dumps(task.examples_document(), indent=2, sort_keys=True) + "\n"
        )
        bk_bytes = task.bk_text.encode("utf-8")
        examples_bytes = examples_text.encode("utf-8")
        task_manifest = _task_manifest(
            bundle=bundle,
            config=config,
            task=task,
            examples_hash=sha256_bytes(examples_bytes),
            bk_hash=sha256_bytes(bk_bytes),
        )
        write_bytes_once(cell.data_path, bundle.sample_bytes)
        write_bytes_once(cell.bk_path, bk_bytes)
        write_bytes_once(cell.examples_path, examples_bytes)
        write_text_once(
            cell.task_manifest_path,
            json.dumps(task_manifest, indent=2, sort_keys=True) + "\n",
        )

    prepared = PreparedTargetwiseCollection(
        config=config,
        bundle=bundle,
        paths=paths,
        tasks=tasks,
    )
    if existing_manifest is None:
        manifest = _base_manifest(prepared, status="prepared")
        _atomic_json_write(paths.manifest_path, manifest)
        _append_log(
            paths.run_log_path,
            f"prepared {len(tasks)} target tasks for "
            f"{bundle.fixture_id}/{bundle.sample_name}",
        )
    return prepared


def _canonical_engine_artifact_name(
    name: str,
    *,
    execution_stem: str,
) -> str | None:
    """Map temporary engine filenames to stable names inside a target cell."""

    if name == f"{execution_stem}.aba":
        return None
    canonical = {
        f"{execution_stem}.bk.sol.aba": "bk.sol.aba",
        f"{execution_stem}.sol.aba": "bk.sol.aba",
        f"{execution_stem}.bk.sol.asp": "bk.sol.asp",
        f"{execution_stem}.sol.asp": "bk.sol.asp",
        f"{execution_stem}.bk.sol_chk.asp": "bk.sol_chk.asp",
        f"{execution_stem}.sol_chk.asp": "bk.sol_chk.asp",
    }
    return canonical.get(name, name)


def _copy_stage_outputs(
    stage: Path,
    output_dir: Path,
    *,
    execution_stem: str,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for source in sorted(stage.rglob("*")):
        if not source.is_file():
            continue
        relative = source.relative_to(stage)
        final_name = _canonical_engine_artifact_name(
            relative.name,
            execution_stem=execution_stem,
        )
        if final_name is None:
            continue
        destination = output_dir / relative.parent / final_name
        write_bytes_once(destination, source.read_bytes())


def _relocate_shared_outputs(
    *,
    execution_stem: str,
    output_dir: Path,
    aba_asp_root: Path | None = None,
) -> None:
    """Move this uniquely named execution's engine artefacts into its cell.

    ABA-ASP can emit solution files under the repository root even when the
    learner is invoked on a cell-local BK file.  The unique execution stem
    makes the ownership of those files unambiguous.  Once ownership is resolved,
    solution artefacts receive stable ``bk.sol*`` names inside the target cell;
    the execution stem is not exposed in the final inspection bundle.
    """

    candidates = (
        f"{execution_stem}.bk.sol.aba",
        f"{execution_stem}.sol.aba",
        f"{execution_stem}.bk.sol.asp",
        f"{execution_stem}.sol.asp",
        f"{execution_stem}.bk.sol_chk.asp",
        f"{execution_stem}.sol_chk.asp",
    )
    if aba_asp_root is None:
        aba_asp_root = Path(__file__).resolve().parents[2]
    for name in candidates:
        source = aba_asp_root / name
        if not source.is_file():
            continue
        final_name = _canonical_engine_artifact_name(
            name,
            execution_stem=execution_stem,
        )
        if final_name is None:
            continue
        destination = output_dir / final_name
        write_bytes_once(destination, source.read_bytes())
        source.unlink()


def _find_solution(output_dir: Path) -> Path | None:
    for name in ("bk.sol.aba", "bk.bk.sol.aba"):
        path = output_dir / name
        if path.is_file():
            return path
    matches = sorted(output_dir.glob("*.sol.aba"))
    return matches[0] if matches else None


def _execute_target(
    prepared: PreparedTargetwiseCollection,
    task: BinaryTargetTask,
    *,
    runner_factory: Callable[[], Any],
    artifact_checker: Callable[..., ArtifactIntegrityCheckResult],
) -> dict[str, Any]:
    config = prepared.config
    bundle = prepared.bundle
    cell = prepared.paths.cell(task.target)
    if cell.metrics_json_path.exists():
        if not cell.metrics_parquet_path.is_file():
            raise ArtifactConflictError(
                "target cell has metrics.json but no metrics.parquet: " f"{cell.root}"
            )
        return json.loads(cell.metrics_json_path.read_text(encoding="utf-8"))
    if cell.output_dir.exists() and any(cell.output_dir.iterdir()):
        raise ArtifactConflictError(
            "target cell has partial outputs but no metrics; refusing to overwrite: "
            f"{cell.output_dir}"
        )
    cell.output_dir.mkdir(parents=True, exist_ok=True)

    stdout = ""
    stderr = ""
    wall_clock_s = 0.0
    timeout = False
    runner_error: str | None = None
    solution_path: Path | None = None
    learned: list[str] = []

    if not task.positive_examples or not task.negative_examples:
        outcome = "skipped"
        failure_reason = "empty E+ or E-"
    else:
        runner = runner_factory()
        started = time.monotonic()
        execution_stem = "targetwise_" + _run_id(
            bundle=bundle, config=config, target=task.target
        )
        with tempfile.TemporaryDirectory(
            dir=cell.root, prefix=".targetwise-run-"
        ) as temporary:
            stage = Path(temporary)
            stage_bk = stage / f"{execution_stem}.aba"
            stage_bk.write_bytes(cell.bk_path.read_bytes())
            try:
                result = runner.run_prolog_aba_asp(
                    stage_bk,
                    positive_examples=list(task.positive_examples),
                    negative_examples=list(task.negative_examples),
                    learning_options=None,
                    timeout_s=config.prolog_timeout_s,
                    prolog_config=config.prolog_config,
                )
                stdout = str(result.get("stdout", "") or "")
                stderr = str(result.get("stderr", "") or "")
                if result.get("status") != "completed":
                    runner_error = str(
                        result.get(
                            "error",
                            f"ABA runner status={result.get('status')!r}",
                        )
                    )
            except TimeoutError as exc:
                timeout = True
                runner_error = str(exc)
                stderr = str(exc)
            except Exception as exc:
                runner_error = repr(exc)
                stderr = repr(exc)
            finally:
                wall_clock_s = time.monotonic() - started
                _copy_stage_outputs(
                    stage,
                    cell.output_dir,
                    execution_stem=execution_stem,
                )
                _relocate_shared_outputs(
                    execution_stem=execution_stem,
                    output_dir=cell.output_dir,
                )

        solution_path = _find_solution(cell.output_dir)
        learned = (
            parse_delta_rules(solution_path, bk_path=cell.bk_path)
            if solution_path is not None
            else []
        )
        if solution_path is not None:
            delta_text = "\n".join(learned)
            if delta_text:
                delta_text += "\n"
            write_text_once(cell.delta_path, delta_text)
        if timeout:
            outcome = "timeout"
            failure_reason = runner_error
        elif runner_error is not None:
            outcome = "error"
            failure_reason = runner_error
        else:
            outcome, failure_reason = outcome_classifier(
                stdout=stdout,
                sol_path=solution_path,
                learned_rules=learned,
                wall_clock_s=wall_clock_s,
                timeout_s=config.prolog_timeout_s,
                examples_ok=True,
            )

    write_text_once(cell.output_dir / "prolog.stdout", stdout)
    write_text_once(cell.output_dir / "prolog.stderr", stderr)
    solution_asp_path = resolve_solution_asp_path(solution_path, cell.output_dir)
    solution_check_asp_path = resolve_solution_check_asp_path(
        solution_path,
        cell.output_dir,
    )
    if outcome in {"solved", "completed_empty_delta"}:
        artifact_check = artifact_checker(
            solution_check_asp_path,
            timeout_s=config.joint_check_timeout_s,
        )
    else:
        artifact_check = unavailable_artifact_integrity_check(
            f"learner outcome {outcome!r} has no completed framework to check"
        )

    run_id = _run_id(bundle=bundle, config=config, target=task.target)
    panel = build_targetwise_diagnostics(
        experiment_id=(
            f"targetwise:{bundle.fixture_id}:{config.configuration_id}:"
            f"{bundle.sample_name}"
        ),
        fixture_id=bundle.fixture_id,
        configuration_id=config.configuration_id,
        configuration_hash=config.configuration_hash,
        sample_name=bundle.sample_name,
        target=task.target,
        variable_names=bundle.variables,
        n=bundle.n,
        seed=bundle.seed,
        config_hash=config.config_hash,
        prolog_config_hash=config.prolog_config_hash,
        run_id=run_id,
        outcome=outcome,
        failure_reason=failure_reason,
        aba_learning_runtime_s=wall_clock_s,
        solution_path=solution_path,
        solution_asp_path=solution_asp_path,
        solution_check_asp_path=solution_check_asp_path,
        delta_path=cell.delta_path if cell.delta_path.is_file() else None,
        learned_rules=learned,
        artifact_integrity_check=artifact_check,
        provenance={
            "fixture_semantic_hash": bundle.semantic_hash,
            "sample_csv_sha256": bundle.sample_hash,
            "task_manifest_sha256": file_sha256(cell.task_manifest_path),
            "predictor_order": list(task.predictor_order),
            "predictor_policy": config.predictor_policy,
            "encoding": config.encoding_type,
            "example_policy": config.example_policy,
            "learning_mode": config.learning_mode,
        },
    )
    write_targetwise_metrics(cell.root, panel)
    return panel


def run_collection(
    config: TargetwiseRunConfig,
    *,
    output_root: Path | str | None = None,
    targets: Sequence[str] | None = None,
    runner_factory: Callable[[], Any] = ABASPRunner,
    artifact_checker: Callable[
        ..., ArtifactIntegrityCheckResult
    ] = final_artifact_integrity_check,
) -> PreparedTargetwiseCollection:
    """Prepare and serially run ABA Learning for selected fixture variables."""

    prepared = prepare_collection(config, output_root=output_root)
    selected = _selected_targets(prepared.bundle, targets)
    existing = _guard_existing_manifest(
        prepared.paths.manifest_path,
        config=config,
        bundle=prepared.bundle,
    )
    manifest = dict(existing or _base_manifest(prepared, status="prepared"))
    if manifest.get("status") == "completed":
        required = (
            prepared.paths.results_path,
            prepared.paths.summary_markdown_path,
            prepared.paths.summary_json_path,
        )
        if all(path.is_file() for path in required) and all(
            prepared.paths.cell(target).metrics_json_path.is_file()
            and prepared.paths.cell(target).metrics_parquet_path.is_file()
            and prepared.paths.cell(target).report_path.is_file()
            for target in prepared.bundle.variables
        ):
            return prepared
        raise ArtifactConflictError(
            "completed target-wise manifest has missing result artefacts: "
            f"{prepared.paths.root}"
        )
    if manifest.get("started_at") is None:
        manifest["started_at"] = _now()
    manifest["status"] = "running"
    _atomic_json_write(prepared.paths.manifest_path, manifest)
    _append_log(
        prepared.paths.run_log_path,
        (
            f"starting target-wise run with {len(selected)} of "
            f"{len(prepared.tasks)} targets"
        ),
    )

    target_entries = {
        str(entry["target"]): dict(entry) for entry in manifest.get("targets", [])
    }
    if set(target_entries) != set(prepared.bundle.variables):
        raise ArtifactConflictError(
            "target-wise manifest target set does not match the fixture variables"
        )
    for target in selected:
        task = prepared.tasks[target]
        cell = prepared.paths.cell(target)
        _append_log(prepared.paths.run_log_path, f"start target={target}")
        metrics = _execute_target(
            prepared,
            task,
            runner_factory=runner_factory,
            artifact_checker=artifact_checker,
        )
        write_target_report(
            bundle=prepared.bundle,
            config=config,
            task=task,
            cell_paths=cell,
            metrics=metrics,
        )
        outcome = str(metrics.get("outcome", "error"))
        entry = target_entries[target]
        entry["outcome"] = outcome
        entry["failure_reason"] = metrics.get("failure_reason")
        entry["artifact_check_status"] = metrics.get("artifact_check_status")
        outcome_counts = Counter(
            str(item["outcome"])
            for item in target_entries.values()
            if item.get("outcome") is not None
        )
        manifest["targets"] = [
            target_entries[item] for item in prepared.bundle.variables
        ]
        manifest["outcome_counts"] = dict(outcome_counts)
        _atomic_json_write(prepared.paths.manifest_path, manifest)
        _append_log(
            prepared.paths.run_log_path,
            f"finish target={target} outcome={outcome}",
        )

    all_complete = all(
        prepared.paths.cell(target).metrics_json_path.is_file()
        and prepared.paths.cell(target).metrics_parquet_path.is_file()
        and prepared.paths.cell(target).report_path.is_file()
        for target in prepared.bundle.variables
    )
    outcome_counts = Counter(
        str(item["outcome"])
        for item in target_entries.values()
        if item.get("outcome") is not None
    )
    manifest["targets"] = [
        target_entries[target] for target in prepared.bundle.variables
    ]
    manifest["outcome_counts"] = dict(outcome_counts)
    if not all_complete:
        manifest["status"] = "partial"
        _atomic_json_write(prepared.paths.manifest_path, manifest)
        _append_log(
            prepared.paths.run_log_path,
            f"partial outcomes={dict(outcome_counts)}",
        )
        return prepared

    cell_summaries = []
    for target in prepared.bundle.variables:
        cell = prepared.paths.cell(target)
        metrics = json.loads(cell.metrics_json_path.read_text(encoding="utf-8"))
        cell_summaries.append(
            write_target_report(
                bundle=prepared.bundle,
                config=config,
                task=prepared.tasks[target],
                cell_paths=cell,
                metrics=metrics,
            )
        )
    write_targetwise_results(prepared.paths.root)
    write_collection_summary(
        bundle=prepared.bundle,
        config=config,
        paths=prepared.paths,
        cells=cell_summaries,
    )
    manifest["status"] = "completed"
    manifest["finished_at"] = _now()
    _atomic_json_write(prepared.paths.manifest_path, manifest)
    _append_log(
        prepared.paths.run_log_path,
        f"completed outcomes={dict(outcome_counts)}",
    )
    return prepared


def validate_collection_config(
    config: TargetwiseRunConfig,
) -> LoadedCausalFixtureBundle:
    """Validate the complete input contract without writing outputs."""

    bundle = load_causal_fixture_bundle(
        config.fixture_directory,
        config.sample,
    )
    for target in bundle.variables:
        build_binary_target_task(
            bundle,
            target,
            predictor_policy=config.predictor_policy,
        )
    return bundle
