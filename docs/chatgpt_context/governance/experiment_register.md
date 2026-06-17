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
- implemented — code in place (by Cursor); not yet run.
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
| QN-001 | — | Comparing ABA Learning strategies on minimal causal motifs | proposed (informed by the greedy-vs-nd qualitative handoff) |

## Template

Copy this block per experiment.

text ### <ID> — <short title> - Status: proposed | planned | implemented | run | analysed | reported - Research question: - Theoretical motivation: - Relation to ABA Learning: - Relation to Causal ABA: - Code path: - Dataset / DGP: - Target variable(s): - Metrics: - Baseline / comparator: - Expected result: - Interpretation rule:        # what each outcome would and would NOT show - Failure modes: - Cursor implementation plan / prompt:   # link or prompt text - Commit hash / run artifact path: - Report relevance: 

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

1. Cursor records facts and artefacts in docs/experiments/<ID>.md.
2. Samuel reviews and corrects the experiment record.
3. ChatGPT drafts candidate report prose from the reviewed record.
4. Samuel verifies, edits, and authors the final report text.
5. Claims are checked against docs/report/claims_ledger.md.

Current report-supporting files:

- docs/experiments/experiments_summary.md;
- docs/report/claims_ledger.md;
- docs/report/report_state.md;
- docs/report/figure_table_index.md;
- docs/report/genai_use_log.md;
- docs/report/manuscript/ — the five drafted report chapters (`.tex` authoritative + `.md` ChatGPT mirrors): introduction, literature_review, background, experimentation, project_plan.

ChatGPT context mirror: `docs/chatgpt_context/` is the upload-staging copy of the governance and repo-orientation docs, using canonical (matching) filenames. The governance set there is research_state.md, experiment_register.md, chatgpt_project_brief.md, supervisor_guidance.md, claims_ledger.md, report_state.md, experiments_summary.md. Cursor edits the repo originals; the mirror is re-copied before upload (see docs/chatgpt_context/README.md).

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

### QN-001 — Comparing ABA Learning strategies on minimal causal motifs

- Status: proposed.
- Detailed record: docs/experiments/QN-001.md.
- Research question: TBD after Cursor inspection and QL-001 — likely: on the same minimal causal motifs, does greedy ABA Learning recover parent-like learned-rule bodies more reliably or efficiently than non-deterministic learning?
- Theoretical motivation: supervisor guidance suggests greedy ABA Learning may behave better for learning causality, but this has not yet been demonstrated in this project.
- Relation to ABA Learning: compares ABA Learning strategy settings while holding DGPs, targets, seeds, sample sizes, and encoding fixed.
- Relation to Causal ABA: strategy comparison is causally motivated, but still does not test full Russo-style Causal ABA unless the code path implements the relevant Causal ABA assumptions and d-separation machinery.
- Code path: TBD after Cursor confirms how greedy and non-deterministic modes are configured.
- Dataset / DGP: likely same motifs as QL-001, subject to QL-001 results.
- Target variable(s): likely same as QL-001, subject to design.
- Metrics: likely solve fraction, body-parent F1, offgraph rate, timeout rate, rule complexity, runtime, folding tokens, and actual fold count if inspectable.
- Baseline / comparator: greedy vs non-deterministic ABA Learning.
- Expected result: not asserted; experiment not run.
- Interpretation rule: a difference in metrics would support only a bounded claim about the tested motifs/settings. It would not establish general strategy superiority for causal discovery.
- Failure modes: strategy settings may not be exposed cleanly; runs may not be comparable; nondeterminism may require repeated runs; fold counts may not be logged; QL-001 may reveal that the motif setup is not interpretable enough for comparison.
- Cursor implementation plan / prompt: TBD after plan-only inspection.
- Commit hash / run artefact path: —
- Report relevance: supports the interim Experimentation / Progress section if run; otherwise supports the Project Plan as the next planned experiment.