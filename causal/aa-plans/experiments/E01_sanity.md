# E01 — Sanity (case studies)

**Status:** spec, ready for implementation after `metrics.py` and `run_grid.py` are in place.
**Companion docs:** `EXPERIMENTS_PLAN.md`, `METRICS.md`, `INFRA.md`, `REPORT_OUTLINE.md` (F2).
**Role in the plan:** P1 exit smoke test **and** the source of Figure F2 in the report.

---

## 1. Question

When the new `run_grid.py` infrastructure is pointed at the *same* DGPs we already studied in `test_aba_learning.py`, does it (a) finish, (b) emit the full metric panel from `METRICS.md`, and (c) reproduce the qualitative findings already in the test logs?

This is the **smallest meaningful experiment**: it doubles as the smoke test of the runner *and* as the source of the report's case-study figure (F2).

---

## 2. Hypothesis

For each of the cells listed below, the metric panel will reproduce the diagnostics currently printed by the corresponding test in `test_aba_learning.py`, namely:

| Cell | Expected outcome | Expected δ-rule(s) | Predicted body-parent F1 |
|------|------------------|---------------------|--------------------------|
| Handcrafted `simple_4`, target `x2` | `solved` | `x2(A) :- x0(A).` | 1.0 |
| Handcrafted `exception_5`, target `x2` | `solved` | rule + ≥1 assumption (alpha/c_alpha) | NaN or 1.0 depending on whether the assumption-laden rule counts in `body_vars` |
| Discrete chain (n=6), target `x1` | `solved` | value-specific `x1_val_*` rules | mid (cites x0) |
| Discrete chain (n=8), target `x2` | `solved` | ancestor-cite (x0) rules | ancestor-only |
| Discrete confounder (n=6), targets x0/x1/x2 | mix of `solved` and `completed_no_solution` | bin/value-specific bodies | mixed |
| Discrete collider (n=8), targets x0/x1/x2 | mostly `solved` | one-parent bodies | partial parent-recall |
| Continuous chain (n=8), target `x2`, bins=2 | `solved` | one rule citing `x0_bin*` | 1.0 |
| Continuous confounder (n=6), target `x2` | **`completed_no_solution`** | none | NaN; **fraction_solved metric will be the headline result** |
| Continuous collider (n=8), target `x2` | `solved` | `x2(A) :- x0_bin0(A).` | 1.0 |

The "expected" column is grounded in what we have already observed running these tests; it is the falsifiable prediction against which the runner is checked.

---

## 3. DGPs included

A **superset** of the current zoo, because E01 also serves as the bridge between the legacy `test_aba_learning.py` tests and the new grid runner. Five distinct DGPs in 8 cell families:

- **Handcrafted (discrete)**:
  - `H-simple-4` — the 4-row handcrafted table from `TestSimpleHandcraftedLearning`.
  - `H-exception-5` — the 5-row handcrafted table from `TestAssumptionIntroduction`.
- **Discrete simulated**:
  - `G3-chain` (n=6).
  - `G3-fork` (n=6).
  - `G3-collider` (n=8).
- **Continuous simulated** (quantile bins, median E+/E−):
  - `G3-chain` (n=8).
  - `G3-fork` (n=6).
  - `G3-collider` (n=8).

The handcrafted DGPs are *not* in the DGP zoo of `EXPERIMENTS_PLAN.md §7` (which is purely simulated). E01 admits them as **case studies only**, never used downstream of E01.

---

## 4. Factors varied (the grid)

E01 is **deliberately not a sweep**. Per DGP we sweep:

- **target** ∈ all variables of the DGP (1 for handcrafted, 3 for simulated).

Everything else is fixed.

---

## 5. Factors held fixed

| Factor | Value |
|--------|-------|
| seed | `42` (matches current tests) |
| n | as specified per DGP above |
| bins | 2 |
| bin_strategy | quantile |
| example_split | median (continuous); `pick_target_variable` (discrete) |
| folding_steps | 15 |
| folding_mode | nd |
| prolog_timeout_s | 120 |

---

## 6. Seeds

**1 seed (`42`)** per cell. Variance is *not* what we are measuring here; reproduction is.

---

## 7. Metrics & outputs

### Per-cell metrics

Full metric panel from `METRICS.md §3`. For E01 the headline subset is:

- `outcome`, `failure_reason`
- `n_delta_rules`, `n_target_rules`, `n_assumptions`, `n_contraries`
- `body_parent_precision`, `body_parent_recall`, `body_parent_f1`, `offgraph_rate`, `ancestor_only_rate`
- `cov_py_*`, `cov_pl_*`, `cov_gap_*`

### Figures and tables

- **F2 — case-study panel** (one mini-card per cell): graph diagram, δ-rule listing, parent/ancestor highlight, outcome label, fraction of E+ / E− covered.
- **F-meth-1 — BK + δ mini-example** for §4 of the report: drawn from `H-simple-4`.

No new tables (the per-cell metric values for E01 are inlined in F2's captions).

### Diff-check (Step 4 of the migration plan)

A `tests/test_e01_diff_check.py` script confirms that the panel emitted by E01 matches the diagnostics printed by the corresponding tests in `test_aba_learning.py`. Tolerance:

- Counts (`n_delta_rules`, `n_target_rules`, `n_assumptions`, `n_contraries`): **exact**.
- `body_parent_*` / `offgraph_rate` / `ancestor_only_rate`: **exact**.
- `cov_py_*`: **exact**.
- `cov_pl_*`: not in the legacy tests, so just sanity-checked as in [0,1].
- `wall_clock_s`: ignored.

A failure of the diff-check is a P1 blocker.

---

## 8. Configuration stub

`causal/configs/experiments/E01_sanity.yaml`:

```yaml
experiment_id: E01_sanity
description: "Reproduce handcrafted + Phase 2/3 case studies under the new runner."
owner: sam

defaults:
  bins: 2
  bin_strategy: quantile
  folding_steps: 15
  folding_mode: nd
  prolog_timeout_s: 120

# Per-DGP entries override graph_type, example_split, and n as needed.
dgps:
  - { id: H-simple-4,         graph_type: handcrafted_table, source: tests.simple_4,         n: 4 }
  - { id: H-exception-5,      graph_type: handcrafted_table, source: tests.exception_5,     n: 5 }
  - { id: G3-chain-disc,      graph_type: discrete,   edges: [[0,1],[1,2]],          n: 6, example_split: pick_target_variable }
  - { id: G3-fork-disc,       graph_type: discrete,   edges: [[0,1],[0,2]],          n: 6, example_split: pick_target_variable }
  - { id: G3-collider-disc,   graph_type: discrete,   edges: [[0,2],[1,2]],          n: 8, example_split: pick_target_variable }
  - { id: G3-chain-cont,      graph_type: continuous, edges: [[0,1],[1,2]],          n: 8, example_split: median }
  - { id: G3-fork-cont,       graph_type: continuous, edges: [[0,1],[0,2]],          n: 6, example_split: median }
  - { id: G3-collider-cont,   graph_type: continuous, edges: [[0,2],[1,2]],          n: 8, example_split: median }

grid:
  seed: [42]
  target: all

provenance:
  code_commit_required: true
```

The `handcrafted_table` graph type is implemented as a small loader inside `run_grid.py` that reads the same fixtures used by the legacy tests.

---

## 9. Estimated cost

| Component | Cells | Median per cell | Total median |
|-----------|------:|----------------:|-------------:|
| Handcrafted (1 target each) | 2 | 5 s | 10 s |
| Discrete simulated (3 targets each, 3 DGPs) | 9 | 10 s | 90 s |
| Continuous simulated (3 targets each, 3 DGPs) | 9 | 30 s | 270 s |
| **Total** | **20** | — | **~6 min** |

Tail: the continuous confounder x2 cell may take up to 60 s and return `completed_no_solution`. This is fine; we record and move on.

---

## 10. Pass / learn criteria

E01 passes if **all** of the following hold:

- [ ] Every cell produces a `metrics.json` and a row in `results.parquet`.
- [ ] The diff-check (Section 7) passes for every cell.
- [ ] F2 renders end-to-end from `results.parquet` via `analysis.py`.
- [ ] At least one cell is in each outcome bucket actually populated by the cases above (`solved`, `completed_no_solution`).
- [ ] Re-running the same config performs zero Prolog calls.

If any item fails, the runner or `metrics.py` is patched and E01 is re-run before anything else proceeds.

---

## 11. Connection to other experiments

- **Feeds:** F2 (report §5.1); also serves as the running example in §4 of the report.
- **Depends on:** `metrics.py` and `run_grid.py` complete (P1).
- **Blocks:** every other experiment. No E02–E10 run begins before E01 is green.
- **Reuses data from:** the legacy test suite indirectly (same seeds, same simulator calls).

---

## 12. Risks & contingencies

| # | Risk | Mitigation |
|---|------|------------|
| R-E01-1 | Diff-check fails because `body_vars` is stricter than the legacy `_correspondence_stats` prefix match. | Verbose mode prints both stats side-by-side; the legacy helper is migrated rather than re-derived, so the answer should match. |
| R-E01-2 | The Prolog-aware coverage helper is slow/flaky on the assumption-heavy `exception_5` cell. | Per-query timeout (5 s) is recorded; cell is still emitted with the timeout flag. |
| R-E01-3 | Handcrafted-table loader diverges from the test fixture. | The loader is a thin wrapper over the test fixture itself; a unit test guards the contract. |

---

## 13. Open questions

- Should E01 also cover `TestFoldingModes` cases? *Default: no — folding-mode coverage lives in E07.*
- Should we emit the `coverage_detail.json` for every E01 cell so the case-study figure can be regenerated without re-running Prolog? *Default: yes; E01 always runs `--verbose-coverage`.*
- Should `H-exception-5` count as `solved` even though it produces assumption-laden rules? *Default: yes (the outcome is `solved`); the assumption count is reported separately and is the more interesting datum.*

Resolutions append to the Decisions log in `EXPERIMENTS_PLAN.md`.
