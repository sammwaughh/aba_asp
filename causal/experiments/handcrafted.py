"""Handcrafted table fixtures lifted from the legacy ``test_aba_learning.py`` suite.

These are small, fully-specified datasets (a perfect-correlation case and an
assumption-introduction case) with fixed positive/negative examples. They let the
grid runner replay deterministic, separable examples as cells, independent of the
random simulators.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass

import pandas as pd

from causal.metrics import GroundTruth

# (pos_atoms, neg_atoms) for one learning target.
ExamplesPair = tuple[tuple[str, ...], tuple[str, ...]]


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
    # When set, YAML/grid default targets (inspection order: nearer sources first).
    learning_targets: tuple[str, ...] | None = None
    # Per-target E+/E−; if absent, ``pos_examples``/``neg_examples`` apply to
    # ``default_target`` only.
    examples_by_target: Mapping[str, ExamplesPair] | None = None

    def resolved_learning_targets(self) -> tuple[str, ...]:
        if self.learning_targets is not None:
            return self.learning_targets
        return (self.default_target,)

    def examples_for_target(self, target: str) -> ExamplesPair:
        if self.examples_by_target is not None and target in self.examples_by_target:
            return self.examples_by_target[target]
        if target == self.default_target:
            return self.pos_examples, self.neg_examples
        raise ValueError(
            f"handcrafted fixture {self.key!r} has no examples for target {target!r}; "
            f"known={sorted((self.examples_by_target or {}).keys()) or [self.default_target]}"
        )

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


# Register QI-001 fixtures (imported at end of module so ``HandcraftedFixture``
# is already defined when ``handcrafted_qi001`` imports it back).
from causal.experiments.handcrafted_qi001 import (  # noqa: E402
    QI001_ALIASES,
    QI001_BUILDERS,
)
from causal.experiments.handcrafted_qi002 import (  # noqa: E402
    QI002_ALIASES,
    QI002_BUILDERS,
)
from causal.experiments.handcrafted_qi003 import (  # noqa: E402
    QI003_ALIASES,
    QI003_BUILDERS,
)
from causal.experiments.handcrafted_qi004 import (  # noqa: E402
    QI004_ALIASES,
    QI004_BUILDERS,
)
from causal.experiments.handcrafted_m11 import (  # noqa: E402
    M11_ALIASES,
    M11_BUILDERS,
)
from causal.experiments.handcrafted_m12 import (  # noqa: E402
    M12_ALIASES,
    M12_BUILDERS,
)
from causal.experiments.handcrafted_m12x import (  # noqa: E402
    M12X_ALIASES,
    M12X_BUILDERS,
)
from causal.experiments.handcrafted_m13 import (  # noqa: E402
    M13_ALIASES,
    M13_BUILDERS,
)

_ALIASES.update(QI001_ALIASES)
_BUILDERS.update(QI001_BUILDERS)
_ALIASES.update(QI002_ALIASES)
_BUILDERS.update(QI002_BUILDERS)
_ALIASES.update(QI003_ALIASES)
_BUILDERS.update(QI003_BUILDERS)
_ALIASES.update(QI004_ALIASES)
_BUILDERS.update(QI004_BUILDERS)
_ALIASES.update(M11_ALIASES)
_BUILDERS.update(M11_BUILDERS)
_ALIASES.update(M12_ALIASES)
_BUILDERS.update(M12_BUILDERS)
_ALIASES.update(M12X_ALIASES)
_BUILDERS.update(M12X_BUILDERS)
_ALIASES.update(M13_ALIASES)
_BUILDERS.update(M13_BUILDERS)
