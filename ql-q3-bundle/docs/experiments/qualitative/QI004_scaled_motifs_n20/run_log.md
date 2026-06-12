# QI-004 run log (QI004_scaled_motifs_n20)

> QI-004 is the feasible (`n=20`, `prolog_timeout_s=300`) follow-up to QI-003: a scaled, confound-controlled parent-set recovery investigation using the current ABA Learning bridge. It is not full Russo-style Causal ABA, graph recovery, d-separation reasoning, or stable-extension-as-DAG machinery.

QI-004 exists because the QI-003 `n=100` run was computationally infeasible under the available Prolog timeout budget. Same conceptual design; `n` reduced to 20, Prolog timeout raised to 300s.

## Environment / provenance

- Conda environment: `aba-asp`
- (Versions, branch, commit, dirty-tree state filled by the post-run audit.)

## Pre-flight commands

| Command | Status | Output |
|---|---|---|
| `python -m pytest causal/tests/test_qi002_fixtures.py causal/tests/test_qi003_fixtures.py causal/tests/test_qi004_fixtures.py causal/tests/test_motif_recovery_summary.py causal/tests/test_metrics.py causal/tests/test_results.py -q` | TBD | TBD |
| `python -c "import pandas, numpy, yaml, pyarrow; print('py-env OK')"` | TBD | TBD |
| `swipl --version` | TBD | TBD |
| `clingo --version` | TBD | TBD |
| `python -m causal.experiments.run_grid --config causal/configs/experiments/QI004_scaled_motifs_n20.yaml --dry-run` | TBD | expect `15 cells planned` |

## ABA Learning run

- Command: `python -m causal.experiments.run_grid --config causal/configs/experiments/QI004_scaled_motifs_n20.yaml --no-resume`
- Status: TBD (filled by the post-run audit).
- Outcome distribution: TBD.

## Summary generation

- Command: `python causal/scripts/motif_recovery_summary.py --experiment QI004_scaled_motifs_n20`
- Status: TBD.

## Output paths

- Run output directory: `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20/`
- Per-cell directories: `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20/cells/<run_id>/`
- Generated summary: `docs/experiments/qualitative/QI004_scaled_motifs_n20_summary.md`

## Note on the test suite

The full `causal/tests/` suite has one known, unrelated failure (`test_qi001_summary.py::test_build_summary_pending_contains_all_cells`) that assumes a clean QI-001 output tree; QI-001 was already run. It is unrelated to QI-002/QI-003/QI-004. Only the affected suites are run for this task.
