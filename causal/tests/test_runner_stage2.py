from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from causal.experiments.config import CellSpec
from causal.experiments.run_grid import execute_cell_stage2


def _cell(*, n: int, seed: int, target: str = "x2") -> CellSpec:
    return CellSpec(
        experiment_id="test",
        dgp="G3-chain",
        nodes=3,
        edges=((0, 1), (1, 2)),
        n=n,
        seed=seed,
        target=target,
        config_hash="sha256:test",
        run_id=f"run_{seed}_{n}_{target}",
        cell_dir_name=f"run_{seed}_{n}_{target}",
        graph_type="continuous",
        example_split="median",
    )


def test_stage2_writes_bk_and_binned_continuous(tmp_path: Path) -> None:
    cell = _cell(n=30, seed=42, target="x2")
    out = execute_cell_stage2(
        cell,
        tmp_path / "cell",
        graph_type="continuous",
        bins=2,
        bin_strategy="quantile",
        example_split="median",
    )
    assert out.outcome == "ok"
    assert out.bk_path is not None and out.bk_path.is_file()
    assert out.data_binned_path is not None and out.data_binned_path.is_file()

    text = out.bk_path.read_text(encoding="utf-8")
    assert "Skipping excluded variable: x2" in text
    assert "x0_bin" in text or "x1_bin" in text

    df_binned = pd.read_csv(out.data_binned_path)
    # We should have sample_id and at least one *_bin column
    assert "sample_id" in df_binned.columns
    assert any(c.endswith("_bin") for c in df_binned.columns)

    # Median split should be reasonably balanced for n=30.
    assert len(out.pos_examples) > 0 and len(out.neg_examples) > 0
    assert abs(len(out.pos_examples) - len(out.neg_examples)) <= 1


def test_stage2_discrete_writes_bk_no_binned(tmp_path: Path) -> None:
    cell = _cell(n=20, seed=7, target="x2")
    out = execute_cell_stage2(
        cell,
        tmp_path / "cell",
        graph_type="discrete",
        example_split="median",
    )
    assert out.outcome == "ok"
    assert out.bk_path is not None and out.bk_path.is_file()
    assert out.data_binned_path is None


def _handcrafted_cell(source: str, target: str) -> CellSpec:
    from causal.experiments.handcrafted import load_handcrafted

    fx = load_handcrafted(source)
    return CellSpec(
        experiment_id="test_m12",
        dgp=source,
        nodes=fx.nodes,
        edges=fx.edges,
        n=len(fx.df),
        seed=0,
        target=target,
        config_hash="sha256:test",
        run_id=f"run_{source}",
        cell_dir_name=f"run_{source}",
        graph_type="handcrafted_table",
        example_split="handcrafted",
        handcrafted_source=source,
    )


@pytest.mark.parametrize("source,target,n", [("m12_sep", "x2", 9), ("m12_conj", "x2", 9)])
def test_stage2_domain_predicate_block_present(
    source: str, target: str, n: int, tmp_path: Path
) -> None:
    cell = _handcrafted_cell(source, target)
    out = execute_cell_stage2(
        cell,
        tmp_path / source,
        graph_type="handcrafted_table",
        bins=3,
        bin_strategy="uniform",
        example_split="handcrafted",
        domain_predicate=True,
    )
    assert out.outcome == "ok"
    assert out.bk_path is not None
    text = out.bk_path.read_text(encoding="utf-8")
    # RuleML domain/1 element over sample ids 1..N, plus domain(default).
    assert "domain(default)." in text
    assert "domain(1)." in text
    assert f"domain({n})." in text
    assert f"domain({n + 1})." not in text
    # No default rule, assumption, or contrary is emitted.
    assert "alpha(" not in text
    assert "contrary(" not in text
    assert f"{target}(X) :-" not in text
    # Target still excluded from the feature BK.
    assert f"{target}_val_" not in text
    assert f"Skipping excluded variable: {target}" in text


@pytest.mark.parametrize("source,target", [("m12_sep", "x2"), ("m12_conj", "x2")])
def test_stage2_feature_bk_no_domain_by_default(
    source: str, target: str, tmp_path: Path
) -> None:
    cell = _handcrafted_cell(source, target)
    out = execute_cell_stage2(
        cell,
        tmp_path / source,
        graph_type="handcrafted_table",
        bins=3,
        bin_strategy="uniform",
        example_split="handcrafted",
    )
    assert out.bk_path is not None
    text = out.bk_path.read_text(encoding="utf-8")
    assert "domain(" not in text
    assert "alpha(" not in text
    assert f"{target}(X) :-" not in text
    assert f"Skipping excluded variable: {target}" in text


def test_stage2_empty_split_skips_without_bk(tmp_path: Path) -> None:
    # Force empty split by making target constant and monkeypatching stage1.
    from causal.experiments import run_grid as rg

    cell = _cell(n=10, seed=0, target="x2")
    run_dir = tmp_path / "cell"

    df = pd.DataFrame({"x0": [0.0] * 10, "x1": [0.0] * 10, "x2": [1.0] * 10})
    data_path = run_dir / "data.csv"
    run_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(data_path, index=False)

    def _fake_stage1(*_args, **_kwargs):
        return rg.Stage1Artefacts(data_path=data_path, df=df)

    # Patch stage1 so stage2 sees our constant df.
    orig = rg.execute_cell_stage1
    rg.execute_cell_stage1 = _fake_stage1  # type: ignore[assignment]
    try:
        out = execute_cell_stage2(cell, run_dir, graph_type="continuous", example_split="median")
    finally:
        rg.execute_cell_stage1 = orig  # type: ignore[assignment]

    assert out.outcome == "skipped"
    assert out.bk_path is None

