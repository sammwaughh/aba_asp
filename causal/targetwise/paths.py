"""Canonical repository paths for target-complete learning collections."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from causal.experiments.paths import repo_root


_SAFE_COMPONENT_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")
_SAFE_SAMPLE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")


def targetwise_output_root() -> Path:
    return repo_root() / "causal" / "outputs" / "aba_learning" / "targetwise"


def _safe_component(value: str, *, where: str, sample: bool = False) -> str:
    pattern = _SAFE_SAMPLE_RE if sample else _SAFE_COMPONENT_RE
    if not pattern.fullmatch(value):
        raise ValueError(f"unsafe {where} path component: {value!r}")
    return value


@dataclass(frozen=True)
class TargetCellPaths:
    root: Path

    @property
    def input_dir(self) -> Path:
        return self.root / "input"

    @property
    def output_dir(self) -> Path:
        return self.root / "output"

    @property
    def data_path(self) -> Path:
        return self.input_dir / "data.csv"

    @property
    def bk_path(self) -> Path:
        return self.input_dir / "bk.aba"

    @property
    def examples_path(self) -> Path:
        return self.input_dir / "examples.json"

    @property
    def task_manifest_path(self) -> Path:
        return self.input_dir / "task_manifest.json"

    @property
    def metrics_json_path(self) -> Path:
        return self.root / "metrics.json"

    @property
    def metrics_parquet_path(self) -> Path:
        return self.root / "metrics.parquet"

    @property
    def report_path(self) -> Path:
        return self.root / "report.md"


@dataclass(frozen=True)
class TargetwiseCollectionPaths:
    root: Path
    fixture_id: str
    configuration_id: str
    sample_name: str

    @classmethod
    def for_bundle(
        cls,
        *,
        fixture_id: str,
        configuration_id: str,
        sample_name: str,
        output_root: Path | str | None = None,
    ) -> "TargetwiseCollectionPaths":
        fixture_component = _safe_component(fixture_id, where="fixture identifier")
        configuration_component = _safe_component(
            configuration_id,
            where="configuration identifier",
        )
        sample_component = _safe_component(
            sample_name, where="sample name", sample=True
        )
        root = (
            Path(output_root).resolve()
            if output_root is not None
            else targetwise_output_root()
        )
        return cls(
            root=(
                root / fixture_component / configuration_component / sample_component
            ),
            fixture_id=fixture_component,
            configuration_id=configuration_component,
            sample_name=sample_component,
        )

    @property
    def fixture_root(self) -> Path:
        return self.root.parent.parent

    @property
    def configuration_root(self) -> Path:
        return self.root.parent

    @property
    def configuration_manifest_path(self) -> Path:
        return self.configuration_root / "configuration_manifest.json"

    @property
    def manifest_path(self) -> Path:
        return self.root / "manifest.json"

    @property
    def run_log_path(self) -> Path:
        return self.root / "run.log"

    @property
    def results_path(self) -> Path:
        return self.root / "results.parquet"

    @property
    def summary_markdown_path(self) -> Path:
        return self.root / "summary.md"

    @property
    def summary_json_path(self) -> Path:
        return self.root / "summary.json"

    @property
    def cells_dir(self) -> Path:
        return self.root / "cells"

    def cell(self, target: str) -> TargetCellPaths:
        target_component = _safe_component(target, where="target")
        return TargetCellPaths(self.cells_dir / f"target-{target_component}")
