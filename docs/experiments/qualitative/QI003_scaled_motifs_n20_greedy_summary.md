# Motif recovery summary: QI004_scaled_motifs_n20_greedy

Generated artefact-collecting summary. Do not edit by hand; regenerate with `causal/scripts/motif_recovery_summary.py`.

Scope: parent-set recovery via ABA Learning. NOT Russo-style Causal ABA (no graph recovery, d-separation, or stable-extension-as-DAG claims). Expected parents are derived from each fixture's ground-truth edges, so parent-position variants are handled correctly. `body_parent_f1` is intentionally omitted (see METRICS.md).

- Experiment: `QI004_scaled_motifs_n20_greedy`
- Config: `causal/configs/experiments/QI004_scaled_motifs_n20_greedy.yaml`
- Output root: `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20_greedy`
- Status: complete run (all cells have artefacts)
- Cells: 15
- Generated at: 2026-06-12T11:08:56.250635+00:00

Recovery classifications: `exact_parent_recovery`, `parent_subset`, `parent_superset`, `non_parent_or_proxy`, `mixed_parent_and_non_parent`, `rote_or_sample_specific`, `no_solution`, `no_output_yet`, `parser_or_metric_failure`.
## Aggregate (clean_recovery over cells with metrics)

- Overall clean-recovery rate: 0.000 (15 cells)
- binary 0/1: 0.000 (0/5)
- categorical (3 values): 0.000 (0/5)
- continuous (3 uniform bins): 0.000 (0/5)

## Cells

### qi004_chain_x1parent_binary

- Source id: `qi004_chain_x1parent_binary`
- Data mode: binary 0/1
- Graph edges: x0 -> x1, x1 -> x2
- Expected parents of `x2` (from edges): {x1}
- Rows: 20
- Run directory: `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20_greedy/cells/34cb7dc162d4`
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

### qi004_chain_x1parent_cat3

- Source id: `qi004_chain_x1parent_cat3`
- Data mode: categorical (3 values)
- Graph edges: x0 -> x1, x1 -> x2
- Expected parents of `x2` (from edges): {x1}
- Rows: 20
- Run directory: `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20_greedy/cells/4d12a21aff90`
- Outcome: `completed_no_solution`
- Recovered body variables: {}
- Recovery classification: `no_solution`
- clean_recovery: `0`
- variable-level P/R/Jaccard: n/a / 0.000 / 0.000
- ancestor_only_rate / body_parent_recall: n/a / 0.000
- Prolog-aware coverage (acc/pos/neg): 0.550 / 0.000 / 1.000
- assumptions / contraries / folding_tokens: 0 / 0 / 0

x2 target rules (0):

```prolog
% (no x2-headed target rules)
```

### qi004_chain_x1parent_cont3

- Source id: `qi004_chain_x1parent_cont3`
- Data mode: continuous (3 uniform bins)
- Graph edges: x0 -> x1, x1 -> x2
- Expected parents of `x2` (from edges): {x1}
- Rows: 20
- Run directory: `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20_greedy/cells/2f9727611d49`
- Outcome: `completed_no_solution`
- Recovered body variables: {}
- Recovery classification: `no_solution`
- clean_recovery: `0`
- variable-level P/R/Jaccard: n/a / 0.000 / 0.000
- ancestor_only_rate / body_parent_recall: n/a / 0.000
- Prolog-aware coverage (acc/pos/neg): 0.450 / 0.000 / 1.000
- assumptions / contraries / folding_tokens: 0 / 0 / 0

x2 target rules (0):

```prolog
% (no x2-headed target rules)
```

### qi004_chain_x0parent_binary

- Source id: `qi004_chain_x0parent_binary`
- Data mode: binary 0/1
- Graph edges: x1 -> x0, x0 -> x2
- Expected parents of `x2` (from edges): {x0}
- Rows: 20
- Run directory: `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20_greedy/cells/a9a29cfd0182`
- Outcome: `completed_no_solution`
- Recovered body variables: {}
- Recovery classification: `no_solution`
- clean_recovery: `0`
- variable-level P/R/Jaccard: n/a / 0.000 / 0.000
- ancestor_only_rate / body_parent_recall: n/a / 0.000
- Prolog-aware coverage (acc/pos/neg): 0.650 / 0.000 / 1.000
- assumptions / contraries / folding_tokens: 0 / 0 / 0

x2 target rules (0):

```prolog
% (no x2-headed target rules)
```

### qi004_chain_x0parent_cat3

- Source id: `qi004_chain_x0parent_cat3`
- Data mode: categorical (3 values)
- Graph edges: x1 -> x0, x0 -> x2
- Expected parents of `x2` (from edges): {x0}
- Rows: 20
- Run directory: `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20_greedy/cells/b87948a29834`
- Outcome: `completed_no_solution`
- Recovered body variables: {}
- Recovery classification: `no_solution`
- clean_recovery: `0`
- variable-level P/R/Jaccard: n/a / 0.000 / 0.000
- ancestor_only_rate / body_parent_recall: n/a / 0.000
- Prolog-aware coverage (acc/pos/neg): 0.750 / 0.000 / 1.000
- assumptions / contraries / folding_tokens: 0 / 0 / 0

x2 target rules (0):

```prolog
% (no x2-headed target rules)
```

### qi004_chain_x0parent_cont3

- Source id: `qi004_chain_x0parent_cont3`
- Data mode: continuous (3 uniform bins)
- Graph edges: x1 -> x0, x0 -> x2
- Expected parents of `x2` (from edges): {x0}
- Rows: 20
- Run directory: `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20_greedy/cells/7998f97b0dc2`
- Outcome: `completed_no_solution`
- Recovered body variables: {}
- Recovery classification: `no_solution`
- clean_recovery: `0`
- variable-level P/R/Jaccard: n/a / 0.000 / 0.000
- ancestor_only_rate / body_parent_recall: n/a / 0.000
- Prolog-aware coverage (acc/pos/neg): 0.500 / 0.000 / 1.000
- assumptions / contraries / folding_tokens: 0 / 0 / 0

x2 target rules (0):

```prolog
% (no x2-headed target rules)
```

### qi004_fork_x0parent_binary

- Source id: `qi004_fork_x0parent_binary`
- Data mode: binary 0/1
- Graph edges: x0 -> x1, x0 -> x2
- Expected parents of `x2` (from edges): {x0}
- Rows: 20
- Run directory: `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20_greedy/cells/ea216a6f0a77`
- Outcome: `error`
- Recovered body variables: {}
- Recovery classification: `parser_or_metric_failure`
- clean_recovery: `0`
- variable-level P/R/Jaccard: n/a / 0.000 / 0.000
- ancestor_only_rate / body_parent_recall: n/a / 0.000
- Prolog-aware coverage (acc/pos/neg): 0.400 / 0.000 / 1.000
- assumptions / contraries / folding_tokens: 0 / 0 / 0

x2 target rules (0):

```prolog
% (no x2-headed target rules)
```

### qi004_fork_x0parent_cat3

- Source id: `qi004_fork_x0parent_cat3`
- Data mode: categorical (3 values)
- Graph edges: x0 -> x1, x0 -> x2
- Expected parents of `x2` (from edges): {x0}
- Rows: 20
- Run directory: `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20_greedy/cells/741c998a06e8`
- Outcome: `completed_no_solution`
- Recovered body variables: {}
- Recovery classification: `no_solution`
- clean_recovery: `0`
- variable-level P/R/Jaccard: n/a / 0.000 / 0.000
- ancestor_only_rate / body_parent_recall: n/a / 0.000
- Prolog-aware coverage (acc/pos/neg): 0.650 / 0.000 / 1.000
- assumptions / contraries / folding_tokens: 0 / 0 / 0

x2 target rules (0):

```prolog
% (no x2-headed target rules)
```

### qi004_fork_x0parent_cont3

- Source id: `qi004_fork_x0parent_cont3`
- Data mode: continuous (3 uniform bins)
- Graph edges: x0 -> x1, x0 -> x2
- Expected parents of `x2` (from edges): {x0}
- Rows: 20
- Run directory: `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20_greedy/cells/649f1c294e68`
- Outcome: `completed_no_solution`
- Recovered body variables: {}
- Recovery classification: `no_solution`
- clean_recovery: `0`
- variable-level P/R/Jaccard: n/a / 0.000 / 0.000
- ancestor_only_rate / body_parent_recall: n/a / 0.000
- Prolog-aware coverage (acc/pos/neg): 0.550 / 0.000 / 1.000
- assumptions / contraries / folding_tokens: 0 / 0 / 0

x2 target rules (0):

```prolog
% (no x2-headed target rules)
```

### qi004_fork_x1parent_binary

- Source id: `qi004_fork_x1parent_binary`
- Data mode: binary 0/1
- Graph edges: x1 -> x0, x1 -> x2
- Expected parents of `x2` (from edges): {x1}
- Rows: 20
- Run directory: `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20_greedy/cells/1a4632a5897c`
- Outcome: `completed_no_solution`
- Recovered body variables: {}
- Recovery classification: `no_solution`
- clean_recovery: `0`
- variable-level P/R/Jaccard: n/a / 0.000 / 0.000
- ancestor_only_rate / body_parent_recall: n/a / 0.000
- Prolog-aware coverage (acc/pos/neg): 0.500 / 0.000 / 1.000
- assumptions / contraries / folding_tokens: 0 / 0 / 0

x2 target rules (0):

```prolog
% (no x2-headed target rules)
```

### qi004_fork_x1parent_cat3

- Source id: `qi004_fork_x1parent_cat3`
- Data mode: categorical (3 values)
- Graph edges: x1 -> x0, x1 -> x2
- Expected parents of `x2` (from edges): {x1}
- Rows: 20
- Run directory: `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20_greedy/cells/a5e30417c45a`
- Outcome: `completed_no_solution`
- Recovered body variables: {}
- Recovery classification: `no_solution`
- clean_recovery: `0`
- variable-level P/R/Jaccard: n/a / 0.000 / 0.000
- ancestor_only_rate / body_parent_recall: n/a / 0.000
- Prolog-aware coverage (acc/pos/neg): 0.750 / 0.000 / 1.000
- assumptions / contraries / folding_tokens: 0 / 0 / 0

x2 target rules (0):

```prolog
% (no x2-headed target rules)
```

### qi004_fork_x1parent_cont3

- Source id: `qi004_fork_x1parent_cont3`
- Data mode: continuous (3 uniform bins)
- Graph edges: x1 -> x0, x1 -> x2
- Expected parents of `x2` (from edges): {x1}
- Rows: 20
- Run directory: `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20_greedy/cells/a60974b69490`
- Outcome: `completed_no_solution`
- Recovered body variables: {}
- Recovery classification: `no_solution`
- clean_recovery: `0`
- variable-level P/R/Jaccard: n/a / 0.000 / 0.000
- ancestor_only_rate / body_parent_recall: n/a / 0.000
- Prolog-aware coverage (acc/pos/neg): 0.500 / 0.000 / 1.000
- assumptions / contraries / folding_tokens: 0 / 0 / 0

x2 target rules (0):

```prolog
% (no x2-headed target rules)
```

### qi004_collider_binary

- Source id: `qi004_collider_binary`
- Data mode: binary 0/1
- Graph edges: x0 -> x2, x1 -> x2
- Expected parents of `x2` (from edges): {x0, x1}
- Rows: 20
- Run directory: `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20_greedy/cells/644721f488da`
- Outcome: `error`
- Recovered body variables: {}
- Recovery classification: `parser_or_metric_failure`
- clean_recovery: `0`
- variable-level P/R/Jaccard: n/a / 0.000 / 0.000
- ancestor_only_rate / body_parent_recall: n/a / 0.000
- Prolog-aware coverage (acc/pos/neg): 0.400 / 0.000 / 1.000
- assumptions / contraries / folding_tokens: 0 / 0 / 0

x2 target rules (0):

```prolog
% (no x2-headed target rules)
```

### qi004_collider_cat3

- Source id: `qi004_collider_cat3`
- Data mode: categorical (3 values)
- Graph edges: x0 -> x2, x1 -> x2
- Expected parents of `x2` (from edges): {x0, x1}
- Rows: 20
- Run directory: `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20_greedy/cells/ab531f5536c3`
- Outcome: `completed_no_solution`
- Recovered body variables: {}
- Recovery classification: `no_solution`
- clean_recovery: `0`
- variable-level P/R/Jaccard: n/a / 0.000 / 0.000
- ancestor_only_rate / body_parent_recall: n/a / 0.000
- Prolog-aware coverage (acc/pos/neg): 0.600 / 0.000 / 1.000
- assumptions / contraries / folding_tokens: 0 / 0 / 0

x2 target rules (0):

```prolog
% (no x2-headed target rules)
```

### qi004_collider_cont3

- Source id: `qi004_collider_cont3`
- Data mode: continuous (3 uniform bins)
- Graph edges: x0 -> x2, x1 -> x2
- Expected parents of `x2` (from edges): {x0, x1}
- Rows: 20
- Run directory: `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20_greedy/cells/fbc19a5e15cc`
- Outcome: `completed_no_solution`
- Recovered body variables: {}
- Recovery classification: `no_solution`
- clean_recovery: `0`
- variable-level P/R/Jaccard: n/a / 0.000 / 0.000
- ancestor_only_rate / body_parent_recall: n/a / 0.000
- Prolog-aware coverage (acc/pos/neg): 0.700 / 0.000 / 1.000
- assumptions / contraries / folding_tokens: 0 / 0 / 0

x2 target rules (0):

```prolog
% (no x2-headed target rules)
```
