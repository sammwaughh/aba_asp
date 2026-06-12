"""Prolog-free tests for the QI-001 qualitative summary script.

These tests run the summary generator in pending-run mode (no grid artefacts)
and exercise the recovery classifier directly. They never require swipl, clingo,
or solution files.
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from causal.scripts.qi001_qualitative_summary import (
    build_summary,
    classify_recovery,
    default_config_path,
    main,
    parse_source_id,
)

_ALL_IDS = (
    "qi001_chain_binary",
    "qi001_fork_binary",
    "qi001_collider_binary",
    "qi001_chain_cat3",
    "qi001_fork_cat3",
    "qi001_collider_cat3",
    "qi001_chain_cont3",
    "qi001_fork_cont3",
    "qi001_collider_cont3",
)


def test_build_summary_pending_contains_all_cells() -> None:
    cfg = default_config_path("QI001_motifs_modes")
    markdown, n_cells, n_with = build_summary("QI001_motifs_modes", cfg)
    assert n_cells == 9
    assert n_with == 0  # no grid artefacts in a clean tree
    for source in _ALL_IDS:
        assert source in markdown
    # Expected parent sets are rendered for each motif.
    assert "{x1}" in markdown  # chain
    assert "{x0}" in markdown  # fork
    assert "{x0, x1}" in markdown  # collider
    # Pending markers present; no post-run-only labels.
    assert "Run status: pending" in markdown
    assert "pending run (no grid artefacts found)" in markdown
    # The per-cell recovery label only appears in post-run blocks (the header
    # legend mentions the term, so check for the rendered field prefix).
    assert "- Recovery classification:" not in markdown


def test_main_writes_markdown_file(tmp_path: Path) -> None:
    out = tmp_path / "QI-001_summary.md"
    rc = main(["--experiment", "QI001_motifs_modes", "--output", str(out)])
    assert rc == 0
    assert out.is_file()
    text = out.read_text(encoding="utf-8")
    assert all(source in text for source in _ALL_IDS)
    assert "parent-set recovery via ABA Learning" in text


def test_main_refuses_to_overwrite_human_record() -> None:
    human = _REPO_ROOT / "docs/experiments/qualitative/QI-001.md"
    try:
        main(["--experiment", "QI001_motifs_modes", "--output", str(human)])
    except SystemExit as e:
        assert "refusing to overwrite" in str(e.code)
    else:  # pragma: no cover
        raise AssertionError("expected SystemExit when targeting the human record")


def test_parse_source_id() -> None:
    assert parse_source_id("qi001_chain_binary") == ("chain", "binary")
    assert parse_source_id("qi001_collider_cont3") == ("collider", "cont3")
    assert parse_source_id("nonsense") == ("unknown", "unknown")


def test_classifier_no_output_yet() -> None:
    assert (
        classify_recovery(
            metrics_present=False,
            outcome=None,
            n_target_rules=0,
            recovered=set(),
            expected={"x1"},
        )
        == "no_output_yet"
    )


def test_classifier_exact_parent_recovery() -> None:
    assert (
        classify_recovery(
            metrics_present=True,
            outcome="solved",
            n_target_rules=1,
            recovered={"x1"},
            expected={"x1"},
        )
        == "exact_parent_recovery"
    )


def test_classifier_non_parent_or_proxy() -> None:
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


def test_classifier_subset_superset_mixed() -> None:
    assert (
        classify_recovery(
            metrics_present=True,
            outcome="solved",
            n_target_rules=1,
            recovered={"x0"},
            expected={"x0", "x1"},
        )
        == "parent_subset"
    )
    assert (
        classify_recovery(
            metrics_present=True,
            outcome="solved",
            n_target_rules=1,
            recovered={"x0", "x1"},
            expected={"x0"},
        )
        == "parent_superset"
    )
    assert (
        classify_recovery(
            metrics_present=True,
            outcome="solved",
            n_target_rules=1,
            recovered={"x1", "x0"},
            expected={"x1"},
        )
        == "parent_superset"
    )
    assert (
        classify_recovery(
            metrics_present=True,
            outcome="solved",
            n_target_rules=2,
            recovered={"x0", "x9"},
            expected={"x0", "x1"},
        )
        == "mixed_parent_and_non_parent"
    )


def test_classifier_rote_and_no_solution() -> None:
    assert (
        classify_recovery(
            metrics_present=True,
            outcome="solved",
            n_target_rules=1,
            recovered=set(),
            expected={"x1"},
        )
        == "rote_or_sample_specific"
    )
    assert (
        classify_recovery(
            metrics_present=True,
            outcome="completed_no_solution",
            n_target_rules=0,
            recovered=set(),
            expected={"x1"},
        )
        == "no_solution"
    )
