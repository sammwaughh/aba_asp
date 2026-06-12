# Motif recovery summary: QI003_scaled_motifs

Generated artefact-collecting summary. Do not edit by hand; regenerate with `causal/scripts/motif_recovery_summary.py`.

Scope: parent-set recovery via ABA Learning. NOT Russo-style Causal ABA (no graph recovery, d-separation, or stable-extension-as-DAG claims). Expected parents are derived from each fixture's ground-truth edges, so parent-position variants are handled correctly. `body_parent_f1` is intentionally omitted (see METRICS.md).

- Experiment: `QI003_scaled_motifs`
- Config: `causal/configs/experiments/QI003_scaled_motifs.yaml`
- Output root: `causal/outputs/aba_learning/grid/QI003_scaled_motifs`
- Status: pending run (no grid artefacts found)
- Cells: 15
- Generated at: 2026-06-12T08:02:45.719784+00:00

Recovery classifications: `exact_parent_recovery`, `parent_subset`, `parent_superset`, `non_parent_or_proxy`, `mixed_parent_and_non_parent`, `rote_or_sample_specific`, `no_solution`, `no_output_yet`, `parser_or_metric_failure`.
## Aggregate (clean_recovery over cells with metrics)

No cells with metrics yet.

## Cells

### qi003_chain_x1parent_binary

- Source id: `qi003_chain_x1parent_binary`
- Data mode: binary 0/1
- Graph edges: x0 -> x1, x1 -> x2
- Expected parents of `x2` (from edges): {x1}
- Rows: 100
- Positive examples: `x2(1)`, `x2(2)`, `x2(6)`, `x2(7)`, `x2(12)`, `x2(13)`, `x2(14)`, `x2(15)`, `x2(16)`, `x2(17)`, `x2(18)`, `x2(19)`, ... (54 total)
- Negative examples: `x2(3)`, `x2(4)`, `x2(5)`, `x2(8)`, `x2(9)`, `x2(10)`, `x2(11)`, `x2(21)`, `x2(25)`, `x2(30)`, `x2(33)`, `x2(34)`, ... (46 total)
- Run status: pending (run_id `413ae4372b86`)

### qi003_chain_x1parent_cat3

- Source id: `qi003_chain_x1parent_cat3`
- Data mode: categorical (3 values)
- Graph edges: x0 -> x1, x1 -> x2
- Expected parents of `x2` (from edges): {x1}
- Rows: 100
- Positive examples: `x2(3)`, `x2(5)`, `x2(6)`, `x2(16)`, `x2(18)`, `x2(32)`, `x2(34)`, `x2(37)`, `x2(38)`, `x2(42)`, `x2(44)`, `x2(52)`, ... (21 total)
- Negative examples: `x2(1)`, `x2(2)`, `x2(4)`, `x2(7)`, `x2(8)`, `x2(9)`, `x2(10)`, `x2(11)`, `x2(12)`, `x2(13)`, `x2(14)`, `x2(15)`, ... (79 total)
- Run status: pending (run_id `4ff9f50c6f50`)

### qi003_chain_x1parent_cont3

- Source id: `qi003_chain_x1parent_cont3`
- Data mode: continuous (3 uniform bins)
- Graph edges: x0 -> x1, x1 -> x2
- Expected parents of `x2` (from edges): {x1}
- Rows: 100
- Positive examples: `x2(4)`, `x2(6)`, `x2(7)`, `x2(8)`, `x2(10)`, `x2(11)`, `x2(13)`, `x2(15)`, `x2(16)`, `x2(21)`, `x2(22)`, `x2(23)`, ... (43 total)
- Negative examples: `x2(1)`, `x2(2)`, `x2(3)`, `x2(5)`, `x2(9)`, `x2(12)`, `x2(14)`, `x2(17)`, `x2(18)`, `x2(19)`, `x2(20)`, `x2(25)`, ... (57 total)
- Run status: pending (run_id `d4c032146d50`)

### qi003_chain_x0parent_binary

- Source id: `qi003_chain_x0parent_binary`
- Data mode: binary 0/1
- Graph edges: x1 -> x0, x0 -> x2
- Expected parents of `x2` (from edges): {x0}
- Rows: 100
- Positive examples: `x2(1)`, `x2(5)`, `x2(9)`, `x2(13)`, `x2(15)`, `x2(16)`, `x2(17)`, `x2(19)`, `x2(20)`, `x2(21)`, `x2(24)`, `x2(25)`, ... (55 total)
- Negative examples: `x2(2)`, `x2(3)`, `x2(4)`, `x2(6)`, `x2(7)`, `x2(8)`, `x2(10)`, `x2(11)`, `x2(12)`, `x2(14)`, `x2(18)`, `x2(22)`, ... (45 total)
- Run status: pending (run_id `518a3ac1d56c`)

### qi003_chain_x0parent_cat3

- Source id: `qi003_chain_x0parent_cat3`
- Data mode: categorical (3 values)
- Graph edges: x1 -> x0, x0 -> x2
- Expected parents of `x2` (from edges): {x0}
- Rows: 100
- Positive examples: `x2(1)`, `x2(4)`, `x2(7)`, `x2(8)`, `x2(9)`, `x2(10)`, `x2(18)`, `x2(22)`, `x2(24)`, `x2(28)`, `x2(31)`, `x2(32)`, ... (32 total)
- Negative examples: `x2(2)`, `x2(3)`, `x2(5)`, `x2(6)`, `x2(11)`, `x2(12)`, `x2(13)`, `x2(14)`, `x2(15)`, `x2(16)`, `x2(17)`, `x2(19)`, ... (68 total)
- Run status: pending (run_id `b12230cc818f`)

### qi003_chain_x0parent_cont3

- Source id: `qi003_chain_x0parent_cont3`
- Data mode: continuous (3 uniform bins)
- Graph edges: x1 -> x0, x0 -> x2
- Expected parents of `x2` (from edges): {x0}
- Rows: 100
- Positive examples: `x2(1)`, `x2(2)`, `x2(4)`, `x2(6)`, `x2(10)`, `x2(14)`, `x2(17)`, `x2(21)`, `x2(22)`, `x2(24)`, `x2(25)`, `x2(26)`, ... (42 total)
- Negative examples: `x2(3)`, `x2(5)`, `x2(7)`, `x2(8)`, `x2(9)`, `x2(11)`, `x2(12)`, `x2(13)`, `x2(15)`, `x2(16)`, `x2(18)`, `x2(19)`, ... (58 total)
- Run status: pending (run_id `30d084a673e6`)

### qi003_fork_x0parent_binary

- Source id: `qi003_fork_x0parent_binary`
- Data mode: binary 0/1
- Graph edges: x0 -> x1, x0 -> x2
- Expected parents of `x2` (from edges): {x0}
- Rows: 100
- Positive examples: `x2(1)`, `x2(4)`, `x2(6)`, `x2(9)`, `x2(10)`, `x2(11)`, `x2(12)`, `x2(14)`, `x2(20)`, `x2(22)`, `x2(24)`, `x2(25)`, ... (48 total)
- Negative examples: `x2(2)`, `x2(3)`, `x2(5)`, `x2(7)`, `x2(8)`, `x2(13)`, `x2(15)`, `x2(16)`, `x2(17)`, `x2(18)`, `x2(19)`, `x2(21)`, ... (52 total)
- Run status: pending (run_id `789b09aae301`)

### qi003_fork_x0parent_cat3

- Source id: `qi003_fork_x0parent_cat3`
- Data mode: categorical (3 values)
- Graph edges: x0 -> x1, x0 -> x2
- Expected parents of `x2` (from edges): {x0}
- Rows: 100
- Positive examples: `x2(2)`, `x2(3)`, `x2(4)`, `x2(5)`, `x2(14)`, `x2(20)`, `x2(23)`, `x2(27)`, `x2(28)`, `x2(33)`, `x2(34)`, `x2(35)`, ... (37 total)
- Negative examples: `x2(1)`, `x2(6)`, `x2(7)`, `x2(8)`, `x2(9)`, `x2(10)`, `x2(11)`, `x2(12)`, `x2(13)`, `x2(15)`, `x2(16)`, `x2(17)`, ... (63 total)
- Run status: pending (run_id `97b198cf06b8`)

### qi003_fork_x0parent_cont3

- Source id: `qi003_fork_x0parent_cont3`
- Data mode: continuous (3 uniform bins)
- Graph edges: x0 -> x1, x0 -> x2
- Expected parents of `x2` (from edges): {x0}
- Rows: 100
- Positive examples: `x2(1)`, `x2(5)`, `x2(7)`, `x2(10)`, `x2(11)`, `x2(13)`, `x2(16)`, `x2(17)`, `x2(19)`, `x2(21)`, `x2(22)`, `x2(23)`, ... (54 total)
- Negative examples: `x2(2)`, `x2(3)`, `x2(4)`, `x2(6)`, `x2(8)`, `x2(9)`, `x2(12)`, `x2(14)`, `x2(15)`, `x2(18)`, `x2(20)`, `x2(26)`, ... (46 total)
- Run status: pending (run_id `73fe43f69667`)

### qi003_fork_x1parent_binary

- Source id: `qi003_fork_x1parent_binary`
- Data mode: binary 0/1
- Graph edges: x1 -> x0, x1 -> x2
- Expected parents of `x2` (from edges): {x1}
- Rows: 100
- Positive examples: `x2(1)`, `x2(2)`, `x2(4)`, `x2(6)`, `x2(7)`, `x2(8)`, `x2(9)`, `x2(10)`, `x2(12)`, `x2(13)`, `x2(15)`, `x2(16)`, ... (59 total)
- Negative examples: `x2(3)`, `x2(5)`, `x2(11)`, `x2(14)`, `x2(20)`, `x2(21)`, `x2(22)`, `x2(25)`, `x2(27)`, `x2(28)`, `x2(30)`, `x2(32)`, ... (41 total)
- Run status: pending (run_id `97ef40a230b7`)

### qi003_fork_x1parent_cat3

- Source id: `qi003_fork_x1parent_cat3`
- Data mode: categorical (3 values)
- Graph edges: x1 -> x0, x1 -> x2
- Expected parents of `x2` (from edges): {x1}
- Rows: 100
- Positive examples: `x2(5)`, `x2(7)`, `x2(9)`, `x2(10)`, `x2(22)`, `x2(23)`, `x2(24)`, `x2(27)`, `x2(32)`, `x2(34)`, `x2(35)`, `x2(37)`, ... (32 total)
- Negative examples: `x2(1)`, `x2(2)`, `x2(3)`, `x2(4)`, `x2(6)`, `x2(8)`, `x2(11)`, `x2(12)`, `x2(13)`, `x2(14)`, `x2(15)`, `x2(16)`, ... (68 total)
- Run status: pending (run_id `e07750682717`)

### qi003_fork_x1parent_cont3

- Source id: `qi003_fork_x1parent_cont3`
- Data mode: continuous (3 uniform bins)
- Graph edges: x1 -> x0, x1 -> x2
- Expected parents of `x2` (from edges): {x1}
- Rows: 100
- Positive examples: `x2(1)`, `x2(2)`, `x2(3)`, `x2(7)`, `x2(10)`, `x2(13)`, `x2(14)`, `x2(16)`, `x2(17)`, `x2(18)`, `x2(19)`, `x2(20)`, ... (53 total)
- Negative examples: `x2(4)`, `x2(5)`, `x2(6)`, `x2(8)`, `x2(9)`, `x2(11)`, `x2(12)`, `x2(15)`, `x2(22)`, `x2(23)`, `x2(24)`, `x2(29)`, ... (47 total)
- Run status: pending (run_id `72bad731e7c2`)

### qi003_collider_binary

- Source id: `qi003_collider_binary`
- Data mode: binary 0/1
- Graph edges: x0 -> x2, x1 -> x2
- Expected parents of `x2` (from edges): {x0, x1}
- Rows: 100
- Positive examples: `x2(2)`, `x2(3)`, `x2(4)`, `x2(6)`, `x2(7)`, `x2(8)`, `x2(9)`, `x2(10)`, `x2(11)`, `x2(12)`, `x2(15)`, `x2(16)`, ... (72 total)
- Negative examples: `x2(1)`, `x2(5)`, `x2(13)`, `x2(14)`, `x2(17)`, `x2(24)`, `x2(30)`, `x2(31)`, `x2(32)`, `x2(37)`, `x2(38)`, `x2(40)`, ... (28 total)
- Run status: pending (run_id `cf0caac01986`)

### qi003_collider_cat3

- Source id: `qi003_collider_cat3`
- Data mode: categorical (3 values)
- Graph edges: x0 -> x2, x1 -> x2
- Expected parents of `x2` (from edges): {x0, x1}
- Rows: 100
- Positive examples: `x2(1)`, `x2(3)`, `x2(4)`, `x2(6)`, `x2(7)`, `x2(11)`, `x2(14)`, `x2(16)`, `x2(18)`, `x2(22)`, `x2(24)`, `x2(26)`, ... (46 total)
- Negative examples: `x2(2)`, `x2(5)`, `x2(8)`, `x2(9)`, `x2(10)`, `x2(12)`, `x2(13)`, `x2(15)`, `x2(17)`, `x2(19)`, `x2(20)`, `x2(21)`, ... (54 total)
- Run status: pending (run_id `36b91f525fef`)

### qi003_collider_cont3

- Source id: `qi003_collider_cont3`
- Data mode: continuous (3 uniform bins)
- Graph edges: x0 -> x2, x1 -> x2
- Expected parents of `x2` (from edges): {x0, x1}
- Rows: 100
- Positive examples: `x2(1)`, `x2(3)`, `x2(5)`, `x2(7)`, `x2(8)`, `x2(10)`, `x2(11)`, `x2(12)`, `x2(14)`, `x2(16)`, `x2(17)`, `x2(19)`, ... (49 total)
- Negative examples: `x2(2)`, `x2(4)`, `x2(6)`, `x2(9)`, `x2(13)`, `x2(15)`, `x2(18)`, `x2(20)`, `x2(21)`, `x2(24)`, `x2(26)`, `x2(27)`, ... (51 total)
- Run status: pending (run_id `8152eaf76aa2`)
