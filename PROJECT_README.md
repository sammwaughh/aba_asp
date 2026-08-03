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
  **M1.3** Buckets 1–2 locked; Bucket 3 H0–H4+H4b are complete / analysed under
  Fabrizio's one-case-at-a-time deterministic-mechanism direction. H5 cautious
  Greedy is deferred; H6/H7 are signposted only; no Bucket 3
  claim is approved. The wider 22 July dimensions are deferred, and M12x/Buckets 1–2
  will not be redone. Primary path:
  `docs/research/milestone_plans/milestone1_high_level_path.md`. M1.3 Approach (method):
  `docs/research/milestone_plans/milestone1_part3/milestone1_part3_approach.md`.
  No M1.4; Milestone 2 has not started.
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
- `docs/report/genai_use_log.md` — factual log of ChatGPT/Cursor assistance.
