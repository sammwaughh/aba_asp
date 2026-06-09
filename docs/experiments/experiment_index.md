# Experiment Index

## Purpose

This file is the repo-side index of experiments for the Causal ABA Learning project.

Each experiment should have a dedicated record under `docs/experiments/`, using `docs/experiments/TEMPLATE.md`.

This index is not a substitute for the detailed experiment records. It is an at-a-glance view of status, artefacts, and report relevance.

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

| ID | Title | Status | Experiment record | Config(s) | Artefacts | Report relevance | Main current conclusion |
|---|---|---|---|---|---|---|---|
| QL-001 | Qualitative inspection of ABA Learning on minimal causal motifs | proposed | `docs/experiments/QL-001.md` | TBD | TBD | Interim Experimentation / Progress | Not run; intended as first qualitative motif investigation. |
| QN-001 | Comparing ABA Learning strategies on minimal causal motifs | proposed | `docs/experiments/QN-001.md` | TBD | TBD | Interim Experimentation / Progress; Project Plan | Not run; depends on whether strategy comparison is supported cleanly. |

## Planned experiment sequence

### 0. DGP and encoding audit

Status: `proposed`

This is a pre-experiment audit rather than necessarily a standalone reportable experiment.

Purpose:

- inspect ArgCausalDisco generated data;
- inspect target construction;
- inspect `E+` and `E-`;
- inspect generated `bk.aba`;
- confirm what background predicates the learner receives;
- check target exclusion from BK.

Potential location:

- may be recorded inside `docs/experiments/QL-001.md`;
- may become a separate record later if it produces enough substantive findings.

### 1. QL-001

Status: `proposed`

Purpose:

> Inspect what ABA Learning recovers on simple three-node causal structures.

Likely motifs:

- chain;
- fork;
- collider.

Primary method:

- qualitative learned-rule inspection;
- target-wise comparison of learned body variables against true parents;
- selected narratable examples for interim report.

Primary risk:

- learned rules may reflect predictive association rather than causal-parent recovery.

### 2. QN-001

Status: `proposed`

Purpose:

> Compare greedy and non-deterministic ABA Learning strategies on the same small motifs, if supported by current implementation/configuration.

Primary method:

- solve-rate comparison;
- parent-body metric comparison;
- offgraph-rate comparison;
- efficiency metric comparison if available.

Primary risk:

- strategy comparison may require implementation inspection or instrumentation before it is meaningful.

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

- Can the current infrastructure already run the exact QL-001 motif/target setup using existing configs?
- Does the current runner expose enough learned-rule detail for qualitative inspection?
- How are greedy and non-deterministic modes configured, if at all?
- Is actual fold count available, or only folding-token/runtime proxies?
- How exactly does ArgCausalDisco generate the discrete/continuous samples used in current experiments?
- Should the DGP/encoding audit become its own documented experiment or remain part of QL-001?

## Next action

Ask Cursor for a plan-only inspection of the current infrastructure to determine:

1. what can be run without code changes;
2. what configs already exist;
3. how to expose learned-rule examples;
4. whether strategy comparison is already configurable;
5. whether fold/efficiency metrics can be extracted cleanly.