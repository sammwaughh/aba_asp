"""Target-free, nested-prefix IID sampling from exact causal fixtures."""

from __future__ import annotations

from dataclasses import dataclass
import json
import platform
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from causal.fixtures.io import LoadedFixture
from causal.fixtures.artifacts import (
    FIXTURE_TOOLKIT_VERSION,
    file_sha256,
    write_text_once,
)
from causal.fixtures.model import CausalFixture, StateValue, point_mass_index


SAMPLER_ID = "row_major_ancestral_inverse_cdf"
SAMPLER_VERSION = 2


@dataclass(frozen=True)
class SampleBatch:
    fixture_id: str
    n: int
    seed: int
    dataframe: pd.DataFrame
    topological_order: tuple[str, ...]


@dataclass(frozen=True)
class SampleArtifacts:
    batch: SampleBatch
    csv_path: Path
    manifest_path: Path
    csv_hash: str
    manifest: dict[str, Any]


def _choose_state(
    states: tuple[StateValue, ...], probabilities, draw: float
) -> StateValue:
    cumulative = 0.0
    for index, (state, probability) in enumerate(zip(states, probabilities)):
        cumulative += float(probability)
        if draw < cumulative or index == len(states) - 1:
            return state
    raise AssertionError("validated probability vector did not yield a state")


def sample_iid(fixture: CausalFixture, *, n: int, seed: int) -> SampleBatch:
    """Sample rows first and nodes second using a local PCG64 generator.

    Restarting this function with the same fixture and seed at a larger ``n``
    reproduces every smaller table as an exact prefix.
    """
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError("n must be a positive integer")
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
        raise ValueError("seed must be a non-negative integer")

    rng = np.random.Generator(np.random.PCG64(seed))
    records: list[dict[str, StateValue]] = []
    for _ in range(n):
        assignment: dict[str, StateValue] = {}
        for variable in fixture.topological_order:
            mechanism = fixture.mechanism_for(variable)
            parent_assignment = {
                parent: assignment[parent] for parent in mechanism.parents
            }
            probabilities = mechanism.distribution(parent_assignment)
            states = fixture.states_of(variable)
            certain_index = point_mass_index(probabilities)
            if certain_index is None:
                assignment[variable] = _choose_state(
                    states, probabilities, float(rng.random())
                )
            else:
                assignment[variable] = states[certain_index]
        records.append(
            {variable: assignment[variable] for variable in fixture.variable_names}
        )

    dataframe = pd.DataFrame.from_records(records, columns=list(fixture.variable_names))
    return SampleBatch(
        fixture_id=fixture.fixture_id,
        n=n,
        seed=seed,
        dataframe=dataframe,
        topological_order=fixture.topological_order,
    )


def _file_hash(path: Path) -> str:
    return file_sha256(path)


def _state_counts(
    fixture: CausalFixture, dataframe: pd.DataFrame
) -> dict[str, list[dict[str, Any]]]:
    return {
        variable: [
            {
                "state": state,
                "count": int((dataframe[variable] == state).sum()),
            }
            for state in fixture.states_of(variable)
        ]
        for variable in fixture.variable_names
    }


def _verify_deterministic_assignments(
    fixture: CausalFixture, dataframe: pd.DataFrame
) -> int:
    checks = 0
    for variable in fixture.deterministic_variables:
        mechanism = fixture.mechanism_for(variable)
        states = fixture.states_of(variable)
        for record in dataframe.to_dict(orient="records"):
            parent_assignment = {parent: record[parent] for parent in mechanism.parents}
            probabilities = mechanism.distribution(parent_assignment)
            certain_index = point_mass_index(probabilities)
            if certain_index is None:  # pragma: no cover - protected by classification
                raise AssertionError(f"{variable} ceased to be deterministic")
            if record[variable] != states[certain_index]:
                raise AssertionError(
                    f"sampled value for {variable} violates its deterministic mechanism"
                )
            checks += 1
    return checks


def write_sample_artifacts(
    loaded: LoadedFixture,
    *,
    n: int,
    seed: int,
    csv_path: Path | str,
    manifest_path: Path | str | None = None,
) -> SampleArtifacts:
    """Write one deterministic CSV and its provenance/coverage manifest."""
    fixture = loaded.fixture
    batch = sample_iid(fixture, n=n, seed=seed)
    deterministic_checks = _verify_deterministic_assignments(fixture, batch.dataframe)
    destination = Path(csv_path)
    csv_text = batch.dataframe.to_csv(index=False, lineterminator="\n")
    write_text_once(destination, csv_text)
    csv_hash = _file_hash(destination)

    if manifest_path is None:
        manifest_destination = destination.with_suffix(".manifest.json")
    else:
        manifest_destination = Path(manifest_path)
    manifest: dict[str, Any] = {
        "sample_manifest_schema_version": 1,
        "fixture": {
            "id": fixture.fixture_id,
            "source_path": str(loaded.source_path),
            "source_hash": loaded.source_hash,
            "source_hash_basis": "exact UTF-8 source-file bytes",
            "document_hash": loaded.document_hash,
            "document_hash_basis": "canonical parsed YAML document",
            "semantic_hash": loaded.semantic_hash,
        },
        "sample": {
            "n": n,
            "seed": seed,
            "target": None,
            "target_note": "target selection occurs after this table is frozen",
            "iid_observational_rows": True,
            "csv_path": str(destination),
            "csv_sha256": csv_hash,
            "csv_columns_are_causal_variables_only": True,
            "row_identifier": "one-based CSV data-row number; not a causal variable",
            "mechanism_regime": fixture.assumptions.mechanism_regime,
        },
        "sampler": {
            "fixture_toolkit_version": FIXTURE_TOOLKIT_VERSION,
            "implementation_hash": file_sha256(Path(__file__)),
            "id": SAMPLER_ID,
            "version": SAMPLER_VERSION,
            "rng": "numpy.random.PCG64",
            "row_major": True,
            "draw_policy": (
                "one uniform draw for each non-degenerate local distribution "
                "encountered; point-mass mechanisms consume no random draw"
            ),
            "stochastic_variables": list(fixture.stochastic_variables),
            "deterministic_variables": list(fixture.deterministic_variables),
            "randomness_confined_to_roots": set(fixture.stochastic_variables)
            <= set(fixture.root_names),
            "topological_order": list(batch.topological_order),
            "output_column_order": list(fixture.variable_names),
            "parent_orders": {
                variable: list(fixture.parents_of(variable))
                for variable in fixture.variable_names
            },
            "state_orders": {
                variable: list(fixture.states_of(variable))
                for variable in fixture.variable_names
            },
            "nested_prefix_guarantee": (
                "for the same semantic fixture, seed, sampler version, and orders, "
                "sample(n_small) equals the first n_small rows of sample(n_large)"
            ),
        },
        "empirical_table_summary": {
            "state_counts": _state_counts(fixture, batch.dataframe),
            "unique_joint_states_observed": int(
                batch.dataframe.drop_duplicates().shape[0]
            ),
            "deterministic_assignments_verified": True,
            "deterministic_assignment_checks": deterministic_checks,
        },
        "runtime": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "pandas": pd.__version__,
        },
    }
    write_text_once(
        manifest_destination, json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )
    return SampleArtifacts(
        batch=batch,
        csv_path=destination,
        manifest_path=manifest_destination,
        csv_hash=csv_hash,
        manifest=manifest,
    )
