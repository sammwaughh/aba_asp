"""Prolog-free tests for the greedy-folding rerun configs.

The greedy configs are copies of the QI001 / QI002 / QI004 non-deterministic
configs with the single conceptual change ``folding_mode: nd -> greedy``. These
tests assert the cell counts match the originals (9 / 6 / 15), the target stays
``x2``, ``folding_mode`` is ``greedy``, and every other default matches the nd
config. No ABA Learning (no swipl/clingo).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from causal.experiments.config import expand_cells, load_config

_EXP_DIR = _REPO_ROOT / "causal/configs/experiments"

# (nd config stem, greedy config stem, expected cell count)
_CASES = [
    ("QI001_motifs_modes", "QI001_motifs_modes_greedy", 9),
    ("QI002_minimal_motifs", "QI002_minimal_motifs_greedy", 6),
    ("QI004_scaled_motifs_n20", "QI004_scaled_motifs_n20_greedy", 15),
]


@pytest.mark.parametrize("nd_stem,greedy_stem,n_cells", _CASES)
def test_greedy_config_expands_to_expected_cells(
    nd_stem: str, greedy_stem: str, n_cells: int
) -> None:
    path = _EXP_DIR / f"{greedy_stem}.yaml"
    cfg = load_config(path)
    cells = expand_cells(cfg, config_path=path)
    assert cfg.experiment_id == greedy_stem
    assert len(cells) == n_cells
    assert all(c.target == "x2" for c in cells)


@pytest.mark.parametrize("nd_stem,greedy_stem,n_cells", _CASES)
def test_greedy_config_sets_greedy_folding(
    nd_stem: str, greedy_stem: str, n_cells: int
) -> None:
    cfg = load_config(_EXP_DIR / f"{greedy_stem}.yaml")
    assert str(cfg.defaults["folding_mode"]) == "greedy"


@pytest.mark.parametrize("nd_stem,greedy_stem,n_cells", _CASES)
def test_greedy_config_only_changes_folding_mode(
    nd_stem: str, greedy_stem: str, n_cells: int
) -> None:
    nd = load_config(_EXP_DIR / f"{nd_stem}.yaml")
    greedy = load_config(_EXP_DIR / f"{greedy_stem}.yaml")
    # nd config must still say nd (originals untouched).
    assert str(nd.defaults["folding_mode"]) == "nd"
    # Every default except folding_mode is identical.
    keys = set(nd.defaults) | set(greedy.defaults)
    for k in keys:
        if k == "folding_mode":
            continue
        assert nd.defaults.get(k) == greedy.defaults.get(k), f"default {k} differs"
    # Same dgp source set and same grid (seed/target).
    assert {d.source for d in nd.dgps} == {d.source for d in greedy.dgps}
    nd_cells = expand_cells(nd, config_path=_EXP_DIR / f"{nd_stem}.yaml")
    greedy_cells = expand_cells(greedy, config_path=_EXP_DIR / f"{greedy_stem}.yaml")
    assert {c.dgp for c in nd_cells} == {c.dgp for c in greedy_cells}
    assert {c.seed for c in nd_cells} == {c.seed for c in greedy_cells}
    assert {c.target for c in nd_cells} == {c.target for c in greedy_cells}
