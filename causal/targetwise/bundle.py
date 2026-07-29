"""Loading and validation of generated causal-fixture bundles."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Mapping

import pandas as pd

from causal.fixtures.artifacts import file_sha256


class CausalFixtureBundleError(ValueError):
    """Raised when a generated fixture bundle is incomplete or inconsistent."""


def _require_schema_version(
    document: Mapping[str, Any],
    *,
    key: str,
    where: str,
) -> None:
    if document.get(key) != 1:
        raise CausalFixtureBundleError(
            f"{where}.{key} must equal the supported version 1"
        )


@dataclass(frozen=True)
class LoadedCausalFixtureBundle:
    """A validated frozen sample and its evaluator-only fixture metadata."""

    fixture_directory: Path
    fixture_id: str
    variables: tuple[str, ...]
    edges: tuple[tuple[str, str], ...]
    state_orders: Mapping[str, tuple[int | str, ...]]
    source_hash: str
    document_hash: str
    semantic_hash: str
    fixture_manifest_path: Path
    fixture_manifest_hash: str
    sample_path: Path
    sample_name: str
    sample_manifest_path: Path
    sample_manifest_hash: str
    sample_hash: str
    n: int
    seed: int
    dataframe: pd.DataFrame
    sample_bytes: bytes
    fixture_manifest: Mapping[str, Any]
    sample_manifest: Mapping[str, Any]


def _read_json(path: Path, *, where: str) -> Mapping[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(path)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CausalFixtureBundleError(f"invalid JSON in {where}: {path}") from exc
    if not isinstance(value, dict):
        raise CausalFixtureBundleError(f"{where} must contain a JSON object")
    return value


def _mapping(value: Any, *, where: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise CausalFixtureBundleError(f"{where} must be a mapping")
    return value


def _string(value: Any, *, where: str) -> str:
    if not isinstance(value, str) or not value:
        raise CausalFixtureBundleError(f"{where} must be a non-empty string")
    return value


def _int(value: Any, *, where: str, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise CausalFixtureBundleError(
            f"{where} must be an integer greater than or equal to {minimum}"
        )
    return value


def _within_directory(path: Path, directory: Path, *, where: str) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(directory.resolve())
    except ValueError as exc:
        raise CausalFixtureBundleError(
            f"{where} must be inside fixture.directory"
        ) from exc
    return resolved


def _parse_edges(
    value: Any, *, variables: tuple[str, ...]
) -> tuple[tuple[str, str], ...]:
    if not isinstance(value, list):
        raise CausalFixtureBundleError("fixture.edges must be a list")
    node_set = set(variables)
    edges: list[tuple[str, str]] = []
    for index, raw in enumerate(value):
        if (
            not isinstance(raw, list)
            or len(raw) != 2
            or not all(isinstance(node, str) for node in raw)
        ):
            raise CausalFixtureBundleError(
                f"fixture.edges[{index}] must be [source, target]"
            )
        edge = (raw[0], raw[1])
        if edge[0] not in node_set or edge[1] not in node_set:
            raise CausalFixtureBundleError(
                f"fixture.edges[{index}] names an unknown variable"
            )
        edges.append(edge)
    if len(set(edges)) != len(edges):
        raise CausalFixtureBundleError("fixture.edges contains duplicates")
    return tuple(edges)


def _parse_state_orders(
    value: Any, *, variables: tuple[str, ...]
) -> dict[str, tuple[int | str, ...]]:
    raw = _mapping(value, where="sampler.state_orders")
    if set(raw) != set(variables):
        raise CausalFixtureBundleError(
            "sampler.state_orders must name every fixture variable exactly once"
        )
    orders: dict[str, tuple[int | str, ...]] = {}
    for variable in variables:
        states = raw[variable]
        if not isinstance(states, list) or len(states) < 2:
            raise CausalFixtureBundleError(
                f"sampler.state_orders.{variable} must contain at least two states"
            )
        if any(
            isinstance(state, bool) or not isinstance(state, (int, str))
            for state in states
        ):
            raise CausalFixtureBundleError(
                f"sampler.state_orders.{variable} contains an invalid state"
            )
        if len(set(states)) != len(states):
            raise CausalFixtureBundleError(
                f"sampler.state_orders.{variable} contains duplicate states"
            )
        orders[variable] = tuple(states)
    return orders


def load_causal_fixture_bundle(
    fixture_directory: Path | str,
    sample: Path | str,
) -> LoadedCausalFixtureBundle:
    """Load one generated fixture directory and one explicitly selected sample."""

    fixture_dir = Path(fixture_directory).resolve()
    if not fixture_dir.is_dir():
        raise NotADirectoryError(fixture_dir)

    fixture_manifest_path = fixture_dir / "fixture_manifest.json"
    fixture_manifest = _read_json(fixture_manifest_path, where="fixture_manifest.json")
    _require_schema_version(
        fixture_manifest,
        key="fixture_manifest_schema_version",
        where="fixture_manifest",
    )
    fixture_info = _mapping(
        fixture_manifest.get("fixture"), where="fixture_manifest.fixture"
    )
    fixture_id = _string(fixture_info.get("id"), where="fixture_manifest.fixture.id")
    if fixture_dir.name != fixture_id:
        raise CausalFixtureBundleError(
            "fixture directory name must equal fixture_manifest.fixture.id: "
            f"{fixture_dir.name!r} != {fixture_id!r}"
        )
    variables_raw = fixture_info.get("variables")
    if (
        not isinstance(variables_raw, list)
        or not variables_raw
        or not all(isinstance(variable, str) and variable for variable in variables_raw)
        or len(set(variables_raw)) != len(variables_raw)
    ):
        raise CausalFixtureBundleError(
            "fixture_manifest.fixture.variables must be a non-empty unique string list"
        )
    variables = tuple(variables_raw)
    edges = _parse_edges(fixture_info.get("edges"), variables=variables)
    source_hash = _string(
        fixture_info.get("source_hash"),
        where="fixture_manifest.fixture.source_hash",
    )
    document_hash = _string(
        fixture_info.get("document_hash"),
        where="fixture_manifest.fixture.document_hash",
    )
    semantic_hash = _string(
        fixture_info.get("semantic_hash"),
        where="fixture_manifest.fixture.semantic_hash",
    )

    sample_relative = Path(sample)
    if sample_relative.is_absolute():
        raise CausalFixtureBundleError(
            "sample must be relative to the supplied fixture directory"
        )
    if sample_relative.suffix.lower() != ".csv":
        raise CausalFixtureBundleError("sample must name a .csv file")
    sample_path = _within_directory(
        fixture_dir / sample_relative,
        fixture_dir,
        where="sample",
    )
    if not sample_path.is_file():
        raise FileNotFoundError(sample_path)
    sample_manifest_path = sample_path.with_suffix(".manifest.json")
    sample_manifest = _read_json(sample_manifest_path, where="sample manifest")
    _require_schema_version(
        sample_manifest,
        key="sample_manifest_schema_version",
        where="sample_manifest",
    )

    sample_fixture = _mapping(
        sample_manifest.get("fixture"), where="sample_manifest.fixture"
    )
    expected_fixture_values = {
        "id": fixture_id,
        "source_hash": source_hash,
        "document_hash": document_hash,
        "semantic_hash": semantic_hash,
    }
    for key, expected in expected_fixture_values.items():
        actual = sample_fixture.get(key)
        if actual != expected:
            raise CausalFixtureBundleError(
                f"sample_manifest.fixture.{key} does not match fixture_manifest: "
                f"{actual!r} != {expected!r}"
            )

    sample_info = _mapping(
        sample_manifest.get("sample"), where="sample_manifest.sample"
    )
    n = _int(sample_info.get("n"), where="sample_manifest.sample.n", minimum=1)
    seed = _int(sample_info.get("seed"), where="sample_manifest.sample.seed", minimum=0)
    if sample_info.get("target") is not None:
        raise CausalFixtureBundleError(
            "selected sample must be target-free (sample.target must be null)"
        )
    if sample_info.get("iid_observational_rows") is not True:
        raise CausalFixtureBundleError(
            "selected sample must declare iid_observational_rows=true"
        )
    if sample_info.get("csv_columns_are_causal_variables_only") is not True:
        raise CausalFixtureBundleError(
            "selected sample must contain causal-variable columns only"
        )
    sample_hash = _string(
        sample_info.get("csv_sha256"),
        where="sample_manifest.sample.csv_sha256",
    )
    actual_sample_hash = file_sha256(sample_path)
    if actual_sample_hash != sample_hash:
        raise CausalFixtureBundleError(
            "sample CSV hash does not match sample manifest: "
            f"{actual_sample_hash} != {sample_hash}"
        )

    sampler = _mapping(sample_manifest.get("sampler"), where="sample_manifest.sampler")
    output_order = sampler.get("output_column_order")
    if output_order != list(variables):
        raise CausalFixtureBundleError(
            "sampler.output_column_order must equal fixture variable order"
        )
    state_orders = _parse_state_orders(sampler.get("state_orders"), variables=variables)

    try:
        dataframe = pd.read_csv(sample_path)
    except Exception as exc:
        raise CausalFixtureBundleError(
            f"could not read sample CSV: {sample_path}"
        ) from exc
    if list(dataframe.columns) != list(variables):
        raise CausalFixtureBundleError(
            "sample CSV columns must equal the declared fixture variable order"
        )
    if len(dataframe) != n:
        raise CausalFixtureBundleError(
            f"sample CSV has {len(dataframe)} rows but manifest declares n={n}"
        )
    if dataframe.isna().any().any():
        raise CausalFixtureBundleError(
            "target-wise baseline samples may not contain missing values"
        )
    for variable in variables:
        observed = set(dataframe[variable].tolist())
        declared = set(state_orders[variable])
        if not observed <= declared:
            raise CausalFixtureBundleError(
                f"sample CSV contains undeclared states for {variable}: "
                f"{sorted(observed - declared, key=str)}"
            )

    return LoadedCausalFixtureBundle(
        fixture_directory=fixture_dir,
        fixture_id=fixture_id,
        variables=variables,
        edges=edges,
        state_orders=state_orders,
        source_hash=source_hash,
        document_hash=document_hash,
        semantic_hash=semantic_hash,
        fixture_manifest_path=fixture_manifest_path,
        fixture_manifest_hash=file_sha256(fixture_manifest_path),
        sample_path=sample_path,
        sample_name=sample_path.stem,
        sample_manifest_path=sample_manifest_path,
        sample_manifest_hash=file_sha256(sample_manifest_path),
        sample_hash=sample_hash,
        n=n,
        seed=seed,
        dataframe=dataframe,
        sample_bytes=sample_path.read_bytes(),
        fixture_manifest=fixture_manifest,
        sample_manifest=sample_manifest,
    )
