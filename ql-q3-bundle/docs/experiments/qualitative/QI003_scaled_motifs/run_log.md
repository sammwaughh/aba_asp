# QI-003 run log (QI003_scaled_motifs)

> QI-003 is a scaled, confound-controlled parent-set recovery investigation using the current ABA Learning bridge. It is not full Russo-style Causal ABA, graph recovery, d-separation reasoning, or stable-extension-as-DAG machinery.

> STATUS (2026-06-12): the QI-003 `n=100` run is a recorded **computational-feasibility attempt**. It repeatedly timed out and is NOT currently canonical evidence for qualitative interpretation. It has been superseded for evidence by **QI-004** (`QI004_scaled_motifs_n20`, `n=20`, `prolog_timeout_s=300`). The QI-003 config, fixtures, and partial outputs are preserved unchanged. See `docs/experiments/qualitative/QI004_scaled_motifs_n20/`.

## First ABA Learning run attempt (n=100) — timed out

- Date: 2026-06-12.
- Config: `causal/configs/experiments/QI003_scaled_motifs.yaml` (n=100 via `handcrafted_qi003.py`, `prolog_timeout_s=120`).
- Command: `python -m causal.experiments.run_grid --config causal/configs/experiments/QI003_scaled_motifs.yaml --no-resume`.
- Outcome: the run was manually aborted after ~17 minutes; 14 of 15 cells had finished, 1 had not. Partial outcome distribution over the 13 cells with `metrics.json` at abort time:

| Outcome | Count | Cells |
|---|---|---|
| `timeout` (Prolog exceeded `timeout_s=120.0`) | 8 | all cat3 + cont3 cells that ran (chain/fork x0parent/x1parent cat3+cont3) |
| `error` (`no solution file and no recognized completion signal`) | 5 | all binary cells that ran (chain/fork x0parent/x1parent binary, collider binary) |
| `solved` | 0 | — |

- Two distinct failure modes (factual, not interpreted):
  - cat3/cont3 cells hit the 120s Prolog timeout (`wall_clock_s ≈ 120.0`);
  - binary cells failed instantly (`wall_clock_s ≈ 0.05`) with `ERROR: unknown constant: <id>` from `check_ep_consts_aux` in `aba_asp.pl`. The binary "positive-cases-only" BK encoding does not declare a sample-id constant for an all-zero-feature row (`x0=0, x1=0`); QI-003's target noise can flip such a row to a positive example, whose constant is then undeclared. Recorded as a known encoding limitation (decision: do not fix in this line of runs).
- Output directory (preserved, not deleted): `causal/outputs/aba_learning/grid/QI003_scaled_motifs/`.
- No QI-003 summary regeneration was performed for this partial run.

## Note on the test suite

The full `causal/tests/` suite has one known, unrelated failure (`test_qi001_summary.py::test_build_summary_pending_contains_all_cells`) that assumes a clean QI-001 output tree; QI-001 was already run. It is unrelated to QI-002/QI-003/QI-004. Only the affected suites are run for these tasks.

## Original plan (pre-run, n=100)

Factual log of commands. The ABA Learning / grid run is pending.

## Environment / provenance

- Conda environment: `aba-asp`
- SWI-Prolog / clingo: not invoked yet (fixtures/config/summary are Prolog-free).

## Commands run (implemented stage; Prolog-free)

| Command | Status | Output |
|---|---|---|
| `python -m pytest causal/tests/test_qi003_fixtures.py -q` | TBD | TBD |
| `python -m causal.experiments.run_grid --config causal/configs/experiments/QI003_scaled_motifs.yaml --dry-run` | TBD | expect `15 cells planned` |
| `python causal/scripts/motif_recovery_summary.py --experiment QI003_scaled_motifs` | TBD | expect `15 cells: 15 pending, 0 with artefacts` |

(Statuses filled by the validation step; see the implementation report.)

## First ABA Learning run

- Status: pending.
- Command (not yet run): `python -m causal.experiments.run_grid --config causal/configs/experiments/QI003_scaled_motifs.yaml --no-resume`

## Output paths

- Run output directory: `causal/outputs/aba_learning/grid/QI003_scaled_motifs/`
- Per-cell directories: `causal/outputs/aba_learning/grid/QI003_scaled_motifs/cells/<run_id>/`
- Generated summary: `docs/experiments/qualitative/QI003_scaled_motifs_summary.md`
