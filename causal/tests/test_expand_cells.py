from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from causal.experiments.config import config_hash_from_path, expand_cells, load_config
from causal.experiments.manifest import close_manifest, open_manifest


def _write_multi_stub(tmp_path: Path) -> Path:
    p = tmp_path / "E00_multi_stub.yaml"
    p.write_text(
        "\n".join(
            [
                "experiment_id: E00_multi_stub",
                "description: stub",
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
                "  - id: G3-fork",
                "    nodes: 3",
                "    edges: [[0,1],[0,2]]",
                "  - id: G3-collider",
                "    nodes: 3",
                "    edges: [[0,2],[1,2]]",
                "  - id: G4-forkchain",
                "    nodes: 4",
                "    edges: [[0,1],[0,2],[2,3]]",
                "  - id: G4-hub",
                "    nodes: 4",
                "    edges: [[0,1],[0,2],[0,3]]",
                "grid:",
                "  n: [25]",
                "  seed: { range: [0, 30] }",
                "  target: all",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return p


def _write_budget_stub(tmp_path: Path) -> Path:
    p = tmp_path / "E00_budget_stub.yaml"
    p.write_text(
        "\n".join(
            [
                "experiment_id: E00_budget_stub",
                "description: stub",
                "defaults:",
                "  graph_type: continuous",
                "  bins: 2",
                "  folding_steps: 30",
                "  prolog_timeout_s: 600",
                "  query_timeout_s: 5",
                "dgps:",
                "  - id: G3-chain",
                "    nodes: 3",
                "    edges: [[0,1],[1,2]]",
                "  - id: G3-fork",
                "    nodes: 3",
                "    edges: [[0,1],[0,2]]",
                "  - id: G3-collider",
                "    nodes: 3",
                "    edges: [[0,2],[1,2]]",
                "  - id: G4-forkchain",
                "    nodes: 4",
                "    edges: [[0,1],[0,2],[2,3]]",
                "  - id: G4-hub",
                "    nodes: 4",
                "    edges: [[0,1],[0,2],[0,3]]",
                "grid:",
                "  n: [12]",
                "  seed: { range: [0, 3] }",
                "  target: all",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return p


def test_expand_cells_multi_count_and_stability(tmp_path: Path) -> None:
    cfg_path = _write_multi_stub(tmp_path)
    cfg = load_config(cfg_path)

    cells1 = expand_cells(cfg, config_path=cfg_path)
    cells2 = expand_cells(cfg, config_path=cfg_path)

    assert len(cells1) == 510  # (3+3+3+4+4) targets * 30 seeds * 1 n
    assert [c.run_id for c in cells1[:20]] == [c.run_id for c in cells2[:20]]
    assert cells1[0].config_hash == cells2[0].config_hash


def test_expand_cells_budget_count(tmp_path: Path) -> None:
    cfg_path = _write_budget_stub(tmp_path)
    cfg = load_config(cfg_path)
    cells = expand_cells(cfg, config_path=cfg_path)
    assert len(cells) == 51  # 17 targets * 3 seeds * 1 n


def test_expand_cells_e00_continuous_smoke_count() -> None:
    cfg_path = _REPO_ROOT / "causal/configs/experiments/E00_continuous_smoke.yaml"
    cfg = load_config(cfg_path)
    cells = expand_cells(cfg, config_path=cfg_path)
    assert cfg.defaults["graph_type"] == "continuous"
    assert cfg.defaults["example_split"] == "median"
    assert len(cells) == 36  # 3 dgps * 3 targets * 4 seeds * 1 n


def test_config_hash_deterministic(tmp_path: Path) -> None:
    cfg_path = _write_multi_stub(tmp_path)
    h1 = config_hash_from_path(cfg_path)
    h2 = config_hash_from_path(cfg_path)
    assert h1.startswith("sha256:")
    assert h1 == h2


def test_manifest_schema_minimum(tmp_path: Path) -> None:
    cfg_path = _write_multi_stub(tmp_path)
    cfg = load_config(cfg_path)
    cells = expand_cells(cfg, config_path=cfg_path)

    out_root = tmp_path / "out" / cfg.experiment_id
    m = open_manifest(out_root, cfg=cfg, config_path=cfg_path, n_cells_planned=len(cells))
    manifest_path = out_root / "manifest.json"
    assert manifest_path.is_file()

    parsed = json.loads(manifest_path.read_text(encoding="utf-8"))
    for k in ("code_commit", "config_hash", "started_at", "finished_at", "outcome_counts"):
        assert k in parsed

    close_manifest(out_root, n_cells_completed=1, n_cells_skipped=0, outcome_counts={"solved": 1})
    parsed2 = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert parsed2["finished_at"] is not None
    assert parsed2["outcome_counts"]["solved"] == 1

