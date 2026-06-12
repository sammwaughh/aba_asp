# QI-003 decision record (QI003_scaled_motifs)

> QI-003 is a scaled, confound-controlled parent-set recovery investigation using the current ABA Learning bridge. It is not full Russo-style Causal ABA, graph recovery, d-separation reasoning, or stable-extension-as-DAG machinery.

## Status

`computational-feasibility attempt; superseded for evidence by QI-004 (n=20, prolog_timeout_s=300)`

The QI-003 `n=100` run (with `prolog_timeout_s=120`) repeatedly timed out (cat3/cont3 cells) or failed instantly on the binary all-zero-positive encoding limitation (binary cells); 0 cells solved before the run was manually aborted. See `run_log.md` for the partial outcome distribution. QI-003's config, fixtures, and partial outputs are preserved unchanged as a recorded feasibility attempt. The conceptually identical but computationally feasible follow-up is **QI-004** (`QI004_scaled_motifs_n20`): same design, `n=20`, `prolog_timeout_s=300`. See `docs/experiments/qualitative/QI004_scaled_motifs_n20/`.

## Purpose recap

Scaled noisy run with parent-position controls and enough samples for continuous/discretised data. QI-001's continuous/categorical behaviours may be artefacts of tiny `n`, sparse bins, or x0-position confounding. QI-003 tests whether behaviour persists with `n=100`, mild noise, populated bins, and the true parent placed in either column.

## Acceptance / rerun criteria

| Criterion | Pass | Rerun / investigate |
|---|---|---|
| Cells planned | 15 | any other count -> stop, config bug |
| Cells completed | 15 with artefacts (`metrics.json` + `bk.sol.aba`) | missing artefacts -> investigate pipeline |
| Outcome distribution | mostly `solved` | widespread `error` / `timeout` -> investigate before interpreting (note: larger n + noise may stress the learner) |
| Continuous bin-health | all 3 uniform bins non-empty for `x0`/`x1` in every `*_cont3` cell | empty/sparse bins -> flag; binning/n design issue |
| Confound check feasible | both `*_x0parent` and `*_x1parent` variants produced usable artefacts so the comparison can be made | one orientation missing -> rerun that cell |
| Determinism | re-running yields identical tables (fixed per-fixture RNG seed) | divergence -> builder seed bug |

## Decisions taken

- Run with the default learner config (nd folding, `folding_steps: 15`); no extra flags/seeds/targets.
- Determinism comes from each fixture's internal RNG seed (the `handcrafted_table` path ignores `cell.seed`); grid `seed: [0]`.
- Do not modify fixtures/config/metrics unless a clear bug is found (then stop and report).
- Interpretation deferred to Samuel/ChatGPT after raw outputs are reviewed; the x0parent-vs-x1parent comparison is the decision-critical confound check.
