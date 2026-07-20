"""Expanded M1.2 (M12x) fixtures U1–U7 from mechanism cards.

Design: ``docs/research/milestone_plans/milestone1_part2/mechanism_cards/``.
Regime: alphabet {0,1,2}; full source factorial (U5/U7: curated multi-row support);
nonzero-positive labels (E+ = t != 0). BK is ``val``-only: M12x YAML sets
``defaults.definitional_nz: false`` (no definitional ``*_nz`` predicates).

Pilot fixtures in ``handcrafted_m12.py`` are left unchanged.
"""

from __future__ import annotations

import itertools
from collections.abc import Callable, Mapping

import pandas as pd

from causal.experiments.handcrafted import ExamplesPair, HandcraftedFixture

_VALUES: tuple[int, ...] = (0, 1, 2)

_CAT3: dict[str, str] = {
    "x0": "categorical",
    "x1": "categorical",
    "x2": "categorical",
}

_CAT4: dict[str, str] = {
    "x0": "categorical",
    "x1": "categorical",
    "x2": "categorical",
    "x3": "categorical",
}


def _nonzero_examples(target: str, values: list[int]) -> ExamplesPair:
    """E+ = target != 0; E- = target == 0; 1-based sample ids."""
    pos = tuple(f"{target}({i + 1})" for i, v in enumerate(values) if v != 0)
    neg = tuple(f"{target}({i + 1})" for i, v in enumerate(values) if v == 0)
    return pos, neg


def _examples_map(
    columns: Mapping[str, list[int]], targets: tuple[str, ...]
) -> dict[str, ExamplesPair]:
    return {t: _nonzero_examples(t, list(columns[t])) for t in targets}


def _fixture(
    *,
    key: str,
    df: pd.DataFrame,
    var_types: dict[str, str],
    nodes: int,
    edges: tuple[tuple[int, int], ...],
    learning_targets: tuple[str, ...],
) -> HandcraftedFixture:
    cols = {c: df[c].astype(int).tolist() for c in df.columns}
    by_target = _examples_map(cols, learning_targets)
    default = learning_targets[0]
    pos, neg = by_target[default]
    return HandcraftedFixture(
        key=key,
        df=df,
        var_types=var_types,
        pos_examples=pos,
        neg_examples=neg,
        nodes=nodes,
        edges=edges,
        default_target=default,
        learning_targets=learning_targets,
        examples_by_target=by_target,
    )


def m12_u1_separator_copy() -> HandcraftedFixture:
    """U1: x1 -> x2; x0 isolated; x2 := copy(x1)."""
    combos = list(itertools.product(_VALUES, _VALUES))
    x0 = [a for a, _ in combos]
    x1 = [b for _, b in combos]
    x2 = list(x1)
    return _fixture(
        key="m12_u1_separator_copy",
        df=pd.DataFrame({"x0": x0, "x1": x1, "x2": x2}),
        var_types=dict(_CAT3),
        nodes=3,
        edges=((1, 2),),
        learning_targets=("x2",),
    )


def m12_u2_collider_min() -> HandcraftedFixture:
    """U2: collider; x2 := min(x0, x1)."""
    combos = list(itertools.product(_VALUES, _VALUES))
    x0 = [a for a, _ in combos]
    x1 = [b for _, b in combos]
    x2 = [min(a, b) for a, b in zip(x0, x1)]
    return _fixture(
        key="m12_u2_collider_min",
        df=pd.DataFrame({"x0": x0, "x1": x1, "x2": x2}),
        var_types=dict(_CAT3),
        nodes=3,
        edges=((0, 2), (1, 2)),
        learning_targets=("x2",),
    )


def m12_u3_collider_max() -> HandcraftedFixture:
    """U3: collider; x2 := max(x0, x1)."""
    combos = list(itertools.product(_VALUES, _VALUES))
    x0 = [a for a, _ in combos]
    x1 = [b for _, b in combos]
    x2 = [max(a, b) for a, b in zip(x0, x1)]
    return _fixture(
        key="m12_u3_collider_max",
        df=pd.DataFrame({"x0": x0, "x1": x1, "x2": x2}),
        var_types=dict(_CAT3),
        nodes=3,
        edges=((0, 2), (1, 2)),
        learning_targets=("x2",),
    )


def m12_u4_fork_double_copy() -> HandcraftedFixture:
    """U4: fork; x1 := 2 if x0 != 2 else 0; x2 := 2 if x0 != 0 else 0."""
    x0 = list(_VALUES)
    x1 = [2 if v != 2 else 0 for v in x0]
    x2 = [2 if v != 0 else 0 for v in x0]
    return _fixture(
        key="m12_u4_fork_double_copy",
        df=pd.DataFrame({"x0": x0, "x1": x1, "x2": x2}),
        var_types=dict(_CAT3),
        nodes=3,
        edges=((0, 1), (0, 2)),
        learning_targets=("x1", "x2"),
    )


# Pilot m12_chain support: for each x0, pairs (x0, x0) and (x0, (x0+1)%3); x2 := x1.
_U5_CHAIN_X0_X1: tuple[tuple[int, int], ...] = (
    (0, 0),
    (0, 1),
    (1, 1),
    (1, 2),
    (2, 2),
    (2, 0),
)


def m12_u5_chain_double_copy() -> HandcraftedFixture:
    """U5: chain; pilot (x0,x1) support; x2 := copy(x1)."""
    x0 = [a for a, _ in _U5_CHAIN_X0_X1]
    x1 = [b for _, b in _U5_CHAIN_X0_X1]
    x2 = list(x1)
    return _fixture(
        key="m12_u5_chain_double_copy",
        df=pd.DataFrame({"x0": x0, "x1": x1, "x2": x2}),
        var_types=dict(_CAT3),
        nodes=3,
        edges=((0, 1), (1, 2)),
        learning_targets=("x1", "x2"),
    )


def m12_u6_g1_and_cone() -> HandcraftedFixture:
    """U6: G1; x2 := min(x0,x1), x3 := x1 - x2."""
    combos = list(itertools.product(_VALUES, _VALUES))
    x0 = [a for a, _ in combos]
    x1 = [b for _, b in combos]
    x2 = [min(a, b) for a, b in zip(x0, x1)]
    x3 = [b - c for b, c in zip(x1, x2)]
    return _fixture(
        key="m12_u6_g1_and_cone",
        df=pd.DataFrame({"x0": x0, "x1": x1, "x2": x2, "x3": x3}),
        var_types=dict(_CAT4),
        nodes=4,
        edges=((0, 2), (1, 2), (1, 3), (2, 3)),
        learning_targets=("x2", "x3"),
    )


def m12_u7_g1_or_cone() -> HandcraftedFixture:
    """U7: diamond; noisy fork arms; x3 := |x1 - x2|."""
    x0: list[int] = []
    x1: list[int] = []
    x2: list[int] = []
    for a in _VALUES:
        b = (a + 1) % 3
        # differ then collapse
        for c in ((a + 2) % 3, b):
            x0.append(a)
            x1.append(b)
            x2.append(c)
    x3 = [abs(b - c) for b, c in zip(x1, x2)]
    return _fixture(
        key="m12_u7_g1_or_cone",
        df=pd.DataFrame({"x0": x0, "x1": x1, "x2": x2, "x3": x3}),
        var_types=dict(_CAT4),
        nodes=4,
        edges=((0, 1), (0, 2), (1, 3), (2, 3)),
        learning_targets=("x3",),
    )


M12X_BUILDERS: dict[str, Callable[[], HandcraftedFixture]] = {
    "m12_u1_separator_copy": m12_u1_separator_copy,
    "m12_u2_collider_min": m12_u2_collider_min,
    "m12_u3_collider_max": m12_u3_collider_max,
    "m12_u4_fork_double_copy": m12_u4_fork_double_copy,
    "m12_u5_chain_double_copy": m12_u5_chain_double_copy,
    "m12_u6_g1_and_cone": m12_u6_g1_and_cone,
    "m12_u7_g1_or_cone": m12_u7_g1_or_cone,
}

M12X_ALIASES: dict[str, str] = {key: key for key in M12X_BUILDERS}

# Unit id → fixture key (for docs / tests).
M12X_UNIT_TO_KEY: dict[str, str] = {
    "U1": "m12_u1_separator_copy",
    "U2": "m12_u2_collider_min",
    "U3": "m12_u3_collider_max",
    "U4": "m12_u4_fork_double_copy",
    "U5": "m12_u5_chain_double_copy",
    "U6": "m12_u6_g1_and_cone",
    "U7": "m12_u7_g1_or_cone",
}
