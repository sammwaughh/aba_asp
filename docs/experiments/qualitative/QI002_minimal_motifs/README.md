# QI-002 — operational dossier (QI002_minimal_motifs)

> QI-002 is a minimal-baseline parent-set recovery investigation using the current ABA Learning bridge. It is not full Russo-style Causal ABA, graph recovery, d-separation reasoning, or stable-extension-as-DAG machinery.

## Related documents

- `../QI-002.md` — high-level experiment record.
- `README.md` (this file) — operational dossier.
- `../QI002_minimal_motifs_summary.md` — generated per-cell summary (motif_recovery_summary.py).
- `run_log.md` — factual run log (pending the ABA Learning run).
- `interpretation.md` — human interpretation template (pending).
- `artefacts.md` — artefact map.
- `metrics.md` — metrics used and what each measures (headline: clean_recovery + variable-level P/R/Jaccard).
- `decision_record.md` — status + acceptance/rerun criteria.

## Investigation question

On *complete, noiseless truth tables* for three 3-node motifs, where the true parent of `x2` is the unique zero-error separator of the positive class, does the current ABA Learning bridge learn a target rule for `x2` whose body variables equal the true direct parents?

## Why minimal, and why these sizes (size derivation)

A table can force the parent rule only if (1) the parent perfectly separates E+/E-, and (2) every non-parent fails to. The smallest design guaranteeing this is the **complete factorial** over the two candidate predictors, repeated so a single row cannot be a fluke:

- 2 binary predictors -> `2^2 = 4` combinations -> repeated x2 -> **8 rows**;
- 2 ternary predictors -> `3^2 = 9` combinations -> repeated x2 -> **18 rows**.

This is the principled replacement for QI-001's unjustified 4-5 row tables. With the full truth table present and a noiseless target, the true parent is the *only* perfect single-column rule (collider needs both parents), so a genuine causal rule is learnable in principle.

## Scope

- In scope: per-cell learned `x2` rules, their body variables vs the encoded parents, and the new variable-level metrics + `clean_recovery`.
- Out of scope: DAG discovery, edge orientation, d-separation, stable-extension-as-DAG.
- Confound treatment: the complete factorial decorrelates non-parents from `x2` (true parent = unique perfect separator), which is a principled **data-level** correction against the QI-001 x0/first-column confound and makes the canonical **chain** cell (where `x0 ⊥ x2`) a genuine probe of any residual positional x0-preference. QI-002 does **not** provide the full *symmetric* break — the fork cell's parent is `x0` (bias and recovery coincide), and there is no within-structure parent-position swap; that symmetric/empirical break is QI-003/QI-004's job. See `QI-002.md` → "Confound treatment (corrected framing)".

## Matrix

```text
3 motifs x 2 data modes x target x2 = 6 cells
chain:    x0 -> x1 -> x2          parents(x2) = {x1}
fork:     x0 -> x1, x0 -> x2      parents(x2) = {x0}
collider: x0 -> x2, x1 -> x2      parents(x2) = {x0, x1}
```

| Cell | Motif | Data mode | Rows | Expected parents |
|---|---|---|---|---|
| `qi002_chain_binary` | chain | binary 0/1 | 8 | {x1} |
| `qi002_fork_binary` | fork | binary 0/1 | 8 | {x0} |
| `qi002_collider_binary` | collider | binary 0/1 | 8 | {x0, x1} |
| `qi002_chain_cat3` | chain | categorical (3) | 18 | {x1} |
| `qi002_fork_cat3` | fork | categorical (3) | 18 | {x0} |
| `qi002_collider_cat3` | collider | categorical (3) | 18 | {x0, x1} |

## Key paths

| Item | Path |
|---|---|
| Config | `causal/configs/experiments/QI002_minimal_motifs.yaml` |
| Fixtures | `causal/experiments/handcrafted_qi002.py` |
| Fixture registration | `causal/experiments/handcrafted.py` |
| Summary script | `causal/scripts/motif_recovery_summary.py` |
| Generated summary | `docs/experiments/qualitative/QI002_minimal_motifs_summary.md` |
| Expected output directory | `causal/outputs/aba_learning/grid/QI002_minimal_motifs/` |

## Status

Fixtures, config, tests, and the generalized summary script are in place. The ABA Learning run is pending. See `run_log.md` and `interpretation.md`.
