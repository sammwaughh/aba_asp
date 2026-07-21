"""M1.3 (M13) targeted qualitative fixtures.

M13-C1 is a causal-role-underdetermination control.  Its two fixtures describe
different valid causal models over the same ordered table:

* ``m13_c1_parent_x0``: x0 is the direct parent of target x2;
* ``m13_c1_parent_x1``: x1 is the direct parent of target x2.

The learner-visible components (table, column order, target, E+/E-, and hence
generated BK) are deliberately identical.  Only the external edge metadata
used for graph-relative evaluation differs.
"""

from __future__ import annotations

from collections.abc import Callable

import pandas as pd

from causal.experiments.handcrafted import HandcraftedFixture

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


M13_BUILDERS: dict[str, Callable[[], HandcraftedFixture]] = {
    "m13_c1_parent_x0": m13_c1_parent_x0,
    "m13_c1_parent_x1": m13_c1_parent_x1,
}

M13_ALIASES: dict[str, str] = {key: key for key in M13_BUILDERS}
