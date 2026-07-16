# Infrastructure Specification

**Status:** describes the infrastructure as currently implemented.
**Companion doc:** `METRICS.md` (the per-cell metric panel).

This document specifies the execution layer that turns a YAML experiment config
into a `results.parquet` table and a tree of per-cell artefacts. It covers the
**runner**, the **config schema**, the **artefact layout**, the **results
schema**, **determinism**, **failure handling**, **resumability**, and the
**summary layer** that turns rows into a report-ready table and figure.

The two experiments that currently ship are `E00_discrete_smoke` and
`E00_continuous_smoke`; they are used as the running examples below.

---

## 1. Goals (and non-goals)

**Goals:**

- One command runs an experiment end-to-end:
  `python -m causal.experiments.run_grid --config causal/configs/experiments/E00_discrete_smoke.yaml`.
- A run is **resumable**: cells with a complete `metrics.json` are skipped on rerun.
- A run is **reproducible**: same config + same code → same per-cell δ-rules and
  metrics (modulo Prolog wall-clock and outcome timing).
- Summarisation is **disconnected** from execution: `summarize_experiment.py`
  consumes only `results.parquet` and renders the report's table/figure.
- The whole stack runs **locally** in the `aba-env` conda environment, serially
  by default or across processes with `--workers N`.

**Non-goals:**

- No cluster / distributed execution; no remote storage.
- No automatic hyper-parameter search; configs are explicit.
- No dashboard; the summary script is sufficient.

---

## 2. Directory layout

**Path resolution note.** All paths below are **relative to the `aba_asp/` repo
root** (the directory that contains the `causal/` package). The runner resolves
the grid output root (see `causal/experiments/paths.py`) as:

```
<repo_root>/causal/outputs/aba_learning/grid/<experiment_id>/
```

```
causal/
├── aa-plans/
│   ├── INFRA.md                     ← this document
│   └── METRICS.md
├── configs/
│   └── experiments/
│       ├── E00_discrete_smoke.yaml
│       └── E00_continuous_smoke.yaml
├── experiments/
│   ├── __init__.py
│   ├── paths.py                     ← repo_root() / grid_root()
│   ├── config.py                    ← schema, load_config, expand_cells, hashing
│   ├── dgp.py                       ← DGP zoo + get_dgp
│   ├── handcrafted.py               ← handcrafted-table fixtures (load_handcrafted)
│   ├── manifest.py                  ← open_manifest / close_manifest
│   ├── results.py                   ← per-cell shards + results.parquet
│   ├── run_grid.py                  ← entry point (the runner)
│   └── figures/                     ← summary output (<experiment_id>_summary.{md,png})
├── scripts/
│   └── summarize_experiment.py      ← results.parquet → table + heatmaps
├── metrics.py                       ← see METRICS.md
├── run_aba_asp.py                   ← pre-existing SWI-Prolog wrapper
├── argcausaldisco_integration.py    ← pre-existing BK / example builders
├── outputs/
│   └── aba_learning/
│       ├── <existing class dirs>/   ← legacy test artefacts (unchanged)
│       └── grid/
│           └── <experiment_id>/
│               ├── results.parquet         ← one row per cell
│               ├── manifest.json           ← config + code hash + start/end times
│               ├── run.log                 ← per-invocation log
│               └── cells/
│                   └── <cell_dir_name>/   # hash run_id by default; dgp/slug if configured
│                       ├── data.csv
│                       ├── data.binned.csv        (continuous only)
│                       ├── bk.aba
│                       ├── bk.sol.aba             (if outcome=solved)
│                       ├── prolog.stdout
│                       ├── prolog.stderr
│                       ├── metrics.json           ← per-cell source of truth
│                       ├── metrics.parquet        ← single-row shard
│                       └── <ABA-ASP intermediates: asp.clingo, cc.pl, …>
└── tests/
    ├── test_config.py               ← config schema / validation
    ├── test_expand_cells.py         ← cell expansion + determinism
    ├── test_metrics.py              ← metrics.py (Prolog-free)
    ├── test_results.py              ← parquet dtypes / shard round-trip
    ├── test_prolog_query.py         ← Prolog-dependent (skips without swipl)
    ├── test_run_aba_timeout.py      ← subprocess timeout handling
    ├── test_runner_cli.py           ← CLI / lifecycle / resume / workers
    └── test_runner_stage1.py … stage4.py  ← per-stage runner tests
```

`outputs/aba_learning/<existing class dirs>/` are unchanged; the legacy test
suite continues to write there. The grid runner writes only under
`outputs/aba_learning/grid/`.

---

## 3. Config schema (YAML)

Configs are human-edited and live in `causal/configs/experiments/`. Each file
describes one experiment. The loader (`config.py:load_config`) validates the
file and `expand_cells` turns it into the cell list.

### 3.1 Top-level keys

```yaml
experiment_id: E00_discrete_smoke          # must match the filename stem
description: "Known-good regime smoke test: small discrete 3-node DGPs…"
owner: sam

defaults:                                  # base config for every cell
  graph_type: discrete                     # discrete | continuous | handcrafted_table
  noise_type: gaussian                     # continuous only (passed to the simulator)
  bins: 2                                   # quantile bins for continuous BK
  bin_strategy: quantile                   # quantile | uniform
  example_split: pick_target_variable      # pick_target_variable (discrete) | median (continuous)
  folding_steps: 10
  folding_mode: nd                         # nd | greedy
  prolog_timeout_s: 45                      # wall-clock cap on the learning subprocess
  query_timeout_s: 5                        # per-example cap for Prolog-aware coverage

dgps:                                      # list of DGPs; each is run for every grid point
  - id: G3-chain
    nodes: 3
    edges: [[0, 1], [1, 2]]
  - id: G3-fork
    nodes: 3
    edges: [[0, 1], [0, 2]]
  - id: G3-collider
    nodes: 3
    edges: [[0, 2], [1, 2]]

grid:                                      # Cartesian product fields
  n: [6]                                   # sample sizes
  seed: { range: [0, 4] }                  # expands to range(0, 4) → seeds 0,1,2,3
  target: all                              # "all" → x0..x_{nodes-1}, or an explicit list

provenance:
  code_commit_required: true               # recorded in the manifest (see §4.5)
```

### 3.2 Resolution rules (`expand_cells`)

- `defaults` apply to every cell; a DGP entry may override `graph_type`,
  `example_split`, `n`, or `targets` for itself.
- The cell list is the Cartesian product `dgps × n × seeds × targets`.
- `grid.seed` is **optional**. Omit it for deterministic / no-seed experiments
  (e.g. handcrafted tables): expansion uses a single cell with `seed=None`.
  When present, `seed: { range: [a, b] }` expands to `range(a, b)`, or use an
  explicit non-empty list. An empty `seed: []` is rejected — omit the key instead.
- Stochastic `discrete` / `continuous` cells require a real seed at run time
  (stage 1 errors if `seed` is `None`).
- `target: all` expands to `["x0", …, "x_{nodes-1}"]` per DGP.
- For `graph_type: handcrafted_table`, the DGP entry carries a `source` naming a
  fixture in `handcrafted.py`, and `example_split` is forced to `handcrafted`.
- Each cell gets a `run_id` = first 12 hex chars of the SHA-1 of
  `experiment_id|dgp|nodes|edges|n|seed|target|graph_type|config_hash`
  (`seed` token is `none` when `grid.seed` was omitted). This is stored in
  `metrics.json` / `results.parquet` and is stable across reruns.
- Optional `grid.cell_dir` controls the filesystem directory name under
  `cells/` (default `hash`):
  - `hash` — `cell_dir_name == run_id` (legacy behaviour; safe for large grids).
  - `dgp` — `cell_dir_name == dgp.id` (e.g. `m11_binary_A`; one cell per DGP).
  - `slug` — `{dgp}__target-{target}__seed-{seed}` when a seed is present;
    `{dgp}__target-{target}` when `grid.seed` was omitted.
- `expand_cells` rejects configs where two cells share the same `cell_dir_name`.
- Resume (`cell_is_done`): a cell is skipped only when `metrics.json` parses and
  its stored `config_hash` matches the current config. This keeps `dgp`/`slug`
  directory names valid when the YAML changes.

### 3.3 Validation

`load_config` rejects a config that:

- is missing required keys, or whose `experiment_id` ≠ filename stem;
- has duplicate DGP ids, or edges referencing nodes outside `range(nodes)`;
- has a non-positive `n`, an empty seed list when `grid.seed` is present, or a
  target out of range.

`--dry-run` loads + expands the config, prints the planned cell count, and exits.

---

## 4. The runner — `experiments/run_grid.py`

### 4.1 CLI

```
python -m causal.experiments.run_grid \
    --config causal/configs/experiments/E00_discrete_smoke.yaml \
    [--dry-run]              # print planned cell count and exit
    [--limit N]              # run at most N cells (smoke tests)
    [--only-target x2]       # filter to a single target
    [--only-dgp G3-chain]    # filter to a single DGP
    [--no-resume]            # ignore existing metrics.json (re-run all cells)
    [--workers N]            # default 1 (serial); N>1 runs cells in separate processes
    [--skip-prolog-coverage] # skip the second SWI-Prolog pass (cov_pl_*/cov_gap_* → NaN)
    [--force]                # reserved; currently a no-op
    [--log-level INFO]
```

### 4.2 Control flow (`run_experiment`)

```python
cfg   = load_config(config_path)
cells = expand_cells(cfg, config_path=config_path)
cells = filter_cells(cells, only_target=…, only_dgp=…)
if dry_run: print(f"{len(cells)} cells planned"); return

open_manifest(out_root, cfg=cfg, …)         # writes manifest.json
for cell in cells[:limit]:
    run_dir = out_root / "cells" / cell.cell_dir_name
    if cell_is_done(run_dir, config_hash=cell.config_hash) and not no_resume:
        skip
    else:
        _run_single_cell(cell, run_dir, …)        # serial, or via ProcessPoolExecutor when workers>1
write_results_parquet(out_root)             # concat all per-cell shards
close_manifest(out_root, outcome_counts=…)
```

`_run_single_cell` wraps `execute_cell` and converts a `TimeoutError` into a
`timeout` outcome shard and any other exception into an `error` shard, so every
attempted cell ends with a written `metrics.json`.

### 4.3 `execute_cell` — four stages

`execute_cell` chains four stages (each independently tested):

1. **Stage 1 — simulate** (`execute_cell_stage1`): draw data with the backend for
   `cell.graph_type` (`simulate_discrete_data` or
   `simulate_linear_continuous_data`) at `cell.seed`; write `data.csv`. For
   `handcrafted_table`, load the fixture table instead.
2. **Stage 2 — encode** (`execute_cell_stage2`): build `E+/E-` with the cell's
   `example_split`, then `generate_aba_background_knowledge(..., exclude_cols=[target])`
   → `bk.aba` (+ `data.binned.csv` for continuous). If `E+` or `E-` is empty, the
   cell short-circuits to `skipped`.
3. **Stage 3 — learn** (`execute_cell_stage3`): run ABA-ASP via
   `ABASPRunner.run_prolog_aba_asp(..., timeout_s=prolog_timeout_s)`, capture
   stdout/stderr, relocate any solution file into the cell directory, extract
   δ-rules, and classify the `outcome` (`metrics.outcome_classifier`).
4. **Stage 4 — score** (`execute_cell_stage4`): assemble a `CellInputs`
   (see `METRICS.md`), call `compute_cell_metrics`, and write `metrics.json` +
   `metrics.parquet`.

### 4.4 Determinism and parallelism

- A `numpy.random.RandomState(cell.seed)` is constructed per cell and the
  simulator is called with `random_seed=cell.seed`.
- `bk.aba` ordering is deterministic given the same dataframe and var-types.
- Prolog is single-threaded; the runner does **not** parallelise within a cell.
- Cross-cell parallelism (`--workers N>1`) uses a `spawn` `ProcessPoolExecutor`.
  Each cell writes only under `cells/<cell_dir_name>/`; solution files that ABA-ASP may
  emit under the shared repo root are relocated into the cell directory after
  learning to avoid worker races. Per-cell wall-clock order and log interleaving
  are not deterministic when `N>1`.
- `run_prolog_aba_asp` honours the YAML `prolog_timeout_s` (subprocess wall
  clock); on expiry it kills the process and raises `TimeoutError`.
- `--skip-prolog-coverage` omits the coverage-query Prolog pass; `cov_pl_*` and
  `cov_gap_*` become NaN with reason `grid_skip_prolog_coverage`.

### 4.5 Resumability and provenance

- A cell is "done" iff `metrics.json` exists and parses; reruns skip done cells.
- `--no-resume` forces re-execution.
- The config may set `provenance.code_commit_required: true`. The runner records
  `code_commit` and `code_dirty` in the manifest but does **not** currently abort
  on a dirty tree; `--force` is parsed but is a no-op.

**Manifest caveat.** Each invocation rewrites `manifest.json`. A resume-only
re-run (0 executed cells) records `n_cells_completed=0` for that invocation even
though `cells/` is fully populated; the per-cell `metrics.json` files (and
`results.parquet`) remain the source of truth.

### 4.6 Outcome handling

`metrics.outcome_classifier` maps raw signals to one category (see
`METRICS.md §2`):

| Signal | Outcome |
|--------|---------|
| `bk.sol.aba` exists and ≥1 extracted δ-rule | `solved` |
| `bk.sol.aba` exists but 0 δ-rules | `completed_empty_delta` |
| `* No solution found!` in `prolog.stdout`, no `bk.sol.aba` | `completed_no_solution` |
| Wall-clock ≥ `prolog_timeout_s` | `timeout` |
| Empty `E+` or `E-` detected before the Prolog call | `skipped` |
| Any Python exception (parsing, missing file, simulator) | `error` |

`failure_reason` carries a one-line summary whenever the outcome is not `solved`.

---

## 5. Results schema (`results.parquet`)

One row per cell, written by concatenating the per-cell `metrics.parquet` shards
(`results.py:write_results_parquet`). The authoritative column list is
`metrics.RESULT_PARQUET_COLUMNS`; dtypes are pinned in
`results.py:enforce_results_dtypes` (no `object` columns).

```
# identification
experiment_id, dgp, graph_type, target, n, seed, config_hash, run_id

# outcome
outcome, failure_reason, wall_clock_s, folding_tokens_used

# δ-rule structure
n_delta_rules, n_target_rules, n_assumptions, n_contraries,
n_trivial_target_rules, n_nontrivial_target_rules,
max_body_length, mean_body_length

# body-level (RQ1)
body_parent_precision, body_parent_recall, body_parent_f1,
offgraph_rate, ancestor_only_rate

# Python-Horn coverage
cov_py_accuracy, cov_py_pos, cov_py_neg, cov_py_tp, cov_py_fp, cov_py_tn, cov_py_fn

# Prolog-aware coverage
cov_pl_accuracy, cov_pl_pos, cov_pl_neg, cov_pl_tp, cov_pl_fp, cov_pl_tn, cov_pl_fn

# coverage gap (Prolog-aware − Python-Horn)
cov_gap_accuracy, cov_gap_pos, cov_gap_neg

# ASP answer-set coverage (brave entailment on bk.sol.asp)
cov_asp_accuracy, cov_asp_pos, cov_asp_neg, cov_asp_tp, cov_asp_fp, cov_asp_tn, cov_asp_fn,
cov_asp_n_pos, cov_asp_n_neg

# parser sanity
parser_unread_lines, sol_file_bytes

# RESERVED placeholder columns — present in the schema but NOT computed;
# always NaN/None (see METRICS.md §3.7). Kept so the schema is stable if/when
# implied-skeleton and bridge metrics are added.
skel_precision, skel_recall, skel_f1,
dir_d1_precision, dir_d1_recall, dir_d1_f1,
dir_d2_precision, dir_d2_recall, dir_d2_f1,
bridge_mode, shd, dir_edge_precision, dir_edge_recall, dir_edge_f1, runtime_s_bridge
```

**Range note.** `cov_gap_* = cov_pl_* − cov_py_*`, so each gap lies in **[-1, 1]**.

Why Parquet: typed columns, fast in pandas, small on disk, no concurrent-writer
problems (each cell writes its own shard; the runner concatenates at the end).

---

## 6. Manifest schema (`manifest.json`)

One per experiment (`manifest.py`), rewritten on each invocation:

```json
{
  "experiment_id": "E00_discrete_smoke",
  "config_path": "…/E00_discrete_smoke.yaml",
  "config_hash": "sha256:…",
  "code_commit": "42c7234…",
  "code_dirty": true,
  "python": "3.10.20",
  "swipl": "SWI-Prolog version 10.0.2 …",
  "aba_asp_version": null,
  "argcausaldisco_commit": null,
  "started_at": "2026-06-01T18:02:56+00:00",
  "finished_at": "2026-06-01T18:05:51+00:00",
  "n_cells_planned": 36,
  "n_cells_completed": 36,
  "n_cells_skipped": 0,
  "outcome_counts": {"solved": 27, "completed_no_solution": 7, "error": 1, "timeout": 1},
  "host": "…", "platform": "…", "pid": 84561,
  "config_defaults": { … },
  "dgps": [ … ]
}
```

This is the audit trail for the report.

---

## 7. Per-cell `metrics.json`

A flat JSON document containing every column of the Parquet schema (§5), with
NaN floats serialised as `null`, plus `*_nan_reason` keys explaining each NaN
(e.g. `body_parent_recall_nan_reason: "no_parents"`). `write_cell_metrics` can
optionally embed a `context` block, but the runner does not currently populate
one. `metrics.json` and the single-row `metrics.parquet` shard are the same data
in two forms; `results.parquet` is their concatenation.

---

## 8. Summary layer — `scripts/summarize_experiment.py`

The summariser is the only post-processing step and is fully disconnected from
execution (it never runs Prolog or touches `cells/`).

```
python -m causal.scripts.summarize_experiment --experiment E00_discrete_smoke
```

It loads `grid/<experiment_id>/results.parquet`, annotates each `(dgp, target)`
with whether the target truly has parents (via `dgp.get_dgp`), and writes:

- `causal/experiments/figures/<experiment_id>_summary.md` — a per-`(dgp, target)`
  table: true parents, role (root vs has-parents), solved/seeds, median body-F1
  on solved cells, timeouts, median wall-clock.
- `causal/experiments/figures/<experiment_id>_summary.png` — two heatmaps
  (solve fraction; median `body_parent_f1`), with root targets annotated.

The interpretive convention: a **root** target (no parents) *should* yield no
rule (correct rejection); a target *with* parents should be solved with a rule
body recovering the true parents (`body_parent_f1 → 1.0`); timeouts are search
blow-ups, reported separately.

---

## 9. Testing the infrastructure

All suites live in `causal/tests/` and pass under `aba-env`:

- `test_config.py` — schema validation, `experiment_id`/filename match, DGP zoo.
- `test_expand_cells.py` — cell counts, run-id/config-hash determinism, manifest.
- `test_metrics.py` — `metrics.py` on hand-built rule sets (Prolog-free).
- `test_results.py` — Parquet dtype pinning and shard round-trips.
- `test_runner_stage1.py … stage4.py` — each `execute_cell` stage in isolation.
- `test_runner_cli.py` — dry-run counts, `--limit`, resume (zero re-execution),
  timeout/error shards, `--workers`, `--skip-prolog-coverage`.
- `test_prolog_query.py`, `test_run_aba_timeout.py` — Prolog-dependent paths
  (skip when `swipl` is unavailable).

---

## 10. Reproducibility contract

`manifest.json` records the code commit, config hash, SWI-Prolog version, and
outcome counts; every `results.parquet` row carries the `config_hash`. Random
seeds are per-cell, so the same seed reproduces the same simulated dataset and
δ-rules given the same code. A reader of the report can therefore:

1. Check out the repo at the recorded commit and `conda activate aba-env`.
2. `python -m causal.experiments.run_grid --config causal/configs/experiments/E00_discrete_smoke.yaml`.
3. `python -m causal.scripts.summarize_experiment --experiment E00_discrete_smoke`.

…and obtain the same table and figure (modulo Prolog wall-clock). The runner's
resumability means a re-run skips completed cells.

---

## 11. Logging policy

- **Runner**: `INFO` for cell start/finish, `WARN` for any outcome ≠ `solved`.
  Logs for a run go to `outputs/aba_learning/grid/<experiment_id>/run.log` and to
  the console.
- **`metrics.py`**: silent (no logging, no I/O beyond reading `bk.aba` / `bk.sol.aba`).
- **`run_aba_asp` / `argcausaldisco_integration`**: log at `INFO` and may print
  the full SWI-Prolog learning trace. `--log-level` on `run_grid` does not silence
  those loggers, so expect noisy consoles under `--workers N>1`. Prefer `run.log`
  and per-cell `prolog.stdout` for inspection.
- Logs are **not** the source of truth — `metrics.json` is.
