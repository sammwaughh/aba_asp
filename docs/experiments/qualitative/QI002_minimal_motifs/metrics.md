# QI-002 metrics (QI002_minimal_motifs)

> QI-002 is a minimal-baseline parent-set recovery investigation using the current ABA Learning bridge. It is not full Russo-style Causal ABA, graph recovery, d-separation reasoning, or stable-extension-as-DAG machinery.

This file records which metrics QI-002 leads with and what each one measures. Full definitions live in `causal/aa-plans/METRICS.md`; the variable-level metrics are §3.4b.

## Headline metrics (variable-level parent-set recovery)

Computed by `variable_level_stats(target, learned, ground_truth)` over the non-trivial `x2` target rules. Let `recovered` be the union of graph variables cited across those rule bodies (target removed), and `P` the true parents of `x2`.

| Metric | Meaning | Range / edge case |
|---|---|---|
| `clean_recovery` | strict success flag: `1` iff `recovered == P` (and `P` non-empty), else `0` | {0,1}; `0` when unsolved / no rules |
| `var_parent_precision` | fraction of recovered variables that are true parents = \|recovered ∩ P\| / \|recovered\| | [0,1]; NaN (`no_recovered_vars`) if nothing recovered |
| `var_parent_recall` | fraction of true parents recovered = \|recovered ∩ P\| / \|P\| | [0,1]; NaN (`no_parents`) if root |
| `var_parent_jaccard` | set overlap = \|recovered ∩ P\| / \|recovered ∪ P\| | [0,1]; NaN if both empty |

These are the primary QI-002 metrics: in the noiseless complete-truth-table design the true parent is the unique zero-error separator, so `clean_recovery = 1` is the meaningful "the perfect causal rule was learned" outcome.

## Supporting diagnostics

| Metric | Meaning |
|---|---|
| `ancestor_only_rate` | fraction of non-trivial `x2` rules whose body variables are ancestors but not direct parents (proxy detection) |
| `body_parent_recall` | rule-level recall of parent variables across `x2` rules |
| `offgraph_rate` | fraction of `x2` rule body variables not in the graph (inert at 3 nodes; kept for schema stability) |
| `outcome` | `solved` / `completed_no_solution` / `completed_empty_delta` / `timeout` / `skipped` / `error` |
| `n_delta_rules`, `n_target_rules`, `n_trivial/nontrivial_target_rules` | learned rule structure |
| `n_assumptions`, `n_contraries` | ABA Learning structure introduced |
| `folding_tokens_used`, `wall_clock_s` | efficiency proxies |
| `cov_pl_*`, `cov_py_*` | Prolog-aware and Python-Horn coverage of E+/E- |

## De-emphasised

- `body_parent_f1`: mixes a rule-level precision with a variable-level recall (different denominators) and is lenient (a rule citing a parent plus an ancestor still counts as a parent hit). Retained in the parquet schema for cross-experiment stability but not led with for motif recovery; the generated summary omits it.

## Not applicable to QI-002

- Continuous bin-health: QI-002 has no continuous cells (binary + categorical-3 only), so bin-occupancy diagnostics do not apply. (They do apply to QI-003.)
- Graph-level skeleton/direction/bridge metrics: reserved, not computed.
