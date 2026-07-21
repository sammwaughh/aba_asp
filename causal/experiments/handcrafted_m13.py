"""M1.3 (M13) targeted qualitative fixtures.

M13-C1 is a causal-role-underdetermination control.  Its two fixtures describe
different valid causal models over the same ordered table:

* ``m13_c1_parent_x0``: x0 is the direct parent of target x2;
* ``m13_c1_parent_x1``: x1 is the direct parent of target x2.

The learner-visible components (table, column order, target, E+/E-, and hence
generated BK) are deliberately identical.  Only the external edge metadata
used for graph-relative evaluation differs.

M13-C2 reuses the locked U2, U5, and U7 named data while permuting complete
non-target feature blocks.  Graphs, row identifiers, targets, examples, and BK
rule sets remain fixed; only predictor presentation order changes.
"""

from __future__ import annotations

from collections.abc import Callable

import pandas as pd

from causal.experiments.handcrafted import HandcraftedFixture
from causal.experiments.handcrafted_m12x import (
    m12_u2_collider_min,
    m12_u5_chain_curated,
    m12_u7_diamond_noisy,
)

_VAR_TYPES: dict[str, str] = {
    "x0": "categorical",
    "x1": "categorical",
    "x2": "categorical",
}

_POS_EXAMPLES: tuple[str, ...] = ("x2(2)", "x2(3)")
_NEG_EXAMPLES: tuple[str, ...] = ("x2(1)",)


def _shared_copy_table() -> pd.DataFrame:
    """Return the input-equivalent table shared by both causal models."""
    values = [0, 1, 2]
    return pd.DataFrame({"x0": values, "x1": values, "x2": values})


def _role_fixture(
    *,
    key: str,
    edges: tuple[tuple[int, int], ...],
) -> HandcraftedFixture:
    return HandcraftedFixture(
        key=key,
        df=_shared_copy_table(),
        var_types=dict(_VAR_TYPES),
        pos_examples=_POS_EXAMPLES,
        neg_examples=_NEG_EXAMPLES,
        nodes=3,
        edges=edges,
        default_target="x2",
        learning_targets=("x2",),
        examples_by_target={"x2": (_POS_EXAMPLES, _NEG_EXAMPLES)},
    )


def m13_c1_parent_x0() -> HandcraftedFixture:
    """G0: x0 is the common cause and direct parent of x2."""
    return _role_fixture(
        key="m13_c1_parent_x0",
        edges=((0, 1), (0, 2)),
    )


def m13_c1_parent_x1() -> HandcraftedFixture:
    """G1: x1 is the common cause and direct parent of x2."""
    return _role_fixture(
        key="m13_c1_parent_x1",
        edges=((1, 0), (1, 2)),
    )


def _order_fixture(
    *,
    key: str,
    base: HandcraftedFixture,
    predictor_order: tuple[str, ...],
    target: str,
) -> HandcraftedFixture:
    expected_predictors = set(base.df.columns) - {target}
    if set(predictor_order) != expected_predictors:
        raise ValueError(
            f"{key}: predictor_order={predictor_order!r} does not match "
            f"{sorted(expected_predictors)!r}"
        )
    ordered_columns = (*predictor_order, target)
    positive, negative = base.examples_for_target(target)
    return HandcraftedFixture(
        key=key,
        df=base.df.loc[:, ordered_columns].copy(),
        var_types={column: base.var_types[column] for column in ordered_columns},
        pos_examples=positive,
        neg_examples=negative,
        nodes=base.nodes,
        edges=base.edges,
        default_target=target,
        learning_targets=(target,),
        examples_by_target={target: (positive, negative)},
    )


def m13_c2_u2_x0_x1() -> HandcraftedFixture:
    """U2 control with the locked x0-before-x1 predictor order."""
    return _order_fixture(
        key="m13_c2_u2_x0_x1",
        base=m12_u2_collider_min(),
        predictor_order=("x0", "x1"),
        target="x2",
    )


def m13_c2_u2_x1_x0() -> HandcraftedFixture:
    """U2 control with the two parent feature blocks reversed."""
    return _order_fixture(
        key="m13_c2_u2_x1_x0",
        base=m12_u2_collider_min(),
        predictor_order=("x1", "x0"),
        target="x2",
    )


def m13_c2_u5_x0_x1() -> HandcraftedFixture:
    """U5 control with non-parent ancestor x0 before parent x1."""
    return _order_fixture(
        key="m13_c2_u5_x0_x1",
        base=m12_u5_chain_curated(),
        predictor_order=("x0", "x1"),
        target="x2",
    )


def m13_c2_u5_x1_x0() -> HandcraftedFixture:
    """U5 control with direct parent x1 before ancestor x0."""
    return _order_fixture(
        key="m13_c2_u5_x1_x0",
        base=m12_u5_chain_curated(),
        predictor_order=("x1", "x0"),
        target="x2",
    )


def m13_c2_u7_x0_x1_x2() -> HandcraftedFixture:
    """U7 order x0, x1, x2 (locked M12x baseline)."""
    return _order_fixture(
        key="m13_c2_u7_x0_x1_x2",
        base=m12_u7_diamond_noisy(),
        predictor_order=("x0", "x1", "x2"),
        target="x3",
    )


def m13_c2_u7_x0_x2_x1() -> HandcraftedFixture:
    """U7 order x0, x2, x1."""
    return _order_fixture(
        key="m13_c2_u7_x0_x2_x1",
        base=m12_u7_diamond_noisy(),
        predictor_order=("x0", "x2", "x1"),
        target="x3",
    )


def m13_c2_u7_x1_x0_x2() -> HandcraftedFixture:
    """U7 order x1, x0, x2."""
    return _order_fixture(
        key="m13_c2_u7_x1_x0_x2",
        base=m12_u7_diamond_noisy(),
        predictor_order=("x1", "x0", "x2"),
        target="x3",
    )


def m13_c2_u7_x1_x2_x0() -> HandcraftedFixture:
    """U7 order x1, x2, x0."""
    return _order_fixture(
        key="m13_c2_u7_x1_x2_x0",
        base=m12_u7_diamond_noisy(),
        predictor_order=("x1", "x2", "x0"),
        target="x3",
    )


def m13_c2_u7_x2_x0_x1() -> HandcraftedFixture:
    """U7 order x2, x0, x1."""
    return _order_fixture(
        key="m13_c2_u7_x2_x0_x1",
        base=m12_u7_diamond_noisy(),
        predictor_order=("x2", "x0", "x1"),
        target="x3",
    )


def m13_c2_u7_x2_x1_x0() -> HandcraftedFixture:
    """U7 order x2, x1, x0."""
    return _order_fixture(
        key="m13_c2_u7_x2_x1_x0",
        base=m12_u7_diamond_noisy(),
        predictor_order=("x2", "x1", "x0"),
        target="x3",
    )


M13_BUILDERS: dict[str, Callable[[], HandcraftedFixture]] = {
    "m13_c1_parent_x0": m13_c1_parent_x0,
    "m13_c1_parent_x1": m13_c1_parent_x1,
    "m13_c2_u2_x0_x1": m13_c2_u2_x0_x1,
    "m13_c2_u2_x1_x0": m13_c2_u2_x1_x0,
    "m13_c2_u5_x0_x1": m13_c2_u5_x0_x1,
    "m13_c2_u5_x1_x0": m13_c2_u5_x1_x0,
    "m13_c2_u7_x0_x1_x2": m13_c2_u7_x0_x1_x2,
    "m13_c2_u7_x0_x2_x1": m13_c2_u7_x0_x2_x1,
    "m13_c2_u7_x1_x0_x2": m13_c2_u7_x1_x0_x2,
    "m13_c2_u7_x1_x2_x0": m13_c2_u7_x1_x2_x0,
    "m13_c2_u7_x2_x0_x1": m13_c2_u7_x2_x0_x1,
    "m13_c2_u7_x2_x1_x0": m13_c2_u7_x2_x1_x0,
}

M13_ALIASES: dict[str, str] = {key: key for key in M13_BUILDERS}
