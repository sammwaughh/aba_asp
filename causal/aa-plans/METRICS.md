# Metrics Specification

**Status:** describes the metric panel as currently implemented in `causal/metrics.py`.
**Companion doc:** `INFRA.md` (the runner and artefact layout).

This document defines how outcomes are measured. Every metric that appears in
`results.parquet` is defined here with a formula and an edge-case rule.
`metrics.py` is a single, side-effect-free module callable both from tests and
from the batch runner: same inputs → same outputs, no logging, no file writes
beyond reading `bk.aba` / `bk.sol.aba`.

---

## 1. Scope and units of analysis

The atomic **unit of analysis** is a single learning **cell**:

```
cell = (experiment_id, dgp, target, n, seed, config)
```

where `config` captures the knobs that vary across the grid (`folding_steps`,
`bins`, `bin_strategy`, `example_split`, `graph_type`, …). One cell produces:

- one BK file (`bk.aba`), one `data.csv` (and `data.binned.csv` if continuous),
- zero or one solution files (`bk.sol.aba` if Prolog found a solution),
- one `metrics.json` containing the **metric panel** below,
- one single-row `metrics.parquet` shard, later concatenated into
  `results.parquet`.

Aggregation is downstream of cells: the summary groups by `(dgp, target)` and
reduces over `seed`.

---

## 2. Outcome category (categorical)

Every cell takes exactly one of these values. "No solution found" is a real
result, not an error.

| Value | Meaning |
|-------|---------|
| `solved` | `bk.sol.aba` exists and `parse_delta_rules` returned ≥1 δ-rule. |
| `completed_empty_delta` | `bk.sol.aba` exists but 0 δ-rules were extracted. |
| `completed_no_solution` | Prolog printed `* No solution found!` and produced no `bk.sol.aba`. |
| `timeout` | The learning subprocess hit `prolog_timeout_s`. |
| `skipped` | Cell intentionally skipped (empty `E+` or `E-`). |
| `error` | Any other failure (parsing, crash, missing inputs). |

`failure_reason` is a one-line string whenever the outcome is not `solved`. The
mapping is implemented in `metrics.outcome_classifier`.

**Reporting rule:** for any cell-derived numeric metric, also report
**fraction_solved** = #cells with `outcome=solved` / #cells. Numeric metrics are
computed only over `solved` cells unless stated otherwise.

---

## 3. The metric panel (one per cell)

`compute_cell_metrics(inp: CellInputs) -> dict` returns the full panel. Numeric
metrics are `NaN` when not applicable, and each NaN is paired with a
`<metric>_nan_reason` key in `metrics.json`.

### 3.1 Identification

```
experiment_id, dgp, graph_type, target, n, seed, config_hash, run_id
```

### 3.2 Outcome

```
outcome             : str        # see Section 2
failure_reason      : str | None
wall_clock_s        : float      # seconds in the learning Prolog call
folding_tokens_used : int        # last "Increasing folding tokens to: K", else 0
```

### 3.3 δ-rule structure

```
n_delta_rules            : int    # all δ-rules (any head)
n_target_rules           : int    # δ-rules whose head matches the target
n_assumptions            : int    # alpha_*/N in the ABAF
n_contraries             : int    # c_alpha_*/N
n_trivial_target_rules   : int    # body head-equivalent (e.g. x2(A) :- x2(A).)
n_nontrivial_target_rules: int
max_body_length          : int    # over target rules
mean_body_length         : float  # over target rules (NaN if none)
```

Implemented by `triviality_counts`, `abaf_structure_counts`, and
`body_level_stats`.

### 3.4 Body-level metrics (RQ1)

Computed **over non-trivial target rules** by `body_level_stats`. These are the
main quantitative answer to RQ1.

Let, for target `t` in ground-truth graph G\*:
- `P_t` = true parents of `t`; `A_t` = true ancestors of `t` (parents and above).
- For a δ-rule `r`, `vars(r)` = base variable names cited in its body, after
  stripping suffixes (`metrics.body_vars`, §5): e.g. `x0_bin0(A)` → `{x0}`.

Per non-trivial target rule `r`:
- `parent_hit(r)` = 1 if `vars(r) ∩ P_t ≠ ∅`.
- `ancestor_only_hit(r)` = 1 if `vars(r) ∩ A_t ≠ ∅` and `vars(r) ∩ P_t = ∅`.
- `offgraph_hit(r)` = 1 if none of `vars(r)` lie in `A_t`.

Aggregated per cell:

| Metric | Formula | Range | Edge case |
|--------|---------|-------|-----------|
| `body_parent_precision` | Σ `parent_hit(r)` / #non-trivial target rules | [0,1] | NaN if no non-trivial target rules |
| `body_parent_recall` | \|{v ∈ P_t : ∃ r, v ∈ vars(r)}\| / \|P_t\| | [0,1] | NaN if `P_t = ∅` (root target) |
| `body_parent_f1` | harmonic mean of precision/recall | [0,1] | NaN if either is NaN |
| `offgraph_rate` | Σ `offgraph_hit(r)` / #non-trivial target rules | [0,1] | NaN if no non-trivial rules |
| `ancestor_only_rate` | Σ `ancestor_only_hit(r)` / #non-trivial target rules | [0,1] | same |

**Variable-stripping rule.** `body_vars(lit)` maps a body literal to base
variable names, stripping `_binK`, `_val_V`, `_gt_*`, `_lt_*`, and other
`_[a-z0-9]+` suffixes after a leading `x\d+` (anchored on the full digit run, so
`x10_bin0 → {x10}`, not `{x1}`).

**Direction note.** Body-parent precision treats a rule body as a *predictor
set*; it does not assert edge direction.

### 3.5 Coverage (Python-Horn and Prolog-aware)

Both definitions are reported, plus the gap between them (the gap reflects ABAF
assumption machinery that the plain Horn check ignores). Given `E+` and `E-`:

- **Python-Horn coverage** (`python_horn_coverage`): treats δ-rules as plain Horn
  clauses over the BK feature map and computes `TP/FP/TN/FN`, `accuracy`,
  `pos_coverage`, `neg_coverage`. Keys: `cov_py_accuracy`, `cov_py_pos`,
  `cov_py_neg`, `cov_py_tp/fp/tn/fn`.
- **Prolog-aware coverage** (`prolog_aware_coverage`): queries each example
  against `bk.sol.aba` (or `bk.aba` when there is no solution) through SWI-Prolog,
  respecting assumptions and contraries, time-boxed per query by `query_timeout_s`
  (default 5 s). Keys: `cov_pl_accuracy`, `cov_pl_pos`, `cov_pl_neg`,
  `cov_pl_tp/fp/tn/fn`.
- **Gap**: `cov_gap_accuracy/pos/neg = cov_pl_* − cov_py_*`.

When `outcome ≠ solved`, Python-Horn coverage is computed against an empty δ-set
(so `cov_py_pos = 0`, `cov_py_neg = 1` typically), and Prolog-aware coverage
queries `bk.aba`. Both remain meaningful and are recorded.

**Runner integration.** `query_timeout_s` (YAML `defaults`) flows through
`CellInputs` into `prolog_aware_coverage`. `prolog_timeout_s` caps the *learning*
subprocess only (`INFRA.md §4.4`). With `--skip-prolog-coverage`, the
Prolog-aware pass is skipped and all `cov_pl_*` / `cov_gap_*` are NaN with reason
`grid_skip_prolog_coverage`.

### 3.6 Parser sanity

```
parser_unread_lines : int   # lines in bk.sol.aba not classified by the parser
sol_file_bytes      : int   # size of bk.sol.aba if present, else 0
```

### 3.7 Reserved columns — NOT computed

`results.parquet` reserves columns for implied-skeleton and bridge-to-Causal-ABA
metrics, but **these are not implemented**: `compute_cell_metrics` fills them
with NaN/None placeholders (`metrics._placeholder_skeleton_and_bridge`). They are
kept so the schema stays stable if the metrics are added later. Always NaN/None:

```
skel_precision, skel_recall, skel_f1,
dir_d1_precision, dir_d1_recall, dir_d1_f1,
dir_d2_precision, dir_d2_recall, dir_d2_f1,
bridge_mode, shd, dir_edge_precision, dir_edge_recall, dir_edge_f1, runtime_s_bridge
```

Their NaN reasons are `implied_skeleton_not_aggregated` and `bridge_not_run`.

---

## 4. Aggregation (cell → summary)

`scripts/summarize_experiment.py` aggregates `results.parquet`:

1. **Group keys**: `(dgp, target)`.
2. **fraction_solved** = `mean(outcome == "solved")` per group.
3. **median body-F1** is conditioned on `outcome == "solved"`.
4. Targets are annotated as *root* (no true parents → no rule is the correct
   answer) or *has-parents*; timeouts are reported separately as search blow-ups.

The output is a markdown table and a two-panel heatmap (solve fraction; median
`body_parent_f1`) per experiment — see `INFRA.md §8`.

---

## 5. Code shape — `causal/metrics.py`

The implemented public surface:

```python
@dataclass(frozen=True)
class GroundTruth:
    nodes: tuple[str, ...]
    edges: frozenset[tuple[str, str]]      # directed (parent, child)
    def parents_of(self, t: str) -> frozenset[str]: ...
    def ancestors_of(self, t: str) -> frozenset[str]: ...

@dataclass(frozen=True)
class CellInputs:
    experiment_id, dgp, graph_type, target, n, seed, config_hash, run_id
    bk_path: Path
    sol_path: Path | None                  # None if no solution
    pos_examples: tuple[str, ...]
    neg_examples: tuple[str, ...]
    ground_truth: GroundTruth
    wall_clock_s: float
    outcome: str
    failure_reason: str | None
    folding_tokens_used: int
    query_timeout_s: float = 5.0           # per-example cap for prolog_aware_coverage
    skip_prolog_coverage: bool = False      # when True, cov_pl_* are placeholder NaN

def compute_cell_metrics(inp: CellInputs) -> dict: ...   # full panel (Section 3)

# building blocks
def body_vars(literal: str) -> frozenset[str]: ...        # "x0_bin0(A)" -> {"x0"}
def parse_delta_rules(sol_path: Path) -> list[str]: ...
def target_rule_filter(target, learned) -> list[str]: ...
def triviality_counts(target, learned) -> dict: ...
def abaf_structure_counts(learned) -> dict: ...
def parse_bk_feature_map(bk_path: Path) -> dict[int, frozenset[str]]: ...
def body_level_stats(target, learned, ground_truth) -> dict: ...
def python_horn_coverage(bk_path, learned, pos, neg, *, target) -> dict: ...
def prolog_aware_coverage(sol_path, bk_path, pos, neg, *, timeout_s=5.0) -> dict: ...
def outcome_classifier(stdout, sol_path, learned_rules, wall_clock_s, timeout_s, examples_ok) -> tuple[str, str|None]: ...
def parse_folding_tokens_used(stdout: str) -> int: ...
```

The Parquet column list and dtype pinning live in
`metrics.RESULT_PARQUET_COLUMNS` and `results.py` respectively.

### 5.1 What `metrics.py` must not do

- It must not log, write files, invoke the runner, or modify its inputs.

This keeps the metrics layer trivially testable; `test_metrics.py` exercises it
without Prolog.

---

## 6. Worked micro-example

For `G3-fork` with `P_{x2} = {x0}`, `A_{x2} = {x0}`, suppose ABA-ASP returns one
non-trivial target rule:

```
x2(A) :- x0_bin0(A).
```

- `body_vars("x0_bin0(A)")` = `{x0}`.
- `parent_hit` = 1, `ancestor_only_hit` = 0, `offgraph_hit` = 0.
- `body_parent_precision = 1.0`, `body_parent_recall = 1.0`, `body_parent_f1 = 1.0`,
  `offgraph_rate = 0.0`, `ancestor_only_rate = 0.0`.

Now suppose for the root `x0` we instead get `x0(A) :- x1_bin0(A).`:

- `vars = {x1}`; for `x0`, `P_{x0} = ∅`, `A_{x0} = ∅`.
- `parent_hit = 0`, `ancestor_only_hit = 0`, `offgraph_hit = 1`.
- `body_parent_precision = 0.0`, `body_parent_recall = NaN` (no parents to recall),
  `offgraph_rate = 1.0`.

This is the "off-graph" pattern: ABA-ASP can learn a `body → head` dependency
that corresponds to the *child → parent* direction of the true graph.

---

## 7. Validation & sanity checks

Enforced by `test_metrics.py` and the implementation:

1. **Range**: every ratio metric is in [0,1] ∪ {NaN}.
2. **Coverage balance**: `cov_py_tp + cov_py_fn = |E+|` and
   `cov_py_tn + cov_py_fp = |E−|` (same for the Prolog-aware totals).
3. **No silent NaNs**: every NaN float in `metrics.json` has a matching
   `<metric>_nan_reason` (e.g. `no_nontrivial_rules`, `no_parents`,
   `grid_skip_prolog_coverage`, `implied_skeleton_not_aggregated`).
