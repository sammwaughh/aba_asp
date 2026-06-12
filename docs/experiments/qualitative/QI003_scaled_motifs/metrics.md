# QI-003 metrics (QI003_scaled_motifs)

> QI-003 is a scaled, confound-controlled parent-set recovery investigation using the current ABA Learning bridge. It is not full Russo-style Causal ABA, graph recovery, d-separation reasoning, or stable-extension-as-DAG machinery.

This file records which metrics QI-003 leads with and what each one measures. Full definitions live in `causal/aa-plans/METRICS.md`; the variable-level metrics are §3.4b.

## Headline metrics (variable-level parent-set recovery)

Computed by `variable_level_stats(target, learned, ground_truth)` over the non-trivial `x2` target rules. Let `recovered` be the union of graph variables cited across those rule bodies (target removed), and `P` the true parents of `x2`.

| Metric | Meaning | Range / edge case |
|---|---|---|
| `clean_recovery` | strict success flag: `1` iff `recovered == P` (and `P` non-empty), else `0` | {0,1}; `0` when unsolved / no rules |
| `var_parent_precision` | \|recovered ∩ P\| / \|recovered\| | [0,1]; NaN (`no_recovered_vars`) if nothing recovered |
| `var_parent_recall` | \|recovered ∩ P\| / \|P\| | [0,1]; NaN (`no_parents`) if root |
| `var_parent_jaccard` | \|recovered ∩ P\| / \|recovered ∪ P\| | [0,1]; NaN if both empty |

## Confound-check use of the headline metrics

QI-003's design goal is to break the QI-001 x0/first-column confound via parent-position variants. The decision-critical reading is the `clean_recovery` (and `var_parent_*`) comparison between the `*_x0parent` and `*_x1parent` variants of each motif:

- recovery tracking the true parent column (high `clean_recovery` for both orientations) is evidence of parent recovery;
- recovery tracking `x0` regardless of where the parent sits is evidence of the positional confound.

## Continuous bin-health / occupancy

Continuous cells (`*_cont3`) are binned into 3 uniform bins at BK-generation time (`bins=3`, `bin_strategy=uniform`). With `n=100` the bins are expected to be populated (verified pre-run: each of the 3 bins had >= 7 samples for `x0`/`x1` across the continuous fixtures). Bin-health note recorded per cell in the raw status table: whether all 3 bins are non-empty, since sparse/empty bins would make the categorical predicate vocabulary degenerate.

## Supporting diagnostics

| Metric | Meaning |
|---|---|
| `ancestor_only_rate` | fraction of non-trivial `x2` rules citing ancestors but not direct parents (proxy detection; matters for chain) |
| `body_parent_recall` | rule-level recall of parent variables across `x2` rules |
| `offgraph_rate` | fraction of `x2` rule body variables off-graph (inert at 3 nodes; schema stability) |
| `outcome` | `solved` / `completed_no_solution` / `completed_empty_delta` / `timeout` / `skipped` / `error` |
| `n_delta_rules`, `n_target_rules`, `n_trivial/nontrivial_target_rules` | learned rule structure |
| `n_assumptions`, `n_contraries` | ABA Learning structure introduced |
| `folding_tokens_used`, `wall_clock_s` | efficiency proxies |
| `cov_pl_*`, `cov_py_*` | Prolog-aware and Python-Horn coverage of E+/E- |

## De-emphasised

- `body_parent_f1`: lenient and mixes denominators; retained in the parquet schema for cross-experiment stability but omitted from the generated motif-recovery summary.

## Not computed

- Graph-level skeleton/direction/bridge metrics: reserved, not computed.
