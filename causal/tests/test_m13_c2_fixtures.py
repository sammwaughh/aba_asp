"""Stage-0 invariants for M13-C2 BK feature-block order controls."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from causal.experiments.config import CellSpec, expand_cells, load_config
from causal.experiments.handcrafted import load_handcrafted
from causal.experiments.handcrafted_m13 import M13_BUILDERS
from causal.experiments.run_grid import execute_cell_stage2

_ORDER_BY_SOURCE: dict[str, tuple[str, ...]] = {
    "m13_c2_u2_x0_x1": ("x0", "x1"),
    "m13_c2_u2_x1_x0": ("x1", "x0"),
    "m13_c2_u5_x0_x1": ("x0", "x1"),
    "m13_c2_u5_x1_x0": ("x1", "x0"),
    "m13_c2_u7_x0_x1_x2": ("x0", "x1", "x2"),
    "m13_c2_u7_x0_x2_x1": ("x0", "x2", "x1"),
    "m13_c2_u7_x1_x0_x2": ("x1", "x0", "x2"),
    "m13_c2_u7_x1_x2_x0": ("x1", "x2", "x0"),
    "m13_c2_u7_x2_x0_x1": ("x2", "x0", "x1"),
    "m13_c2_u7_x2_x1_x0": ("x2", "x1", "x0"),
}
_FAMILIES: dict[str, tuple[str, ...]] = {
    "u2": ("m13_c2_u2_x0_x1", "m13_c2_u2_x1_x0"),
    "u5": ("m13_c2_u5_x0_x1", "m13_c2_u5_x1_x0"),
    "u7": (
        "m13_c2_u7_x0_x1_x2",
        "m13_c2_u7_x0_x2_x1",
        "m13_c2_u7_x1_x0_x2",
        "m13_c2_u7_x1_x2_x0",
        "m13_c2_u7_x2_x0_x1",
        "m13_c2_u7_x2_x1_x0",
    ),
}
_TARGET_BY_FAMILY = {"u2": "x2", "u5": "x2", "u7": "x3"}
_BASE_SOURCE_BY_FAMILY = {
    "u2": "m12_u2_collider_min",
    "u5": "m12_u5_chain_curated",
    "u7": "m12_u7_diamond_noisy",
}
_SOURCES: tuple[str, ...] = tuple(
    source for family in ("u2", "u5", "u7") for source in _FAMILIES[family]
)
_CONFIG_DIR = Path(__file__).resolve().parents[1] / "configs" / "experiments"
_CONFIGS = (
    _CONFIG_DIR / "M13_c2_bk_order_ecai2024.yaml",
    _CONFIG_DIR / "M13_c2_bk_order_aamas2025.yaml",
)


def _fixture(source: str):
    return load_handcrafted(source)


def _canonical_df(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[:, sorted(df.columns)].reset_index(drop=True)


def _rule_set(bk_text: str) -> frozenset[str]:
    return frozenset(
        line.strip()
        for line in bk_text.splitlines()
        if line.strip() and not line.lstrip().startswith("%")
    )


def _cell(source: str, target: str) -> CellSpec:
    fx = _fixture(source)
    return CellSpec(
        experiment_id="M13_c2_stage0",
        dgp=source,
        nodes=fx.nodes,
        edges=fx.edges,
        n=len(fx.df),
        seed=None,
        target=target,
        config_hash="sha256:test",
        run_id=f"run_{source}",
        cell_dir_name=source,
        graph_type="handcrafted_table",
        example_split="handcrafted",
        handcrafted_source=source,
    )


def test_registry_contains_all_c2_variants() -> None:
    assert set(_SOURCES) <= set(M13_BUILDERS)


@pytest.mark.parametrize("family", ("u2", "u5", "u7"))
def test_family_changes_only_predictor_presentation_order(family: str) -> None:
    target = _TARGET_BY_FAMILY[family]
    base = _fixture(_BASE_SOURCE_BY_FAMILY[family])
    expected_df = _canonical_df(base.df)
    expected_examples = base.examples_for_target(target)

    for source in _FAMILIES[family]:
        fx = _fixture(source)
        pd.testing.assert_frame_equal(_canonical_df(fx.df), expected_df)
        assert fx.edges == base.edges
        assert fx.nodes == base.nodes
        assert fx.resolved_learning_targets() == (target,)
        assert fx.examples_for_target(target) == expected_examples
        assert tuple(column for column in fx.df.columns if column != target) == (
            _ORDER_BY_SOURCE[source]
        )
        assert fx.df.columns[-1] == target


@pytest.mark.parametrize("family", ("u2", "u5", "u7"))
def test_family_stage2_bk_differs_only_by_block_order(
    family: str,
    tmp_path: Path,
) -> None:
    target = _TARGET_BY_FAMILY[family]
    rule_sets: list[frozenset[str]] = []
    examples: list[tuple[tuple[str, ...], tuple[str, ...]]] = []

    for source in _FAMILIES[family]:
        out = execute_cell_stage2(
            _cell(source, target),
            tmp_path / source,
            graph_type="handcrafted_table",
            bins=3,
            bin_strategy="uniform",
            example_split="handcrafted",
        )
        assert out.outcome == "ok", (out.outcome, out.failure_reason)
        assert out.bk_path is not None
        bk_text = out.bk_path.read_text(encoding="utf-8")
        rule_sets.append(_rule_set(bk_text))
        examples.append((out.pos_examples, out.neg_examples))

        positions = [
            bk_text.index(f"Feature predicates for variable: {variable}")
            for variable in _ORDER_BY_SOURCE[source]
        ]
        assert positions == sorted(positions)
        assert f"Skipping excluded variable: {target}" in bk_text
        assert f"{target}_val_" not in bk_text

    assert all(rules == rule_sets[0] for rules in rule_sets[1:])
    assert all(pair == examples[0] for pair in examples[1:])


@pytest.mark.parametrize("config_path", _CONFIGS)
def test_configs_expand_to_all_ten_order_cells(config_path: Path) -> None:
    cfg = load_config(config_path)
    cells = expand_cells(cfg, config_path=config_path)
    assert len(cells) == 10
    assert [cell.dgp for cell in cells] == list(_SOURCES)
    assert [cell.handcrafted_source for cell in cells] == list(_SOURCES)
    assert [cell.target for cell in cells] == [
        "x2",
        "x2",
        "x2",
        "x2",
        "x3",
        "x3",
        "x3",
        "x3",
        "x3",
        "x3",
    ]
