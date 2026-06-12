# Motif recovery summary: QI002_minimal_motifs

Generated artefact-collecting summary. Do not edit by hand; regenerate with `causal/scripts/motif_recovery_summary.py`.

Scope: parent-set recovery via ABA Learning. NOT Russo-style Causal ABA (no graph recovery, d-separation, or stable-extension-as-DAG claims). Expected parents are derived from each fixture's ground-truth edges, so parent-position variants are handled correctly. `body_parent_f1` is intentionally omitted (see METRICS.md).

- Experiment: `QI002_minimal_motifs`
- Config: `causal/configs/experiments/QI002_minimal_motifs.yaml`
- Output root: `causal/outputs/aba_learning/grid/QI002_minimal_motifs`
- Status: complete run (all cells have artefacts)
- Cells: 6
- Generated at: 2026-06-12T08:11:16.359294+00:00

Recovery classifications: `exact_parent_recovery`, `parent_subset`, `parent_superset`, `non_parent_or_proxy`, `mixed_parent_and_non_parent`, `rote_or_sample_specific`, `no_solution`, `no_output_yet`, `parser_or_metric_failure`.
## Aggregate (clean_recovery over cells with metrics)

- Overall clean-recovery rate: 0.500 (6 cells)
- binary 0/1: 0.667 (2/3)
- categorical (3 values): 0.333 (1/3)

## Cells

### qi002_chain_binary

- Source id: `qi002_chain_binary`
- Data mode: binary 0/1
- Graph edges: x0 -> x1, x1 -> x2
- Expected parents of `x2` (from edges): {x1}
- Rows: 8
- Run directory: `causal/outputs/aba_learning/grid/QI002_minimal_motifs/cells/45486ba3a361`
- Outcome: `solved`
- Recovered body variables: {x1}
- Recovery classification: `exact_parent_recovery`
- clean_recovery: `1`
- variable-level P/R/Jaccard: 1.000 / 1.000 / 1.000
- ancestor_only_rate / body_parent_recall: 0.000 / 1.000
- Prolog-aware coverage (acc/pos/neg): 1.000 / 1.000 / 1.000
- assumptions / contraries / folding_tokens: 0 / 0 / 0

x2 target rules (1):

```prolog
x2(A) :- x1(A).
```

### qi002_fork_binary

- Source id: `qi002_fork_binary`
- Data mode: binary 0/1
- Graph edges: x0 -> x1, x0 -> x2
- Expected parents of `x2` (from edges): {x0}
- Rows: 8
- Run directory: `causal/outputs/aba_learning/grid/QI002_minimal_motifs/cells/820abf0b0794`
- Outcome: `solved`
- Recovered body variables: {x0}
- Recovery classification: `exact_parent_recovery`
- clean_recovery: `1`
- variable-level P/R/Jaccard: 1.000 / 1.000 / 1.000
- ancestor_only_rate / body_parent_recall: 0.000 / 1.000
- Prolog-aware coverage (acc/pos/neg): 1.000 / 1.000 / 1.000
- assumptions / contraries / folding_tokens: 0 / 0 / 0

x2 target rules (1):

```prolog
x2(A) :- x0(A).
```

### qi002_collider_binary

- Source id: `qi002_collider_binary`
- Data mode: binary 0/1
- Graph edges: x0 -> x2, x1 -> x2
- Expected parents of `x2` (from edges): {x0, x1}
- Rows: 8
- Run directory: `causal/outputs/aba_learning/grid/QI002_minimal_motifs/cells/337667a5bfd2`
- Outcome: `completed_no_solution`
- Recovered body variables: {}
- Recovery classification: `no_solution`
- clean_recovery: `0`
- variable-level P/R/Jaccard: n/a / 0.000 / 0.000
- ancestor_only_rate / body_parent_recall: n/a / 0.000
- Prolog-aware coverage (acc/pos/neg): 0.750 / 0.000 / 1.000
- assumptions / contraries / folding_tokens: 0 / 0 / 15

x2 target rules (0):

```prolog
% (no x2-headed target rules)
```

### qi002_chain_cat3

- Source id: `qi002_chain_cat3`
- Data mode: categorical (3 values)
- Graph edges: x0 -> x1, x1 -> x2
- Expected parents of `x2` (from edges): {x1}
- Rows: 18
- Run directory: `causal/outputs/aba_learning/grid/QI002_minimal_motifs/cells/2843e9b5d658`
- Outcome: `solved`
- Recovered body variables: {x0}
- Recovery classification: `non_parent_or_proxy`
- clean_recovery: `0`
- variable-level P/R/Jaccard: 0.000 / 0.000 / 0.000
- ancestor_only_rate / body_parent_recall: 1.000 / 0.000
- Prolog-aware coverage (acc/pos/neg): 0.667 / 0.000 / 1.000
- assumptions / contraries / folding_tokens: 3 / 3 / 0

x2 target rules (3):

```prolog
x2(A) :- alpha_1(A), x0_val_0(A).
x2(A) :- alpha_2(A), x0_val_1(A).
x2(A) :- alpha_3(A), x0_val_2(A).
```

### qi002_fork_cat3

- Source id: `qi002_fork_cat3`
- Data mode: categorical (3 values)
- Graph edges: x0 -> x1, x0 -> x2
- Expected parents of `x2` (from edges): {x0}
- Rows: 18
- Run directory: `causal/outputs/aba_learning/grid/QI002_minimal_motifs/cells/0fee1761813c`
- Outcome: `solved`
- Recovered body variables: {x0}
- Recovery classification: `exact_parent_recovery`
- clean_recovery: `1`
- variable-level P/R/Jaccard: 1.000 / 1.000 / 1.000
- ancestor_only_rate / body_parent_recall: 0.000 / 1.000
- Prolog-aware coverage (acc/pos/neg): 1.000 / 1.000 / 1.000
- assumptions / contraries / folding_tokens: 0 / 0 / 0

x2 target rules (1):

```prolog
x2(A) :- x0_val_2(A).
```

### qi002_collider_cat3

- Source id: `qi002_collider_cat3`
- Data mode: categorical (3 values)
- Graph edges: x0 -> x2, x1 -> x2
- Expected parents of `x2` (from edges): {x0, x1}
- Rows: 18
- Run directory: `causal/outputs/aba_learning/grid/QI002_minimal_motifs/cells/2cca7a4a1fde`
- Outcome: `solved`
- Recovered body variables: {x0}
- Recovery classification: `parent_subset`
- clean_recovery: `0`
- variable-level P/R/Jaccard: 1.000 / 0.500 / 0.500
- ancestor_only_rate / body_parent_recall: 0.000 / 0.500
- Prolog-aware coverage (acc/pos/neg): 0.444 / 0.000 / 1.000
- assumptions / contraries / folding_tokens: 2 / 2 / 0

x2 target rules (3):

```prolog
x2(A) :- alpha_1(A), x0_val_0(A).
x2(A) :- alpha_2(A), x0_val_1(A).
x2(A) :- x0_val_2(A).
```
