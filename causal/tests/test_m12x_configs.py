"""Expanded M1.2 (M12x) YAML expands to the locked 20-cell grid (10 per arm)."""

from __future__ import annotations

from pathlib import Path

import pytest

from causal.experiments.config import expand_cells, load_config

_ROOT = Path(__file__).resolve().parents[1]
_CFG_ECAI = _ROOT / "configs" / "experiments" / "M12x_ecai2024.yaml"
_CFG_AAMAS = _ROOT / "configs" / "experiments" / "M12x_aamas2025.yaml"

_EXPECTED_CELLS = {
    ("m12_u1_separator_copy", "x2"),
    ("m12_u2_collider_min", "x2"),
    ("m12_u3_collider_max", "x2"),
    ("m12_u4_fork_double_copy", "x1"),
    ("m12_u4_fork_double_copy", "x2"),
    ("m12_u5_chain_double_copy", "x1"),
    ("m12_u5_chain_double_copy", "x2"),
    ("m12_u6_g1_and_cone", "x2"),
    ("m12_u6_g1_and_cone", "x3"),
    ("m12_u7_g1_or_cone", "x3"),
}


@pytest.mark.parametrize("cfg_path", [_CFG_ECAI, _CFG_AAMAS])
def test_m12x_expands_to_ten_cells(cfg_path: Path) -> None:
    assert cfg_path.is_file()
    cfg = load_config(cfg_path)
    cells = expand_cells(cfg, config_path=cfg_path)
    assert len(cells) == 10
    pairs = {(c.dgp, c.target) for c in cells}
    assert pairs == _EXPECTED_CELLS
    assert all(c.seed is None for c in cells)
    assert all(c.cell_dir_name == f"{c.dgp}__target-{c.target}" for c in cells)
    assert cfg.grid.seeds == ()
    prolog = Path(cfg.defaults["prolog_config"])
    if not prolog.is_file():
        # configs/ is relative to repo root
        prolog = _ROOT.parent / cfg.defaults["prolog_config"]
    assert prolog.is_file(), cfg.defaults["prolog_config"]


def test_m12x_two_arms_make_twenty_cells() -> None:
    n = 0
    for cfg_path in (_CFG_ECAI, _CFG_AAMAS):
        cfg = load_config(cfg_path)
        n += len(expand_cells(cfg, config_path=cfg_path))
    assert n == 20
