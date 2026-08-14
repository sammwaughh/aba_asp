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
| M12x | — | m1.2 expanded U1–U7 (ECAI/AAMAS; val-only BK; 18 cells) | closed / analysed | `M1.2-expanded.md` | `M12x_{ecai2024,aamas2025}.yaml` | `M12x_summary.md`; `M12x_cell_reports/` (18) | Interim Experimentation / Progress (Milestone 1) | Fresh 18/18 solved + Stage-3 18/18 (2026-07-20); **closed**; evidence locked for M1.3. |
| M13 | — | m1.3 causal-recovery capabilities and limits of unguided ABA Learning | **closed / analysed** | `M1.3-bucket1-claims.md` (locked); `M1.3-bucket2-claims.md` (locked); `M1.3-bucket3-claims.md` (closed) | — | M13-C3 H0–H7b; `findings_for_fabrizio.tex` | Milestone 1 closure / report evidence | Buckets 1–2 retain six locked claims; Bucket 3 closes with six cross-cutting findings and no separate locked claim list. |
| M13-C1 | M13 | Causal-role underdetermination under learner-input equivalence | analysed | `M13-C1-causal-role-underdetermination/experiment.md` | `M13_c1_role_equivalence_{ecai2024,aamas2025}.yaml` | `M13_c1_role_equivalence_summary.{md,json}`; 4 cell dirs | Interim Experimentation / Progress (Milestone 1) | 4/4 solved; paired inputs/delta/coverage identical. ECAI exact under \(G_0\), sibling-only under \(G_1\); AAMAS parent-plus-sibling under both. |
| M13-C2 | M13 | Comparative sensitivity to BK feature-block order | analysed | `M13-C2-bk-feature-order/experiment.md` | `M13_c2_bk_order_{ecai2024,aamas2025}.yaml` | `M13_c2_bk_order_summary.{md,json}`; 20 cell dirs | Interim Experimentation / Progress (Milestone 1) | 20/20 solved. Every tested ECAI order produced a distinct delta within U2/U5/U7; AAMAS delta and coverage invariant per family. U5 swap restored exact ECAI parent recovery; U7 coverage depended on whether \(x_2\) was in the first two blocks. |
| M13-C3 | M13 | Bucket 3 binary deterministic AND collider | **closed / analysed** | `experiment.md`; `h1`–`h7b` records; `future_probes.*`; `findings_for_fabrizio.tex` | H0–H7b configurations | H0–H7b collections | Milestone 1 closure / report evidence | Six cross-cutting findings consolidate Greedy, nd-order, semantics, folding-budget, multiplicity, and assumption-introduction behaviour; see the synthesis for exact scope and caveats. |
| M2 | — | Causal ABA and ABA Learning integration | **open** | `docs/research/milestone_plans/milestone2/README.md` | none yet | none yet | Milestone 2 | Understand the argumentative causal discovery paper and ArgCausalDisco intimately; then try and test possible integrations without fixing the approach in advance. |
| M2-S1 | — | baseline_cautious solved/no-solution on seven exhaustive-support mechanisms | **run** | `qualitative/M2-S1-support-mechanism-outcomes/experiment.md` | `causal/configs/targetwise/m2_support_*/baseline_cautious/support.yaml` | `causal/outputs/aba_learning/targetwise/m2_support_*/baseline_cautious/support/` | Milestone 2 | Wave 0: AND/OR roots `no-sol`, children `solved`; XOR/copy/NOT/chain/fork all `solved`. No non-root `no-sol`. |
| M2-S2 | — | mode-2 hunt: baseline_cautious on non-roots | **run** | `qualitative/M2-S2-mode2-nonroot-outcomes/experiment.md` | same Wave 0 configs plus 3-AND, 3-OR, leading-isolated | same `targetwise/m2_support_*/` cells | Milestone 2 | Combined grid: every scored non-root `solved` (10/10). 3-AND roots `timeout` at 300s. Mode 2 did not occur. |
| M2-G1 | — | ABALearnG vs ABALearnU on oracle-parent BK | **run** | `qualitative/M2-G1-oracle-parent-bk/experiment.md` | `.../baseline_cautious_oracle_parents/support.yaml` | `targetwise/<fixture>/baseline_cautious_oracle_parents/support/` | Milestone 2 | Flagship 3-AND+isolate `c`: G 8 rules/2 asm vs U 20/5; G vocab `{b,d,e}`. Copy-chain `c`: G parent `b`, U ancestor `a`; same length. |

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

### Done / closed: Milestone 1 Part 2 — M12x

Status: **`analysed` / closed** — fresh 18-cell grid **18/18 `solved`** (2026-07-20); Stage-3
**18/18 written** (2026-07-20); evidence package locked for M1.3.

**Primary path:** `docs/research/milestone_plans/milestone1_high_level_path.md`  
**Approach:** `docs/research/milestone_plans/milestone1_part2/milestone1_part2_expanded_approach.md`  
Expanded record: `docs/experiments/qualitative/M1.2-expanded.md`  
Inspection: `docs/experiments/qualitative/M1.2-expanded-cell-inspection.md`  
Matrix: `causal/outputs/aba_learning/grid/M12x_summary.md`  
Pilot (historical): `docs/experiments/qualitative/M1.2-config-comparison.md`

### Closed: Milestone 1 Part 3 — causal-recovery capabilities and limits (M1.3)

Status: **`closed / analysed`** — Bucket 1 **locked**; Bucket 2 **locked / closed** with
Claims 1–2 from M13-C1/C2; Bucket 3 **H0–H7b run / analysed** (includes H4b).
H5 experimental
`greedy_cautious` is **run / analysed** (`h5_greedy_cautious.md`); **H6 is
`run / analysed`** (`h6_folding_and_n_ablation.md`); **H7a is `run /
analysed`** (`h7a_relto_vs_sechk.md`); **H7b is `run / analysed`** (`h7b_cautious_relto_vs_sechk.md`).
Method: `milestone1_part3_approach.md`. Cross-cutting closure synthesis:
`M13-C3-binary-collider-and/findings_for_fabrizio.tex`.

**Primary path:** `docs/research/milestone_plans/milestone1_high_level_path.md`  
Detail: `docs/research/milestone_plans/milestone1_part3/`  
Bucket 1 (locked): `docs/experiments/qualitative/M1.3-bucket1-claims.md`  
Bucket 2 (locked): `docs/experiments/qualitative/M1.3-bucket2-claims.md`

Bucket 3 (M13-C3 **closed; H0–H7b analysed**; no separate locked claim list):
`docs/experiments/qualitative/M1.3-bucket3-claims.md`
Case: `docs/experiments/qualitative/M13-C3-binary-collider-and/experiment.md`
H0: `.../learning_analysis.md`  
H1: `.../h1_support_ablation.md`  
H2: `.../h2_irrelevant_covariate.md`
H3: `.../h3_bk_leading_distractor.md`
H4: `.../h4_cautious_vs_brave.md`
H4b: `.../h4b_cautious_split_under_a.md`
H5: `.../h5_greedy_cautious.md`
H6: `.../h6_folding_and_n_ablation.md`
H7a: `.../h7a_relto_vs_sechk.md`
H7b: `.../h7b_cautious_relto_vs_sechk.md`

H5 lead: under Greedy, brave→cautious matches 18/18 outcomes and solved deltas;
Analysis B contrasts vs nd `baseline_cautious` are search-bundle (not the mode
flip). No Bucket 3 claim. **H6** folding-step / nested-n ablations are **run /
analysed** (`h6_folding_and_n_ablation.md`). **H7a** is **run / analysed**
(`h7a_relto_vs_sechk.md`); **H7b** is **run / analysed**
(`h7b_cautious_relto_vs_sechk.md`).


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

1. The responsible implementation or evidence agent records facts, commands, artefacts,
   and bounded interpretation notes.
2. Samuel reviews and corrects the record.
3. The Orchestrator or a named writing agent drafts candidate report prose from the
   reviewed record when Samuel requests it.
4. Samuel verifies, edits, and integrates into the report.
5. Claims are checked against `docs/report/claims_ledger.md`.

## Milestone 1 closure boundary

- No further H7 / Bucket-3 probe is pending.
- The six cross-cutting Bucket-3 findings are recorded in `findings_for_fabrizio.tex`;
  individual H-probes remain bounded evidence rather than standalone claims.
- Missingness, larger graphs, parameter/category variation, and non-discrete data were
  not required for closure and are not automatically M2 work.

## Current direction

Milestone 2 begins with intimate study of the argumentative causal discovery paper and
ArgCausalDisco code. Possible integrations with ABA Learning will then be tried and tested.
No more specific process is fixed by the milestone approach.


Completed so far in Milestone 1:

1. **M1.1 (M11)** — closed.
2. **M1.2 pilot (M12)** — Stages 0–3 analysed (10 cells).
3. **M1.2 expanded (M12x)** — closed (18/18 solved + Stage-3 18/18).
4. **M1.3 Bucket 1** — locked (4 claims).
5. **M1.3 Bucket 2** — locked (2 claims; M13-C1/C2).

6. **M1.3 Bucket 3** — closed after H0–H7b and six-finding synthesis.

Milestone 1 is closed. No M1.4. Milestone 2 is open.
