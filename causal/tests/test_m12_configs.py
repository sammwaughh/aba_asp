"""Prolog-free tests for the two M1.2 published-arm configs.

Each arm YAML consults one shipped ``.pl`` config verbatim (via ``prolog_config``)
over feature-BK. These tests assert the configs load, expand to the five M1.2
fixtures (target x2), and reference existing config files. No ABA Learning
(no swipl/clingo).
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

_ARMS = {
    "M12_ecai2024": "configs/ecai2024_config.pl",
    "M12_aamas2025": "configs/aamas2025_config.pl",
}

_FIXTURES = ("m12_sep", "m12_conj", "m12_disj", "m12_fork", "m12_chain")
_EXPECTED_TARGET = {
    "m12_sep": "x2",
    "m12_conj": "x2",
    "m12_disj": "x2",
    "m12_fork": "x2",
    "m12_chain": "x2",
}


@pytest.mark.parametrize("arm", sorted(_ARMS))
def test_arm_config_loads_and_expands(arm: str) -> None:
    path = _EXP_DIR / f"{arm}.yaml"
    cfg = load_config(path)
    assert cfg.experiment_id == arm
    cells = expand_cells(cfg, config_path=path)
    assert len(cells) == 5
    assert {c.dgp for c in cells} == set(_FIXTURES)
    for c in cells:
        assert c.target == _EXPECTED_TARGET[c.dgp], (c.dgp, c.target)
        assert c.graph_type == "handcrafted_table"
        assert c.cell_dir_name == c.dgp
        assert c.cell_dir_name != c.run_id


@pytest.mark.parametrize("arm", sorted(_ARMS))
def test_arm_defaults_prolog_config_and_bk_construction(arm: str) -> None:
    cfg = load_config(_EXP_DIR / f"{arm}.yaml")
    assert cfg.defaults.get("prolog_config") == _ARMS[arm]
    assert float(cfg.defaults.get("prolog_timeout_s")) == 60.0
    assert "default_assumption" not in cfg.defaults
    # The arms consult a config verbatim, so folding options are NOT set here.
    assert "folding_mode" not in cfg.defaults
    assert "folding_steps" not in cfg.defaults


@pytest.mark.parametrize("arm", sorted(_ARMS))
def test_referenced_config_file_exists(arm: str) -> None:
    assert (_REPO_ROOT / _ARMS[arm]).is_file()


def test_arms_have_distinct_config_hashes() -> None:
    from causal.experiments.config import config_hash_from_path

    hashes = {arm: config_hash_from_path(_EXP_DIR / f"{arm}.yaml") for arm in _ARMS}
    assert len(set(hashes.values())) == len(_ARMS)
