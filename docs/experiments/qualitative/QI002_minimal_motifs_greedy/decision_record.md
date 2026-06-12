# QI-002 greedy — decision record

| Field | Value |
|---|---|
| Status | run complete; interpreted |
| Greedy setting | `folding_mode: greedy` (only conceptual change vs nd) |
| Canonical evidence? | Yes — canonical greedy-arm evidence for the QL2 greedy-vs-nd comparison |
| Further rerun needed? | No |

## Acceptance / reading criteria

- Greedy run is comparative evidence against the nd QI-002 baseline, not a standalone causal-discovery result.
- Decision-critical reading: in the noiseless best case, does greedy change `clean_recovery`, no-solution rate, error rate, runtime, or interpretability relative to nd?

## Status notes

- Raw outputs available: yes (6/6 solved; all metrics + solution files present).
- Interpretation completed: yes (`interpretation.md`).
- Rerun appears needed: no.
- Headline: in the noiseless best case, greedy **strictly improved** over nd — clean_recovery 4/6 vs 3/6, solved 6/6 vs 5/6 (greedy solved the `collider_binary` cell nd could not), and ~5x faster. One cell (`fork_cat3`) regressed from exact to `parent_superset`.
