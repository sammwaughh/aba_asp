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
| M11 | — | m1.1 Parent-position and representation-order control | analysed | `docs/experiments/qualitative/M1.1-parent-position.md` | `causal/configs/experiments/M11_parent_position.yaml`; `M11_parent_position_greedy.yaml` | `M11_parent_position/cells/`; `M11_parent_position_greedy/`; `M11_ablations/` | Interim Experimentation / Progress (Milestone 1) | nd: 8/8 solved; binary σ/π pass; cat3 σ fails (ablation-supported). Stage 7 greedy: binary matches nd; cat3 all supersets; rule-level σ restored under greedy. |
| M12 | — | m1.2 Published-configuration comparison (pilot) | pilot analysed | `docs/experiments/qualitative/M1.2-config-comparison.md` | `causal/configs/experiments/M12_ecai2024.yaml`; `M12_aamas2025.yaml` | `causal/outputs/aba_learning/grid/M12_{ecai2024,aamas2025}/` | Interim Experimentation / Progress (Milestone 1) | 10-cell pilot analysed (historical). Expanded as M12x (redesign). No M1.4. |
| M12x | — | m1.2 expanded U1–U7 (ECAI/AAMAS; val-only BK; 20 cells) | run | `M1.2-expanded.md`; `M1.2-expanded-cell-inspection.md` | `M12x_{ecai2024,aamas2025}.yaml` | `M12x_summary.md`; `M12x_cell_reports/` | Interim Experimentation / Progress (Milestone 1) | Redesign re-run 20/20 solved (2026-07-20). Stage-3 rewrite pending. Catalogue: `m12x_units_reference.tex`. |
| M13 | — | m1.3 Recovery patterns and limits (claims + targeted probes from M12x) | paused | `docs/experiments/qualitative/M1.3-failure-modes.md` | — | `causal/outputs/aba_learning/grid/M13_<ablation-id>/` (only if probes run) | Interim Experimentation / Progress (Milestone 1) | Claim drafting withdrawn; Approach method retained. Restart after redesigned M12x. |

## Experiment sequence to date and next

### Done: QL1/QL2/QL3 qualitative parent-set recovery (QI-001/QI-002/QI-004)

Status: `analysed`

Inspected what ABA Learning recovers on chain/fork/collider motifs under binary/categorical-3/continuous-binned encodings, target-wise on `x2`, comparing learned body variables against the true parents. Outcome: parent recovery works in selected idealised cases but is not robust across motifs, encodings or modest noisy scaling. The DGP/encoding details are documented in the per-experiment records and the report Experimentation chapter.

### Done: greedy vs non-deterministic folding (qualitative)

Status: `analysed`

Compared `folding_mode: nd` vs `greedy` on identical fixtures (QI-001/QI-002/QI-004 greedy reruns). Greedy is faster (~120x at the QL3 scale), solve rate >= nd, net better clean recovery (colliders), one regression (cat3 fork), no recovery change at the noisy n=20 scale. See `docs/experiments/qualitative/greedy_vs_nd_qualitative_handoff.md`.

### Analysed: Milestone 1 Part 1 — parent-position and representation-order control (M11 / m1.1)

Status: **`analysed`**

Initial eight-cell metamorphic grid complete (nd + Stage 7 greedy). nd: binary passes all checks; cat3 fails σ-invariance (ablation-supported). Stage 7 greedy: binary matches nd; cat3 rule-level σ restored; all cat3 cells are parent supersets (B/C regress from nd singleton). Findings: `docs/report/findings/milestone1_part1_m11_findings.tex`. Record: `docs/experiments/qualitative/M1.1-parent-position.md`.

### Done (historical): Milestone 1 Part 2 — first M12x grid

Status: **`analysed` / superseded by redesign**

First expanded grid (M12x): U1–U7 × ECAI/AAMAS = 22 cells, all `solved`; Stage-3
against nz-BK / double-copy fixtures — historical only.

**Primary path:** `docs/research/milestone_plans/milestone1_high_level_path.md`  
**Approach:** `docs/research/milestone_plans/milestone1_part2/milestone1_part2_expanded_approach.md`  
Expanded record: `docs/experiments/qualitative/M1.2-expanded.md`  
Stage-3 inspection: `docs/experiments/qualitative/M1.2-expanded-cell-inspection.md` (historical)  
Pilot: `docs/experiments/qualitative/M1.2-config-comparison.md`

### In progress: Milestone 1 Part 2 — M12x redesign re-run

Status: **`run`** — redesigned 20-cell grid **20/20 `solved`** (2026-07-20); matrix refreshed.
Stage-3 inspection rewrite next. Matrix: `causal/outputs/aba_learning/grid/M12x_summary.md`

### Paused: Milestone 1 Part 3 — recovery patterns and limits (M1.3)

Status: **`paused`** — provisional claim drafting from the first M12x grid
**withdrawn** (2026-07-20). Method: `milestone1_part3_approach.md`. Restart after
redesigned Stage-3. No M1.4 — large-graph / bnlearn evaluation is deferred.

**Primary path:** `docs/research/milestone_plans/milestone1_high_level_path.md`  
Detail: `docs/research/milestone_plans/milestone1_part3/`

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
- Is actual fold count available, or only folding-token/runtime proxies (for M1.2 efficiency comparisons)?
- What success metrics beyond parent membership best capture whether causality is being learned (supervisor guidance: construct expected outputs from graph + DGP and compare against actual learned rules)?

## Next action

**Rewrite M12x Stage-3 inspection** for the redesign re-run (20/20 solved), then restart M1.3.

Completed so far in Milestone 1:

1. **M1.1 (M11)** — closed.
2. **M1.2 pilot (M12)** — Stages 0–3 analysed (10 cells).
3. **M1.2 expanded (M12x)** — redesign re-run complete; Stage-3 rewrite pending.

Remaining: Stage-3 → M1.3 → Milestone 1 write-up. No M1.4.