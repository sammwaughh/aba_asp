"""Tests for target-complete ABA Learning over frozen causal-fixture samples."""

from __future__ import annotations

import json
from pathlib import Path
import re
import shutil
import subprocess
from typing import Any

import pandas as pd
import pytest

from causal.experiments.paths import repo_root
from causal.fixtures.artifacts import (
    ArtifactConflictError,
    file_sha256,
)
from causal.targetwise.bundle import (
    CausalFixtureBundleError,
    load_causal_fixture_bundle,
)
from causal.targetwise.cli import main as targetwise_main
from causal.targetwise.collection import (
    _relocate_shared_outputs,
    prepare_collection,
    run_collection,
    validate_collection_config,
)
from causal.targetwise.config import (
    TargetwiseConfigError,
    load_targetwise_config,
)
from causal.targetwise.diagnostics import TARGETWISE_RESULT_COLUMNS
from causal.targetwise.encoding import (
    TargetwiseEncodingError,
    build_binary_target_task,
)
from causal.targetwise.paths import TargetwiseCollectionPaths
from causal.targetwise.semantics import (
    ArtifactIntegrityCheckResult,
    final_artifact_integrity_check,
    resolve_solution_check_asp_path,
)


_VARIABLES = ("x0", "x1", "x2", "x3")
_EDGES = (
    ("x0", "x1"),
    ("x0", "x2"),
    ("x1", "x3"),
    ("x2", "x3"),
)
_SAMPLE_ROWS = (
    (0, 0, 0, 0),
    (0, 0, 1, 1),
    (0, 1, 0, 1),
    (0, 1, 1, 0),
    (1, 0, 0, 1),
    (1, 0, 1, 0),
    (1, 1, 0, 0),
    (1, 1, 1, 1),
)


def _write_json(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_fixture_bundle(tmp_path: Path) -> Path:
    fixture_id = "test_binary_diamond"
    fixture_directory = tmp_path / fixture_id
    sample_path = fixture_directory / "samples" / "n8_seed42.csv"
    sample_path.parent.mkdir(parents=True)
    lines = [",".join(_VARIABLES)]
    lines.extend(",".join(str(value) for value in row) for row in _SAMPLE_ROWS)
    sample_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    fixture_manifest = {
        "fixture_manifest_schema_version": 1,
        "fixture": {
            "id": fixture_id,
            "variables": list(_VARIABLES),
            "edges": [list(edge) for edge in _EDGES],
            "source_hash": "sha256:test-source",
            "document_hash": "sha256:test-document",
            "semantic_hash": "sha256:test-semantic",
        },
    }
    _write_json(
        fixture_directory / "fixture_manifest.json",
        fixture_manifest,
    )
    sample_manifest = {
        "sample_manifest_schema_version": 1,
        "fixture": {
            "id": fixture_id,
            "source_hash": "sha256:test-source",
            "document_hash": "sha256:test-document",
            "semantic_hash": "sha256:test-semantic",
        },
        "sample": {
            "n": len(_SAMPLE_ROWS),
            "seed": 42,
            "target": None,
            "iid_observational_rows": True,
            "csv_columns_are_causal_variables_only": True,
            "csv_sha256": file_sha256(sample_path),
        },
        "sampler": {
            "output_column_order": list(_VARIABLES),
            "state_orders": {variable: [0, 1] for variable in _VARIABLES},
        },
    }
    _write_json(sample_path.with_suffix(".manifest.json"), sample_manifest)
    return fixture_directory


def _write_config(
    tmp_path: Path,
    fixture_directory: Path,
    *,
    description: str = "test target-complete collection",
    configuration_id: str = "aamas2025",
    encoding_type: str = "exact_value",
    sample: str = "samples/n8_seed42.csv",
    prolog_config: Path | None = None,
) -> Path:
    config_path = tmp_path / f"targetwise-{len(list(tmp_path.glob('*.yaml')))}.yaml"
    if prolog_config is None:
        prolog_config = repo_root() / "configs" / "aamas2025_config.pl"
    config_path.write_text(
        f"""\
description: "{description}"
configuration:
  id: "{configuration_id}"
fixture:
  directory: "{fixture_directory}"
  sample: "{sample}"
encoding:
  type: "{encoding_type}"
  example_policy: binary_one_vs_zero
learner:
  prolog_config: "{prolog_config}"
  prolog_timeout_s: 30
  joint_check_timeout_s: 1
""",
        encoding="utf-8",
    )
    return config_path


class _FakeRunner:
    """Write one deterministic learned rule while exercising runner staging."""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def run_prolog_aba_asp(
        self,
        predicate_file: Path,
        positive_examples: list[str],
        negative_examples: list[str],
        learning_options: None,
        timeout_s: float,
        prolog_config: Path,
    ) -> dict[str, Any]:
        target = positive_examples[0].split("(", 1)[0]
        text = predicate_file.read_text(encoding="utf-8")
        feature_by_row: dict[int, list[str]] = {}
        for predicate, row in re.findall(
            r"^([a-z][A-Za-z0-9_]*_val_[01])\(A\) :- A=(\d+)\.$",
            text,
            re.M,
        ):
            feature_by_row.setdefault(int(row), []).append(f"{predicate}(A)")
        learned_rules = []
        for atom in positive_examples:
            row = int(atom.split("(", 1)[1].rstrip(")"))
            learned_rules.append(f"{target}(A) :- {', '.join(feature_by_row[row])}.")
        solution = predicate_file.with_name(f"{predicate_file.stem}.sol.aba")
        solution.write_text(
            text + "\n".join(learned_rules) + "\n",
            encoding="utf-8",
        )
        solution_asp = predicate_file.with_name(f"{predicate_file.stem}.sol.asp")
        solution_asp.write_text(
            text + "\n".join(learned_rules) + "\n",
            encoding="utf-8",
        )
        solution_check_asp = predicate_file.with_name(
            f"{predicate_file.stem}.sol_chk.asp"
        )
        solution_check_asp.write_text(
            text
            + "\n".join(learned_rules)
            + "\n"
            + "\n".join(f":- not {atom}." for atom in positive_examples)
            + "\n"
            + "\n".join(f":- {atom}." for atom in negative_examples)
            + "\n",
            encoding="utf-8",
        )
        self.calls.append(
            {
                "target": target,
                "predicate_file": predicate_file,
                "positive_examples": tuple(positive_examples),
                "negative_examples": tuple(negative_examples),
                "learning_options": learning_options,
                "timeout_s": timeout_s,
                "prolog_config": prolog_config,
            }
        )
        return {
            "status": "completed",
            "stdout": "Increasing folding tokens to: 3\n",
            "stderr": "",
        }


class _FakeArtifactChecker:
    def __init__(self, status: str = "SAT") -> None:
        self.status = status
        self.calls: list[dict[str, Any]] = []

    def __call__(
        self,
        solution_check_asp_path: Path | None,
        *,
        timeout_s: float,
    ) -> ArtifactIntegrityCheckResult:
        assert (
            solution_check_asp_path is not None
            and solution_check_asp_path.is_file()
            and solution_check_asp_path.name.endswith(".sol_chk.asp")
        )
        self.calls.append(
            {
                "solution_check_asp_path": solution_check_asp_path,
                "timeout_s": timeout_s,
            }
        )
        return ArtifactIntegrityCheckResult(
            status=self.status,
            runtime_s=0.001,
            failure_reason=None,
            checked_asp_path=str(solution_check_asp_path),
            clingo_path="/test/clingo",
            returncode=10 if self.status == "SAT" else 20,
        )


def test_config_loader_is_strict_and_resolves_paths(tmp_path: Path) -> None:
    fixture_directory = _write_fixture_bundle(tmp_path)
    config_path = _write_config(tmp_path, fixture_directory)

    config = load_targetwise_config(config_path)

    assert config.fixture_directory == fixture_directory.resolve()
    assert config.configuration_id == "aamas2025"
    assert config.configuration_hash.startswith("sha256:")
    assert config.sample == Path("samples/n8_seed42.csv")
    assert config.encoding_type == "exact_value"
    assert config.example_policy == "binary_one_vs_zero"
    assert config.prolog_timeout_s == 30.0
    assert config.learning_mode == "brave"
    assert config.joint_check_timeout_s == 1.0
    assert config.config_hash.startswith("sha256:")
    assert config.prolog_config_hash == file_sha256(config.prolog_config)

    bad_path = _write_config(
        tmp_path,
        fixture_directory,
        encoding_type="one_hot",
    )
    with pytest.raises(TargetwiseConfigError, match="exact_value"):
        load_targetwise_config(bad_path)


def test_config_rejects_unsafe_configuration_identifier(tmp_path: Path) -> None:
    fixture_directory = _write_fixture_bundle(tmp_path)
    config_path = _write_config(
        tmp_path,
        fixture_directory,
        configuration_id="../ecai2024",
    )

    with pytest.raises(TargetwiseConfigError, match="configuration.id"):
        load_targetwise_config(config_path)


def test_configuration_hash_is_stable_across_selected_samples(
    tmp_path: Path,
) -> None:
    fixture_directory = _write_fixture_bundle(tmp_path)
    first = load_targetwise_config(
        _write_config(
            tmp_path,
            fixture_directory,
            sample="samples/n8_seed42.csv",
        )
    )
    second = load_targetwise_config(
        _write_config(
            tmp_path,
            fixture_directory,
            sample="samples/n16_seed42.csv",
        )
    )

    assert first.configuration_hash == second.configuration_hash
    assert first.config_hash != second.config_hash


def test_config_rejects_non_brave_learning_mode(tmp_path: Path) -> None:
    fixture_directory = _write_fixture_bundle(tmp_path)
    cautious_config = tmp_path / "cautious.pl"
    cautious_config.write_text(
        ":- set_lopt(learning_mode(cautious)).\n",
        encoding="utf-8",
    )
    config_path = _write_config(
        tmp_path,
        fixture_directory,
        prolog_config=cautious_config,
    )

    with pytest.raises(TargetwiseConfigError, match="supports brave"):
        load_targetwise_config(config_path)


def test_config_requires_engine_checked_solution_artefact(tmp_path: Path) -> None:
    fixture_directory = _write_fixture_bundle(tmp_path)
    unchecked_config = tmp_path / "unchecked.pl"
    unchecked_config.write_text(
        ":- set_lopt(learning_mode(brave)).\n",
        encoding="utf-8",
    )
    config_path = _write_config(
        tmp_path,
        fixture_directory,
        prolog_config=unchecked_config,
    )

    with pytest.raises(TargetwiseConfigError, match=r"set_lopt\(check_ic\)"):
        load_targetwise_config(config_path)


def test_config_rejects_absolute_or_escaping_sample_paths(
    tmp_path: Path,
) -> None:
    fixture_directory = _write_fixture_bundle(tmp_path)
    absolute = _write_config(
        tmp_path,
        fixture_directory,
        sample=str(fixture_directory / "samples" / "n8_seed42.csv"),
    )
    with pytest.raises(TargetwiseConfigError, match="must be relative"):
        load_targetwise_config(absolute)

    escaping = _write_config(
        tmp_path,
        fixture_directory,
        sample="../outside.csv",
    )
    config = load_targetwise_config(escaping)
    with pytest.raises(CausalFixtureBundleError, match="inside"):
        validate_collection_config(config)


def test_bundle_loader_validates_frozen_sample_contract(
    tmp_path: Path,
) -> None:
    fixture_directory = _write_fixture_bundle(tmp_path)

    bundle = load_causal_fixture_bundle(
        fixture_directory,
        Path("samples/n8_seed42.csv"),
    )

    assert bundle.fixture_id == "test_binary_diamond"
    assert bundle.variables == _VARIABLES
    assert bundle.edges == _EDGES
    assert bundle.n == 8
    assert bundle.seed == 42
    assert bundle.sample_name == "n8_seed42"
    assert bundle.sample_hash == file_sha256(bundle.sample_path)
    assert list(bundle.dataframe.columns) == list(_VARIABLES)


def test_bundle_loader_rejects_hash_drift_and_missing_values(
    tmp_path: Path,
) -> None:
    fixture_directory = _write_fixture_bundle(tmp_path)
    sample_path = fixture_directory / "samples" / "n8_seed42.csv"
    sample_path.write_text(
        sample_path.read_text(encoding="utf-8") + "0,0,0,0\n",
        encoding="utf-8",
    )
    with pytest.raises(CausalFixtureBundleError, match="hash"):
        load_causal_fixture_bundle(
            fixture_directory,
            Path("samples/n8_seed42.csv"),
        )

    fixture_directory = _write_fixture_bundle(tmp_path / "missing")
    sample_path = fixture_directory / "samples" / "n8_seed42.csv"
    sample_text = sample_path.read_text(encoding="utf-8").replace(
        "0,0,0,0\n",
        "0,,0,0\n",
        1,
    )
    sample_path.write_text(sample_text, encoding="utf-8")
    manifest_path = sample_path.with_suffix(".manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["sample"]["csv_sha256"] = file_sha256(sample_path)
    _write_json(manifest_path, manifest)
    with pytest.raises(CausalFixtureBundleError, match="missing"):
        load_causal_fixture_bundle(
            fixture_directory,
            Path("samples/n8_seed42.csv"),
        )


def test_bundle_loader_rejects_unsupported_manifest_schema(
    tmp_path: Path,
) -> None:
    fixture_directory = _write_fixture_bundle(tmp_path)
    fixture_manifest_path = fixture_directory / "fixture_manifest.json"
    fixture_manifest = json.loads(fixture_manifest_path.read_text(encoding="utf-8"))
    fixture_manifest["fixture_manifest_schema_version"] = 2
    _write_json(fixture_manifest_path, fixture_manifest)

    with pytest.raises(CausalFixtureBundleError, match="supported version 1"):
        load_causal_fixture_bundle(
            fixture_directory,
            Path("samples/n8_seed42.csv"),
        )


def test_exact_value_encoder_builds_symmetric_target_task(
    tmp_path: Path,
) -> None:
    fixture_directory = _write_fixture_bundle(tmp_path)
    bundle = load_causal_fixture_bundle(
        fixture_directory,
        Path("samples/n8_seed42.csv"),
    )

    task = build_binary_target_task(bundle, "x0")

    assert task.predictor_order == ("x1", "x2", "x3")
    assert task.positive_examples == (
        "x0(5)",
        "x0(6)",
        "x0(7)",
        "x0(8)",
    )
    assert task.negative_examples == (
        "x0(1)",
        "x0(2)",
        "x0(3)",
        "x0(4)",
    )
    assert task.feature_clause_count == 8 * 3
    assert "x0_val_0" not in task.bk_text
    assert "x0_val_1" not in task.bk_text
    assert "x1_val_0(A) :- A=1." in task.bk_text
    assert "x1_val_1(A) :- A=3." in task.bk_text
    assert bundle.fixture_id not in task.bk_text
    assert bundle.sample_name not in task.bk_text
    clauses = "\n".join(
        line for line in task.bk_text.splitlines() if line and not line.startswith("%")
    ).lower()
    assert "parent" not in clauses
    assert "edge" not in clauses


def test_exact_value_encoder_rejects_nonbinary_state_orders(
    tmp_path: Path,
) -> None:
    fixture_directory = _write_fixture_bundle(tmp_path)
    manifest_path = fixture_directory / "samples" / "n8_seed42.manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["sampler"]["state_orders"]["x3"] = [0, 1, 2]
    _write_json(manifest_path, manifest)
    bundle = load_causal_fixture_bundle(
        fixture_directory,
        Path("samples/n8_seed42.csv"),
    )

    with pytest.raises(TargetwiseEncodingError, match=r"\[0, 1\]"):
        build_binary_target_task(bundle, "x3")


def test_exact_value_encoder_rejects_names_outside_initial_predicate_contract(
    tmp_path: Path,
) -> None:
    fixture_directory = _write_fixture_bundle(tmp_path)
    fixture_manifest_path = fixture_directory / "fixture_manifest.json"
    fixture_manifest = json.loads(fixture_manifest_path.read_text(encoding="utf-8"))
    fixture_manifest["fixture"]["variables"][0] = "a"
    fixture_manifest["fixture"]["edges"] = [
        ["a" if node == "x0" else node for node in edge]
        for edge in fixture_manifest["fixture"]["edges"]
    ]
    _write_json(fixture_manifest_path, fixture_manifest)

    sample_path = fixture_directory / "samples" / "n8_seed42.csv"
    sample_path.write_text(
        sample_path.read_text(encoding="utf-8").replace(
            "x0,x1,x2,x3",
            "a,x1,x2,x3",
            1,
        ),
        encoding="utf-8",
    )
    sample_manifest_path = sample_path.with_suffix(".manifest.json")
    sample_manifest = json.loads(sample_manifest_path.read_text(encoding="utf-8"))
    sample_manifest["sample"]["csv_sha256"] = file_sha256(sample_path)
    sample_manifest["sampler"]["output_column_order"][0] = "a"
    sample_manifest["sampler"]["state_orders"]["a"] = sample_manifest["sampler"][
        "state_orders"
    ].pop("x0")
    _write_json(sample_manifest_path, sample_manifest)
    bundle = load_causal_fixture_bundle(
        fixture_directory,
        Path("samples/n8_seed42.csv"),
    )

    with pytest.raises(TargetwiseEncodingError, match="form xN"):
        build_binary_target_task(bundle, "a")


def test_targetwise_paths_match_fixture_configuration_sample_target_hierarchy(
    tmp_path: Path,
) -> None:
    paths = TargetwiseCollectionPaths.for_bundle(
        fixture_id="m13_bucket3_binary_diamond",
        configuration_id="aamas2025",
        sample_name="n50_seed42",
        output_root=tmp_path,
    )

    assert paths.root == (
        tmp_path / "m13_bucket3_binary_diamond" / "aamas2025" / "n50_seed42"
    )
    assert paths.configuration_root == (
        tmp_path / "m13_bucket3_binary_diamond" / "aamas2025"
    )
    assert paths.configuration_manifest_path == (
        paths.configuration_root / "configuration_manifest.json"
    )
    assert paths.cell("x2").data_path == (
        paths.root / "cells" / "target-x2" / "input" / "data.csv"
    )
    assert paths.cell("x2").output_dir == (
        paths.root / "cells" / "target-x2" / "output"
    )

    with pytest.raises(ValueError, match="unsafe"):
        paths.cell("../escape")


def test_shared_engine_outputs_are_relocated_into_the_target_cell(
    tmp_path: Path,
) -> None:
    engine_root = tmp_path / "engine"
    output_dir = tmp_path / "cell" / "output"
    engine_root.mkdir()
    shared_solution = engine_root / "targetwise_test.sol.aba"
    shared_asp = engine_root / "targetwise_test.sol.asp"
    shared_solution.write_text("x0(A) :- x1_val_1(A).\n", encoding="utf-8")
    shared_asp.write_text("x0(1).\n", encoding="utf-8")

    _relocate_shared_outputs(
        execution_stem="targetwise_test",
        output_dir=output_dir,
        aba_asp_root=engine_root,
    )

    assert not shared_solution.exists()
    assert not shared_asp.exists()
    assert (output_dir / "targetwise_test.sol.aba").read_text(
        encoding="utf-8"
    ) == "x0(A) :- x1_val_1(A).\n"
    assert (output_dir / "targetwise_test.sol.asp").read_text(
        encoding="utf-8"
    ) == "x0(1).\n"


def test_prepare_writes_all_targets_without_running_learner(
    tmp_path: Path,
) -> None:
    fixture_directory = _write_fixture_bundle(tmp_path / "source")
    config = load_targetwise_config(_write_config(tmp_path, fixture_directory))
    output_root = tmp_path / "outputs"

    prepared = prepare_collection(config, output_root=output_root)

    assert tuple(prepared.tasks) == _VARIABLES
    copied_hashes = {
        file_sha256(prepared.paths.cell(target).data_path) for target in _VARIABLES
    }
    assert copied_hashes == {prepared.bundle.sample_hash}
    for target in _VARIABLES:
        cell = prepared.paths.cell(target)
        assert cell.bk_path.is_file()
        assert cell.examples_path.is_file()
        assert cell.task_manifest_path.is_file()
        assert not cell.output_dir.exists()
        task_manifest = json.loads(cell.task_manifest_path.read_text(encoding="utf-8"))
        assert task_manifest["task"]["target"] == target
        assert task_manifest["evaluator_only"][
            "not_serialized_into_background_knowledge_or_examples"
        ]
    manifest = json.loads(prepared.paths.manifest_path.read_text(encoding="utf-8"))
    assert manifest["status"] == "prepared"
    assert manifest["configuration"]["id"] == "aamas2025"
    assert manifest["configuration"]["hash"] == config.configuration_hash
    assert manifest["target_order"] == list(_VARIABLES)
    configuration_manifest = json.loads(
        prepared.paths.configuration_manifest_path.read_text(encoding="utf-8")
    )
    assert configuration_manifest["configuration"] == {
        "id": "aamas2025",
        "hash": config.configuration_hash,
    }
    assert configuration_manifest["fixture"]["id"] == "test_binary_diamond"


def test_configuration_ids_create_separate_sample_collections(
    tmp_path: Path,
) -> None:
    fixture_directory = _write_fixture_bundle(tmp_path / "source")
    aamas = load_targetwise_config(
        _write_config(
            tmp_path,
            fixture_directory,
            configuration_id="aamas2025",
        )
    )
    ecai = load_targetwise_config(
        _write_config(
            tmp_path,
            fixture_directory,
            configuration_id="ecai2024",
        )
    )

    aamas_prepared = prepare_collection(aamas, output_root=tmp_path / "outputs")
    ecai_prepared = prepare_collection(ecai, output_root=tmp_path / "outputs")

    assert aamas_prepared.paths.root != ecai_prepared.paths.root
    assert aamas_prepared.paths.root.parts[-3:] == (
        "test_binary_diamond",
        "aamas2025",
        "n8_seed42",
    )
    assert ecai_prepared.paths.root.parts[-3:] == (
        "test_binary_diamond",
        "ecai2024",
        "n8_seed42",
    )
    assert aamas.configuration_hash != ecai.configuration_hash


def test_prepare_refuses_to_overwrite_changed_frozen_input(
    tmp_path: Path,
) -> None:
    fixture_directory = _write_fixture_bundle(tmp_path / "source")
    config = load_targetwise_config(_write_config(tmp_path, fixture_directory))
    prepared = prepare_collection(config, output_root=tmp_path / "outputs")
    prepared.paths.cell("x0").bk_path.write_text(
        "% changed\n",
        encoding="utf-8",
    )

    with pytest.raises(ArtifactConflictError, match="non-identical"):
        prepare_collection(config, output_root=tmp_path / "outputs")


def test_output_directory_rejects_a_different_run_configuration(
    tmp_path: Path,
) -> None:
    fixture_directory = _write_fixture_bundle(tmp_path / "source")
    first = load_targetwise_config(
        _write_config(tmp_path, fixture_directory, description="first")
    )
    second = load_targetwise_config(
        _write_config(tmp_path, fixture_directory, description="second")
    )
    assert first.configuration_hash == second.configuration_hash
    assert first.config_hash != second.config_hash
    prepare_collection(first, output_root=tmp_path / "outputs")

    with pytest.raises(ArtifactConflictError, match="different"):
        prepare_collection(second, output_root=tmp_path / "outputs")


def test_output_directory_rejects_changed_prolog_configuration_bytes(
    tmp_path: Path,
) -> None:
    fixture_directory = _write_fixture_bundle(tmp_path / "source")
    prolog_config = tmp_path / "learner.pl"
    prolog_config.write_text(
        ":- set_lopt(learning_mode(brave)).\n"
        ":- set_lopt(folding_mode(greedy)).\n"
        ":- set_lopt(check_ic).\n",
        encoding="utf-8",
    )
    config_path = _write_config(
        tmp_path,
        fixture_directory,
        prolog_config=prolog_config,
    )
    first = load_targetwise_config(config_path)
    prepare_collection(first, output_root=tmp_path / "outputs")
    prolog_config.write_text(
        ":- set_lopt(learning_mode(brave)).\n"
        ":- set_lopt(folding_mode(nd)).\n"
        ":- set_lopt(check_ic).\n",
        encoding="utf-8",
    )
    changed = load_targetwise_config(config_path)

    assert first.config_hash == changed.config_hash
    assert first.prolog_config_hash != changed.prolog_config_hash
    assert first.configuration_hash != changed.configuration_hash
    with pytest.raises(ArtifactConflictError, match="different"):
        prepare_collection(changed, output_root=tmp_path / "outputs")


def test_fake_runner_executes_all_targets_and_writes_inspection_bundle(
    tmp_path: Path,
) -> None:
    pytest.importorskip("pyarrow")
    fixture_directory = _write_fixture_bundle(tmp_path / "source")
    config = load_targetwise_config(_write_config(tmp_path, fixture_directory))
    fake = _FakeRunner()
    fake_artifact = _FakeArtifactChecker()

    prepared = run_collection(
        config,
        output_root=tmp_path / "outputs",
        runner_factory=lambda: fake,
        artifact_checker=fake_artifact,
    )

    assert [call["target"] for call in fake.calls] == list(_VARIABLES)
    assert len(fake_artifact.calls) == 4
    manifest = json.loads(prepared.paths.manifest_path.read_text(encoding="utf-8"))
    assert manifest["status"] == "completed"
    assert manifest["outcome_counts"] == {"solved": 4}
    assert prepared.paths.results_path.is_file()
    results = pd.read_parquet(prepared.paths.results_path)
    assert len(results) == 4
    assert tuple(results.columns) == TARGETWISE_RESULT_COLUMNS
    assert set(results["target"]) == set(_VARIABLES)
    assert set(results["configuration_id"]) == {"aamas2025"}
    assert set(results["configuration_hash"]) == {config.configuration_hash}
    assert set(results["n_target_rules"]) == {4}
    assert set(results["artifact_check_status"]) == {"SAT"}
    assert not any("parent" in column for column in results.columns)
    assert not any(column.startswith("cov_") for column in results.columns)
    summary = json.loads(prepared.paths.summary_json_path.read_text(encoding="utf-8"))
    assert len(summary["targets"]) == 4
    assert "No per-example coverage panel" in summary["boundary"]

    for target in _VARIABLES:
        cell = prepared.paths.cell(target)
        output_files = {path.name for path in cell.output_dir.iterdir()}
        assert any(name.endswith(".sol.aba") for name in output_files)
        assert any(
            name.startswith("targetwise_")
            and name.endswith(".aba")
            and not name.endswith(".sol.aba")
            for name in output_files
        )
        assert {"prolog.stdout", "prolog.stderr"} <= output_files
        metrics = json.loads(cell.metrics_json_path.read_text(encoding="utf-8"))
        assert metrics["outcome"] == "solved"
        assert metrics["n_target_rules"] == 4
        assert metrics["artifact_check_status"] == "SAT"
        assert metrics["solution_check_asp_path"].endswith(".sol_chk.asp")
        assert metrics["body_lengths"] == [3, 3, 3, 3]
        assert "cov_asp_pos" not in metrics
        assert "body_parent_precision" not in metrics
        report = cell.report_path.read_text(encoding="utf-8")
        assert f"# Target-wise cell: {target}" in report
        assert "Final-artefact integrity audit" in report
        assert "Generating parents" not in report

    original_calls = len(fake.calls)
    run_collection(
        config,
        output_root=tmp_path / "outputs",
        runner_factory=lambda: fake,
        artifact_checker=fake_artifact,
    )
    assert len(fake.calls) == original_calls


def test_constant_sample_target_is_recorded_as_skipped(
    tmp_path: Path,
) -> None:
    pytest.importorskip("pyarrow")
    fixture_directory = _write_fixture_bundle(tmp_path / "source")
    sample_path = fixture_directory / "samples" / "n8_seed42.csv"
    frame = pd.read_csv(sample_path)
    frame["x0"] = 0
    frame.to_csv(sample_path, index=False)
    sample_manifest_path = sample_path.with_suffix(".manifest.json")
    sample_manifest = json.loads(sample_manifest_path.read_text(encoding="utf-8"))
    sample_manifest["sample"]["csv_sha256"] = file_sha256(sample_path)
    _write_json(sample_manifest_path, sample_manifest)
    config = load_targetwise_config(_write_config(tmp_path, fixture_directory))
    fake = _FakeRunner()
    fake_artifact = _FakeArtifactChecker()

    prepared = run_collection(
        config,
        output_root=tmp_path / "outputs",
        runner_factory=lambda: fake,
        artifact_checker=fake_artifact,
    )

    assert [call["target"] for call in fake.calls] == ["x1", "x2", "x3"]
    x0_metrics = json.loads(
        prepared.paths.cell("x0").metrics_json_path.read_text(encoding="utf-8")
    )
    assert x0_metrics["outcome"] == "skipped"
    assert x0_metrics["failure_reason"] == "empty E+ or E-"
    manifest = json.loads(prepared.paths.manifest_path.read_text(encoding="utf-8"))
    assert manifest["outcome_counts"] == {"skipped": 1, "solved": 3}
    assert len(fake_artifact.calls) == 3


def test_solution_check_resolver_uses_learner_produced_artefact(
    tmp_path: Path,
) -> None:
    solution = tmp_path / "learned.sol.aba"
    solution.write_text("% learned framework\n", encoding="utf-8")
    checked = tmp_path / "learned.sol_chk.asp"
    checked.write_text("x3(2).\n:- not x3(2).\n", encoding="utf-8")

    assert resolve_solution_check_asp_path(solution, tmp_path) == checked


def test_artifact_integrity_check_runs_saved_file_once_and_classifies_sat(
    tmp_path: Path,
) -> None:
    solution_check_asp = tmp_path / "learned.sol_chk.asp"
    solution_check_asp.write_text("x3(2).\n:- not x3(2).\n", encoding="utf-8")
    calls: list[dict[str, Any]] = []

    def fake_run(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        calls.append({"command": command, **kwargs})
        return subprocess.CompletedProcess(command, 10, "SATISFIABLE\n", "")

    result = final_artifact_integrity_check(
        solution_check_asp,
        timeout_s=1,
        clingo_path="/test/clingo",
        command_runner=fake_run,
    )

    assert result.status == "SAT"
    assert result.returncode == 10
    assert len(calls) == 1
    assert str(solution_check_asp) in calls[0]["command"]
    assert "-" not in calls[0]["command"]
    assert "input" not in calls[0]
    assert "--models=1" in calls[0]["command"]


def test_artifact_integrity_check_classifies_unsat_timeout_and_unavailable(
    tmp_path: Path,
) -> None:
    solution_check_asp = tmp_path / "learned.sol_chk.asp"
    solution_check_asp.write_text("x3(2).\n:- x3(2).\n", encoding="utf-8")

    def unsat_run(
        command: list[str], **kwargs: Any
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(command, 20, "UNSATISFIABLE\n", "")

    unsat = final_artifact_integrity_check(
        solution_check_asp,
        timeout_s=1,
        clingo_path="/test/clingo",
        command_runner=unsat_run,
    )
    assert unsat.status == "UNSAT"

    def timeout_run(command: list[str], **kwargs: Any) -> Any:
        raise subprocess.TimeoutExpired(command, kwargs["timeout"])

    timed_out = final_artifact_integrity_check(
        solution_check_asp,
        timeout_s=1,
        clingo_path="/test/clingo",
        command_runner=timeout_run,
    )
    assert timed_out.status == "TIMEOUT"

    unavailable = final_artifact_integrity_check(
        tmp_path / "missing.sol_chk.asp",
        timeout_s=1,
    )
    assert unavailable.status == "UNAVAILABLE"


@pytest.mark.skipif(shutil.which("clingo") is None, reason="clingo is not on PATH")
def test_artifact_integrity_check_with_real_clingo(tmp_path: Path) -> None:
    sat_asp = tmp_path / "sat.sol_chk.asp"
    sat_asp.write_text("x3(2).\n:- not x3(2).\n:- x3(1).\n", encoding="utf-8")
    unsat_asp = tmp_path / "unsat.sol_chk.asp"
    unsat_asp.write_text("x3(2).\n:- x3(2).\n", encoding="utf-8")

    sat = final_artifact_integrity_check(
        sat_asp,
        timeout_s=2,
    )
    unsat = final_artifact_integrity_check(
        unsat_asp,
        timeout_s=2,
    )

    assert sat.status == "SAT"
    assert unsat.status == "UNSAT"


def test_cli_validate_and_prepare_are_machine_inspectable(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    fixture_directory = _write_fixture_bundle(tmp_path / "source")
    config_path = _write_config(tmp_path, fixture_directory)
    config = load_targetwise_config(config_path)

    assert targetwise_main(["validate", "--config", str(config_path)]) == 0
    validated = json.loads(capsys.readouterr().out)
    assert validated["validated"] is True
    assert validated["configuration_id"] == "aamas2025"
    assert validated["configuration_hash"] == config.configuration_hash
    assert validated["targets"] == list(_VARIABLES)
    assert validated["learning_mode"] == "brave"
    assert validated["joint_check_timeout_s"] == 1.0

    output_root = tmp_path / "outputs"
    assert (
        targetwise_main(
            [
                "prepare",
                "--config",
                str(config_path),
                "--output-root",
                str(output_root),
            ]
        )
        == 0
    )
    prepared = json.loads(capsys.readouterr().out)
    assert prepared["prepared"] is True
    assert Path(prepared["manifest"]).is_file()
