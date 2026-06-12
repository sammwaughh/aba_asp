# Motif recovery summary: QI001_motifs_modes_greedy

Generated artefact-collecting summary. Do not edit by hand; regenerate with `causal/scripts/motif_recovery_summary.py`.

Scope: parent-set recovery via ABA Learning. NOT Russo-style Causal ABA (no graph recovery, d-separation, or stable-extension-as-DAG claims). Expected parents are derived from each fixture's ground-truth edges, so parent-position variants are handled correctly. `body_parent_f1` is intentionally omitted (see METRICS.md).

- Experiment: `QI001_motifs_modes_greedy`
- Config: `causal/configs/experiments/QI001_motifs_modes_greedy.yaml`
- Output root: `causal/outputs/aba_learning/grid/QI001_motifs_modes_greedy`
- Status: complete run (all cells have artefacts)
- Cells: 9
- Generated at: 2026-06-12T11:08:55.527066+00:00

Recovery classifications: `exact_parent_recovery`, `parent_subset`, `parent_superset`, `non_parent_or_proxy`, `mixed_parent_and_non_parent`, `rote_or_sample_specific`, `no_solution`, `no_output_yet`, `parser_or_metric_failure`.
## Aggregate (clean_recovery over cells with metrics)

- Overall clean-recovery rate: 0.333 (9 cells)
- binary 0/1: 0.333 (1/3)
- categorical (3 values): 0.333 (1/3)
- continuous (3 uniform bins): 0.333 (1/3)

## Cells

### qi001_chain_binary

- Source id: `qi001_chain_binary`
- Data mode: binary 0/1
- Graph edges: x0 -> x1, x1 -> x2
- Expected parents of `x2` (from edges): {x1}
- Rows: 4
- Run directory: `causal/outputs/aba_learning/grid/QI001_motifs_modes_greedy/cells/1880fb73b11c`
- Outcome: `solved`
- Recovered body variables: {x0, x1}
- Recovery classification: `parent_superset`
- clean_recovery: `0`
- variable-level P/R/Jaccard: 0.500 / 1.000 / 0.500
- ancestor_only_rate / body_parent_recall: 0.000 / 1.000
- Prolog-aware coverage (acc/pos/neg): 1.000 / 1.000 / 1.000
- assumptions / contraries / folding_tokens: 0 / 0 / 0

x2 target rules (2):

```prolog
x2(A) :- x0(A), x1(A).
x2(A) :- x1(A).
```

### qi001_fork_binary

- Source id: `qi001_fork_binary`
- Data mode: binary 0/1
- Graph edges: x0 -> x1, x0 -> x2
- Expected parents of `x2` (from edges): {x0}
- Rows: 4
- Run directory: `causal/outputs/aba_learning/grid/QI001_motifs_modes_greedy/cells/6cf436fdac47`
- Outcome: `solved`
- Recovered body variables: {x0, x1}
- Recovery classification: `parent_superset`
- clean_recovery: `0`
- variable-level P/R/Jaccard: 0.500 / 1.000 / 0.500
- ancestor_only_rate / body_parent_recall: 0.000 / 1.000
- Prolog-aware coverage (acc/pos/neg): 1.000 / 1.000 / 1.000
- assumptions / contraries / folding_tokens: 0 / 0 / 0

x2 target rules (2):

```prolog
x2(A) :- x0(A), x1(A).
x2(A) :- x0(A).
```

### qi001_collider_binary

- Source id: `qi001_collider_binary`
- Data mode: binary 0/1
- Graph edges: x0 -> x2, x1 -> x2
- Expected parents of `x2` (from edges): {x0, x1}
- Rows: 4
- Run directory: `causal/outputs/aba_learning/grid/QI001_motifs_modes_greedy/cells/d9f6f951653e`
- Outcome: `solved`
- Recovered body variables: {x0, x1}
- Recovery classification: `exact_parent_recovery`
- clean_recovery: `1`
- variable-level P/R/Jaccard: 1.000 / 1.000 / 1.000
- ancestor_only_rate / body_parent_recall: 0.000 / 1.000
- Prolog-aware coverage (acc/pos/neg): 1.000 / 1.000 / 1.000
- assumptions / contraries / folding_tokens: 0 / 0 / 0

x2 target rules (2):

```prolog
x2(A) :- x1(A).
x2(A) :- x0(A).
```

### qi001_chain_cat3

- Source id: `qi001_chain_cat3`
- Data mode: categorical (3 values)
- Graph edges: x0 -> x1, x1 -> x2
- Expected parents of `x2` (from edges): {x1}
- Rows: 4
- Run directory: `causal/outputs/aba_learning/grid/QI001_motifs_modes_greedy/cells/6d153efa06f7`
- Outcome: `solved`
- Recovered body variables: {x0, x1}
- Recovery classification: `parent_superset`
- clean_recovery: `0`
- variable-level P/R/Jaccard: 0.500 / 1.000 / 0.500
- ancestor_only_rate / body_parent_recall: 0.000 / 1.000
- Prolog-aware coverage (acc/pos/neg): 1.000 / 1.000 / 1.000
- assumptions / contraries / folding_tokens: 0 / 0 / 0

x2 target rules (2):

```prolog
x2(A) :- x0_val_2(A), x1_val_2(A).
x2(A) :- x0_val_0(A), x1_val_2(A).
```

### qi001_fork_cat3

- Source id: `qi001_fork_cat3`
- Data mode: categorical (3 values)
- Graph edges: x0 -> x1, x0 -> x2
- Expected parents of `x2` (from edges): {x0}
- Rows: 4
- Run directory: `causal/outputs/aba_learning/grid/QI001_motifs_modes_greedy/cells/bb45b82de519`
- Outcome: `solved`
- Recovered body variables: {x0, x1}
- Recovery classification: `parent_superset`
- clean_recovery: `0`
- variable-level P/R/Jaccard: 0.500 / 1.000 / 0.500
- ancestor_only_rate / body_parent_recall: 0.000 / 1.000
- Prolog-aware coverage (acc/pos/neg): 1.000 / 1.000 / 1.000
- assumptions / contraries / folding_tokens: 0 / 0 / 0

x2 target rules (2):

```prolog
x2(A) :- x0_val_2(A), x1_val_2(A).
x2(A) :- x0_val_2(A), x1_val_0(A).
```

### qi001_collider_cat3

- Source id: `qi001_collider_cat3`
- Data mode: categorical (3 values)
- Graph edges: x0 -> x2, x1 -> x2
- Expected parents of `x2` (from edges): {x0, x1}
- Rows: 5
- Run directory: `causal/outputs/aba_learning/grid/QI001_motifs_modes_greedy/cells/40f7a0f10f80`
- Outcome: `solved`
- Recovered body variables: {x0, x1}
- Recovery classification: `exact_parent_recovery`
- clean_recovery: `1`
- variable-level P/R/Jaccard: 1.000 / 1.000 / 1.000
- ancestor_only_rate / body_parent_recall: 0.000 / 1.000
- Prolog-aware coverage (acc/pos/neg): 1.000 / 1.000 / 1.000
- assumptions / contraries / folding_tokens: 0 / 0 / 0

x2 target rules (2):

```prolog
x2(A) :- x0_val_0(A), x1_val_2(A).
x2(A) :- x0_val_2(A), x1_val_1(A).
```

### qi001_chain_cont3

- Source id: `qi001_chain_cont3`
- Data mode: continuous (3 uniform bins)
- Graph edges: x0 -> x1, x1 -> x2
- Expected parents of `x2` (from edges): {x1}
- Rows: 5
- Run directory: `causal/outputs/aba_learning/grid/QI001_motifs_modes_greedy/cells/5828e8de706f`
- Outcome: `solved`
- Recovered body variables: {x0, x1}
- Recovery classification: `parent_superset`
- clean_recovery: `0`
- variable-level P/R/Jaccard: 0.500 / 1.000 / 0.500
- ancestor_only_rate / body_parent_recall: 0.000 / 1.000
- Prolog-aware coverage (acc/pos/neg): 1.000 / 1.000 / 1.000
- assumptions / contraries / folding_tokens: 0 / 0 / 0

x2 target rules (2):

```prolog
x2(A) :- x0_bin1(A), x1_bin1(A).
x2(A) :- x0_bin2(A), x1_bin2(A).
```

### qi001_fork_cont3

- Source id: `qi001_fork_cont3`
- Data mode: continuous (3 uniform bins)
- Graph edges: x0 -> x1, x0 -> x2
- Expected parents of `x2` (from edges): {x0}
- Rows: 5
- Run directory: `causal/outputs/aba_learning/grid/QI001_motifs_modes_greedy/cells/fc07ec7aef7b`
- Outcome: `solved`
- Recovered body variables: {x0, x1}
- Recovery classification: `parent_superset`
- clean_recovery: `0`
- variable-level P/R/Jaccard: 0.500 / 1.000 / 0.500
- ancestor_only_rate / body_parent_recall: 0.000 / 1.000
- Prolog-aware coverage (acc/pos/neg): 1.000 / 1.000 / 1.000
- assumptions / contraries / folding_tokens: 0 / 0 / 0

x2 target rules (2):

```prolog
x2(A) :- x0_bin1(A), x1_bin1(A).
x2(A) :- x0_bin2(A), x1_bin0(A).
```

### qi001_collider_cont3

- Source id: `qi001_collider_cont3`
- Data mode: continuous (3 uniform bins)
- Graph edges: x0 -> x2, x1 -> x2
- Expected parents of `x2` (from edges): {x0, x1}
- Rows: 5
- Run directory: `causal/outputs/aba_learning/grid/QI001_motifs_modes_greedy/cells/2dfe8684b040`
- Outcome: `solved`
- Recovered body variables: {x0, x1}
- Recovery classification: `exact_parent_recovery`
- clean_recovery: `1`
- variable-level P/R/Jaccard: 1.000 / 1.000 / 1.000
- ancestor_only_rate / body_parent_recall: 0.000 / 1.000
- Prolog-aware coverage (acc/pos/neg): 1.000 / 1.000 / 1.000
- assumptions / contraries / folding_tokens: 0 / 0 / 0

x2 target rules (3):

```prolog
x2(A) :- x0_bin0(A), x1_bin2(A).
x2(A) :- x0_bin2(A), x1_bin2(A).
x2(A) :- x0_bin2(A), x1_bin1(A).
```
