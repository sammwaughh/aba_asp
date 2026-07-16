"""Stage-0 checks for expanded M1.2 (M12x) fixtures U1–U7."""

from __future__ import annotations

from pathlib import Path

import pytest

from causal.experiments.config import CellSpec
from causal.experiments.handcrafted import load_handcrafted
from causal.experiments.handcrafted_m12x import M12X_BUILDERS, M12X_UNIT_TO_KEY
from causal.experiments.run_grid import execute_cell_stage2

_ALL_IDS = sorted(M12X_BUILDERS)

_EXPECTED_EDGES = {
    "m12_u1_separator_copy": ((1, 2),),
    "m12_u2_collider_min": ((0, 2), (1, 2)),
    "m12_u3_collider_max": ((0, 2), (1, 2)),
    "m12_u4_fork_double_copy": ((0, 1), (0, 2)),
    "m12_u5_chain_double_copy": ((0, 1), (1, 2)),
    "m12_u6_g1_and_cone": ((0, 2), (1, 2), (1, 3), (2, 3)),
    "m12_u7_g1_or_cone": ((0, 2), (1, 2), (1, 3), (2, 3)),
}

_EXPECTED_ROWS = {
    "m12_u1_separator_copy": 9,
    "m12_u2_collider_min": 9,
    "m12_u3_collider_max": 9,
    "m12_u4_fork_double_copy": 3,
    "m12_u5_chain_double_copy": 3,
    "m12_u6_g1_and_cone": 9,
    "m12_u7_g1_or_cone": 9,
}

_EXPECTED_TARGETS = {
    "m12_u1_separator_copy": ("x2",),
    "m12_u2_collider_min": ("x2",),
    "m12_u3_collider_max": ("x2",),
    "m12_u4_fork_double_copy": ("x1", "x2"),
    "m12_u5_chain_double_copy": ("x1", "x2"),
    "m12_u6_g1_and_cone": ("x2", "x3"),
    "m12_u7_g1_or_cone": ("x2", "x3"),
}


def _fx(source: str):
    return load_handcrafted(source)


def test_registry_has_seven_units() -> None:
    assert len(M12X_BUILDERS) == 7
    assert set(M12X_UNIT_TO_KEY.values()) == set(M12X_BUILDERS)


@pytest.mark.parametrize("source", _ALL_IDS)
def test_edges_nodes_rows(source: str) -> None:
    fx = _fx(source)
    assert fx.edges == _EXPECTED_EDGES[source]
    assert fx.nodes == (4 if "g1" in source else 3)
    assert len(fx.df) == _EXPECTED_ROWS[source]
    assert fx.resolved_learning_targets() == _EXPECTED_TARGETS[source]


@pytest.mark.parametrize("source", _ALL_IDS)
def test_nonzero_labels_partition(source: str) -> None:
    fx = _fx(source)
    for target in fx.resolved_learning_targets():
        pos, neg = fx.examples_for_target(target)
        values = fx.df[target].astype(int).tolist()
        expect_pos = {i + 1 for i, v in enumerate(values) if v != 0}
        expect_neg = {i + 1 for i, v in enumerate(values) if v == 0}
        got_pos = {int(a[a.index("(") + 1 : -1]) for a in pos}
        got_neg = {int(a[a.index("(") + 1 : -1]) for a in neg}
        assert got_pos == expect_pos
        assert got_neg == expect_neg
        assert got_pos.isdisjoint(got_neg)
        assert got_pos | got_neg == set(range(1, len(values) + 1))
        assert pos and neg


def test_u2_min_table() -> None:
    fx = _fx("m12_u2_collider_min")
    for _, row in fx.df.iterrows():
        assert int(row["x2"]) == min(int(row["x0"]), int(row["x1"]))


def test_u3_max_table() -> None:
    fx = _fx("m12_u3_collider_max")
    for _, row in fx.df.iterrows():
        assert int(row["x2"]) == max(int(row["x0"]), int(row["x1"]))


def test_u6_composition_x3_equals_x2() -> None:
    fx = _fx("m12_u6_g1_and_cone")
    assert (fx.df["x2"] == fx.df["x3"]).all()
    for _, row in fx.df.iterrows():
        assert int(row["x2"]) == min(int(row["x0"]), int(row["x1"]))
        assert int(row["x3"]) == min(int(row["x1"]), int(row["x2"]))


def test_u7_composition_x3_equals_x2() -> None:
    fx = _fx("m12_u7_g1_or_cone")
    assert (fx.df["x2"] == fx.df["x3"]).all()


def test_u1_copy_ignores_x0() -> None:
    fx = _fx("m12_u1_separator_copy")
    assert (fx.df["x2"] == fx.df["x1"]).all()


def test_u4_u5_copies() -> None:
    u4 = _fx("m12_u4_fork_double_copy")
    assert (u4.df["x1"] == u4.df["x0"]).all()
    assert (u4.df["x2"] == u4.df["x0"]).all()
    u5 = _fx("m12_u5_chain_double_copy")
    assert (u5.df["x1"] == u5.df["x0"]).all()
    assert (u5.df["x2"] == u5.df["x1"]).all()


def _cell(source: str, target: str) -> CellSpec:
    fx = _fx(source)
    return CellSpec(
        experiment_id="M12x_stage0",
        dgp=source,
        nodes=fx.nodes,
        edges=fx.edges,
        n=len(fx.df),
        seed=0,
        target=target,
        config_hash="sha256:test",
        run_id=f"run_{source}_{target}",
        cell_dir_name=f"run_{source}_{target}",
        graph_type="handcrafted_table",
        example_split="handcrafted",
        handcrafted_source=source,
    )


def _bk(source: str, target: str, tmp_path: Path, *, nz: bool) -> str:
    out = execute_cell_stage2(
        _cell(source, target),
        tmp_path / f"{source}_{target}_{int(nz)}",
        graph_type="handcrafted_table",
        bins=3,
        bin_strategy="uniform",
        example_split="handcrafted",
        definitional_nz=nz,
    )
    assert out.outcome == "ok", (source, target, out.outcome, out.failure_reason)
    assert out.bk_path is not None
    return out.bk_path.read_text(encoding="utf-8")


@pytest.mark.parametrize(
    "source,target,bk_cols,must_include_descendant",
    [
        ("m12_u1_separator_copy", "x2", ("x0", "x1"), None),
        ("m12_u2_collider_min", "x2", ("x0", "x1"), None),
        ("m12_u5_chain_double_copy", "x1", ("x0", "x2"), "x2"),
        ("m12_u6_g1_and_cone", "x2", ("x0", "x1", "x3"), "x3"),
        ("m12_u7_g1_or_cone", "x2", ("x0", "x1", "x3"), "x3"),
    ],
)
def test_bk_includes_non_targets_and_nz(
    source: str,
    target: str,
    bk_cols: tuple[str, ...],
    must_include_descendant: str | None,
    tmp_path: Path,
) -> None:
    text = _bk(source, target, tmp_path, nz=True)
    assert f"Skipping excluded variable: {target}" in text
    assert f"{target}_val_" not in text
    assert f"{target}_nz" not in text
    for col in bk_cols:
        assert f"{col}_val_" in text
        assert f"{col}_nz(A) :- {col}_val_1(A)." in text
        assert f"{col}_nz(A) :- {col}_val_2(A)." in text
    if must_include_descendant is not None:
        d = must_include_descendant
        assert f"{d}_val_" in text
        assert f"{d}_nz(A) :- {d}_val_1(A)." in text


def test_definitional_nz_off_by_default(tmp_path: Path) -> None:
    text = _bk("m12_u2_collider_min", "x2", tmp_path, nz=False)
    assert "x0_val_" in text
    assert "_nz(A)" not in text
