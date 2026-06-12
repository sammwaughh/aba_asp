# QI-004 interpretation (QI004_scaled_motifs_n20)

> QI-004 is the feasible (`n=20`, `prolog_timeout_s=300`) follow-up to QI-003: a scaled, confound-controlled parent-set recovery investigation using the current ABA Learning bridge. It is not full Russo-style Causal ABA, graph recovery, d-separation reasoning, or stable-extension-as-DAG machinery.

Status: pending interpretation (raw outputs recorded by the post-run audit). Fill one section per cell after reviewing `bk.sol.aba` / the generated summary, copying learned rules exactly.

## Classification vocabulary

- `exact_parent_recovery` (`clean_recovery = 1`), `parent_subset`, `parent_superset`,
  `non_parent_or_proxy`, `mixed_parent_and_non_parent`, `rote_or_sample_specific`,
  `no_solution`, `no_output_yet`, `parser_or_metric_failure`.

## Headline metrics to record per cell

`clean_recovery`, `var_parent_precision/recall/jaccard`, `ancestor_only_rate`, `n_assumptions`, `folding_tokens_used`, outcome.

## Decision-critical confound check

Compare the x0-parent vs x1-parent variants. If recovery tracks the *true parent column* (high `clean_recovery` for both `*_x0parent` and `*_x1parent`), the learner is finding the cause. If recovery tracks `x0` regardless of where the parent is, it is exhibiting the positional confound.

| Comparison | x0parent clean_recovery | x1parent clean_recovery | Verdict |
|---|---|---|---|
| chain (binary) | TBD | TBD | TBD |
| chain (cat3) | TBD | TBD | TBD |
| chain (cont3) | TBD | TBD | TBD |
| fork (binary) | TBD | TBD | TBD |
| fork (cat3) | TBD | TBD | TBD |
| fork (cont3) | TBD | TBD | TBD |

---

## Per-cell sections (15)

For each fixture id below: record learned rules, recovered body variables, `clean_recovery`, classification, interpretation, next decision.

### chain
- `qi004_chain_x1parent_binary` (parents {x1}): `TBD`
- `qi004_chain_x1parent_cat3` (parents {x1}): `TBD`
- `qi004_chain_x1parent_cont3` (parents {x1}): `TBD`
- `qi004_chain_x0parent_binary` (parents {x0}): `TBD`
- `qi004_chain_x0parent_cat3` (parents {x0}): `TBD`
- `qi004_chain_x0parent_cont3` (parents {x0}): `TBD`

### fork
- `qi004_fork_x0parent_binary` (parents {x0}): `TBD`
- `qi004_fork_x0parent_cat3` (parents {x0}): `TBD`
- `qi004_fork_x0parent_cont3` (parents {x0}): `TBD`
- `qi004_fork_x1parent_binary` (parents {x1}): `TBD`
- `qi004_fork_x1parent_cat3` (parents {x1}): `TBD`
- `qi004_fork_x1parent_cont3` (parents {x1}): `TBD`

### collider
- `qi004_collider_binary` (parents {x0, x1}): `TBD`
- `qi004_collider_cat3` (parents {x0, x1}): `TBD`
- `qi004_collider_cont3` (parents {x0, x1}): `TBD`

---

## Cross-cell summary (fill after all cells)

- Clean-recovery rate overall: `TBD`
- By data mode (binary / cat3 / cont3): `TBD`
- By parent position (x0parent / x1parent): `TBD`
- Is the x0 confound broken? `TBD`
- Comparison vs QI-002 (noiseless) behaviour: `TBD`
- Next decision for the project: `TBD`
