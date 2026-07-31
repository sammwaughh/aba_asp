from __future__ import annotations

import pytest

from causal.predicate_naming import (
    exact_value_body_variables,
    is_safe_learner_variable_name,
    learner_variable_name_error,
)


@pytest.mark.parametrize("name", ["a", "b", "c", "d", "x0", "node_12"])
def test_safe_lowercase_variable_names(name: str) -> None:
    assert is_safe_learner_variable_name(name)
    assert learner_variable_name_error(name) is None


@pytest.mark.parametrize(
    "name",
    [
        "A",
        "a-b",
        "0a",
        "alpha",
        "alpha_1",
        "c_alpha",
        "c_alpha_1",
        "assumption",
        "contrary",
        "not",
    ],
)
def test_unsafe_or_reserved_variable_names(name: str) -> None:
    assert not is_safe_learner_variable_name(name)
    assert learner_variable_name_error(name)


def test_exact_value_body_variables_use_declared_fixture_names() -> None:
    text = (
        "alpha_1(A), a_val_1(A), b_val_0(A), c_alpha_2(A), "
        "x0_val_1(A)"
    )

    assert exact_value_body_variables(text, ("a", "b", "c")) == frozenset(
        {"a", "b"}
    )
    assert exact_value_body_variables(text, ("x0", "x1")) == frozenset({"x0"})
    assert exact_value_body_variables(
        "a_val_val_1(A)", ("a", "a_val")
    ) == frozenset({"a_val"})
