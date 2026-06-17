"""QI-004 reduced-n scaled fixtures: 5 structural configs x 3 data modes, target ``x2``.

QI-004 is the computationally feasible follow-up to QI-003. The QI-003 ``n=100``
run was infeasible under the available Prolog timeout budget (cat3/cont3 cells
timed out at 120s; see ``docs/experiments/qualitative/QI-003.md``).
QI-004 keeps the **same conceptual design** as QI-003 - the same motifs,
parent-position controls, mechanisms, and noise levels - but reduces the sample
size to ``n=20`` (run with ``prolog_timeout_s=300``).

Why new fixtures rather than a config change: the ``handcrafted_table`` path
copies ``fixture.df`` directly and ignores ``cell.n`` (see
``causal/experiments/run_grid.py``), so the sample size is the module constant
``_N`` here, not a grid parameter.

Scope: parent-set recovery via ABA Learning, NOT Russo-style Causal ABA.

This module reuses the N-agnostic helpers from ``handcrafted_qi003`` (example
construction, noise flips, positive-class predicates, fixture assembly, var-type
maps) and redefines only the ``_N``-dependent array generators, so QI-003 stays
completely untouched.

Encoding contract (enforced by ``causal/argcausaldisco_integration.py``):
- binary mode: ``categorical`` var_type, values ``{0,1}`` -> bare predicates;
- categorical-3 mode: ``categorical`` var_type, values ``{0,1,2}`` -> ``_val_``;
- continuous mode: ``continuous`` var_type -> ``_bin`` predicates (run with
  ``bins=3``, ``bin_strategy=uniform``).

Sample-id convention is 1-based (row index ``i`` -> atom ``x2(i+1)``).

Parent-position tracking (identical to QI-003; 0-based edges ``(s,t)`` = ``xs -> xt``):
- qi004_chain_x1parent : x0=root, x1=parent  -> edges ((0,1),(1,2)), parents={x1}
- qi004_chain_x0parent : x1=root, x0=parent  -> edges ((1,0),(0,2)), parents={x0}
- qi004_fork_x0parent  : x0=cause, x1=sibling-> edges ((0,1),(0,2)), parents={x0}
- qi004_fork_x1parent  : x1=cause, x0=sibling-> edges ((1,0),(1,2)), parents={x1}
- qi004_collider       : x0,x1 both parents  -> edges ((0,2),(1,2)), parents={x0,x1}

Known carry-over limitation: the binary "positive-cases-only" BK encoding cannot
declare a sample-id constant for an all-zero-feature row (``x0=0, x1=0``); target
noise can flip such a row to a positive example, which then trips
``check_ep_consts_aux`` in ``aba_asp.pl`` (``unknown constant``). Reducing n
lowers but does not eliminate the chance; recorded as a known limitation.
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

from causal.experiments.handcrafted import HandcraftedFixture
from causal.experiments.handcrafted_qi003 import (
    _CHAIN_FLIP,
    _FORK_SIB_NOISE,
    _TARGET_NOISE,
    _build_fixture,
    _flip_binary,
    _flip_cat3,
)

# Reduced sample size (QI-003 used 100; QI-004 uses 20 for tractability).
_N = 20


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


# Structural configs: (base_key, motif, parent_position). Mirrors QI-003.
_CONFIGS: tuple[tuple[str, str, str | None], ...] = (
    ("qi004_chain_x1parent", "chain", "x1"),
    ("qi004_chain_x0parent", "chain", "x0"),
    ("qi004_fork_x0parent", "fork", "x0"),
    ("qi004_fork_x1parent", "fork", "x1"),
    ("qi004_collider", "collider", None),
)
_MODES: tuple[str, ...] = ("binary", "cat3", "cont3")
# Base seed chosen so that at n=20 both binary/cat3 chain fixtures keep the
# intermediate distinct from its root (>= ~0.15 disagreement), avoiding the
# QI-001 degenerate collinear chain where parent and ancestor coincide.
_BASE_SEED = 20040002


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


QI004_BUILDERS: dict[str, Callable[[], HandcraftedFixture]] = {}
for _i, (_base, _motif, _ppos) in enumerate(_CONFIGS):
    for _j, _mode in enumerate(_MODES):
        _key = f"{_base}_{_mode}"
        _seed = _BASE_SEED + _i * 10 + _j
        QI004_BUILDERS[_key] = _make_builder(_key, _motif, _ppos, _mode, _seed)

# Each fixture id is its own canonical alias.
QI004_ALIASES: dict[str, str] = {key: key for key in QI004_BUILDERS}
