# QI-004 greedy — decision record

| Field | Value |
|---|---|
| Status | run complete; interpreted |
| Greedy setting | `folding_mode: greedy` (only conceptual change vs nd) |
| Canonical evidence? | Yes — canonical greedy-arm evidence for the QI-004 greedy-vs-nd comparison |
| Further rerun needed? | No |

## Acceptance / reading criteria

- Greedy run is comparative evidence against the nd QI-004 baseline, not a standalone causal-discovery result.
- Decision-critical reading: at the scaled/noisy setting, does greedy change `clean_recovery`, the x0/x1 confound behaviour, no-solution rate, error rate, runtime, or interpretability relative to nd?
- Greedy cost caveat: if cat3/cont3 cells repeatedly time out at 300s, record the timeout status and stop (no blind reruns).

## Status notes

- Raw outputs available: yes (15/15 cells completed; metrics present; 1 solution file).
- Interpretation completed: yes (`interpretation.md`).
- Rerun appears needed: no. The greedy cost caveat did not materialise (no timeouts; ~10 s total vs nd ~1233 s).
- Headline: greedy QI004 is **cell-by-cell identical to nd** in outcomes and recovery (1 solved, 12 no-solution, 2 binary errors; clean_recovery 0/15) but ~120x faster. Greedy changes runtime only at this scaled/noisy setting; it does not rescue recovery.
