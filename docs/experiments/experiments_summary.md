# Experiment Index

## Purpose

This file is the repo-side index of experiments for the Causal ABA Learning project.

Each experiment should have a dedicated record under `docs/experiments/`, using `docs/experiments/TEMPLATE.md`.

This index is not a substitute for the detailed experiment records. It is an at-a-glance view of status, artefacts, and report relevance.

## Report-label mapping

The report (`docs/report/manuscript/`) refers to the qualitative experiments as QL1/QL2/QL3, which map to repo ids QI-001/QI-002/QI-004. The earlier n=100 scaled attempt was cut and is not part of the canonical experiment set; only the reduced n=20 study is canonical and is QL3.

## Status categories

Use the same status categories as `experiment_register.md`.

| Status | Meaning |
|---|---|
| `proposed` | Idea noted; not yet designed in full. |
| `planned` | Design agreed: question, setup, metrics, and interpretation rule are specified. |
| `implemented` | Code/config/docs are in place, but the experiment has not yet been run. |
| `run` | Experiment executed and raw artefacts produced. |
| `analysed` | Results interpreted against the interpretation rule. |
| `reported` | Written into the interim/final report. |

## Experiment table

| ID | Report label | Title | Status | Experiment record | Config(s) | Artefacts | Report relevance | Main current conclusion |
|---|---|---|---|---|---|---|---|---|
| QL-001 | — | Qualitative inspection of ABA Learning on minimal causal motifs | realised by QI series | `docs/experiments/QL-001.md` | — | — | Interim Experimentation / Progress | Umbrella proposal carried out by QI-001..QI-004 and their greedy reruns. |
| QI-001 | QL1 | Qualitative parent-set recovery across 3 motifs x 3 data modes | analysed | `docs/experiments/qualitative/QI-001.md` | `causal/configs/experiments/QI001_motifs_modes.yaml` | `causal/outputs/aba_learning/grid/QI001_motifs_modes/` | Interim Experimentation / Progress | 9/9 solved. Fork exact (but x0-confounded); chain often recovers the ancestor x0; collider exact only in binary. Exposes the x0/first-column confound and weak (4–5 row) table design, motivating QI-002. |
| QI-002 | QL2 | Minimal truth-table baseline for x2 parent recovery | analysed | `docs/experiments/qualitative/QI-002.md` | `causal/configs/experiments/QI002_minimal_motifs.yaml` | `causal/outputs/aba_learning/grid/QI002_minimal_motifs/` | Interim Experimentation / Progress | 6 noiseless cells. Binary chain/fork exact; binary collider NO solution (though the conjunctive parent rule exists); cat3 chain recovers non-parent x0; cat3 collider parent-subset. Mean F1 ~ 0.61. Ideal data is not sufficient for reliable recovery. |
| QI-004 | QL3 | Scaled noisy motifs with parent-position controls (n=20) | analysed | `docs/experiments/qualitative/QI-004.md` | `causal/configs/experiments/QI004_scaled_motifs_n20.yaml` | `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20/` | Interim Experimentation / Progress | 15/15 cells, no timeouts: 1 solved (binary chain x1-parent, superset {x0,x1}, F1 0.67), 12 no-solution, 2 binary `unknown constant` errors; 0 exact recoveries. Feasible at n=20 but no robust recovery with the arbitrarily chosen noise; a systematic noise sweep is the follow-up. |
| QI-001 greedy | — | Greedy-folding rerun of QI-001 (3 motifs x 3 modes) | analysed | `docs/experiments/qualitative/QI001_motifs_modes_greedy/` | `causal/configs/experiments/QI001_motifs_modes_greedy.yaml` | `causal/outputs/aba_learning/grid/QI001_motifs_modes_greedy/` | Interim Experimentation / Progress | Only change `folding_mode: greedy`. 9/9 solved; greedy faster and recovers all three colliders cleanly across modes (nd clean only in binary); chain/fork remain supersets. |
| QI-002 greedy | — | Greedy-folding rerun of QI-002 (minimal truth-table baseline) | analysed | `docs/experiments/qualitative/QI002_minimal_motifs_greedy/` | `causal/configs/experiments/QI002_minimal_motifs_greedy.yaml` | `causal/outputs/aba_learning/grid/QI002_minimal_motifs_greedy/` | Interim Experimentation / Progress | Only change `folding_mode: greedy`. 6/6 solved (vs nd 5/6): solves the binary collider nd could not; cat3 collider now exact; clean recovery 3/6 -> 4/6 with one regression (cat3 fork exact -> superset). |
| QI-004 greedy | — | Greedy-folding rerun of QI-004 (scaled noisy n=20) | analysed | `docs/experiments/qualitative/QI004_scaled_motifs_n20_greedy/` | `causal/configs/experiments/QI004_scaled_motifs_n20_greedy.yaml` | `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20_greedy/` | Interim Experimentation / Progress | Only change `folding_mode: greedy`. Same outcomes as nd (1 solved, 12 no-solution, 2 errors; 0/15 clean) but ~120x faster (≈1233 s -> ≈10 s). At noisy n=20 greedy changes only runtime; binary errors persist. |
| QN-001 | — | Comparing ABA Learning strategies on minimal causal motifs | proposed | `docs/experiments/QN-001.md` | TBD | TBD | Interim Experimentation / Progress; Project Plan | Not run; the greedy-vs-nd qualitative handoff motivates a controlled quantitative comparison (repeated seeds, timing methodology). |
| M11 | — | m1.1 Parent-position and representation-order control | run | `docs/experiments/qualitative/M1.1-parent-position.md` | `causal/configs/experiments/M11_parent_position.yaml` | `causal/outputs/aba_learning/grid/M11_parent_position/cells/<dgp>/` (learning); `causal/outputs/m11_parent_position/validation/` (Stage-0) | Interim Experimentation / Progress (Milestone 1) | 8/8 solved. 6/8 exact expected one-literal parent rule (all binary; cat3 B, C). cat3 A/D discrepant (assumption structure; cov_py/cov_pl flag). DGP-named cell dirs (`grid.cell_dir: dgp`). Stage 2/3 pending. |

## Experiment sequence to date and next

### Done: QL1/QL2/QL3 qualitative parent-set recovery (QI-001/QI-002/QI-004)

Status: `analysed`

Inspected what ABA Learning recovers on chain/fork/collider motifs under binary/categorical-3/continuous-binned encodings, target-wise on `x2`, comparing learned body variables against the true parents. Outcome: parent recovery works in selected idealised cases but is not robust across motifs, encodings or modest noisy scaling. The DGP/encoding details are documented in the per-experiment records and the report Experimentation chapter.

### Done: greedy vs non-deterministic folding (qualitative)

Status: `analysed`

Compared `folding_mode: nd` vs `greedy` on identical fixtures (QI-001/QI-002/QI-004 greedy reruns). Greedy is faster (~120x at the QL3 scale), solve rate >= nd, net better clean recovery (colliders), one regression (cat3 fork), no recovery change at the noisy n=20 scale. See `docs/experiments/qualitative/greedy_vs_nd_qualitative_handoff.md`.

### Next: QN-001 controlled strategy comparison

Status: `proposed`

Purpose:

> Confirm the qualitative greedy-vs-nd signals quantitatively (repeated seeds, larger grids, proper timing methodology).

Primary method:

- solve-rate comparison;
- parent-body / variable-level metric comparison;
- efficiency metric comparison (runtime; fold count if inspectable).

Primary risk:

- strategy settings may need instrumentation; nondeterminism may require repeated runs to be comparable.

### Next: Milestone 1 diagnostic closure and then the Causal-ABA-guided bridge

Status: `proposed`

Close the parent-set diagnostic (QL2 parent-position swap, collider-failure inspection, small noise sweep, first-principles metrics beyond parent membership), then design and implement the bridge in which Causal ABA-style information guides ABA Learning (Milestones 2–3 in the project plan).

## Current metric families

Current implemented metrics, according to the project metrics summary, include:

- outcome category;
- learned delta-rule structure;
- body-level parent recovery;
- offgraph and ancestor diagnostics;
- Python-Horn coverage;
- Prolog-aware coverage;
- parser sanity.

Graph-level skeleton/direction/bridge metrics are reserved and should not be treated as computed.

## Experiment documentation rule

Every experiment record should include:

- research question;
- theoretical motivation;
- relation to ABA Learning;
- relation to Causal ABA;
- implementation scope;
- DGP;
- encoding;
- commands;
- environment;
- artefact paths;
- outcome summary;
- quantitative results;
- qualitative learned-rule inspection;
- failure modes;
- interpretation notes;
- claims supported;
- claims not supported;
- report relevance;
- next decision.

Use:

- `docs/experiments/TEMPLATE.md`

## Report-writing rule

Experiment records are evidence records, not polished report prose.

Workflow:

1. Cursor records facts, commands, artefacts, and bounded interpretation notes.
2. Samuel reviews and corrects the record.
3. ChatGPT drafts candidate report prose from the reviewed record.
4. Samuel verifies, edits, and integrates into the report.
5. Claims are checked against `docs/report/claims_ledger.md`.

## Current open questions

- Why does the configured learner return no solution on the binary collider (QL2) when a conjunctive parent rule exists in the table?
- Under which noise levels and sample sizes can ABA Learning recover parents in the scaled noisy setting (a systematic sweep beyond QL3's arbitrary hyper-parameters)?
- What is the root cause of the binary `unknown constant` errors in QL3, and how should the BK encoding be fixed?
- Is actual fold count available, or only folding-token/runtime proxies (for QN-001 efficiency metrics)?
- What success metrics beyond parent membership best capture whether causality is being learned (supervisor guidance: construct expected outputs from graph + DGP and compare against actual learned rules)?

## Next action

Close the parent-set diagnostic (Milestone 1):

1. implement the QL2 parent-position swap to show order-dependence;
2. inspect and explain the collider no-solution and the binary encoding errors;
3. run a small noise/hyperparameter check and the compact greedy-vs-nd comparison;
4. define first-principles success metrics beyond parent membership;
5. give each presented result an interpretation and conclusion, reasoning about DGP-expected vs actual outputs.