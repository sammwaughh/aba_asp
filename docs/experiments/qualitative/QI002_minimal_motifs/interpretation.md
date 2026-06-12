# QI-002 interpretation (QI002_minimal_motifs)

> QI-002 is a minimal-baseline parent-set recovery investigation using the current ABA Learning bridge. It is not full Russo-style Causal ABA, graph recovery, d-separation reasoning, or stable-extension-as-DAG machinery.

Status: pending run. Fill one section per cell after the ABA Learning run, copying learned rules exactly from `bk.sol.aba` / the generated summary. Do not fill from assumptions.

## Classification vocabulary

- `exact_parent_recovery` — recovered body variables equal the expected parents (`clean_recovery = 1`).
- `parent_subset` — recovered are all parents but miss at least one.
- `parent_superset` — recovered include all parents plus extras.
- `non_parent_or_proxy` — recovered disjoint from parents.
- `mixed_parent_and_non_parent` — some parents and some non-parents.
- `rote_or_sample_specific` — target rules exist but cite no base variables.
- `no_solution` / `no_output_yet` / `parser_or_metric_failure`.

## Headline metrics to record per cell

`clean_recovery`, `var_parent_precision/recall/jaccard`, `ancestor_only_rate`, `n_assumptions`, `folding_tokens_used`, outcome.

---

## qi002_chain_binary (chain, binary) — expected parents {x1}

- Learned rules:

```text
TBD
```

- Recovered body variables: `TBD`
- clean_recovery: `TBD`
- Classification: `TBD`
- Interpretation: `TBD`
- Next decision: `TBD`

---

## qi002_fork_binary (fork, binary) — expected parents {x0}

- Learned rules:

```text
TBD
```

- Recovered body variables: `TBD`
- clean_recovery: `TBD`
- Classification: `TBD`
- Interpretation: `TBD`
- Next decision: `TBD`

---

## qi002_collider_binary (collider, binary) — expected parents {x0, x1}

- Learned rules:

```text
TBD
```

- Recovered body variables: `TBD`
- clean_recovery: `TBD`
- Classification: `TBD`
- Interpretation: `TBD`
- Next decision: `TBD`

---

## qi002_chain_cat3 (chain, categorical-3) — expected parents {x1}

- Learned rules:

```text
TBD
```

- Recovered body variables: `TBD`
- clean_recovery: `TBD`
- Classification: `TBD`
- Interpretation: `TBD`
- Next decision: `TBD`

---

## qi002_fork_cat3 (fork, categorical-3) — expected parents {x0}

- Learned rules:

```text
TBD
```

- Recovered body variables: `TBD`
- clean_recovery: `TBD`
- Classification: `TBD`
- Interpretation: `TBD`
- Next decision: `TBD`

---

## qi002_collider_cat3 (collider, categorical-3) — expected parents {x0, x1}

- Learned rules:

```text
TBD
```

- Recovered body variables: `TBD`
- clean_recovery: `TBD`
- Classification: `TBD`
- Interpretation: `TBD`
- Next decision: `TBD`

---

## Cross-cell summary (fill after all cells)

- Clean-recovery rate overall: `TBD`
- Recovery by data mode (binary / cat3): `TBD`
- Recovery by motif (chain / fork / collider): `TBD`
- Does the perfect-rule-exists baseline succeed? `TBD`
- Next decision for the project: `TBD`
