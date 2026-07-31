"""Shared naming rules for learner-visible causal predicates."""

from __future__ import annotations

import re
from typing import Iterable


_SAFE_LOWERCASE_ATOM_RE = re.compile(r"^[a-z][a-z0-9_]*$")
_BODY_FUNCTOR_RE = re.compile(r"\b([a-z][a-z0-9_]*)\s*\(")

# These names belong to the ABA representation or the learner's fresh-symbol
# namespace. Prolog distinguishes predicates by name and arity, but rejecting
# them as causal-variable identifiers avoids collisions and misleading traces.
_RESERVED_EXACT_NAMES = frozenset(
    {
        "assumption",
        "contrary",
        "not",
        "alpha",
        "c_alpha",
    }
)
_RESERVED_PREFIXES = ("alpha_", "c_alpha_")


def learner_variable_name_error(name: str) -> str | None:
    """Return why ``name`` is unsafe as a learner-visible variable, if anything."""

    if not _SAFE_LOWERCASE_ATOM_RE.fullmatch(name):
        return (
            "must be a lowercase Prolog atom beginning with a letter and containing "
            "only lowercase letters, digits, or underscores"
        )
    if name in _RESERVED_EXACT_NAMES or name.startswith(_RESERVED_PREFIXES):
        return "uses a name reserved for ABA assumptions, contraries, or negation"
    return None


def is_safe_learner_variable_name(name: str) -> bool:
    """Whether ``name`` is safe for direct use as an ABA/Prolog predicate."""

    return learner_variable_name_error(name) is None


def exact_value_body_variables(
    text: str,
    declared_variables: Iterable[str],
) -> frozenset[str]:
    """Extract declared causal variables from exact-value body predicates.

    Target-wise fixtures encode a variable ``a`` using predicates such as
    ``a_val_0/1`` and ``a_val_1/1``. Matching against the fixture's declared
    variable names keeps learner-generated ``alpha_N`` and ``c_alpha_N`` symbols
    outside the causal-variable diagnostic and avoids the legacy ``xN`` parser.
    """

    functors = {match.group(1) for match in _BODY_FUNCTOR_RE.finditer(text)}
    variables = tuple(declared_variables)
    variable_set = set(variables)
    found: set[str] = set()
    for functor in functors:
        if functor in variable_set:
            found.add(functor)
            continue
        candidates = [
            variable
            for variable in variables
            if functor.startswith(f"{variable}_val_")
        ]
        if candidates:
            # Prefer the most specific declared prefix, e.g. ``a_val`` over
            # ``a`` for the generated functor ``a_val_val_1``.
            found.add(max(candidates, key=len))
    return frozenset(found)
