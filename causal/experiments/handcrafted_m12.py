"""M1.2 divergence-designed categorical fixtures (Milestone 1, Part 2).

Five minimal handcrafted categorical fixture families supporting the M1.2
published-configuration comparison (ASP-ABAlearnB / RASP-ABAlearn / Greedy ABA
Learning), planned in
``docs/research/milestone_plans/milestone1_part2/milestone1_part2_config_comparison.md``
and recorded in ``docs/experiments/qualitative/M1.2-config-comparison.md``.

Every fixture declares its intended graph G (directed edges over ``x0..x{n-1}``)
and mechanism here, in machine-readable ``edges`` metadata, and in the run
config/record (the plan's "three places" rule). All fixtures are **coherent**
tables (no duplicated feature rows with conflicting labels); the minimally
incoherent families (``m12_incoh_pos`` / ``m12_incoh_neg``) are deferred
follow-ups, NOT part of this module (plan Section 4.1).

Families (0-based edge ``(s, t)`` means ``xs -> xt``):

- ``m12_sep`` — separator anchor. G: ``x1 -> x2``; ``x0`` isolated.
  Complete factorial over ``(x0, x1) in {0,1,2}^2`` (9 rows); ``x2 := x1``;
  positive class ``x2 == 2``. Expected: ``x2(A) :- x1_val_2(A).``
- ``m12_conj`` — conjunctive mechanism on a collider. G: ``x0 -> x3``,
  ``x1 -> x3``; ``x2`` isolated. Complete factorial over
  ``(x0, x1, x2) in {0,1,2}^3`` (27 rows); ``x3 := min(x0, x1)``; positive
  class ``x3 == 2`` (iff ``x0 == 2 and x1 == 2``). ``min`` mirrors QI-002's
  collider ``max`` convention and keeps a 3-valued target column. Expected:
  ``x3(A) :- x0_val_2(A), x1_val_2(A).`` — no single value literal separates.
- ``m12_disj`` — disjunctive mechanism on a collider. G: ``x0 -> x3``,
  ``x1 -> x3``; ``x2`` isolated (symmetric twin of ``m12_conj`` — same
  topology, row count, and BK shape; differs only in mechanism). Complete
  factorial over ``(x0, x1, x2) in {0,1,2}^3`` (27 rows);
  ``x3 := max(x0, x1)``; positive class ``x3 == 2`` (iff ``x0 == 2 or
  x1 == 2``; 15 pos / 12 neg). Expected: the two-rule set
  ``x3(A) :- x0_val_2(A).`` and ``x3(A) :- x1_val_2(A).``
- ``m12_fork`` — fork with a correlated sibling. G: ``x0 -> x1``,
  ``x0 -> x2``. Both children are DETERMINISTIC functions of ``x0`` with
  different mechanisms (Samuel's design, decision recorded in the M1.2
  record): ``x1 := 2 if x0 == 1 else 0`` and ``x2 := 2 if x0 == 2 else 0``.
  Three distinct assignments ``(x0, x1, x2)`` = (0,0,0), (1,2,0), (2,0,2),
  each repeated 3x in block order = 9 rows. NOT a complete factorial: the
  edge ``x0 -> x1`` is represented in the data (``x1`` is associated with
  ``x2`` through the shared cause but is not a zero-error separator; only
  ``x0`` is). ``x1`` takes exactly two values {0, 2}: a deterministic child
  of a 3-valued cause that is an imperfect separator cannot be injective.
  The label 2 (not 1) is used so ``x1``'s value set is not exactly {0, 1},
  keeping it on the ``x1_val_v`` value-predicate encoding path (the BK
  writer encodes value-set-{0,1} columns as bare binary predicates).
  Expected: ``x2(A) :- x0_val_2(A).``
- ``m12_chain`` — correlated ancestor. G: ``x0 -> x1 -> x2``. Non-factorial:
  per ``x0`` block of 3 rows, ``x1 := x0`` twice plus one cyclic deviation
  ``x1 := (x0 + 1) % 3``; ``x2 := x1``; positive class ``x2 == 2`` (9 rows).
  ``x1`` is the unique zero-error separator; the ancestor ``x0`` is strictly
  associated with ``x2`` (P(pos | x0) = 0, 1/3, 2/3) but imperfect. Expected:
  ``x2(A) :- x1_val_2(A).`` — failure mode of interest: ancestor citation.

Encoding contract (enforced by ``causal/argcausaldisco_integration.py``): all
columns are ``categorical``; no predictor column has value set exactly {0, 1},
so every predictor is serialised as value predicates ``xi_val_v(A)``. The
target column is excluded from the feature BK; E+/E- are fixed target atoms
with 1-based sample ids (row ``i`` -> atom ``t(i+1)``).

Scope: recovery of mechanism-aligned rules via unguided ABA Learning, NOT
Russo-style Causal ABA (no arr/noe/indep, d-separation, or
stable-extension-as-DAG machinery).
"""

from __future__ import annotations

import itertools
from collections.abc import Callable

import pandas as pd

from causal.experiments.handcrafted import HandcraftedFixture

_CATEGORICAL_3: dict[str, str] = {
    "x0": "categorical",
    "x1": "categorical",
    "x2": "categorical",
}

_CATEGORICAL_4: dict[str, str] = {
    "x0": "categorical",
    "x1": "categorical",
    "x2": "categorical",
    "x3": "categorical",
}

_VALUES: tuple[int, ...] = (0, 1, 2)


def _examples(
    target: str, target_values: list[int], positive_value: int
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Build fixed (pos, neg) ``target(id)`` atoms using 1-based sample ids."""
    pos = tuple(
        f"{target}({i + 1})" for i, v in enumerate(target_values) if v == positive_value
    )
    neg = tuple(
        f"{target}({i + 1})" for i, v in enumerate(target_values) if v != positive_value
    )
    return pos, neg


def m12_sep() -> HandcraftedFixture:
    """Separator anchor. G: x1 -> x2; x0 isolated. x2 := x1; positive x2 == 2."""
    combos = list(itertools.product(_VALUES, _VALUES))
    x0 = [a for a, _ in combos]
    x1 = [b for _, b in combos]
    x2 = list(x1)
    pos, neg = _examples("x2", x2, 2)
    return HandcraftedFixture(
        key="m12_sep",
        df=pd.DataFrame({"x0": x0, "x1": x1, "x2": x2}),
        var_types=dict(_CATEGORICAL_3),
        pos_examples=pos,
        neg_examples=neg,
        nodes=3,
        edges=((1, 2),),
    )


def m12_conj() -> HandcraftedFixture:
    """Conjunctive collider. G: x0 -> x3, x1 -> x3; x2 isolated. x3 := min(x0, x1)."""
    combos = list(itertools.product(_VALUES, _VALUES, _VALUES))
    x0 = [a for a, _, _ in combos]
    x1 = [b for _, b, _ in combos]
    x2 = [c for _, _, c in combos]
    x3 = [min(a, b) for a, b in zip(x0, x1)]
    pos, neg = _examples("x3", x3, 2)
    return HandcraftedFixture(
        key="m12_conj",
        df=pd.DataFrame({"x0": x0, "x1": x1, "x2": x2, "x3": x3}),
        var_types=dict(_CATEGORICAL_4),
        pos_examples=pos,
        neg_examples=neg,
        nodes=4,
        edges=((0, 3), (1, 3)),
        default_target="x3",
    )


def m12_disj() -> HandcraftedFixture:
    """Disjunctive collider. G: x0 -> x3, x1 -> x3; x2 isolated. x3 := max(x0, x1)."""
    combos = list(itertools.product(_VALUES, _VALUES, _VALUES))
    x0 = [a for a, _, _ in combos]
    x1 = [b for _, b, _ in combos]
    x2 = [c for _, _, c in combos]
    x3 = [max(a, b) for a, b in zip(x0, x1)]
    pos, neg = _examples("x3", x3, 2)
    return HandcraftedFixture(
        key="m12_disj",
        df=pd.DataFrame({"x0": x0, "x1": x1, "x2": x2, "x3": x3}),
        var_types=dict(_CATEGORICAL_4),
        pos_examples=pos,
        neg_examples=neg,
        nodes=4,
        edges=((0, 3), (1, 3)),
        default_target="x3",
    )


# Fork: three distinct deterministic assignments (x0, x1, x2), each repeated
# _FORK_REPEATS times in block order. x1 := 2 if x0 == 1 else 0 (values {0, 2},
# deliberately avoiding the bare-binary {0, 1} encoding path);
# x2 := 2 if x0 == 2 else 0.
_FORK_ASSIGNMENTS: tuple[tuple[int, int, int], ...] = (
    (0, 0, 0),
    (1, 2, 0),
    (2, 0, 2),
)
_FORK_REPEATS = 3


def m12_fork() -> HandcraftedFixture:
    """Fork with correlated sibling. G: x0 -> x1, x0 -> x2 (both deterministic)."""
    rows = [a for a in _FORK_ASSIGNMENTS for _ in range(_FORK_REPEATS)]
    x0 = [r[0] for r in rows]
    x1 = [r[1] for r in rows]
    x2 = [r[2] for r in rows]
    pos, neg = _examples("x2", x2, 2)
    return HandcraftedFixture(
        key="m12_fork",
        df=pd.DataFrame({"x0": x0, "x1": x1, "x2": x2}),
        var_types=dict(_CATEGORICAL_3),
        pos_examples=pos,
        neg_examples=neg,
        nodes=3,
        edges=((0, 1), (0, 2)),
    )


# Chain: per x0 block of 3 rows, x1 := x0 twice + one cyclic deviation
# x1 := (x0 + 1) % 3; x2 := x1. The (x0, x1) rows, in fixed order:
_CHAIN_X0_X1: tuple[tuple[int, int], ...] = (
    (0, 0),
    (0, 0),
    (0, 1),
    (1, 1),
    (1, 1),
    (1, 2),
    (2, 2),
    (2, 2),
    (2, 0),
)


def m12_chain() -> HandcraftedFixture:
    """Correlated ancestor chain. G: x0 -> x1 -> x2. x2 := x1; x0 imperfect."""
    x0 = [a for a, _ in _CHAIN_X0_X1]
    x1 = [b for _, b in _CHAIN_X0_X1]
    x2 = list(x1)
    pos, neg = _examples("x2", x2, 2)
    return HandcraftedFixture(
        key="m12_chain",
        df=pd.DataFrame({"x0": x0, "x1": x1, "x2": x2}),
        var_types=dict(_CATEGORICAL_3),
        pos_examples=pos,
        neg_examples=neg,
        nodes=3,
        edges=((0, 1), (1, 2)),
    )


M12_BUILDERS: dict[str, Callable[[], HandcraftedFixture]] = {
    "m12_sep": m12_sep,
    "m12_conj": m12_conj,
    "m12_disj": m12_disj,
    "m12_fork": m12_fork,
    "m12_chain": m12_chain,
}

# Each fixture id is its own canonical alias.
M12_ALIASES: dict[str, str] = {key: key for key in M12_BUILDERS}
