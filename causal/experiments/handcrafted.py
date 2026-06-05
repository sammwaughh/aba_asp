"""Handcrafted table fixtures lifted from the legacy ``test_aba_learning.py`` suite.

These are small, fully-specified datasets (a perfect-correlation case and an
assumption-introduction case) with fixed positive/negative examples. They let the
grid runner replay deterministic, separable examples as cells, independent of the
random simulators.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import pandas as pd

from causal.metrics import GroundTruth


@dataclass(frozen=True)
class HandcraftedFixture:
    """Fixed small table + E+/E− used by ``test_aba_learning.py``."""

    key: str
    df: pd.DataFrame
    var_types: dict[str, str]
    pos_examples: tuple[str, ...]
    neg_examples: tuple[str, ...]
    nodes: int
    edges: tuple[tuple[int, int], ...]
    default_target: str = "x2"

    def ground_truth(self) -> GroundTruth:
        names = tuple(f"x{i}" for i in range(self.nodes))
        edge_names = frozenset((f"x{s}", f"x{t}") for s, t in self.edges)
        return GroundTruth(nodes=names, edges=edge_names)


def simple_4_fixture() -> HandcraftedFixture:
    """``TestSimpleHandcraftedLearning.test_simple_4_samples`` table."""
    data = {
        "x0": [1, 1, 0, 0],
        "x1": [1, 0, 1, 0],
        "x2": [1, 1, 0, 0],
    }
    return HandcraftedFixture(
        key="simple_4",
        df=pd.DataFrame(data),
        var_types={c: "categorical" for c in data},
        pos_examples=("x2(1)", "x2(2)"),
        neg_examples=("x2(3)", "x2(4)"),
        nodes=3,
        edges=((0, 2),),
    )


def exception_5_fixture() -> HandcraftedFixture:
    """``TestAssumptionIntroduction.test_exception_triggers_assumption_intro`` table."""
    data = {
        "x0": [1, 1, 1, 0, 0],
        "x1": [0, 0, 1, 0, 1],
        "x2": [1, 1, 0, 0, 0],
    }
    return HandcraftedFixture(
        key="exception_5",
        df=pd.DataFrame(data),
        var_types={c: "categorical" for c in data},
        pos_examples=("x2(1)", "x2(2)"),
        neg_examples=("x2(3)", "x2(4)", "x2(5)"),
        nodes=3,
        edges=((0, 2),),
    )


_ALIASES: dict[str, str] = {
    "simple_4": "simple_4",
    "tests.simple_4": "simple_4",
    "exception_5": "exception_5",
    "tests.exception_5": "exception_5",
}

_BUILDERS: dict[str, Callable[[], HandcraftedFixture]] = {
    "simple_4": simple_4_fixture,
    "exception_5": exception_5_fixture,
}


def normalize_source(source: str) -> str:
    key = source.strip()
    if key not in _ALIASES:
        raise KeyError(
            f"unknown handcrafted source {source!r}; "
            f"expected one of {sorted(_ALIASES)}"
        )
    return _ALIASES[key]


def load_handcrafted(source: str) -> HandcraftedFixture:
    """Load a handcrafted fixture by config ``source`` key."""
    canonical = normalize_source(source)
    return _BUILDERS[canonical]()
