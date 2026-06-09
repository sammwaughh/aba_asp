# Experiment Register

Lightweight index of experiments and a reusable template. Detailed records live under docs/experiments/ per the research-logging rule; this register is the at-a-glance view for project framing and reporting.

## Status categories

- proposed — idea noted; not yet designed in full.
- planned — design agreed (question, setup, metrics, interpretation rule).
- implemented — code in place (by Cursor); not yet run.
- run — executed; raw artefacts produced.
- analysed — results interpreted against the interpretation rule.
- reported — written into an interim/final report section.

## Register

| ID | Title | Status |
|----|-------|--------|
| QL-001 | Qualitative inspection of ABA Learning on minimal causal motifs | proposed |
| QN-001 | Comparing ABA Learning strategies on minimal causal motifs | proposed |

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

- docs/experiments/EXPERIMENT_INDEX.md;
- docs/report/claims_ledger.md;
- docs/report/interim_section_plan.md;
- docs/report/figure_table_index.md;
- docs/report/genai_use_log.md;
- ChatGPT-facing mirrors: experiments_summary_current.md, claims_ledger_current.md, report_state_current.md, supervisor_guidance_current.md.

## Entries

### QL-001 — Qualitative inspection of ABA Learning on minimal causal motifs

- Status: proposed.
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