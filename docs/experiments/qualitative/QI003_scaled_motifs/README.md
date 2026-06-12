# QI-003 — operational dossier (QI003_scaled_motifs)

> QI-003 is a scaled, confound-controlled parent-set recovery investigation using the current ABA Learning bridge. It is not full Russo-style Causal ABA, graph recovery, d-separation reasoning, or stable-extension-as-DAG machinery.

## Related documents

- `../QI-003.md` — high-level experiment record.
- `README.md` (this file) — operational dossier.
- `../QI003_scaled_motifs_summary.md` — generated per-cell summary (motif_recovery_summary.py).
- `run_log.md` — factual run log (pending the ABA Learning run).
- `interpretation.md` — human interpretation template (pending).
- `artefacts.md` — artefact map.
- `metrics.md` — metrics used and what each measures (headline: clean_recovery + variable-level P/R/Jaccard; plus continuous bin-health).
- `decision_record.md` — status + acceptance/rerun criteria (incl. the x0parent/x1parent confound check).

## Investigation question

With `n=100` noisy samples per cell, and the true direct parent of `x2` placed in either column, does the current ABA Learning bridge recover the true parent(s) of `x2` *regardless of column position*, across binary, categorical-3, and continuous-3 data modes?

## Why scaled + noisy

QI-002 establishes whether the perfect rule is learnable in the ideal noiseless case. QI-003 asks the more realistic question: with `n=100` and mild noise, do learners still pick out the causal parent? Noise also breaks the QI-001 chain degeneracy where `x0` and `x1` were identical (parent vs ancestor undecidable).

## Why parent-position controls (the confound fix)

In QI-001 the true parent coincided with the first column for fork and opposed it for chain, so "found the cause" and "preferred x0" made identical predictions — an unbroken confound. QI-003 generates BOTH orientations for chain and fork, placing the true parent in `x0` for some cells and `x1` for others. A learner that simply prefers `x0` will fail the `*_x1parent` cells. The decision-critical comparison is `*_x1parent` vs `*_x0parent`.

## Scope

- In scope: per-cell learned `x2` rules, recovered body variables vs encoded parents, variable-level metrics + `clean_recovery`, and the position-controlled confound check.
- Out of scope: DAG discovery, edge orientation, d-separation, stable-extension-as-DAG.

## Parent-position tracking table

5 structural configs x 3 data modes = 15 cells. Edges are 0-based; `(s,t)` means `xs -> xt`.

| Fixture base | Motif | Edges | Parent column | Ancestor/sibling column | Parents(x2) | Mechanism | Noise |
|---|---|---|---|---|---|---|---|
| `qi003_chain_x1parent` | chain | (0,1),(1,2) | `x1` (mid) | `x0` (root) | {x1} | root->mid->x2 | mid-flip ~0.2; target ~0.1/Gauss |
| `qi003_chain_x0parent` | chain | (1,0),(0,2) | `x0` (mid) | `x1` (root) | {x0} | root->mid->x2 | mid-flip ~0.2; target ~0.1/Gauss |
| `qi003_fork_x0parent` | fork | (0,1),(0,2) | `x0` (cause) | `x1` (sibling) | {x0} | cause->{x2, sibling} | sibling ~0.2; target ~0.1/Gauss |
| `qi003_fork_x1parent` | fork | (1,0),(1,2) | `x1` (cause) | `x0` (sibling) | {x1} | cause->{x2, sibling} | sibling ~0.2; target ~0.1/Gauss |
| `qi003_collider` | collider | (0,2),(1,2) | `x0` and `x1` | — | {x0, x1} | x2 = OR/max/sum of parents | target ~0.1/Gauss |

Each base is instantiated in three modes (`_binary`, `_cat3`, `_cont3`), e.g. `qi003_chain_x1parent_cont3`. All cells: `n=100`; deterministic per-fixture internal RNG seed.

## Data modes

```text
binary 0/1                              -> bare predicates x0(A)
categorical with exactly 3 values       -> value predicates x0_val_v(A)
continuous, 3 uniform bins (n=100)       -> bin predicates x0_binK(A)
```

Positive class: `x2 == 1` (binary), `x2 == 2` (cat3), `x2 >= 0` (cont3).

## Key paths

| Item | Path |
|---|---|
| Config | `causal/configs/experiments/QI003_scaled_motifs.yaml` |
| Fixtures | `causal/experiments/handcrafted_qi003.py` |
| Fixture registration | `causal/experiments/handcrafted.py` |
| Summary script | `causal/scripts/motif_recovery_summary.py` |
| Generated summary | `docs/experiments/qualitative/QI003_scaled_motifs_summary.md` |
| Expected output directory | `causal/outputs/aba_learning/grid/QI003_scaled_motifs/` |

## Status

Fixtures, config, tests, and the generalized summary script are in place. The ABA Learning run is pending. See `run_log.md` and `interpretation.md`.
