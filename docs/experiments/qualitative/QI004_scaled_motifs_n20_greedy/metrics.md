# QI-004 greedy — metrics

> Greedy-folding rerun of `QI004_scaled_motifs_n20`. Metric definitions are unchanged from the nd run; only `folding_mode` differs. Scope: target-wise parent-set recovery under the current `aba_asp/causal` implementation; not causal discovery.

Full definitions live in `causal/aa-plans/METRICS.md`; the variable-level metrics are §3.4b.

## Headline metrics (variable-level parent-set recovery)

Computed by `variable_level_stats(target, learned, ground_truth)` over the non-trivial `x2` target rules. `recovered` is the union of graph variables cited across those rule bodies (target removed); `P` the true parents of `x2`.

| Metric | Meaning | Range / edge case |
|---|---|---|
| `clean_recovery` | strict success flag: `1` iff `recovered == P` (and `P` non-empty), else `0` | {0,1}; `0` when unsolved / no rules |
| `var_parent_precision` | \|recovered ∩ P\| / \|recovered\| | [0,1]; NaN if nothing recovered |
| `var_parent_recall` | \|recovered ∩ P\| / \|P\| | [0,1]; NaN if root |
| `var_parent_jaccard` | \|recovered ∩ P\| / \|recovered ∪ P\| | [0,1]; NaN if both empty |

## Confound-check use of the headline metrics

As in nd QI-004, the decision-critical reading is the `clean_recovery` / `var_parent_*` comparison between `*_x0parent` and `*_x1parent` variants of each motif. The greedy run additionally asks whether the search strategy changes this confound behaviour.

## Continuous bin-health / occupancy

Continuous cells (`*_cont3`) binned into 3 uniform bins at BK-generation time. Bin-health recorded per cell in the raw status table (identical fixtures to nd QI-004).

## Greedy-specific comparison focus

Greedy vs nd separated across: `clean_recovery`, no-solution rate, error rate, runtime (`wall_clock_s`, `folding_tokens_used`, timeout incidence), and interpretability. These are separate axes.

## Supporting diagnostics

`ancestor_only_rate`, `body_parent_recall`, `offgraph_rate`, `outcome`, `n_delta_rules`, `n_target_rules`, `n_assumptions`, `n_contraries`, `folding_tokens_used`, `wall_clock_s`, `cov_pl_*`, `cov_py_*`.

## Not computed

Graph-level skeleton/direction metrics: reserved, not computed.
