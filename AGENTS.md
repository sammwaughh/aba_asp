# AGENTS.md

This repository supports experimentation for the Causal ABA Learning MSc project.

The agent should treat `docs/theory/` as the canonical project context and
`docs/research/environment_setup.md` as the canonical **local environment** record (conda env
`aba-asp`, pip packages, SWI-Prolog, clingo, ArgCausalDisco path rules). Do not invent setup
steps that contradict that file.

The main theoretical sources are:

- `background.tex`
- `literature_review.tex`
- `theory_primer.md`
- `paper_summaries/`

The PDFs in `docs/papers/core/` are reference material only. Use the summaries and theory files first.

The agent should not invent new theoretical definitions. It should help implement, test, document, and inspect ideas supplied by the user.

The initial experimental priority is to investigate whether ABA Learning techniques can be applied to causal discovery on small controlled cases.

Before editing code, the agent should inspect relevant files, state the intended change, identify expected observable output, and avoid unrelated modifications.

All experiments should be documented under `docs/experiments/`.

Cursor-specific behavioural rules are stored in `.cursor/rules/`. Follow those rules when working in Cursor.