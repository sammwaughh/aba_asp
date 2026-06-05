from __future__ import annotations

import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from causal.experiments.config import ConfigError, ExperimentConfig, load_config
from causal.experiments.dgp import dgp_zoo, get_dgp


def test_invalid_yaml_missing_experiment_id(tmp_path: Path) -> None:
    p = tmp_path / "E99_bad.yaml"
    p.write_text(
        "\n".join(
            [
                "description: bad",
                "defaults: {bins: 2, folding_steps: 1, prolog_timeout_s: 1, query_timeout_s: 1}",
                "dgps: []",
                "grid: {n: [25], seed: {range: [0, 1]}, target: all}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    with pytest.raises(ConfigError, match="experiment_id"):
        load_config(p)


def test_experiment_id_must_match_filename(tmp_path: Path) -> None:
    p = tmp_path / "E99_bad.yaml"
    p.write_text(
        "\n".join(
            [
                "experiment_id: E98_other",
                "defaults: {bins: 2, folding_steps: 1, prolog_timeout_s: 1, query_timeout_s: 1}",
                "dgps: []",
                "grid: {n: [25], seed: {range: [0, 1]}, target: all}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    with pytest.raises(ConfigError, match="filename stem"):
        load_config(p)


def test_load_config_from_infra_fixture(tmp_path: Path) -> None:
    p = tmp_path / "E00_multi_stub.yaml"
    p.write_text(
        "\n".join(
            [
                "experiment_id: E00_multi_stub",
                "description: test fixture",
                "defaults:",
                "  graph_type: continuous",
                "  bins: 2",
                "  folding_steps: 15",
                "  prolog_timeout_s: 120",
                "  query_timeout_s: 5",
                "dgps:",
                "  - id: G3-chain",
                "    nodes: 3",
                "    edges: [[0,1],[1,2]]",
                "grid:",
                "  n: [25]",
                "  seed: { range: [0, 30] }",
                "  target: all",
                "",
            ]
        ),
        encoding="utf-8",
    )
    cfg = load_config(p)
    assert isinstance(cfg, ExperimentConfig)
    assert cfg.experiment_id == "E00_multi_stub"
    assert cfg.grid.seeds == tuple(range(0, 30))
    assert cfg.grid.target == "all"
    assert cfg.dgps[0].id == "G3-chain"


def test_dgp_registry_parents_and_ancestors() -> None:
    assert len(dgp_zoo()) == 5

    fork = get_dgp("G3-fork").ground_truth()
    assert fork.parents_of("x1") == frozenset({"x0"})
    assert fork.ancestors_of("x2") == frozenset({"x0"})

    hub = get_dgp("G4-hub").ground_truth()
    assert hub.parents_of("x3") == frozenset({"x0"})
    assert hub.ancestors_of("x3") == frozenset({"x0"})

