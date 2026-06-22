# Interim Report Section Plan

## Purpose

This file maps the interim report sections to available evidence, missing evidence, and planned writing steps.

It is a repo-side planning document. It should help Samuel, Cursor, and ChatGPT coordinate report writing without confusing raw artefacts, experiment records, and polished report prose.

## Current interim report status

| Section | Status | Evidence source | Writing source | Notes |
|---|---|---|---|---|
| Literature Review | drafted | `docs/report/manuscript/literature_review.md`; `.tex` in `docs/report/manuscript/` | Samuel-authored report draft | Reusable for final report. Theory canon also in `docs/theory/literature_review.tex`. |
| Background | drafted | `docs/report/manuscript/background.md`; `.tex` in `docs/report/manuscript/` | Samuel-authored report draft | Reusable for final report. Theory canon also in `docs/theory/background.tex`. |
| Introduction | drafted | `docs/report/manuscript/introduction.md`; `.tex` in `docs/report/manuscript/` | Samuel-authored report draft | States RQ1/RQ2/RQ3 and the settled "Causal ABA guides ABA Learning" direction. |
| Experimentation / Progress | drafted | `docs/report/manuscript/experimentation.md`; QI-001/QI-002/QI-004 records under `docs/experiments/` | Samuel-authored draft from experiment records | Covers QL1/QL2/QL3 (= QI-001/QI-002/QI-004). Needs the audit corrections (expected-vs-actual reasoning, conclusions per result). |
| Project Plan | drafted | `docs/report/manuscript/project_plan.md`; supervisor guidance; experiment interpretations | Samuel-authored draft | Milestones 1–6 and the 14-week schedule. |
| GenAI / authorship declaration | pending | `docs/report/genai_use_log.md`; Samuel notes | Samuel final declaration | Should remain factual and transparent. |

## Interim report framing

The interim report should present progress and a credible plan, not a final evaluation.

The experimentation section should be framed as:

> an initial diagnostic and feasibility investigation into whether the current ABA Learning bridge can recover causal-parent-like learned rules on small controlled structures.

It should not claim that the current implementation performs full Russo-style Causal ABA.

## Section outline

### 1. Introduction

Status: `drafted`

Current source:

- `docs/report/manuscript/introduction.md` (ChatGPT mirror)
- `docs/report/manuscript/introduction.tex` (report chapter)

Purpose:

- introduce the project problem;
- motivate the interaction between causal discovery and ABA Learning;
- state the interim-stage focus (RQ1 groundwork);
- preview contributions/progress and the settled direction (Causal ABA guides ABA Learning).

Use in interim report:

- already drafted; states RQ1/RQ2/RQ3;
- light editing only, kept consistent with the final experiment/plan framing.

### 2. Literature Review

Status: `complete`

Current source:

- `docs/report/manuscript/literature_review.md` (ChatGPT mirror)
- `docs/report/manuscript/literature_review.tex` (report chapter; copy in / edit here)
- Theory canon: `docs/theory/literature_review.tex`

Use in interim report:

- already drafted;
- only light editing if required for flow.

### 3. Background

Status: `complete`

Current source:

- `docs/report/manuscript/background.md` (ChatGPT mirror)
- `docs/report/manuscript/background.tex` (report chapter; copy in / edit here)
- Theory canon: `docs/theory/background.tex`

Use in interim report:

- already drafted;
- only light editing if required for flow.

### 4. Experimentation / Progress

Status: `drafted`

Current source:

- `docs/report/manuscript/experimentation.md` (ChatGPT mirror)
- `docs/report/manuscript/experimentation.tex` (report chapter)

Label mapping: report QL1/QL2/QL3 = repo QI-001/QI-002/QI-004. (The earlier n=100 scaled attempt was cut; only the reduced n=20 study is canonical and is QL3.)

Drafted structure:

1. **Setup and metrics**
   - target-wise learning of `x2` from handcrafted three-node motif tables (chain/fork/collider);
   - target column excluded from BK; binary/categorical-3/continuous-binned encodings;
   - variable-level precision, recall and F1 against the true parent set (clean-recovery de-emphasised in favour of F1, per supervisor guidance).

2. **QL1 (QI-001): initial motif-by-data-mode probe**
   - 9 tiny (4–5 row) cells, all solved;
   - fork exact (but confounded with x0/first-column preference), chain often recovers the ancestor x0, collider exact only in binary;
   - exposes the x0 confound and weak table design.

3. **QL2 (QI-002): complete truth-table baseline**
   - 6 noiseless cells; binary chain/fork exact, binary collider no-solution, cat3 chain recovers non-parent x0, cat3 collider parent-subset;
   - mean F1 ~ 0.61; recovery not reliable even under ideal separability.

4. **QL3 (QI-004): scaled noisy follow-up (n=20)**
   - 15 cells, no timeouts; 1 solved (binary chain x1-parent, superset {x0,x1}, F1 0.67), 12 no-solution, 2 binary errors; 0 exact recoveries;
   - DGP described explicitly (binary flip, categorical noise, Gaussian continuous; positive-class definitions; 3 uniform bins). Noise hyper-parameters were chosen arbitrarily — a systematic sweep is immediate future work.

5. **Greedy vs non-deterministic folding (qualitative)**
   - greedy faster (~120x at the QL3 scale), solve rate >= nd, net better clean recovery (colliders), one regression (cat3 fork), no recovery change at the noisy n=20 scale;
   - motivates Milestone 1 Part 2 (M1.2): greedy vs nd on the m1.1 grid.

6. **M1.1 (M11): parent-position and representation-order control**
   - initial eight-cell nd grid complete; binary σ/π hold; cat3 σ fails;
   - status **`more work needed`**: supervisor review (June 2026) requires granular trace/runner investigation before closure;
   - interim findings: `docs/report/findings/milestone1_part1_m11_findings.tex`.

7. **Interim interpretation and limitations**
   - bounded conclusion: parent recovery works in selected idealised cases but is not robust across motifs/encodings/noise;
   - does not implement full Russo-style Causal ABA; learned predictive rules are not automatically causal; continuous variables are binned; metrics need refinement beyond parent membership.

Per supervisor guidance, each presented result should carry an interpretation and a conclusion, and discrepancies between the expected outputs of the handcrafted DGP and the actual learned rules should be reasoned about explicitly.

Required evidence for drafting / revision:

- `docs/experiments/qualitative/QI-001.md`, `QI-002.md`, `QI-004.md`;
- `docs/experiments/qualitative/M1.1-parent-position.md`;
- `docs/experiments/qualitative/greedy_vs_nd_qualitative_handoff.md`;
- `docs/report/findings/milestone1_part1_m11_findings.tex`;
- `docs/report/claims_ledger.md`;
- selected figures/tables from `docs/report/figure_table_index.md`.

### 5. Project Plan

Status: `drafted`

Current source:

- `docs/report/manuscript/project_plan.md` (ChatGPT mirror)
- `docs/report/manuscript/project_plan.tex` (report chapter)

Purpose:

Explain what will happen after the interim report, following from the QL1/QL2/QL3 findings, the literature gap, supervisor guidance, and implementation limitations.

Drafted milestones (Weeks 1–13, with a Week-11 holiday):

1. **Milestone 1 (Weeks 1–2)** — parent-set diagnostic in four parts: **Part 1 in progress (M1.1/M11)** — metamorphic control run complete; granular π/σ mechanism investigation outstanding; **Part 2 (M1.2)** — greedy vs nd deferred until m1.1 mechanistic account clearer; Parts 3–4 — failure analysis and noise/continuous DGP investigation; first-principles success metrics beyond parent membership.
2. **Milestone 2 (Weeks 3–4)** — design the bridge in which Causal ABA-style information guides ABA Learning; specify comparable outputs and metrics.
3. **Milestone 3 (Weeks 5–6)** — implement causal-guided ABA Learning variants; compare against unguided learning; build bespoke metrics that judge whether causality (not just predictive parents) is learned.
4. **Milestone 4 (Weeks 7–8)** — scale beyond three-node motifs; set up representative external comparators and a frozen evaluation protocol.
5. **Milestone 5 (Weeks 9–10)** — evaluation, ablations, and a supervisor-reviewable full draft before the break.
6. **Milestone 6 (Weeks 12–13)** — supervisor-feedback edits, final polish, and presentation preparation.

The core direction is "Causal ABA guides ABA Learning"; parent-set recovery is groundwork (RQ1), not the main contribution.

Required evidence for drafting / revision:

- analysed experiment records;
- updated claims ledger;
- supervisor guidance (`docs/research/supervisor_guidance.md`);
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
| `docs/report/manuscript/background.md` | Background theory | Background |
| `docs/report/manuscript/literature_review.md` | Related work and gap | Literature Review |
| `docs/report/manuscript/introduction.md` | Problem framing and RQs | Introduction |
| `docs/report/manuscript/experimentation.md` | QL1/QL2/QL3 results and interpretation | Experimentation / Progress |
| `docs/report/manuscript/project_plan.md` | Milestones and schedule | Project Plan |
| `docs/research/supervisor_guidance.md` | Supervisor guidance | Experimentation / Project Plan |
| `docs/experiments/TEMPLATE.md` | Structure for experiment records | Not cited directly; supports writing workflow |
| `docs/experiments/qualitative/QI-001.md`, `QI-002.md`, `QI-004.md` | Qualitative motif experiments (QL1/QL2/QL3) | Experimentation / Progress |
| `docs/experiments/qualitative/M1.1-parent-position.md` | M1.1 metamorphic parent-position experiment | Experimentation / Progress |
| `docs/report/findings/milestone1_part1_m11_findings.tex` | M1.1 supervisor findings log | Experimentation / Progress |
| `docs/experiments/qualitative/greedy_vs_nd_qualitative_handoff.md` | Greedy vs nd folding comparison | Experimentation / Progress / Project Plan |
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

The five report chapters are drafted under `docs/report/manuscript/`. The current writing focus is to revise the Experimentation chapter to apply the audit corrections and supervisor guidance:

- give each presented result an explicit interpretation and conclusion;
- reason about the discrepancy between the handcrafted DGP's expected outputs and the actual learned rules;
- describe the DGP clearly, including where the QL3 noise comes from;
- report F1 in place of the clean-recovery score;
- implement the QL2 parent-position swap so order-dependence can be shown;
- keep the claims ledger in step with any revised interpretations.