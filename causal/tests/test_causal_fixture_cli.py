from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from causal.fixtures.artifacts import ArtifactConflictError
from causal.fixtures.cli import main
from causal.fixtures.io import default_diamond_spec_path


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


def test_individual_write_subcommands(tmp_path: Path, capsys) -> None:
    fixture = str(default_diamond_spec_path())

    certificate_dir = tmp_path / "certificate"
    assert main(["certify", "--fixture", fixture, "--output-dir", str(certificate_dir)]) == 0
    json.loads(capsys.readouterr().out)
    assert (certificate_dir / "population.csv").is_file()
    assert (certificate_dir / "certificate.json").is_file()
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
