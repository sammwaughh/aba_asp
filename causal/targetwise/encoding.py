"""Exact-value binary ABA task construction from one frozen sample."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any

from causal.targetwise.bundle import LoadedCausalFixtureBundle


class TargetwiseEncodingError(ValueError):
    """Raised when a fixture sample cannot use the requested encoding policy."""


_PREDICATE_RE = re.compile(r"^x[0-9]+$")


@dataclass(frozen=True)
class BinaryTargetTask:
    """One learner-visible binary task for a selected target variable."""

    target: str
    predictor_order: tuple[str, ...]
    positive_examples: tuple[str, ...]
    negative_examples: tuple[str, ...]
    bk_text: str
    feature_clause_count: int

    @property
    def n_positive(self) -> int:
        return len(self.positive_examples)

    @property
    def n_negative(self) -> int:
        return len(self.negative_examples)

    def examples_document(self) -> dict[str, Any]:
        return {
            "examples_schema_version": 1,
            "target": self.target,
            "encoding": "exact_value",
            "example_policy": "binary_one_vs_zero",
            "positive_value": 1,
            "negative_value": 0,
            "positive_examples": list(self.positive_examples),
            "negative_examples": list(self.negative_examples),
            "n_positive": self.n_positive,
            "n_negative": self.n_negative,
        }


def _validate_binary_bundle(bundle: LoadedCausalFixtureBundle) -> None:
    for variable in bundle.variables:
        if tuple(bundle.state_orders[variable]) != (0, 1):
            raise TargetwiseEncodingError(
                "binary_one_vs_zero requires declared state order [0, 1] for "
                f"every variable; {variable} has {bundle.state_orders[variable]!r}"
            )
        observed = set(bundle.dataframe[variable].tolist())
        if not observed <= {0, 1}:
            raise TargetwiseEncodingError(
                f"{variable} contains values outside the binary domain: {observed!r}"
            )
        if not _PREDICATE_RE.fullmatch(variable):
            raise TargetwiseEncodingError(
                "the initial target-wise metrics contract requires variable names "
                f"of the form xN; got {variable!r}"
            )


def build_binary_target_task(
    bundle: LoadedCausalFixtureBundle,
    target: str,
) -> BinaryTargetTask:
    """Build exact-value BK and 1-vs-0 examples for one target."""

    _validate_binary_bundle(bundle)
    if target not in bundle.variables:
        raise TargetwiseEncodingError(
            f"unknown target {target!r}; expected one of {bundle.variables!r}"
        )

    predictor_order = tuple(
        variable for variable in bundle.variables if variable != target
    )
    positive_examples: list[str] = []
    negative_examples: list[str] = []
    target_values = bundle.dataframe[target].tolist()
    for row_number, raw_value in enumerate(target_values, start=1):
        value = int(raw_value)
        atom = f"{target}({row_number})"
        if value == 1:
            positive_examples.append(atom)
        elif value == 0:
            negative_examples.append(atom)
        else:  # guarded above, retained as a local invariant
            raise TargetwiseEncodingError(
                f"unexpected target value {raw_value!r} for {target}"
            )

    lines: list[str] = [
        "% Exact-value binary background knowledge",
        f"% Learning target excluded from BK: {target}",
        "% Row identifiers are one-based CSV data-row numbers.",
        "",
    ]
    feature_clause_count = 0
    for predictor in predictor_order:
        lines.append(f"% Predictor block: {predictor}")
        for row_number, raw_value in enumerate(
            bundle.dataframe[predictor].tolist(), start=1
        ):
            value = int(raw_value)
            lines.append(f"{predictor}_val_{value}(A) :- A={row_number}.")
            feature_clause_count += 1
        lines.append("")

    expected_clause_count = bundle.n * (len(bundle.variables) - 1)
    if feature_clause_count != expected_clause_count:
        raise AssertionError(
            f"exact-value encoder produced {feature_clause_count} clauses; "
            f"expected {expected_clause_count}"
        )

    return BinaryTargetTask(
        target=target,
        predictor_order=predictor_order,
        positive_examples=tuple(positive_examples),
        negative_examples=tuple(negative_examples),
        bk_text="\n".join(lines).rstrip() + "\n",
        feature_clause_count=feature_clause_count,
    )
