"""QI-002 minimal truth-table fixtures: 3 motifs x 2 data modes, target ``x2``.

These six deterministic fixtures support the QI-002 minimal baseline (see
``docs/experiments/qualitative/QI-002.md``). Unlike the QI-001 pilot (tiny
hand-picked tables), each fixture here is a *complete factorial* over the two
candidate predictors ``(x0, x1)``, repeated twice, with a noiseless target:

- binary mode: all 4 combinations of ``(x0, x1) in {0,1}^2`` x2 = 8 rows;
- categorical-3 mode: all 9 combinations of ``(x0, x1) in {0,1,2}^2`` x2 = 18 rows.

This is the principled minimum: with the full truth table present, the true
parent is the *unique* zero-error separator of the positive class, and every
non-parent (ancestor or sibling) is provably an imperfect separator. So a
genuine causal rule could be learned *in principle* (it is the only perfect
rule).

Scope: parent-set recovery via ABA Learning, NOT Russo-style Causal ABA. The
motif names describe the data-generating structure encoded in the table.

Orientation note: QI-002 uses the *canonical* orientation only (chain parent
``x1``, fork parent ``x0``). It does NOT break the x0/first-column confound
flagged in QI-001; that is the job of QI-003's parent-position variants. QI-002
documents the confound as a known limitation it does not address.

Encoding contract (enforced by ``causal/argcausaldisco_integration.py``):
- binary mode: ``categorical`` var_type, values exactly ``{0,1}`` -> bare
  predicates ``x0(A) :- A=n.``;
- categorical-3 mode: ``categorical`` var_type, values ``{0,1,2}`` -> value
  predicates ``x0_val_<v>(A)``.

Sample-id convention is 1-based (row index ``i`` -> atom ``x2(i+1)``).

Motif edges (0-based; ``(s, t)`` means ``xs -> xt``) and encoded parents of x2:
- chain    ((0,1),(1,2)) -> parents(x2) = {x1}
- fork     ((0,1),(0,2)) -> parents(x2) = {x0}
- collider ((0,2),(1,2)) -> parents(x2) = {x0, x1}
"""

from __future__ import annotations

import itertools
from collections.abc import Callable

import pandas as pd

from causal.experiments.handcrafted import HandcraftedFixture

_CHAIN_EDGES: tuple[tuple[int, int], ...] = ((0, 1), (1, 2))
_FORK_EDGES: tuple[tuple[int, int], ...] = ((0, 1), (0, 2))
_COLLIDER_EDGES: tuple[tuple[int, int], ...] = ((0, 2), (1, 2))

_CATEGORICAL_TYPES: dict[str, str] = {
    "x0": "categorical",
    "x1": "categorical",
    "x2": "categorical",
}

# Each combination is repeated this many times (>=2 avoids single-row flukes).
_REPEATS = 2


def _x2_examples(
    x2_values: list[int], is_positive: Callable[[int], bool]
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Build fixed (pos, neg) ``x2(id)`` atoms using 1-based sample ids."""
    pos = tuple(f"x2({i + 1})" for i, v in enumerate(x2_values) if is_positive(v))
    neg = tuple(f"x2({i + 1})" for i, v in enumerate(x2_values) if not is_positive(v))
    return pos, neg


def _factorial_columns(values: tuple[int, ...]) -> tuple[list[int], list[int]]:
    """Return (x0, x1) as the complete factorial over ``values``, repeated.

    Combinations are enumerated in lexicographic ``(x0, x1)`` order and then the
    whole block is repeated ``_REPEATS`` times, so every ``(x0, x1)`` pair is
    present an equal number of times.
    """
    combos = list(itertools.product(values, values))
    x0 = [a for a, _ in combos] * _REPEATS
    x1 = [b for _, b in combos] * _REPEATS
    return x0, x1


# --- Binary mode (categorical var_type, values {0,1}, positive: x2 == 1) -----


def _binary_fixture(
    key: str,
    edges: tuple[tuple[int, int], ...],
    x2_fn: Callable[[int, int], int],
) -> HandcraftedFixture:
    x0, x1 = _factorial_columns((0, 1))
    x2 = [x2_fn(a, b) for a, b in zip(x0, x1)]
    pos, neg = _x2_examples(x2, lambda v: v == 1)
    return HandcraftedFixture(
        key=key,
        df=pd.DataFrame({"x0": x0, "x1": x1, "x2": x2}),
        var_types=dict(_CATEGORICAL_TYPES),
        pos_examples=pos,
        neg_examples=neg,
        nodes=3,
        edges=edges,
    )


def qi002_chain_binary() -> HandcraftedFixture:
    """Chain x0->x1->x2 (binary). x2 = x1; x0 is an imperfect ancestor."""
    return _binary_fixture("qi002_chain_binary", _CHAIN_EDGES, lambda a, b: b)


def qi002_fork_binary() -> HandcraftedFixture:
    """Fork x0->x1, x0->x2 (binary). x2 = x0; x1 is an imperfect sibling."""
    return _binary_fixture("qi002_fork_binary", _FORK_EDGES, lambda a, b: a)


def qi002_collider_binary() -> HandcraftedFixture:
    """Collider x0->x2, x1->x2 (binary). x2 = x0 AND x1 (both parents needed)."""
    return _binary_fixture(
        "qi002_collider_binary", _COLLIDER_EDGES, lambda a, b: int(a == 1 and b == 1)
    )


# --- Categorical-3 mode (categorical var_type, values {0,1,2}, positive: x2==2)


def _cat3_fixture(
    key: str,
    edges: tuple[tuple[int, int], ...],
    x2_fn: Callable[[int, int], int],
) -> HandcraftedFixture:
    x0, x1 = _factorial_columns((0, 1, 2))
    x2 = [x2_fn(a, b) for a, b in zip(x0, x1)]
    pos, neg = _x2_examples(x2, lambda v: v == 2)
    return HandcraftedFixture(
        key=key,
        df=pd.DataFrame({"x0": x0, "x1": x1, "x2": x2}),
        var_types=dict(_CATEGORICAL_TYPES),
        pos_examples=pos,
        neg_examples=neg,
        nodes=3,
        edges=edges,
    )


def qi002_chain_cat3() -> HandcraftedFixture:
    """Chain x0->x1->x2 (3-valued). x2 = x1; positive iff x1 == 2."""
    return _cat3_fixture("qi002_chain_cat3", _CHAIN_EDGES, lambda a, b: b)


def qi002_fork_cat3() -> HandcraftedFixture:
    """Fork x0->x1, x0->x2 (3-valued). x2 = x0; positive iff x0 == 2."""
    return _cat3_fixture("qi002_fork_cat3", _FORK_EDGES, lambda a, b: a)


def qi002_collider_cat3() -> HandcraftedFixture:
    """Collider x0->x2, x1->x2 (3-valued). x2 = max(x0, x1); positive iff max == 2."""
    return _cat3_fixture("qi002_collider_cat3", _COLLIDER_EDGES, lambda a, b: max(a, b))


QI002_BUILDERS: dict[str, Callable[[], HandcraftedFixture]] = {
    "qi002_chain_binary": qi002_chain_binary,
    "qi002_fork_binary": qi002_fork_binary,
    "qi002_collider_binary": qi002_collider_binary,
    "qi002_chain_cat3": qi002_chain_cat3,
    "qi002_fork_cat3": qi002_fork_cat3,
    "qi002_collider_cat3": qi002_collider_cat3,
}

# Each fixture id is its own canonical alias.
QI002_ALIASES: dict[str, str] = {key: key for key in QI002_BUILDERS}
