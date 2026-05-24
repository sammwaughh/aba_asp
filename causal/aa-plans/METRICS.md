# Metrics Specification

**Status:** living document. Last updated: 2026-05-24.
**Companion docs:** `EXPERIMENTS_PLAN.md`, `INFRA.md`.

This document defines **exactly** how outcomes are measured across every experiment in this project. It is the single source of truth: any metric appearing in the report or in `results.parquet` must be defined here, with a formula and an edge-case rule. If you want a new metric, add it here first.

The goal is twofold: (i) make every figure in the report **reproducible** from the per-cell `metrics.json` files; (ii) keep `metrics.py` a single, side-effect-free module callable both from tests and from the batch runner.

---

## 1. Scope and units of analysis

The atomic **unit of analysis** is a single learning **cell**:

```
cell = (experiment_id, dgp, target, n, seed, config)
```

where `config` captures all knobs that vary across an experiment's grid (e.g. `folding_steps`, `bins`, `bin_strategy`, `noise`, BK content, etc.). One cell produces:

- one BK file (`.bk.aba`), one CSV (and `.binned.csv` if continuous),
- zero or one solution files (`.bk.sol.aba` if Prolog found a solution),
- one `metrics.json` containing the **metric panel** defined below,
- one row appended to the experiment's `results.parquet`.

Aggregation is downstream of cells: figures group by `(dgp, target, n, ...)` and reduce over `seed`.

---

## 2. Outcome category (categorical)

Every cell takes exactly one of these values. We surface this in the report because "no solution found" is a real result, not an error.

| Value | Meaning |
|-------|---------|
| `solved` | Prolog produced a `.bk.sol.aba` and `_extract_learned_rules` returned ≥1 δ-rule. |
| `completed_no_solution` | Prolog ran to completion but printed `* No solution found!` (no `.bk.sol.aba`, empty δ-set). |
| `completed_empty_delta` | A `.bk.sol.aba` exists but `_extract_learned_rules` returned 0 δ-rules (rare but possible after subsumption). |
| `timeout` | Prolog did not finish within the configured time-box. |
| `error` | Any other failure mode (parsing, crash, missing inputs). |
| `skipped` | Cell intentionally skipped (e.g. empty E+ or E−). |

Each cell carries a `failure_reason` string when outcome ∉ {`solved`}.

**Reporting rule:** for any cell-derived numeric metric, also report **fraction_solved** = #cells with outcome=`solved` / #cells. Numeric metrics are computed only over `solved` cells unless stated otherwise; we must say so in the figure caption.

---

## 3. The metric panel (one panel per cell)

The full per-cell schema. Numeric metrics are `NaN` when not applicable; the runner records this in `metrics.json` so downstream analysis can detect missingness without re-running.

### 3.1 Identification

```
experiment_id    : str        # e.g. "E02_seed_robustness"
dgp              : str        # e.g. "G3-chain", "G4-hub"
graph_type       : str        # "discrete" | "continuous"
target           : str        # e.g. "x2"
n                : int        # sample size
seed             : int
config_hash      : str        # short hash of the full YAML config
run_id           : str        # unique per cell (experiment_id + index)
```

### 3.2 Outcome

```
outcome          : str        # see Section 2
failure_reason   : str | None
wall_clock_s     : float      # total seconds in the Prolog call
folding_tokens_used : int     # last "Increasing folding tokens to: K" seen, or 0
```

### 3.3 δ-rule structure

```
n_delta_rules        : int    # all δ-rules (any head)
n_target_rules       : int    # δ-rules whose head matches the target
n_assumptions        : int    # alpha_*/N in the ABAF
n_contraries         : int    # c_alpha_*/N
n_trivial_target_rules : int  # body literal head-equivalent (e.g. x2(A) :- x2(A).)
n_nontrivial_target_rules : int
max_body_length      : int    # over target rules
mean_body_length     : float  # over target rules (NaN if 0)
```

### 3.4 Body-level metrics (RQ1)

These are computed **over non-trivial target rules**. They are the main quantitative answer to RQ1.

Let:
- `P_t` = set of true parents of target `t` in G\*.
- `A_t` = set of true ancestors of `t` (parents and above).
- `V_t` = the universe of variables (`{x0, x1, ...}`).
- For a δ-rule `r` with body literals like `x0_bin0(A)`, `x1(A)`, define `vars(r)` = the set of base variable names cited (here `{x0, x1}` after stripping `_binK`, `_val_V`, etc.).

Per non-trivial target rule `r`:

- `parent_hit(r)` = 1 if `vars(r) ∩ P_t ≠ ∅`, else 0.
- `ancestor_only_hit(r)` = 1 if `vars(r) ∩ A_t ≠ ∅` and `vars(r) ∩ P_t = ∅`, else 0.
- `offgraph_hit(r)` = 1 if `vars(r) ⊄ A_t` *and* (none of its cited vars are in `A_t`), else 0.

Aggregated **per cell**:

| Metric | Formula | Range | Edge cases |
|--------|---------|-------|------------|
| `body_parent_precision` | (Σ `parent_hit(r)`) / (#non-trivial target rules) | [0,1] | NaN if no non-trivial target rules. |
| `body_parent_recall` | `\|{v ∈ P_t : ∃ r with v ∈ vars(r)}\| / \|P_t\|` | [0,1] | NaN if `P_t = ∅`. |
| `body_parent_f1` | Harmonic mean of precision/recall | [0,1] | NaN if either is NaN. |
| `offgraph_rate` | (Σ `offgraph_hit(r)`) / (#non-trivial target rules) | [0,1] | NaN if no non-trivial rules. |
| `ancestor_only_rate` | (Σ `ancestor_only_hit(r)`) / (#non-trivial target rules) | [0,1] | same. |

**Variable-stripping rule.** When mapping a body literal to a base variable, strip `_binK`, `_val_V`, `_gt_*`, `_lt_*` and any suffix matching `_[a-z0-9]+` after the leading `x\d+`. Implementation lives in `metrics.body_vars(lit) -> set[str]`. The current `_correspondence_stats` does a simpler prefix match; we will reuse and tighten it.

**Direction note.** "Body-parent precision" treats a rule body as a *predictor set*. It does not assert direction — that interpretation belongs to E09's implied-skeleton step (Section 3.7 below).

### 3.5 Coverage (Python-Horn and Prolog-aware)

We report **both** definitions and the gap between them. The gap is itself a finding (it reflects ABAF assumption machinery that the Horn check ignores).

For each cell, given E+ and E−:

- **Python-Horn coverage** (already implemented in `_example_coverage_report`):
  - Treats δ-rules as plain Horn clauses; computes `TP, FP, TN, FN`, `accuracy`, `pos_coverage`, `neg_coverage` by saturating BK + δ.
  - Naming: `cov_py_accuracy`, `cov_py_pos`, `cov_py_neg`, `cov_py_tp/fp/tn/fn`.

- **Prolog-aware coverage** (*new*, to be implemented):
  - For each `e ∈ E+ ∪ E−`, query `e` against the produced `.bk.sol.aba` (or the original `.bk.aba` if outcome ≠ `solved`) via the existing Prolog backend, respecting assumptions and contraries.
  - Naming: `cov_pl_accuracy`, `cov_pl_pos`, `cov_pl_neg`, `cov_pl_tp/fp/tn/fn`.
  - Implementation: extend `run_aba_asp` (or add a sibling helper) with a `query_examples` entry point that returns boolean entailment per example. Time-boxed per query (default 5s).

- **Gap metrics**:
  - `cov_gap_accuracy = cov_pl_accuracy - cov_py_accuracy`
  - `cov_gap_pos = cov_pl_pos - cov_py_pos`
  - `cov_gap_neg = cov_pl_neg - cov_py_neg`

If outcome ≠ `solved`, Python-Horn coverage is computed against an **empty δ-set** (so `cov_py_pos = 0`, `cov_py_neg = 1` typically), and Prolog-aware coverage queries the original `.bk.aba`. Both are still meaningful and recorded.

### 3.6 Outcome stability metrics (within a cell)

Cheap, but useful when debugging E07 (learner ablation):

```
parser_unread_lines : int     # lines in *.sol.aba we did not classify (sanity)
sol_file_bytes      : int     # size of *.sol.aba if present, 0 otherwise
```

### 3.7 Implied-skeleton metrics (RQ3 / E09)

Computed at a **higher level** than a single cell: per `(dgp, n, seed, config)` aggregated across targets. We still emit them in the cell's metrics for the cell whose target is the *last* in the canonical order `x0, x1, ..., x_{k-1}`, with the rest empty. The runner does this aggregation step explicitly.

Let `B_t` = the set of variables cited (after stripping) across all non-trivial target rules for target `t`.

- **Implied undirected skeleton** `S_impl = { {t, v} : v ∈ B_t \ {t} }`.
- **True undirected skeleton** `S_true = { {u, v} : (u, v) ∈ E(G*) or (v, u) ∈ E(G*) }`.
- `skel_precision = |S_impl ∩ S_true| / |S_impl|` (NaN if `S_impl = ∅`).
- `skel_recall    = |S_impl ∩ S_true| / |S_true|` (NaN if `S_true = ∅`).
- `skel_f1` = harmonic mean.

**Two directional rules**, both reported:

- **Rule D1 (rule-as-edge)**: for each non-trivial target rule for `t` with body var `v`, emit a directed edge `v → t`. Compute directed P/R/F1 against `E(G*)`.
- **Rule D2 (conservative)**: same as D1, but only emit `v → t` when `v ∈ P_t ∪ A_t` (i.e. agree with reality on at least the *ordering*). This is more permissive about direction errors and quantifies "if the learner agrees structurally, does it get direction right?"

Naming: `skel_precision`, `skel_recall`, `skel_f1`, `dir_d1_precision/recall/f1`, `dir_d2_precision/recall/f1`.

### 3.8 Bridge metrics (RQ3 / E10)

For each `(dgp, n, seed, config, bridge_mode)` cell, where `bridge_mode ∈ {ci_only, ci_plus_hints}`:

- `shd` — Structural Hamming Distance between Ĝ and G\*.
- `dir_edge_precision`, `dir_edge_recall`, `dir_edge_f1`.
- `skel_precision`, `skel_recall`, `skel_f1` (treating Ĝ as undirected for skeleton check).
- `runtime_s_bridge` — wall clock of the Causal ABA call.

These are defined here for forward reference; their measurement code lives downstream of the Phase A investigation in E10.

---

## 4. Aggregation rules (cell → figure)

The analysis layer (`analysis.py`) aggregates rows from `results.parquet`. Conventions:

1. **Group keys** are explicit per figure (e.g. `groupby(["dgp", "n", "target"])`).
2. **Reduction across seeds** uses:
   - **Median + IQR (Q1, Q3)** for ratios in [0,1] (precision, recall, F1, coverage, rates).
   - **Median + IQR** for `wall_clock_s`, `n_delta_rules`, etc.
   - **Mean + SE** only when justified explicitly (rare).
3. **Fraction-solved** is computed at the same group level: `mean(outcome == "solved")`. Numeric metrics are conditioned on `outcome == "solved"` *unless* explicitly stated.
4. **CI bands** in plots: shaded IQR. Sample size `n_seeds` printed next to every bar/marker.
5. **Missing groups** (e.g. fraction_solved == 0) are drawn as ghost bars with a striped pattern (no claim attached).

---

## 5. Code shape — `causal/metrics.py`

This is the **only** place metrics are computed. No logging, no I/O except reading the `.bk.aba` / `.bk.sol.aba`. Pure-ish: same inputs → same outputs.

### 5.1 Public API

```python
# causal/metrics.py

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

VarSet = frozenset[str]

@dataclass(frozen=True)
class GroundTruth:
    nodes: tuple[str, ...]           # ("x0", "x1", "x2", ...)
    edges: frozenset[tuple[str, str]]  # directed edges (parent, child)

    def parents_of(self, t: str) -> VarSet: ...
    def ancestors_of(self, t: str) -> VarSet: ...

@dataclass(frozen=True)
class CellInputs:
    experiment_id: str
    dgp: str
    graph_type: str           # "discrete" | "continuous"
    target: str
    n: int
    seed: int
    config_hash: str
    run_id: str
    bk_path: Path
    sol_path: Path | None     # None if no solution
    pos_examples: tuple[str, ...]
    neg_examples: tuple[str, ...]
    ground_truth: GroundTruth
    wall_clock_s: float
    outcome: str              # see Section 2
    failure_reason: str | None
    folding_tokens_used: int

def compute_cell_metrics(inp: CellInputs) -> dict: ...
    # Returns the full metric panel (Section 3) as a flat dict.

def aggregate_implied_skeleton(
    cells: Sequence[dict],      # cells for one (dgp, n, seed, config)
    ground_truth: GroundTruth,
) -> dict: ...
    # Returns skel_precision/recall/f1, dir_d1_*, dir_d2_*.

def body_vars(literal: str) -> VarSet: ...
    # Public, testable. e.g. "x0_bin0(A)" -> {"x0"}.

def prolog_aware_coverage(
    sol_path: Path | None,
    bk_path: Path,
    pos_examples: Sequence[str],
    neg_examples: Sequence[str],
    timeout_s: float = 5.0,
) -> dict: ...
    # Returns cov_pl_* keys. Falls back to bk_path when sol_path is None.
```

### 5.2 Migration from current tests

The following helpers in `test_aba_learning.py` map to `metrics.py` as follows:

| Current helper | New home | Notes |
|----------------|----------|-------|
| `_extract_learned_rules` | `metrics.parse_delta_rules` | Pure; already returns a list. Move and add types. |
| `_correspondence_stats` | `metrics.body_level_stats` | Tighten variable stripping (use `body_vars`). |
| `_example_coverage_report` | `metrics.python_horn_coverage` | Remove logging; return dict. |
| `_summarize_target_rule_dependencies` | folded into `metrics.body_level_stats` | Returned as part of the dict. |
| `_summarize_target_rule_triviality` | `metrics.triviality_counts` | Same. |
| `_record_abaf_coverage` | `metrics.abaf_structure_counts` | Counts of `asm/ctr/alpha_mentions/c_alpha_mentions`. |
| (new) | `metrics.prolog_aware_coverage` | Implementation calls into Prolog via a new helper in `run_aba_asp.py` (or sibling). |

Tests for `metrics.py` live in `causal/tests/test_metrics.py` and **do not depend on Prolog** for the Python-Horn paths; the Prolog-aware path is tested in a separate module that requires SWI-Prolog.

### 5.3 What `metrics.py` must not do

- It must not log.
- It must not write files.
- It must not invoke the runner.
- It must not modify its inputs.

This keeps the metrics layer trivially memoisable and trivially testable.

---

## 6. Worked micro-example

For a confounder DGP `G3-fork` with `P_{x2} = {x0}`, `A_{x2} = {x0}`, suppose ABA-ASP returns one non-trivial target rule:

```
x2(A) :- x0_bin0(A).
```

- `body_vars("x0_bin0(A)")` = `{"x0"}`.
- `parent_hit` = 1 (because `{x0} ∩ {x0} = {x0}` ≠ ∅).
- `ancestor_only_hit` = 0.
- `offgraph_hit` = 0.

Per cell:

- `body_parent_precision` = 1/1 = 1.0.
- `body_parent_recall` = 1/1 = 1.0.
- `body_parent_f1` = 1.0.
- `offgraph_rate` = 0.0.
- `ancestor_only_rate` = 0.0.

Now suppose for `x0` we get instead:

```
x0(A) :- x1_bin0(A).
```

- `vars` = `{x1}`.
- For `x0`, `P_{x0} = ∅`, `A_{x0} = ∅` (it's a root).
- `parent_hit` = 0; `ancestor_only_hit` = 0; `offgraph_hit` = 1 (x1 is not an ancestor of x0; in fact x0 is its parent).
- `body_parent_precision` = 0/1 = 0.0.
- `body_parent_recall` = NaN (no parents to recall).
- `offgraph_rate` = 1.0.

This is exactly the "off-graph" pattern we have already seen in Phase 2 logs, and it is a real finding: ABA-ASP can find body→head dependencies that the **child → parent** direction would predict.

---

## 7. What to put in figures vs in `metrics.json`

`metrics.json` per cell is the **complete record**. Figures are reductions:

| Figure (per `REPORT_OUTLINE.md`) | Group keys | Primary metric | Secondary metric (annotation) |
|----------------------------------|------------|----------------|-------------------------------|
| F3 — Seed-stability boxplots | `dgp`, `target` | `body_parent_f1` | `fraction_solved` |
| F4 — n-scaling curves | `dgp`, `target`, `n` | `body_parent_f1` (median + IQR) | `fraction_solved` |
| F5 — Structural-sweep bars | `dgp`, `target` | `offgraph_rate`, `body_parent_f1` | `fraction_solved` |
| F6 — Implied-skeleton | `dgp`, `n` | `skel_f1`, `dir_d1_f1` | `skel_precision`, `skel_recall` |
| F7 — Bridge prelim | `dgp`, `bridge_mode` | `dir_edge_f1`, `shd` | `runtime_s_bridge` |

Tables T1 (ablations) display:

- T1a (binning E06): grid over `bins × strategy` → `body_parent_f1` (median, IQR, n_seeds, fraction_solved).
- T1b (learner E07): grid over `folding_steps × folding_mode`.

---

## 8. Validation & sanity checks

`metrics.py` ships with the following self-tests:

1. **Identity**: rerunning `compute_cell_metrics` on the same inputs yields byte-identical dicts (modulo float ordering).
2. **Range**: every ratio metric is in [0,1] ∪ {NaN}.
3. **Mass balance**: `parent_hit + ancestor_only_hit + offgraph_hit + (rules citing no graph vars at all) = #non-trivial target rules`. The last bucket is recorded as `degenerate_hit` (NaN-counted; rarely non-zero).
4. **Coverage sanity**: `cov_py_tp + cov_py_fn = |E+|` and `cov_py_tn + cov_py_fp = |E−|`. Same for Prolog-aware.
5. **No silent NaNs**: every NaN is matched by a recorded reason (e.g. `"no_nontrivial_rules"` or `"no_parents"`).

---

## 9. Open issues

These are flagged for the implementation step (Session C):

- **Q1**: should `body_vars` also strip continuous-target predicates we did *not* bin (currently we always bin)? **Default**: yes, for symmetry.
- **Q2**: do we include `c_alpha_*` bodies when computing body-vars? **Default**: no — they are not target rules.
- **Q3**: how do we expose Prolog-aware coverage's per-example results without bloating `metrics.json`? **Default**: store the totals only in `metrics.json`, but write a `coverage_detail.json` per cell if a `--verbose` flag is set.
- **Q4**: do we count assumption-laden δ-rules differently? **Default**: no — they are target rules and count, but we also record `n_assumptions` so the report can stratify.

Resolutions to these questions are appended to the Decisions log in `EXPERIMENTS_PLAN.md`.
