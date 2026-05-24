#!/usr/bin/env python3
"""
Unified test suite for ABA-ASP learning with ArgCausalDisco integration.

This test suite validates the complete integration pipeline:
1. Data generation (ArgCausalDisco)
2. Predicate conversion (data_utils)
3. Background knowledge generation (argcausaldisco_integration)
4. ABA-ASP learning (run_aba_asp)

Test Coverage:
1. Simple handcrafted data (4 samples, clear patterns)
2. Handcrafted exception (assumptions/contraries)
3. Minimal discrete chain data (6-8 samples from ArgCausalDisco)
4. ArgCausalDisco confounder structure (X0->X1, X0->X2; learn all targets)
5. ArgCausalDisco collider structure (X0->X2, X1->X2; learn all targets)
6. Minimal continuous data (8 samples with median split)
7. Continuous confounder (6 samples, median split, 2 bins)
8. Continuous collider (8 samples, median split, 2 bins)
9. Folding-mode comparison
10. Greedy folding: discrete chain (targets X0/X1/X2)
11. Greedy folding: confounder (targets X0/X1/X2)
12. Greedy folding: collider (targets X0/X1/X2)
13. BK ordering sensitivity (chain, target X2): ND changes, greedy stable

Continuous confounder/collider mirror discrete test_02/test_03 but use
simulate_linear_continuous_data, quantile bins, and median E+/E- splits.

Usage:
    pytest test_aba_learning.py -v
    OR
    python test_aba_learning.py
"""

import logging
import ast
import re
import sys
import unittest
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Tuple

import pandas as pd

# Setup paths
THIS_DIR = Path(__file__).resolve().parent
ABA_ASP_ROOT = THIS_DIR.parent
REPO_ROOT = ABA_ASP_ROOT.parent
ARGCAUSALDISCO_ROOT = REPO_ROOT / "ArgCausalDisco"

for p in (REPO_ROOT, ARGCAUSALDISCO_ROOT, THIS_DIR):
    sys.path.insert(0, str(p))

from run_aba_asp import ABASPRunner  # type: ignore
from argcausaldisco_integration import (  # type: ignore
    generate_aba_background_knowledge,
    pick_target_variable,
    _extract_learned_rules,
)
from ArgCausalDisco.utils.data_utils import (  # type: ignore
    simulate_discrete_data,
    simulate_linear_continuous_data,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("test_aba_learning")


_OUTPUT_ROOT = THIS_DIR / "outputs" / "aba_learning"


def _get_test_output_dir(test_name: str) -> Path:
    """Return a per-test output directory under `outputs/aba_learning/`.

    We keep artifacts separated to make debugging easier and to avoid the
    shared `aba_learning/` directory becoming cluttered.
    """

    safe = re.sub(r"[^a-zA-Z0-9_.-]+", "_", test_name).strip("_")
    return _OUTPUT_ROOT / safe


# Accumulate ABAF coverage stats across the whole test suite.
_ABAF_COVERAGE = {
    "total_learned_lines": 0,
    "assumptions": 0,
    "contraries": 0,
    "alpha_mentions": 0,
    "c_alpha_mentions": 0,
    "runs": 0,
    "runs_with_assumption": 0,
    "runs_with_contrary": 0,
}


_VAR_PREFIX_RE = re.compile(r"^x\d+$")


def _parse_sample_id(atom: str) -> int:
    """Parse x2(3) -> 3."""
    m = re.search(r"\((\d+)\)", atom)
    if not m:
        raise ValueError(f"Could not parse sample id from atom: {atom}")
    return int(m.group(1))


def _parse_bk_feature_map(bk_path: Path) -> dict:
    """Parse BK lines like `x0_val_7(A) :- A=2.` into per-sample feature sets."""
    feature_map: dict[int, set[str]] = {}
    # Matches: pred(A) :- A=12.
    pat = re.compile(r"^\s*([a-zA-Z_][a-zA-Z0-9_]*)\(A\)\s*:-\s*A\s*=\s*(\d+)\s*\.\s*$")
    for line in bk_path.read_text().splitlines():
        if not line or line.startswith("%"):
            continue
        m = pat.match(line)
        if not m:
            continue
        pred = m.group(1)
        sid = int(m.group(2))
        feature_map.setdefault(sid, set()).add(pred)
    return feature_map


def _write_bk_with_reordered_feature_sections(
    *,
    src_bk_path: Path,
    dst_bk_path: Path,
    feature_order: List[str],
) -> None:
    """Rewrite a BK file so `% Feature predicates for variable: xk` sections follow `feature_order`.

    This is useful for checking whether Prolog/ABA-ASP behavior depends on BK line ordering.
    The transformation preserves all other content, and updates the trailing reproducibility
    comment (the `aba_asp('...')` line) to point at `dst_bk_path`.
    """

    lines = src_bk_path.read_text().splitlines(keepends=True)
    header_pat = re.compile(r"^% Feature predicates for variable: (x\d+)\s*$")

    header_idxs: List[Tuple[int, str]] = []
    for idx, line in enumerate(lines):
        m = header_pat.match(line.rstrip("\n"))
        if m:
            header_idxs.append((idx, m.group(1)))

    if not header_idxs:
        dst_bk_path.write_text("".join(lines))
        return

    blocks: dict[str, List[str]] = {}
    for i, (start_idx, var) in enumerate(header_idxs):
        end_idx = header_idxs[i + 1][0] if i + 1 < len(header_idxs) else len(lines)
        blocks[var] = lines[start_idx:end_idx]

    prefix = lines[: header_idxs[0][0]]
    suffix = []
    # Keep any content after the last feature block that is not part of it.
    # (In practice, this includes the "Skipping excluded variable" and the aba_asp(...) comment.)
    last_end = header_idxs[-1][0] + len(blocks[header_idxs[-1][1]])
    suffix = lines[last_end:]

    ordered_vars: List[str] = []
    seen: set[str] = set()
    for v in feature_order:
        if v in blocks and v not in seen:
            ordered_vars.append(v)
            seen.add(v)
    # Append any remaining feature blocks in their original order.
    for _, v in header_idxs:
        if v in blocks and v not in seen:
            ordered_vars.append(v)
            seen.add(v)

    out_lines: List[str] = []
    out_lines.extend(prefix)
    for v in ordered_vars:
        out_lines.extend(blocks[v])
    out_lines.extend(suffix)

    # Update the trailing reproducibility comment to use the destination path.
    # Keep the rest (examples) identical.
    repro_pat = re.compile(r"^%\s*aba_asp\('\s*[^']+\s*'\s*,")
    for i, line in enumerate(out_lines):
        if repro_pat.match(line.rstrip("\n")):
            out_lines[i] = re.sub(
                r"^%\s*aba_asp\('\s*[^']+\s*'",
                f"% aba_asp('{dst_bk_path.as_posix()}'",
                line,
                count=1,
            )

    dst_bk_path.write_text("".join(out_lines))


def _rule_holds_for_sample(rule: str, sample_id: int, sample_features: set[str]) -> bool:
    """Evaluate whether a rule body holds for a specific sample.

    This is a *syntactic* coverage check over BK-derived feature predicates.
    - Treats `alpha_*` as always satisfiable (assumptions), so they do not block coverage.
    - Ignores built-ins like `A=1`.
    """
    if ":-" not in rule:
        return False
    functors = _predicate_names_in_body(rule)
    for f in functors:
        if not f:
            continue
        if f.startswith("alpha"):
            continue
        # Some solutions may contain c_alpha_* rules; they are not target rules typically.
        if f.startswith("c_alpha"):
            continue
        if f not in sample_features:
            return False
    return True


def _example_coverage_report(
    *,
    target: str,
    bk_path: Path,
    learned_rules: List[str],
    pos_examples: List[str],
    neg_examples: List[str],
    max_rule_lines: int = 8,
) -> dict:
    """Log how well learned target rules cover E+/E- for this run."""
    feature_map = _parse_bk_feature_map(bk_path)
    target_rules = [r for r in learned_rules if r.startswith(f"{target}(A)")]

    pos_ids = [_parse_sample_id(a) for a in pos_examples]
    neg_ids = [_parse_sample_id(a) for a in neg_examples]

    def _predict(sample_id: int) -> bool:
        feats = feature_map.get(sample_id, set())
        return any(_rule_holds_for_sample(r, sample_id, feats) for r in target_rules)

    tp = sum(1 for i in pos_ids if _predict(i))
    fn = len(pos_ids) - tp
    fp = sum(1 for i in neg_ids if _predict(i))
    tn = len(neg_ids) - fp

    total = len(pos_ids) + len(neg_ids)
    acc = (tp + tn) / total if total else 0.0
    pos_cov = tp / len(pos_ids) if pos_ids else 0.0
    neg_cov = tn / len(neg_ids) if neg_ids else 0.0

    logger.info(
        "Coverage(%s): TP=%d FN=%d | TN=%d FP=%d | acc=%.3f | pos_cov=%.3f | neg_cov=%.3f",
        target,
        tp,
        fn,
        tn,
        fp,
        acc,
        pos_cov,
        neg_cov,
    )

    # Per-rule support (how many E+/E- each displayed rule fires on)
    # We compute support for target rules; non-target lines get 0/0.
    shown_rules = learned_rules[:max_rule_lines]
    if shown_rules:
        logger.info("Rule support(%s): showing up to %d rules", target, max_rule_lines)
        for r in shown_rules:
            if r.startswith(f"{target}(A)"):
                r_pos = sum(1 for i in pos_ids if _rule_holds_for_sample(r, i, feature_map.get(i, set())))
                r_neg = sum(1 for i in neg_ids if _rule_holds_for_sample(r, i, feature_map.get(i, set())))
            else:
                r_pos, r_neg = 0, 0
            logger.info("  pos=%d neg=%d | %s", r_pos, r_neg, r)

    return {
        "TP": tp,
        "FN": fn,
        "TN": tn,
        "FP": fp,
        "acc": acc,
        "pos_cov": pos_cov,
        "neg_cov": neg_cov,
    }


def _format_edges(edges: set) -> str:
    """Format a set of edges like {(0,1),(1,2)} into 'x0→x1, x1→x2'."""
    if not edges:
        return "(none)"
    ordered = sorted(edges)
    return ", ".join([f"x{s}→x{t}" for s, t in ordered])


def _format_edges_dag(edges: set) -> str:
    """Format edges into 'X0->X1, X1->X2' (requested log style)."""
    if not edges:
        return "(none)"
    ordered = sorted(edges)
    return ", ".join([f"X{s}->X{t}" for s, t in ordered])


def _parents_from_edges(target: str, edges: set) -> List[str]:
    """Return direct parents (as 'xk') for a target like 'x2'."""
    try:
        t = int(target[1:])
    except Exception:
        return []
    parents = sorted({f"x{s}" for s, dst in edges if dst == t})
    return parents


def _ancestors_from_edges(target: str, edges: set) -> List[str]:
    """Return all ancestors (as 'xk') for a target like 'x2' in a small DAG."""
    try:
        t = int(target[1:])
    except Exception:
        return []
    reverse_adj: dict[int, set[int]] = {}
    for s, dst in edges:
        reverse_adj.setdefault(dst, set()).add(s)

    ancestors: set[int] = set()
    stack = list(reverse_adj.get(t, set()))
    while stack:
        node = stack.pop()
        if node in ancestors:
            continue
        ancestors.add(node)
        stack.extend(list(reverse_adj.get(node, set())))
    return sorted([f"x{a}" for a in ancestors])


def _rule_body_prefixes(rule: str) -> set:
    functors = _predicate_names_in_body(rule)
    prefixes = set()
    for f in functors:
        prefixes.add(f.split("_", 1)[0])
    return prefixes


def _correspondence_stats(target: str, learned_rules: List[str], gt_edges: set) -> dict:
    """Compute small, readable correspondence stats vs the GT DAG.

    This is *not* DAG discovery; we simply check whether learned target rules
    reference predicates derived from direct parents / ancestors.
    """
    target_rules = [r for r in learned_rules if r.startswith(f"{target}(A)")]
    n_target_rules, n_trivial, n_nontrivial = _summarize_target_rule_triviality(target, learned_rules)

    parents = set(_parents_from_edges(target, gt_edges))
    ancestors = set(_ancestors_from_edges(target, gt_edges))
    # Ancestors includes parents; for reporting, we separate them.
    ancestors_only = ancestors - parents

    n_parent_hit = 0
    n_ancestor_only_hit = 0
    n_offgraph_var_hit = 0

    for r in target_rules:
        prefixes = _rule_body_prefixes(r)
        if prefixes & parents:
            n_parent_hit += 1
        if prefixes & ancestors_only:
            n_ancestor_only_hit += 1

        # "Off-graph variable" here means an xK variable not in {target}∪ancestors.
        var_prefixes = {p for p in prefixes if _VAR_PREFIX_RE.match(p or "")}
        allowed = set([target]) | ancestors
        if any(v not in allowed for v in var_prefixes):
            n_offgraph_var_hit += 1

    return {
        "target_rules": n_target_rules,
        "trivial": n_trivial,
        "nontrivial": n_nontrivial,
        "parent_hit": n_parent_hit,
        "ancestor_only_hit": n_ancestor_only_hit,
        "offgraph_var_hit": n_offgraph_var_hit,
        "parents": sorted(parents),
        "ancestors": sorted(ancestors),
    }


def _abaf_component_stats(learned_rules: List[str]) -> dict:
    assumptions = [r for r in learned_rules if r.startswith("assumption(")]
    contraries = [r for r in learned_rules if r.startswith("contrary(")]
    alpha_mentions = [r for r in learned_rules if "alpha_" in r]
    c_alpha_mentions = [r for r in learned_rules if "c_alpha" in r]
    return {
        "assumptions": len(assumptions),
        "contraries": len(contraries),
        "alpha_mentions": len(alpha_mentions),
        "c_alpha_mentions": len(c_alpha_mentions),
    }


def _record_abaf_coverage(learned_rules: List[str]) -> None:
    stats = _abaf_component_stats(learned_rules)
    _ABAF_COVERAGE["runs"] += 1
    _ABAF_COVERAGE["total_learned_lines"] += len(learned_rules)
    _ABAF_COVERAGE["assumptions"] += stats["assumptions"]
    _ABAF_COVERAGE["contraries"] += stats["contraries"]
    _ABAF_COVERAGE["alpha_mentions"] += stats["alpha_mentions"]
    _ABAF_COVERAGE["c_alpha_mentions"] += stats["c_alpha_mentions"]
    if stats["assumptions"] > 0:
        _ABAF_COVERAGE["runs_with_assumption"] += 1
    if stats["contraries"] > 0:
        _ABAF_COVERAGE["runs_with_contrary"] += 1


def _log_run_header(title: str, *, dgp: str, gt_edges: set | None = None, n_samples: int | None = None) -> None:
    line = "-" * 78
    logger.info("\n%s", line)
    if n_samples is None:
        logger.info("RUN: %s", title)
    else:
        logger.info("RUN: %s | n=%s", title, n_samples)
    logger.info("DGP: %s", dgp)
    if gt_edges is not None:
        # Keep this single DAG line to avoid repetition in logs.
        logger.info("DAG: %s", _format_edges_dag(gt_edges))
    logger.info("%s", line)


@dataclass
class _TargetSummary:
    target: str
    variant: str | None = None
    learned_delta_rules: int | None = None
    target_rules: int | None = None
    trivial_label: str | None = None
    triv_count: int | None = None
    nontriv_count: int | None = None
    coverage: str | None = None
    deps: str | None = None
    corr: str | None = None
    abaf: str | None = None
    rules: list[str] = field(default_factory=list)
    rule_support: dict[str, tuple[int, int]] = field(default_factory=dict)


@dataclass
class _RunSummary:
    title: str
    dgp: str | None = None
    dag: str | None = None
    targets: list[_TargetSummary] = field(default_factory=list)
    folding_rows: list[dict] = field(default_factory=list)
    folding_unique: str | None = None
    folding_groups: list[str] = field(default_factory=list)
    folding_theories: list[dict] = field(default_factory=list)


class _LogCaptureHandler(logging.Handler):
    """Capture log messages (message-only, no timestamps) for summary rendering."""

    def __init__(self) -> None:
        super().__init__()
        self.messages: list[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        try:
            self.messages.append(record.getMessage())
        except Exception:
            # Never let summary capture break tests.
            pass


def _parse_run_summaries(messages: list[str]) -> list[_RunSummary]:
    """Parse key info from the test logs into structured summaries."""
    runs: list[_RunSummary] = []
    current_run: _RunSummary | None = None
    current_variant: str | None = None
    current_target: _TargetSummary | None = None

    re_run = re.compile(r"^RUN:\s+(.*)$")
    re_dgp = re.compile(r"^DGP:\s+(.*)$")
    re_dag = re.compile(r"^DAG:\s+(.*)$")
    re_bins = re.compile(r"bins\s*=\s*(\d+)")
    re_learned = re.compile(r"^Learned delta rules for\s+([a-zA-Z0-9_]+):\s+(\d+)")
    re_triv = re.compile(r"^Triviality for\s+([a-zA-Z0-9_]+):\s+(.*)$")
    re_triv_fields = re.compile(r"rules=(\d+)\s+triv=(\d+)\s+nontriv=(\d+)\s+=>\s+(\w+)")
    re_cov = re.compile(r"^Coverage\(([a-zA-Z0-9_]+)\):\s+(.*)$")
    re_deps = re.compile(r"^Dependencies \(target rule prefixes\):\s+(.*)$")
    re_corr = re.compile(r"^Corr vs GT:\s+(.*)$")
    re_abaf = re.compile(r"^ABAF\(delta\):\s+(.*)$")
    re_rule_line = re.compile(r"^\s{2}(.+)$")
    re_rule_support_hdr = re.compile(r"^Rule support\(([a-zA-Z0-9_]+)\):\s+(.*)$")
    re_support_line = re.compile(r"^pos=(\d+)\s+neg=(\d+)\s+\|\s+(.+)$")

    re_mode_cov = re.compile(
        r"^mode=(\w+)\s+\|\s+learned=(\d+)\s+\|\s+deps=(.+?)\s+\|\s+GT\s+parent=(\d+)\s+anc_only=(\d+)\s+offgraph=(\d+)\s+\|\s+TP=(\d+)\s+FN=(\d+)\s+\|\s+TN=(\d+)\s+FP=(\d+)\s+\|\s+acc=([0-9.]+)\s+\|\s+pos_cov=([0-9.]+)\s+\|\s+neg_cov=([0-9.]+)\s+\|\s+asm=(\d+)\s+ctr=(\d+)\s*$"
    )
    re_mode = re.compile(
        r"^mode=(\w+)\s+\|\s+learned=(\d+)\s+\|\s+deps=(.+?)\s+\|\s+GT\s+parent=(\d+)\s+anc_only=(\d+)\s+offgraph=(\d+)\s*$"
    )
    re_unique = re.compile(r"^Folding-mode uniqueness:\s+(.*)$")
    re_folding_group = re.compile(r"^Folding-mode theory group:\s+modes=([^|]+)\|\s+delta_lines=(\d+)\s*$")
    re_folding_theory_hdr = re.compile(r"^Folding-mode theory rules:\s+modes=([^|]+)\|\s+delta_lines=(\d+)\s*$")

    in_rules_block = False
    in_folding_theory_block = False
    current_folding_theory: dict | None = None
    for raw in messages:
        line = (raw or "").rstrip("\n")
        stripped = line.strip()
        if not stripped:
            continue

        if in_folding_theory_block and current_run is not None and current_folding_theory is not None:
            mr = re_rule_line.match(line)
            if mr:
                rule_text = mr.group(1).strip()
                if rule_text:
                    rules = current_folding_theory.setdefault("rules", [])
                    if len(rules) < 60:
                        rules.append(rule_text)
                continue
            in_folding_theory_block = False
            current_folding_theory = None

        m = re_run.match(stripped)
        if m:
            current_run = _RunSummary(title=m.group(1).strip())
            runs.append(current_run)
            current_variant = None
            current_target = None
            in_rules_block = False
            continue

        if current_run is None:
            continue

        m = re_dgp.match(stripped)
        if m:
            current_run.dgp = m.group(1).strip()
            continue

        m = re_dag.match(stripped)
        if m:
            current_run.dag = m.group(1).strip()
            continue

        if stripped.startswith("Continuous bins experiment"):
            # Normalize variant label to e.g. "bins=3".
            mb = re_bins.search(stripped)
            current_variant = f"bins={mb.group(1)}" if mb else stripped.replace("Continuous bins experiment:", "").strip()
            current_target = None
            in_rules_block = False
            continue

        if stripped.startswith("BK ordering experiment"):
            # Normalize variant label to whatever follows the colon, e.g.
            # "nd/orig" or "greedy/swapped".
            current_variant = stripped.replace("BK ordering experiment:", "").strip()
            current_target = None
            in_rules_block = False
            continue

        m = re_learned.match(stripped)
        if m:
            target = m.group(1)
            learned_n = int(m.group(2))
            current_target = _TargetSummary(target=target, variant=current_variant)
            current_target.learned_delta_rules = learned_n
            current_run.targets.append(current_target)
            in_rules_block = True
            continue

        if in_rules_block:
            # Allow the ABAF(delta) line that appears between header and indented rules.
            mab = re_abaf.match(stripped)
            if mab and current_target is not None:
                current_target.abaf = mab.group(1).strip()
                continue

            mr = re_rule_line.match(line)
            # Keep only the immediately following indented rule lines.
            if mr and current_target is not None:
                rule_text = mr.group(1).strip()
                if rule_text:
                    # Cap rules shown in summary.
                    if len(current_target.rules) < 12:
                        current_target.rules.append(rule_text)
                continue

            # End of rules block once we hit a non-indented, non-ABAF line.
            in_rules_block = False

        m = re_triv.match(stripped)
        if m and current_target is not None and m.group(1) == current_target.target:
            raw_triv = m.group(2).strip()
            mf = re_triv_fields.search(raw_triv)
            if mf:
                current_target.target_rules = int(mf.group(1))
                current_target.triv_count = int(mf.group(2))
                current_target.nontriv_count = int(mf.group(3))
                current_target.trivial_label = mf.group(4)
            else:
                # Fallback: keep the raw string as the label.
                current_target.trivial_label = raw_triv
            continue

        m = re_cov.match(stripped)
        if m and current_target is not None and m.group(1) == current_target.target:
            current_target.coverage = m.group(2).strip()
            continue

        m = re_deps.match(stripped)
        if m and current_target is not None:
            current_target.deps = m.group(1).strip()
            continue

        m = re_corr.match(stripped)
        if m and current_target is not None:
            current_target.corr = m.group(1).strip()
            continue

        m = re_abaf.match(stripped)
        if m and current_target is not None:
            current_target.abaf = m.group(1).strip()
            continue

        m = re_mode_cov.match(stripped)
        if m:
            current_run.folding_rows.append(
                {
                    "mode": m.group(1),
                    "learned": int(m.group(2)),
                    "deps": m.group(3).strip(),
                    "parent": int(m.group(4)),
                    "anc_only": int(m.group(5)),
                    "offgraph": int(m.group(6)),
                    "TP": int(m.group(7)),
                    "FN": int(m.group(8)),
                    "TN": int(m.group(9)),
                    "FP": int(m.group(10)),
                    "acc": float(m.group(11)),
                    "pos_cov": float(m.group(12)),
                    "neg_cov": float(m.group(13)),
                    "asm": int(m.group(14)),
                    "ctr": int(m.group(15)),
                }
            )
            continue

        m = re_mode.match(stripped)
        if m:
            current_run.folding_rows.append(
                {
                    "mode": m.group(1),
                    "learned": int(m.group(2)),
                    "deps": m.group(3).strip(),
                    "parent": int(m.group(4)),
                    "anc_only": int(m.group(5)),
                    "offgraph": int(m.group(6)),
                }
            )
            continue

        m = re_unique.match(stripped)
        if m:
            current_run.folding_unique = m.group(1).strip()
            continue

        m = re_folding_group.match(stripped)
        if m and current_run is not None:
            modes = m.group(1).strip()
            delta_lines = m.group(2).strip()
            current_run.folding_groups.append(f"modes={modes} | delta={delta_lines}")
            continue

        m = re_folding_theory_hdr.match(stripped)
        if m and current_run is not None:
            current_folding_theory = {
                "modes": m.group(1).strip(),
                "delta": int(m.group(2)),
                "rules": [],
            }
            current_run.folding_theories.append(current_folding_theory)
            in_folding_theory_block = True
            continue

        m = re_rule_support_hdr.match(stripped)
        if m and current_target is not None and m.group(1) == current_target.target:
            # Next "support:" lines are for this target; we just capture a few.
            continue

        m = re_support_line.match(stripped)
        if m and current_target is not None:
            # Store per-rule support; defaulting happens at render time.
            if len(current_target.rule_support) < 24:
                pos = int(m.group(1))
                neg = int(m.group(2))
                rule = m.group(3).strip()
                if rule:
                    current_target.rule_support[rule] = (pos, neg)
            continue

    return runs


def _render_run_summaries(runs: list[_RunSummary], result: unittest.result.TestResult) -> str:
    lines: list[str] = []
    lines.append("=" * 70)
    lines.append("TESTs SUMMARY")
    lines.append("=" * 70)
    lines.append(
        f"Result: {'PASS' if result.wasSuccessful() else 'FAIL'} | "
        f"run={result.testsRun} fail={len(result.failures)} err={len(result.errors)} skip={len(getattr(result, 'skipped', []))}"
    )

    def _fmt_target_name(t: str) -> str:
        return t.upper() if t.startswith("x") else t

    def _parse_deps(d: str | None) -> dict:
        if not d:
            return {}
        s = d.strip()
        if s.startswith("{"):
            try:
                parsed = ast.literal_eval(s)
                return parsed if isinstance(parsed, dict) else {}
            except Exception:
                return {}
        # Fallback: parse a compact format like "x0=4 alpha=2".
        out: dict[str, int] = {}
        for tok in s.split():
            if "=" not in tok:
                continue
            k, v = tok.split("=", 1)
            try:
                out[k.strip()] = int(v)
            except Exception:
                continue
        return out

    def _parse_corr(c: str | None) -> dict[str, int]:
        if not c:
            return {"parent": 0, "anc_only": 0, "offgraph": 0, "nontriv": 0}
        out = {"parent": 0, "anc_only": 0, "offgraph": 0, "nontriv": 0}
        m = re.search(r"parent=(\d+)\s+anc_only=(\d+)\s+offgraph=(\d+)", c)
        if m:
            out["parent"] = int(m.group(1))
            out["anc_only"] = int(m.group(2))
            out["offgraph"] = int(m.group(3))
        m2 = re.search(r"nontriv=(\d+)", c)
        if m2:
            out["nontriv"] = int(m2.group(1))
        return out

    def _parse_cov(cov: str | None) -> dict[str, float]:
        """Parse the Coverage(...) payload into a few stable numeric fields."""
        if not cov:
            return {}
        # Example payload:
        #   TP=2 FN=0 | TN=2 FP=1 | acc=0.800 | pos_cov=1.000 | neg_cov=0.667
        m = re.search(
            r"TP=(\d+)\s+FN=(\d+)\s+\|\s+TN=(\d+)\s+FP=(\d+)\s+\|\s+acc=([0-9.]+)\s+\|\s+pos_cov=([0-9.]+)\s+\|\s+neg_cov=([0-9.]+)",
            cov,
        )
        if not m:
            return {}
        return {
            "TP": float(m.group(1)),
            "FN": float(m.group(2)),
            "TN": float(m.group(3)),
            "FP": float(m.group(4)),
            "acc": float(m.group(5)),
            "pos_cov": float(m.group(6)),
            "neg_cov": float(m.group(7)),
        }

    # Aggregate how often target rules mention the target itself (via deps[target]).
    total_rules = 0
    total_self = 0

    for i, run in enumerate(runs, start=1):
        lines.append("")
        lines.append(f"[{i}] {run.title}")
        if run.dgp:
            lines.append(f"  DGP: {run.dgp}")
        if run.dag:
            lines.append(f"  DAG: {run.dag}")
        if not run.targets:
            # Some runs (folding-mode comparison) don't log per-target learned-rule blocks.
            if run.folding_rows:
                lines.append("  Folding modes:")
                if run.folding_unique:
                    lines.append(f"    Uniqueness: {run.folding_unique}")
                if run.folding_theories:
                    lines.append("    Unique theories:")
                    for th in run.folding_theories:
                        lines.append(f"      - modes={th['modes']} | delta={th['delta']}")
                        for r in th.get("rules", []):
                            lines.append(f"          {r}")
                elif run.folding_groups:
                    lines.append("    Unique theories:")
                    for g in run.folding_groups:
                        lines.append(f"      - {g}")
                for row in run.folding_rows:
                    cov = ""
                    if all(k in row for k in ("TP", "FN", "TN", "FP", "acc", "pos_cov", "neg_cov")):
                        cov = (
                            f" | TP={row['TP']} FN={row['FN']}"
                            f" | TN={row['TN']} FP={row['FP']}"
                            f" | acc={float(row['acc']):.3f}"
                            f" | pos_cov={float(row['pos_cov']):.3f}"
                            f" | neg_cov={float(row['neg_cov']):.3f}"
                        )
                    abaf = ""
                    if "asm" in row and "ctr" in row:
                        abaf = f" | asm={row['asm']} ctr={row['ctr']}"
                    lines.append(
                        f"    - {row['mode']}: delta={row['learned']} | parent={row['parent']} anc_only={row['anc_only']} offgraph={row['offgraph']} | deps={row['deps']}" + cov + abaf
                    )
            continue
        for t in run.targets:
            variant = f" ({t.variant})" if t.variant else ""
            rules_n = t.target_rules if t.target_rules is not None else 0
            delta_n = int(t.learned_delta_rules) if t.learned_delta_rules is not None else 0
            nontriv_n = t.nontriv_count
            if nontriv_n is None:
                nontriv_n = _parse_corr(t.corr).get("nontriv", 0)
            corr_stats = _parse_corr(t.corr)
            deps_dict = _parse_deps(t.deps)
            self_n = int(deps_dict.get(t.target, 0) or 0)
            asm_n = 0
            if t.abaf:
                m_asm = re.search(r"asm=(\d+)", t.abaf)
                if m_asm:
                    asm_n = int(m_asm.group(1))

            if t.target_rules is not None:
                total_rules += int(rules_n)
                total_self += self_n

            head_parts: list[str] = [
                f"rules={rules_n}",
                f"delta={delta_n}",
                f"nontrivial={int(nontriv_n or 0)}",
                f"self={self_n}",
                f"parent={corr_stats['parent']}",
                f"anc_only={corr_stats['anc_only']}",
                f"offgraph={corr_stats['offgraph']}",
                f"asm={asm_n}",
            ]

            cov_stats = _parse_cov(t.coverage)
            cov = ""
            if cov_stats:
                cov = (
                    f" | TP={int(cov_stats['TP'])} FN={int(cov_stats['FN'])}"
                    f" | TN={int(cov_stats['TN'])} FP={int(cov_stats['FP'])}"
                    f" | acc={cov_stats['acc']:.3f}"
                    f" | pos_cov={cov_stats['pos_cov']:.3f}"
                    f" | neg_cov={cov_stats['neg_cov']:.3f}"
                )
            lines.append(
                f"  - Target={_fmt_target_name(t.target)}{variant}: "
                + ", ".join(head_parts)
                + cov
            )

            if t.rules:
                lines.append("    Rules:")
                for r in t.rules:
                    pos, neg = t.rule_support.get(r, (0, 0))
                    lines.append(f"      {r} | support: pos={pos} neg={neg}")

    lines.append("=" * 70)
    if total_rules:
        lines.insert(
            4,
            f"Target-in-body (self): {total_self}/{total_rules} target rules mention their own xk_* predicates",
        )
    return "\n".join(lines)


def _log_learned_rules_block(target: str, learned_rules: List[str], *, max_lines: int = 12) -> None:
    shown = learned_rules[:max_lines]
    suffix = "" if len(learned_rules) <= max_lines else f" (showing first {max_lines})"
    logger.info("Learned delta rules for %s: %d%s", target, len(learned_rules), suffix)
    abaf = _abaf_component_stats(learned_rules)
    logger.info(
        "ABAF(delta): asm=%d ctr=%d alpha_mentions=%d c_alpha_mentions=%d",
        abaf["assumptions"],
        abaf["contraries"],
        abaf["alpha_mentions"],
        abaf["c_alpha_mentions"],
    )
    for rule in shown:
        logger.info("  %s", rule)


def _log_triviality(target: str, learned_rules: List[str]) -> None:
    n_rules, n_trivial, n_nontrivial = _summarize_target_rule_triviality(target, learned_rules)
    label = "TRIVIAL" if (n_rules > 0 and n_nontrivial == 0) else "NONTRIVIAL"
    logger.info(
        "Triviality for %s: rules=%d triv=%d nontriv=%d => %s",
        target,
        n_rules,
        n_trivial,
        n_nontrivial,
        label,
    )


def _extract_prolog_counts(stdout: str) -> dict:
    """Parse key numeric stats from ABA-ASP stdout for readability.

    Note: ABA-ASP's internal BK/ABA counts are *Prolog-level* notions.
    They don't necessarily line up 1:1 with our "delta lines" extracted from
    the solution file (which can include assumptions/contraries and utility).
    """
    out: dict = {}
    if not stdout:
        return out

    patterns = {
        "bk_rules": r"BK size \(rules\):\s+(\d+)",
        "aba_rules": r"ABA size \(rules\):\s+(\d+)",
        "pos": r"Positive examples:\s+(\d+)",
        "neg": r"Negative examples:\s+(\d+)",
    }
    for k, pat in patterns.items():
        m = re.search(pat, stdout)
        if m:
            out[k] = int(m.group(1))

    if "bk_rules" in out and "aba_rules" in out:
        out["aba_minus_bk"] = out["aba_rules"] - out["bk_rules"]
    return out


def _format_counts(d: dict, *, max_items: int = 6) -> str:
    """Format a small count dict as 'k1=3 k2=1 ...'."""
    if not d:
        return "(none)"
    items = list(d.items())[:max_items]
    s = " ".join([f"{k}={v}" for k, v in items])
    if len(d) > max_items:
        s += " …"
    return s


def _log_aba_asp_call(bk_path: Path, pos_examples: List[str], neg_examples: List[str]) -> None:
    """Log the aba_asp() call with pos/neg examples for reproducibility.
    
    Also writes the call as a comment to the .bk.aba file for reference.
    Uses relative paths to avoid exposing username/system paths.
    """
    pos_str = ",".join(pos_examples)
    neg_str = ",".join(neg_examples)
    
    # Use relative path from current directory to avoid exposing username
    try:
        rel_path = bk_path.relative_to(Path.cwd())
    except ValueError:
        # If bk_path is not relative to cwd, just use the name
        rel_path = bk_path.name
    
    call_str = f"aba_asp('{rel_path}', [{pos_str}], [{neg_str}])."
    logger.info(call_str)


def _median_pos_neg_examples(df: pd.DataFrame, target: str) -> Tuple[List[str], List[str]]:
    """Split samples into E+/E- using median split on a continuous target column."""
    median_val = df[target].median()
    pos_examples = [f"{target}({i + 1})" for i in df.index if df[target].iloc[i] >= median_val]
    neg_examples = [f"{target}({i + 1})" for i in df.index if df[target].iloc[i] < median_val]
    return pos_examples, neg_examples
    
    # Also write to the .bk.aba file as a comment
    if bk_path.exists():
        with open(bk_path, "a") as f:
            f.write(f"\n% {call_str}\n")


def _predicate_names_in_body(rule: str) -> List[str]:
    """Extract predicate functor names appearing in the body of a rule.

    Handles simple Prolog-style rules like:
        x2(A) :- x0_low(A), x1_high(A).
    Ignores built-ins like A=1.
    """
    if ":-" not in rule:
        return []
    body = rule.split(":-", 1)[1]
    body = body.strip().rstrip(".")
    names: List[str] = []
    for part in body.split(","):
        atom = part.strip()
        if not atom or "=" in atom:
            continue
        functor = atom.split("(", 1)[0].strip()
        if functor:
            names.append(functor)
    return names


def _summarize_target_rule_triviality(target: str, learned_rules: List[str]) -> Tuple[int, int, int]:
    """Return (num_target_rules, num_trivial, num_nontrivial).

    We call a learned target rule "trivial" if its body only references feature
    predicates derived from the target variable itself (prefix: f"{target}_").
    If it references any other predicate functor, it's "nontrivial".
    """
    target_rules = [r for r in learned_rules if r.startswith(f"{target}(A)")]
    trivial = 0
    nontrivial = 0
    for r in target_rules:
        functors = _predicate_names_in_body(r)
        # If there are no functors (unlikely), treat as trivial.
        if not functors:
            trivial += 1
            continue
        if all(f.startswith(f"{target}_") for f in functors):
            trivial += 1
        else:
            nontrivial += 1
    return len(target_rules), trivial, nontrivial


def _summarize_target_rule_dependencies(target: str, learned_rules: List[str]) -> dict:
    """Summarize which variable prefixes appear in learned target rules.

    Returns a dict like {"x0": 3, "x1": 1, "alpha": 1} counting how many
    target rules mention at least one predicate derived from that prefix.
    """
    counts: dict = {}
    target_rules = [r for r in learned_rules if r.startswith(f"{target}(A)")]
    for r in target_rules:
        functors = _predicate_names_in_body(r)
        prefixes = set()
        for f in functors:
            # e.g. x0_val_7 -> x0, x1_high -> x1, alpha_1 -> alpha
            prefixes.add(f.split("_", 1)[0])
        for p in prefixes:
            counts[p] = counts.get(p, 0) + 1
    return dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))


class TestSimpleHandcraftedLearning(unittest.TestCase):
    """Test learning with handcrafted minimal data using production pipeline."""
    
    @classmethod
    def setUpClass(cls):
        """Setup test fixtures."""
        cls.output_dir = _get_test_output_dir(cls.__name__)
        cls.output_dir.mkdir(parents=True, exist_ok=True)
        cls.runner = ABASPRunner()
    
    def test_simple_4_samples(self):
        """Test learning with 4 samples and clear pattern using production pipeline."""
        # Create minimal data: x2 is perfectly correlated with x0.
        # This is a deterministic DGP (not a sampled DAG) and is useful for
        # sanity-checking whether the learner can pick up a simple dependence.
        data = {
            "x0": [1, 1, 0, 0],
            "x1": [1, 0, 1, 0],
            "x2": [1, 1, 0, 0],  # Perfectly correlated with x0
        }
        df = pd.DataFrame(data)
        var_types = {c: "categorical" for c in df.columns}

        _log_run_header(
            "Handcrafted perfect correlation",
            n_samples=len(df),
            dgp="x2 := x0 (deterministic); x1 arbitrary/noise",
            gt_edges={(0, 2)},
        )
        
        # Use the production BK generation function
        # Exclude target (x2) predicates from BK (these are to be learned)
        bk_path = generate_aba_background_knowledge(
            df, var_types, "simple_4", self.output_dir, exclude_cols=["x2"],
        )
        
        # Target: x2, expect to learn rule involving x0
        pos_examples = ["x2(1)", "x2(2)"]
        neg_examples = ["x2(3)", "x2(4)"]
        
        if not self.runner.prolog_available:
            self.skipTest("SWI-Prolog not available")
        
        _log_aba_asp_call(bk_path, pos_examples, neg_examples)
        result = self.runner.run_prolog_aba_asp(
            bk_path,
            positive_examples=pos_examples,
            negative_examples=neg_examples,
            learning_options={"folding_steps": "10"},

        )
        
        self.assertEqual(result.get("status"), "completed")
        
        # Extract and display learned rules
        learned_rules = _extract_learned_rules(bk_path)
        _log_learned_rules_block("x2", learned_rules)
        _log_triviality("x2", learned_rules)
        _record_abaf_coverage(learned_rules)
        _example_coverage_report(
            target="x2",
            bk_path=bk_path,
            learned_rules=learned_rules,
            pos_examples=pos_examples,
            neg_examples=neg_examples,
        )

        deps = _summarize_target_rule_dependencies("x2", learned_rules)
        stats = _correspondence_stats("x2", learned_rules, {(0, 2)})
        logger.info("Dependencies (target rule prefixes): %s", deps)
        logger.info("GT sets: parents=%s | ancestors=%s", stats["parents"], stats["ancestors"])
        logger.info(
            "Corr vs GT: rules=%d triv=%d nontriv=%d parent=%d anc_only=%d offgraph=%d",
            stats["target_rules"],
            stats["trivial"],
            stats["nontrivial"],
            stats["parent_hit"],
            stats["ancestor_only_hit"],
            stats["offgraph_var_hit"],
        )
        
        # Assert that we actually learned something
        self.assertGreater(len(learned_rules), 0, "Should learn at least one rule")
        logger.info("✓ Handcrafted perfect-correlation learning produced rules")


class TestMinimalDiscreteData(unittest.TestCase):
    """Discrete-data integration tests (chain/confounder/collider).

    These are grouped together because they share the same ArgCausalDisco
    discrete-data generation pipeline and are easiest to compare side-by-side.
    """
    
    @classmethod
    def setUpClass(cls):
        """Setup test fixtures."""
        cls.output_dir = _get_test_output_dir(cls.__name__)
        cls.output_dir.mkdir(parents=True, exist_ok=True)
        cls.runner = ABASPRunner()
    
    def test_01_discrete_chain_6_samples(self):
        """Test learning with 6 discrete chain samples using production pipeline."""
        # Generate minimal discrete data: X0 -> X1 -> X2
        edges = {(0, 1), (1, 2)}
        data = simulate_discrete_data(
            num_of_nodes=3,
            sample_size=6,
            truth_DAG_directed_edges=edges,
            random_seed=42,
        )
        
        df = pd.DataFrame(data, columns=["x0", "x1", "x2"])
        var_types = {c: "categorical" for c in df.columns}

        _log_run_header(
            "ArgCausalDisco discrete chain",
            n_samples=len(df),
            dgp="x0→x1→x2 (discrete); learner may pick correlated ancestors",
            gt_edges=edges,
        )
        
        if not self.runner.prolog_available:
            self.skipTest("SWI-Prolog not available")

        # We want to see whether the learned rules depend on the *target*.
        # So we learn for x0, x1 and then x2 from the same chain dataset.

        # --- Learn x0 -----------------------------------------------------
        bk_x0 = generate_aba_background_knowledge(
            df, var_types, "discrete_6_x0", self.output_dir, exclude_cols=["x0"]
        )
        _, pos_x0, neg_x0 = pick_target_variable(df, "x0")
        if not pos_x0 or not neg_x0:
            self.skipTest("Need both positive and negative examples for x0")

        _log_aba_asp_call(bk_x0, pos_x0, neg_x0)
        res_x0 = self.runner.run_prolog_aba_asp(
            bk_x0,
            positive_examples=pos_x0,
            negative_examples=neg_x0,
            learning_options={"folding_steps": "15"},
        )
        self.assertEqual(res_x0.get("status"), "completed")
        learned_x0 = _extract_learned_rules(bk_x0)
        _log_learned_rules_block("x0", learned_x0)
        _log_triviality("x0", learned_x0)
        _record_abaf_coverage(learned_x0)
        _example_coverage_report(
            target="x0",
            bk_path=bk_x0,
            learned_rules=learned_x0,
            pos_examples=pos_x0,
            neg_examples=neg_x0,
        )
        deps_x0 = _summarize_target_rule_dependencies("x0", learned_x0)
        stats_x0 = _correspondence_stats("x0", learned_x0, edges)
        logger.info("Dependencies (target rule prefixes): %s", deps_x0)
        logger.info("GT sets: parents=%s | ancestors=%s", stats_x0["parents"], stats_x0["ancestors"])
        logger.info(
            "Corr vs GT: rules=%d triv=%d nontriv=%d parent=%d anc_only=%d offgraph=%d",
            stats_x0["target_rules"],
            stats_x0["trivial"],
            stats_x0["nontrivial"],
            stats_x0["parent_hit"],
            stats_x0["ancestor_only_hit"],
            stats_x0["offgraph_var_hit"],
        )
        self.assertTrue(any(r.startswith("x0(A)") for r in learned_x0), "Expected learned x0(A) rule")

        # --- Learn x1 -----------------------------------------------------
        bk_x1 = generate_aba_background_knowledge(
            df, var_types, "discrete_6_x1", self.output_dir, exclude_cols=["x1"]
        )
        _, pos_x1, neg_x1 = pick_target_variable(df, "x1")
        if not pos_x1 or not neg_x1:
            self.skipTest("Need both positive and negative examples for x1")

        _log_aba_asp_call(bk_x1, pos_x1, neg_x1)
        res_x1 = self.runner.run_prolog_aba_asp(
            bk_x1,
            positive_examples=pos_x1,
            negative_examples=neg_x1,
            learning_options={"folding_steps": "15"},
        )
        self.assertEqual(res_x1.get("status"), "completed")
        learned_x1 = _extract_learned_rules(bk_x1)
        _log_learned_rules_block("x1", learned_x1)
        _log_triviality("x1", learned_x1)
        _record_abaf_coverage(learned_x1)
        _example_coverage_report(
            target="x1",
            bk_path=bk_x1,
            learned_rules=learned_x1,
            pos_examples=pos_x1,
            neg_examples=neg_x1,
        )
        deps_x1 = _summarize_target_rule_dependencies("x1", learned_x1)
        stats_x1 = _correspondence_stats("x1", learned_x1, edges)
        logger.info("Dependencies (target rule prefixes): %s", deps_x1)
        logger.info("GT sets: parents=%s | ancestors=%s", stats_x1["parents"], stats_x1["ancestors"])
        logger.info(
            "Corr vs GT: rules=%d triv=%d nontriv=%d parent=%d anc_only=%d offgraph=%d",
            stats_x1["target_rules"],
            stats_x1["trivial"],
            stats_x1["nontrivial"],
            stats_x1["parent_hit"],
            stats_x1["ancestor_only_hit"],
            stats_x1["offgraph_var_hit"],
        )

        # Note: ABA-ASP can legitimately learn an empty delta for some
        # target/dataset combinations. We still learn x1 here to surface that
        # behavior in the run summary without making the whole suite flaky.

        # --- Learn x2 -----------------------------------------------------
        bk_x2 = generate_aba_background_knowledge(
            df, var_types, "discrete_6_x2", self.output_dir, exclude_cols=["x2"]
        )
        _, pos_x2, neg_x2 = pick_target_variable(df, "x2")
        if not pos_x2 or not neg_x2:
            self.skipTest("Need both positive and negative examples for x2")

        _log_aba_asp_call(bk_x2, pos_x2, neg_x2)
        res_x2 = self.runner.run_prolog_aba_asp(
            bk_x2,
            positive_examples=pos_x2,
            negative_examples=neg_x2,
            learning_options={"folding_steps": "15"},
        )
        self.assertEqual(res_x2.get("status"), "completed")
        learned_x2 = _extract_learned_rules(bk_x2)
        _log_learned_rules_block("x2", learned_x2)
        _log_triviality("x2", learned_x2)
        _record_abaf_coverage(learned_x2)
        _example_coverage_report(
            target="x2",
            bk_path=bk_x2,
            learned_rules=learned_x2,
            pos_examples=pos_x2,
            neg_examples=neg_x2,
        )
        self.assertTrue(any(r.startswith("x2(A)") for r in learned_x2), "Expected learned x2(A) rule")

        # Triviality + correspondence report for x2 against the GT chain DAG.
        deps = _summarize_target_rule_dependencies("x2", learned_x2)
        stats = _correspondence_stats("x2", learned_x2, edges)
        logger.info("Dependencies (target rule prefixes): %s", deps)
        logger.info("GT sets: parents=%s | ancestors=%s", stats["parents"], stats["ancestors"])
        logger.info(
            "Corr vs GT: rules=%d triv=%d nontriv=%d parent=%d anc_only=%d offgraph=%d",
            stats["target_rules"],
            stats["trivial"],
            stats["nontrivial"],
            stats["parent_hit"],
            stats["ancestor_only_hit"],
            stats["offgraph_var_hit"],
        )

        # The main check requested: learning different targets yields different learned theories.
        self.assertNotEqual(set(learned_x0), set(learned_x1), "Expected learned rules for x0 vs x1 to differ")
        self.assertNotEqual(set(learned_x1), set(learned_x2), "Expected learned rules for x1 vs x2 to differ")
        self.assertNotEqual(set(learned_x0), set(learned_x2), "Expected learned rules for x0 vs x2 to differ")
        logger.info("✓ Discrete chain: learned rules differ for x0 vs x2")

    def test_02_confounder_x0_to_x1_x2_all_targets(self):
        # ArgCausalDisco discrete confounder: x0 -> x1 and x0 -> x2
        edges = {(0, 1), (0, 2)}
        data = simulate_discrete_data(
            num_of_nodes=3,
            sample_size=6,
            truth_DAG_directed_edges=edges,
            random_seed=42,
        )

        df = pd.DataFrame(data, columns=["x0", "x1", "x2"])
        var_types = {c: "categorical" for c in df.columns}

        _log_run_header(
            "ArgCausalDisco confounder (common cause)",
            n_samples=len(df),
            dgp="x0→x1 and x0→x2 (discrete); learn all targets",
            gt_edges=edges,
        )

        if not self.runner.prolog_available:
            self.skipTest("SWI-Prolog not available")

        for target in ("x0", "x1", "x2"):
            bk_path = generate_aba_background_knowledge(
                df,
                var_types,
                f"confounder_6_{target}",
                self.output_dir,
                exclude_cols=[target],
            )
            _, pos, neg = pick_target_variable(df, target)
            if not pos or not neg:
                self.skipTest(f"Need both positive and negative examples for {target}")

            _log_aba_asp_call(bk_path, pos, neg)
            res = self.runner.run_prolog_aba_asp(
                bk_path,
                positive_examples=pos,
                negative_examples=neg,
                learning_options={"folding_steps": "15"},
            )
            self.assertEqual(res.get("status"), "completed")

            learned = _extract_learned_rules(bk_path)
            _log_learned_rules_block(target, learned)
            _log_triviality(target, learned)
            _record_abaf_coverage(learned)
            _example_coverage_report(
                target=target,
                bk_path=bk_path,
                learned_rules=learned,
                pos_examples=pos,
                neg_examples=neg,
            )

            deps = _summarize_target_rule_dependencies(target, learned)
            stats = _correspondence_stats(target, learned, edges)
            logger.info("Dependencies (target rule prefixes): %s", deps)
            logger.info("GT sets: parents=%s | ancestors=%s", stats["parents"], stats["ancestors"])
            logger.info(
                "Corr vs GT: rules=%d triv=%d nontriv=%d parent=%d anc_only=%d offgraph=%d",
                stats["target_rules"],
                stats["trivial"],
                stats["nontrivial"],
                stats["parent_hit"],
                stats["ancestor_only_hit"],
                stats["offgraph_var_hit"],
            )

            # Note: ABA-ASP can legitimately return "* No solution found!" for some
            # configurations. In that case, no .bk.sol.aba is written and the learned
            # delta is empty; this test is primarily to surface that behavior in the
            # final run summary while ensuring the pipeline executes.

    def test_03_collider_x0_x1_to_x2_all_targets(self):
        # ArgCausalDisco discrete collider: x0 -> x2, x1 -> x2
        edges = {(0, 2), (1, 2)}
        sample_size = 8
        data = simulate_discrete_data(
            num_of_nodes=3,
            sample_size=sample_size,
            truth_DAG_directed_edges=edges,
            random_seed=42,
        )

        df = pd.DataFrame(data, columns=["x0", "x1", "x2"])
        var_types = {c: "categorical" for c in df.columns}

        _log_run_header(
            "ArgCausalDisco collider (common effect)",
            n_samples=len(df),
            dgp="x0→x2 and x1→x2 (discrete); learn all targets",
            gt_edges=edges,
        )

        if not self.runner.prolog_available:
            self.skipTest("SWI-Prolog not available")

        for target in ("x0", "x1", "x2"):
            bk_path = generate_aba_background_knowledge(
                df,
                var_types,
                f"collider_{sample_size}_{target}",
                self.output_dir,
                exclude_cols=[target],
            )
            _, pos, neg = pick_target_variable(df, target)
            if not pos or not neg:
                self.skipTest(f"Need both positive and negative examples for {target}")

            _log_aba_asp_call(bk_path, pos, neg)
            res = self.runner.run_prolog_aba_asp(
                bk_path,
                positive_examples=pos,
                negative_examples=neg,
                learning_options={"folding_steps": "15"},
            )
            self.assertEqual(res.get("status"), "completed")

            learned = _extract_learned_rules(bk_path)
            _log_learned_rules_block(target, learned)
            _log_triviality(target, learned)
            _record_abaf_coverage(learned)
            _example_coverage_report(
                target=target,
                bk_path=bk_path,
                learned_rules=learned,
                pos_examples=pos,
                neg_examples=neg,
            )

            deps = _summarize_target_rule_dependencies(target, learned)
            stats = _correspondence_stats(target, learned, edges)
            logger.info("Dependencies (target rule prefixes): %s", deps)
            logger.info("GT sets: parents=%s | ancestors=%s", stats["parents"], stats["ancestors"])
            logger.info(
                "Corr vs GT: rules=%d triv=%d nontriv=%d parent=%d anc_only=%d offgraph=%d",
                stats["target_rules"],
                stats["trivial"],
                stats["nontrivial"],
                stats["parent_hit"],
                stats["ancestor_only_hit"],
                stats["offgraph_var_hit"],
            )

            # Note: ABA-ASP can legitimately return "* No solution found!" for some
            # configurations. In that case, no .bk.sol.aba is written and the learned
            # delta is empty; this test is primarily to surface that behavior in the
            # final run summary while ensuring the pipeline executes.


class TestGreedyFoldingDiscreteChain(unittest.TestCase):
    """Greedy folding variant of the discrete-chain learning test."""

    @classmethod
    def setUpClass(cls):
        cls.output_dir = _get_test_output_dir(cls.__name__)
        cls.output_dir.mkdir(parents=True, exist_ok=True)
        cls.runner = ABASPRunner()

    def test_discrete_chain_greedy_folding_all_targets(self):
        edges = {(0, 1), (1, 2)}
        data = simulate_discrete_data(
            num_of_nodes=3,
            sample_size=6,
            truth_DAG_directed_edges=edges,
            random_seed=42,
        )
        df = pd.DataFrame(data, columns=["x0", "x1", "x2"])
        var_types = {c: "categorical" for c in df.columns}

        _log_run_header(
            "Greedy folding: discrete chain",
            n_samples=len(df),
            dgp="x0→x1→x2 (discrete); folding_mode=greedy; learn all targets",
            gt_edges=edges,
        )

        if not self.runner.prolog_available:
            self.skipTest("SWI-Prolog not available")

        for target in ("x0", "x1", "x2"):
            bk_path = generate_aba_background_knowledge(
                df,
                var_types,
                f"discrete_6_{target}_greedy",
                self.output_dir,
                exclude_cols=[target],
            )
            _, pos, neg = pick_target_variable(df, target)
            if not pos or not neg:
                self.skipTest(f"Need both positive and negative examples for {target}")

            _log_aba_asp_call(bk_path, pos, neg)
            res = self.runner.run_prolog_aba_asp(
                bk_path,
                positive_examples=pos,
                negative_examples=neg,
                learning_options={"folding_steps": "15", "folding_mode": "greedy", "verbosity": "off"},
            )
            self.assertEqual(res.get("status"), "completed")

            learned = _extract_learned_rules(bk_path)
            _log_learned_rules_block(target, learned)
            _log_triviality(target, learned)
            _record_abaf_coverage(learned)
            _example_coverage_report(
                target=target,
                bk_path=bk_path,
                learned_rules=learned,
                pos_examples=pos,
                neg_examples=neg,
            )

            deps = _summarize_target_rule_dependencies(target, learned)
            stats = _correspondence_stats(target, learned, edges)
            logger.info("Dependencies (target rule prefixes): %s", deps)
            logger.info("GT sets: parents=%s | ancestors=%s", stats["parents"], stats["ancestors"])
            logger.info(
                "Corr vs GT: rules=%d triv=%d nontriv=%d parent=%d anc_only=%d offgraph=%d",
                stats["target_rules"],
                stats["trivial"],
                stats["nontrivial"],
                stats["parent_hit"],
                stats["ancestor_only_hit"],
                stats["offgraph_var_hit"],
            )


class TestGreedyFoldingConfounder(unittest.TestCase):
    """Greedy folding variant of the confounder (common-cause) test."""

    @classmethod
    def setUpClass(cls):
        cls.output_dir = _get_test_output_dir(cls.__name__)
        cls.output_dir.mkdir(parents=True, exist_ok=True)
        cls.runner = ABASPRunner()

    def test_confounder_greedy_folding_all_targets(self):
        edges = {(0, 1), (0, 2)}
        data = simulate_discrete_data(
            num_of_nodes=3,
            sample_size=6,
            truth_DAG_directed_edges=edges,
            random_seed=42,
        )
        df = pd.DataFrame(data, columns=["x0", "x1", "x2"])
        var_types = {c: "categorical" for c in df.columns}

        _log_run_header(
            "Greedy folding: confounder (common cause)",
            n_samples=len(df),
            dgp="x0→x1 and x0→x2 (discrete); folding_mode=greedy; learn all targets",
            gt_edges=edges,
        )

        if not self.runner.prolog_available:
            self.skipTest("SWI-Prolog not available")

        for target in ("x0", "x1", "x2"):
            bk_path = generate_aba_background_knowledge(
                df,
                var_types,
                f"confounder_6_{target}_greedy",
                self.output_dir,
                exclude_cols=[target],
            )
            _, pos, neg = pick_target_variable(df, target)
            if not pos or not neg:
                self.skipTest(f"Need both positive and negative examples for {target}")

            _log_aba_asp_call(bk_path, pos, neg)
            res = self.runner.run_prolog_aba_asp(
                bk_path,
                positive_examples=pos,
                negative_examples=neg,
                learning_options={"folding_steps": "15", "folding_mode": "greedy", "verbosity": "off"},
            )
            self.assertEqual(res.get("status"), "completed")

            learned = _extract_learned_rules(bk_path)
            _log_learned_rules_block(target, learned)
            _log_triviality(target, learned)
            _record_abaf_coverage(learned)
            _example_coverage_report(
                target=target,
                bk_path=bk_path,
                learned_rules=learned,
                pos_examples=pos,
                neg_examples=neg,
            )

            deps = _summarize_target_rule_dependencies(target, learned)
            stats = _correspondence_stats(target, learned, edges)
            logger.info("Dependencies (target rule prefixes): %s", deps)
            logger.info("GT sets: parents=%s | ancestors=%s", stats["parents"], stats["ancestors"])
            logger.info(
                "Corr vs GT: rules=%d triv=%d nontriv=%d parent=%d anc_only=%d offgraph=%d",
                stats["target_rules"],
                stats["trivial"],
                stats["nontrivial"],
                stats["parent_hit"],
                stats["ancestor_only_hit"],
                stats["offgraph_var_hit"],
            )


class TestGreedyFoldingCollider(unittest.TestCase):
    """Greedy folding variant of the collider (common-effect) test."""

    @classmethod
    def setUpClass(cls):
        cls.output_dir = _get_test_output_dir(cls.__name__)
        cls.output_dir.mkdir(parents=True, exist_ok=True)
        cls.runner = ABASPRunner()

    def test_collider_greedy_folding_all_targets(self):
        edges = {(0, 2), (1, 2)}
        sample_size=8
        data = simulate_discrete_data(
            num_of_nodes=3,
            sample_size=sample_size,
            truth_DAG_directed_edges=edges,
            random_seed=42,
        )
        df = pd.DataFrame(data, columns=["x0", "x1", "x2"])
        var_types = {c: "categorical" for c in df.columns}

        _log_run_header(
            "Greedy folding: collider (common effect)",
            n_samples=len(df),
            dgp="x0→x2 and x1→x2 (discrete); folding_mode=greedy; learn all targets",
            gt_edges=edges,
        )

        if not self.runner.prolog_available:
            self.skipTest("SWI-Prolog not available")

        for target in ("x0", "x1", "x2"):
            bk_path = generate_aba_background_knowledge(
                df,
                var_types,
                f"collider_{sample_size}_{target}_greedy",
                self.output_dir,
                exclude_cols=[target],
            )
            _, pos, neg = pick_target_variable(df, target)
            if not pos or not neg:
                self.skipTest(f"Need both positive and negative examples for {target}")

            _log_aba_asp_call(bk_path, pos, neg)
            res = self.runner.run_prolog_aba_asp(
                bk_path,
                positive_examples=pos,
                negative_examples=neg,
                learning_options={"folding_steps": "15", "folding_mode": "greedy", "verbosity": "off"},
            )
            self.assertEqual(res.get("status"), "completed")

            learned = _extract_learned_rules(bk_path)
            _log_learned_rules_block(target, learned)
            _log_triviality(target, learned)
            _record_abaf_coverage(learned)
            _example_coverage_report(
                target=target,
                bk_path=bk_path,
                learned_rules=learned,
                pos_examples=pos,
                neg_examples=neg,
            )

            deps = _summarize_target_rule_dependencies(target, learned)
            stats = _correspondence_stats(target, learned, edges)
            logger.info("Dependencies (target rule prefixes): %s", deps)
            logger.info("GT sets: parents=%s | ancestors=%s", stats["parents"], stats["ancestors"])
            logger.info(
                "Corr vs GT: rules=%d triv=%d nontriv=%d parent=%d anc_only=%d offgraph=%d",
                stats["target_rules"],
                stats["trivial"],
                stats["nontrivial"],
                stats["parent_hit"],
                stats["ancestor_only_hit"],
                stats["offgraph_var_hit"],
            )


class TestBKOrderingSensitivity(unittest.TestCase):
    """Show BK feature ordering affects nd folding but not greedy (chain, target x2)."""

    @classmethod
    def setUpClass(cls):
        cls.output_dir = _get_test_output_dir(cls.__name__)
        cls.output_dir.mkdir(parents=True, exist_ok=True)
        cls.runner = ABASPRunner()

    def test_chain_x2_bk_ordering_changes_nd_not_greedy(self):
        edges = {(0, 1), (1, 2)}
        var_types = {"x0": "categorical", "x1": "categorical", "x2": "categorical"}

        _log_run_header(
            "BK ordering sensitivity (chain, target x2)",
            n_samples=12,
            dgp="x0→x1→x2 (discrete); swap BK feature section order (x1 before x0)",
            gt_edges=edges,
        )

        if not self.runner.prolog_available:
            self.skipTest("SWI-Prolog not available")

        # Seed chosen by probing for a deterministic case where:
        # - nd folding changes under BK feature section ordering
        # - greedy folding remains invariant
        seed = 7
        data = simulate_discrete_data(
            num_of_nodes=3,
            sample_size=12,
            truth_DAG_directed_edges=edges,
            random_seed=seed,
        )
        df = pd.DataFrame(data, columns=["x0", "x1", "x2"])

        bk_orig = generate_aba_background_knowledge(
            df,
            var_types,
            f"discrete_12_x2_bkorder_seed{seed}_orig",
            self.output_dir,
            exclude_cols=["x2"],
        )
        bk_swapped = self.output_dir / f"discrete_12_x2_bkorder_seed{seed}_x1_before_x0.bk.aba"
        _write_bk_with_reordered_feature_sections(
            src_bk_path=bk_orig,
            dst_bk_path=bk_swapped,
            feature_order=["x1", "x0"],
        )

        _, pos, neg = pick_target_variable(df, "x2")
        if not pos or not neg:
            self.skipTest("Need both positive and negative examples for x2")

        # ND folding
        logger.info("BK ordering experiment: nd/orig")
        _log_aba_asp_call(bk_orig, pos, neg)
        res1 = self.runner.run_prolog_aba_asp(
            bk_orig,
            positive_examples=pos,
            negative_examples=neg,
            learning_options={"folding_steps": "15", "folding_mode": "nd", "verbosity": "off"},
        )
        self.assertEqual(res1.get("status"), "completed")
        self.assertNotIn("No solution found!", res1.get("stdout", ""))
        learned_nd_orig = _extract_learned_rules(bk_orig)
        _log_learned_rules_block("x2", learned_nd_orig)
        _log_triviality("x2", learned_nd_orig)
        _record_abaf_coverage(learned_nd_orig)

        logger.info("BK ordering experiment: nd/swapped")
        _log_aba_asp_call(bk_swapped, pos, neg)
        res2 = self.runner.run_prolog_aba_asp(
            bk_swapped,
            positive_examples=pos,
            negative_examples=neg,
            learning_options={"folding_steps": "15", "folding_mode": "nd", "verbosity": "off"},
        )
        self.assertEqual(res2.get("status"), "completed")
        self.assertNotIn("No solution found!", res2.get("stdout", ""))
        learned_nd_swapped = _extract_learned_rules(bk_swapped)
        _log_learned_rules_block("x2", learned_nd_swapped)
        nd_added = sorted(set(learned_nd_swapped) - set(learned_nd_orig))
        nd_removed = sorted(set(learned_nd_orig) - set(learned_nd_swapped))
        if nd_added:
            logger.info("  Δadded (nd):")
            for r in nd_added[:12]:
                logger.info("  %s", r)
        else:
            logger.info("  Δadded (nd): (none)")
        if nd_removed:
            logger.info("  Δremoved (nd):")
            for r in nd_removed[:12]:
                logger.info("  %s", r)
        else:
            logger.info("  Δremoved (nd): (none)")
        _log_triviality("x2", learned_nd_swapped)
        _record_abaf_coverage(learned_nd_swapped)

        self.assertTrue(learned_nd_orig, "Expected nd folding to learn a non-empty delta (orig BK)")
        self.assertTrue(learned_nd_swapped, "Expected nd folding to learn a non-empty delta (swapped BK)")

        nd_same = set(learned_nd_orig) == set(learned_nd_swapped)
        logger.info(
            "BK order (seed=%d) nd: orig=%d swapped=%d same=%s",
            seed,
            len(learned_nd_orig),
            len(learned_nd_swapped),
            nd_same,
        )
        self.assertFalse(
            nd_same,
            "Expected nd folding learned deltas to differ under BK feature section reordering",
        )

        # Greedy folding should be stable under this BK reorder.
        logger.info("BK ordering experiment: greedy/orig")
        res3 = self.runner.run_prolog_aba_asp(
            bk_orig,
            positive_examples=pos,
            negative_examples=neg,
            learning_options={"folding_steps": "15", "folding_mode": "greedy", "verbosity": "off"},
        )
        self.assertEqual(res3.get("status"), "completed")
        self.assertNotIn("No solution found!", res3.get("stdout", ""))
        learned_greedy_orig = _extract_learned_rules(bk_orig)
        _log_learned_rules_block("x2", learned_greedy_orig)
        _log_triviality("x2", learned_greedy_orig)
        _record_abaf_coverage(learned_greedy_orig)

        logger.info("BK ordering experiment: greedy/swapped")
        res4 = self.runner.run_prolog_aba_asp(
            bk_swapped,
            positive_examples=pos,
            negative_examples=neg,
            learning_options={"folding_steps": "15", "folding_mode": "greedy", "verbosity": "off"},
        )
        self.assertEqual(res4.get("status"), "completed")
        self.assertNotIn("No solution found!", res4.get("stdout", ""))
        learned_greedy_swapped = _extract_learned_rules(bk_swapped)
        _log_learned_rules_block("x2", learned_greedy_swapped)
        greedy_added = sorted(set(learned_greedy_swapped) - set(learned_greedy_orig))
        greedy_removed = sorted(set(learned_greedy_orig) - set(learned_greedy_swapped))
        if greedy_added:
            logger.info("  Δadded (greedy):")
            for r in greedy_added[:12]:
                logger.info("  %s", r)
        else:
            logger.info("  Δadded (greedy): (none)")
        if greedy_removed:
            logger.info("  Δremoved (greedy):")
            for r in greedy_removed[:12]:
                logger.info("  %s", r)
        else:
            logger.info("  Δremoved (greedy): (none)")
        _log_triviality("x2", learned_greedy_swapped)
        _record_abaf_coverage(learned_greedy_swapped)

        self.assertTrue(learned_greedy_orig, "Expected greedy folding to learn a non-empty delta (orig BK)")
        self.assertTrue(learned_greedy_swapped, "Expected greedy folding to learn a non-empty delta (swapped BK)")

        greedy_same = set(learned_greedy_orig) == set(learned_greedy_swapped)
        logger.info(
            "BK order (seed=%d) greedy: orig=%d swapped=%d same=%s",
            seed,
            len(learned_greedy_orig),
            len(learned_greedy_swapped),
            greedy_same,
        )
        self.assertTrue(
            greedy_same,
            "Expected greedy folding learned deltas to be invariant to BK feature section ordering",
        )


class TestAssumptionIntroduction(unittest.TestCase):
    """Regression: ensure assumption introduction can appear in learned ABA output."""

    @classmethod
    def setUpClass(cls):
        cls.output_dir = _get_test_output_dir(cls.__name__)
        cls.output_dir.mkdir(parents=True, exist_ok=True)
        cls.runner = ABASPRunner()

    def test_exception_triggers_assumption_intro(self):
        """Create an exception pattern that requires an assumption/contrary to fit E+/E-."""
        data = {
            "x0": [1, 1, 1, 0, 0],
            "x1": [0, 0, 1, 0, 1],
            # Mostly x2 follows x0, except sample 3 is a counterexample
            "x2": [1, 1, 0, 0, 0],
        }
        df = pd.DataFrame(data)
        var_types = {c: "categorical" for c in df.columns}

        _log_run_header(
            "Handcrafted exception → ABAF components",
            n_samples=len(df),
            dgp="Mostly x2 follows x0, with a counterexample requiring an exception",
            gt_edges={(0, 2)},
        )

        # Exclude target (x2) predicates so the exception must be captured via ABA machinery
        bk_path = generate_aba_background_knowledge(
            df, var_types, "exception_5", self.output_dir, exclude_cols=["x2"]
        )

        pos_examples = ["x2(1)", "x2(2)"]
        neg_examples = ["x2(3)", "x2(4)", "x2(5)"]

        if not self.runner.prolog_available:
            self.skipTest("SWI-Prolog not available")

        _log_aba_asp_call(bk_path, pos_examples, neg_examples)
        result = self.runner.run_prolog_aba_asp(
            bk_path,
            positive_examples=pos_examples,
            negative_examples=neg_examples,
            learning_options={"folding_steps": "10"},
        )
        self.assertEqual(result.get("status"), "completed")

        learned_rules = _extract_learned_rules(bk_path)
        _log_learned_rules_block("x2", learned_rules, max_lines=50)
        _log_triviality("x2", learned_rules)
        _record_abaf_coverage(learned_rules)
        _example_coverage_report(
            target="x2",
            bk_path=bk_path,
            learned_rules=learned_rules,
            pos_examples=pos_examples,
            neg_examples=neg_examples,
        )

        deps = _summarize_target_rule_dependencies("x2", learned_rules)
        stats = _correspondence_stats("x2", learned_rules, {(0, 2)})
        logger.info("Dependencies (target rule prefixes): %s", deps)
        logger.info("GT sets: parents=%s | ancestors=%s", stats["parents"], stats["ancestors"])
        logger.info(
            "Corr vs GT: rules=%d triv=%d nontriv=%d parent=%d anc_only=%d offgraph=%d",
            stats["target_rules"],
            stats["trivial"],
            stats["nontrivial"],
            stats["parent_hit"],
            stats["ancestor_only_hit"],
            stats["offgraph_var_hit"],
        )

        abaf = _abaf_component_stats(learned_rules)
        logger.info(
            "ABAF coverage: assumptions=%d | contraries=%d | alpha_mentions=%d | c_alpha_mentions=%d",
            abaf["assumptions"],
            abaf["contraries"],
            abaf["alpha_mentions"],
            abaf["c_alpha_mentions"],
        )

        # Confirm ABA-specific components appear (assumption + contrary)
        self.assertTrue(any("assumption(" in r for r in learned_rules), "Should introduce an assumption")
        self.assertTrue(any("contrary(" in r for r in learned_rules), "Should introduce a contrary")
        self.assertTrue(any("alpha_" in r for r in learned_rules), "Expected learned alpha_* assumption")
        logger.info("✓ Assumption introduction produced ABA framework components")


class TestMinimalContinuousData(unittest.TestCase):
    """Test learning with ArgCausalDisco continuous data using production pipeline."""
    
    @classmethod
    def setUpClass(cls):
        """Setup test fixtures."""
        cls.output_dir = _get_test_output_dir(cls.__name__)
        cls.output_dir.mkdir(parents=True, exist_ok=True)
        cls.runner = ABASPRunner()
    
    def test_continuous_8_samples(self):
        """Test learning with 8 continuous samples (median split) using production pipeline."""
        # Generate minimal continuous data: X0 -> X1 -> X2
        edges = {(0, 1), (1, 2)}
        data = simulate_linear_continuous_data(
            num_of_nodes=3,
            sample_size=8,
            truth_DAG_directed_edges=edges,
            noise_type="gaussian",
            random_seed=42,
        )
        
        df = pd.DataFrame(data, columns=["x0", "x1", "x2"])
        var_types = {c: "continuous" for c in df.columns}

        _log_run_header(
            "ArgCausalDisco continuous chain",
            n_samples=len(df),
            dgp="x0→x1→x2 (linear Gaussian); learner may pick correlated ancestors",
            gt_edges=edges,
        )
        
        if not self.runner.prolog_available:
            self.skipTest("SWI-Prolog not available")

        # Learn x0 then x2 and compare learned rules.
        if not self.runner.prolog_available:
            self.skipTest("SWI-Prolog not available")

        # --- Learn x0 (BK bins=2) ----------------------------------------
        bk_x0 = generate_aba_background_knowledge(
            df,
            var_types,
            "continuous_8_x0",
            self.output_dir,
            exclude_cols=["x0"],
            continuous_bins=2,
            bin_strategy="quantile",
        )
        median_x0 = df["x0"].median()
        x0_binary = (df["x0"] >= median_x0).astype(int)
        pos_x0 = [f"x0({i+1})" for i in df.index if x0_binary.iloc[i] == 1]
        neg_x0 = [f"x0({i+1})" for i in df.index if x0_binary.iloc[i] == 0]
        if not pos_x0 or not neg_x0:
            self.skipTest("Need both positive and negative examples for x0")
        _log_aba_asp_call(bk_x0, pos_x0, neg_x0)
        res_x0 = self.runner.run_prolog_aba_asp(
            bk_x0,
            positive_examples=pos_x0,
            negative_examples=neg_x0,
            learning_options={"folding_steps": "15"},
        )
        self.assertEqual(res_x0.get("status"), "completed")
        learned_x0 = _extract_learned_rules(bk_x0)
        _log_learned_rules_block("x0", learned_x0)
        _log_triviality("x0", learned_x0)
        _record_abaf_coverage(learned_x0)
        _example_coverage_report(
            target="x0",
            bk_path=bk_x0,
            learned_rules=learned_x0,
            pos_examples=pos_x0,
            neg_examples=neg_x0,
        )
        deps_x0 = _summarize_target_rule_dependencies("x0", learned_x0)
        stats_x0 = _correspondence_stats("x0", learned_x0, edges)
        logger.info("Dependencies (target rule prefixes): %s", deps_x0)
        logger.info("GT sets: parents=%s | ancestors=%s", stats_x0["parents"], stats_x0["ancestors"])
        logger.info(
            "Corr vs GT: rules=%d triv=%d nontriv=%d parent=%d anc_only=%d offgraph=%d",
            stats_x0["target_rules"],
            stats_x0["trivial"],
            stats_x0["nontrivial"],
            stats_x0["parent_hit"],
            stats_x0["ancestor_only_hit"],
            stats_x0["offgraph_var_hit"],
        )
        self.assertTrue(any(r.startswith("x0(A)") for r in learned_x0), "Expected learned x0(A) rule")

        # --- Learn x2 (BK bins=2) ----------------------------------------
        logger.info("\nContinuous bins experiment: bins=2 (feature BK)")
        bk_x2 = generate_aba_background_knowledge(
            df,
            var_types,
            "continuous_8_x2_bins2",
            self.output_dir,
            exclude_cols=["x2"],
            continuous_bins=2,
            bin_strategy="quantile",
        )
        median_x2 = df["x2"].median()
        x2_binary = (df["x2"] >= median_x2).astype(int)
        pos_x2 = [f"x2({i+1})" for i in df.index if x2_binary.iloc[i] == 1]
        neg_x2 = [f"x2({i+1})" for i in df.index if x2_binary.iloc[i] == 0]
        if not pos_x2 or not neg_x2:
            self.skipTest("Need both positive and negative examples for x2")
        _log_aba_asp_call(bk_x2, pos_x2, neg_x2)
        res_x2 = self.runner.run_prolog_aba_asp(
            bk_x2,
            positive_examples=pos_x2,
            negative_examples=neg_x2,
            learning_options={"folding_steps": "15"},
        )
        self.assertEqual(res_x2.get("status"), "completed")
        learned_x2 = _extract_learned_rules(bk_x2)
        _log_learned_rules_block("x2", learned_x2)
        _log_triviality("x2", learned_x2)
        _record_abaf_coverage(learned_x2)
        _example_coverage_report(
            target="x2",
            bk_path=bk_x2,
            learned_rules=learned_x2,
            pos_examples=pos_x2,
            neg_examples=neg_x2,
        )
        self.assertTrue(any(r.startswith("x2(A)") for r in learned_x2), "Expected learned x2(A) rule")

        deps = _summarize_target_rule_dependencies("x2", learned_x2)
        stats = _correspondence_stats("x2", learned_x2, edges)
        logger.info("Dependencies (target rule prefixes): %s", deps)
        logger.info("GT sets: parents=%s | ancestors=%s", stats["parents"], stats["ancestors"])
        logger.info(
            "Corr vs GT: rules=%d triv=%d nontriv=%d parent=%d anc_only=%d offgraph=%d",
            stats["target_rules"],
            stats["trivial"],
            stats["nontrivial"],
            stats["parent_hit"],
            stats["ancestor_only_hit"],
            stats["offgraph_var_hit"],
        )

        self.assertNotEqual(
            set(learned_x0),
            set(learned_x2),
            "Expected learned rules for x0 vs x2 to differ on the chain dataset",
        )
        logger.info("✓ Continuous chain: learned rules differ for x0 vs x2")

        # --- Learn x2 again (BK bins=3) ----------------------------------
        logger.info("\nContinuous bins experiment: bins=3 (feature BK)")
        bk_x2_bins3 = generate_aba_background_knowledge(
            df,
            var_types,
            "continuous_8_x2_bins3",
            self.output_dir,
            exclude_cols=["x2"],
            continuous_bins=3,
            bin_strategy="quantile",
        )
        _log_aba_asp_call(bk_x2_bins3, pos_x2, neg_x2)
        res_x2_bins3 = self.runner.run_prolog_aba_asp(
            bk_x2_bins3,
            positive_examples=pos_x2,
            negative_examples=neg_x2,
            learning_options={"folding_steps": "15"},
        )
        self.assertEqual(res_x2_bins3.get("status"), "completed")
        learned_x2_bins3 = _extract_learned_rules(bk_x2_bins3)
        _log_learned_rules_block("x2", learned_x2_bins3)
        _log_triviality("x2", learned_x2_bins3)
        _record_abaf_coverage(learned_x2_bins3)
        _example_coverage_report(
            target="x2",
            bk_path=bk_x2_bins3,
            learned_rules=learned_x2_bins3,
            pos_examples=pos_x2,
            neg_examples=neg_x2,
        )
        deps_x2b3 = _summarize_target_rule_dependencies("x2", learned_x2_bins3)
        stats_x2b3 = _correspondence_stats("x2", learned_x2_bins3, edges)
        logger.info("Dependencies (target rule prefixes): %s", deps_x2b3)
        logger.info("GT sets: parents=%s | ancestors=%s", stats_x2b3["parents"], stats_x2b3["ancestors"])
        logger.info(
            "Corr vs GT: rules=%d triv=%d nontriv=%d parent=%d anc_only=%d offgraph=%d",
            stats_x2b3["target_rules"],
            stats_x2b3["trivial"],
            stats_x2b3["nontrivial"],
            stats_x2b3["parent_hit"],
            stats_x2b3["ancestor_only_hit"],
            stats_x2b3["offgraph_var_hit"],
        )

    def _run_continuous_all_targets(
        self,
        *,
        edges: set,
        sample_size: int,
        run_prefix: str,
        dgp: str,
        run_title: str,
    ) -> None:
        """Shared continuous-zoo driver: simulate once, learn x0/x1/x2 with median E+/E-."""
        data = simulate_linear_continuous_data(
            num_of_nodes=3,
            sample_size=sample_size,
            truth_DAG_directed_edges=edges,
            noise_type="gaussian",
            random_seed=42,
        )
        df = pd.DataFrame(data, columns=["x0", "x1", "x2"])
        var_types = {c: "continuous" for c in df.columns}

        _log_run_header(
            run_title,
            n_samples=len(df),
            dgp=dgp,
            gt_edges=edges,
        )

        if not self.runner.prolog_available:
            self.skipTest("SWI-Prolog not available")

        for target in ("x0", "x1", "x2"):
            bk_path = generate_aba_background_knowledge(
                df,
                var_types,
                f"{run_prefix}_{target}",
                self.output_dir,
                exclude_cols=[target],
                continuous_bins=2,
                bin_strategy="quantile",
            )
            pos_examples, neg_examples = _median_pos_neg_examples(df, target)
            if not pos_examples or not neg_examples:
                self.skipTest(f"Need both positive and negative examples for {target}")

            _log_aba_asp_call(bk_path, pos_examples, neg_examples)
            res = self.runner.run_prolog_aba_asp(
                bk_path,
                positive_examples=pos_examples,
                negative_examples=neg_examples,
                learning_options={"folding_steps": "15"},
            )
            self.assertEqual(res.get("status"), "completed")

            learned = _extract_learned_rules(bk_path)
            _log_learned_rules_block(target, learned)
            _log_triviality(target, learned)
            _record_abaf_coverage(learned)
            _example_coverage_report(
                target=target,
                bk_path=bk_path,
                learned_rules=learned,
                pos_examples=pos_examples,
                neg_examples=neg_examples,
            )

            deps = _summarize_target_rule_dependencies(target, learned)
            stats = _correspondence_stats(target, learned, edges)
            logger.info("Dependencies (target rule prefixes): %s", deps)
            logger.info("GT sets: parents=%s | ancestors=%s", stats["parents"], stats["ancestors"])
            logger.info(
                "Corr vs GT: rules=%d triv=%d nontriv=%d parent=%d anc_only=%d offgraph=%d",
                stats["target_rules"],
                stats["trivial"],
                stats["nontrivial"],
                stats["parent_hit"],
                stats["ancestor_only_hit"],
                stats["offgraph_var_hit"],
            )

            # ABA-ASP can legitimately return "* No solution found!" for some
            # configurations. In that case, no .bk.sol.aba is written and the learned
            # delta is empty; this test surfaces that behavior in the run summary.

    def test_continuous_confounder_x0_to_x1_x2_all_targets(self):
        """Continuous confounder: x0->x1 and x0->x2; learn all targets (median E+/E-)."""
        self._run_continuous_all_targets(
            edges={(0, 1), (0, 2)},
            sample_size=6,
            run_prefix="cont_confounder_6",
            dgp="x0→x1 and x0→x2 (linear Gaussian); median split; learn all targets",
            run_title="ArgCausalDisco continuous confounder (common cause)",
        )

    def test_continuous_collider_x0_x1_to_x2_all_targets(self):
        """Continuous collider: x0->x2 and x1->x2; learn all targets (median E+/E-)."""
        self._run_continuous_all_targets(
            edges={(0, 2), (1, 2)},
            sample_size=8,
            run_prefix="cont_collider_8",
            dgp="x0→x2 and x1→x2 (linear Gaussian); median split; learn all targets",
            run_title="ArgCausalDisco continuous collider (common effect)",
        )


class TestFoldingModes(unittest.TestCase):
    """Explore ABA-ASP folding modes on the same dataset.

    This is intentionally a light-touch integration test:
    - Ensures each supported folding mode runs to completion.
    - Logs how learned target rules vary (if at all) across modes.
    """

    @classmethod
    def setUpClass(cls):
        cls.output_dir = _get_test_output_dir(cls.__name__)
        cls.output_dir.mkdir(parents=True, exist_ok=True)
        cls.runner = ABASPRunner()

    def test_discrete_chain_across_folding_modes(self):
        edges = {(0, 1), (1, 2)}
        data = simulate_discrete_data(
            num_of_nodes=3,
            sample_size=12,
            truth_DAG_directed_edges=edges,
            random_seed=7,
        )
        df = pd.DataFrame(data, columns=["x0", "x1", "x2"])
        var_types = {c: "categorical" for c in df.columns}

        if not self.runner.prolog_available:
            self.skipTest("SWI-Prolog not available")

        _, pos_x2, neg_x2 = pick_target_variable(df, "x2")
        if not pos_x2 or not neg_x2:
            self.skipTest("Need both positive and negative examples for x2")

        modes = ["nd", "greedy", "all", "lazy"]
        learned_by_mode: dict[str, List[str]] = {}
        rows: List[dict] = []

        _log_run_header(
            "Folding-mode comparison (discrete chain)",
            n_samples=len(df),
            dgp="x0→x1→x2 (discrete); compare folding_mode in {nd,greedy,all,lazy}",
            gt_edges=edges,
        )

        for mode in modes:
            bk_path = generate_aba_background_knowledge(
                df,
                var_types,
                f"discrete_12_x2_folding_{mode}",
                self.output_dir,
                exclude_cols=["x2"],
            )
            _log_aba_asp_call(bk_path, pos_x2, neg_x2)
            res = self.runner.run_prolog_aba_asp(
                bk_path,
                positive_examples=pos_x2,
                negative_examples=neg_x2,
                learning_options={"folding_steps": "15", "folding_mode": mode, "verbosity": "off"},
            )
            self.assertEqual(res.get("status"), "completed")

            learned = _extract_learned_rules(bk_path)
            learned_by_mode[mode] = learned
            _record_abaf_coverage(learned)

            cov = _example_coverage_report(
                target="x2",
                bk_path=bk_path,
                learned_rules=learned,
                pos_examples=pos_x2,
                neg_examples=neg_x2,
                max_rule_lines=4,
            )

            abaf = _abaf_component_stats(learned)

            deps = _summarize_target_rule_dependencies("x2", learned)
            stats = _correspondence_stats("x2", learned, edges)
            counts = _extract_prolog_counts(res.get("stdout", ""))
            row = {
                "mode": mode,
                "learned": len(learned),
                "deps": deps,
                "parent": stats["parent_hit"],
                "anc_only": stats["ancestor_only_hit"],
                "offgraph": stats["offgraph_var_hit"],
                "bk_rules": counts.get("bk_rules"),
                "aba_rules": counts.get("aba_rules"),
                "aba_minus_bk": counts.get("aba_minus_bk"),
                "target_rules": stats["target_rules"],
                "triv": stats["trivial"],
                "nontriv": stats["nontrivial"],
            }
            rows.append(row)
            logger.info(
                "mode=%s | learned=%d | deps=%s | GT parent=%d anc_only=%d offgraph=%d | "
                "TP=%d FN=%d | TN=%d FP=%d | acc=%.3f | pos_cov=%.3f | neg_cov=%.3f | asm=%d ctr=%d",
                mode,
                len(learned),
                _format_counts(deps, max_items=4),
                stats["parent_hit"],
                stats["ancestor_only_hit"],
                stats["offgraph_var_hit"],
                int(cov.get("TP", 0)),
                int(cov.get("FN", 0)),
                int(cov.get("TN", 0)),
                int(cov.get("FP", 0)),
                float(cov.get("acc", 0.0)),
                float(cov.get("pos_cov", 0.0)),
                float(cov.get("neg_cov", 0.0)),
                int(abaf.get("assumptions", 0)),
                int(abaf.get("contraries", 0)),
            )

            # Clarify the common confusion: ABA-BK (Prolog internal counts) vs delta lines.
            if counts.get("bk_rules") is not None and counts.get("aba_rules") is not None:
                logger.info(
                    "mode=%s | Prolog counts: BK=%d ABA=%d (ABA-BK=%d) | delta_lines=%d",
                    mode,
                    counts["bk_rules"],
                    counts["aba_rules"],
                    counts.get("aba_minus_bk", 0),
                    len(learned),
                )

        unique_theories = {
            mode: tuple(sorted(set(rules)))
            for mode, rules in learned_by_mode.items()
        }
        n_unique = len(set(unique_theories.values()))
        logger.info("Folding-mode uniqueness: %d unique learned theories across %d modes", n_unique, len(modes))

        # Group modes by identical learned delta theories (so the summary can show which modes match).
        theory_to_modes: dict[tuple[str, ...], list[str]] = {}
        for mode, theory in unique_theories.items():
            theory_to_modes.setdefault(theory, []).append(mode)
        for theory, mode_list in sorted(theory_to_modes.items(), key=lambda kv: (-len(kv[1]), ",".join(sorted(kv[1])))):
            logger.info(
                "Folding-mode theory group: modes=%s | delta_lines=%d",
                ",".join(sorted(mode_list)),
                len(theory),
            )

        # Log the actual rule sets for each unique theory (so the end summary can print them).
        for theory, mode_list in sorted(theory_to_modes.items(), key=lambda kv: (-len(kv[1]), ",".join(sorted(kv[1])))):
            logger.info(
                "Folding-mode theory rules: modes=%s | delta_lines=%d",
                ",".join(sorted(mode_list)),
                len(theory),
            )
            for rule in theory:
                logger.info("  %s", rule)

        # Nice end-of-test summary block.
        logger.info("\nFOLDING MODE SUMMARY (target=x2)")
        logger.info("mode | delta_lines | target_rules triv/nontriv | BK->ABA | parent anc_only offgraph | deps")
        for row in rows:
            bk_aba = (
                f"{row['bk_rules']}→{row['aba_rules']}" if row.get("bk_rules") is not None and row.get("aba_rules") is not None else "?"
            )
            logger.info(
                "%s | %d | %d %d/%d | %s | %d %d %d | %s",
                row["mode"],
                row["learned"],
                row["target_rules"],
                row["triv"],
                row["nontriv"],
                bk_aba,
                row["parent"],
                row["anc_only"],
                row["offgraph"],
                _format_counts(row["deps"], max_items=5),
            )

        logger.info("\nDEFINITIONS")
        logger.info("deps: prefixes appearing in bodies of learned x2(A) rules (e.g., x0, x1, alpha)")
        logger.info("alpha: ABA assumptions introduced by the learner (alpha_*/1); may appear without any 'exception' dataset")
        logger.info("GT parent: count of learned x2 rules that mention direct-parent predicates (x1_*)")
        logger.info("anc_only: count of learned x2 rules that mention non-parent ancestors (x0_* here)")
        logger.info("offgraph: count of learned x2 rules that mention xK not in {x2}∪ancestors")
        logger.info(
            "BK→ABA: ABA-ASP internal rule counts printed by Prolog; delta_lines is our solution-file diff (can be larger)")

        self.assertTrue(
            any(len(rules) > 0 for rules in learned_by_mode.values()),
            "Expected at least one folding mode to learn a non-empty delta theory",
        )


def run_all_tests():
    """Run all test suites."""
    logger.info("\n" + "="*70)
    logger.info("ABA-ASP LEARNING TEST SUITE")
    logger.info("="*70 + "\n")

    # Keep test output readable: the Prolog runner and some dependencies can be very verbose.
    # The detailed logs are still available by increasing these loggers locally when debugging.
    for noisy in ("run_aba_asp", "argcausaldisco_integration"):
        logging.getLogger(noisy).setLevel(logging.WARNING)
    # pgmpy is chatty at WARNING; suppress those for normal runs.
    logging.getLogger("pgmpy").setLevel(logging.ERROR)

    # Capture log messages so we can print a clean, non-grepped summary at the end.
    capture = _LogCaptureHandler()
    logger.addHandler(capture)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestSimpleHandcraftedLearning))
    suite.addTests(loader.loadTestsFromTestCase(TestAssumptionIntroduction))
    suite.addTests(loader.loadTestsFromTestCase(TestMinimalDiscreteData))
    # Discrete data: chain/confounder/collider are grouped in one class.
    suite.addTests(loader.loadTestsFromTestCase(TestMinimalContinuousData))
    # BK ordering sensitivity: keep this before folding-mode comparison as requested.
    suite.addTests(loader.loadTestsFromTestCase(TestBKOrderingSensitivity))
    suite.addTests(loader.loadTestsFromTestCase(TestFoldingModes))

    # Greedy folding variants (append at the end as requested)
    suite.addTests(loader.loadTestsFromTestCase(TestGreedyFoldingDiscreteChain))
    suite.addTests(loader.loadTestsFromTestCase(TestGreedyFoldingConfounder))
    suite.addTests(loader.loadTestsFromTestCase(TestGreedyFoldingCollider))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    logger.info("\n" + "="*70)
    logger.info("TEST SUMMARY")
    logger.info("="*70)
    logger.info(f"Tests run: {result.testsRun}")
    logger.info(f"Failures: {len(result.failures)}")
    logger.info(f"Errors: {len(result.errors)}")
    logger.info(f"Skipped: {len(result.skipped)}")
    
    if result.wasSuccessful():
        logger.info("\n✓ All tests PASSED")
    else:
        logger.error("\n✗ Some tests FAILED")

    logger.info("\nABAF COVERAGE (across learned deltas)")
    logger.info(
        "Runs=%d | total_delta_lines=%d | assumption_lines=%d (runs=%d) | contrary_lines=%d (runs=%d)",
        _ABAF_COVERAGE["runs"],
        _ABAF_COVERAGE["total_learned_lines"],
        _ABAF_COVERAGE["assumptions"],
        _ABAF_COVERAGE["runs_with_assumption"],
        _ABAF_COVERAGE["contraries"],
        _ABAF_COVERAGE["runs_with_contrary"],
    )
    logger.info(
        "Mentions: alpha_=%d | c_alpha_=%d",
        _ABAF_COVERAGE["alpha_mentions"],
        _ABAF_COVERAGE["c_alpha_mentions"],
    )
    
    logger.info("="*70 + "\n")

    # Print a compact, readable run summary to stdout (no timestamps).
    try:
        runs = _parse_run_summaries(capture.messages)
        print(_render_run_summaries(runs, result))
    finally:
        logger.removeHandler(capture)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
