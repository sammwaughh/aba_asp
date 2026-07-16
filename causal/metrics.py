"""
Pure metrics helpers for ABA-ASP causal learning experiments.

See causal/aa-plans/METRICS.md for the full metric panel. This module is the
single, side-effect-free place where per-cell metrics are computed; it is called
by the grid runner (``experiments/run_grid.py``) and exercised directly by tests.
"""

from __future__ import annotations

import re
from collections import deque
from dataclasses import dataclass
import math
from pathlib import Path
from typing import Any, FrozenSet, Mapping, Sequence

VarSet = FrozenSet[str]

Outcome = str  # solved | completed_no_solution | completed_empty_delta | timeout | error | skipped

_FOLDING_TOKENS_RE = re.compile(
    r"Increasing folding tokens to:\s*(\d+)", re.IGNORECASE
)
_NO_SOLUTION_MARKER = "* No solution found!"

# Columns written to results.parquet (INFRA.md §5).
RESULT_PARQUET_COLUMNS: tuple[str, ...] = (
    "experiment_id",
    "dgp",
    "graph_type",
    "target",
    "n",
    "seed",
    "config_hash",
    "run_id",
    "outcome",
    "failure_reason",
    "wall_clock_s",
    "folding_tokens_used",
    "n_delta_rules",
    "n_target_rules",
    "n_assumptions",
    "n_contraries",
    "n_trivial_target_rules",
    "n_nontrivial_target_rules",
    "max_body_length",
    "mean_body_length",
    "body_parent_precision",
    "body_parent_recall",
    "body_parent_f1",
    "offgraph_rate",
    "ancestor_only_rate",
    "var_parent_precision",
    "var_parent_recall",
    "var_parent_jaccard",
    "clean_recovery",
    "cov_py_accuracy",
    "cov_py_pos",
    "cov_py_neg",
    "cov_py_tp",
    "cov_py_fp",
    "cov_py_tn",
    "cov_py_fn",
    "cov_pl_accuracy",
    "cov_pl_pos",
    "cov_pl_neg",
    "cov_pl_tp",
    "cov_pl_fp",
    "cov_pl_tn",
    "cov_pl_fn",
    "cov_gap_accuracy",
    "cov_gap_pos",
    "cov_gap_neg",
    "cov_asp_accuracy",
    "cov_asp_pos",
    "cov_asp_neg",
    "cov_asp_tp",
    "cov_asp_fp",
    "cov_asp_tn",
    "cov_asp_fn",
    "cov_asp_n_pos",
    "cov_asp_n_neg",
    "skel_precision",
    "skel_recall",
    "skel_f1",
    "dir_d1_precision",
    "dir_d1_recall",
    "dir_d1_f1",
    "dir_d2_precision",
    "dir_d2_recall",
    "dir_d2_f1",
    "bridge_mode",
    "shd",
    "dir_edge_precision",
    "dir_edge_recall",
    "dir_edge_f1",
    "runtime_s_bridge",
    "parser_unread_lines",
    "sol_file_bytes",
)

_FLOAT_METRICS_WITH_NAN_REASONS: tuple[str, ...] = (
    "mean_body_length",
    "body_parent_precision",
    "body_parent_recall",
    "body_parent_f1",
    "offgraph_rate",
    "ancestor_only_rate",
    "var_parent_precision",
    "var_parent_recall",
    "var_parent_jaccard",
    "cov_py_accuracy",
    "cov_py_pos",
    "cov_py_neg",
    "cov_pl_accuracy",
    "cov_pl_pos",
    "cov_pl_neg",
    "cov_gap_accuracy",
    "cov_gap_pos",
    "cov_gap_neg",
    "cov_asp_accuracy",
    "cov_asp_pos",
    "cov_asp_neg",
    "skel_precision",
    "skel_recall",
    "skel_f1",
    "dir_d1_precision",
    "dir_d1_recall",
    "dir_d1_f1",
    "dir_d2_precision",
    "dir_d2_recall",
    "dir_d2_f1",
    "dir_edge_precision",
    "dir_edge_recall",
    "dir_edge_f1",
    "runtime_s_bridge",
)

# Match xN optionally followed by a known suffix (_binK, _val_V, _gt_*, _lt_*, or generic).
_VAR_TOKEN_RE = re.compile(
    r"\b(x\d+)(?:_(?:bin\d+|val_\d+|gt_[a-z0-9_]+|lt_[a-z0-9_]+|[a-z0-9_]+))?\b"
)

_PER_SAMPLE_INDICATOR_RE = re.compile(r"^[A-Za-z0-9_]+\(A\)\s*:-\s*A=\d+\.$")
_BK_FEATURE_LINE_RE = re.compile(
    r"^\s*([a-zA-Z_][a-zA-Z0-9_]*)\(A\)\s*:-\s*A\s*=\s*(\d+)\s*\.\s*$"
)
_SAMPLE_ATOM_RE = re.compile(r"\((\d+)\)")


@dataclass(frozen=True)
class GroundTruth:
    """Directed ground-truth DAG over named nodes (e.g. x0, x1, x2)."""

    nodes: tuple[str, ...]
    edges: frozenset[tuple[str, str]]  # (parent, child)

    def parents_of(self, t: str) -> VarSet:
        """Direct parents of target t."""
        return frozenset(parent for parent, child in self.edges if child == t)

    def ancestors_of(self, t: str) -> VarSet:
        """All ancestors of t (parents and above), including direct parents."""
        if t not in self.nodes:
            return frozenset()

        reverse_adj: dict[str, set[str]] = {}
        for parent, child in self.edges:
            reverse_adj.setdefault(child, set()).add(parent)

        seen: set[str] = set()
        queue: deque[str] = deque(reverse_adj.get(t, ()))
        while queue:
            node = queue.popleft()
            if node in seen:
                continue
            seen.add(node)
            queue.extend(reverse_adj.get(node, ()))
        return frozenset(seen)


@dataclass(frozen=True)
class CellInputs:
    """Inputs required to compute the full per-cell metric panel (METRICS.md §5)."""

    experiment_id: str
    dgp: str
    graph_type: str
    target: str
    n: int
    seed: int | None
    config_hash: str
    run_id: str
    bk_path: Path
    sol_path: Path | None
    pos_examples: tuple[str, ...]
    neg_examples: tuple[str, ...]
    ground_truth: GroundTruth
    wall_clock_s: float
    outcome: str
    failure_reason: str | None
    folding_tokens_used: int
    query_timeout_s: float = 5.0
    skip_prolog_coverage: bool = False


def body_vars(literal: str) -> VarSet:
    """Map a body literal (or rule fragment) to base variable names.

    Strips ``_binK``, ``_val_V``, ``_gt_*``, ``_lt_*``, and other ``_[a-z0-9]+``
    suffixes after a leading ``x\\d+``, anchored on the full digit run so
    ``x10_bin0`` maps to ``{x10}`` rather than ``{x1}``.
    """
    return frozenset(m.group(1) for m in _VAR_TOKEN_RE.finditer(literal))


def _parse_rule_lines(text: str) -> list[str]:
    """Return non-comment Prolog clause lines (those with ``:-`` or ending ``.``)."""
    out: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("%"):
            continue
        if ":-" in line or line.endswith("."):
            out.append(line)
    return out


def _bk_path_from_sol(sol_path: Path) -> Path:
    """Derive the BK file path that corresponds to a solution file path."""
    name = sol_path.name
    if name.endswith(".bk.sol.aba"):
        base = name[: -len(".bk.sol.aba")]
        return sol_path.parent / f"{base}.bk.aba"
    if name.endswith(".sol.aba"):
        base = name[: -len(".sol.aba")]
        return sol_path.parent / f"{base}.aba"
    raise ValueError(f"Cannot derive BK path from solution file: {sol_path}")


def parse_delta_rules(sol_path: Path) -> list[str]:
    """Return δ-rules introduced by learning (solution rules minus BK rules).

    ``sol_path`` should point to a ``.bk.sol.aba`` (or ``.sol.aba``) file; the
    corresponding BK file is resolved in the same directory.
    """
    sol_path = Path(sol_path)
    if not sol_path.is_file():
        return []

    bk_path = _bk_path_from_sol(sol_path)
    if not bk_path.is_file():
        return []

    solution_rules = _parse_rule_lines(sol_path.read_text(encoding="utf-8"))
    bk_rules = _parse_rule_lines(bk_path.read_text(encoding="utf-8"))
    bk_set = set(bk_rules)
    learned = [r for r in solution_rules if r not in bk_set]
    return [r for r in learned if not _PER_SAMPLE_INDICATOR_RE.match(r)]


def _predicate_names_in_body(rule: str) -> list[str]:
    """Extract predicate functor names from the body of a Prolog-style rule."""
    if ":-" not in rule:
        return []
    body = rule.split(":-", 1)[1]
    body = body.strip().rstrip(".")
    names: list[str] = []
    for part in body.split(","):
        atom = part.strip()
        if not atom or "=" in atom:
            continue
        functor = atom.split("(", 1)[0].strip()
        if functor:
            names.append(functor)
    return names


def target_rule_filter(target: str, learned: Sequence[str]) -> list[str]:
    """Return δ-rules whose head matches ``target(A)``."""
    prefix = f"{target}(A)"
    return [r for r in learned if r.startswith(prefix)]


def triviality_counts(target: str, learned: Sequence[str]) -> dict[str, int | float]:
    """Count trivial vs non-trivial target rules (METRICS.md §3.3).

    A target rule is *trivial* when every body functor is derived only from the
    target variable (prefix ``{target}_``). Matches
    ``test_aba_learning._summarize_target_rule_triviality``.
    """
    target_rules = target_rule_filter(target, learned)
    n_trivial = 0
    n_nontrivial = 0
    body_lengths: list[int] = []

    for rule in target_rules:
        functors = _predicate_names_in_body(rule)
        body_lengths.append(len(functors))
        if not functors or all(f.startswith(f"{target}_") for f in functors):
            n_trivial += 1
        else:
            n_nontrivial += 1

    n_target = len(target_rules)
    if body_lengths:
        max_body_length = max(body_lengths)
        mean_body_length = sum(body_lengths) / len(body_lengths)
    else:
        max_body_length = 0
        mean_body_length = math.nan

    return {
        "n_target_rules": n_target,
        "n_trivial_target_rules": n_trivial,
        "n_nontrivial_target_rules": n_nontrivial,
        "max_body_length": max_body_length,
        "mean_body_length": mean_body_length,
    }


def abaf_structure_counts(learned: Sequence[str]) -> dict[str, int]:
    """Count ABAF structural lines in the learned δ-set (METRICS.md §3.3).

    Matches ``test_aba_learning._abaf_component_stats`` key-for-key.
    """
    assumptions = [r for r in learned if r.startswith("assumption(")]
    contraries = [r for r in learned if r.startswith("contrary(")]
    alpha_mentions = [r for r in learned if "alpha_" in r]
    c_alpha_mentions = [r for r in learned if "c_alpha" in r]
    return {
        "n_delta_rules": len(learned),
        "assumptions": len(assumptions),
        "contraries": len(contraries),
        "alpha_mentions": len(alpha_mentions),
        "c_alpha_mentions": len(c_alpha_mentions),
    }


def _harmonic_mean(a: float, b: float) -> float:
    """Harmonic mean of two values; NaN if either is NaN, 0.0 if both are 0."""
    if math.isnan(a) or math.isnan(b):
        return math.nan
    if a + b == 0:
        return 0.0
    return 2.0 * a * b / (a + b)


def _parse_sample_id(atom: str) -> int:
    """Extract the numeric sample id from an example atom, e.g. ``x2(3)`` -> 3."""
    match = _SAMPLE_ATOM_RE.search(atom)
    if not match:
        raise ValueError(f"Could not parse sample id from atom: {atom}")
    return int(match.group(1))


def parse_bk_feature_map(bk_path: Path) -> dict[int, frozenset[str]]:
    """Parse BK feature lines ``pred(A) :- A=n.`` into per-sample feature sets."""
    feature_map: dict[int, set[str]] = {}
    text = Path(bk_path).read_text(encoding="utf-8")
    for line in text.splitlines():
        if not line or line.startswith("%"):
            continue
        match = _BK_FEATURE_LINE_RE.match(line)
        if not match:
            continue
        pred = match.group(1)
        sid = int(match.group(2))
        feature_map.setdefault(sid, set()).add(pred)
    return {sid: frozenset(preds) for sid, preds in feature_map.items()}


def _rule_holds_for_sample(
    rule: str, sample_id: int, sample_features: frozenset[str]
) -> bool:
    """Whether a Horn rule body holds for one sample (BK feature predicates only)."""
    if ":-" not in rule:
        return False
    for functor in _predicate_names_in_body(rule):
        if not functor:
            continue
        if functor.startswith("alpha") or functor.startswith("c_alpha"):
            continue
        if functor not in sample_features:
            return False
    return True


def _is_nontrivial_target_rule(target: str, rule: str) -> bool:
    """True if the rule body cites a predicate not derived solely from the target."""
    functors = _predicate_names_in_body(rule)
    if not functors:
        return False
    return not all(f.startswith(f"{target}_") for f in functors)


def _rule_body_var_set(rule: str) -> VarSet:
    """Base variable names cited in a rule's body (empty for a fact)."""
    if ":-" not in rule:
        return frozenset()
    return body_vars(rule.split(":-", 1)[1])


def body_level_stats(
    target: str,
    learned: Sequence[str],
    ground_truth: GroundTruth,
) -> dict[str, int | float | bool]:
    """Body-level RQ1 metrics over non-trivial target rules (METRICS.md §3.4)."""
    parents = ground_truth.parents_of(target)
    ancestors = ground_truth.ancestors_of(target)
    universe = frozenset(ground_truth.nodes)

    nontrivial_rules = [
        r
        for r in target_rule_filter(target, learned)
        if _is_nontrivial_target_rule(target, r)
    ]
    n_nt = len(nontrivial_rules)

    parent_hits = 0
    ancestor_only_hits = 0
    offgraph_hits = 0
    degenerate_hits = 0
    parents_recalled: set[str] = set()

    for rule in nontrivial_rules:
        vars_r = _rule_body_var_set(rule)
        graph_vars = vars_r & universe

        if not graph_vars:
            degenerate_hits += 1
            continue

        if vars_r & parents:
            parent_hits += 1
            parents_recalled |= vars_r & parents
        elif vars_r & ancestors:
            ancestor_only_hits += 1
        else:
            offgraph_hits += 1

    mass_balance_ok = (
        parent_hits + ancestor_only_hits + offgraph_hits + degenerate_hits == n_nt
    )

    if n_nt == 0:
        precision = math.nan
        offgraph_rate = math.nan
        ancestor_only_rate = math.nan
    else:
        precision = parent_hits / n_nt
        offgraph_rate = offgraph_hits / n_nt
        ancestor_only_rate = ancestor_only_hits / n_nt

    if not parents:
        recall = math.nan
    else:
        recall = len(parents_recalled) / len(parents)

    f1 = _harmonic_mean(precision, recall)

    return {
        "body_parent_precision": precision,
        "body_parent_recall": recall,
        "body_parent_f1": f1,
        "offgraph_rate": offgraph_rate,
        "ancestor_only_rate": ancestor_only_rate,
        "degenerate_hit": degenerate_hits,
        "mass_balance_ok": mass_balance_ok,
    }


def variable_level_stats(
    target: str,
    learned: Sequence[str],
    ground_truth: GroundTruth,
) -> dict[str, float | int]:
    """Variable-level set comparison of recovered body vars vs true parents.

    ``recovered`` is the union of graph variables cited across all non-trivial
    target rules (with the target itself removed). This complements the
    rule-level ``body_level_stats``: here precision penalises *any*
    ancestor/off-graph contamination in the recovered set, and
    ``clean_recovery`` is the strict full-success flag (recovered set equals the
    true parent set, nothing more, nothing less). See METRICS.md §3.4b.
    """
    parents = ground_truth.parents_of(target)
    universe = frozenset(ground_truth.nodes)

    nontrivial_rules = [
        r
        for r in target_rule_filter(target, learned)
        if _is_nontrivial_target_rule(target, r)
    ]
    recovered: set[str] = set()
    for rule in nontrivial_rules:
        recovered |= _rule_body_var_set(rule) & universe
    recovered.discard(target)
    recovered_fs = frozenset(recovered)

    inter = recovered_fs & parents
    union = recovered_fs | parents

    var_precision = len(inter) / len(recovered_fs) if recovered_fs else math.nan
    var_recall = len(inter) / len(parents) if parents else math.nan
    var_jaccard = len(inter) / len(union) if union else math.nan
    # Strict success: recovered exactly the parent set (and there is a parent set).
    clean = 1 if (bool(parents) and recovered_fs == parents) else 0

    return {
        "var_parent_precision": var_precision,
        "var_parent_recall": var_recall,
        "var_parent_jaccard": var_jaccard,
        "clean_recovery": clean,
    }


def python_horn_coverage(
    bk_path: Path,
    learned: Sequence[str],
    pos: Sequence[str],
    neg: Sequence[str],
    *,
    target: str | None = None,
) -> dict[str, float | int]:
    """Python-Horn coverage of E+/E- by learned target rules (METRICS.md §3.5)."""
    if target is None:
        if not pos:
            raise ValueError("Cannot infer target without positive examples")
        target = pos[0].split("(", 1)[0]

    feature_map = parse_bk_feature_map(bk_path)
    target_rules = target_rule_filter(target, learned)

    pos_ids = [_parse_sample_id(atom) for atom in pos]
    neg_ids = [_parse_sample_id(atom) for atom in neg]

    def _predict(sample_id: int) -> bool:
        feats = feature_map.get(sample_id, frozenset())
        return any(_rule_holds_for_sample(r, sample_id, feats) for r in target_rules)

    tp = sum(1 for sid in pos_ids if _predict(sid))
    fn = len(pos_ids) - tp
    fp = sum(1 for sid in neg_ids if _predict(sid))
    tn = len(neg_ids) - fp

    total = len(pos_ids) + len(neg_ids)
    accuracy = (tp + tn) / total if total else 0.0
    pos_cov = tp / len(pos_ids) if pos_ids else 0.0
    neg_cov = tn / len(neg_ids) if neg_ids else 0.0

    return {
        "cov_py_tp": tp,
        "cov_py_fp": fp,
        "cov_py_tn": tn,
        "cov_py_fn": fn,
        "cov_py_accuracy": accuracy,
        "cov_py_pos": pos_cov,
        "cov_py_neg": neg_cov,
    }


def prolog_aware_coverage(
    sol_path: Path | None,
    bk_path: Path,
    pos_examples: Sequence[str],
    neg_examples: Sequence[str],
    *,
    timeout_s: float = 5.0,
) -> dict[str, float | int]:
    """Prolog-aware coverage (METRICS.md §3.5).

    Queries each example against the produced solution program when available,
    otherwise falls back to the original BK program.
    """
    # Local import to keep metrics.py usable when Prolog isn't installed.
    from causal.run_aba_asp import query_examples  # noqa: WPS433

    program = Path(sol_path) if sol_path is not None else Path(bk_path)
    examples = list(pos_examples) + list(neg_examples)
    if not examples:
        # No examples: define coverage as 0.0 with zero counts.
        return {
            "cov_pl_accuracy": 0.0,
            "cov_pl_pos": 0.0,
            "cov_pl_neg": 0.0,
            "cov_pl_tp": 0,
            "cov_pl_fp": 0,
            "cov_pl_tn": 0,
            "cov_pl_fn": 0,
            "cov_gap_accuracy": math.nan,
            "cov_gap_pos": math.nan,
            "cov_gap_neg": math.nan,
        }

    try:
        entail = query_examples(program, examples, timeout_s=timeout_s)
    except Exception:
        nan = math.nan
        return {
            "cov_pl_accuracy": nan,
            "cov_pl_pos": nan,
            "cov_pl_neg": nan,
            "cov_pl_tp": 0,
            "cov_pl_fp": 0,
            "cov_pl_tn": 0,
            "cov_pl_fn": 0,
            "cov_gap_accuracy": nan,
            "cov_gap_pos": nan,
            "cov_gap_neg": nan,
        }

    tp = sum(1 for ex in pos_examples if entail.get(ex, False))
    fn = len(pos_examples) - tp
    fp = sum(1 for ex in neg_examples if entail.get(ex, False))
    tn = len(neg_examples) - fp

    total = len(pos_examples) + len(neg_examples)
    accuracy = (tp + tn) / total if total else 0.0
    pos_cov = tp / len(pos_examples) if pos_examples else 0.0
    neg_cov = tn / len(neg_examples) if neg_examples else 0.0

    return {
        "cov_pl_accuracy": accuracy,
        "cov_pl_pos": pos_cov,
        "cov_pl_neg": neg_cov,
        "cov_pl_tp": tp,
        "cov_pl_fp": fp,
        "cov_pl_tn": tn,
        "cov_pl_fn": fn,
        # gap keys are filled in by compute_cell_metrics because they depend on cov_py_*
        "cov_gap_accuracy": math.nan,
        "cov_gap_pos": math.nan,
        "cov_gap_neg": math.nan,
    }


def parse_folding_tokens_used(stdout: str) -> int:
    """Last ``Increasing folding tokens to: K`` value in Prolog stdout, or 0."""
    matches = _FOLDING_TOKENS_RE.findall(stdout)
    if not matches:
        return 0
    return int(matches[-1])


def outcome_classifier(
    stdout: str,
    sol_path: Path | None,
    learned_rules: Sequence[str],
    wall_clock_s: float,
    timeout_s: float,
    examples_ok: bool,
) -> tuple[str, str | None]:
    """Map raw run signals to an outcome category (METRICS.md §2, INFRA.md §4.6)."""
    if not examples_ok:
        return "skipped", "empty E+ or E-"
    if timeout_s > 0 and wall_clock_s >= timeout_s:
        return (
            "timeout",
            f"wall_clock_s={wall_clock_s:.3f} >= prolog_timeout_s={timeout_s}",
        )

    sol_exists = sol_path is not None and Path(sol_path).is_file()
    if sol_exists:
        if len(learned_rules) >= 1:
            return "solved", None
        return (
            "completed_empty_delta",
            "solution file present but zero delta rules",
        )

    if _NO_SOLUTION_MARKER in stdout:
        return "completed_no_solution", "Prolog reported no solution"

    return "error", "no solution file and no recognized completion signal"


def _count_parser_unread_lines(sol_path: Path | None) -> int:
    """Count non-comment lines in the solution file the rule parser did not classify."""
    if sol_path is None or not Path(sol_path).is_file():
        return 0
    text = Path(sol_path).read_text(encoding="utf-8")
    parsed = set(_parse_rule_lines(text))
    unread = 0
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("%"):
            continue
        if line not in parsed:
            unread += 1
    return unread


def _learned_for_metrics(inp: CellInputs) -> tuple[str, ...]:
    """Learned δ-rules to score: the parsed solution if solved, else empty."""
    if inp.outcome == "solved" and inp.sol_path is not None:
        return tuple(parse_delta_rules(inp.sol_path))
    return ()


def _placeholder_prolog_coverage(*, nan_reason: str = "prolog_unavailable_or_failed") -> dict[str, float | int]:
    """Prolog-aware coverage not computed (unavailable or explicitly skipped)."""
    nan = math.nan
    return {
        "cov_pl_accuracy": nan,
        "cov_pl_pos": nan,
        "cov_pl_neg": nan,
        "cov_pl_tp": 0,
        "cov_pl_fp": 0,
        "cov_pl_tn": 0,
        "cov_pl_fn": 0,
        "cov_gap_accuracy": nan,
        "cov_gap_pos": nan,
        "cov_gap_neg": nan,
        "_cov_pl_nan_reason": nan_reason,
    }


def _placeholder_skeleton_and_bridge() -> dict[str, Any]:
    """Reserved implied-skeleton and bridge columns — not computed; always NaN/None.

    These columns exist in the results schema so it stays stable if the metrics
    are added later (see METRICS.md §3.7).
    """
    nan = math.nan
    return {
        "skel_precision": nan,
        "skel_recall": nan,
        "skel_f1": nan,
        "dir_d1_precision": nan,
        "dir_d1_recall": nan,
        "dir_d1_f1": nan,
        "dir_d2_precision": nan,
        "dir_d2_recall": nan,
        "dir_d2_f1": nan,
        "bridge_mode": None,
        "shd": None,
        "dir_edge_precision": nan,
        "dir_edge_recall": nan,
        "dir_edge_f1": nan,
        "runtime_s_bridge": nan,
    }


def _nan_reason_for_metric(
    metric: str,
    panel: Mapping[str, Any],
    inp: CellInputs,
) -> str:
    """Return a short machine-readable reason explaining why ``metric`` is NaN."""
    if metric.startswith("cov_pl_") or metric.startswith("cov_gap_"):
        if inp.skip_prolog_coverage:
            return "grid_skip_prolog_coverage"
        if not inp.pos_examples and not inp.neg_examples:
            return "no_examples"
        return "prolog_unavailable_or_failed"
    if metric.startswith("cov_asp_"):
        if not inp.pos_examples and not inp.neg_examples:
            return "no_examples"
        reason = panel.get("_cov_asp_nan_reason")
        if isinstance(reason, str) and reason:
            return reason
        return "asp_unavailable_or_failed"
    if metric.startswith(("skel_", "dir_d1_", "dir_d2_")):
        return "implied_skeleton_not_aggregated"
    if metric.startswith("dir_edge_") or metric == "runtime_s_bridge":
        return "bridge_not_run"
    if metric == "mean_body_length" and panel.get("n_target_rules", 0) == 0:
        return "no_target_rules"
    if metric == "body_parent_recall":
        if not inp.ground_truth.parents_of(inp.target):
            return "no_parents"
    if metric in ("body_parent_precision", "body_parent_f1", "offgraph_rate", "ancestor_only_rate"):
        if panel.get("n_nontrivial_target_rules", 0) == 0:
            return "no_nontrivial_rules"
    if metric == "var_parent_precision":
        return "no_recovered_vars"
    if metric == "var_parent_recall":
        if not inp.ground_truth.parents_of(inp.target):
            return "no_parents"
    if metric == "var_parent_jaccard":
        return "no_vars_or_parents"
    if metric == "body_parent_f1":
        if math.isnan(float(panel.get("body_parent_precision", 0.0))) or math.isnan(
            float(panel.get("body_parent_recall", 0.0))
        ):
            return "precision_or_recall_unavailable"
    if metric == "cov_py_accuracy" and not inp.pos_examples and not inp.neg_examples:
        return "no_examples"
    return "not_applicable"


def _attach_nan_reasons(panel: dict[str, Any], inp: CellInputs) -> None:
    """Add a ``<metric>_nan_reason`` key for every NaN float metric in the panel."""
    for key in _FLOAT_METRICS_WITH_NAN_REASONS:
        value = panel.get(key)
        if isinstance(value, float) and math.isnan(value):
            panel[f"{key}_nan_reason"] = _nan_reason_for_metric(key, panel, inp)


def compute_cell_metrics(inp: CellInputs) -> dict[str, Any]:
    """Assemble the full per-cell metric panel (METRICS.md §3, INFRA.md §5)."""
    learned = _learned_for_metrics(inp)
    triv = triviality_counts(inp.target, learned)
    abaf = abaf_structure_counts(learned)
    body = body_level_stats(inp.target, learned, inp.ground_truth)
    var = variable_level_stats(inp.target, learned, inp.ground_truth)
    cov_py = python_horn_coverage(
        inp.bk_path,
        learned,
        inp.pos_examples,
        inp.neg_examples,
        target=inp.target,
    )
    if inp.skip_prolog_coverage:
        cov_pl = _placeholder_prolog_coverage(nan_reason="grid_skip_prolog_coverage")
    else:
        cov_pl = prolog_aware_coverage(
            inp.sol_path,
            inp.bk_path,
            inp.pos_examples,
            inp.neg_examples,
            timeout_s=inp.query_timeout_s,
        )
    cov_pl.pop("_cov_pl_nan_reason", None)
    # Gaps are defined as Prolog-aware minus Python-Horn (METRICS.md §3.5).
    if isinstance(cov_pl.get("cov_pl_accuracy"), float) and not math.isnan(
        float(cov_pl["cov_pl_accuracy"])
    ):
        cov_pl["cov_gap_accuracy"] = float(cov_pl["cov_pl_accuracy"]) - float(
            cov_py["cov_py_accuracy"]
        )
        cov_pl["cov_gap_pos"] = float(cov_pl["cov_pl_pos"]) - float(cov_py["cov_py_pos"])
        cov_pl["cov_gap_neg"] = float(cov_pl["cov_pl_neg"]) - float(cov_py["cov_py_neg"])

    from causal.asp_coverage import (  # noqa: WPS433
        asp_answer_set_coverage,
        resolve_sol_asp_path,
    )

    sol_asp = resolve_sol_asp_path(inp.bk_path, inp.sol_path)
    if inp.outcome == "solved" and sol_asp is not None:
        cov_asp = asp_answer_set_coverage(
            sol_asp,
            inp.pos_examples,
            inp.neg_examples,
            timeout_s=inp.query_timeout_s,
        )
    else:
        cov_asp = asp_answer_set_coverage(
            None,
            inp.pos_examples,
            inp.neg_examples,
            timeout_s=inp.query_timeout_s,
        )
        if inp.outcome != "solved":
            cov_asp["_cov_asp_nan_reason"] = "not_solved"
        elif sol_asp is None:
            cov_asp["_cov_asp_nan_reason"] = "sol_asp_missing"
    asp_nan_reason = cov_asp.pop("_cov_asp_nan_reason", None)

    sol_bytes = 0
    if inp.sol_path is not None and Path(inp.sol_path).is_file():
        sol_bytes = Path(inp.sol_path).stat().st_size

    panel: dict[str, Any] = {
        "experiment_id": inp.experiment_id,
        "dgp": inp.dgp,
        "graph_type": inp.graph_type,
        "target": inp.target,
        "n": inp.n,
        "seed": inp.seed,
        "config_hash": inp.config_hash,
        "run_id": inp.run_id,
        "outcome": inp.outcome,
        "failure_reason": inp.failure_reason,
        "wall_clock_s": inp.wall_clock_s,
        "folding_tokens_used": inp.folding_tokens_used,
        "n_delta_rules": abaf["n_delta_rules"],
        "n_target_rules": triv["n_target_rules"],
        "n_assumptions": abaf["assumptions"],
        "n_contraries": abaf["contraries"],
        "n_trivial_target_rules": triv["n_trivial_target_rules"],
        "n_nontrivial_target_rules": triv["n_nontrivial_target_rules"],
        "max_body_length": triv["max_body_length"],
        "mean_body_length": triv["mean_body_length"],
        "body_parent_precision": body["body_parent_precision"],
        "body_parent_recall": body["body_parent_recall"],
        "body_parent_f1": body["body_parent_f1"],
        "offgraph_rate": body["offgraph_rate"],
        "ancestor_only_rate": body["ancestor_only_rate"],
        "var_parent_precision": var["var_parent_precision"],
        "var_parent_recall": var["var_parent_recall"],
        "var_parent_jaccard": var["var_parent_jaccard"],
        "clean_recovery": var["clean_recovery"],
        "parser_unread_lines": _count_parser_unread_lines(inp.sol_path),
        "sol_file_bytes": sol_bytes,
    }
    panel.update(cov_py)
    panel.update(cov_pl)
    panel.update(cov_asp)
    if asp_nan_reason is not None:
        panel["_cov_asp_nan_reason"] = asp_nan_reason
    panel.update(_placeholder_skeleton_and_bridge())
    _attach_nan_reasons(panel, inp)
    panel.pop("_cov_asp_nan_reason", None)
    return panel
