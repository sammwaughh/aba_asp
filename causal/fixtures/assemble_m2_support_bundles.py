#!/usr/bin/env python3
"""Assemble M2 exhaustive-support fixture bundles and target-wise configs."""

from __future__ import annotations

import json
import shutil
from collections import Counter
from pathlib import Path

import pandas as pd

from causal.experiments.paths import repo_root
from causal.fixtures.artifacts import file_sha256
from causal.fixtures.cli import certify_to_directory
from causal.fixtures.io import load_fixture
from causal.fixtures.reference import (
    build_mechanism_reference,
    write_mechanism_reference,
)

FIXTURES = (
    "m2_support_and_collider",
    "m2_support_or_collider",
    "m2_support_xor_collider",
    "m2_support_copy",
    "m2_support_not",
    "m2_support_copy_chain",
    "m2_support_fork_copy_not",
    "m2_support_and3",
    "m2_support_or3",
    "m2_support_and4",
    "m2_support_and3_lead_iso",
    "m2_support_majority3",
    "m2_support_mux",
)


def _write_fixture_manifest(loaded, *, output_dir: Path, artifacts: dict) -> Path:
    from causal.fixtures.cli import _write_fixture_manifest as write_manifest
    from causal.fixtures.analysis import build_certificate

    population, certificate = build_certificate(loaded)
    return write_manifest(
        loaded,
        output_dir=output_dir,
        artifacts=artifacts,
        certificate=certificate,
        sample_summary={
            "n": None,
            "seed": 0,
            "target": None,
            "table": "handwritten_exhaustive_root_support",
            "csv_name": "support.csv",
        },
    )


def assemble_one(fixture_id: str) -> None:
    root = repo_root()
    spec = root / "causal" / "fixtures" / "specs" / f"{fixture_id}.yaml"
    table = (
        root / "causal" / "fixtures" / "handwritten_tables" / f"{fixture_id}.csv"
    )
    output_dir = root / "causal" / "outputs" / "causal_fixtures" / fixture_id
    output_dir.mkdir(parents=True, exist_ok=True)

    loaded = load_fixture(spec)
    population, certificate, artifacts = certify_to_directory(loaded, output_dir)
    mechanism_reference = build_mechanism_reference(
        loaded,
        population,
        sample=pd.read_csv(table),
        sample_name="support",
    )
    artifacts["mechanism_reference"] = write_mechanism_reference(
        mechanism_reference, output_dir / "mechanism_reference.json"
    )

    samples_dir = output_dir / "samples"
    samples_dir.mkdir(parents=True, exist_ok=True)
    csv_path = samples_dir / "support.csv"
    shutil.copyfile(table, csv_path)
    dataframe = pd.read_csv(csv_path)
    variables = list(loaded.fixture.variable_names)
    if list(dataframe.columns) != variables:
        raise SystemExit(
            f"{fixture_id}: CSV columns {list(dataframe.columns)} != {variables}"
        )

    state_counts = {}
    for variable in variables:
        counts = Counter(int(value) for value in dataframe[variable].tolist())
        state_counts[variable] = [
            {"state": state, "count": counts.get(state, 0)}
            for state in loaded.fixture.states_of(variable)
        ]

    parent_orders = {
        variable: list(loaded.fixture.mechanism_for(variable).parents)
        for variable in variables
    }
    deterministic = [
        variable
        for variable in variables
        if loaded.fixture.mechanism_for(variable).parents
    ]
    stochastic = [
        variable
        for variable in variables
        if not loaded.fixture.mechanism_for(variable).parents
    ]
    csv_hash = file_sha256(csv_path)
    manifest = {
        "empirical_table_summary": {
            "deterministic_assignment_checks": len(dataframe),
            "deterministic_assignments_verified": True,
            "state_counts": state_counts,
            "unique_joint_states_observed": int(
                dataframe.drop_duplicates().shape[0]
            ),
            "table_kind": "handwritten_exhaustive_root_support",
        },
        "fixture": {
            "document_hash": loaded.document_hash,
            "document_hash_basis": "canonical parsed YAML document",
            "id": loaded.fixture.fixture_id,
            "semantic_hash": loaded.semantic_hash,
            "source_hash": loaded.source_hash,
            "source_hash_basis": "exact UTF-8 source-file bytes",
            "source_path": str(spec),
        },
        "sample": {
            "csv_columns_are_causal_variables_only": True,
            "csv_path": str(
                csv_path.relative_to(root) if csv_path.is_relative_to(root) else csv_path
            ),
            "csv_sha256": csv_hash,
            "iid_observational_rows": True,
            "mechanism_regime": loaded.fixture.assumptions.mechanism_regime,
            "n": int(len(dataframe)),
            "row_identifier": "one-based CSV data-row number; not a causal variable",
            "seed": 0,
            "target": None,
            "target_note": (
                "handwritten exhaustive root-support table; not an IID draw. "
                "The iid_observational_rows flag is required by the target-wise "
                "loader and does not mean the rows were sampled."
            ),
        },
        "sample_manifest_schema_version": 1,
        "sampler": {
            "deterministic_variables": deterministic,
            "draw_policy": (
                "handwritten exhaustive combinations of root assignments; "
                "non-roots are the deterministic mechanism values"
            ),
            "id": "handwritten_exhaustive_root_support",
            "output_column_order": variables,
            "parent_orders": parent_orders,
            "randomness_confined_to_roots": True,
            "state_orders": {
                variable: list(loaded.fixture.states_of(variable))
                for variable in variables
            },
            "stochastic_variables": stochastic,
            "topological_order": list(loaded.fixture.topological_order),
            "version": 1,
        },
    }
    manifest_path = samples_dir / "support.manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    artifacts["sample_csv"] = csv_path
    artifacts["sample_manifest"] = manifest_path

    from causal.fixtures.cli import _write_fixture_manifest

    _write_fixture_manifest(
        loaded,
        output_dir=output_dir,
        artifacts=artifacts,
        certificate=certificate,
        sample_summary={
            "n": int(len(dataframe)),
            "seed": 0,
            "target": None,
            "csv_sha256": csv_hash,
            "unique_joint_states_observed": int(
                dataframe.drop_duplicates().shape[0]
            ),
            "table_kind": "handwritten_exhaustive_root_support",
        },
    )

    config_dir = (
        root
        / "causal"
        / "configs"
        / "targetwise"
        / fixture_id
        / "baseline_cautious"
    )
    config_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_dir / "support.yaml"
    config_path.write_text(
        "\n".join(
            [
                f'description: "M2 exhaustive-support {fixture_id} under baseline_cautious."',
                "",
                "configuration:",
                "  id: baseline_cautious",
                "",
                "fixture:",
                f"  directory: causal/outputs/causal_fixtures/{fixture_id}",
                "  sample: samples/support.csv",
                "",
                "encoding:",
                "  type: exact_value",
                "  example_policy: binary_one_vs_zero",
                "",
                "learner:",
                "  prolog_config: configs/baseline_cautious_config.pl",
                "  prolog_timeout_s: 300",
                "  joint_check_timeout_s: 5",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"assembled {fixture_id} n={len(dataframe)}")


def main() -> None:
    for fixture_id in FIXTURES:
        assemble_one(fixture_id)


if __name__ == "__main__":
    main()
