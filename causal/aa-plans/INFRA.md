# Infrastructure Specification

**Read after:** [`meta-understanding-plan.md`](meta-understanding-plan.md) — **Phase 4** (runner and artefacts).

**Status:** living document. Last updated: 2026-05-24.
**Companion docs:** `EXPERIMENTS_PLAN.md`, `METRICS.md`.

This document specifies the execution layer that turns a YAML experiment config into a `results.parquet` table and a tree of per-cell artefacts. It covers the **runner**, the **config schema**, the **artefact layout**, the **results schema**, **determinism**, **failure handling**, **resumability**, and the **analysis layer** that turns rows into figures.

Anything in here that conflicts with an experiment spec (`experiments/E0X_*.md`) should be resolved here first.

---

## 1. Goals (and non-goals) of the infrastructure

**Goals:**

- One command runs an experiment end-to-end: `python -m causal.experiments.run_grid --config configs/experiments/E02_seed_robustness.yaml`.
- A run is **resumable**: cells with a complete `metrics.json` are skipped on rerun.
- A run is **reproducible**: same config + same code commit → same `results.parquet` (modulo Prolog wall-clock).
- Analysis is **disconnected** from execution: `analysis.py` consumes only `results.parquet` files and renders the report's figures.
- The whole stack runs **locally**, single core, in the `aba-env` conda environment.

**Non-goals:**

- No cluster / distributed execution.
- No remote storage; everything is on local disk.
- No automatic hyper-parameter search; configs are explicit.
- No fancy dashboard; the notebook + `analysis.py` are sufficient.

---

## 2. Directory layout

```
causal/
├── aa-plans/                       ← planning docs (this set)
├── configs/
│   └── experiments/
│       ├── E01_sanity.yaml
│       ├── E02_seed_robustness.yaml
│       ├── ...
│       └── E10_bridge.yaml
├── experiments/
│   ├── __init__.py
│   ├── run_grid.py                 ← entry point
│   ├── analysis.py                 ← figures/tables from results.parquet
│   ├── aba_learn_lab.ipynb         ← presentational notebook
│   ├── figures/                    ← versioned PNG/PDF output of analysis.py
│   └── tables/                     ← versioned CSV/TeX tables
├── metrics.py                      ← see METRICS.md §5
├── outputs/
│   └── aba_learning/
│       ├── <existing class dirs>/  ← legacy test artefacts (unchanged)
│       └── grid/
│           └── <experiment_id>/
│               ├── results.parquet         ← one row per cell
│               ├── manifest.json           ← config + code hash + start/end times
│               └── cells/
│                   └── <run_id>/
│                       ├── config.json
│                       ├── data.csv
│                       ├── data.binned.csv (if continuous)
│                       ├── bk.aba
│                       ├── bk.sol.aba       (if outcome=solved)
│                       ├── prolog.stdout    (full Prolog output)
│                       ├── prolog.stderr
│                       ├── metrics.json     ← single source of truth per cell
│                       └── coverage_detail.json  (if --verbose)
├── run_aba_asp.py                  ← existing
├── argcausaldisco_integration.py   ← existing
└── tests/
    ├── test_metrics.py              ← unit tests on metrics.py (no Prolog)
    ├── test_runner.py               ← smoke tests on run_grid.py
    └── test_prolog_coverage.py      ← Prolog-dependent (skipped if unavailable)
```

`outputs/aba_learning/<existing class dirs>/` (e.g. `TestMinimalContinuousData/`) are unchanged; the test suite continues to write there. The new grid runner writes only under `outputs/aba_learning/grid/`.

---

## 3. Config schema (YAML)

Configs are human-edited and live in `causal/configs/experiments/`. Each file describes one experiment. The schema is small and uniform across experiments.

### 3.1 Top-level keys

```yaml
experiment_id: E02_seed_robustness        # must match the filename stem
description: "30 seeds per cell across DGP zoo; locks RQ1 variance bars."
owner: sam
created: 2026-05-24

defaults:                                  # base config, then `grid` overrides per cell
  graph_type: continuous                   # discrete | continuous
  noise_type: gaussian                     # continuous only
  noise_scale: 1.0                          # continuous only
  bins: 2
  bin_strategy: quantile                   # quantile | uniform
  example_split: median                    # median | top_bottom_third | bin_specific
  folding_steps: 15
  folding_mode: nd                         # nd | greedy
  prolog_timeout_s: 120
  query_timeout_s: 5                       # per-example Prolog-aware coverage timeout
  verbose_coverage: false

dgps:                                      # list of DGPs to run; expanded against grid
  - id: G3-chain
    nodes: 3
    edges: [[0,1],[1,2]]
  - id: G3-fork
    nodes: 3
    edges: [[0,1],[0,2]]
  - id: G3-collider
    nodes: 3
    edges: [[0,2],[1,2]]
  - id: G4-forkchain
    nodes: 4
    edges: [[0,1],[0,2],[2,3]]
  - id: G4-hub
    nodes: 4
    edges: [[0,1],[0,2],[0,3]]

grid:                                      # Cartesian product fields
  n: [25]                                  # E02 fixes n=25; E03 sweeps it
  seed: { range: [0, 30] }                 # 30 seeds: 0..29
  target: all                              # or an explicit list, e.g. ["x2"]

derived:                                   # computed at load time, written to manifest
  total_cells: 5 * 1 * 30 * 3 = 450        # (commentary)

provenance:
  code_commit_required: true               # runner refuses dirty git unless --force
```

### 3.2 Resolution rules

- `defaults` apply to every cell.
- `grid` is the Cartesian product. `seed: { range: [a, b] }` expands to `range(a, b)`.
- `target: all` expands to `["x0", "x1", ..., "x_{nodes-1}"]` per DGP.
- DGP-specific overrides go in the `dgp` entry, e.g. `graph_type: discrete` for E01's discrete cases. (We will use one config per "kind" — discrete vs continuous — when needed, rather than mixing in one file.)

### 3.3 Validation

`run_grid.py` validates the config before running:

- Required keys present.
- `experiment_id` matches filename stem.
- All DGPs have unique IDs.
- Edges reference valid node indices in `range(nodes)`.
- `seeds` non-empty and non-overlapping.
- `bins ≥ 2`, `folding_steps ≥ 1`, timeouts positive.
- A **dry-run** mode (`--dry-run`) prints the full cell list and exits.

---

## 4. The runner — `experiments/run_grid.py`

### 4.1 CLI

```
python -m causal.experiments.run_grid \
    --config causal/configs/experiments/E02_seed_robustness.yaml \
    [--dry-run] \
    [--limit N]              # run at most N cells (for smoke tests)
    [--only-target x2]       # filter to a single target
    [--only-dgp G3-chain]    # filter to a single DGP
    [--force]                # bypass clean-git check
    [--no-resume]            # ignore existing metrics.json (re-run all cells)
    [--workers 1]            # default 1; ≥2 is optional and may break determinism guarantees
    [--log-level INFO]
```

### 4.2 Pseudocode

```python
def run_experiment(cfg_path: Path) -> None:
    cfg = load_and_validate(cfg_path)
    out_root = Path("causal/outputs/aba_learning/grid") / cfg.experiment_id
    manifest = open_manifest(out_root, cfg)
    cells = expand_cells(cfg)
    for cell in cells:
        run_dir = out_root / "cells" / cell.run_id
        if (run_dir / "metrics.json").exists() and not opts.no_resume:
            continue
        run_dir.mkdir(parents=True, exist_ok=True)
        try:
            artefacts = execute_cell(cell, run_dir)
            metrics = compute_cell_metrics(artefacts)
            write_json(run_dir / "metrics.json", metrics)
            append_row(out_root / "results.parquet", metrics)
        except TimeoutError:
            write_outcome(run_dir, outcome="timeout", reason=str(e))
        except Exception as e:
            write_outcome(run_dir, outcome="error", reason=repr(e))
    close_manifest(manifest)
```

### 4.3 `execute_cell` responsibilities

1. **Simulate** data with the right backend (`simulate_discrete_data` or `simulate_linear_continuous_data`) using `cell.seed`.
2. Write `data.csv` (and `data.binned.csv` if continuous).
3. Call `generate_aba_background_knowledge` with `cell.bins`, `cell.bin_strategy`, `exclude_cols=[cell.target]`. Write `bk.aba`.
4. Compute E+ / E− using `cell.example_split` (median for continuous; `pick_target_variable` for discrete).
5. Call `run_prolog_aba_asp` with `folding_steps`, `folding_mode`, `prolog_timeout_s`. Capture stdout/stderr verbatim.
6. Locate `bk.sol.aba` if produced; set `outcome` accordingly.
7. Build a `CellInputs` (see `METRICS.md §5.1`) and return it.

### 4.4 Determinism

- Numpy's `RandomState(seed)` is created per cell from `cell.seed`. The simulator is called with that seed.
- `bk.aba` ordering is deterministic given the same `df` and `var_types` (already true for `generate_aba_background_knowledge`; if not, fix in implementation).
- Prolog is single-threaded; the runner does **not** parallelise within a cell.
- Cross-cell parallelism (`--workers N>1`) is supported but voids reproducibility of per-cell wall-clock and may interleave outputs; turned off by default.

### 4.5 Resumability

- A cell is "done" iff `metrics.json` exists and parses.
- Re-running the same config skips done cells.
- `--no-resume` forces re-execution; `--force` is needed if the git tree is dirty.

### 4.6 Outcome handling

Mapping from raw signals to outcome category (see `METRICS.md §2`):

| Signal | Outcome |
|--------|---------|
| `bk.sol.aba` exists and parser returns ≥1 δ-rule | `solved` |
| `* No solution found!` in `prolog.stdout`, no `bk.sol.aba` | `completed_no_solution` |
| `bk.sol.aba` exists but parser returns 0 δ-rules | `completed_empty_delta` |
| Wall-clock exceeded `prolog_timeout_s` | `timeout` |
| Python exception (parsing, missing file, simulator) | `error` |
| Empty E+ or E− detected before Prolog call | `skipped` |

`failure_reason` captures a one-line summary in all cases except `solved`.

---

## 5. Results schema (`results.parquet`)

One row per cell. Columns are the union of fields in `METRICS.md §3` plus identification:

```
experiment_id          str
dgp                    str
graph_type             str
target                 str
n                      int
seed                   int
config_hash            str
run_id                 str

outcome                str
failure_reason         str (nullable)
wall_clock_s           float
folding_tokens_used    int

n_delta_rules          int
n_target_rules         int
n_assumptions          int
n_contraries           int
n_trivial_target_rules int
n_nontrivial_target_rules int
max_body_length        int
mean_body_length       float (nullable)

body_parent_precision  float (nullable)
body_parent_recall     float (nullable)
body_parent_f1         float (nullable)
offgraph_rate          float (nullable)
ancestor_only_rate     float (nullable)

cov_py_accuracy        float
cov_py_pos             float
cov_py_neg             float
cov_py_tp              int
cov_py_fp              int
cov_py_tn              int
cov_py_fn              int

cov_pl_accuracy        float
cov_pl_pos             float
cov_pl_neg             float
cov_pl_tp              int
cov_pl_fp              int
cov_pl_tn              int
cov_pl_fn              int

cov_gap_accuracy       float
cov_gap_pos            float
cov_gap_neg            float

# Implied-skeleton metrics — populated only on the "last target" cell of each (dgp,n,seed,config)
skel_precision         float (nullable)
skel_recall            float (nullable)
skel_f1                float (nullable)
dir_d1_precision       float (nullable)
dir_d1_recall          float (nullable)
dir_d1_f1              float (nullable)
dir_d2_precision       float (nullable)
dir_d2_recall          float (nullable)
dir_d2_f1              float (nullable)

# Bridge metrics — populated only for E10 cells
bridge_mode            str (nullable)
shd                    int (nullable)
dir_edge_precision     float (nullable)
dir_edge_recall        float (nullable)
dir_edge_f1            float (nullable)
runtime_s_bridge       float (nullable)
```

Storage: pyarrow Parquet, with column dtypes pinned in `analysis.py` to avoid `object` columns sneaking in.

Why Parquet over CSV: typed columns, fast in pandas, small on disk. Why over SQLite: no concurrent writers, no need for joins.

---

## 6. Manifest schema (`manifest.json`)

Per experiment:

```json
{
  "experiment_id": "E02_seed_robustness",
  "config_path": "causal/configs/experiments/E02_seed_robustness.yaml",
  "config_hash": "sha256:...",
  "code_commit": "abc1234",
  "code_dirty": false,
  "python": "3.11.x",
  "swipl": "9.x.x",
  "aba_asp_version": "<from run_aba_asp module>",
  "argcausaldisco_commit": "abc1234",
  "started_at": "2026-05-24T12:13:00+01:00",
  "finished_at": "2026-05-24T12:48:11+01:00",
  "n_cells_planned": 450,
  "n_cells_completed": 450,
  "n_cells_skipped": 0,
  "outcome_counts": {"solved": 312, "completed_no_solution": 130, ...},
  "host": "samuelwaugh.local"
}
```

This is the audit trail for the report.

---

## 7. Per-cell `metrics.json`

A flat JSON file with exactly the columns of the Parquet schema (Section 5). The Parquet table is a concatenation of these. We keep both because:

- `metrics.json` is human-readable and easy to inspect.
- `results.parquet` is what `analysis.py` loads.
- They are the **same data**, and the runner is responsible for keeping them in sync.

We also include in `metrics.json` (but not in Parquet) a small `context` block:

```json
{
  "context": {
    "ground_truth_edges": [["x0","x1"],["x1","x2"]],
    "parents": ["x0"],
    "ancestors": ["x0"],
    "delta_rules": ["x2(A) :- x0_bin0(A)."],
    "pos_examples": ["x2(1)", "x2(3)", ...],
    "neg_examples": ["x2(2)", ...]
  }
}
```

This makes cell-level debugging trivial without re-running.

---

## 8. Analysis layer — `experiments/analysis.py`

### 8.1 Responsibilities

- Load `results.parquet` for one or more experiments.
- Apply the aggregation rules in `METRICS.md §4`.
- Produce figures (`figures/F<i>_<slug>.{png,pdf}`) and tables (`tables/T<i>_<slug>.{csv,tex}`).
- **No execution**: it does not run Prolog, simulate data, or modify anything under `cells/`.

### 8.2 Public API

```python
# causal/experiments/analysis.py

import pandas as pd
from pathlib import Path

def load_results(experiment_ids: list[str]) -> pd.DataFrame: ...
def aggregate_seed_stability(df: pd.DataFrame) -> pd.DataFrame: ...
def aggregate_n_scaling(df: pd.DataFrame) -> pd.DataFrame: ...
def aggregate_structural(df: pd.DataFrame) -> pd.DataFrame: ...
def aggregate_skeleton(df: pd.DataFrame) -> pd.DataFrame: ...

def plot_seed_boxplots(agg, out_dir: Path) -> Path: ...    # F3
def plot_n_curves(agg, out_dir: Path) -> Path: ...          # F4
def plot_structural_bars(agg, out_dir: Path) -> Path: ...   # F5
def plot_skeleton(agg, out_dir: Path) -> Path: ...          # F6
def table_ablations(df, out_dir: Path) -> Path: ...         # T1a, T1b
```

### 8.3 Notebook

`aba_learn_lab.ipynb` is a thin presentational layer:

- Cell 1: imports + paths.
- Cell 2: `load_results([...])`.
- Cell 3 onward: call each `plot_*` / `table_*` in turn, display, save to `figures/` / `tables/`.

No analysis logic in the notebook itself. Everything is callable from the CLI as `python -m causal.experiments.analysis --experiment E02 --figure F3`.

---

## 9. Testing the infrastructure

### 9.1 `tests/test_metrics.py` (Prolog-free)

- Variable stripping (`body_vars`) on a battery of literal strings.
- Body-level stats on hand-crafted (G\*, δ-rule) pairs.
- Python-Horn coverage on a small toy with a known answer.
- Edge cases: empty δ-set, no parents, all-trivial rules.

### 9.2 `tests/test_prolog_coverage.py` (Prolog-dependent)

- Skip if `swipl` not on PATH.
- Run one cell of E01 end-to-end through `run_grid.py` in a temporary directory.
- Assert `metrics.json` keys match the Parquet schema.
- Assert Prolog-aware coverage on the known-good `cont_collider_8_x2` example equals 1.0 / 1.0.

### 9.3 `tests/test_runner.py`

- Dry run: assert correct cell count.
- Resume: run twice; assert second run does no Prolog work.
- Invalid config: assert validation error with helpful message.
- `--limit 1`: only one cell runs and is recorded.

---

## 10. Provenance and reproducibility

- **Code commit** recorded in `manifest.json`. Dirty trees are refused (unless `--force`).
- **Config hash** recorded in every row of `results.parquet` and in `metrics.json`.
- **SWI-Prolog version** captured.
- **ArgCausalDisco commit** captured (sibling repo).
- **Random seeds** are per-cell (not global). The same seed across reruns reproduces the same simulated dataset and therefore the same δ-rules, given the same code.

A reader of the report should be able to:

1. Clone the repo at the recorded commit.
2. `pip install -e .` and `conda activate aba-env`.
3. `python -m causal.experiments.run_grid --config causal/configs/experiments/E02_seed_robustness.yaml`.
4. `python -m causal.experiments.analysis --experiment E02 --figure F3`.

…and obtain the same figure. This is the contract.

---

## 11. Compute budget — back-of-envelope

Using observed wall-clock from current Phase 2/3 runs (~15 s/cell median, ~50 s/cell tail for `folding_steps=15`):

| Experiment | Cells | Median cost | Tail cost | Plan |
|------------|-------|-------------|-----------|------|
| E01 (sanity) | ~6 | 1.5 min | 5 min | trivial |
| E02 (30 seeds × 5 DGPs × 3 targets × 1 n) | 450 | ~2 h | ~6 h | one overnight run |
| E03 (30 seeds × 5 DGPs × 3 targets × 6 n) | 2700 | ~11 h | ~38 h | weekend run; consider capping `folding_steps` to 10 |
| E04 | merged with E02 (same data) | — | — | analysis only |
| E06 (binning, smaller grid) | ~360 | ~1.5 h | ~5 h | overnight |
| E07 (learner ablation) | ~480 | ~2 h | ~7 h | overnight |
| E09 | analysis pass over E02–E04 data | minutes | — | analysis only |
| E10 prelim | ~30 (1 DGP × 30 seeds, 2 modes) | depends on Causal ABA | — | TBD post Phase A |

The runner's resumability matters here: if a wave fails, we resume from the last completed cell.

---

## 12. Migration plan from the current test suite

The existing `test_aba_learning.py` continues to work and remains a useful **smoke test**. We do not remove it. The plan:

1. **Lift helpers** (`_extract_learned_rules`, `_correspondence_stats`, etc.) into `metrics.py`, keeping thin wrappers in the test file that delegate to `metrics.*` for logging output.
2. **Add `prolog_aware_coverage`** in `metrics.py` and use it from a new test in `tests/test_prolog_coverage.py`.
3. **Add `run_grid.py`** and a single `E01_sanity.yaml` config that reproduces the *content* of the existing handcrafted/Phase 2/Phase 3 tests as cells.
4. **Diff check**: the metric panel emitted by the runner for E01 cells matches (within tolerance) the diagnostics logged by the current tests.

Step 4 is the bridge: when it passes, we know the new infra is faithful to the old tests, and we can scale up.

---

## 13. Logging policy

- **Runner**: `INFO` for cell start/finish, `WARN` for outcome ≠ `solved`, `DEBUG` for verbose per-step diagnostics.
- **Metrics**: silent (see `METRICS.md §5.3`).
- **Tests**: keep current rich logging style — that is part of the report's case studies.
- Logs from a grid run are written to `outputs/aba_learning/grid/<experiment_id>/run.log`, rotated per invocation. They are **not** the source of truth — `metrics.json` is.

---

## 14. What is intentionally not in this spec

- Specific YAML files per experiment (live in `experiments/E0X_*.md` specs, written in Session B).
- Exact figure styles (palette, fonts, axes) — those are decided in `analysis.py` and `REPORT_OUTLINE.md`.
- Causal ABA call signatures (live in `experiments/E10_bridge_to_causal_aba.md` after Phase A investigation).

---

## 15. Sign-off checklist

The infra is "ready" when:

- [ ] `metrics.py` ships and `tests/test_metrics.py` passes.
- [ ] `tests/test_prolog_coverage.py` passes locally.
- [ ] `run_grid.py --config E01_sanity.yaml` writes a `results.parquet` and a tree of `metrics.json`.
- [ ] `analysis.py` renders at least one figure from that Parquet.
- [ ] `manifest.json` records the code commit, config hash, and outcome counts.
- [ ] A re-run of the same config performs zero Prolog calls.

When all six are ticked, P1 exit criterion (`EXPERIMENTS_PLAN.md §5`) is met and we proceed to P2 runs.
