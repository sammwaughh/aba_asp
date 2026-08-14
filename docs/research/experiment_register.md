# Experiment Register

Lightweight index of experiments and a reusable template. Detailed records live under docs/experiments/ per the research-logging rule; this register is the at-a-glance view for project framing and reporting.

## Report-label mapping

The report (docs/report/manuscript/) refers to the qualitative experiments as QL1/QL2/QL3. These map to repo ids as follows:

- QL1 = QI-001 (motif × data-mode probe);
- QL2 = QI-002 (complete truth-table baseline);
- QL3 = QI-004 (scaled noisy follow-up, n=20).

The earlier n=100 scaled attempt was cut and is not part of the canonical experiment set; only the reduced n=20 study is canonical and is QL3.

## Status categories

- proposed — idea noted; not yet designed in full.
- planned — design agreed (question, setup, metrics, interpretation rule).
- implemented — code in place; not yet run.
- run — executed; raw artefacts produced.
- analysed — results interpreted against the interpretation rule.
- reported — written into an interim/final report section.

## Register

| ID | Report label | Title | Status |
|----|------|-------|--------|
| QL-001 | — | Qualitative inspection of ABA Learning on minimal causal motifs | realised by the QI-001..QI-004 series |
| QI-001 | QL1 | Qualitative parent-set recovery across 3 motifs x 3 data modes | analysed |
| QI-002 | QL2 | Minimal truth-table baseline for x2 parent recovery | analysed |
| QI-004 | QL3 | Scaled noisy motifs with parent-position controls (n=20) | analysed |
| QI-001 greedy | — | Greedy-folding rerun of QI-001 (3 motifs x 3 modes) | analysed |
| QI-002 greedy | — | Greedy-folding rerun of QI-002 (minimal truth-table baseline) | analysed |
| QI-004 greedy | — | Greedy-folding rerun of QI-004 (scaled noisy n=20) | analysed |
| M11 | — | m1.1 Parent-position and representation-order control | analysed (Stages 0–7; ablations + greedy comparator) |
| M12 | — | m1.2 Published-configuration comparison (ASP-ABAlearnB / Greedy ABA Learning) | analysed (Stages 0–3: 10-cell grid + full cell inspection / failure-mode taxonomy) |
| M12x | — | m1.2 expanded U1–U7 (ECAI/AAMAS; val-only BK; 18 cells) | closed / analysed (18/18 Stage-3) |
| M13 | — | m1.3 capabilities and limits of unguided ABA Learning for causal recovery | **closed / analysed** (Buckets 1–2 locked; Bucket 3 H0–H7b synthesised) |
| M13-C1 | M13 | Causal-role underdetermination under learner-input equivalence | analysed |
| M13-C2 | M13 | Comparative sensitivity to BK feature-block order | analysed |
| M13-C3 | M13 | Bucket 3 binary deterministic AND collider | **closed / analysed**; six cross-cutting findings; no separate locked claim list |
| M2 | — | Causal ABA and ABA Learning integration | **open**; approach intentionally provisional |
| M2-S1 | — | baseline_cautious solved/no-solution on seven exhaustive-support mechanisms | **run** |
| M2-S2 | — | mode-2 hunt: baseline_cautious on non-roots (Wave 0 + 3-AND/3-OR + leading isolated) | **run** |

## Template

Copy this block per experiment.

```text
### <ID> — <short title>
- Status: proposed | planned | implemented | run | analysed | reported
- Research question:
- Theoretical motivation:
- Relation to ABA Learning:
- Relation to Causal ABA:
- Code path:
- Dataset / DGP:
- Target variable(s):
- Metrics:
- Baseline / comparator:
- Expected result:
- Interpretation rule:        # what each outcome would and would NOT show
- Failure modes:
- Implementation plan / agent hand-off:   # link or prompt text
- Commit hash / run artefact path:
- Report relevance:
```

## Documentation workflow

Detailed experiment records should use:

- docs/experiments/TEMPLATE.md

Experiment records are evidence records, not polished report prose. They should record:

- exact commands;
- config paths;
- artefact paths;
- outcome summaries;
- quantitative tables;
- qualitative learned-rule examples;
- failure modes;
- supported claims;
- unsupported claims;
- next decisions.

Report-writing workflow:

1. The responsible implementation or evidence agent records facts and artefacts in
   docs/experiments/<ID>.md.
2. Samuel reviews and corrects the experiment record.
3. The Orchestrator or a named writing agent drafts candidate report prose from the
   reviewed record when Samuel requests it.
4. Samuel verifies, edits, and authors the final report text.
5. Claims are checked against docs/report/claims_ledger.md.

Current report-supporting files:

- docs/experiments/experiments_summary.md;
- docs/report/claims_ledger.md;
- docs/report/report_state.md;
- docs/report/figure_table_index.md;
- docs/report/genai_use_log.md;
- docs/experiments/qualitative/M13-C3-binary-collider-and/findings_for_fabrizio.tex
  (Milestone-1 closure synthesis);
- docs/research/milestone_plans/milestone2/README.md (active M2 path);
- docs/report/manuscript/ — the five drafted report chapters (`.tex` authoritative + `.md` ChatGPT mirrors): introduction, literature_review, background, experimentation, project_plan.

ChatGPT context mirror: `docs/chatgpt_context/` is the upload-staging copy of the
governance and repo-orientation docs, using canonical filenames. The governance set also
includes the closed Bucket-3 record, active M2 approach, and completed
`findings_for_fabrizio.tex`. Edit repo originals; re-copy the mirror before upload (see
`docs/chatgpt_context/README.md`).

## Entries

### QL-001 — Qualitative inspection of ABA Learning on minimal causal motifs

- Status: realised. The original umbrella proposal was carried out by the QI-001..QI-004 series (report labels QL1/QL2/QL3) and their greedy reruns; see those entries for the concrete designs, runs, and conclusions.
- Detailed record: docs/experiments/QL-001.md.
- Research question: TBD after focused design — likely: when tabular data is generated from simple three-node causal motifs and the current aba_asp/causal bridge learns target rules target-by-target, what rule bodies are recovered, and when do those bodies correspond to true causal parents rather than non-parent predictive associations?
- Theoretical motivation: initial qualitative feasibility/diagnostic probe for applying ABA Learning to causal discovery (Direction 1). This follows supervisor guidance to start with small motifs and inspect what ABA Learn actually recovers.
- Relation to ABA Learning: uses the inherited transformation-rule learner via the causal/ bridge; inspects learned delta rules, target rules, body variables, and possibly assumptions/contraries.
- Relation to Causal ABA: does not exercise Russo-style arr/noe/indep, d-separation, or stable-extension-as-DAG machinery unless code evidence later shows otherwise. It is a learned-rule / parent-set recovery investigation only.
- Code path: current causal/ bridge, exact config/path TBD.
- Dataset / DGP: TBD — expected to use small three-node motifs: chain, fork, collider.
- Target variable(s): TBD — likely all three variables per motif.
- Metrics: TBD — likely body-parent precision/recall/F1, offgraph rate, ancestor diagnostics, outcome category, rule complexity, coverage, and selected learned-rule inspection.
- Baseline / comparator: none required for the qualitative first pass.
- Expected result: not asserted; experiment not run.
- Interpretation rule: success would show that the current bridge can sometimes recover parent-like learned rule bodies on small controlled cases. It would not show full causal discovery or full Causal ABA.
- Failure modes: no solution, empty delta, timeout, non-parent body variables, encoding issues, data-generation ambiguity, parser issues, or uninterpretable learned rules.
- Cursor implementation plan / prompt: TBD after plan-only inspection.
- Commit hash / run artefact path: —
- Report relevance: supports the interim Experimentation / Progress section as a small qualitative diagnostic experiment.

### QI-001 — Qualitative parent-set recovery across 3 motifs x 3 data modes

- Report label: QL1.
- Status: analysed. 9/9 cells solved. Fork recovered exactly in all three modes (but the true parent is x0, so this is confounded with a first-variable preference); chain often recovered the ancestor x0 instead of the direct parent x1; collider exact only in binary. Exposed the x0/first-column confound and the weak (4–5 row) table-design problem, motivating QI-002.
- Detailed record: docs/experiments/qualitative/QI-001.md.
- Research question: whether the current ABA Learning bridge learns target rules whose body variables coincide with the direct parents of x2 across three canonical 3-node motifs (chain, fork, collider) and three data representations (binary, 3-valued categorical, continuous binned into 3 uniform bins).
- Theoretical motivation: controlled qualitative diagnostic isolating the effect of the data encoding on parent-set recovery while holding the motif fixed. Not full Causal ABA and not graph recovery.
- Relation to ABA Learning: uses the inherited learner via the causal/ bridge with fixed handcrafted examples targeting x2 only; current defaults (nd folding, folding_steps 15).
- Relation to Causal ABA: does not exercise arr/noe/indep, d-separation, or stable-extension-as-DAG machinery.
- Code path: causal/experiments/run_grid.py with graph_type handcrafted_table; fixtures in causal/experiments/handcrafted_qi001.py.
- Dataset / DGP: 9 deterministic handcrafted fixtures (3 motifs x 3 data modes).
- Target variable(s): x2 only. Encoded parents: chain {x1}, fork {x0}, collider {x0, x1}.
- Metrics: body-parent precision/recall/F1, offgraph/ancestor diagnostics, coverage, outcome category, learned-rule inspection (run stage).
- Baseline / comparator: none (qualitative first pass).
- Expected result: not asserted; experiment not run.
- Interpretation rule: success would show the bridge can recover parent-like rule bodies for x2 in these controlled cases. It would not show causal discovery or full Causal ABA.
- Failure modes: missing parent, extra ancestor, off-graph body, empty delta, no solution, timeout, parser issue.
- Cursor implementation plan / prompt: see plan "QI-001 fixtures stage 1".
- Commit hash / run artefact path: —
- Report relevance: interim Experimentation / Progress.

### QI-002 — Minimal truth-table baseline for x2 parent recovery

- Report label: QL2.
- Status: analysed. 6 cells (3 motifs x {binary, cat3}), complete noiseless truth tables. Binary chain/fork recovered exactly; binary collider returned NO solution (although the conjunctive parent rule x2 <- x0, x1 exists in the table); cat3 chain recovered the non-parent x0; cat3 collider recovered only one of two parents (parent-subset). Mean variable-level F1 ~ 0.61. Shows the perfect causal rule is learnable in some ideal cases but recovery is not reliable even under ideal separability.
- Detailed record: docs/experiments/qualitative/QI-002.md.
- Research question: under complete, noiseless truth tables for three 3-node motifs, where the true parent of x2 is the unique zero-error separator, does the current ABA Learning bridge learn an x2 target rule whose body variables equal the true direct parents?
- Theoretical motivation: principled minimal baseline replacing QI-001's unjustified 4-5 row tables; the complete factorial (binary 8 rows, cat3 18 rows) is the smallest design that makes the parent the unique perfect rule, so a causal rule is learnable in principle.
- Relation to ABA Learning: target-wise learning of x2 over handcrafted_table fixtures; default nd folding, folding_steps 15; target excluded from BK.
- Relation to Causal ABA: does not exercise arr/noe/indep, d-separation, or stable-extension-as-DAG.
- Code path: causal/experiments/run_grid.py (handcrafted_table); fixtures in causal/experiments/handcrafted_qi002.py.
- Dataset / DGP: 6 deterministic handcrafted fixtures (3 motifs x {binary, cat3}), canonical orientation, noiseless.
- Target variable(s): x2 only. Parents: chain {x1}, fork {x0}, collider {x0, x1}.
- Metrics: clean_recovery + var_parent_precision/recall/jaccard (new), ancestor_only_rate, body_parent_recall, coverage, outcome, folding tokens. body_parent_f1 de-emphasised.
- Baseline / comparator: none (qualitative baseline).
- Expected result: not asserted; experiment not run.
- Interpretation rule: success (high clean_recovery) would show the perfect causal rule is learnable in the ideal case; failure would bound the method even under ideal separability. Neither shows causal discovery or full Causal ABA. Confound treatment: the complete factorial is a principled data-level correction against the QI-001 x0/first-column confound (it decorrelates non-parents from x2, so the true parent is the unique perfect separator, and makes the canonical chain cell — where x0 ⊥ x2 — a positional-bias probe). It does NOT provide the full symmetric break: the fork's parent is x0 (bias and recovery coincide), there is no correlated-ancestor test, and no within-structure parent-position swap — those are QL3 (QI-004)'s job.
- Failure modes: missing parent, extra ancestor, off-graph body, empty delta, no solution, timeout, parser issue.
- Cursor implementation plan / prompt: see plan "Minimal and scaled motif runs (QI-002, QI-004) + metric upgrades".
- Commit hash / run artefact path: —
- Report relevance: interim Experimentation / Progress.

### QI-004 — Scaled noisy motifs with parent-position controls (n=20)

- Report label: QL3.
- Status: analysed. 15/15 cells completed with NO timeouts: 1 solved, 12 completed_no_solution, 2 binary `unknown constant` errors; clean_recovery=0 for all. The only solved cell (binary chain, x1-parent) recovered the superset {x0, x1} when the true parent set was {x1} (F1 0.67, recall 1.0, precision 0.5) — partial recovery, not exact. No exact recoveries. The scaled noisy setting is computationally feasible at n=20 but does not yield robust recovery with the arbitrarily chosen noise hyper-parameters; a systematic noise sweep is the immediate follow-up. See docs/experiments/qualitative/QI004_scaled_motifs_n20/interpretation.md.
- Detailed record: docs/experiments/qualitative/QI-004.md.
- Research question: with n=20 noisy samples and the true direct parent of x2 placed in either column, does the current ABA Learning bridge recover the true parent(s) regardless of column position, across binary/cat3/cont3 modes?
- Theoretical motivation: a computationally feasible scaled-and-noisy follow-up to the QL2 noiseless baseline, retaining parent-position variants (chain and fork generated in both orientations) so "found the cause" and "prefers x0" are distinguishable. n=20 with a 300s Prolog timeout.
- Relation to ABA Learning: target-wise learning of x2 over handcrafted_table fixtures; default nd folding, folding_steps 15; target excluded from BK.
- Relation to Causal ABA: does not exercise arr/noe/indep, d-separation, or stable-extension-as-DAG.
- Code path: causal/experiments/run_grid.py (handcrafted_table); fixtures in causal/experiments/handcrafted_qi004.py.
- Dataset / DGP: 15 deterministic handcrafted fixtures (5 structural configs x {binary, cat3, cont3}), n=20, mild noise, fixed per-fixture RNG seed.
- Target variable(s): x2 only. Parents per fixture: chain_x1parent {x1}, chain_x0parent {x0}, fork_x0parent {x0}, fork_x1parent {x1}, collider {x0, x1}.
- Metrics: clean_recovery + var_parent_precision/recall/jaccard, ancestor_only_rate, body_parent_recall, coverage, outcome, folding tokens. body_parent_f1 de-emphasised. Continuous bin-health recorded per cell.
- Baseline / comparator: x0parent vs x1parent within each motif (the confound check); plus the noiseless QI-002 baseline.
- Expected result: not asserted.
- Interpretation rule: recovery tracking the true parent column (both orientations) indicates parent recovery; recovery tracking x0 regardless indicates the positional confound. Known carry-over limitation: the binary all-zero-positive encoding may still trip `unknown constant` on some binary cells; recorded, not fixed.
- Failure modes: positional confound, ancestor proxy, sibling proxy, missing parent, off-graph body, empty delta, no solution, timeout, binary unknown-constant encoding error, parser issue.
- Cursor implementation plan / prompt: see plan "QL004 reduced-n scaled run".
- Commit hash / run artefact path: causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20/.
- Report relevance: interim Experimentation / Progress.

### QI-001 greedy — Greedy-folding rerun of QI-001

- Status: analysed. 9/9 solved; greedy is faster than nd and recovers all three colliders cleanly across modes (nd was clean only in binary); chain/fork remain supersets. See docs/experiments/qualitative/greedy_vs_nd_qualitative_handoff.md.
- Detailed record: docs/experiments/qualitative/QI001_motifs_modes_greedy/.
- Research question: relative to non-deterministic folding, does greedy folding change parent-set recovery, stability, runtime, or failure modes on the QI-001 motif-by-data-mode tasks?
- Only conceptual change: defaults.folding_mode nd -> greedy (folding_steps retained but ignored by greedy). All fixtures, motifs, target x2, data modes, bins, seeds, and the 120s timeout identical to the nd QI-001 config.
- Relation to Causal ABA: does not exercise arr/noe/indep, d-separation, or stable-extension-as-DAG. Target-wise parent-set recovery only; not causal discovery.
- Code path: causal/experiments/run_grid.py (handcrafted_table); fixtures qi001_* in causal/experiments/handcrafted.py.
- Dataset / DGP: 9 cells (3 motifs x 3 data modes), target x2.
- Metrics: clean_recovery + var_parent_precision/recall/jaccard; runtime/solve-rate/error-rate/interpretability separated in the greedy-vs-nd comparison.
- Baseline / comparator: the nd QI-001 run.
- Report relevance: interim Experimentation / Progress (greedy-vs-nd qualitative comparison).

### QI-002 greedy — Greedy-folding rerun of QI-002

- Status: analysed. 6/6 solved (vs nd's 5/6): greedy solves the binary collider that nd could not, and recovers the cat3 collider exactly; clean recovery improves 3/6 (nd) -> 4/6 (greedy), with one regression (cat3 fork exact -> superset). See docs/experiments/qualitative/greedy_vs_nd_qualitative_handoff.md.
- Detailed record: docs/experiments/qualitative/QI002_minimal_motifs_greedy/.
- Research question: in the noiseless best case, does greedy folding change whether the perfect x2 target rule is found, plus runtime/solve-rate/interpretability, relative to nd?
- Only conceptual change: defaults.folding_mode nd -> greedy. All fixtures, motifs, target x2, data modes, bins, seeds, and the 120s timeout identical to the nd QI-002 config.
- Relation to Causal ABA: does not exercise arr/noe/indep, d-separation, or stable-extension-as-DAG. Target-wise parent-set recovery only.
- Code path: causal/experiments/run_grid.py (handcrafted_table); fixtures qi002_* in causal/experiments/handcrafted.py.
- Dataset / DGP: 6 cells (3 motifs x {binary, cat3}), target x2, canonical orientation (complete factorial gives a data-level correction against the x0 confound — chain cell is a positional-bias probe; the full symmetric break via parent-position swap is QL3 (QI-004)'s job).
- Metrics: clean_recovery + var_parent_precision/recall/jaccard; greedy-vs-nd axes separated.
- Baseline / comparator: the nd QI-002 run.
- Report relevance: interim Experimentation / Progress.

### QI-004 greedy — Greedy-folding rerun of QI-004

- Status: analysed. Same outcomes as nd (1 solved, 12 no-solution, 2 binary errors; 0/15 clean) but ~120x faster (total wall ≈1233 s -> ≈10 s). At the noisy n=20 scale greedy changes only runtime, not recovery; the binary `unknown constant` errors persist (BK-encoding issue, folding-mode-independent). See docs/experiments/qualitative/greedy_vs_nd_qualitative_handoff.md.
- Detailed record: docs/experiments/qualitative/QI004_scaled_motifs_n20_greedy/.
- Research question: at the scaled/noisy n=20 setting, does greedy folding change parent-set recovery, the x0/x1 confound behaviour, runtime, solve rate, error rate, or interpretability relative to nd?
- Only conceptual change: defaults.folding_mode nd -> greedy. All fixtures, motifs, target x2, data modes, n=20, bins, seeds, and the 300s timeout identical to the nd QI-004 config. Greedy may be costlier; if cat3/cont3 cells repeatedly time out at 300s, record status and stop (no blind reruns).
- Relation to Causal ABA: does not exercise arr/noe/indep, d-separation, or stable-extension-as-DAG. Target-wise parent-set recovery only.
- Code path: causal/experiments/run_grid.py (handcrafted_table); fixtures qi004_* in causal/experiments/handcrafted_qi004.py.
- Dataset / DGP: 15 cells (5 structural configs x {binary, cat3, cont3}), target x2.
- Metrics: clean_recovery + var_parent_precision/recall/jaccard, bin-health for cont3; greedy-vs-nd axes separated. The cut n=100 attempt (QI-003) is excluded from the greedy reruns.
- Baseline / comparator: the nd QI-004 run.
- Report relevance: interim Experimentation / Progress.

### M11 — m1.1 Parent-position and representation-order control

- Status: **analysed** (Stages 0–7 complete; ablations ABL-100–107; greedy comparator June 2026).
- Detailed record: docs/experiments/qualitative/M1.1-parent-position.md.
- Interim supervisor findings: docs/report/findings/milestone1_part1_m11_findings.tex.
- Design source: docs/research/milestone_plans/milestone1_part1/milestone1_part1_parent_position.md; ablation plan `milestone1_part1/milestone1_part1_ablations.md`; greedy comparator `milestone1_part1/milestone1_part1_greedy_comparator.md`.
- Ablation artefacts: `causal/outputs/aba_learning/grid/M11_ablations/`; summary `M11_ablations/summary/abl_results.md`.
- Greedy comparator: config `M11_parent_position_greedy.yaml`; artefacts `M11_parent_position_greedy/cells/`; summary `M11_parent_position_greedy/summary/compare_nd_greedy.md`.
- Ablation command: `python -m causal.scripts.m11_ablation_run --all-required` (commit 93d51bf).
- Greedy command: `python -m causal.experiments.run_grid --config causal/configs/experiments/M11_parent_position_greedy.yaml --no-resume`.
- Stage 6 outcome: ABL-101 pass (BK flip on cat3 A → singleton); ABL-103 pass (π symmetry); ABL-105 pass (folding_mode all does not recover); ABL-100/107 audits pass. Mechanism ablation-supported.
- Stage 7 outcome: binary greedy matches nd; cat3 greedy all parent supersets; cat3 rule-level σ restored under greedy; B/C regress from nd singleton.
- Research question: under complete, noiseless QL2-style target tables, when the direct-parent and non-parent roles are exchanged between x0 and x1 and the learner-visible predictor order is independently reversed, does the learnt x2 rule follow the variable in the direct-parent role (vs a fixed x0 identity or a fixed representation position)?
- Theoretical motivation: metamorphic validity control on the QL2 (QI-002) parent-recovery proxy, targeting the unresolved categorical-chain discrepancy (expected x1, returned x0).
- Relation to ABA Learning: target-wise learning of x2 with target excluded from BK; fixed QI-002-style nd folding (folding_steps 15, timeout 120 s).
- Relation to Causal ABA: does not exercise arr/noe/indep, d-separation, or stable-extension-as-DAG. Parent-set / learned-rule recovery proxy only.
- Code path: causal/experiments/run_grid.py (handcrafted_table); fixtures in causal/experiments/handcrafted_m11.py; config causal/configs/experiments/M11_parent_position.yaml.
- Dataset / DGP: 8 deterministic fixtures (2 encodings {binary, cat3} x cells A/B/C/D), derived from one canonical A per encoding via sigma (predictor-order reversal) and pi (x0<->x1 identity swap). **Tabular DGP (not chain sampling):** exhaustive factorial over (x0,x1); x2 := parent deterministically; non-parent marginally independent of x2 (one isolated predictor + connected parent-target pair per cell). Chain-style role labels in fixtures annotate parent vs non-parent for pi only. Minimal complete factorial, one row per assignment: binary 4 rows; cat3 9 rows; noiseless. (Corrected from the inherited QI-002 x2 per-assignment repeat, which had no separator/pi/sigma/engine justification.)
- Target variable(s): x2 only. Parents: A/B {x1}, C/D {x0}.
- Metrics: Stage-0 fixture/validation assertions + learner metrics (expected-rule match, coverage, clean_recovery, var_parent_*) from the eight-cell grid run.
- Baseline / comparator: QL2 (QI-002) parent recovery; within-experiment sigma/pi square.
- Expected result: not asserted pre-run; run complete (see detailed record).
- Interpretation rule: pi-equivariance + sigma-invariance with correct coverage indicates direct-parent-role tracking; persistence of a fixed name across a valid pi-comparison indicates identity preference; a valid sigma-pair difference indicates representation-order sensitivity (interpreted only after verifying the order reaches the learner).
- Failure modes: silent column canonicalisation voiding sigma (not observed); no-solution; parser/normalisation discrepancy; implementation/artefact error; cov_py/cov_pl disagreement on assumption-based rules (cat3 A/D flagged).
- Cursor implementation plan / prompt: grid cell_dir naming implemented (`grid.cell_dir: dgp` on M11 config).
- Commit hash / run artefact path: Stage-0 validation at `causal/outputs/m11_parent_position/validation/`; learning grid at `causal/outputs/aba_learning/grid/M11_parent_position/cells/<dgp>/`; ablations at `M11_ablations/`.
- Report relevance: interim Experimentation / Progress (Milestone 1 Part 1 — analysed, Stages 0–7). The subsequent M1.2 two-config comparison is also analysed.

### M12 — m1.2 Published-configuration comparison

- Status: pilot analysed (Stages 0–3). The completed successor **M12x** is closed /
  analysed. Pilot grid: 10/10 `solved`; exact-match 2/10; ASP coverage 10/10; cell
  inspection 2026-07-13. No M1.4.
- Planning docs: `docs/research/milestone_plans/milestone1_high_level_path.md`; **Approach** `docs/research/milestone_plans/milestone1_part2/milestone1_part2_expanded_approach.md`; `docs/research/milestone_plans/milestone1_part2/`.
- Record: docs/experiments/qualitative/M1.2-config-comparison.md; Stage-3 inspection: docs/experiments/qualitative/M1.2-config-comparison-cell-inspection.md.
- Stage-0 artefacts: causal/experiments/handcrafted_m12.py (fixtures m12_sep / m12_conj / m12_disj / m12_fork / m12_chain); causal/tests/test_m12_fixtures.py (validation checks); registration in causal/experiments/handcrafted.py.
- Stage-1 artefacts: causal/run_aba_asp.py (`prolog_config` + `_build_learning_program`); causal/experiments/run_grid.py (thread `prolog_config`); causal/argcausaldisco_integration.py (shared feature-BK generation); causal/configs/experiments/M12_{ecai2024,aamas2025}.yaml; causal/experiments/m12_summary.py (side-car); tests test_m12_configs.py / test_m12_summary.py / test_runner_program.py + extended test_runner_stage2.py.
- Stage-2 artefacts: causal/outputs/aba_learning/grid/M12_{ecai2024,aamas2025}/ (cells/<fixture>/ via `grid.cell_dir: dgp`) + M12_summary.{md,json} — 2026-07-09 rerun on revised minimal fixtures (commit `9123af7`).
- Fork design note: m12_fork uses the deterministic two-child fork (x1 := 2 if x0=1 else 0; x2 := 2 if x0=2 else 0; three distinct rows, one each = 3 rows); x1's alphabet is {0,2} to stay on the value-predicate encoding path.
- Research question: for a fixed encoding of small categorical tables (each with a declared graph G, mechanism, and pre-specified expected learned output), how do ASP-ABAlearnB (`configs/ecai2024_config.pl`) and Greedy ABA Learning (`configs/aamas2025_config.pl`) differ in whether the expected output is learned, the structural class of what is learned instead, and which data properties expose divergence?
- Theoretical motivation: Milestone 1's goal is a report-ready account of when and how unguided ABA Learning recovers mechanism-aligned rules; comparing the two scoped published configurations (rather than ad-hoc option hybrids) anchors the observed divergence to the ECAI 2024 and AAMAS 2025 systems.
- Relation to ABA Learning: the inherited engine runs under the two shipped configuration files, consulted verbatim (brave mode, `check_ic` kept, `asm_intro(relto)` in both arms); both use the shared feature-BK + E+/E- construction.
- Relation to Causal ABA: does not exercise arr/noe/indep, d-separation, or stable-extension-as-DAG. Mechanism-aligned rule recovery only; not causal discovery.
- Code path: causal/experiments/handcrafted_m12.py (fixtures); runner consults a `prolog_config` .pl file verbatim (done, Stage 1); shared feature-BK construction (done); M12 metric side-car causal/experiments/m12_summary.py (done); timeout 60 s.
- Dataset / DGP: five minimal 3-variable (x0,x1,x2) categorical fixtures, target x2, positive x2=2, no duplicate rows: separator anchor (9 rows, x2:=x1, x0 isolated), conjunctive collider (9-row factorial over (x0,x1), x2:=min(x0,x1), single positive), disjunctive collider (twin of conj, x2:=max(x0,x1), 5 pos/4 neg), fork (correlated-sibling confound, 3 deterministic rows, single positive), correlated-ancestor chain (6 rows; P(pos|x0)=0, 1/2, 1/2).
- Target variable(s): fixture-designated target, excluded from feature BK; one-vs-rest positive class.
- Metrics (at-a-glance divergence detectors only; qualitative expected-vs-learned comparison is the instrument): table-relative outcome class; body-scope parent F1 + framework-scope variable set; ASP `pos_covered` / `neg_rejected` fractions; framework complexity (rules/assumptions/contraries/body length); prolog.stdout line count as runtime proxy.
- Baseline / comparator: the two arms against each other, per fixture.
- Expected result: not asserted; per-cell expected outputs pre-specified in the plan/record before any run.
- Interpretation rule: success per cell = learned framework matches the pre-specified expected output up to harmless syntactic variation (all M1.2 fixtures are coherent intensional targets). Divergence between the scoped arms is the unit of finding; mechanistic confirmation is M1.3's job.
- Failure modes: parent superset, misaligned assumption structure, non-parent rule, ancestor citation (chain family), no solution, timeout, error; config-consult or BK-encoding issues.
- Report relevance: interim Experimentation / Progress (Milestone 1 Part 2).

### M12x — m1.2 expanded U1–U7 grid

- Status: **`analysed` / closed** — fresh 18-cell grid **18/18 `solved`** (2026-07-20); Stage-3 **done** (18/18); evidence package locked for M1.3.
- Record: `docs/experiments/qualitative/M1.2-expanded.md`.
- Inspection: `docs/experiments/qualitative/M1.2-expanded-cell-inspection.md` (done; 18/18).
- Design: Approach + unit set + `mechanism_cards/` U1–U7; catalogue `m12x_units_reference.tex`.
- Fixtures: `causal/experiments/handcrafted_m12x.py` (nonzero-positive; val-only BK).
- Configs: `causal/configs/experiments/M12x_{ecai2024,aamas2025}.yaml` (`cell_dir: slug`; `grid.seed` omitted).
- Cells: 9 per config × 2 = **18**; dirs `{dgp}__target-{t}`.
- Output: `M12x_{ecai2024,aamas2025}/`; `M12x_summary.md`; `M12x_cell_reports/` (18).
- Generator: `causal/experiments/m12x_summary.py`.
- Relation to Causal ABA: none exercised.
- Next: none for M12x — hand off to M1.3 claim drafting.

### M13 — m1.3 causal-recovery capabilities and limits

- Status: **`closed / analysed`** (2026-08-08) — Bucket 1 **written / locked**;
  Bucket 2 **locked / closed** with Claims 1–2; Bucket 3 **H0–H7b run /
  analysed** (includes H4b). H5 experimental
  `greedy_cautious` is **run / analysed** (`h5_greedy_cautious.md`); **H6 is
  `run / analysed`** (`h6_folding_and_n_ablation.md`); **H7a is
  `run / analysed`** (`h7a_relto_vs_sechk.md`); **H7b is `run / analysed`** (`h7b_cautious_relto_vs_sechk.md`).
- Planning docs: `docs/research/milestone_plans/milestone1_high_level_path.md`; `docs/research/milestone_plans/milestone1_part3/`.
- Approach (method): `docs/research/milestone_plans/milestone1_part3/milestone1_part3_approach.md`.
- Bucket 1 (locked): `docs/experiments/qualitative/M1.3-bucket1-claims.md` (TeX: `docs/report/findings/milestone1_part3_bucket1_claims.tex`).
- Bucket 2 (locked): `docs/experiments/qualitative/M1.3-bucket2-claims.md` (two claims; M13-C1/C2).
- Bucket 3: `docs/experiments/qualitative/M1.3-bucket3-claims.md`.
- Investigation: **M13-C3** —
  `docs/experiments/qualitative/M13-C3-binary-collider-and/experiment.md`
  (H0: `learning_analysis.md`; H1: `h1_support_ablation.md`; H2:
  `h2_irrelevant_covariate.md`; H3: `h3_bk_leading_distractor.md`; H4:
  `h4_cautious_vs_brave.md`; H4b: `h4b_cautious_split_under_a.md`; H5:
  `h5_greedy_cautious.md`; H6: `h6_folding_and_n_ablation.md`; H7a:
  `h7a_relto_vs_sechk.md`; H7b: `h7b_cautious_relto_vs_sechk.md`).
- Closure synthesis:
  `docs/experiments/qualitative/M13-C3-binary-collider-and/findings_for_fabrizio.tex`.
  It records six cross-cutting findings. No separate locked Bucket-3 claim list was
  created.


#### M13-C1 — causal-role underdetermination

- Status: **`analysed`** (2026-07-21); 4/4 cells runner-`solved`.
- Record:
  `docs/experiments/qualitative/M13-C1-causal-role-underdetermination/experiment.md`.
- Configs: `M13_c1_role_equivalence_{ecai2024,aamas2025}.yaml`.
- Summary: `M13_c1_role_equivalence_summary.{md,json}`.
- Result: learner-visible inputs, normalised delta, and coverage were identical within
  each graph-labelled pair. ECAI was exact under \(G_0\) and sibling-only under \(G_1\);
  AAMAS retained parent plus sibling under both.
- Next: none; supports Bucket 2 Claim 1.

#### M13-C2 — BK feature-block order

- Status: **`analysed`** (2026-07-21); 20/20 cells runner-`solved`.
- Record: `docs/experiments/qualitative/M13-C2-bk-feature-order/experiment.md`.
- Configs: `M13_c2_bk_order_{ecai2024,aamas2025}.yaml`.
- Summary: `M13_c2_bk_order_summary.{md,json}`.
- Result: all tested ECAI feature orders yielded distinct normalised deltas within U2,
  U5, and U7. AAMAS preserved one normalised delta and coverage result per family.
  U5 parent-first order restored exact ECAI recovery; U7 negative rejection depended
  on whether required parent \(x_2\) occurred in the first two blocks.
- Next: none; supports locked Bucket 2 Claim 2. The proposed Bucket 2 Claim 3 was
  parked on 22 July.

#### M13-C3 — binary deterministic AND collider (Bucket 3)

- Status: **`closed / analysed`** — H0–H7b complete (incl. H4b); six
  cross-cutting findings consolidated; no separate locked Bucket-3 claim list.
- Record: `docs/experiments/qualitative/M13-C3-binary-collider-and/experiment.md`.
- H0: `.../learning_analysis.md` / `.tex`.
- H1: `.../h1_support_ablation.md` / `.tex`.
- H2: `.../h2_irrelevant_covariate.md` / `.tex`.
- H3: `.../h3_bk_leading_distractor.md` / `.tex`.
- H4: `.../h4_cautious_vs_brave.md` / `.tex`.
- H4b: `.../h4b_cautious_split_under_a.md` / `.tex`.
- H5: `.../h5_greedy_cautious.md` / `.tex`.
- H6: `.../h6_folding_and_n_ablation.md` / `.tex`.
- H7a: `.../h7a_relto_vs_sechk.md` / `.tex`.
- H7b: `.../h7b_cautious_relto_vs_sechk.md` / `.tex`.
- Catalogue: `.../future_probes.md` / `.tex`.
- H7b lead (bounded; not a claim): under cautious nd, relto vs sechk —
  child `c` deltas differ (Q1–Q2); sechk retains `b`/`d` (unlike brave H7a);
  Q4–Q5 empty-stdout timeouts non-comparable.
- H7a lead (bounded; not a claim): under brave nd, relto vs sechk — 7/7
  solved with differing deltas; sechk first-BK latch + α-chain vs richer
  relto contraries; not a method ranking.
- H6 lead (bounded; not a claim): under cautious+nd, root search cost ≈
  linear in `folding_steps(M)` (failed-band replays) and in nested `n` at
  fixed `M=2` (per-band bookkeeping); control `c` delta-stable.
- H5 lead (bounded; not a claim): under Greedy, brave→cautious matches 18/18
  outcomes and solved deltas; Analysis B contrasts vs nd `baseline_cautious`
  are search-bundle (not the mode flip). Config is experimental
  `greedy_cautious`, not an AAMAS-paper method.
- H4b lead (bounded; not a claim): on H3 fixture target `c`, cautious changes only `c_alpha_3` to `d_val_1` (Layer B); Layer A shared with H3.
- H4 lead (bounded; not a claim): `baseline_cautious` on the H0 table blocks
  the brave residual α-gadget for roots `a`/`b` (`completed_no_solution`);
  control `c` still solves with identical delta to locked ECAI.
- H3 lead (bounded; not a claim): ECAI on
  `m13_bucket3_binary_bd_and_lead_a` / `n30_seed42` first-folds to / retains
  BK-leading `a` for target `c` (not evaluator BD AND).
- H2 lead (bounded; not a claim): AAMAS on
  `m13_bucket3_binary_collider_and_iso_d` / `n30_seed42` solves `c` with
  bodies that **include irrelevant `d_val_*`**, not the evaluator D-free AND.
- H4 collection:
  `causal/outputs/aba_learning/targetwise/m13_bucket3_binary_collider_and/baseline_cautious/n30_seed42/`.
- H4b config:
  `causal/configs/targetwise/m13_bucket3_binary_bd_and_lead_a/baseline_cautious/n30_seed42.yaml`.
- H4b collection:
  `causal/outputs/aba_learning/targetwise/m13_bucket3_binary_bd_and_lead_a/baseline_cautious/n30_seed42/`.
- H5 collections:
  `.../targetwise/<fixture>/{aamas2025,greedy_cautious}/<sample>/` across the
  five completed AAMAS tables.
- H6 collections (new):
  `.../m13_bucket3_binary_collider_and/baseline_cautious_steps{1,2,5}/...`
  plus nested `n60_seed42` / `n90_seed42` under steps2; steps-10 = reused H4.
- Closure: `findings_for_fabrizio.tex` is the canonical cross-probe synthesis. No
  further M1.3 probe is pending.

### M2 — Causal ABA and ABA Learning integration

- Status: **open** (2026-08-08); approach intentionally provisional.
- Primary path: `docs/research/milestone_plans/milestone2/README.md`.
- Current direction: understand the argumentative causal discovery paper and
  ArgCausalDisco code intimately, then try and test possible integrations with ABA
  Learning.
- Boundary: no architecture, deliverable sequence, experiment portfolio, or
  investigation order is fixed in advance. ArgCausalDisco and this checkout's target-wise
  `causal/` bridge remain distinct implementations.

### M2-S1 — baseline_cautious outcomes on exhaustive-support mechanisms

- Status: **run** (2026-08-14).
- Research question: under `baseline_cautious` and handwritten exhaustive root-support
  tables, which targets are `solved` vs `completed_no_solution` on AND, OR, XOR,
  copy, NOT, copy-chain, and copy/NOT fork?
- Record: `docs/experiments/qualitative/M2-S1-support-mechanism-outcomes/experiment.md`.
- Code path: target-wise `causal.targetwise.cli run` with
  `causal/configs/targetwise/m2_support_*/baseline_cautious/support.yaml`.
- Artefacts:
  `causal/outputs/aba_learning/targetwise/m2_support_*/baseline_cautious/support/`.
- Boundary: outcome grid only; not a Causal ABA integration result and not a locked
  claim. Deltas retained for later inspection.

### M2-S2 — mode-2 hunt on non-roots

- Status: **run** (2026-08-14).
- Research question: under `baseline_cautious` and exhaustive root-support tables,
  does any **non-root** return `completed_no_solution` (failure mode 2)?
- Record: `docs/experiments/qualitative/M2-S2-mode2-nonroot-outcomes/experiment.md`.
- Scope: Wave 0 non-roots reused from M2-S1; new cells are 3-OR `c` and
  leading-isolated 3-AND `c`. 4-AND, majority-3, and mux were not run.
- Artefacts:
  `causal/outputs/aba_learning/targetwise/m2_support_*/baseline_cautious/support/cells/target-*/output/`.
- Result: every scored non-root was `solved` (10/10). Combined outcome grid is
  in the experiment record. Mode 2 did not occur on this set.
