"""m1.1 parent-position / representation-order fixtures (Milestone 1, Part 1).

Eight metamorphic fixtures (2 encodings x cells A/B/C/D) supporting the
m1.1 control described in
``docs/research/milestone_plans/milestone1_part1_parent_position.md``.

**Tabular DGP (all cells):** exhaustive factorial over (x0, x1); x2 := parent
deterministically; the non-parent is marginally independent of x2. At the data
level each cell is one *isolated* predictor plus a connected parent-target
pair (``isolated ; parent -> x2``), NOT observational data from a chain SCM.

Chain-style ``edges`` in the fixture metadata label which variable is parent vs
non-parent for the ``pi`` swap; they do not generate ancestor-parent association
in the table. Faithful correlated-ancestor chains remain QI-003/QI-004.

The design crosses two factors at a fixed target ``x2``:

1. direct-parent identity: ``x1`` (cells A, B) or ``x0`` (cells C, D);
2. learner-visible predictor order: ``[x0, x1]`` (cells A, C) or ``[x1, x0]``
   (cells B, D).

Following the plan, the four cells of one encoding are a single transformation
orbit derived from the canonical cell A, NOT regenerated ad hoc:

- ``sigma`` reverses the learner-visible predictor order without renaming
  variables or changing any value, example, graph role, or target label;
- ``pi`` exchanges the variable identities ``x0`` and ``x1`` (names *and*
  values together), relabels the graph roles, and fixes ``x2`` and the sample
  identities.

So per encoding::

    A --sigma--> B
    |             |
    pi            pi
    v             v
    D --sigma--> C

with ``B = sigma(A)``, ``D = pi(A)``, ``C = sigma(D) = pi(B)``.

Predictor order reaching the learner is the **DataFrame column order**: the BK
writer in ``causal/argcausaldisco_integration.py`` serialises by iterating
``df.columns`` (skipping the excluded target) with no sorting. So ``sigma`` is
implemented as a column reorder and ``x2`` is always kept last.

Scope: parent-set / learned-rule recovery proxy via ABA Learning, NOT
Russo-style Causal ABA. Fixture ``edges`` annotate structural roles (direct
parent vs isolated non-parent) for ``pi``; the exhaustive factorial table
deliberately keeps the non-parent independent of ``x2``. This is NOT a faithful
chain SCM sample: a correlated-ancestor test remains the job of QI-003/QI-004.

Data construction (minimal complete factorial, once per assignment):
- binary: ``(x0, x1) in {0,1}^2`` = 4 rows; positive iff ``x2 == 1``;
- categorical-3: ``(x0, x1) in {0,1,2}^2`` = 9 rows; positive iff ``x2 == 2``.
In ``x1``-parent cells ``x2 := x1``; in ``x0``-parent cells ``x2 := x0``.
Sample ids are 1-based and row order is fixed.

Row multiplicity: the complete factorial once per assignment is the principled
minimum. The true parent is the unique zero-error one-literal separator and the
pi/sigma orbit relations are independent of row multiplicity, so no per-row
repeat is needed (``_REPEATS`` is kept as an explicit, reversible knob, default
1). The learner imposes no ``|E+| >= 2`` requirement; even at ``_REPEATS = 1``
the x1-parent binary cell has ``|E+| = 2`` and cat3 has ``|E+| = 3``.
"""

from __future__ import annotations

import itertools
from collections.abc import Callable
from dataclasses import dataclass, replace

import pandas as pd

from causal.experiments.handcrafted import HandcraftedFixture

# Canonical chain orientation for cell A: x0 -> x1 -> x2 (direct parent x1).
_CHAIN_EDGES: tuple[tuple[int, int], ...] = ((0, 1), (1, 2))

_CATEGORICAL_TYPES: dict[str, str] = {
    "x0": "categorical",
    "x1": "categorical",
    "x2": "categorical",
}

# Each (x0, x1) assignment is represented this many times. The principled minimum
# is the complete factorial once per assignment (1); this is an explicit,
# reversible knob and does not affect the separator logic or the pi/sigma orbit.
_REPEATS = 1

_TARGET = "x2"
_ENCODINGS: tuple[str, ...] = ("binary", "cat3")
_CELLS: tuple[str, ...] = ("A", "B", "C", "D")


# --- Canonical cell A construction ------------------------------------------


def _factorial_columns(values: tuple[int, ...]) -> tuple[list[int], list[int]]:
    """Return (x0, x1) as the complete factorial over ``values``, repeated.

    Combinations are enumerated in lexicographic ``(x0, x1)`` order and the whole
    block is repeated ``_REPEATS`` times (default 1), so every ``(x0, x1)`` pair
    appears an equal number of times.
    """
    combos = list(itertools.product(values, values))
    x0 = [a for a, _ in combos] * _REPEATS
    x1 = [b for _, b in combos] * _REPEATS
    return x0, x1


def _x2_examples(
    x2_values: list[int], positive_value: int
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Build fixed (pos, neg) ``x2(id)`` atoms using 1-based sample ids."""
    pos = tuple(f"x2({i + 1})" for i, v in enumerate(x2_values) if v == positive_value)
    neg = tuple(f"x2({i + 1})" for i, v in enumerate(x2_values) if v != positive_value)
    return pos, neg


def _canonical_a(values: tuple[int, ...], positive_value: int, key: str) -> HandcraftedFixture:
    """Canonical cell A: chain x0->x1->x2 with x2 := x1, order [x0, x1]."""
    x0, x1 = _factorial_columns(values)
    x2 = list(x1)  # direct parent of x2 in cell A is x1
    pos, neg = _x2_examples(x2, positive_value)
    return HandcraftedFixture(
        key=key,
        df=pd.DataFrame({"x0": x0, "x1": x1, "x2": x2}),
        var_types=dict(_CATEGORICAL_TYPES),
        pos_examples=pos,
        neg_examples=neg,
        nodes=3,
        edges=_CHAIN_EDGES,
    )


def canonical_a_binary() -> HandcraftedFixture:
    """Canonical binary cell A: x2 = x1 over {0,1}^2 (4 rows), positive iff x2 == 1."""
    return _canonical_a((0, 1), positive_value=1, key="m11_binary_A")


def canonical_a_cat3() -> HandcraftedFixture:
    """Canonical cat3 cell A: x2 = x1 over {0,1,2}^2 (9 rows), positive iff x2 == 2."""
    return _canonical_a((0, 1, 2), positive_value=2, key="m11_cat3_A")


# --- Transformations (sigma, pi) --------------------------------------------

_PI_NAME_SWAP: dict[str, str] = {"x0": "x1", "x1": "x0"}
_PI_INDEX_SWAP: dict[int, int] = {0: 1, 1: 0}


def predictor_columns(fx: HandcraftedFixture) -> list[str]:
    """Learner-visible predictor order = DataFrame columns minus the target."""
    return [c for c in fx.df.columns if c != fx.default_target]


def apply_sigma(fx: HandcraftedFixture) -> HandcraftedFixture:
    """Reverse the learner-visible predictor order; keep the target last.

    Only the column order changes: values, examples, sample identities, graph
    roles, and the target label are all preserved.
    """
    predictors = predictor_columns(fx)
    new_cols = list(reversed(predictors)) + [fx.default_target]
    return replace(fx, df=fx.df[new_cols].copy())


def apply_pi(fx: HandcraftedFixture) -> HandcraftedFixture:
    """Exchange variable identities ``x0`` and ``x1`` (names and values together).

    The target ``x2`` and the sample identities are fixed. Graph-role edges are
    relabelled via ``0 <-> 1``, and the predictor order becomes the pi-image of
    the original order (so reversing it as a side effect of the renaming).
    """
    target = fx.default_target
    renamed = fx.df.rename(columns=_PI_NAME_SWAP)
    new_pred_order = [_PI_NAME_SWAP.get(c, c) for c in predictor_columns(fx)]
    new_cols = new_pred_order + [target]
    new_df = renamed[new_cols].copy()

    new_edges = tuple(
        (_PI_INDEX_SWAP.get(s, s), _PI_INDEX_SWAP.get(t, t)) for s, t in fx.edges
    )
    new_var_types = {_PI_NAME_SWAP.get(k, k): v for k, v in fx.var_types.items()}
    return replace(fx, df=new_df, edges=new_edges, var_types=new_var_types)


# --- Orbit assembly ---------------------------------------------------------


def _canonical_a_for(encoding: str) -> HandcraftedFixture:
    if encoding == "binary":
        return canonical_a_binary()
    if encoding == "cat3":
        return canonical_a_cat3()
    raise ValueError(f"unknown encoding {encoding!r}")


def build_cell(encoding: str, cell: str) -> HandcraftedFixture:
    """Build one m1.1 fixture from the canonical A of its encoding via sigma/pi."""
    base = _canonical_a_for(encoding)
    if cell == "A":
        fx = base
    elif cell == "B":
        fx = apply_sigma(base)
    elif cell == "D":
        fx = apply_pi(base)
    elif cell == "C":
        fx = apply_sigma(apply_pi(base))
    else:
        raise ValueError(f"unknown cell {cell!r}")
    return replace(fx, key=f"m11_{encoding}_{cell}")


# Explicit builders (one per fixture) for an inspectable registry.
def m11_binary_A() -> HandcraftedFixture:  # noqa: N802 - cell labels are uppercase
    return build_cell("binary", "A")


def m11_binary_B() -> HandcraftedFixture:  # noqa: N802
    return build_cell("binary", "B")


def m11_binary_C() -> HandcraftedFixture:  # noqa: N802
    return build_cell("binary", "C")


def m11_binary_D() -> HandcraftedFixture:  # noqa: N802
    return build_cell("binary", "D")


def m11_cat3_A() -> HandcraftedFixture:  # noqa: N802
    return build_cell("cat3", "A")


def m11_cat3_B() -> HandcraftedFixture:  # noqa: N802
    return build_cell("cat3", "B")


def m11_cat3_C() -> HandcraftedFixture:  # noqa: N802
    return build_cell("cat3", "C")


def m11_cat3_D() -> HandcraftedFixture:  # noqa: N802
    return build_cell("cat3", "D")


M11_BUILDERS: dict[str, Callable[[], HandcraftedFixture]] = {
    "m11_binary_A": m11_binary_A,
    "m11_binary_B": m11_binary_B,
    "m11_binary_C": m11_binary_C,
    "m11_binary_D": m11_binary_D,
    "m11_cat3_A": m11_cat3_A,
    "m11_cat3_B": m11_cat3_B,
    "m11_cat3_C": m11_cat3_C,
    "m11_cat3_D": m11_cat3_D,
}

# Each fixture id is its own canonical alias.
M11_ALIASES: dict[str, str] = {key: key for key in M11_BUILDERS}


# --- Per-cell metadata (requested order / parent identity) ------------------


@dataclass(frozen=True)
class M11CellMeta:
    """Design metadata for one m1.1 cell (independent of the table contents)."""

    key: str
    encoding: str
    cell: str
    parent: str  # direct parent of x2 by design
    requested_order: tuple[str, ...]  # learner-visible predictor order


def _meta(encoding: str, cell: str) -> M11CellMeta:
    parent = "x1" if cell in ("A", "B") else "x0"
    requested_order = ("x0", "x1") if cell in ("A", "C") else ("x1", "x0")
    return M11CellMeta(
        key=f"m11_{encoding}_{cell}",
        encoding=encoding,
        cell=cell,
        parent=parent,
        requested_order=requested_order,
    )


M11_CELLS: tuple[M11CellMeta, ...] = tuple(
    _meta(encoding, cell) for encoding in _ENCODINGS for cell in _CELLS
)

M11_META_BY_KEY: dict[str, M11CellMeta] = {m.key: m for m in M11_CELLS}


# --- Structural validation helpers (Prolog-free, table-only) ----------------


def positive_rows(fx: HandcraftedFixture) -> set[int]:
    """Zero-based row indices that are positive examples (parsed from atoms)."""
    rows: set[int] = set()
    for atom in fx.pos_examples:
        sample_id = int(atom[atom.index("(") + 1 : atom.index(")")])
        rows.add(sample_id - 1)
    return rows


def _column_is_binary01(fx: HandcraftedFixture, col: str) -> bool:
    return sorted(int(v) for v in set(fx.df[col])) == [0, 1]


def candidate_predicates(fx: HandcraftedFixture, col: str) -> list[tuple[str, int]]:
    """One-literal feature predicates the BK writer would emit for ``col``.

    Binary 0/1 columns emit only the bare positive-case predicate ``col`` (value
    1); other discrete columns emit a value predicate per observed value.
    """
    if _column_is_binary01(fx, col):
        return [(col, 1)]
    return [(col, int(v)) for v in sorted(set(int(x) for x in fx.df[col]))]


def is_zero_error_separator(fx: HandcraftedFixture, col: str, value: int) -> bool:
    """True iff ``x2(A) <- pred(A)`` (pred = col==value) is a perfect separator.

    Perfect = the rows where ``col == value`` are exactly the positive rows
    (covers all positives, covers no negatives).
    """
    pos = positive_rows(fx)
    covered = {i for i in range(len(fx.df)) if int(fx.df[col].iloc[i]) == value}
    return covered == pos


def expected_parent_predicate(fx: HandcraftedFixture, parent: str) -> tuple[str, int]:
    """The intended one-literal parent predicate for this encoding/cell."""
    if _column_is_binary01(fx, parent):
        return (parent, 1)
    return (parent, 2)


def _every_assignment_present(fx: HandcraftedFixture) -> bool:
    """Every ``(x0, x1)`` assignment occurs exactly ``_REPEATS`` times (default 1)."""
    combos = list(zip(fx.df["x0"], fx.df["x1"]))
    values = sorted(set(int(v) for v in fx.df["x0"]) | set(int(v) for v in fx.df["x1"]))
    return all(
        combos.count(combo) == _REPEATS
        for combo in itertools.product(values, values)
    )


def structural_checks(key: str) -> dict[str, bool]:
    """Run the table-only Stage-0 checks for one m1.1 fixture.

    BK-dependent checks (target exclusion, BK group order) are validated
    separately by the test/manifest layer, which generates the actual BK.
    """
    fx = M11_BUILDERS[key]()
    meta = M11_META_BY_KEY[key]
    parent = meta.parent
    non_parent = "x1" if parent == "x0" else "x0"

    base_combos = 4 if meta.encoding == "binary" else 9
    expected_rows = base_combos * _REPEATS
    p_pred = expected_parent_predicate(fx, parent)

    checks: dict[str, bool] = {
        "row_count": len(fx.df) == expected_rows,
        "every_assignment_present": _every_assignment_present(fx),
        "x2_equals_parent": all(
            int(fx.df["x2"].iloc[i]) == int(fx.df[parent].iloc[i])
            for i in range(len(fx.df))
        ),
        "requested_equals_table_order": tuple(predictor_columns(fx)) == meta.requested_order,
        "examples_partition_rows": (
            positive_rows(fx).isdisjoint(_negative_rows(fx))
            and positive_rows(fx) | _negative_rows(fx) == set(range(len(fx.df)))
        ),
        "parent_is_zero_error_separator": is_zero_error_separator(fx, *p_pred),
        "non_parent_has_no_separator": not any(
            is_zero_error_separator(fx, col, val)
            for (col, val) in candidate_predicates(fx, non_parent)
        ),
    }
    return checks


def _negative_rows(fx: HandcraftedFixture) -> set[int]:
    rows: set[int] = set()
    for atom in fx.neg_examples:
        sample_id = int(atom[atom.index("(") + 1 : atom.index(")")])
        rows.add(sample_id - 1)
    return rows


# --- Pairwise (orbit) equivalence helpers -----------------------------------


def fixtures_equal_ignoring_key(fx1: HandcraftedFixture, fx2: HandcraftedFixture) -> bool:
    """Compare two fixtures for everything except ``key``.

    DataFrames must match exactly including column order; var_types, examples,
    nodes, edges, and target must all be equal.
    """
    if list(fx1.df.columns) != list(fx2.df.columns):
        return False
    if not fx1.df.reset_index(drop=True).equals(fx2.df.reset_index(drop=True)):
        return False
    return (
        dict(fx1.var_types) == dict(fx2.var_types)
        and fx1.pos_examples == fx2.pos_examples
        and fx1.neg_examples == fx2.neg_examples
        and fx1.nodes == fx2.nodes
        and tuple(fx1.edges) == tuple(fx2.edges)
        and fx1.default_target == fx2.default_target
    )


def is_sigma_pair(fx_a: HandcraftedFixture, fx_b: HandcraftedFixture) -> bool:
    """True iff ``fx_b == sigma(fx_a)`` exactly (only predictor order differs)."""
    return fixtures_equal_ignoring_key(apply_sigma(fx_a), fx_b)


def is_pi_pair(fx_a: HandcraftedFixture, fx_b: HandcraftedFixture) -> bool:
    """True iff ``fx_b == pi(fx_a)`` exactly (x0<->x1 names and values swapped)."""
    return fixtures_equal_ignoring_key(apply_pi(fx_a), fx_b)


def bk_predictor_order(bk_text: str) -> list[str]:
    """Order in which the ``x0``/``x1`` feature-predicate groups appear in BK.

    Reads the generated ``bk.aba`` text and returns the base variables in the
    order their first feature rule line occurs. Comment lines are ignored, so the
    order reflects the learner-visible serialisation rather than annotations.
    """
    order: list[str] = []
    for line in bk_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("%") or "(A)" not in stripped:
            continue
        head = stripped.split("(", 1)[0].strip()
        base: str | None = None
        if head == "x0" or head.startswith("x0_"):
            base = "x0"
        elif head == "x1" or head.startswith("x1_"):
            base = "x1"
        if base is not None and base not in order:
            order.append(base)
    return order
