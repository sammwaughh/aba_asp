# Interim Report Section Plan

## Purpose

This file maps the interim report sections to available evidence, missing evidence, and planned writing steps.

It is a repo-side planning document. It should help Samuel, Cursor, and ChatGPT coordinate report writing without confusing raw artefacts, experiment records, and polished report prose.

## Current interim report status

| Section | Status | Evidence source | Writing source | Notes |
|---|---|---|---|---|
| Literature Review | complete | `literature_review_current.md`; canonical report `.tex` source in repo | Samuel-authored report draft | Reusable for final report. |
| Background | complete | `background_current.md`; canonical report `.tex` source in repo | Samuel-authored report draft | Reusable for final report. |
| Introduction | not started | Final section plan and experiment framing | To be written last | Not a current blocker. |
| Experimentation / Progress | pending | Experiment records under `docs/experiments/` | ChatGPT draft from records, Samuel final edit | Main current bottleneck. |
| Project Plan | pending | Supervisor guidance, experiment interpretations, literature gap | ChatGPT draft from records, Samuel final edit | Should follow experiments. |
| GenAI / authorship declaration | pending | `docs/report/genai_use_log.md`; Samuel notes | Samuel final declaration | Should remain factual and transparent. |

## Interim report framing

The interim report should present progress and a credible plan, not a final evaluation.

The experimentation section should be framed as:

> an initial diagnostic and feasibility investigation into whether the current ABA Learning bridge can recover causal-parent-like learned rules on small controlled structures.

It should not claim that the current implementation performs full Russo-style Causal ABA.

## Section outline

### 1. Introduction

Status: `not started`

Purpose:

- introduce the project problem;
- motivate the interaction between causal discovery and ABA Learning;
- state the interim-stage focus;
- preview contributions/progress.

Evidence needed:

- completed literature review and background;
- final experiment/progress summary;
- project plan.

Drafting rule:

Write this section last.

### 2. Literature Review

Status: `complete`

Current source:

- `literature_review_current.md`
- canonical editable report source remains the corresponding `.tex` file in the repo.

Use in interim report:

- already drafted;
- only light editing if required for flow.

### 3. Background

Status: `complete`

Current source:

- `background_current.md`
- canonical editable report source remains the corresponding `.tex` file in the repo.

Use in interim report:

- already drafted;
- only light editing if required for flow.

### 4. Experimentation / Progress

Status: `pending`

Purpose:

Show concrete technical progress after the literature/background work.

Recommended structure:

1. **Experimental infrastructure**
   - YAML-configured grid runner.
   - Per-cell artefacts.
   - Result aggregation.
   - Basic metrics.
   - Current limitation: parent-set / learned-rule recovery, not full DAG-level Causal ABA.

2. **Motivation for minimal motif experiments**
   - Supervisor guidance: start with simple three-node structures.
   - Qualitative inspection is needed before large-scale evaluation.
   - Aim: understand what ABA Learn recovers.

3. **DGP and encoding audit**
   - Inspect ArgCausalDisco-generated samples.
   - Inspect ABA encoding.
   - Confirm what the learner is actually given.

4. **QL-001 qualitative investigation**
   - chain/fork/collider motifs;
   - target-wise learned rules;
   - comparison of learned bodies with true parents;
   - selected narratable examples.

5. **QN-001 strategy comparison, if available**
   - greedy versus non-deterministic learning;
   - solve rate;
   - parent-body metrics;
   - efficiency proxies;
   - failure modes.

6. **Limitations**
   - current implementation does not test full Causal ABA;
   - learned predictive rules are not automatically causal rules;
   - small motifs are diagnostic, not conclusive;
   - metrics are partial and need refinement.

Required evidence before drafting:

- `docs/experiments/QL-001.md`;
- `docs/experiments/QN-001.md` if run or plan-only status if not run;
- `docs/report/claims_ledger.md`;
- selected figures/tables from `docs/report/figure_table_index.md`.

### 5. Project Plan

Status: `pending`

Purpose:

Explain what will happen after the interim report.

Plan should follow from:

- literature gap;
- supervisor guidance;
- QL-001 findings;
- QN-001 findings or design status;
- implementation limitations.

Likely future directions:

1. refine small-motif experiments;
2. compare ABA Learning strategies more systematically;
3. add or improve efficiency metrics, e.g. folds if inspectable;
4. extend beyond three-node motifs;
5. distinguish predictive association from causal-parent recovery;
6. explore richer causal encodings;
7. move closer to Causal ABA machinery if feasible;
8. explore reverse direction: using causal structure to guide ABA Learning.

Required evidence before drafting:

- analysed experiment records;
- updated claims ledger;
- supervisor guidance;
- known implementation constraints.

### 6. GenAI / authorship declaration

Status: `pending`

Purpose:

Transparently record use of ChatGPT and Cursor while preserving Samuel’s authorship.

Evidence source:

- `docs/report/genai_use_log.md`;
- Samuel’s Notion `AI-use and Authorship Notes`.

Must include:

- ChatGPT used for planning, theory alignment, drafting assistance, and critical review;
- Cursor used for implementation assistance, repo inspection, tests, diffs, and artefact collection;
- Samuel reviewed, verified, edited, and authored the submitted work.

## Evidence-to-section map

| Evidence / document | Used for | Section |
|---|---|---|
| `background_current.md` | Background theory | Background |
| `literature_review_current.md` | Related work and gap | Literature Review |
| `supervisor_guidance_current.md` | Motivation for initial experimental direction | Experimentation / Project Plan |
| `docs/experiments/TEMPLATE.md` | Structure for experiment records | Not cited directly; supports writing workflow |
| `docs/experiments/QL-001.md` | Qualitative motif experiment | Experimentation / Progress |
| `docs/experiments/QN-001.md` | Strategy comparison | Experimentation / Progress / Project Plan |
| `docs/report/claims_ledger.md` | Claim verification | All report sections |
| `docs/report/figure_table_index.md` | Figures/tables and captions | Experimentation / Progress |
| `docs/report/genai_use_log.md` | AI-use declaration | Declaration / appendix if required |

## Writing workflow

1. Cursor records experiment evidence in `docs/experiments/<ID>.md`.
2. Samuel reviews and corrects the experiment record.
3. ChatGPT drafts candidate report prose from the reviewed record.
4. Samuel edits, verifies, and integrates the prose into the report.
5. Claims used in the report are added to or checked against `docs/report/claims_ledger.md`.

## Report claim rule

No claim should enter the interim report unless it is one of:

- directly supported by theory/background/literature;
- directly supported by code/experiment evidence;
- explicitly marked as a limitation;
- explicitly marked as future work.

Avoid unsupported claims such as:

- the current bridge implements full Causal ABA;
- the current experiments prove causal discovery;
- learned predictive rules are necessarily causal rules;
- reserved graph-level metrics have been computed.

## Current next writing milestone

Before drafting the Experimentation / Progress section, complete:

- QL-001 design;
- Cursor plan-only inspection;
- DGP/encoding audit;
- at least one documented qualitative learned-rule inspection;
- update claims ledger.