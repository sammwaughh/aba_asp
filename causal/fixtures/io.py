"""YAML loading and stable hashing for causal fixture definitions."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

from causal.fixtures.model import (
    CPTRow,
    CausalAssumptions,
    CausalFixture,
    FixtureValidationError,
    Mechanism,
    POSITIVE_STOCHASTIC_REGIME,
    StateValue,
    Variable,
)


@dataclass(frozen=True)
class LoadedFixture:
    """A validated fixture plus source and semantic provenance hashes."""

    fixture: CausalFixture
    source_path: Path
    source_hash: str
    document_hash: str
    semantic_hash: str
    raw: Mapping[str, Any]


def _require_mapping(value: Any, *, where: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise FixtureValidationError(f"{where} must be a mapping")
    return value


def _require_list(value: Any, *, where: str) -> Sequence[Any]:
    if not isinstance(value, list):
        raise FixtureValidationError(f"{where} must be a list")
    return value


def _require_str(value: Any, *, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise FixtureValidationError(f"{where} must be a non-empty string")
    return value


def _require_bool(value: Any, *, where: str) -> bool:
    if not isinstance(value, bool):
        raise FixtureValidationError(f"{where} must be a boolean")
    return value


def _check_keys(
    mapping: Mapping[str, Any],
    *,
    where: str,
    required: set[str],
    optional: set[str] | None = None,
) -> None:
    optional = optional or set()
    missing = required - set(mapping)
    unknown = set(mapping) - required - optional
    if missing:
        raise FixtureValidationError(f"{where} is missing required keys: {sorted(missing)}")
    if unknown:
        raise FixtureValidationError(f"{where} contains unknown keys: {sorted(unknown)}")


def parse_fraction(value: Any, *, where: str) -> Fraction:
    """Parse an exact rational and reject YAML floats."""
    if isinstance(value, bool) or isinstance(value, float):
        raise FixtureValidationError(
            f"{where} must be an exact integer or rational string, not a float"
        )
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, str):
        try:
            return Fraction(value.strip())
        except (ValueError, ZeroDivisionError) as exc:
            raise FixtureValidationError(
                f"{where} is not a valid exact rational: {value!r}"
            ) from exc
    raise FixtureValidationError(f"{where} must be an integer or rational string")


def _parse_state(value: Any, *, where: str) -> StateValue:
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise FixtureValidationError(f"{where} must be an int or string")
    if isinstance(value, str) and not value:
        raise FixtureValidationError(f"{where} must not be empty")
    return value


def _canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def _semantic_payload(fixture: CausalFixture) -> dict[str, Any]:
    """Return a normalized scientific payload independent of YAML formatting."""
    mechanisms: list[dict[str, Any]] = []
    for variable in fixture.variables:
        mechanism = fixture.mechanism_for(variable.name)
        rows: list[dict[str, Any]] = []
        parent_domains = [fixture.states_of(parent) for parent in mechanism.parents]
        from itertools import product

        for parent_values in product(*parent_domains):
            parent_assignment = dict(zip(mechanism.parents, parent_values))
            rows.append(
                {
                    "when": [list(item) for item in zip(mechanism.parents, parent_values)],
                    "probabilities": [
                        str(probability)
                        for probability in mechanism.distribution(parent_assignment)
                    ],
                }
            )
        mechanisms.append(
            {
                "variable": variable.name,
                "parents": list(mechanism.parents),
                "cpt": rows,
            }
        )

    node_index = {node: i for i, node in enumerate(fixture.variable_names)}
    edges = sorted(
        fixture.edges, key=lambda edge: (node_index[edge[0]], node_index[edge[1]])
    )
    assumptions = {
        "causal_sufficiency_declared": (
            fixture.assumptions.causal_sufficiency_declared
        ),
        "exogenous_noise": fixture.assumptions.exogenous_noise,
        "sampling_regime": fixture.assumptions.sampling_regime,
    }
    if fixture.schema_version >= 2:
        assumptions["mechanism_regime"] = fixture.assumptions.mechanism_regime

    return {
        "schema_version": fixture.schema_version,
        "id": fixture.fixture_id,
        "variables": [
            {"name": variable.name, "states": list(variable.states)}
            for variable in fixture.variables
        ],
        "edges": [list(edge) for edge in edges],
        "mechanisms": mechanisms,
        "assumptions": assumptions,
    }


def semantic_hash(fixture: CausalFixture) -> str:
    return _canonical_hash(_semantic_payload(fixture))


def fixture_specs_root() -> Path:
    return Path(__file__).resolve().parent / "specs"


def default_diamond_spec_path() -> Path:
    return fixture_specs_root() / "m13_bucket3_binary_diamond.yaml"


def load_fixture(path: Path | str) -> LoadedFixture:
    """Load, strictly parse, and validate an exact fixture YAML file."""
    source_path = Path(path)
    if not source_path.is_file():
        raise FileNotFoundError(source_path)
    source_bytes = source_path.read_bytes()
    try:
        source_text = source_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise FixtureValidationError(f"fixture source must be UTF-8: {source_path}") from exc
    try:
        raw_value = yaml.safe_load(source_text)
    except yaml.YAMLError as exc:
        raise FixtureValidationError(f"YAML parse error in {source_path}: {exc}") from exc

    raw = _require_mapping(raw_value, where="fixture")
    _check_keys(
        raw,
        where="fixture",
        required={
            "schema_version",
            "id",
            "variables",
            "graph",
            "mechanisms",
            "assumptions",
        },
        optional={"title", "description", "metadata"},
    )
    schema_version = raw["schema_version"]
    if isinstance(schema_version, bool) or not isinstance(schema_version, int):
        raise FixtureValidationError("fixture.schema_version must be an int")
    if schema_version not in {1, 2}:
        raise FixtureValidationError(
            f"unsupported fixture schema_version: {schema_version!r}"
        )
    fixture_id = _require_str(raw["id"], where="fixture.id")
    title = raw.get("title", fixture_id)
    title = _require_str(title, where="fixture.title")
    description_value = raw.get("description", "")
    if not isinstance(description_value, str):
        raise FixtureValidationError("fixture.description must be a string")

    variables_raw = _require_list(raw["variables"], where="fixture.variables")
    variables: list[Variable] = []
    for i, value in enumerate(variables_raw):
        variable_raw = _require_mapping(value, where=f"fixture.variables[{i}]")
        _check_keys(
            variable_raw,
            where=f"fixture.variables[{i}]",
            required={"name", "states"},
        )
        name = _require_str(variable_raw["name"], where=f"fixture.variables[{i}].name")
        states_raw = _require_list(
            variable_raw["states"], where=f"fixture.variables[{i}].states"
        )
        states = tuple(
            _parse_state(state, where=f"fixture.variables[{i}].states[{j}]")
            for j, state in enumerate(states_raw)
        )
        variables.append(Variable(name=name, states=states))

    graph_raw = _require_mapping(raw["graph"], where="fixture.graph")
    _check_keys(graph_raw, where="fixture.graph", required={"edges"})
    edges_raw = _require_list(graph_raw["edges"], where="fixture.graph.edges")
    edges: list[tuple[str, str]] = []
    for i, edge in enumerate(edges_raw):
        if not isinstance(edge, list) or len(edge) != 2:
            raise FixtureValidationError(
                f"fixture.graph.edges[{i}] must be [source, target]"
            )
        edges.append(
            (
                _require_str(edge[0], where=f"fixture.graph.edges[{i}][0]"),
                _require_str(edge[1], where=f"fixture.graph.edges[{i}][1]"),
            )
        )

    mechanisms_raw = _require_mapping(raw["mechanisms"], where="fixture.mechanisms")
    mechanisms: list[Mechanism] = []
    for variable in variables:
        if variable.name not in mechanisms_raw:
            raise FixtureValidationError(
                f"fixture.mechanisms is missing variable {variable.name!r}"
            )
        mechanism_raw = _require_mapping(
            mechanisms_raw[variable.name],
            where=f"fixture.mechanisms.{variable.name}",
        )
        _check_keys(
            mechanism_raw,
            where=f"fixture.mechanisms.{variable.name}",
            required={"parents", "cpt"},
        )
        parents_raw = _require_list(
            mechanism_raw["parents"],
            where=f"fixture.mechanisms.{variable.name}.parents",
        )
        parents = tuple(
            _require_str(
                parent, where=f"fixture.mechanisms.{variable.name}.parents[{i}]"
            )
            for i, parent in enumerate(parents_raw)
        )
        cpt_raw = _require_list(
            mechanism_raw["cpt"], where=f"fixture.mechanisms.{variable.name}.cpt"
        )
        rows: list[CPTRow] = []
        for i, row_value in enumerate(cpt_raw):
            row_raw = _require_mapping(
                row_value, where=f"fixture.mechanisms.{variable.name}.cpt[{i}]"
            )
            _check_keys(
                row_raw,
                where=f"fixture.mechanisms.{variable.name}.cpt[{i}]",
                required={"when", "probabilities"},
            )
            when_raw = _require_mapping(
                row_raw["when"],
                where=f"fixture.mechanisms.{variable.name}.cpt[{i}].when",
            )
            when: list[tuple[str, StateValue]] = []
            for parent in parents:
                if parent not in when_raw:
                    raise FixtureValidationError(
                        f"fixture.mechanisms.{variable.name}.cpt[{i}].when "
                        f"is missing parent {parent!r}"
                    )
                when.append(
                    (
                        parent,
                        _parse_state(
                            when_raw[parent],
                            where=(
                                f"fixture.mechanisms.{variable.name}.cpt[{i}]"
                                f".when.{parent}"
                            ),
                        ),
                    )
                )
            unknown_when = set(when_raw) - set(parents)
            if unknown_when:
                raise FixtureValidationError(
                    f"fixture.mechanisms.{variable.name}.cpt[{i}].when contains "
                    f"unknown parents: {sorted(unknown_when)}"
                )
            probabilities_raw = _require_list(
                row_raw["probabilities"],
                where=f"fixture.mechanisms.{variable.name}.cpt[{i}].probabilities",
            )
            probabilities = tuple(
                parse_fraction(
                    probability,
                    where=(
                        f"fixture.mechanisms.{variable.name}.cpt[{i}]"
                        f".probabilities[{j}]"
                    ),
                )
                for j, probability in enumerate(probabilities_raw)
            )
            rows.append(CPTRow(when=tuple(when), probabilities=probabilities))
        mechanisms.append(
            Mechanism(variable=variable.name, parents=parents, rows=tuple(rows))
        )

    extra_mechanisms = set(mechanisms_raw) - {variable.name for variable in variables}
    if extra_mechanisms:
        raise FixtureValidationError(
            f"fixture.mechanisms contains unknown variables: {sorted(extra_mechanisms)}"
        )

    assumptions_raw = _require_mapping(raw["assumptions"], where="fixture.assumptions")
    assumption_keys = {"causal_sufficiency", "observational_sampling"}
    if schema_version >= 2:
        assumption_keys.add("mechanism_regime")
    _check_keys(
        assumptions_raw,
        where="fixture.assumptions",
        required=assumption_keys,
    )
    sufficiency_raw = _require_mapping(
        assumptions_raw["causal_sufficiency"],
        where="fixture.assumptions.causal_sufficiency",
    )
    _check_keys(
        sufficiency_raw,
        where="fixture.assumptions.causal_sufficiency",
        required={"declared", "exogenous_noise"},
    )
    sampling_raw = _require_mapping(
        assumptions_raw["observational_sampling"],
        where="fixture.assumptions.observational_sampling",
    )
    _check_keys(
        sampling_raw,
        where="fixture.assumptions.observational_sampling",
        required={"regime"},
    )
    assumptions = CausalAssumptions(
        causal_sufficiency_declared=_require_bool(
            sufficiency_raw["declared"],
            where="fixture.assumptions.causal_sufficiency.declared",
        ),
        exogenous_noise=_require_str(
            sufficiency_raw["exogenous_noise"],
            where="fixture.assumptions.causal_sufficiency.exogenous_noise",
        ),
        sampling_regime=_require_str(
            sampling_raw["regime"],
            where="fixture.assumptions.observational_sampling.regime",
        ),
        mechanism_regime=(
            POSITIVE_STOCHASTIC_REGIME
            if schema_version == 1
            else _require_str(
                assumptions_raw["mechanism_regime"],
                where="fixture.assumptions.mechanism_regime",
            )
        ),
    )

    fixture = CausalFixture(
        schema_version=schema_version,
        fixture_id=fixture_id,
        title=title,
        description=description_value,
        variables=tuple(variables),
        edges=tuple(edges),
        mechanisms=tuple(mechanisms),
        assumptions=assumptions,
    )
    return LoadedFixture(
        fixture=fixture,
        source_path=source_path.resolve(),
        source_hash=f"sha256:{hashlib.sha256(source_bytes).hexdigest()}",
        document_hash=_canonical_hash(raw),
        semantic_hash=semantic_hash(fixture),
        raw=raw,
    )
