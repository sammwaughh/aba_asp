"""Strict configuration loading for target-complete causal-fixture runs."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Mapping

import yaml

from causal.experiments.paths import repo_root
from causal.fixtures.artifacts import file_sha256


class TargetwiseConfigError(ValueError):
    """Raised when a target-wise run configuration is invalid."""


@dataclass(frozen=True)
class TargetwiseRunConfig:
    """One target-complete run over a selected frozen fixture sample."""

    config_path: Path
    config_hash: str
    configuration_id: str
    configuration_hash: str
    description: str | None
    fixture_directory: Path
    sample: Path
    encoding_type: str
    example_policy: str
    prolog_config: Path
    prolog_config_hash: str
    learning_mode: str
    prolog_timeout_s: float
    joint_check_timeout_s: float


_LEARNING_MODE_RE = re.compile(
    r"set_lopt\s*\(\s*learning_mode\s*\(\s*([a-z]+)\s*\)\s*\)"
)
_CHECK_IC_RE = re.compile(r"set_lopt\s*\(\s*check_ic\s*\)")
_CONFIGURATION_ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")
_SUPPORTED_LEARNING_MODES = frozenset({"brave", "cautious"})


def _mapping(value: Any, *, where: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise TargetwiseConfigError(f"{where} must be a mapping")
    return value


def _string(value: Any, *, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TargetwiseConfigError(f"{where} must be a non-empty string")
    return value.strip()


def _positive_number(value: Any, *, where: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
        raise TargetwiseConfigError(f"{where} must be a positive number")
    return float(value)


def _check_keys(
    value: Mapping[str, Any],
    *,
    where: str,
    required: set[str],
    optional: set[str] | None = None,
) -> None:
    optional = optional or set()
    missing = required - set(value)
    unknown = set(value) - required - optional
    if missing:
        raise TargetwiseConfigError(
            f"{where} is missing required keys: {sorted(missing)}"
        )
    if unknown:
        raise TargetwiseConfigError(f"{where} contains unknown keys: {sorted(unknown)}")


def _resolve_repo_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root() / path
    return path.resolve()


def _canonical_hash(value: Any) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    )
    return f"sha256:{hashlib.sha256(payload.encode('utf-8')).hexdigest()}"


def _configuration_id(value: Any) -> str:
    identifier = _string(value, where="configuration.id")
    if not _CONFIGURATION_ID_RE.fullmatch(identifier):
        raise TargetwiseConfigError(
            "configuration.id must start with a letter and contain only "
            "letters, digits, underscores, or hyphens"
        )
    return identifier


def _read_learning_mode(prolog_config: Path) -> str:
    text = "\n".join(
        line.split("%", 1)[0]
        for line in prolog_config.read_text(encoding="utf-8").splitlines()
    )
    modes = set(_LEARNING_MODE_RE.findall(text))
    if len(modes) != 1:
        raise TargetwiseConfigError(
            "learner.prolog_config must explicitly select exactly one "
            f"learning_mode; found {sorted(modes)!r}"
        )
    mode = modes.pop()
    if mode not in _SUPPORTED_LEARNING_MODES:
        raise TargetwiseConfigError(
            "the current target-wise runner supports only brave or cautious "
            f"learning; got learning_mode({mode})"
        )
    if not _CHECK_IC_RE.search(text):
        raise TargetwiseConfigError(
            "learner.prolog_config must explicitly enable set_lopt(check_ic) "
            "so the engine emits the final .sol_chk.asp integrity artefact"
        )
    return mode


def load_targetwise_config(path: Path | str) -> TargetwiseRunConfig:
    """Load a strict YAML configuration for a target-complete collection."""

    config_path = Path(path).resolve()
    if not config_path.is_file():
        raise FileNotFoundError(config_path)
    try:
        raw_value = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise TargetwiseConfigError(
            f"YAML parse error in {config_path}: {exc}"
        ) from exc
    raw = _mapping(raw_value, where="config")
    _check_keys(
        raw,
        where="config",
        required={"configuration", "fixture", "encoding", "learner"},
        optional={"description"},
    )

    description = raw.get("description")
    if description is not None and not isinstance(description, str):
        raise TargetwiseConfigError("description must be a string when present")

    configuration = _mapping(raw["configuration"], where="configuration")
    _check_keys(
        configuration,
        where="configuration",
        required={"id"},
    )
    configuration_id = _configuration_id(configuration["id"])

    fixture = _mapping(raw["fixture"], where="fixture")
    _check_keys(
        fixture,
        where="fixture",
        required={"directory", "sample"},
    )
    fixture_directory = _resolve_repo_path(
        _string(fixture["directory"], where="fixture.directory")
    )
    sample = Path(_string(fixture["sample"], where="fixture.sample"))
    if sample.is_absolute():
        raise TargetwiseConfigError(
            "fixture.sample must be relative to fixture.directory"
        )
    if sample.suffix.lower() != ".csv":
        raise TargetwiseConfigError("fixture.sample must name a .csv file")

    encoding = _mapping(raw["encoding"], where="encoding")
    _check_keys(
        encoding,
        where="encoding",
        required={"type", "example_policy"},
    )
    encoding_type = _string(encoding["type"], where="encoding.type")
    example_policy = _string(
        encoding["example_policy"], where="encoding.example_policy"
    )
    if encoding_type != "exact_value":
        raise TargetwiseConfigError(
            "the initial target-wise runner supports encoding.type='exact_value' only"
        )
    if example_policy != "binary_one_vs_zero":
        raise TargetwiseConfigError(
            "the initial target-wise runner supports "
            "encoding.example_policy='binary_one_vs_zero' only"
        )

    learner = _mapping(raw["learner"], where="learner")
    _check_keys(
        learner,
        where="learner",
        required={"prolog_config"},
        optional={
            "prolog_timeout_s",
            "joint_check_timeout_s",
        },
    )
    prolog_config = _resolve_repo_path(
        _string(learner["prolog_config"], where="learner.prolog_config")
    )
    if not prolog_config.is_file():
        raise FileNotFoundError(prolog_config)
    prolog_config_hash = file_sha256(prolog_config)
    learning_mode = _read_learning_mode(prolog_config)
    prolog_timeout_s = _positive_number(
        learner.get("prolog_timeout_s", 120),
        where="learner.prolog_timeout_s",
    )
    joint_check_timeout_s = _positive_number(
        learner.get("joint_check_timeout_s", 5),
        where="learner.joint_check_timeout_s",
    )
    configuration_hash = _canonical_hash(
        {
            "configuration_id": configuration_id,
            "encoding": {
                "type": encoding_type,
                "example_policy": example_policy,
            },
            "learner": {
                "prolog_config_sha256": prolog_config_hash,
                "learning_mode": learning_mode,
                "prolog_timeout_s": prolog_timeout_s,
                "joint_check_timeout_s": joint_check_timeout_s,
            },
        }
    )

    return TargetwiseRunConfig(
        config_path=config_path,
        config_hash=_canonical_hash(raw),
        configuration_id=configuration_id,
        configuration_hash=configuration_hash,
        description=description,
        fixture_directory=fixture_directory,
        sample=sample,
        encoding_type=encoding_type,
        example_policy=example_policy,
        prolog_config=prolog_config,
        prolog_config_hash=prolog_config_hash,
        learning_mode=learning_mode,
        prolog_timeout_s=prolog_timeout_s,
        joint_check_timeout_s=joint_check_timeout_s,
    )
