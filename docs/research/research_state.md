# Research State

Snapshot of where the Causal ABA Learning project stands. For ChatGPT project context; keep
updated as milestones change. Does not duplicate `repo_map.md`, `execution_guide.md`, or
`environment_setup.md` — see those for detail.

## Current goal

Investigate whether **ABA Learning** techniques can be applied to **causal discovery** on
small controlled cases (the MSc project's initial priority). The broader project also
considers the reverse direction (using causal structure to guide ABA Learning), but the
immediate focus is the first direction on toy cases.

## Literature / background status

- `docs/theory/background.tex` and `docs/theory/literature_review.tex` drafted: causal
  graphs / d-separation / Markov + faithfulness; ABA frameworks and stable extensions;
  Causal ABA encoding; ABA Learning (cautious/brave/greedy); the integration gap.
- Paper summaries exist under `docs/theory/paper_summaries/` (Russo et al. 2024;
  Proietti & Toni 2024; De Angelis et al. 2023/2024/2025; Toni 2014).
- Canonical theory source: `docs/theory/theory_primer.md`.

## Conceptual distinctions (keep separate)

- **ABA foundations** — frameworks `⟨L, R, A, contrary⟩`, attacks, stable extensions.
- **ABA Learning** — transforming an ABA framework from background knowledge + E⁺/E⁻ via
  Rote Learning, Folding, Assumption Introduction, Subsumption.
- **Causal ABA / argumentative causal discovery** (Russo et al. 2024) — encoding
  causal-discovery evidence in ABA: `arr/noe/indep` assumptions, d-separation, stable
  extensions ↔ candidate DAGs.
- **Current `aba_asp/causal` implementation** — an ABA Learning pipeline over tabular data
  (parent-set recovery). **Not** the Russo-style Causal ABA encoding.

## Implementation reality

- **Inherited Prolog ABA learner** (repo root: `aba_asp.pl`, `gen.pl`, `folding.pl`,
  `rote_learning.pl`, `asp_engine.pl`, `asp_utils.pl`). Transformation-rule learning with a
  clingo backend.
- **Python causal bridge** (`causal/`): data → ABA background knowledge → per-target
  learning → parent-set metrics; plus a grid harness.
- **ArgCausalDisco**: sibling repo, used only as a data-generation dependency
  (`simulate_discrete_data`, `simulate_linear_continuous_data`).
- **Environment**: verified locally (conda `aba-asp`, Python 3.10; SWI-Prolog 10.0.2;
  clingo 5.8.0) — see `environment_setup.md`.
- **Docs**: `repo_map.md`, `execution_guide.md`, `environment_setup.md` created.

## Startup sequence status

1. Repo orientation — complete.
2. Implementation inspection — complete.
3. Repo / environment / execution docs — created.
4. Environment — verified.
5. Canonical `flies_birds` Prolog learner example — passed (wrote
   `examples/flies_birds.bk.sol.aba`).
6. **QL-001 — next** (to be designed before any new implementation).

## Open conceptual risks

- The current bridge is likely **parent-set recovery via ABA Learning**, not full Causal ABA;
  do not conflate the two.
- QL-001 must be framed **modestly** — a coherence/feasibility probe, not a solution to
  general causal discovery.
- Result interpretation must distinguish **empirical parent recovery** (a learned rule body
  matching true parents) from **causal-argumentative discovery** (stable extensions ↔
  compatible DAGs). The former does not establish the latter.

## Next milestone

Design **QL-001** (research question, setup, metrics, interpretation rule) and have it
reviewed before asking Cursor to implement anything new. Tracked in
`experiment_register.md`.
