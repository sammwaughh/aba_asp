# QI-001 greedy — decision record

| Field | Value |
|---|---|
| Status | run complete; interpreted |
| Greedy setting | `folding_mode: greedy` (only conceptual change vs nd) |
| Canonical evidence? | Yes — canonical greedy-arm evidence for the QI-001 greedy-vs-nd comparison |
| Further rerun needed? | No |

## Acceptance / reading criteria

- Greedy run is comparative evidence against the nd QI-001 baseline, not a standalone causal-discovery result.
- Decision-critical reading: does greedy change `clean_recovery`, no-solution rate, error rate, runtime, or learned-rule interpretability relative to nd, on identical fixtures?

## Status notes

- Raw outputs available: yes (9/9 solved; all metrics + solution files present).
- Interpretation completed: yes (`interpretation.md`).
- Rerun appears needed: no.
- Headline: greedy QI001 = 9/9 solved, clean_recovery 3/9 (all colliders clean; chain/fork all `parent_superset`). Runtime ≈ 2.9 s (nd ≈ 4.0 s). nd QI001 predates the `clean_recovery` field, so the recovery comparison is qualitative (see `interpretation.md`).
