# QI-001 run log (QI001_motifs_modes)

> QI-001 is a qualitative parent-set recovery investigation using the current ABA Learning bridge. It is not full Russo-style Causal ABA, graph recovery, d-separation reasoning, or stable-extension-as-DAG machinery.

Factual log of commands run for QI-001. The ABALearn/grid run is pending. See `README.md` for context and `artefacts.md` for the artefact map.

## Environment / provenance

- Date authored: 2026-06-12
- Branch: `sam`
- Commit: `0468207`
- Working tree: dirty at authoring time (Stage 1 fixtures/config/tests and the summary script were not yet committed).
- Conda environment: `aba-asp`
- SWI-Prolog / clingo: not invoked (Stage 1 + summary are Prolog-free).

## Commands run (Stage 1 + summary setup)

All Prolog-free; no ABALearn.

| Command | Status | Output |
|---|---|---|
| `python -m pytest causal/tests/test_config.py causal/tests/test_expand_cells.py causal/tests/test_metrics.py causal/tests/test_results.py -q` | pass | `49 passed` |
| `python -m pytest causal/tests/test_qi001_fixtures.py -q` | pass | `83 passed` |
| `python -m causal.experiments.run_grid --config causal/configs/experiments/QI001_motifs_modes.yaml --dry-run` | pass | `9 cells planned for QI001_motifs_modes` |
| `python causal/scripts/qi001_qualitative_summary.py --experiment QI001_motifs_modes` | pass | `9 cells: 9 pending, 0 with artefacts` |
| `python -m pytest causal/tests/test_qi001_summary.py -q` | pass | `9 passed` |

A combined Prolog-free run of the fixture + summary + config/expand/metrics/results suites reported `141 passed`.

## First ABALearn run (completed)

- Date/time: 2026-06-12 07:47 (UTC+1)
- Branch: `sam`
- Commit: `0468207` (tree dirty; run artefacts and doc updates uncommitted)
- Tooling: SWI-Prolog 10.0.2 for fat-darwin; clingo 5.8.0; conda env `aba-asp`.

Pre-flight (all pass):

| Command | Status | Output |
|---|---|---|
| `python -m pytest causal/tests/test_qi001_fixtures.py causal/tests/test_qi001_summary.py causal/tests/test_config.py causal/tests/test_expand_cells.py causal/tests/test_metrics.py causal/tests/test_results.py -q` | pass | `141 passed` |
| `python -c "import pandas, numpy, yaml, pyarrow; print('py-env OK')"` | pass | `py-env OK` |
| `swipl --version` | pass | `SWI-Prolog version 10.0.2 for fat-darwin` |
| `clingo --version` | pass | `clingo version 5.8.0` |

Run + summary:

| Command | Status | Output |
|---|---|---|
| `python -m causal.experiments.run_grid --config causal/configs/experiments/QI001_motifs_modes.yaml --no-resume` | pass | `done: completed=9 skipped=0 outcomes={'solved': 9}` |
| `python causal/scripts/qi001_qualitative_summary.py --experiment QI001_motifs_modes` | pass | `9 cells: 0 pending, 9 with artefacts` |

High-level factual status: 9/9 cells `solved`; all cells have `metrics.json` and `bk.sol.aba`. No timeouts, no errors, no `completed_no_solution`, no empty deltas. Interpretation is pending review (see `interpretation.md`).

## Output paths

- Run output directory: `causal/outputs/aba_learning/grid/QI001_motifs_modes/`
- Per-cell directories: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/<run_id>/`
- Generated summary: `docs/experiments/qualitative/QI-001_summary.md`

Per-cell run ids:

| Cell | run_id |
|---|---|
| `qi001_chain_binary` | `de68cb1d975d` |
| `qi001_fork_binary` | `451489acc4f2` |
| `qi001_collider_binary` | `7f5f3debd5c5` |
| `qi001_chain_cat3` | `5b4dd6ff5d85` |
| `qi001_fork_cat3` | `f489167a07fe` |
| `qi001_collider_cat3` | `86a25857d983` |
| `qi001_chain_cont3` | `f6734b41b746` |
| `qi001_fork_cont3` | `e72376c9b2d9` |
| `qi001_collider_cont3` | `d8586dce641b` |
