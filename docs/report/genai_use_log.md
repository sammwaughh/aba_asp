# GenAI Use Log

## Purpose

This file records factual use of ChatGPT/Codex, Cursor, and named specialist agents during
the Causal ABA Learning project.

It supports transparent authorship and future AI-use declarations. It is not itself polished declaration text.

Samuel remains the author and final decision-maker for submitted work.

## Logging principles

Record:

- what tool was used;
- what it was used for;
- what output it produced;
- what Samuel checked or changed;
- whether the output influenced submitted work.

Do not record private chain-of-thought or irrelevant chat detail.

## Tool roles

The role descriptions below include both historical and current workflows. The current
main task is the **Orchestrator Agent**, which has live repository access; older entries
that separate ChatGPT from Cursor remain historically accurate.

### Samuel

Role:

- project owner;
- final decision-maker;
- report author;
- verifier of claims, results, and prose;
- final editor of submitted work.

### ChatGPT

Permitted uses:

- research framing;
- theory alignment;
- experiment design;
- report planning;
- drafting candidate prose;
- reviewing interpretations;
- producing Cursor prompts;
- checking for overclaiming.

Not responsible for:

- final authorship;
- unverified claims;
- live repo execution;
- final submitted wording.

### Orchestrator Agent (current)

Permitted uses when Samuel requests them:

- live repository and project-context inspection;
- theory/code/evidence comparison;
- approved code and documentation edits;
- tests and consistency checks;
- research planning and drafting assistance;
- coordination of focused specialist agents.

Not responsible for research ownership, independent validation, final authorship, or
unapproved experiments and semantic changes.

### Cursor

Permitted uses:

- live repo inspection;
- implementation;
- code edits;
- test execution;
- running experiments;
- collecting artefacts;
- producing diffs;
- documenting commands and outputs.

Not responsible for:

- final research claims;
- final report prose unless explicitly requested and reviewed;
- theoretical judgement without Samuel/ChatGPT review.

## Log table

| Date | Tool | Task | Output / artefact | Used in report? | Samuel verification / edits | Notes |
|---|---|---|---|---|---|---|
| 2026-08-08 | Orchestrator Agent | Close M1.3/Milestone 1 in repository documentation and open M2 context | canonical status docs, milestone plans, experiment indexes, claims ledger, deliberately agnostic M2 approach, refreshed ChatGPT mirrors | indirect; report planning and supervisor hand-off | Samuel explicitly directed the milestone transition and will review/commit | No experiment or learner code changed; no M2 integration idea or result invented. |
| 2026-08-04–2026-08-08 | Orchestrator + specialist documentation/trace agents | Analyse and synthesise H0–H7b; support the supervisor-facing M1.3 document | H-probe evidence records and `findings_for_fabrizio.tex` | supervisor-facing evidence synthesis; not automatically submitted prose | Samuel directed the findings, reviewed sections, and completed the document | Six bounded findings; explicit ABA Learning/Causal ABA boundary preserved. |
| 2026-07-22 | Cursor | Record Fabrizio scope review; close Bucket 2; open Bucket 3; refresh ChatGPT context | supervisor guidance; research state/decisions/log; milestone plans; Bucket 3 planning stub; regenerated `docs/chatgpt_context/` | no (planning context) | Samuel supplied meeting notes and directed pivot | No Bucket 3 claims or experiments generated; mirrors prepared for manual re-upload. |
| 2026-07-21 | Cursor | M1.3 Bucket 2 targeted controls and Markdown claim records | M13-C1 (4 cells), M13-C2 (20 cells), experiment records/summaries; Bucket 2 Claims 1–2 | evidence candidate | Samuel reviewed claim direction and requested implementation | Current bridge described as unguided target-wise ABA Learning; no full Causal ABA claim. |
| 2026-07-20 | Cursor | Delete prior M12x outputs; reset status docs | deleted M12x_* grid trees/summary/cell-inspection; status → implemented awaiting fresh run | no | Samuel directed | Clean slate before locked 18-cell run; prior grids not evidence. |
| 2026-07-20 | Cursor | Withdraw M1.3 claim analysis; mark M12x redesign | deleted claim list + claim working doc; status/path docs; Approach paused | no | Samuel directed | First-grid claims not reusable; redesign U4–U7 before M1.3. |
| 2026-07-17 | Cursor | M1.3 Approach integration and initial M12x claim synthesis | `milestone1_part3_approach.md`; claim list (later deleted) | no | withdrawn 2026-07-20 | Six unordered claims from first M12x grid; **withdrawn** as uninformative fixtures. |
| 2026-06-22 | Cursor | M1.1 final closure (Stages 0–7) | `M1.1-parent-position.md`; findings tex; decisions; registers; claims; supervisor_guidance; milestone plans; `chatgpt_context` sync | m1.1 closed for report | synced; pending Samuel review | Stage 7 greedy complete; QI-002 disambiguation; M1.2 next. |
| 2026-06-22 | Cursor | M1.1 ablation doc sync; findings rewrite | `milestone1_part1_m11_findings.tex`; `M1.1-parent-position.md`; milestone plans; `decisions.md`; registers; claims M11-C-007 | findings tex §Integrated conclusion | pending Samuel review | Post-ABL-100–107; nd mechanism analysed. |
| 2026-06-22 | Cursor | M1.1 ablation pipeline + execution | `m11_ablation_*.py`; `M11_ablations/`; Stage 6 record | evidence for findings | pending Samuel review | ABL-101 pass; closure criteria met. |
| 2026-06-22 | Cursor | M1.1 status reopen; supervisor guidance sync | `M1.1-parent-position.md`; findings tex; planning doc §15.1; registers; claims M11-C-003/004/005; `supervisor_guidance.md` | superseded by ablation closure | pending Samuel review | Fabrizio M1.1 review: granular traces before ablations. |
| 2026-06-18 | Cursor | M1.1 initial run record and interim findings tex | `M1.1-parent-position.md`; `milestone1_part1_m11_findings.tex`; registers; claims M11-C-* | findings tex for supervisor; not manuscript yet | superseded by 2026-06-22 reopen | Stage 2/3 tables; later deemed insufficient for closure. |
| 2026-06-18 | Cursor | M1.1→M1.2 doc tidy; QN-001 removal | `experiments_summary`, `research_state`, `report_state`, registers, logging docs | indirect (navigation) | pending Samuel review | Retired QN-001; synced ChatGPT mirrors. |
| TBD | ChatGPT | Report-writing workflow design | Documentation plan and file templates | TBD | TBD | Planning support only. |
| TBD | ChatGPT | Generated documentation scaffold | Batch 1–3 Markdown files | TBD | TBD | To be reviewed before committing. |
| TBD | Cursor | TBD | TBD | TBD | TBD | TBD |

## ChatGPT usage entries

### Entry: documentation workflow planning

- Date: `TBD`
- Tool: `ChatGPT`
- Context: Main project hub.
- Task:
  - designed a semi-automated report-writing workflow;
  - separated repo docs, ChatGPT context files, and Notion pages;
  - proposed documentation files for experiment records, claims, report state, and AI-use tracking.
- Output:
  - documentation plan;
  - generated Markdown scaffolding.
- Samuel verification:
  - `TBD`
- Used in report:
  - `not directly | indirectly | yes`
- Notes:
  - This was workflow support, not empirical evidence.

### Entry: experiment design support

- Date: `TBD`
- Tool: `ChatGPT`
- Context: focused experiment chat.
- Task:
  - design QL-001 and milestone experiments;
  - define research question, setup, metrics, and interpretation rules.
- Output:
  - `TBD`
- Samuel verification:
  - `TBD`
- Used in report:
  - `TBD`
- Notes:
  - Must ensure no unsupported claims enter report.

### Entry: report drafting support

- Date: `TBD`
- Tool: `ChatGPT`
- Context: focused report-writing chat.
- Task:
  - draft candidate report prose from reviewed experiment records.
- Output:
  - `TBD`
- Samuel verification:
  - `TBD`
- Used in report:
  - `TBD`
- Notes:
  - Samuel must verify numerical claims, theoretical claims, citations, and wording.

## Cursor usage entries

### Entry: plan-only repo inspection

- Date: `TBD`
- Tool: `Cursor`
- Task:
  - inspect whether QL-001 can be run using existing infrastructure.
- Output:
  - `TBD`
- Commands:
```bash
TBD
```
- Files inspected:
```text
TBD
```
- Files changed:
```text
TBD
```
- Samuel verification:
  - `TBD`
- Used in report:
  - `TBD`

### Entry: implementation

- Date: `TBD`
- Tool: `Cursor`
- Task:
  - implement or configure experiment.
- Output:
  - `TBD`
- Commands:
```bash
TBD
```
- Files changed:
```text
TBD
```
- Diff reviewed by Samuel:
  - `yes | no | TBD`
- Used in report:
  - `TBD`

### Entry: experiment run

- Date: `TBD`
- Tool: `Cursor`
- Task:
  - run experiment and collect artefacts.
- Output:
  - `TBD`
- Commands:
```bash
TBD
```
- Artefacts:
```text
TBD
```
- Samuel verification:
  - `TBD`
- Used in report:
  - `TBD`

## Verification checklist

Before using AI-assisted material in submitted work:

- [ ] Samuel has read the generated material.
- [ ] Samuel has checked technical correctness.
- [ ] Samuel has checked numerical claims against artefacts.
- [ ] Samuel has checked theoretical claims against project sources/papers.
- [ ] Samuel has edited the wording into his own report style.
- [ ] Unsupported claims have been removed or caveated.
- [ ] AI assistance is recorded in this log.
- [ ] The final report remains Samuel-authored.

## Material not to treat as evidence

The following are not empirical evidence:

- ChatGPT suggestions;
- Cursor suggestions before code inspection or execution;
- supervisor guidance by itself;
- draft report prose;
- hypotheses about what ABA Learn should do.

Evidence must come from:

- code inspection;
- commands run;
- generated artefacts;
- experiment records;
- project papers/docs;
- manually verified calculations.

## Future declaration notes

Possible ingredients for a later declaration:

```text
During the project I used ChatGPT for planning, theory alignment, experiment-design discussion, and drafting assistance. I used Cursor for code navigation, implementation assistance, running tests/experiments, and collecting artefacts. All claims, results, code changes, and report prose were reviewed and edited by me before inclusion.
```

This is only a note. Final declaration text should be written later and aligned with Imperial guidance.
