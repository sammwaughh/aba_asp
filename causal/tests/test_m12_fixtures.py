"""M1.2 Stage-0 Prolog-free validation checks for the five M12 fixtures.

Locks the fixture tables against the designs agreed in
``docs/research/milestone_plans/milestone1_part2/milestone1_part2_config_comparison.md``
(Section 4) and recorded in ``docs/experiments/qualitative/M1.2-config-comparison.md``:

- registration, node counts, targets, and declared-G consistency;
- row counts and construction (factorial for sep/conj/disj; three distinct
  deterministic assignments x3 for fork; correlated block structure for chain);
- separator logic: unique zero-error separator per family; distractors not
  zero-error; association PRESENT for fork x1 and chain x0, ABSENT for the
  isolated columns (sep x0, conj x2, disj x2);
- conj/disj minimality: no single one-literal value predicate is
  complete+consistent; the expected rule (set) exactly covers E+ with no E-;
- E+/E- atoms match the positive mask with 1-based sample ids;
- no column has value set exactly {0, 1} (bare-binary BK encoding guard);
- BK encoding via ``execute_cell_stage2`` (stops before Prolog): value
  predicates for all predictors, target excluded.

No ABA Learning is run (no swipl/clingo).
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from causal.experiments.config import CellSpec
from causal.experiments.handcrafted import load_handcrafted, normalize_source
from causal.experiments.handcrafted_m12 import M12_ALIASES, M12_BUILDERS
from causal.experiments.run_grid import execute_cell_stage2

_ALL_IDS = ("m12_sep", "m12_conj", "m12_disj", "m12_fork", "m12_chain")

# Per-fixture design facts (kept in one place so each check reads off the plan).
_TARGET = {
    "m12_sep": "x2",
    "m12_conj": "x3",
    "m12_disj": "x3",
    "m12_fork": "x2",
    "m12_chain": "x2",
}
_NODES = {
    "m12_sep": 3,
    "m12_conj": 4,
    "m12_disj": 4,
    "m12_fork": 3,
    "m12_chain": 3,
}
_EXPECTED_PARENTS = {
    "m12_sep": {"x1"},
    "m12_conj": {"x0", "x1"},
    "m12_disj": {"x0", "x1"},
    "m12_fork": {"x0"},
    "m12_chain": {"x1"},
}
_EDGES = {
    "m12_sep": ((1, 2),),
    "m12_conj": ((0, 3), (1, 3)),
    "m12_disj": ((0, 3), (1, 3)),
    "m12_fork": ((0, 1), (0, 2)),
    "m12_chain": ((0, 1), (1, 2)),
}
_ROW_COUNT = {
    "m12_sep": 9,
    "m12_conj": 27,
    "m12_disj": 27,
    "m12_fork": 9,
    "m12_chain": 9,
}
_POSITIVE_VALUE = 2


def _fx(source: str):
    return load_handcrafted(source)


def _predictors(source: str) -> list[str]:
    fx = _fx(source)
    return [c for c in fx.df.columns if c != _TARGET[source]]


def _positive_mask(source: str) -> list[bool]:
    fx = _fx(source)
    return [int(v) == _POSITIVE_VALUE for v in fx.df[_TARGET[source]]]


def _column_is_zero_error_separator(source: str, col: str) -> bool:
    """True iff no value of ``col`` appears in both a positive and a negative row."""
    fx = _fx(source)
    pos = _positive_mask(source)
    by_value: dict[int, set[bool]] = {}
    for val, is_pos in zip(fx.df[col], pos):
        by_value.setdefault(int(val), set()).add(is_pos)
    return all(len(labels) == 1 for labels in by_value.values())


def _column_is_associated(source: str, col: str) -> bool:
    """True iff in-sample P(pos | col == v) is not constant across values of col."""
    fx = _fx(source)
    pos = _positive_mask(source)
    counts: dict[int, list[int]] = {}
    for val, is_pos in zip(fx.df[col], pos):
        n_pos, n_all = counts.setdefault(int(val), [0, 0])
        counts[int(val)] = [n_pos + int(is_pos), n_all + 1]
    rates = {n_pos / n_all for n_pos, n_all in counts.values()}
    return len(rates) > 1


def _one_literal_rules(source: str) -> list[tuple[str, int]]:
    """All (column, value) one-literal candidate rules over the predictors."""
    fx = _fx(source)
    return [
        (col, int(v))
        for col in _predictors(source)
        for v in sorted(set(int(x) for x in fx.df[col]))
    ]


def _rule_covers(source: str, literals: list[tuple[str, int]]) -> list[bool]:
    """Per-row coverage mask of a conjunctive rule over (column, value) literals."""
    fx = _fx(source)
    return [
        all(int(fx.df[col].iloc[i]) == val for col, val in literals)
        for i in range(len(fx.df))
    ]


# --- Registration and metadata ------------------------------------------------


def test_module_registers_five_fixtures() -> None:
    assert len(M12_BUILDERS) == 5
    assert set(M12_BUILDERS) == set(_ALL_IDS)
    assert set(M12_ALIASES) == set(_ALL_IDS)


@pytest.mark.parametrize("source", _ALL_IDS)
def test_fixture_loads_via_registry(source: str) -> None:
    assert _fx(source).key == source
    assert normalize_source(source) == source


@pytest.mark.parametrize("source", _ALL_IDS)
def test_nodes_target_edges_parents(source: str) -> None:
    fx = _fx(source)
    assert fx.nodes == _NODES[source]
    assert fx.default_target == _TARGET[source]
    assert tuple(fx.edges) == _EDGES[source]
    gt = fx.ground_truth()
    assert set(gt.parents_of(_TARGET[source])) == _EXPECTED_PARENTS[source]


@pytest.mark.parametrize("source", _ALL_IDS)
def test_row_count(source: str) -> None:
    assert len(_fx(source).df) == _ROW_COUNT[source]


@pytest.mark.parametrize("source", _ALL_IDS)
def test_all_columns_categorical(source: str) -> None:
    fx = _fx(source)
    assert set(fx.var_types) == set(fx.df.columns)
    assert set(fx.var_types.values()) == {"categorical"}


@pytest.mark.parametrize("source", _ALL_IDS)
def test_no_column_has_bare_binary_value_set(source: str) -> None:
    """No column may have value set exactly {0, 1}: that triggers the bare
    binary predicate encoding path instead of value predicates."""
    fx = _fx(source)
    for col in fx.df.columns:
        assert sorted(set(int(v) for v in fx.df[col])) != [0, 1], col


@pytest.mark.parametrize("source", _ALL_IDS)
def test_examples_match_positive_mask(source: str) -> None:
    fx = _fx(source)
    target = _TARGET[source]
    pos_mask = _positive_mask(source)
    expected_pos = tuple(f"{target}({i + 1})" for i, p in enumerate(pos_mask) if p)
    expected_neg = tuple(f"{target}({i + 1})" for i, p in enumerate(pos_mask) if not p)
    assert fx.pos_examples == expected_pos
    assert fx.neg_examples == expected_neg
    assert len(fx.pos_examples) >= 2  # avoid single-example flukes
    assert len(fx.neg_examples) >= 2


# --- Construction checks ------------------------------------------------------


def test_sep_is_complete_factorial_and_copies_parent() -> None:
    fx = _fx("m12_sep")
    combos = list(zip(fx.df["x0"], fx.df["x1"]))
    for combo in itertools.product((0, 1, 2), (0, 1, 2)):
        assert combos.count(combo) == 1
    assert list(fx.df["x2"]) == list(fx.df["x1"])


def test_conj_is_complete_factorial_with_min_mechanism() -> None:
    fx = _fx("m12_conj")
    combos = list(zip(fx.df["x0"], fx.df["x1"], fx.df["x2"]))
    for combo in itertools.product((0, 1, 2), repeat=3):
        assert combos.count(combo) == 1
    assert list(fx.df["x3"]) == [min(a, b) for a, b in zip(fx.df["x0"], fx.df["x1"])]
    # positive iff x0 == 2 and x1 == 2 (3 rows: x2 free)
    pos = _positive_mask("m12_conj")
    assert sum(pos) == 3
    for i, p in enumerate(pos):
        assert p == (int(fx.df["x0"].iloc[i]) == 2 and int(fx.df["x1"].iloc[i]) == 2)


def test_disj_is_complete_factorial_with_max_mechanism() -> None:
    fx = _fx("m12_disj")
    combos = list(zip(fx.df["x0"], fx.df["x1"], fx.df["x2"]))
    for combo in itertools.product((0, 1, 2), repeat=3):
        assert combos.count(combo) == 1
    assert list(fx.df["x3"]) == [max(a, b) for a, b in zip(fx.df["x0"], fx.df["x1"])]
    # positive iff x0 == 2 or x1 == 2 (5 pos per x2 block -> 15 total / 12 neg)
    pos = _positive_mask("m12_disj")
    assert sum(pos) == 15
    for i, p in enumerate(pos):
        assert p == (int(fx.df["x0"].iloc[i]) == 2 or int(fx.df["x1"].iloc[i]) == 2)


def test_fork_three_assignments_repeated_in_blocks() -> None:
    """Fork = (0,0,0), (1,2,0), (2,0,2), each x3 in block order; both children
    deterministic functions of x0."""
    fx = _fx("m12_fork")
    rows = [tuple(int(v) for v in row) for row in fx.df.itertuples(index=False)]
    expected = [(0, 0, 0)] * 3 + [(1, 2, 0)] * 3 + [(2, 0, 2)] * 3
    assert rows == expected
    for a, b, c in rows:
        assert b == (2 if a == 1 else 0)  # x1 := 2 if x0 == 1 else 0
        assert c == (2 if a == 2 else 0)  # x2 := 2 if x0 == 2 else 0
    # x1 takes exactly the two values {0, 2} (deterministic imperfect child).
    assert sorted(set(int(v) for v in fx.df["x1"])) == [0, 2]
    # x0 takes all three values.
    assert sorted(set(int(v) for v in fx.df["x0"])) == [0, 1, 2]


def test_chain_block_structure_and_copy_mechanism() -> None:
    """Chain: per x0 block of 3, x1 := x0 twice + one cyclic deviation; x2 == x1."""
    fx = _fx("m12_chain")
    assert list(fx.df["x2"]) == list(fx.df["x1"])
    rows = list(zip((int(v) for v in fx.df["x0"]), (int(v) for v in fx.df["x1"])))
    expected = [
        (0, 0), (0, 0), (0, 1),
        (1, 1), (1, 1), (1, 2),
        (2, 2), (2, 2), (2, 0),
    ]
    assert rows == expected
    for a, b in rows:
        assert b in (a, (a + 1) % 3)
    # All three values appear in every column.
    for col in ("x0", "x1", "x2"):
        assert sorted(set(int(v) for v in fx.df[col])) == [0, 1, 2]


# --- Separator and association logic ------------------------------------------

# (fixture, unique zero-error separator column, non-separator predictor columns)
_SINGLE_SEPARATOR_CASES = (
    ("m12_sep", "x1", ("x0",)),
    ("m12_fork", "x0", ("x1",)),
    ("m12_chain", "x1", ("x0",)),
)


@pytest.mark.parametrize("source,separator,others", _SINGLE_SEPARATOR_CASES)
def test_unique_zero_error_separator(
    source: str, separator: str, others: tuple[str, ...]
) -> None:
    assert _column_is_zero_error_separator(source, separator)
    for col in others:
        assert not _column_is_zero_error_separator(source, col), (source, col)


@pytest.mark.parametrize("source", ("m12_conj", "m12_disj"))
def test_collider_no_single_column_separates(source: str) -> None:
    for col in _predictors(source):
        assert not _column_is_zero_error_separator(source, col), (source, col)


def test_fork_sibling_is_associated_but_imperfect() -> None:
    assert _column_is_associated("m12_fork", "x1")
    assert not _column_is_zero_error_separator("m12_fork", "x1")


def test_chain_ancestor_is_associated_but_imperfect() -> None:
    assert _column_is_associated("m12_chain", "x0")
    assert not _column_is_zero_error_separator("m12_chain", "x0")
    # The plan's dose: P(pos | x0 = v) = 0, 1/3, 2/3 for v = 0, 1, 2.
    fx = _fx("m12_chain")
    pos = _positive_mask("m12_chain")
    for value, expected_rate in ((0, 0.0), (1, 1 / 3), (2, 2 / 3)):
        rows = [p for v, p in zip(fx.df["x0"], pos) if int(v) == value]
        assert sum(rows) / len(rows) == pytest.approx(expected_rate)


def test_sep_isolated_column_is_unassociated() -> None:
    assert not _column_is_associated("m12_sep", "x0")


def test_conj_isolated_column_is_unassociated() -> None:
    assert not _column_is_associated("m12_conj", "x2")


def test_disj_isolated_column_is_unassociated() -> None:
    assert not _column_is_associated("m12_disj", "x2")


# --- Minimality of the expected rules (conj/disj) ------------------------------


def _covers_all_pos_no_neg(source: str, covered: list[bool]) -> bool:
    pos = _positive_mask(source)
    return all(c for c, p in zip(covered, pos) if p) and not any(
        c for c, p in zip(covered, pos) if not p
    )


@pytest.mark.parametrize("source", ("m12_conj", "m12_disj"))
def test_no_one_literal_rule_is_complete_and_consistent(source: str) -> None:
    for col, val in _one_literal_rules(source):
        covered = _rule_covers(source, [(col, val)])
        assert not _covers_all_pos_no_neg(source, covered), (source, col, val)


def test_conj_expected_two_literal_rule_exactly_covers() -> None:
    covered = _rule_covers("m12_conj", [("x0", 2), ("x1", 2)])
    assert covered == _positive_mask("m12_conj")


def test_disj_expected_two_rule_union_exactly_covers() -> None:
    cov_x0 = _rule_covers("m12_disj", [("x0", 2)])
    cov_x1 = _rule_covers("m12_disj", [("x1", 2)])
    union = [a or b for a, b in zip(cov_x0, cov_x1)]
    assert union == _positive_mask("m12_disj")
    # Each disjunct alone is consistent (no negatives) but incomplete.
    pos = _positive_mask("m12_disj")
    for cov in (cov_x0, cov_x1):
        assert not any(c for c, p in zip(cov, pos) if not p)
        assert not all(c for c, p in zip(cov, pos) if p)


# --- BK encoding (Prolog-free: stage 2 stops before the engine) ----------------


def _cell_for(source: str) -> CellSpec:
    fx = _fx(source)
    return CellSpec(
        experiment_id="M12_stage0_validation",
        dgp=source,
        nodes=fx.nodes,
        edges=fx.edges,
        n=len(fx.df),
        seed=0,
        target=fx.default_target,
        config_hash="sha256:test",
        run_id=f"run_{source}",
        cell_dir_name=f"run_{source}",
        graph_type="handcrafted_table",
        example_split="handcrafted",
        handcrafted_source=source,
    )


def _bk_text(source: str, tmp_path: Path) -> str:
    out = execute_cell_stage2(
        _cell_for(source),
        tmp_path / source,
        graph_type="handcrafted_table",
        bins=3,
        bin_strategy="uniform",
        example_split="handcrafted",
    )
    assert out.outcome == "ok", f"{source} stage2 outcome={out.outcome}"
    assert out.bk_path is not None and out.bk_path.is_file()
    return out.bk_path.read_text(encoding="utf-8")


@pytest.mark.parametrize("source", _ALL_IDS)
def test_bk_uses_value_predicates_for_all_predictors(
    source: str, tmp_path: Path
) -> None:
    text = _bk_text(source, tmp_path)
    for col in _predictors(source):
        assert f"{col}_val_" in text, (source, col)
        assert f"{col}(A) :-" not in text, (source, col)  # no bare binary path
    assert "_bin" not in text  # no continuous binning


@pytest.mark.parametrize("source", _ALL_IDS)
def test_bk_excludes_target(source: str, tmp_path: Path) -> None:
    target = _TARGET[source]
    text = _bk_text(source, tmp_path)
    assert f"Skipping excluded variable: {target}" in text
    assert f"{target}(A) :-" not in text
    assert f"{target}_val_" not in text
