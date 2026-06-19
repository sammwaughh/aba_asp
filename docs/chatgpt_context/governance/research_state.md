# Research State

Snapshot of where the Causal ABA Learning project stands. For ChatGPT project context; keep
updated as milestones change. Does not duplicate `repo_map.md`, `execution_guide.md`, or
`environment_setup.md` — see those for detail.

## Current goal

Learn causal relationships from data in an **argumentative** form by combining **ABA Learning**
and **Causal ABA**. The settled project direction is that **Causal ABA guides ABA Learning**:
causal information (candidate arrows, no-edge claims, conditional-independence evidence,
acyclicity, d-separation) is used as argumentative background knowledge to constrain, prioritise
or interpret ABA Learning transformations. See `docs/report/manuscript/introduction.md` and
`docs/report/manuscript/project_plan.md`.

The current empirical work is the **groundwork** stage (RQ1): a narrower target-wise ABA
Learning pipeline that converts a data table into ABA background predicates, runs ABA Learning
for a chosen target, and compares the variables in learned target-rule bodies against the true
direct parents of a known synthetic graph. This parent-set comparison is a **diagnostic proxy**,
not a proof of causal discovery.

## Research questions

- **RQ1** — When does unguided ABA Learning recover parent variables in learned target rules,
  rather than ancestors, descendants, siblings, correlated non-parents or representation
  artefacts?
- **RQ2** — Can Causal ABA-style evidence and graph constraints guide ABA Learning towards
  rules/frameworks that are more causally meaningful, interpretable, robust or efficient?
- **RQ3** — How does the resulting causally guided ABA Learning bridge compare with
  representative causal-discovery methods on controlled canonical examples?

At this interim stage the main empirical contribution concerns **RQ1**.

## Report / literature / background status

- Five report chapters are drafted under `docs/report/manuscript/` (authoritative `.tex` plus
  ChatGPT `.md` mirrors): `introduction`, `literature_review`, `background`, `experimentation`,
  `project_plan`.
- Literature Review and Background are drafted and reusable; the theory canon remains in
  `docs/theory/background.tex` and `docs/theory/literature_review.tex`.
- Experimentation is drafted from the QL1/QL2/QL3 records; Project Plan sets out Milestones 1–6
  and a 14-calendar-week schedule.
- Paper summaries exist under `docs/theory/paper_summaries/` (Russo et al. 2024; Proietti & Toni
  2024; De Angelis et al. 2023/2024/2025; Toni 2014). Canonical theory source:
  `docs/theory/theory_primer.md`.

## Conceptual distinctions (keep separate)

- **ABA foundations** — frameworks `⟨L, R, A, contrary⟩`, attacks, stable extensions.
- **ABA Learning** — transforming an ABA framework from background knowledge + E⁺/E⁻ via
  Rote Learning, Folding, Assumption Introduction, Subsumption.
- **Causal ABA / argumentative causal discovery** (Russo et al. 2024) — encoding
  causal-discovery evidence in ABA: `arr/noe/indep` assumptions, d-separation, stable
  extensions ↔ candidate DAGs.
- **Current `aba_asp/causal` implementation** — an ABA Learning pipeline over tabular data
  (target-wise parent-set recovery). **Not** the Russo-style Causal ABA encoding.

## Implementation reality

- **Inherited Prolog ABA learner** (repo root: `aba_asp.pl`, `gen.pl`, `folding.pl`,
  `rote_learning.pl`, `asp_engine.pl`, `asp_utils.pl`). Transformation-rule learning with a
  clingo backend; supports non-deterministic (`nd`) and `greedy` folding modes.
- **Python causal bridge** (`causal/`): data → ABA background knowledge → per-target
  learning → parent-set metrics; plus a YAML-configured grid harness (`run_grid.py`).
- **ArgCausalDisco**: sibling repo, used only as a data-generation dependency
  (`simulate_discrete_data`, `simulate_linear_continuous_data`). The QL1–QL3 fixtures are
  purpose-built handcrafted tables, not generic ArgCausalDisco samples.
- **Environment**: verified locally (conda `aba-asp`, Python 3.10; SWI-Prolog 10.0.2;
  clingo 5.8.0) — see `environment_setup.md`.
- **Docs**: `repo_map.md`, `execution_guide.md`, `environment_setup.md` created.

## Experiment status (groundwork / RQ1)

Report labels map to repo ids: **QL1 = QI-001, QL2 = QI-002, QL3 = QI-004**. (The earlier
n=100 scaled attempt was cut; only the reduced n=20 study is canonical and is now QL3.)

- **QL1 (QI-001)** — 9 cells (3 motifs × 3 data modes), tiny 4–5 row handcrafted tables. All 9
  solved. Fork recovered exactly (but the true parent is `x0`, so this is confounded with a
  first-variable preference); chain often recovered the ancestor `x0` instead of the direct
  parent `x1`; collider exact only in binary. Exposed the `x0`/first-column confound and the
  weak-table-design problem.
- **QL2 (QI-002)** — 6 cells (3 motifs × {binary, cat3}), complete noiseless truth tables so the
  true parent is the unique perfect rule. Binary chain/fork recovered exactly; **binary collider
  returned no solution** (although the conjunctive parent rule exists in the table); cat3 chain
  recovered the non-parent `x0`; cat3 collider recovered only one of two parents. Mean
  variable-level F1 ≈ 0.61.
- **QL3 (QI-004, n=20)** — 15 cells (5 structural configs × 3 data modes), small noisy samples,
  parent-position controls. All 15 completed without timeout: 1 solved, 12 completed-no-solution,
  2 binary `unknown constant` errors. The one solved cell (binary chain, `x1`-parent) recovered
  the superset {x0, x1} (F1 0.67). No exact recoveries.
- **Greedy vs nd reruns** (QI-001/QI-002/QI-004 greedy) — switching `folding_mode: nd → greedy`
  is better-or-equal on most axes: greedy is much faster (≈120× at the QL3 scale; QL3 wall
  ≈1233 s → ≈10 s), solve rate ≥ nd (the binary collider no-solution becomes solved+exact),
  net better clean recovery (colliders), with one regression (cat3 fork exact → superset) and no
  recovery change at the noisy n=20 scale. See
  `docs/experiments/qualitative/greedy_vs_nd_qualitative_handoff.md`.
- **M1.1 (M11)** — eight-cell metamorphic parent-position / representation-order control under
  fixed nd folding. Binary: 4/4 exact expected rules; σ and π hold. Cat3: 2/4 exact; σ fails
  (A↔B, D↔C); π holds B↔C only. Stage 3 trace: BK order → first nd-fold literal → entailment
  fork. Status `analysed`. Record: `docs/experiments/qualitative/M1.1-parent-position.md`;
  findings: `docs/report/findings/milestone1_part1_m11_findings.tex`.

**Bounded conclusion.** The current target-wise pipeline can recover parent sets in selected
idealised cases (especially simple binary and fork cases) but recovery is not robust across
motifs, encodings or modest noisy scaling. M1.1 adds that binary parent-role tracking holds under
σ/π controls while cat3 shows encoding-dependent representation-order sensitivity under nd.
This characterises what unguided ABA Learning does before causal guidance is added; it does not
establish causal discovery.

## Open conceptual risks

- The current bridge is **target-wise parent-set recovery via ABA Learning**, not full Causal
  ABA; do not conflate the two.
- Parent-set membership is only a **proxy** for causality. Per supervisor guidance, success
  metrics should be defined more nuanced than "parents appear in the rule body" — by
  constructing inputs (graph + DGP → table) with explicit **expected** learned rules and
  comparing actual outputs against them.
- A learned predictive rule is not automatically a causal rule; recovering an ancestor, sibling
  proxy or partial parent set must be distinguished from exact parent recovery.
- Result interpretation must distinguish **empirical parent recovery** from
  **causal-argumentative discovery** (stable extensions ↔ compatible DAGs). The former does not
  establish the latter.

## Next milestone

**Milestone 1 Part 2 (M1.2)** — greedy vs non-deterministic folding on the m1.1 eight-cell grid.
Write `docs/research/milestone_plans/milestone1_part2_greedy_vs_nondeterministic.md`, rerun under
`folding_mode: greedy`, and compare to the M11 nd baseline (motivated by cat3 σ failure under nd).
Parts 3–4 of Milestone 1 (failure analysis; noise/continuous DGP) follow M1.2. Then **Milestone 2**
(Causal-ABA-guided ABA Learning bridge). Tracked in `experiment_register.md`,
`docs/experiments/experiments_summary.md`, and `docs/report/manuscript/project_plan.md`.
