"""Evaluator-only mechanism references for causal-fixture interpretation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from causal.fixtures.analysis import ExactPopulation, fraction_text
from causal.fixtures.artifacts import (
    FIXTURE_TOOLKIT_VERSION,
    file_sha256,
    write_text_once,
)
from causal.fixtures.io import LoadedFixture
from causal.fixtures.model import CausalFixture, StateValue, point_mass_index
from causal.predicate_naming import is_safe_learner_variable_name


def _binary_targetwise_compatible(fixture: CausalFixture) -> bool:
    return all(
        fixture.states_of(variable) == (0, 1)
        and is_safe_learner_variable_name(variable)
        for variable in fixture.variable_names
    )


def _canonical_positive_rule(
    target: str, parent_assignment: tuple[tuple[str, StateValue], ...]
) -> str:
    body = ", ".join(
        f"{parent}_val_{value}(A)" for parent, value in parent_assignment
    )
    return f"{target}(A) :- {body}."


def _sample_count(
    sample: pd.DataFrame | None,
    parent_assignment: tuple[tuple[str, StateValue], ...],
) -> int | None:
    if sample is None:
        return None
    selected = sample
    for parent, value in parent_assignment:
        selected = selected[selected[parent] == value]
    return int(len(selected))


def _root_distribution(fixture: CausalFixture, variable: str) -> list[dict[str, Any]]:
    mechanism = fixture.mechanism_for(variable)
    probabilities = mechanism.rows[0].probabilities
    return [
        {"state": state, "probability": fraction_text(probability)}
        for state, probability in zip(fixture.states_of(variable), probabilities)
    ]


def build_mechanism_reference(
    loaded: LoadedFixture,
    population: ExactPopulation,
    *,
    sample: pd.DataFrame | None = None,
    sample_name: str | None = None,
) -> dict[str, Any]:
    """Build the non-learner-visible rule and support reference for one fixture."""

    fixture = loaded.fixture
    if sample is not None and list(sample.columns) != list(fixture.variable_names):
        raise ValueError("sample columns must equal the fixture variable order")
    if sample is None and sample_name is not None:
        raise ValueError("sample_name requires a sample")

    encoding_compatible = _binary_targetwise_compatible(fixture)
    targets: list[dict[str, Any]] = []
    for variable in fixture.variable_names:
        mechanism = fixture.mechanism_for(variable)
        if not mechanism.parents:
            targets.append(
                {
                    "target": variable,
                    "causal_parents": [],
                    "mechanism_kind": "stochastic_root",
                    "root_distribution": _root_distribution(fixture, variable),
                    "deterministic_truth_table": None,
                    "canonical_positive_rules": {
                        "formal": [],
                        "population_supported": [],
                        "sample_observed": [] if sample is not None else None,
                    },
                    "reference_status": "no_observed_parent_deterministic_rule",
                    "reference_note": (
                        "The generating mechanism is a root distribution, not a "
                        "deterministic rule over other observed variables. Rules learned "
                        "from descendants or other predictors may be predictive without "
                        "representing this root mechanism."
                    ),
                }
            )
            continue

        if not mechanism.deterministic:
            targets.append(
                {
                    "target": variable,
                    "causal_parents": list(mechanism.parents),
                    "mechanism_kind": "stochastic_non_root",
                    "root_distribution": None,
                    "deterministic_truth_table": None,
                    "canonical_positive_rules": {
                        "formal": [],
                        "population_supported": [],
                        "sample_observed": [] if sample is not None else None,
                    },
                    "reference_status": "not_a_deterministic_mechanism",
                    "reference_note": (
                        "No deterministic exact-value rule reference is asserted for "
                        "this stochastic conditional mechanism."
                    ),
                }
            )
            continue

        truth_table: list[dict[str, Any]] = []
        formal_rules: list[str] = []
        population_supported_rules: list[str] = []
        sample_observed_rules: list[str] = []
        for row in mechanism.rows:
            output_index = point_mass_index(row.probabilities)
            if output_index is None:  # pragma: no cover - protected by validation
                raise AssertionError(f"{variable} ceased to be deterministic")
            output = fixture.states_of(variable)[output_index]
            parent_assignment = tuple(row.when)
            population_mass = population.mass(dict(parent_assignment))
            count = _sample_count(sample, parent_assignment)
            rule = None
            if encoding_compatible and output == 1:
                rule = _canonical_positive_rule(variable, parent_assignment)
                formal_rules.append(rule)
                if population_mass > 0:
                    population_supported_rules.append(rule)
                if count is not None and count > 0:
                    sample_observed_rules.append(rule)
            truth_table.append(
                {
                    "when": dict(parent_assignment),
                    "output": output,
                    "population_parent_assignment_probability": fraction_text(
                        population_mass
                    ),
                    "population_supported": population_mass > 0,
                    "sample_count": count,
                    "sample_observed": count > 0 if count is not None else None,
                    "canonical_positive_rule": rule,
                }
            )

        targets.append(
            {
                "target": variable,
                "causal_parents": list(mechanism.parents),
                "mechanism_kind": "deterministic_non_root",
                "root_distribution": None,
                "deterministic_truth_table": truth_table,
                "canonical_positive_rules": {
                    "formal": formal_rules,
                    "population_supported": population_supported_rules,
                    "sample_observed": (
                        sample_observed_rules if sample is not None else None
                    ),
                },
                "reference_status": (
                    "available"
                    if encoding_compatible
                    else "unavailable_for_current_binary_targetwise_encoding"
                ),
                "reference_note": (
                    "Rules are the unsimplified positive-state DNF induced by the "
                    "truth table. Equivalent learned ABA frameworks need not match "
                    "these strings exactly."
                ),
            }
        )

    return {
        "mechanism_reference_schema_version": 1,
        "fixture_toolkit_version": FIXTURE_TOOLKIT_VERSION,
        "generator": {
            "implementation_hash": file_sha256(Path(__file__)),
        },
        "fixture": {
            "id": fixture.fixture_id,
            "schema_version": fixture.schema_version,
            "mechanism_regime": fixture.assumptions.mechanism_regime,
            "source_hash": loaded.source_hash,
            "document_hash": loaded.document_hash,
            "semantic_hash": loaded.semantic_hash,
        },
        "sample": {
            "available": sample is not None,
            "name": sample_name,
            "n": int(len(sample)) if sample is not None else None,
        },
        "encoding_reference": {
            "name": "binary_one_vs_zero_exact_value",
            "compatible": encoding_compatible,
            "positive_state": 1,
            "negative_state": 0,
            "body_predicate_form": "<parent>_val_<state>(A)",
        },
        "targets": targets,
        "boundaries": [
            "this artefact is evaluator-only and must not enter learner BK or examples",
            "formal, population-supported, and finite-sample-observed configurations are distinct",
            "canonical rules describe deterministic positive-state truth-table rows",
            "syntactic rule equality is not an automatic causal-recovery verdict",
            "predictive rules for root targets do not constitute root-mechanism recovery",
            "no learned-rule-to-graph or learned-rule-to-CPDAG decoder is applied",
        ],
    }


def write_mechanism_reference(
    document: dict[str, Any], path: Path | str
) -> Path:
    destination = Path(path)
    write_text_once(
        destination, json.dumps(document, indent=2, sort_keys=True) + "\n"
    )
    return destination
