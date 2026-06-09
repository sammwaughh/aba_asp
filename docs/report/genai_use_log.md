# GenAI Use Log

## Purpose

This file records factual use of ChatGPT and Cursor during the Causal ABA Learning project.

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
  - design QL-001 and/or QN-001;
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
  - inspect whether QL-001/QN-001 can be run using existing infrastructure.
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