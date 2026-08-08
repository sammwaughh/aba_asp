# Causal ABA Learning

This repository supports experimentation for an MSc project on integrating Causal ABA and ABA Learning.

## Project context

The project investigates two directions:

1. Applying ABA Learning to causal discovery.
2. Using causal structure to guide ABA Learning.

## Theory context

The canonical theory context is in:

- `docs/theory/theory_primer.md`
- `docs/theory/background.tex`
- `docs/theory/literature_review.tex`
- `docs/theory/paper_summaries/`

Core PDFs are stored privately under:

- `docs/papers/core/`

## Environment

Local setup (conda `aba-asp`, pip deps, SWI-Prolog, clingo, ArgCausalDisco sibling repo):

- `docs/research/environment_setup.md`

Run commands and success criteria: `docs/research/execution_guide.md`.

## Implementation note

The current `causal/` bridge should be described as **ABA Learning-based, target-wise
learned-rule / parent-set recovery** over tabular data. Do not describe it as full
Russo-style Causal ABA (arrow/no-edge/independence assumptions, d-separation,
stable-extension-as-DAG) unless direct code evidence supports that.

## Experiments

Experiments are documented under `docs/experiments/`:

- Experiment records should use the canonical template `docs/experiments/TEMPLATE.md`.
- The at-a-glance index is `docs/experiments/experiments_summary.md`.
- Milestone 1 Part 1 (M11 / m1.1) is **closed** (Stages 0–7, June 2026): `docs/experiments/qualitative/M1.1-parent-position.md`; supervisor findings `docs/report/findings/milestone1_part1_m11_findings.tex`.
- Milestone 1 Part 2 (M1.2 / M12x) is **closed** (18/18 run + Stage-3, 2026-07-20).
- **Milestone 1 is closed** (8 August 2026). M1.3 Buckets 1–2 retain their locked
  claims; Bucket 3 H0–H7b are complete / analysed (including H4b). The six
  cross-cutting Bucket-3 findings and resulting working recommendations are synthesised in
  `docs/experiments/qualitative/M13-C3-binary-collider-and/findings_for_fabrizio.tex`.
  The individual H-probes remain bounded evidence records; there is no separate locked
  Bucket-3 claim list. Closure path:
  `docs/research/milestone_plans/milestone1_high_level_path.md`. There is no M1.4.
- **Milestone 2 is open.** Its current priority is an intimate understanding of the
  argumentative causal discovery paper and ArgCausalDisco code. Possible integrations
  with ABA Learning will subsequently be tried and tested, without fixing the form or
  sequence of that work in advance. Primary path:
  `docs/research/milestone_plans/milestone2/README.md`.
- ArgCausalDisco is a separate codebase from this checkout's target-wise `causal/` bridge;
  their behaviour and roles must not be conflated.
- Future target-wise fixtures use lowercase internal variable identifiers `a`, `b`,
  `c`, ... (displayed mathematically as (A,B,C,\ldots)); existing `xN` fixtures remain
  supported and unchanged. This is a Python-bridge convention and does not modify the
  inherited Prolog learner.

Each experiment record should capture an ID, research question, theoretical motivation,
setup, exact command, output, interpretation, and next decision. Records are evidence
records, not polished report prose.

## Report support

Report-supporting docs live under `docs/report/`:

- `docs/report/claims_ledger.md` — evidence-to-claim guardrail.
- `docs/report/report_state.md` — interim report section/evidence plan.
- `docs/report/figure_table_index.md` — figure/table provenance.
- `docs/report/genai_use_log.md` — factual log of AI-agent assistance.
