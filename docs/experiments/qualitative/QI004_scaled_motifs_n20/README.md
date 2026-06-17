# QI-004 — operational dossier (QI004_scaled_motifs_n20)

> QI-004 is the computationally feasible follow-up to QI-003: a scaled, confound-controlled parent-set recovery investigation using the current `aba_asp/causal` implementation (target-wise ABA Learning pipeline) at `n=20` with `prolog_timeout_s=300`. It is not full Russo-style Causal ABA, graph recovery, d-separation reasoning, or stable-extension-as-DAG machinery.

## Why QI-004 supersedes QI-003 for evidence

QI-003's `n=100` run was computationally infeasible under the 120s Prolog timeout budget (cat3/cont3 timed out; binary hit the all-zero-positive encoding limitation; 0 cells solved before manual abort — see the QI-003 record `../QI-003.md` and the partial outputs in `causal/outputs/aba_learning/grid/QI003_scaled_motifs/`). QI-004 keeps the identical conceptual design but reduces `n` to 20 and raises the timeout to 300s. QI-003 is preserved unchanged as a recorded feasibility attempt.

## Related documents

- `../QI-004.md` — high-level experiment record.
- `README.md` (this file) — operational dossier.
- `../QI004_scaled_motifs_n20_summary.md` — generated per-cell summary (motif_recovery_summary.py).
- `run_log.md` — factual run log.
- `interpretation.md` — human interpretation template.
- `artefacts.md` — artefact map.
- `metrics.md` — metrics used and what each measures (headline: clean_recovery + variable-level P/R/Jaccard; plus continuous bin-health).
- `decision_record.md` — status + acceptance/rerun criteria (incl. the x0parent/x1parent confound check).

## Investigation question

With `n=20` noisy samples per cell, and the true direct parent of `x2` placed in either column, does the current `aba_asp/causal` implementation recover the true parent(s) of `x2` *regardless of column position*, across binary, categorical-3, and continuous-3 data modes?

## Why scaled + noisy (and why n=20 rather than 100)

QI-002 establishes whether the perfect rule is learnable in the ideal noiseless case. QI-003/QI-004 ask the more realistic question: with noise, do learners still pick out the causal parent? Noise also breaks the QI-001 chain degeneracy where `x0` and `x1` were identical. QI-004 uses `n=20` because the learner did not complete within the timeout budget at `n=100`; 20 noisy samples still populate all data-mode vocabularies (verified pre-run) while keeping the Prolog search tractable.

## Why parent-position controls (the confound fix)

In QI-001 the true parent coincided with the first column for fork and opposed it for chain, so "found the cause" and "preferred x0" made identical predictions — an unbroken confound. QI-004 (like QI-003) generates BOTH orientations for chain and fork, placing the true parent in `x0` for some cells and `x1` for others. A learner that simply prefers `x0` will fail the `*_x1parent` cells. The decision-critical comparison is `*_x1parent` vs `*_x0parent`.

## Scope

- In scope: per-cell learned `x2` rules, recovered body variables vs encoded parents, variable-level metrics + `clean_recovery`, and the position-controlled confound check.
- Out of scope: DAG discovery, edge orientation, d-separation, stable-extension-as-DAG.

## Parent-position tracking table

5 structural configs x 3 data modes = 15 cells. Edges are 0-based; `(s,t)` means `xs -> xt`.

| Fixture base | Motif | Edges | Parent column | Ancestor/sibling column | Parents(x2) | Mechanism | Noise |
|---|---|---|---|---|---|---|---|
| `qi004_chain_x1parent` | chain | (0,1),(1,2) | `x1` (mid) | `x0` (root) | {x1} | root->mid->x2 | mid-flip ~0.2; target ~0.1/Gauss |
| `qi004_chain_x0parent` | chain | (1,0),(0,2) | `x0` (mid) | `x1` (root) | {x0} | root->mid->x2 | mid-flip ~0.2; target ~0.1/Gauss |
| `qi004_fork_x0parent` | fork | (0,1),(0,2) | `x0` (cause) | `x1` (sibling) | {x0} | cause->{x2, sibling} | sibling ~0.2; target ~0.1/Gauss |
| `qi004_fork_x1parent` | fork | (1,0),(1,2) | `x1` (cause) | `x0` (sibling) | {x1} | cause->{x2, sibling} | sibling ~0.2; target ~0.1/Gauss |
| `qi004_collider` | collider | (0,2),(1,2) | `x0` and `x1` | — | {x0, x1} | x2 = OR/max/sum of parents | target ~0.1/Gauss |

Each base is instantiated in three modes (`_binary`, `_cat3`, `_cont3`), e.g. `qi004_chain_x1parent_cont3`. All cells: `n=20`; deterministic per-fixture internal RNG seed.

## Data modes

```text
binary 0/1                              -> bare predicates x0(A)
categorical with exactly 3 values       -> value predicates x0_val_v(A)
continuous, 3 uniform bins (n=20)        -> bin predicates x0_binK(A)
```

Positive class: `x2 == 1` (binary), `x2 == 2` (cat3), `x2 >= 0` (cont3).

## Key paths

| Item | Path |
|---|---|
| Config | `causal/configs/experiments/QI004_scaled_motifs_n20.yaml` |
| Fixtures | `causal/experiments/handcrafted_qi004.py` |
| Fixture registration | `causal/experiments/handcrafted.py` |
| Summary script | `causal/scripts/motif_recovery_summary.py` |
| Generated summary | `docs/experiments/qualitative/QI004_scaled_motifs_n20_summary.md` |
| Output directory | `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20/` |

## Status

Fixtures, config, tests, and the generalized summary script are in place. The ABA Learning run and audit are performed by this task; see `run_log.md` and `decision_record.md`.
