# QI-001 — operational investigation dossier (QI001_motifs_modes)

> QI-001 is a qualitative parent-set recovery investigation using the current ABA Learning bridge. It is not full Russo-style Causal ABA, graph recovery, d-separation reasoning, or stable-extension-as-DAG machinery.

## Related documents

- `../QI-001.md` — high-level experiment record (the human-written investigation account).
- `README.md` (this file) — operational investigation dossier.
- `../QI-001_summary.md` — generated per-cell summary produced by the summary script.
- `run_log.md` — factual run log (pending until the ABALearn run).
- `interpretation.md` — human interpretation template (pending; filled after results are reviewed).
- `artefacts.md` — artefact map for the run outputs.

## Investigation question

When tabular data is generated from three canonical 3-node causal motifs and the current `aba_asp/causal` bridge learns target rules for `x2` target-by-target, do the learned rule bodies for `x2` recover the encoded direct parents of `x2`, and how does this behaviour change across binary, 3-valued categorical, and continuous (3-bin) data representations?

## Scope

- In scope: per-cell learned target rules for `x2`, the body variables they cite mapped back to base variables, and whether those base variables coincide with the encoded parents of `x2`.
- Out of scope: discovery of the full DAG, edge orientation guarantees, independence/d-separation testing, and any stable-extension-as-DAG interpretation.

This is parent-set recovery via ABA Learning. The motif names (chain/fork/collider) describe the data-generating structure encoded in each fixture table, not an ABA causal encoding.

## Why this is qualitative

The point is to inspect what the learner actually produces on small, fully controlled cases: the exact learned rule bodies, whether they cite true parents versus non-parent predictive associations, and the failure modes. Aggregate metrics alone can hide whether a learned body recovers parents, ancestors, or proxies, so each of the 9 cells is narrated individually.

## Why binary / categorical / continuous are compared

Holding the motif fixed while varying only the data representation isolates the effect of the BK encoding on what is recovered:

- binary 0/1 → bare predicates such as `x0(A)`;
- categorical with exactly 3 values → value predicates such as `x0_val_2(A)`;
- continuous, binned into 3 uniform bins → bin predicates such as `x0_bin2(A)`.

Comparing the three modes shows whether parent-set recovery is robust to the predicate vocabulary or sensitive to it.

## Planned matrix

```text
3 motifs x 3 data modes x target x2 = 9 cells
```

Motifs (0-based node indices; edge `(s, t)` means `xs -> xt`):

```text
chain:    x0 -> x1 -> x2          expected parents of x2: {x1}
fork:     x0 -> x1, x0 -> x2      expected parents of x2: {x0}
collider: x0 -> x2, x1 -> x2      expected parents of x2: {x0, x1}
```

Data modes:

```text
binary 0/1
categorical with exactly 3 values
continuous, binned into 3 bins using uniform binning
```

Target: `x2` only (no target expansion).

Cells (fixture source ids):

| Cell | Motif | Data mode | Expected parents of x2 |
|---|---|---|---|
| `qi001_chain_binary` | chain | binary 0/1 | {x1} |
| `qi001_fork_binary` | fork | binary 0/1 | {x0} |
| `qi001_collider_binary` | collider | binary 0/1 | {x0, x1} |
| `qi001_chain_cat3` | chain | categorical (3 values) | {x1} |
| `qi001_fork_cat3` | fork | categorical (3 values) | {x0} |
| `qi001_collider_cat3` | collider | categorical (3 values) | {x0, x1} |
| `qi001_chain_cont3` | chain | continuous (3 uniform bins) | {x1} |
| `qi001_fork_cont3` | fork | continuous (3 uniform bins) | {x0} |
| `qi001_collider_cont3` | collider | continuous (3 uniform bins) | {x0, x1} |

## Key paths

| Item | Path |
|---|---|
| Config | `causal/configs/experiments/QI001_motifs_modes.yaml` |
| Fixtures | `causal/experiments/handcrafted_qi001.py` |
| Fixture registration | `causal/experiments/handcrafted.py` |
| Summary script | `causal/scripts/qi001_qualitative_summary.py` |
| Generated summary | `docs/experiments/qualitative/QI-001_summary.md` |
| Expected output directory | `causal/outputs/aba_learning/grid/QI001_motifs_modes/` |

## Status

Stage 1 (fixtures, config, tests) and the summary script are in place. The ABALearn run is pending. See `run_log.md` for the factual command log and `interpretation.md` for the per-cell interpretation template.
