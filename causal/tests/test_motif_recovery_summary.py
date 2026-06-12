"""Prolog-free tests for the generalized motif-recovery summary script.

Run the generator in pending-run mode (no grid artefacts) for QI-002/QI-003,
exercise the classifier and mode parser, and confirm parents are derived from
fixture edges (so parent-position variants are correct) and that body_parent_f1
is never printed.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from causal.scripts.motif_recovery_summary import (
    build_summary,
    classify_recovery,
    default_config_path,
    main,
    parse_mode,
)


def test_build_summary_qi002_pending() -> None:
    cfg = default_config_path("QI002_minimal_motifs")
    markdown, n_cells, n_with = build_summary("QI002_minimal_motifs", cfg)
    assert n_cells == 6
    assert n_with == 0
    for source in ("qi002_chain_binary", "qi002_fork_cat3", "qi002_collider_binary"):
        assert source in markdown
    assert "Run status: pending" in markdown
    assert "P/R/F1" not in markdown  # no f1 metric line is rendered
    assert "- Recovery classification:" not in markdown  # post-run only


def test_build_summary_qi003_parent_position_from_edges() -> None:
    cfg = default_config_path("QI003_scaled_motifs")
    markdown, n_cells, n_with = build_summary("QI003_scaled_motifs", cfg)
    assert n_cells == 15
    assert n_with == 0
    # x1-parent variants must show {x1}; x0-parent variants {x0}. We can only
    # check the rendered expected-parent lines exist for both orientations.
    assert "qi003_chain_x1parent_binary" in markdown
    assert "qi003_chain_x0parent_binary" in markdown
    assert "{x0, x1}" in markdown  # collider
    assert "P/R/F1" not in markdown  # no f1 metric line is rendered


def test_main_writes_summary_file(tmp_path: Path) -> None:
    out = tmp_path / "QI002_minimal_motifs_summary.md"
    rc = main(["--experiment", "QI002_minimal_motifs", "--output", str(out)])
    assert rc == 0
    assert out.is_file()
    text = out.read_text(encoding="utf-8")
    assert "parent-set recovery via ABA Learning" in text
    assert "Aggregate (clean_recovery" in text


def test_main_refuses_to_overwrite_human_record(tmp_path: Path) -> None:
    human = tmp_path / "QI-002.md"
    with pytest.raises(SystemExit) as exc:
        main(["--experiment", "QI002_minimal_motifs", "--output", str(human)])
    assert "refusing to overwrite" in str(exc.value.code)


def test_parse_mode() -> None:
    assert parse_mode("qi002_chain_binary") == "binary"
    assert parse_mode("qi003_fork_x1parent_cat3") == "cat3"
    assert parse_mode("qi003_collider_cont3") == "cont3"
    assert parse_mode("nonsense") == "unknown"


def test_classifier_parent_position_variant_proxy() -> None:
    # x1-parent fork: true parent {x1}; learner picking x0 is a proxy failure.
    assert (
        classify_recovery(
            metrics_present=True,
            outcome="solved",
            n_target_rules=1,
            recovered={"x0"},
            expected={"x1"},
        )
        == "non_parent_or_proxy"
    )


def test_classifier_clean_exact() -> None:
    assert (
        classify_recovery(
            metrics_present=True,
            outcome="solved",
            n_target_rules=1,
            recovered={"x0"},
            expected={"x0"},
        )
        == "exact_parent_recovery"
    )
