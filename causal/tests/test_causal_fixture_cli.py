from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from causal.fixtures.artifacts import ArtifactConflictError
from causal.fixtures.cli import main
from causal.fixtures.io import default_diamond_spec_path
from causal.targetwise.bundle import load_causal_fixture_bundle
from causal.targetwise.encoding import build_binary_target_task
from causal.tests.fixture_test_utils import write_root_stochastic_deterministic_and


def test_validate_command_is_read_only_and_reports_hashes(capsys) -> None:
    assert main(["validate", "--fixture", str(default_diamond_spec_path())]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["validated"] is True
    assert result["fixture_id"] == "m13_bucket3_binary_diamond"
    assert result["source_hash"].startswith("sha256:")
    assert result["document_hash"].startswith("sha256:")
    assert result["semantic_hash"].startswith("sha256:")


def test_build_command_writes_complete_checked_bundle(
    tmp_path: Path, capsys
) -> None:
    output_dir = tmp_path / "bundle"
    assert (
        main(
            [
                "build",
                "--fixture",
                str(default_diamond_spec_path()),
                "--output-dir",
                str(output_dir),
                "--n",
                "50",
                "--seed",
                "42",
            ]
        )
        == 0
    )
    result = json.loads(capsys.readouterr().out)
    assert result["faithfulness"] == "verified_exactly"
    assert result["bif_round_trip_ok"] is True

    expected_files = {
        "population.csv",
        "certificate.json",
        "mechanism_reference.json",
        "model.bif",
        "fixture_manifest.json",
        "samples/n50_seed42.csv",
        "samples/n50_seed42.manifest.json",
    }
    observed_files = {
        str(path.relative_to(output_dir))
        for path in output_dir.rglob("*")
        if path.is_file()
    }
    assert observed_files == expected_files

    certificate = json.loads((output_dir / "certificate.json").read_text())
    manifest = json.loads((output_dir / "fixture_manifest.json").read_text())
    sample = pd.read_csv(output_dir / "samples" / "n50_seed42.csv")
    assert certificate["conditional_independence_audit"]["query_count"] == 24
    assert manifest["certificate_summary"]["mec_size"] == 3
    assert manifest["sample"]["target"] is None
    assert len(sample) == 50
    mechanism_reference = json.loads(
        (output_dir / "mechanism_reference.json").read_text(encoding="utf-8")
    )
    assert mechanism_reference["sample"]["available"] is True
    assert mechanism_reference["fixture"]["mechanism_regime"] == "positive_stochastic"

    # Identical rebuilds are idempotent; a different frozen sample is refused.
    capsys.readouterr()
    assert (
        main(
            [
                "build",
                "--fixture",
                str(default_diamond_spec_path()),
                "--output-dir",
                str(output_dir),
                "--n",
                "50",
                "--seed",
                "42",
            ]
        )
        == 0
    )
    capsys.readouterr()
    with pytest.raises(ArtifactConflictError, match="different bundle"):
        main(
            [
                "build",
                "--fixture",
                str(default_diamond_spec_path()),
                "--output-dir",
                str(output_dir),
                "--n",
                "50",
                "--seed",
                "43",
            ]
        )


def test_build_refuses_legacy_bundle_before_writing_new_artifacts(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "legacy_bundle"
    output_dir.mkdir()
    (output_dir / "fixture_manifest.json").write_text(
        json.dumps(
            {
                "fixture_manifest_schema_version": 1,
                "fixture_toolkit_version": 1,
                "sample": {"n": 50, "seed": 42},
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ArtifactConflictError, match="preserve it unchanged"):
        main(
            [
                "build",
                "--fixture",
                str(default_diamond_spec_path()),
                "--output-dir",
                str(output_dir),
                "--n",
                "50",
                "--seed",
                "42",
            ]
        )

    assert sorted(path.name for path in output_dir.iterdir()) == [
        "fixture_manifest.json"
    ]


def test_individual_write_subcommands(tmp_path: Path, capsys) -> None:
    fixture = str(default_diamond_spec_path())

    certificate_dir = tmp_path / "certificate"
    assert main(["certify", "--fixture", fixture, "--output-dir", str(certificate_dir)]) == 0
    json.loads(capsys.readouterr().out)
    assert (certificate_dir / "population.csv").is_file()
    assert (certificate_dir / "certificate.json").is_file()
    assert (certificate_dir / "mechanism_reference.json").is_file()
    assert (certificate_dir / "fixture_manifest.json").is_file()

    bif_path = tmp_path / "model.bif"
    assert main(["export-bif", "--fixture", fixture, "--output", str(bif_path)]) == 0
    bif_result = json.loads(capsys.readouterr().out)
    assert bif_result["round_trip"]["ok"] is True

    csv_path = tmp_path / "sample.csv"
    assert (
        main(
            [
                "sample",
                "--fixture",
                fixture,
                "--n",
                "7",
                "--seed",
                "42",
                "--output",
                str(csv_path),
            ]
        )
        == 0
    )
    sample_result = json.loads(capsys.readouterr().out)
    assert sample_result["target"] is None
    assert len(pd.read_csv(csv_path)) == 7
    assert csv_path.with_suffix(".manifest.json").is_file()


def test_schema2_bundle_is_accepted_by_binary_targetwise_encoder(
    tmp_path: Path, capsys
) -> None:
    fixture_path = write_root_stochastic_deterministic_and(tmp_path)
    output_dir = tmp_path / "test_root_stochastic_deterministic_and"
    assert (
        main(
            [
                "build",
                "--fixture",
                str(fixture_path),
                "--output-dir",
                str(output_dir),
                "--n",
                "12",
                "--seed",
                "42",
            ]
        )
        == 0
    )
    result = json.loads(capsys.readouterr().out)
    assert result["faithfulness"] == "verified_exactly"

    bundle = load_causal_fixture_bundle(output_dir, "samples/n12_seed42.csv")
    task = build_binary_target_task(bundle, "c")
    assert task.target == "c"
    assert task.predictor_order == ("a", "b")
    assert task.n_positive + task.n_negative == 12
