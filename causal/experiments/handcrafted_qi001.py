"""QI-001 handcrafted fixtures: 3 motifs x 3 data modes, target ``x2``.

These nine deterministic fixtures support the QI-001 qualitative parent-set
recovery investigation (see ``docs/experiments/qualitative/QI-001.md``). Each
fixture is a small, fully specified table with fixed positive/negative examples
targeting ``x2`` only. They are consumed via ``graph_type: handcrafted_table``,
which uses the fixture's own examples and ``var_types`` directly (no median
split, no var-type overwrite).

This is parent-set recovery via ABA Learning, NOT Russo-style Causal ABA: the
motif names describe the data-generating structure encoded in the table, not an
ABA causal encoding (no arr/noe/indep, no d-separation, no stable extensions).

Encoding contract (enforced by ``causal/argcausaldisco_integration.py``):
- binary mode: ``var_types`` ``categorical`` with values exactly ``{0,1}`` per
  non-target column -> bare predicates ``x0(A) :- A=n.``;
- categorical-3 mode: ``var_types`` ``categorical`` with values including
  ``{0,1,2}`` per non-target column -> value predicates ``x0_val_<v>(A)``;
- continuous mode: ``var_types`` ``continuous`` -> binned predicates
  ``x0_bin<k>(A)`` (the grid runs these with ``bins=3``, ``bin_strategy=uniform``).

No fixture uses ``var_type="binary"`` (that string would route to continuous
binning in the BK generator).

Sample-id convention is 1-based (matches the legacy fixtures and the BK
generator's ``sample_id = idx + 1``): row index ``i`` maps to atom ``x2(i+1)``.

Motif edges (0-based; ``(s, t)`` means ``xs -> xt``) and encoded parents of x2:
- chain    ((0,1),(1,2)) -> parents(x2) = {x1}
- fork     ((0,1),(0,2)) -> parents(x2) = {x0}
- collider ((0,2),(1,2)) -> parents(x2) = {x0, x1}
"""

from __future__ import annotations

from collections.abc import Callable

import pandas as pd

from causal.experiments.handcrafted import HandcraftedFixture

_CHAIN_EDGES: tuple[tuple[int, int], ...] = ((0, 1), (1, 2))
_FORK_EDGES: tuple[tuple[int, int], ...] = ((0, 1), (0, 2))
_COLLIDER_EDGES: tuple[tuple[int, int], ...] = ((0, 2), (1, 2))

_CATEGORICAL_TYPES: dict[str, str] = {"x0": "categorical", "x1": "categorical", "x2": "categorical"}
_CONTINUOUS_TYPES: dict[str, str] = {"x0": "continuous", "x1": "continuous", "x2": "continuous"}


def _x2_examples(
    x2_values: list[float], is_positive: Callable[[float], bool]
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Build fixed (pos, neg) ``x2(id)`` atoms using 1-based sample ids."""
    pos = tuple(f"x2({i + 1})" for i, v in enumerate(x2_values) if is_positive(v))
    neg = tuple(f"x2({i + 1})" for i, v in enumerate(x2_values) if not is_positive(v))
    return pos, neg


# --- Binary mode (categorical var_type, values {0,1}, positive: x2 == 1) ----


def qi001_chain_binary() -> HandcraftedFixture:
    """Chain x0->x1->x2. x2 tracks x1; x0 decorrelated from x2."""
    data = {
        "x0": [0, 1, 0, 1],
        "x1": [0, 1, 1, 0],
        "x2": [0, 1, 1, 0],
    }
    pos, neg = _x2_examples(data["x2"], lambda v: v == 1)
    return HandcraftedFixture(
        key="qi001_chain_binary",
        df=pd.DataFrame(data),
        var_types=dict(_CATEGORICAL_TYPES),
        pos_examples=pos,
        neg_examples=neg,
        nodes=3,
        edges=_CHAIN_EDGES,
    )


def qi001_fork_binary() -> HandcraftedFixture:
    """Fork x0->x1, x0->x2. x2 tracks x0; x1 decorrelated from x2."""
    data = {
        "x0": [0, 1, 0, 1],
        "x1": [0, 1, 1, 0],
        "x2": [0, 1, 0, 1],
    }
    pos, neg = _x2_examples(data["x2"], lambda v: v == 1)
    return HandcraftedFixture(
        key="qi001_fork_binary",
        df=pd.DataFrame(data),
        var_types=dict(_CATEGORICAL_TYPES),
        pos_examples=pos,
        neg_examples=neg,
        nodes=3,
        edges=_FORK_EDGES,
    )


def qi001_collider_binary() -> HandcraftedFixture:
    """Collider x0->x2, x1->x2. x2 = x0 OR x1 (both parents matter)."""
    data = {
        "x0": [0, 0, 1, 1],
        "x1": [0, 1, 0, 1],
        "x2": [0, 1, 1, 1],
    }
    pos, neg = _x2_examples(data["x2"], lambda v: v == 1)
    return HandcraftedFixture(
        key="qi001_collider_binary",
        df=pd.DataFrame(data),
        var_types=dict(_CATEGORICAL_TYPES),
        pos_examples=pos,
        neg_examples=neg,
        nodes=3,
        edges=_COLLIDER_EDGES,
    )


# --- Categorical-3 mode (categorical var_type, values {0,1,2}, positive: x2 == 2)


def qi001_chain_cat3() -> HandcraftedFixture:
    """Chain x0->x1->x2 with 3-valued columns. x2 tracks x1."""
    data = {
        "x0": [0, 1, 2, 0],
        "x1": [0, 1, 2, 2],
        "x2": [0, 1, 2, 2],
    }
    pos, neg = _x2_examples(data["x2"], lambda v: v == 2)
    return HandcraftedFixture(
        key="qi001_chain_cat3",
        df=pd.DataFrame(data),
        var_types=dict(_CATEGORICAL_TYPES),
        pos_examples=pos,
        neg_examples=neg,
        nodes=3,
        edges=_CHAIN_EDGES,
    )


def qi001_fork_cat3() -> HandcraftedFixture:
    """Fork x0->x1, x0->x2 with 3-valued columns. x2 tracks x0."""
    data = {
        "x0": [0, 1, 2, 2],
        "x1": [0, 1, 2, 0],
        "x2": [0, 1, 2, 2],
    }
    pos, neg = _x2_examples(data["x2"], lambda v: v == 2)
    return HandcraftedFixture(
        key="qi001_fork_cat3",
        df=pd.DataFrame(data),
        var_types=dict(_CATEGORICAL_TYPES),
        pos_examples=pos,
        neg_examples=neg,
        nodes=3,
        edges=_FORK_EDGES,
    )


def qi001_collider_cat3() -> HandcraftedFixture:
    """Collider x0->x2, x1->x2 with 3-valued columns. x2 = max(x0, x1)."""
    data = {
        "x0": [0, 1, 0, 2, 1],
        "x1": [0, 0, 2, 1, 1],
        "x2": [0, 1, 2, 2, 1],
    }
    pos, neg = _x2_examples(data["x2"], lambda v: v == 2)
    return HandcraftedFixture(
        key="qi001_collider_cat3",
        df=pd.DataFrame(data),
        var_types=dict(_CATEGORICAL_TYPES),
        pos_examples=pos,
        neg_examples=neg,
        nodes=3,
        edges=_COLLIDER_EDGES,
    )


# --- Continuous mode (continuous var_type, float values, positive: x2 >= 0.0) -
# Threshold rule: a row is positive iff x2 >= 0.0. Examples are hard-coded from
# this rule (NOT a later median split). x0/x1 span [-2, 2] so 3 uniform bins are
# each exercised.

_CONT_THRESHOLD = 0.0


def qi001_chain_cont3() -> HandcraftedFixture:
    """Chain x0->x1->x2 (continuous). x2 follows x1's sign; positive iff x2 >= 0."""
    data = {
        "x0": [-2.0, -1.0, 0.0, 1.0, 2.0],
        "x1": [-2.0, -1.0, 0.0, 1.0, 2.0],
        "x2": [-1.5, -0.5, 0.5, 1.0, 2.0],
    }
    pos, neg = _x2_examples(data["x2"], lambda v: v >= _CONT_THRESHOLD)
    return HandcraftedFixture(
        key="qi001_chain_cont3",
        df=pd.DataFrame(data),
        var_types=dict(_CONTINUOUS_TYPES),
        pos_examples=pos,
        neg_examples=neg,
        nodes=3,
        edges=_CHAIN_EDGES,
    )


def qi001_fork_cont3() -> HandcraftedFixture:
    """Fork x0->x1, x0->x2 (continuous). x2 follows x0; x1 anti-correlated."""
    data = {
        "x0": [-2.0, -1.0, 0.0, 1.0, 2.0],
        "x1": [2.0, 1.0, 0.0, -1.0, -2.0],
        "x2": [-1.5, -0.5, 0.2, 1.0, 1.8],
    }
    pos, neg = _x2_examples(data["x2"], lambda v: v >= _CONT_THRESHOLD)
    return HandcraftedFixture(
        key="qi001_fork_cont3",
        df=pd.DataFrame(data),
        var_types=dict(_CONTINUOUS_TYPES),
        pos_examples=pos,
        neg_examples=neg,
        nodes=3,
        edges=_FORK_EDGES,
    )


def qi001_collider_cont3() -> HandcraftedFixture:
    """Collider x0->x2, x1->x2 (continuous). x2 = x0 + x1; positive iff x2 >= 0."""
    data = {
        "x0": [-2.0, -1.0, 0.0, 1.0, 2.0],
        "x1": [-1.0, 1.0, -2.0, 2.0, 0.0],
        "x2": [-3.0, 0.0, -2.0, 3.0, 2.0],
    }
    pos, neg = _x2_examples(data["x2"], lambda v: v >= _CONT_THRESHOLD)
    return HandcraftedFixture(
        key="qi001_collider_cont3",
        df=pd.DataFrame(data),
        var_types=dict(_CONTINUOUS_TYPES),
        pos_examples=pos,
        neg_examples=neg,
        nodes=3,
        edges=_COLLIDER_EDGES,
    )


QI001_BUILDERS: dict[str, Callable[[], HandcraftedFixture]] = {
    "qi001_chain_binary": qi001_chain_binary,
    "qi001_fork_binary": qi001_fork_binary,
    "qi001_collider_binary": qi001_collider_binary,
    "qi001_chain_cat3": qi001_chain_cat3,
    "qi001_fork_cat3": qi001_fork_cat3,
    "qi001_collider_cat3": qi001_collider_cat3,
    "qi001_chain_cont3": qi001_chain_cont3,
    "qi001_fork_cont3": qi001_fork_cont3,
    "qi001_collider_cont3": qi001_collider_cont3,
}

# Each fixture id is its own canonical alias.
QI001_ALIASES: dict[str, str] = {key: key for key in QI001_BUILDERS}
