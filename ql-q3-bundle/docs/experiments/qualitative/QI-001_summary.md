# QI-001 generated summary: QI001_motifs_modes

Generated artefact-collecting summary (distinct from the human-written record `docs/experiments/qualitative/QI-001.md`). Do not edit by hand; regenerate with the command below.

Scope: parent-set recovery via ABA Learning. This is NOT full Russo-style Causal ABA and makes no graph-recovery, d-separation, or stable-extension-as-DAG claims.

- Experiment: `QI001_motifs_modes`
- Config: `causal/configs/experiments/QI001_motifs_modes.yaml`
- Output root: `causal/outputs/aba_learning/grid/QI001_motifs_modes`
- Status: complete run (all cells have artefacts)
- Cells: 9
- Generated at: 2026-06-12T06:47:48.234275+00:00

Recovery classifications: `exact_parent_recovery`, `parent_subset`, `parent_superset`, `non_parent_or_proxy`, `mixed_parent_and_non_parent`, `rote_or_sample_specific`, `no_solution`, `no_output_yet`, `parser_or_metric_failure`.

## Cells
### qi001_chain_binary

- Source id: `qi001_chain_binary`
- Motif: chain
- Data mode: binary 0/1
- Graph edges: x0 -> x1, x1 -> x2
- Target: `x2`
- Expected parents of `x2`: {x1}
- Run directory: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/de68cb1d975d`
- data.csv: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/de68cb1d975d/data.csv`
- bk.aba: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/de68cb1d975d/bk.aba`
- bk.sol.aba: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/de68cb1d975d/bk.sol.aba`
- metrics.json: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/de68cb1d975d/metrics.json`
- Outcome: `solved`
- Recovered body variables: {x0, x1}
- Recovery classification: `parent_superset`
- body-parent P/R/F1: 0.500 / 1.000 / 0.667
- Python coverage (acc/pos/neg): 0.750 / 1.000 / 0.500
- Prolog-aware coverage (acc/pos/neg): 0.500 / 0.000 / 1.000
- assumptions / contraries: 1 / 1
- delta rules (5):

```prolog
x2(A) :- alpha_1(A), x0(A).
x2(A) :- x1(A).
c_alpha_1(A) :- x0(A).
assumption(alpha_1(A)).
contrary(alpha_1(A),c_alpha_1(A)) :- assumption(alpha_1(A)).
```

x2 target rules (2):

```prolog
x2(A) :- alpha_1(A), x0(A).
x2(A) :- x1(A).
```

Interpretation notes:

```text

```

### qi001_fork_binary

- Source id: `qi001_fork_binary`
- Motif: fork
- Data mode: binary 0/1
- Graph edges: x0 -> x1, x0 -> x2
- Target: `x2`
- Expected parents of `x2`: {x0}
- Run directory: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/451489acc4f2`
- data.csv: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/451489acc4f2/data.csv`
- bk.aba: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/451489acc4f2/bk.aba`
- bk.sol.aba: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/451489acc4f2/bk.sol.aba`
- metrics.json: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/451489acc4f2/metrics.json`
- Outcome: `solved`
- Recovered body variables: {x0}
- Recovery classification: `exact_parent_recovery`
- body-parent P/R/F1: 1.000 / 1.000 / 1.000
- Python coverage (acc/pos/neg): 1.000 / 1.000 / 1.000
- Prolog-aware coverage (acc/pos/neg): 1.000 / 1.000 / 1.000
- assumptions / contraries: 0 / 0
- delta rules (1):

```prolog
x2(A) :- x0(A).
```

x2 target rules (1):

```prolog
x2(A) :- x0(A).
```

Interpretation notes:

```text

```

### qi001_collider_binary

- Source id: `qi001_collider_binary`
- Motif: collider
- Data mode: binary 0/1
- Graph edges: x0 -> x2, x1 -> x2
- Target: `x2`
- Expected parents of `x2`: {x0, x1}
- Run directory: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/7f5f3debd5c5`
- data.csv: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/7f5f3debd5c5/data.csv`
- bk.aba: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/7f5f3debd5c5/bk.aba`
- bk.sol.aba: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/7f5f3debd5c5/bk.sol.aba`
- metrics.json: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/7f5f3debd5c5/metrics.json`
- Outcome: `solved`
- Recovered body variables: {x0, x1}
- Recovery classification: `exact_parent_recovery`
- body-parent P/R/F1: 1.000 / 1.000 / 1.000
- Python coverage (acc/pos/neg): 1.000 / 1.000 / 1.000
- Prolog-aware coverage (acc/pos/neg): 1.000 / 1.000 / 1.000
- assumptions / contraries: 0 / 0
- delta rules (2):

```prolog
x2(A) :- x1(A).
x2(A) :- x0(A).
```

x2 target rules (2):

```prolog
x2(A) :- x1(A).
x2(A) :- x0(A).
```

Interpretation notes:

```text

```

### qi001_chain_cat3

- Source id: `qi001_chain_cat3`
- Motif: chain
- Data mode: categorical (3 values)
- Graph edges: x0 -> x1, x1 -> x2
- Target: `x2`
- Expected parents of `x2`: {x1}
- Run directory: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/5b4dd6ff5d85`
- data.csv: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/5b4dd6ff5d85/data.csv`
- bk.aba: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/5b4dd6ff5d85/bk.aba`
- bk.sol.aba: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/5b4dd6ff5d85/bk.sol.aba`
- metrics.json: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/5b4dd6ff5d85/metrics.json`
- Outcome: `solved`
- Recovered body variables: {x0}
- Recovery classification: `non_parent_or_proxy`
- body-parent P/R/F1: 0.000 / 0.000 / 0.000
- Python coverage (acc/pos/neg): 0.750 / 1.000 / 0.500
- Prolog-aware coverage (acc/pos/neg): 0.750 / 0.500 / 1.000
- assumptions / contraries: 1 / 1
- delta rules (5):

```prolog
x2(A) :- x0_val_2(A).
x2(A) :- alpha_1(A), x0_val_0(A).
c_alpha_1(A) :- x1_val_0(A).
assumption(alpha_1(A)).
contrary(alpha_1(A),c_alpha_1(A)) :- assumption(alpha_1(A)).
```

x2 target rules (2):

```prolog
x2(A) :- x0_val_2(A).
x2(A) :- alpha_1(A), x0_val_0(A).
```

Interpretation notes:

```text

```

### qi001_fork_cat3

- Source id: `qi001_fork_cat3`
- Motif: fork
- Data mode: categorical (3 values)
- Graph edges: x0 -> x1, x0 -> x2
- Target: `x2`
- Expected parents of `x2`: {x0}
- Run directory: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/f489167a07fe`
- data.csv: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/f489167a07fe/data.csv`
- bk.aba: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/f489167a07fe/bk.aba`
- bk.sol.aba: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/f489167a07fe/bk.sol.aba`
- metrics.json: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/f489167a07fe/metrics.json`
- Outcome: `solved`
- Recovered body variables: {x0}
- Recovery classification: `exact_parent_recovery`
- body-parent P/R/F1: 1.000 / 1.000 / 1.000
- Python coverage (acc/pos/neg): 1.000 / 1.000 / 1.000
- Prolog-aware coverage (acc/pos/neg): 1.000 / 1.000 / 1.000
- assumptions / contraries: 0 / 0
- delta rules (1):

```prolog
x2(A) :- x0_val_2(A).
```

x2 target rules (1):

```prolog
x2(A) :- x0_val_2(A).
```

Interpretation notes:

```text

```

### qi001_collider_cat3

- Source id: `qi001_collider_cat3`
- Motif: collider
- Data mode: categorical (3 values)
- Graph edges: x0 -> x2, x1 -> x2
- Target: `x2`
- Expected parents of `x2`: {x0, x1}
- Run directory: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/86a25857d983`
- data.csv: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/86a25857d983/data.csv`
- bk.aba: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/86a25857d983/bk.aba`
- bk.sol.aba: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/86a25857d983/bk.sol.aba`
- metrics.json: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/86a25857d983/metrics.json`
- Outcome: `solved`
- Recovered body variables: {x0}
- Recovery classification: `parent_subset`
- body-parent P/R/F1: 1.000 / 0.500 / 0.667
- Python coverage (acc/pos/neg): 0.800 / 1.000 / 0.667
- Prolog-aware coverage (acc/pos/neg): 0.600 / 0.000 / 1.000
- assumptions / contraries: 1 / 1
- delta rules (5):

```prolog
x2(A) :- alpha_1(A), x0_val_0(A).
x2(A) :- x0_val_2(A).
c_alpha_1(A) :- x1_val_0(A).
assumption(alpha_1(A)).
contrary(alpha_1(A),c_alpha_1(A)) :- assumption(alpha_1(A)).
```

x2 target rules (2):

```prolog
x2(A) :- alpha_1(A), x0_val_0(A).
x2(A) :- x0_val_2(A).
```

Interpretation notes:

```text

```

### qi001_chain_cont3

- Source id: `qi001_chain_cont3`
- Motif: chain
- Data mode: continuous (3 uniform bins)
- Graph edges: x0 -> x1, x1 -> x2
- Target: `x2`
- Expected parents of `x2`: {x1}
- Run directory: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/f6734b41b746`
- data.csv: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/f6734b41b746/data.csv`
- bk.aba: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/f6734b41b746/bk.aba`
- bk.sol.aba: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/f6734b41b746/bk.sol.aba`
- metrics.json: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/f6734b41b746/metrics.json`
- Outcome: `solved`
- Recovered body variables: {x0}
- Recovery classification: `non_parent_or_proxy`
- body-parent P/R/F1: 0.000 / 0.000 / 0.000
- Python coverage (acc/pos/neg): 1.000 / 1.000 / 1.000
- Prolog-aware coverage (acc/pos/neg): 1.000 / 1.000 / 1.000
- assumptions / contraries: 0 / 0
- delta rules (2):

```prolog
x2(A) :- x0_bin1(A).
x2(A) :- x0_bin2(A).
```

x2 target rules (2):

```prolog
x2(A) :- x0_bin1(A).
x2(A) :- x0_bin2(A).
```

Interpretation notes:

```text

```

### qi001_fork_cont3

- Source id: `qi001_fork_cont3`
- Motif: fork
- Data mode: continuous (3 uniform bins)
- Graph edges: x0 -> x1, x0 -> x2
- Target: `x2`
- Expected parents of `x2`: {x0}
- Run directory: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/e72376c9b2d9`
- data.csv: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/e72376c9b2d9/data.csv`
- bk.aba: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/e72376c9b2d9/bk.aba`
- bk.sol.aba: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/e72376c9b2d9/bk.sol.aba`
- metrics.json: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/e72376c9b2d9/metrics.json`
- Outcome: `solved`
- Recovered body variables: {x0}
- Recovery classification: `exact_parent_recovery`
- body-parent P/R/F1: 1.000 / 1.000 / 1.000
- Python coverage (acc/pos/neg): 1.000 / 1.000 / 1.000
- Prolog-aware coverage (acc/pos/neg): 1.000 / 1.000 / 1.000
- assumptions / contraries: 0 / 0
- delta rules (2):

```prolog
x2(A) :- x0_bin1(A).
x2(A) :- x0_bin2(A).
```

x2 target rules (2):

```prolog
x2(A) :- x0_bin1(A).
x2(A) :- x0_bin2(A).
```

Interpretation notes:

```text

```

### qi001_collider_cont3

- Source id: `qi001_collider_cont3`
- Motif: collider
- Data mode: continuous (3 uniform bins)
- Graph edges: x0 -> x2, x1 -> x2
- Target: `x2`
- Expected parents of `x2`: {x0, x1}
- Run directory: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/d8586dce641b`
- data.csv: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/d8586dce641b/data.csv`
- bk.aba: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/d8586dce641b/bk.aba`
- bk.sol.aba: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/d8586dce641b/bk.sol.aba`
- metrics.json: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/d8586dce641b/metrics.json`
- Outcome: `solved`
- Recovered body variables: {x0}
- Recovery classification: `parent_subset`
- body-parent P/R/F1: 1.000 / 0.500 / 0.667
- Python coverage (acc/pos/neg): 0.800 / 1.000 / 0.500
- Prolog-aware coverage (acc/pos/neg): 0.400 / 0.000 / 1.000
- assumptions / contraries: 1 / 1
- delta rules (5):

```prolog
x2(A) :- alpha_1(A), x0_bin0(A).
x2(A) :- x0_bin2(A).
c_alpha_1(A) :- x1_bin0(A).
assumption(alpha_1(A)).
contrary(alpha_1(A),c_alpha_1(A)) :- assumption(alpha_1(A)).
```

x2 target rules (2):

```prolog
x2(A) :- alpha_1(A), x0_bin0(A).
x2(A) :- x0_bin2(A).
```

Interpretation notes:

```text

```
