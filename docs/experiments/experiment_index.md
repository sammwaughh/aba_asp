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
| QI-001 | Qualitative parent-set recovery across 3 motifs x 3 data modes | implemented | `docs/experiments/qualitative/QI-001.md` | `causal/configs/experiments/QI001_motifs_modes.yaml` | TBD | Interim Experimentation / Progress | Stage 1 fixtures/config/tests in place; first ABA Learning run done (9/9 solved); interpretation pending. Two design limitations (x0 confound, tiny-n) motivate QI-002/QI-003. |
| QI-002 | Minimal truth-table baseline for x2 parent recovery | implemented | `docs/experiments/qualitative/QI-002.md` | `causal/configs/experiments/QI002_minimal_motifs.yaml` | TBD | Interim Experimentation / Progress | 6 cells (3 motifs x binary8/cat3-18), noiseless complete truth tables so the true parent is the unique perfect rule; the complete factorial is a data-level correction against the x0 confound (chain cell is a positional-bias probe), but the full symmetric break (parent-position swap) is QI-003/QI-004's job. |
| QI-003 | Scaled noisy motifs with parent-position controls (n=100) | run (feasibility attempt; superseded by QI-004) | `docs/experiments/qualitative/QI-003.md` | `causal/configs/experiments/QI003_scaled_motifs.yaml` | `causal/outputs/aba_learning/grid/QI003_scaled_motifs/` (partial) | Interim Experimentation / Progress | 15 cells, n=100. Run repeatedly timed out (cat3/cont3) or hit the binary all-zero-positive encoding limitation; 0 solved before abort. Preserved as a computational-feasibility attempt; NOT canonical evidence. Superseded for evidence by QI-004 (n=20, 300s). |
| QI-004 | Scaled noisy motifs with parent-position controls (reduced n=20) | run (interpretation pending) | `docs/experiments/qualitative/QI-004.md` | `causal/configs/experiments/QI004_scaled_motifs_n20.yaml` | `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20/` | Interim Experimentation / Progress | Feasible follow-up to QI-003 (n=20, 300s). 15/15 cells completed, NO timeouts: 1 solved, 12 completed_no_solution, 2 binary `unknown constant` errors; clean_recovery=0 for all. Interpretation deferred. |
| QI-001 greedy | Greedy-folding rerun of QI-001 (3 motifs x 3 modes) | implemented | `docs/experiments/qualitative/QI001_motifs_modes_greedy/` | `causal/configs/experiments/QI001_motifs_modes_greedy.yaml` | `causal/outputs/aba_learning/grid/QI001_motifs_modes_greedy/` | Interim Experimentation / Progress | Greedy-vs-nd comparison; only conceptual change `folding_mode: greedy`. 9 cells, target x2. Run/interpretation by greedy-rerun task. |
| QI-002 greedy | Greedy-folding rerun of QI-002 (minimal truth-table baseline) | implemented | `docs/experiments/qualitative/QI002_minimal_motifs_greedy/` | `causal/configs/experiments/QI002_minimal_motifs_greedy.yaml` | `causal/outputs/aba_learning/grid/QI002_minimal_motifs_greedy/` | Interim Experimentation / Progress | Greedy-vs-nd comparison in the noiseless best case; only change `folding_mode: greedy`. 6 cells, target x2. |
| QI-004 greedy | Greedy-folding rerun of QI-004 (scaled noisy n=20) | implemented | `docs/experiments/qualitative/QI004_scaled_motifs_n20_greedy/` | `causal/configs/experiments/QI004_scaled_motifs_n20_greedy.yaml` | `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20_greedy/` | Interim Experimentation / Progress | Greedy-vs-nd comparison at scaled/noisy setting; only change `folding_mode: greedy`. 15 cells, target x2, 300s timeout (greedy may be costlier). QL3 excluded. |
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