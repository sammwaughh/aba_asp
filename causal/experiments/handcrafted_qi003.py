"""QI-003 scaled noisy fixtures: 5 structural configs x 3 data modes, target ``x2``.

These fifteen deterministic fixtures support the QI-003 scaled run (see
``docs/experiments/qualitative/QI-003.md``). Each fixture is an ``n=100`` table
generated programmatically from a motif mechanism with mild stochastic noise, so
the data look realistic (not degenerate) and every learner gets a fair chance to
recover the causal parent of ``x2``.

Two things distinguish QI-003 from the QI-001 pilot and the QI-002 baseline:

1. Scale + noise: ``n=100`` with noisy edges (chain intermediate flip, fork
   sibling noise, target noise). Determinism comes from a fixed per-fixture RNG
   seed (the ``handcrafted_table`` path ignores ``cell.seed``).

2. Parent-position controls (breaks the QI-001 x0/first-column confound):
   for the chain and fork motifs we generate BOTH orientations, placing the true
   direct parent of ``x2`` in ``x0`` for some fixtures and in ``x1`` for others.
   A learner that simply prefers ``x0`` will therefore FAIL the ``*_x1parent``
   fixtures, separating "prefers the true parent" from "prefers x0".

Scope: parent-set recovery via ABA Learning, NOT Russo-style Causal ABA.

Encoding contract (enforced by ``causal/argcausaldisco_integration.py``):
- binary mode: ``categorical`` var_type, values ``{0,1}`` -> bare predicates;
- categorical-3 mode: ``categorical`` var_type, values ``{0,1,2}`` -> ``_val_``;
- continuous mode: ``continuous`` var_type -> ``_bin`` predicates (run with
  ``bins=3``, ``bin_strategy=uniform``).

Sample-id convention is 1-based (row index ``i`` -> atom ``x2(i+1)``).

Parent-position tracking (0-based edges ``(s,t)`` mean ``xs -> xt``):
- qi003_chain_x1parent : x0=root, x1=parent  -> edges ((0,1),(1,2)), parents={x1}
- qi003_chain_x0parent : x1=root, x0=parent  -> edges ((1,0),(0,2)), parents={x0}
- qi003_fork_x0parent  : x0=cause, x1=sibling-> edges ((0,1),(0,2)), parents={x0}
- qi003_fork_x1parent  : x1=cause, x0=sibling-> edges ((1,0),(1,2)), parents={x1}
- qi003_collider       : x0,x1 both parents  -> edges ((0,2),(1,2)), parents={x0,x1}
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np
import pandas as pd

from causal.experiments.handcrafted import HandcraftedFixture

_N = 100

_CATEGORICAL_TYPES: dict[str, str] = {
    "x0": "categorical",
    "x1": "categorical",
    "x2": "categorical",
}
_CONTINUOUS_TYPES: dict[str, str] = {
    "x0": "continuous",
    "x1": "continuous",
    "x2": "continuous",
}

# Noise levels (kept mild so the causal parent stays the best predictor).
_CHAIN_FLIP = 0.2  # root -> intermediate disagreement (breaks collinearity)
_FORK_SIB_NOISE = 0.2  # cause -> sibling disagreement
_TARGET_NOISE = 0.1  # parent -> x2 disagreement


def _x2_examples(
    x2_values: list[float], is_positive: Callable[[float], bool]
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Build fixed (pos, neg) ``x2(id)`` atoms using 1-based sample ids."""
    pos = tuple(f"x2({i + 1})" for i, v in enumerate(x2_values) if is_positive(v))
    neg = tuple(f"x2({i + 1})" for i, v in enumerate(x2_values) if not is_positive(v))
    return pos, neg


def _flip_binary(arr: np.ndarray, p: float, rng: np.random.RandomState) -> np.ndarray:
    mask = rng.rand(len(arr)) < p
    out = arr.copy()
    out[mask] = 1 - out[mask]
    return out


def _flip_cat3(arr: np.ndarray, p: float, rng: np.random.RandomState) -> np.ndarray:
    """Reassign a fraction of entries to a *different* value in {0,1,2}."""
    mask = rng.rand(len(arr)) < p
    out = arr.copy()
    deltas = rng.randint(1, 3, int(mask.sum()))
    out[mask] = (out[mask] + deltas) % 3
    return out


# --- Mechanism arrays (structural roles, before column assignment) -----------


def _chain_arrays(mode: str, rng: np.random.RandomState) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (root, parent, x2) for root -> parent -> x2."""
    if mode == "binary":
        root = rng.binomial(1, 0.5, _N)
        parent = _flip_binary(root, _CHAIN_FLIP, rng)
        x2 = _flip_binary(parent, _TARGET_NOISE, rng)
    elif mode == "cat3":
        root = rng.randint(0, 3, _N)
        parent = _flip_cat3(root, _CHAIN_FLIP, rng)
        x2 = _flip_cat3(parent, _TARGET_NOISE, rng)
    else:  # cont3
        root = rng.randn(_N)
        parent = root + 0.5 * rng.randn(_N)
        x2 = parent + 0.3 * rng.randn(_N)
    return root, parent, x2


def _fork_arrays(mode: str, rng: np.random.RandomState) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (cause, sibling, x2) for cause -> x2 and cause -> sibling."""
    if mode == "binary":
        cause = rng.binomial(1, 0.5, _N)
        x2 = _flip_binary(cause, _TARGET_NOISE, rng)
        sibling = _flip_binary(cause, _FORK_SIB_NOISE, rng)
    elif mode == "cat3":
        cause = rng.randint(0, 3, _N)
        x2 = _flip_cat3(cause, _TARGET_NOISE, rng)
        sibling = _flip_cat3(cause, _FORK_SIB_NOISE, rng)
    else:  # cont3
        cause = rng.randn(_N)
        x2 = cause + 0.3 * rng.randn(_N)
        sibling = cause + 0.6 * rng.randn(_N)
    return cause, sibling, x2


def _collider_arrays(mode: str, rng: np.random.RandomState) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (x0, x1, x2) for x0 -> x2 <- x1 (both parents)."""
    if mode == "binary":
        x0 = rng.binomial(1, 0.5, _N)
        x1 = rng.binomial(1, 0.5, _N)
        base = (x0 | x1).astype(int)  # OR: each parent needed for full coverage
        x2 = _flip_binary(base, _TARGET_NOISE, rng)
    elif mode == "cat3":
        x0 = rng.randint(0, 3, _N)
        x1 = rng.randint(0, 3, _N)
        base = np.maximum(x0, x1)  # positive (==2) needs x0==2 or x1==2
        x2 = _flip_cat3(base, _TARGET_NOISE, rng)
    else:  # cont3
        x0 = rng.randn(_N)
        x1 = rng.randn(_N)
        x2 = x0 + x1 + 0.3 * rng.randn(_N)
    return x0, x1, x2


def _is_positive(mode: str) -> Callable[[float], bool]:
    if mode == "binary":
        return lambda v: v == 1
    if mode == "cat3":
        return lambda v: v == 2
    return lambda v: v >= 0.0


def _build_fixture(
    key: str,
    cols: dict[str, np.ndarray],
    edges: tuple[tuple[int, int], ...],
    mode: str,
) -> HandcraftedFixture:
    var_types = _CONTINUOUS_TYPES if mode == "cont3" else _CATEGORICAL_TYPES
    x2_values = list(cols["x2"])
    pos, neg = _x2_examples(x2_values, _is_positive(mode))
    df = pd.DataFrame({"x0": cols["x0"], "x1": cols["x1"], "x2": cols["x2"]})
    return HandcraftedFixture(
        key=key,
        df=df,
        var_types=dict(var_types),
        pos_examples=pos,
        neg_examples=neg,
        nodes=3,
        edges=edges,
    )


# Structural configs: (base_key, motif, parent_position).
_CONFIGS: tuple[tuple[str, str, str | None], ...] = (
    ("qi003_chain_x1parent", "chain", "x1"),
    ("qi003_chain_x0parent", "chain", "x0"),
    ("qi003_fork_x0parent", "fork", "x0"),
    ("qi003_fork_x1parent", "fork", "x1"),
    ("qi003_collider", "collider", None),
)
_MODES: tuple[str, ...] = ("binary", "cat3", "cont3")
_BASE_SEED = 20030000


def _assemble(
    motif: str, parent_pos: str | None, mode: str, rng: np.random.RandomState
) -> tuple[dict[str, np.ndarray], tuple[tuple[int, int], ...]]:
    """Map structural-role arrays onto x0/x1 columns + edges for one fixture."""
    if motif == "chain":
        root, parent, x2 = _chain_arrays(mode, rng)
        if parent_pos == "x1":  # x0=root, x1=parent
            return {"x0": root, "x1": parent, "x2": x2}, ((0, 1), (1, 2))
        # parent_pos == "x0": x0=parent, x1=root
        return {"x0": parent, "x1": root, "x2": x2}, ((1, 0), (0, 2))
    if motif == "fork":
        cause, sibling, x2 = _fork_arrays(mode, rng)
        if parent_pos == "x0":  # x0=cause, x1=sibling
            return {"x0": cause, "x1": sibling, "x2": x2}, ((0, 1), (0, 2))
        # parent_pos == "x1": x0=sibling, x1=cause
        return {"x0": sibling, "x1": cause, "x2": x2}, ((1, 0), (1, 2))
    # collider
    x0, x1, x2 = _collider_arrays(mode, rng)
    return {"x0": x0, "x1": x1, "x2": x2}, ((0, 2), (1, 2))


def _make_builder(
    key: str, motif: str, parent_pos: str | None, mode: str, seed: int
) -> Callable[[], HandcraftedFixture]:
    def builder() -> HandcraftedFixture:
        rng = np.random.RandomState(seed)
        cols, edges = _assemble(motif, parent_pos, mode, rng)
        return _build_fixture(key, cols, edges, mode)

    builder.__name__ = key
    builder.__qualname__ = key
    return builder


QI003_BUILDERS: dict[str, Callable[[], HandcraftedFixture]] = {}
for _i, (_base, _motif, _ppos) in enumerate(_CONFIGS):
    for _j, _mode in enumerate(_MODES):
        _key = f"{_base}_{_mode}"
        _seed = _BASE_SEED + _i * 10 + _j
        QI003_BUILDERS[_key] = _make_builder(_key, _motif, _ppos, _mode, _seed)

# Each fixture id is its own canonical alias.
QI003_ALIASES: dict[str, str] = {key: key for key in QI003_BUILDERS}
