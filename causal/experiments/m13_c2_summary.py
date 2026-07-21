"""M13-C2 comparison of ECAI/AAMAS sensitivity to BK block order."""

from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from causal.experiments.handcrafted import load_handcrafted
from causal.experiments.paths import grid_root
from causal.metrics import parse_delta_rules, target_rule_filter

ARMS: tuple[str, ...] = (
    "M13_c2_bk_order_ecai2024",
    "M13_c2_bk_order_aamas2025",
)
ORDER_BY_SOURCE: dict[str, tuple[str, ...]] = {
    "m13_c2_u2_x0_x1": ("x0", "x1"),
    "m13_c2_u2_x1_x0": ("x1", "x0"),
    "m13_c2_u5_x0_x1": ("x0", "x1"),
    "m13_c2_u5_x1_x0": ("x1", "x0"),
    "m13_c2_u7_x0_x1_x2": ("x0", "x1", "x2"),
    "m13_c2_u7_x0_x2_x1": ("x0", "x2", "x1"),
    "m13_c2_u7_x1_x0_x2": ("x1", "x0", "x2"),
    "m13_c2_u7_x1_x2_x0": ("x1", "x2", "x0"),
    "m13_c2_u7_x2_x0_x1": ("x2", "x0", "x1"),
    "m13_c2_u7_x2_x1_x0": ("x2", "x1", "x0"),
}
FAMILY_BY_SOURCE: dict[str, str] = {
    source: family
    for family, sources in {
        "u2": ("m13_c2_u2_x0_x1", "m13_c2_u2_x1_x0"),
        "u5": ("m13_c2_u5_x0_x1", "m13_c2_u5_x1_x0"),
        "u7": (
            "m13_c2_u7_x0_x1_x2",
            "m13_c2_u7_x0_x2_x1",
            "m13_c2_u7_x1_x0_x2",
            "m13_c2_u7_x1_x2_x0",
            "m13_c2_u7_x2_x0_x1",
            "m13_c2_u7_x2_x1_x0",
        ),
    }.items()
    for source in sources
}
SOURCES: tuple[str, ...] = tuple(ORDER_BY_SOURCE)
TARGET_BY_FAMILY = {"u2": "x2", "u5": "x2", "u7": "x3"}
PARENTS_BY_FAMILY: dict[str, frozenset[str]] = {
    "u2": frozenset({"x0", "x1"}),
    "u5": frozenset({"x1"}),
    "u7": frozenset({"x1", "x2"}),
}
HSTAR_BY_FAMILY: dict[str, frozenset[str]] = {
    "u2": frozenset(
        {
            "x2(A):-x0_val_1(A),x1_val_1(A)",
            "x2(A):-x0_val_1(A),x1_val_2(A)",
            "x2(A):-x0_val_2(A),x1_val_1(A)",
            "x2(A):-x0_val_2(A),x1_val_2(A)",
        }
    ),
    "u5": frozenset(
        {
            "x2(A):-x1_val_1(A)",
            "x2(A):-x1_val_2(A)",
        }
    ),
    "u7": frozenset(
        {
            "x3(A):-x1_val_0(A),x2_val_1(A)",
            "x3(A):-x1_val_1(A),x2_val_2(A)",
            "x3(A):-x1_val_2(A),x2_val_0(A)",
        }
    ),
}
_BASE_VAR_RE = re.compile(r"\b(x\d+)_(?:val_\d+|bin\d+)\b")
_FIRST_FOLD_RE = re.compile(
    r"folding \[A=\d+[^\]]*\] with (?:\d+:\s*)?(x\d+)_(?:val_\d+|bin\d+)"
)


def _sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _normalise_rule(rule: str) -> str:
    return "".join(rule.strip().rstrip(".").split())


def _normalised_delta(sol_path: Path) -> tuple[str, ...]:
    return tuple(sorted(_normalise_rule(rule) for rule in parse_delta_rules(sol_path)))


def _variables(rules: tuple[str, ...]) -> tuple[str, ...]:
    variables: set[str] = set()
    for rule in rules:
        variables.update(_BASE_VAR_RE.findall(rule))
    return tuple(sorted(variables))


def _canonical_data_hash(path: Path) -> str:
    df = pd.read_csv(path)
    canonical = df.loc[:, sorted(df.columns)].to_csv(index=False).encode("utf-8")
    return _sha256_bytes(canonical)


def _bk_rule_set_hash(path: Path) -> str:
    rules = sorted(
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("%")
    )
    return _sha256_bytes(("\n".join(rules) + "\n").encode("utf-8"))


def _first_fold_variable(trace: str) -> str | None:
    match = _FIRST_FOLD_RE.search(trace)
    return match.group(1) if match else None


def _body_classification(
    body_variables: tuple[str, ...],
    parents: frozenset[str],
) -> str:
    body = frozenset(body_variables)
    if body == parents:
        return "parent_only"
    if parents < body:
        return "parent_superset"
    if body and body <= parents:
        return "parent_subset"
    if body.isdisjoint(parents):
        return "non_parent_only"
    return "mixed_partial_parent"


@dataclass(frozen=True)
class CellEvidence:
    arm: str
    source: str
    family: str
    target: str
    feature_order: tuple[str, ...]
    parents: tuple[str, ...]
    canonical_data_sha256: str
    bk_rule_set_sha256: str
    positive_examples: tuple[str, ...]
    negative_examples: tuple[str, ...]
    outcome: str
    first_fold_variable: str | None
    normalised_delta: tuple[str, ...]
    target_rules: tuple[str, ...]
    target_body_variables: tuple[str, ...]
    framework_variables: tuple[str, ...]
    body_classification: str
    exact_hstar: bool
    n_assumptions: int
    n_contraries: int
    asp_positive_coverage: float
    asp_negative_rejection: float
    variable_parent_precision: float
    variable_parent_recall: float
    clean_recovery: bool


@dataclass(frozen=True)
class FamilyComparison:
    arm: str
    family: str
    variants: int
    logical_inputs_equivalent: bool
    unique_delta_count: int
    delta_invariant: bool
    coverage_invariant: bool
    first_fold_variables: tuple[str, ...]
    body_scopes: tuple[str, ...]
    framework_scopes: tuple[str, ...]


def _cell_dir(arm: str, source: str, target: str) -> Path:
    return grid_root() / arm / "cells" / f"{source}__target-{target}"


def _read_cell(arm: str, source: str) -> CellEvidence:
    family = FAMILY_BY_SOURCE[source]
    target = TARGET_BY_FAMILY[family]
    cell_dir = _cell_dir(arm, source, target)
    data_path = cell_dir / "data.csv"
    bk_path = cell_dir / "bk.aba"
    sol_path = cell_dir / "bk.sol.aba"
    metrics_path = cell_dir / "metrics.json"
    trace_path = cell_dir / "prolog.stdout"
    for path in (data_path, bk_path, sol_path, metrics_path, trace_path):
        if not path.is_file():
            raise FileNotFoundError(path)

    fixture = load_handcrafted(source)
    positive, negative = fixture.examples_for_target(target)
    metrics: dict[str, Any] = json.loads(metrics_path.read_text(encoding="utf-8"))
    delta = _normalised_delta(sol_path)
    target_rules = tuple(
        sorted(
            _normalise_rule(rule)
            for rule in target_rule_filter(target, parse_delta_rules(sol_path))
        )
    )
    body_variables = _variables(target_rules)
    framework_variables = _variables(delta)
    parents = PARENTS_BY_FAMILY[family]
    return CellEvidence(
        arm=arm,
        source=source,
        family=family,
        target=target,
        feature_order=ORDER_BY_SOURCE[source],
        parents=tuple(sorted(parents)),
        canonical_data_sha256=_canonical_data_hash(data_path),
        bk_rule_set_sha256=_bk_rule_set_hash(bk_path),
        positive_examples=positive,
        negative_examples=negative,
        outcome=str(metrics["outcome"]),
        first_fold_variable=_first_fold_variable(
            trace_path.read_text(encoding="utf-8")
        ),
        normalised_delta=delta,
        target_rules=target_rules,
        target_body_variables=body_variables,
        framework_variables=framework_variables,
        body_classification=_body_classification(body_variables, parents),
        exact_hstar=frozenset(target_rules) == HSTAR_BY_FAMILY[family],
        n_assumptions=int(metrics["n_assumptions"]),
        n_contraries=int(metrics["n_contraries"]),
        asp_positive_coverage=float(metrics["cov_asp_pos"]),
        asp_negative_rejection=float(metrics["cov_asp_neg"]),
        variable_parent_precision=float(metrics["var_parent_precision"]),
        variable_parent_recall=float(metrics["var_parent_recall"]),
        clean_recovery=bool(metrics["clean_recovery"]),
    )


def _compare_family(
    arm: str,
    family: str,
    cells: list[CellEvidence],
) -> FamilyComparison:
    input_signatures = {
        (
            cell.canonical_data_sha256,
            cell.bk_rule_set_sha256,
            cell.positive_examples,
            cell.negative_examples,
        )
        for cell in cells
    }
    deltas = {cell.normalised_delta for cell in cells}
    coverage = {
        (cell.outcome, cell.asp_positive_coverage, cell.asp_negative_rejection)
        for cell in cells
    }
    comparison = FamilyComparison(
        arm=arm,
        family=family,
        variants=len(cells),
        logical_inputs_equivalent=len(input_signatures) == 1,
        unique_delta_count=len(deltas),
        delta_invariant=len(deltas) == 1,
        coverage_invariant=len(coverage) == 1,
        first_fold_variables=tuple(
            cell.first_fold_variable or "none" for cell in cells
        ),
        body_scopes=tuple(",".join(cell.target_body_variables) for cell in cells),
        framework_scopes=tuple(",".join(cell.framework_variables) for cell in cells),
    )
    if not comparison.logical_inputs_equivalent:
        raise AssertionError(f"{arm}/{family}: logical inputs differ beyond block order")
    return comparison


def _yes_no(value: bool) -> str:
    return "yes" if value else "no"


def _render_markdown(
    cells: list[CellEvidence],
    comparisons: list[FamilyComparison],
) -> str:
    lines = [
        "# M13-C2 — BK feature-block order summary",
        "",
        "Within each family, named data, graph, target, examples, and BK rule sets",
        "are fixed. Only complete predictor-block order changes.",
        "",
        "## Family comparisons",
        "",
        "| Arm | Family | Variants | Inputs equivalent | Unique deltas | Delta invariant | Coverage invariant | First folds |",
        "|---|---|---:|:---:|---:|:---:|:---:|---|",
    ]
    for comparison in comparisons:
        lines.append(
            "| "
            + " | ".join(
                (
                    comparison.arm,
                    comparison.family,
                    str(comparison.variants),
                    _yes_no(comparison.logical_inputs_equivalent),
                    str(comparison.unique_delta_count),
                    _yes_no(comparison.delta_invariant),
                    _yes_no(comparison.coverage_invariant),
                    ", ".join(comparison.first_fold_variables),
                )
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Cell results",
            "",
            "| Arm | Family | Order | First fold | Body vars | Framework vars | Class | Exact H* | Assumptions | Contraries | ASP pos | ASP neg | Clean |",
            "|---|---|---|---|---|---|---|:---:|---:|---:|---:|---:|:---:|",
        ]
    )
    for cell in cells:
        lines.append(
            "| "
            + " | ".join(
                (
                    cell.arm,
                    cell.family,
                    "→".join(cell.feature_order),
                    cell.first_fold_variable or "—",
                    ",".join(cell.target_body_variables) or "—",
                    ",".join(cell.framework_variables) or "—",
                    cell.body_classification,
                    _yes_no(cell.exact_hstar),
                    str(cell.n_assumptions),
                    str(cell.n_contraries),
                    f"{cell.asp_positive_coverage:.3f}",
                    f"{cell.asp_negative_rejection:.3f}",
                    _yes_no(cell.clean_recovery),
                )
            )
            + " |"
        )

    lines.extend(["", "## Unique learned target-rule sets", ""])
    grouped: dict[tuple[str, str, tuple[str, ...]], list[CellEvidence]] = defaultdict(
        list
    )
    for cell in cells:
        grouped[(cell.arm, cell.family, cell.target_rules)].append(cell)
    for (arm, family, rules), members in grouped.items():
        orders = ", ".join("→".join(cell.feature_order) for cell in members)
        lines.append(f"### {arm} × {family} ({orders})")
        lines.append("")
        lines.append("```prolog")
        lines.extend(rule + "." for rule in rules)
        lines.append("```")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    cells = [_read_cell(arm, source) for arm in ARMS for source in SOURCES]
    comparisons: list[FamilyComparison] = []
    for arm in ARMS:
        for family in ("u2", "u5", "u7"):
            family_cells = [
                cell for cell in cells if cell.arm == arm and cell.family == family
            ]
            comparisons.append(_compare_family(arm, family, family_cells))

    payload = {
        "experiment_id": "M13-C2",
        "cells": [asdict(cell) for cell in cells],
        "comparisons": [asdict(comparison) for comparison in comparisons],
    }
    root = grid_root()
    json_path = root / "M13_c2_bk_order_summary.json"
    md_path = root / "M13_c2_bk_order_summary.md"
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(_render_markdown(cells, comparisons), encoding="utf-8")
    print(f"wrote {md_path}")
    print(f"wrote {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
