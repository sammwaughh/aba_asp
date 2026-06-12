# QI-002 decision record (QI002_minimal_motifs)

> QI-002 is a minimal-baseline parent-set recovery investigation using the current ABA Learning bridge. It is not full Russo-style Causal ABA, graph recovery, d-separation reasoning, or stable-extension-as-DAG machinery.

## Status

`pre-run before this task`

(Updated to `raw output available; interpretation pending` after the first ABA Learning run; interpretation itself stays in `interpretation.md`.)

## Purpose recap

Principled minimal truth-table baseline following QI-001. QI-001 used tiny, unjustified handcrafted motif tables (4-5 rows) and revealed a possible x0/first-column confound. QI-002 isolates complete, noiseless motif behaviour where the true parent of `x2` is the unique zero-error separator, so a genuine causal rule is learnable in principle.

## Acceptance / rerun criteria

These criteria decide whether the run is usable as a baseline and whether a rerun or design change is warranted. They are evidentiary thresholds, not interpretation.

| Criterion | Pass | Rerun / investigate |
|---|---|---|
| Cells planned | 6 | any other count -> stop, config bug |
| Cells completed | 6 with artefacts (`metrics.json` + `bk.sol.aba`) | missing artefacts -> investigate pipeline |
| Outcome distribution | mostly `solved` | widespread `error` / `timeout` -> investigate before interpreting |
| Baseline learnability | at least some cells reach `clean_recovery = 1` (perfect parent rule learnable in the ideal case) | `clean_recovery = 0` everywhere -> record as a strong negative baseline finding; check encoding before concluding |
| Determinism | re-running yields identical fixtures (deterministic tables) | divergence -> fixture bug |

## Known limitation (by design)

QI-002 uses canonical orientation only and therefore does NOT break the x0/first-column confound. A learner that simply prefers `x0` would look correct on fork and wrong on chain. Breaking that confound is the job of QI-003. QI-002 answers only "can the perfect rule be learned at all?".

## Decisions taken

- Run with the default learner config (nd folding, `folding_steps: 15`); no extra flags/seeds/targets.
- Do not modify fixtures/config/metrics unless a clear bug is found (then stop and report).
- Interpretation deferred to Samuel/ChatGPT after raw outputs are reviewed.
