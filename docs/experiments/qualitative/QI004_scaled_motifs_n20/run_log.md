# QI-004 run log (QI004_scaled_motifs_n20)

> QI-004 is the feasible (`n=20`, `prolog_timeout_s=300`) follow-up to QI-003: a scaled, confound-controlled parent-set recovery investigation using the current `aba_asp/causal` implementation (target-wise ABA Learning pipeline). It is not full Russo-style Causal ABA, graph recovery, d-separation reasoning, or stable-extension-as-DAG machinery.

QI-004 exists because the QI-003 `n=100` run was computationally infeasible under the available Prolog timeout budget. Same conceptual design; `n` reduced to 20, Prolog timeout raised to 300s.

## Environment / provenance

- Date: 2026-06-12.
- Conda environment: `aba-asp`.
- Python: `3.10.20`.
- SWI-Prolog: `10.0.2 for fat-darwin`.
- clingo: `5.8.0`.
- Code commit (from manifest): `0468207b8a9295f6ec1a3a0acba6f227acab43fd`; working tree dirty (`code_dirty: true`) — expected, the new QI-004 fixtures/config/tests/docs are uncommitted.
- Platform: `macOS-26.5.1-arm64`; host `Samuels-MacBook-Pro-2.local`.

## Run configuration (audit)

| Field | Value |
|---|---|
| Config path | `causal/configs/experiments/QI004_scaled_motifs_n20.yaml` |
| Experiment id | `QI004_scaled_motifs_n20` |
| Cells planned | 15 |
| Cells completed (with `metrics.json`) | 15 |
| Sample size (n) | 20 per cell |
| Prolog timeout | 300 s per cell (`prolog_timeout_s`); query timeout 5 s |
| Data modes | binary 0/1, categorical-3, continuous (3 uniform bins) |
| Motifs / structural variants | chain (`x0parent`, `x1parent`), fork (`x0parent`, `x1parent`), collider — 5 configs × 3 modes |
| Target variable | `x2` only (excluded from BK) |
| Seed(s) | grid `seed: [0]`; tables deterministic via per-fixture internal RNG (`_BASE_SEED=20040002`) |
| Bin count / strategy | `bins: 3`, `bin_strategy: uniform` |
| Folding mode / budget | `folding_mode: nd`, `folding_steps: 15` |
| Output directory | `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20/` |
| Aggregated artefacts | `results.parquet`, `manifest.json` (both present) |
| Generated summary | `docs/experiments/qualitative/QI004_scaled_motifs_n20_summary.md` |
| Every completed cell has `metrics.json` | yes (15/15) |
| Every completed cell has a solution file (`bk.sol.aba`) | no — only the 1 `solved` cell (`d97c1b0c8c7c`); the other 14 produced none (expected for no-solution/error) |
| Timeouts | 0 |
| No-solutions (`completed_no_solution`) | 12 |
| Parser/metric failures (`error`, binary `unknown constant`) | 2 |
| Empty deltas | the 12 no-solution + 2 error cells have `n_delta_rules=0`; the solved cell has 5 |
| Missing artefacts | none |

## Pre-flight commands

| Command | Status | Output |
|---|---|---|
| `python -m pytest causal/tests/test_qi002_fixtures.py causal/tests/test_qi003_fixtures.py causal/tests/test_qi004_fixtures.py causal/tests/test_motif_recovery_summary.py causal/tests/test_metrics.py causal/tests/test_results.py -q` | 302 passed, 2 failed | the 2 failures are `test_motif_recovery_summary.py::test_build_summary_qi002_pending` and `::test_build_summary_qi003_parent_position_from_edges`; both assert a clean (`n_with == 0`) output tree, but QI-002 (6 cells) and QI-003 (14 cells, preserved partial run) have artefacts on disk. Same clean-tree fragility as the known QI-001 failure; unrelated to QI-004 code. All `test_qi004_fixtures.py` tests pass. |
| `python -c "import pandas, numpy, yaml, pyarrow; print('py-env OK')"` | OK | `py-env OK` |
| `swipl --version` | OK | `SWI-Prolog version 10.0.2 for fat-darwin` |
| `clingo --version` | OK | `clingo version 5.8.0` |
| `python -m causal.experiments.run_grid --config causal/configs/experiments/QI004_scaled_motifs_n20.yaml --dry-run` | OK | `15 cells planned for QI004_scaled_motifs_n20` |

Note: the first draft of `test_qi004_fixtures.py` had one failure (`test_chain_parent_not_collinear_with_ancestor[qi004_chain_x0parent_binary]`) because, at `n=20`, the original base seed (`20040000`) produced zero noise-flips so the chain intermediate equalled its root (a degenerate collinear chain). Fixed by setting `_BASE_SEED = 20040002`, which keeps all binary/cat3 chains at >= 0.15 parent-vs-ancestor disagreement. No engine or test-logic change.

## ABA Learning run

- Initial command: `python -m causal.experiments.run_grid --config causal/configs/experiments/QI004_scaled_motifs_n20.yaml --no-resume`.
  - This session completed 7 cells with valid `metrics.json` (1 `solved`, 5 `completed_no_solution`, 1 `error`) and was processing the 8th when the controlling shell's wall-clock window elapsed and the harness ended the job. This was an external interruption, NOT a per-cell timeout: the per-cell Prolog timeout was 300s and no cell hit it. The 8th cell (`afa56c4e22f6`) had no `metrics.json` at that point.
- Completion command (resume): `python -m causal.experiments.run_grid --config causal/configs/experiments/QI004_scaled_motifs_n20.yaml`.
  - Resume skips cells with a valid `metrics.json` (`cell_is_done`); it re-ran the incomplete 8th cell + the 7 not-yet-started cells. Final log line: `done: completed=8 skipped=7 outcomes={'completed_no_solution': 7, 'error': 1}` (this is the resume session's view; skipped=7 are the cells finished in the first session).
- Result: all 15 cells produced a valid `metrics.json`. Aggregate outcome distribution over all 15 cells:

| Outcome | Count |
|---|---|
| `completed_no_solution` | 12 |
| `error` (binary `unknown constant`) | 2 |
| `solved` | 1 |
| `timeout` | 0 |

- No timeouts at `n=20` (max per-cell wall-clock `272.8s` for `qi004_collider_cat3`, under the 300s budget). This is the headline feasibility result relative to QI-003's `n=100` timeouts.
- The 2 `error` cells are both binary (`qi004_fork_x0parent_binary`, `qi004_collider_binary`); each failed in ~0.1s with `ERROR: unknown constant: <id>` in `prolog.stdout`, confirming the known all-zero-positive binary encoding limitation (recorded, not fixed).

## Summary generation

- Command: `python causal/scripts/motif_recovery_summary.py --experiment QI004_scaled_motifs_n20`.
- Output: `wrote .../QI004_scaled_motifs_n20_summary.md`; `15 cells: 0 pending, 15 with artefacts`.

## Raw per-cell status table

| # | source (cell) | run_id | outcome | metrics.json | sol file (`bk.sol.aba`) | Δrules | n_nontriv_x2 | n_assum | clean_rec | varP | varR | varJ | wall_s | bin-health | failure_reason |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `qi004_chain_x0parent_binary` | `545c94e295e2` | completed_no_solution | yes | no | 0 | 0 | 0 | 0 | — | 0.00 | 0.00 | 25.5 | — | Prolog reported no solution |
| 2 | `qi004_chain_x0parent_cat3` | `949bebb31b93` | completed_no_solution | yes | no | 0 | 0 | 0 | 0 | — | 0.00 | 0.00 | 89.8 | — | Prolog reported no solution |
| 3 | `qi004_chain_x0parent_cont3` | `b0eba6936c1c` | completed_no_solution | yes | no | 0 | 0 | 0 | 0 | — | 0.00 | 0.00 | 86.4 | all 3 bins (min 3) | Prolog reported no solution |
| 4 | `qi004_chain_x1parent_binary` | `d97c1b0c8c7c` | **solved** | yes | **yes** (26 lines) | 5 | 2 | 1 | 0 | 0.50 | 1.00 | 0.50 | 0.8 | — | — |
| 5 | `qi004_chain_x1parent_cat3` | `02db3ecc32e7` | completed_no_solution | yes | no | 0 | 0 | 0 | 0 | — | 0.00 | 0.00 | 196.8 | — | Prolog reported no solution |
| 6 | `qi004_chain_x1parent_cont3` | `907c13b72728` | completed_no_solution | yes | no | 0 | 0 | 0 | 0 | — | 0.00 | 0.00 | 87.5 | all 3 bins (min 3) | Prolog reported no solution |
| 7 | `qi004_fork_x0parent_binary` | `853b906f8559` | error | yes | no | 0 | 0 | 0 | 0 | — | 0.00 | 0.00 | 0.1 | — | `unknown constant` (binary all-zero-positive limitation) |
| 8 | `qi004_fork_x0parent_cat3` | `afa56c4e22f6` | completed_no_solution | yes | no | 0 | 0 | 0 | 0 | — | 0.00 | 0.00 | 161.6 | — | Prolog reported no solution |
| 9 | `qi004_fork_x0parent_cont3` | `db3c4aeedc1a` | completed_no_solution | yes | no | 0 | 0 | 0 | 0 | — | 0.00 | 0.00 | 68.9 | all 3 bins (min 5) | Prolog reported no solution |
| 10 | `qi004_fork_x1parent_binary` | `50407b0ed3b6` | completed_no_solution | yes | no | 0 | 0 | 0 | 0 | — | 0.00 | 0.00 | 24.8 | — | Prolog reported no solution |
| 11 | `qi004_fork_x1parent_cat3` | `539fc7c15c42` | completed_no_solution | yes | no | 0 | 0 | 0 | 0 | — | 0.00 | 0.00 | 51.8 | — | Prolog reported no solution |
| 12 | `qi004_fork_x1parent_cont3` | `4807c2e15eb8` | completed_no_solution | yes | no | 0 | 0 | 0 | 0 | — | 0.00 | 0.00 | 67.2 | all 3 bins (min 4) | Prolog reported no solution |
| 13 | `qi004_collider_binary` | `c3f09aa40a7d` | error | yes | no | 0 | 0 | 0 | 0 | — | 0.00 | 0.00 | 0.1 | — | `unknown constant` (binary all-zero-positive limitation) |
| 14 | `qi004_collider_cat3` | `47e4cdaac0eb` | completed_no_solution | yes | no | 0 | 0 | 0 | 0 | — | 0.00 | 0.00 | 272.8 | — | Prolog reported no solution |
| 15 | `qi004_collider_cont3` | `8d7a241463e1` | completed_no_solution | yes | no | 0 | 0 | 0 | 0 | — | 0.00 | 0.00 | 99.2 | all 3 bins (min 4) | Prolog reported no solution |

Factual notes (no interpretation):
- 15/15 cells have `metrics.json`; only the single `solved` cell (`d97c1b0c8c7c`) wrote a `bk.sol.aba`.
- `clean_recovery = 0` for every cell, including the solved one (its 2 non-trivial `x2` rules cite `x1` with `var_parent_recall = 1.00` but `var_parent_precision = 0.50`, i.e. an extra non-parent variable is also cited).
- All 5 `*_cont3` cells have all 3 uniform bins non-empty for both `x0` and `x1`.
- No timeouts.

Cells planned: 15. Cells with artefacts: 15.

## Output paths

- Run output directory: `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20/`
- Per-cell directories: `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20/cells/<run_id>/`
- Generated summary: `docs/experiments/qualitative/QI004_scaled_motifs_n20_summary.md`

## Note on the test suite

The full `causal/tests/` suite has one known, unrelated failure (`test_qi001_summary.py::test_build_summary_pending_contains_all_cells`) that assumes a clean QI-001 output tree; QI-001 was already run. It is unrelated to QI-002/QI-003/QI-004. Only the affected suites are run for this task.
