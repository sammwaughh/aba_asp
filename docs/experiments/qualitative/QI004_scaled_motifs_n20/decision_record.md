# QI-004 decision record (QI004_scaled_motifs_n20)

> QI-004 is the feasible (`n=20`, `prolog_timeout_s=300`) follow-up to QI-003: a scaled, confound-controlled parent-set recovery investigation using the current `aba_asp/causal` implementation (target-wise ABA Learning pipeline). It is not full Russo-style Causal ABA, graph recovery, d-separation reasoning, or stable-extension-as-DAG machinery.

## Status

`raw output available; interpretation pending` (interpretation itself stays in `interpretation.md`).

Run completed 2026-06-12: 15/15 cells produced `metrics.json` with **no timeouts** (the QI-003 feasibility problem is resolved at `n=20`). Aggregate outcomes: 1 `solved`, 12 `completed_no_solution`, 2 `error` (binary `unknown constant` encoding limitation). `clean_recovery = 0` for all cells. The acceptance criterion "mostly `solved`" was NOT met; per the decision record this is recorded and interpretation is deferred (no blind reruns). Continuous bin-health passed (all 3 bins non-empty in every `*_cont3` cell). See `run_log.md` for the full per-cell table.

## Why QI-004 exists

QI-004 supersedes the QI-003 `n=100` run for evidence purposes. QI-003 was computationally infeasible under the 120s timeout budget (cat3/cont3 timed out; binary hit the all-zero-positive encoding limitation; 0 solved before manual abort). QI-004 keeps the identical conceptual design but reduces `n` to 20 and raises the Prolog timeout to 300s. QI-003 is preserved unchanged as a recorded feasibility attempt; see the record `../QI-003.md` and the partial outputs `causal/outputs/aba_learning/grid/QI003_scaled_motifs/`.

## Purpose recap

Scaled noisy run with parent-position controls and enough samples for continuous/discretised data. QI-001's continuous/categorical behaviours may be artefacts of tiny `n`, sparse bins, or x0-position confounding. QI-004 tests whether behaviour persists with `n=20`, mild noise, populated bins, and the true parent placed in either column.

## Acceptance / rerun criteria

| Criterion | Pass | Rerun / investigate |
|---|---|---|
| Cells planned | 15 | any other count -> stop, config bug |
| Cells completed | 15 with artefacts (`metrics.json` + `bk.sol.aba`) | missing artefacts -> investigate pipeline |
| Outcome distribution | mostly `solved` | widespread `error` / `timeout` -> record and stop, do not loop |
| Continuous bin-health | all 3 uniform bins non-empty for `x0`/`x1` in every `*_cont3` cell | empty/sparse bins -> flag; binning/n design issue |
| Confound check feasible | both `*_x0parent` and `*_x1parent` variants produced usable artefacts so the comparison can be made | one orientation missing -> rerun that cell |
| Determinism | re-running yields identical tables (fixed per-fixture RNG seed) | divergence -> builder seed bug |
| Binary encoding limitation | recorded per cell where it occurs (`unknown constant`) | do NOT fix the engine in this line of runs |

## Post-interpretation decision (2026-06-12)

- **Is QI-004 canonical evidence for the qualitative investigation?** Yes for the **scaled/noisy feasibility** role (it completes 15/15 cells, no timeouts, and is interpretable), superseding QI-003 for that role. **No** for being the canonical *parent-recovery* evidence: its substantive recovery finding is null (`clean_recovery=0` for all 15 cells), so the canonical recovery evidence remains QI-001 (encoding/motif sensitivity) and QI-002 (best-case learnability, clean_recovery 0.5). QI-004's positive contribution is (a) showing the pipeline runs the scaled/noisy design within budget at `n=20`, and (b) showing that at `n=20` the design recovers nothing clean.
- **Is a further rerun needed?** Not as a blind repeat. The acceptance criterion "mostly solved" was not met (1 solved, 12 no-solution, 2 error), but this is a recorded substantive result, not a pipeline malfunction; per the decision rules we record and stop rather than loop. A *redesigned* follow-up (not a rerun) could be considered later — e.g. an intermediate `n`, more positive examples, or addressing the binary all-zero-positive encoding limitation — but that is a new experiment decision for Samuel, not part of QI-004.
- **Why / why not.** Reruns at the same `n=20`/seed are deterministic and would reproduce these outcomes. Larger `n` re-enters the QI-003 feasibility wall. So neither a same-config rerun nor a naive scale-up is warranted without a design change.
- **How should QI-004 be used in the interim report?** As the scaled/noisy data point in the qualitative sequence: report that the pipeline becomes tractable at `n=20` but recovers no clean parent set, that continuous cells now complete (resolving QI-003's timeout gap) yet still recover nothing, that the only learned rule is an ancestor-contaminated superset, and that the x0 confound therefore remains empirically unbroken. Pair with QI-001/QI-002 for the recovery story and QI-003 for the feasibility note.
- **What remains unresolved.** (i) The x0/first-column confound is still not empirically decided (too few solved cells). (ii) Why categorical/continuous cells return `completed_no_solution` at `n=20` (n vs noise vs learner/encoding interaction) is not separable from this run. (iii) The binary all-zero-positive encoding limitation is still open (recorded, not fixed). (iv) Per-cell hand interpretation beyond the summary-derived synthesis is optional and not done.

## Decisions taken

- Run with the default learner config (nd folding, `folding_steps: 15`); only the two feasibility settings (`n=20`, `prolog_timeout_s=300`) differ from QI-003.
- Determinism comes from each fixture's internal RNG seed (the `handcrafted_table` path ignores `cell.seed`); grid `seed: [0]`.
- Do not modify fixtures/config/metrics unless a clear bug is found (then stop and report).
- Do not modify the upstream Prolog/ASP ABALearn engine. The binary all-zero-positive limitation is recorded, not fixed.
- Interpretation deferred to Samuel/ChatGPT after raw outputs are reviewed; the x0parent-vs-x1parent comparison is the decision-critical confound check.
