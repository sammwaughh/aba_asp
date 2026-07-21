"""M13-C1 comparison for causal-role underdetermination.

The paired cells in each arm have different external graphs but identical
learner-visible inputs.  This script verifies those invariants, compares the
normalised learned delta, and reports graph-relative interpretations separately
from learner-output equality.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from causal.experiments.handcrafted import load_handcrafted
from causal.experiments.paths import grid_root
from causal.metrics import parse_delta_rules, target_rule_filter

ARMS: tuple[str, ...] = (
    "M13_c1_role_equivalence_ecai2024",
    "M13_c1_role_equivalence_aamas2025",
)
MODELS: tuple[str, ...] = ("m13_c1_parent_x0", "m13_c1_parent_x1")
TARGET = "x2"
PARENTS: dict[str, frozenset[str]] = {
    "m13_c1_parent_x0": frozenset({"x0"}),
    "m13_c1_parent_x1": frozenset({"x1"}),
}
HSTAR: dict[str, frozenset[str]] = {
    "m13_c1_parent_x0": frozenset(
        {"x2(A):-x0_val_1(A)", "x2(A):-x0_val_2(A)"}
    ),
    "m13_c1_parent_x1": frozenset(
        {"x2(A):-x1_val_1(A)", "x2(A):-x1_val_2(A)"}
    ),
}
_BASE_VAR_RE = re.compile(r"\b(x\d+)_(?:val_\d+|bin\d+)\b")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _normalise_rule(rule: str) -> str:
    """Canonicalise harmless whitespace and final punctuation."""
    return "".join(rule.strip().rstrip(".").split())


def _normalised_delta(sol_path: Path) -> tuple[str, ...]:
    return tuple(sorted(_normalise_rule(rule) for rule in parse_delta_rules(sol_path)))


def _body_vars(rules: tuple[str, ...]) -> frozenset[str]:
    variables: set[str] = set()
    for rule in rules:
        if ":-" not in rule:
            continue
        variables.update(_BASE_VAR_RE.findall(rule.split(":-", 1)[1]))
    return frozenset(variables)


def _classification(body_vars: frozenset[str], parents: frozenset[str]) -> str:
    if body_vars == parents:
        return "parent_only"
    if parents < body_vars:
        return "parent_plus_sibling"
    if body_vars and body_vars.isdisjoint(parents):
        return "non_parent_only"
    if not body_vars:
        return "no_data_variable"
    return "partial_parent"


def _yes_no(value: bool) -> str:
    return "yes" if value else "no"


@dataclass(frozen=True)
class CellEvidence:
    arm: str
    model: str
    true_parent: str
    data_sha256: str
    bk_sha256: str
    positive_examples: tuple[str, ...]
    negative_examples: tuple[str, ...]
    outcome: str
    asp_positive_coverage: float
    asp_negative_rejection: float
    normalised_delta: tuple[str, ...]
    target_rules: tuple[str, ...]
    target_body_variables: tuple[str, ...]
    n_assumptions: int
    n_contraries: int
    exact_hstar: bool
    graph_relative_classification: str
    body_parent_precision: float
    body_parent_recall: float
    variable_parent_precision: float
    variable_parent_recall: float
    clean_recovery: bool


@dataclass(frozen=True)
class ArmComparison:
    arm: str
    data_identical: bool
    bk_identical: bool
    examples_identical: bool
    delta_identical: bool
    coverage_identical: bool
    learner_visible_task_identical: bool
    learned_framework_identical: bool


def _cell_dir(arm: str, model: str) -> Path:
    return grid_root() / arm / "cells" / f"{model}__target-{TARGET}"


def _read_cell(arm: str, model: str) -> CellEvidence:
    cell_dir = _cell_dir(arm, model)
    data_path = cell_dir / "data.csv"
    bk_path = cell_dir / "bk.aba"
    sol_path = cell_dir / "bk.sol.aba"
    metrics_path = cell_dir / "metrics.json"
    for path in (data_path, bk_path, sol_path, metrics_path):
        if not path.is_file():
            raise FileNotFoundError(path)

    fixture = load_handcrafted(model)
    positive, negative = fixture.examples_for_target(TARGET)
    metrics: dict[str, Any] = json.loads(metrics_path.read_text(encoding="utf-8"))
    delta = _normalised_delta(sol_path)
    target_rules = tuple(
        sorted(
            _normalise_rule(rule)
            for rule in target_rule_filter(TARGET, parse_delta_rules(sol_path))
        )
    )
    body_vars = _body_vars(target_rules)
    parents = PARENTS[model]

    return CellEvidence(
        arm=arm,
        model=model,
        true_parent=next(iter(parents)),
        data_sha256=_sha256(data_path),
        bk_sha256=_sha256(bk_path),
        positive_examples=positive,
        negative_examples=negative,
        outcome=str(metrics["outcome"]),
        asp_positive_coverage=float(metrics["cov_asp_pos"]),
        asp_negative_rejection=float(metrics["cov_asp_neg"]),
        normalised_delta=delta,
        target_rules=target_rules,
        target_body_variables=tuple(sorted(body_vars)),
        n_assumptions=int(metrics["n_assumptions"]),
        n_contraries=int(metrics["n_contraries"]),
        exact_hstar=frozenset(target_rules) == HSTAR[model],
        graph_relative_classification=_classification(body_vars, parents),
        body_parent_precision=float(metrics["body_parent_precision"]),
        body_parent_recall=float(metrics["body_parent_recall"]),
        variable_parent_precision=float(metrics["var_parent_precision"]),
        variable_parent_recall=float(metrics["var_parent_recall"]),
        clean_recovery=bool(metrics["clean_recovery"]),
    )


def _compare_arm(cells: tuple[CellEvidence, CellEvidence]) -> ArmComparison:
    left, right = cells
    data_identical = left.data_sha256 == right.data_sha256
    bk_identical = left.bk_sha256 == right.bk_sha256
    examples_identical = (
        left.positive_examples == right.positive_examples
        and left.negative_examples == right.negative_examples
    )
    delta_identical = left.normalised_delta == right.normalised_delta
    coverage_identical = (
        left.outcome == right.outcome
        and left.asp_positive_coverage == right.asp_positive_coverage
        and left.asp_negative_rejection == right.asp_negative_rejection
    )
    comparison = ArmComparison(
        arm=left.arm,
        data_identical=data_identical,
        bk_identical=bk_identical,
        examples_identical=examples_identical,
        delta_identical=delta_identical,
        coverage_identical=coverage_identical,
        learner_visible_task_identical=(
            data_identical and bk_identical and examples_identical
        ),
        learned_framework_identical=delta_identical,
    )
    if not comparison.learner_visible_task_identical:
        raise AssertionError(f"{left.arm}: learner-visible task differs across models")
    if not comparison.learned_framework_identical:
        raise AssertionError(f"{left.arm}: normalised learned delta differs across models")
    if not comparison.coverage_identical:
        raise AssertionError(f"{left.arm}: outcome or ASP coverage differs across models")
    return comparison


def _render_markdown(
    cells: list[CellEvidence],
    comparisons: list[ArmComparison],
) -> str:
    lines = [
        "# M13-C1 — Causal-role underdetermination summary",
        "",
        "The paired cells in each arm differ only in their external causal graph.",
        "Learner-visible inputs and normalised learned deltas are compared separately",
        "from graph-relative parent evaluation.",
        "",
        "## Pair invariants",
        "",
        "| Arm | Data identical | BK identical | Examples identical | Delta identical | Coverage identical |",
        "|---|:---:|:---:|:---:|:---:|:---:|",
    ]
    for comparison in comparisons:
        lines.append(
            "| "
            + " | ".join(
                (
                    comparison.arm,
                    _yes_no(comparison.data_identical),
                    _yes_no(comparison.bk_identical),
                    _yes_no(comparison.examples_identical),
                    _yes_no(comparison.delta_identical),
                    _yes_no(comparison.coverage_identical),
                )
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Graph-relative cell results",
            "",
            "| Arm | Model | Parent | Body variables | Classification | Exact H* | Var P | Var R | Clean | ASP pos | ASP neg | Assumptions | Contraries |",
            "|---|---|---|---|---|:---:|---:|---:|:---:|---:|---:|---:|---:|",
        ]
    )
    for cell in cells:
        body_vars = ", ".join(cell.target_body_variables) or "—"
        lines.append(
            "| "
            + " | ".join(
                (
                    cell.arm,
                    cell.model,
                    cell.true_parent,
                    body_vars,
                    cell.graph_relative_classification,
                    "yes" if cell.exact_hstar else "no",
                    f"{cell.variable_parent_precision:.3f}",
                    f"{cell.variable_parent_recall:.3f}",
                    _yes_no(cell.clean_recovery),
                    f"{cell.asp_positive_coverage:.3f}",
                    f"{cell.asp_negative_rejection:.3f}",
                    str(cell.n_assumptions),
                    str(cell.n_contraries),
                )
            )
            + " |"
        )

    lines.extend(["", "## Learned target rules", ""])
    for cell in cells:
        lines.append(f"### {cell.arm} × {cell.model}")
        lines.append("")
        lines.append("```prolog")
        lines.extend(rule + "." for rule in cell.target_rules)
        lines.append("```")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    cells: list[CellEvidence] = []
    comparisons: list[ArmComparison] = []
    for arm in ARMS:
        arm_cells = tuple(_read_cell(arm, model) for model in MODELS)
        cells.extend(arm_cells)
        comparisons.append(_compare_arm(arm_cells))

    payload = {
        "experiment_id": "M13-C1",
        "cells": [asdict(cell) for cell in cells],
        "comparisons": [asdict(comparison) for comparison in comparisons],
    }
    root = grid_root()
    json_path = root / "M13_c1_role_equivalence_summary.json"
    md_path = root / "M13_c1_role_equivalence_summary.md"
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(_render_markdown(cells, comparisons), encoding="utf-8")
    print(f"wrote {md_path}")
    print(f"wrote {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
