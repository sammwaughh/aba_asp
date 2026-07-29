from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from causal.fixtures.io import default_diamond_spec_path, load_fixture
from causal.fixtures.artifacts import ArtifactConflictError
from causal.fixtures.sampling import sample_iid, write_sample_artifacts


def test_seed_42_golden_prefix_and_summary() -> None:
    fixture = load_fixture(default_diamond_spec_path()).fixture
    frame = sample_iid(fixture, n=50, seed=42).dataframe

    assert frame.head(4).values.tolist() == [
        [1, 1, 1, 1],
        [0, 1, 1, 1],
        [0, 0, 0, 1],
        [1, 1, 1, 1],
    ]
    assert frame.mean().to_dict() == {
        "x0": 0.46,
        "x1": 0.52,
        "x2": 0.52,
        "x3": 0.54,
    }
    assert frame.drop_duplicates().shape[0] == 13


def test_same_seed_larger_sample_has_exact_nested_prefix() -> None:
    fixture = load_fixture(default_diamond_spec_path()).fixture
    small = sample_iid(fixture, n=50, seed=42).dataframe
    large = sample_iid(fixture, n=100, seed=42).dataframe
    repeated = sample_iid(fixture, n=50, seed=42).dataframe

    pd.testing.assert_frame_equal(small, large.iloc[:50].reset_index(drop=True))
    pd.testing.assert_frame_equal(small, repeated)
    assert not small.equals(sample_iid(fixture, n=50, seed=43).dataframe)


def test_sampler_does_not_mutate_legacy_numpy_global_rng() -> None:
    fixture = load_fixture(default_diamond_spec_path()).fixture
    np.random.seed(1234)
    expected = np.random.random(5)
    np.random.seed(1234)
    sample_iid(fixture, n=10, seed=42)
    observed = np.random.random(5)
    np.testing.assert_array_equal(observed, expected)


def test_sample_csv_has_only_causal_variables_and_manifest_is_explicit(
    tmp_path: Path,
) -> None:
    loaded = load_fixture(default_diamond_spec_path())
    artifacts = write_sample_artifacts(
        loaded,
        n=50,
        seed=42,
        csv_path=tmp_path / "n50_seed42.csv",
    )
    frame = pd.read_csv(artifacts.csv_path)
    manifest = json.loads(artifacts.manifest_path.read_text(encoding="utf-8"))

    assert frame.columns.tolist() == ["x0", "x1", "x2", "x3"]
    assert len(frame) == 50
    assert manifest["sample"]["target"] is None
    assert manifest["sample"]["csv_columns_are_causal_variables_only"] is True
    assert manifest["sampler"]["id"] == "row_major_ancestral_inverse_cdf"
    assert manifest["sampler"]["rng"] == "numpy.random.PCG64"
    assert manifest["empirical_table_summary"]["unique_joint_states_observed"] == 13
    assert artifacts.csv_hash == manifest["sample"]["csv_sha256"]

    repeated = write_sample_artifacts(
        loaded,
        n=50,
        seed=42,
        csv_path=artifacts.csv_path,
        manifest_path=artifacts.manifest_path,
    )
    assert repeated.csv_hash == artifacts.csv_hash
    with pytest.raises(ArtifactConflictError, match="refusing to overwrite"):
        write_sample_artifacts(
            loaded,
            n=50,
            seed=43,
            csv_path=artifacts.csv_path,
            manifest_path=artifacts.manifest_path,
        )


@pytest.mark.parametrize("n", [0, -1, 1.5, True])
def test_invalid_sample_size_is_rejected(n) -> None:
    fixture = load_fixture(default_diamond_spec_path()).fixture
    with pytest.raises(ValueError, match="positive integer"):
        sample_iid(fixture, n=n, seed=42)
