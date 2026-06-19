# AGENTS.md

This repository supports experimentation for the Causal ABA Learning MSc project.

## Canonical context

The agent should treat `docs/theory/` as the canonical project theory context and
`docs/research/environment_setup.md` as the canonical **local environment** record
(conda env `aba-asp`, pip packages, SWI-Prolog, clingo, ArgCausalDisco path rules).

Do not invent setup steps that contradict `docs/research/environment_setup.md`.

The main theoretical sources are:

- `docs/theory/background.tex`
- `docs/theory/literature_review.tex`
- `docs/theory/theory_primer.md`
- `docs/theory/paper_summaries/`

The PDFs in `docs/papers/core/` are reference material only. Use the summaries and theory files first.

## Role of the agent

The agent should help implement, test, inspect, and document ideas supplied by Samuel.

The agent should not invent new theoretical definitions, experiment results, or report claims.

Before editing code, the agent should:

1. inspect relevant files;
2. state the intended change;
3. identify the expected observable output;
4. avoid unrelated modifications;
5. stop for approval when the task is plan-only or when the change affects inherited ABA Learning engine semantics.

## Current implementation distinction

Preserve this distinction in all code comments, documentation, experiment records, and summaries:

- **ABA foundations**: frameworks, rules, assumptions, contraries, attacks, and semantics.
- **ABA Learning / ABALearn**: transformation-rule learning from background knowledge and positive/negative examples.
- **Causal ABA / argumentative causal discovery**: Russo-style causal ABA with arrow/no-edge/independence assumptions, d-separation reasoning, and stable extensions corresponding to candidate DAGs.
- **Current `aba_asp/causal` implementation**: an ABA Learning-based bridge over tabular data, currently best treated as target-wise learned-rule / parent-set recovery.

Do not describe the current implementation as full Russo-style Causal ABA unless direct code evidence shows that it implements the relevant `arr`/`noe`/`indep`, d-separation, and stable-extension-as-DAG machinery.

## Experimental priority

The current experimental priority is Milestone 1: close the unguided parent-set diagnostic, then design the Causal-ABA-guided bridge.

Key experiment records:

- `docs/experiments/qualitative/QL-001.md` — qualitative inspection of ABA Learning on minimal causal motifs (realised by QI series).
- `docs/experiments/qualitative/M1.1-parent-position.md` — Milestone 1 Part 1 (M11); `analysed`.
- **Next:** Milestone 1 Part 2 (M1.2) — greedy vs nd on the m1.1 grid; planning doc `docs/research/milestone_plans/milestone1_part2_greedy_vs_nondeterministic.md` (Samuel).

## Experiment documentation rule

All experiments should be documented under `docs/experiments/`.

Every experiment record must use:

- `docs/experiments/TEMPLATE.md`

After creating or updating an experiment record, also update the at-a-glance views:

- `docs/experiments/experiments_summary.md`
- `docs/research/experiment_register.md`

Experiment records are **evidence records**, not polished report prose.

They should record:

- facts;
- exact commands;
- config paths;
- artefact paths;
- files changed;
- diffs or diff summaries;
- outputs and outcome summaries;
- quantitative/metric summaries and tables;
- qualitative learned-rule examples;
- failure modes;
- supported claims;
- unsupported claims;
- next decisions.

## Report-writing rule

Cursor should not write polished report prose unless explicitly asked.

For report support, Cursor should record facts, commands, artefacts, diffs, and bounded interpretation notes. Samuel and ChatGPT will use these records for report drafting and review.

The report-writing workflow is:

1. Cursor records experiment evidence in `docs/experiments/<ID>.md`.
2. Samuel reviews and corrects the experiment record.
3. ChatGPT drafts candidate report prose from reviewed records.
4. Samuel verifies, edits, and authors the final submitted report.
5. Claims are checked against `docs/report/claims_ledger.md`.

## Report-supporting docs

Use these files for report-writing support:

- `docs/report/manuscript/` — report chapter sources (`.tex`) and ChatGPT mirrors (`.md`).
- `docs/report/README.md` — index for report layout and workflow.
- `docs/report/claims_ledger.md` — evidence-to-claim guardrail.
- `docs/report/report_state.md` — interim report section/evidence plan.
- `docs/report/figure_table_index.md` — figure/table provenance.
- `docs/report/genai_use_log.md` — factual log of ChatGPT/Cursor assistance.

## Files to treat carefully

Do not modify casually:

- inherited Prolog engine files:
  - `aba_asp.pl`
  - `gen.pl`
  - `folding.pl`
  - `rote_learning.pl`
  - `asp_engine.pl`
  - `asp_utils.pl`
  - `io.pl`
  - `cc.pl`
  - `configs/*.pl`
- theory files in `docs/theory/`;
- generated outputs under `causal/outputs/`;
- `.cursor/rules/*.mdc`;
- existing benchmark/paper artefact trees.

Cursor-specific behavioural rules are stored in `.cursor/rules/`. Follow those rules when working in Cursor.