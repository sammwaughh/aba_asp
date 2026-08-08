# Research State

Snapshot of where the Causal ABA Learning project stands. For ChatGPT project context; keep
updated as milestones change. Does not duplicate `repo_map.md`, `execution_guide.md`, or
`environment_setup.md` — see those for detail.

## Current goal

Learn causal relationships from data in an **argumentative** form by investigating how
**ABA Learning** and **argumentative causal discovery** might be combined. The form of that
integration is deliberately undecided. The existing manuscript introduction and project
plan predate this milestone-opening decision and must not be treated as an approved
implementation design.

The current empirical implementation remains a **target-wise ABA Learning** pipeline that
converts a data table into ABA background predicates and learns a framework for a chosen
target. Milestone 1 used parent-set and expected-rule comparisons as diagnostic proxies and
then closed with a trace-backed account of what the learner does on controlled fixtures.
Its final Bucket-3 synthesis is
`docs/experiments/qualitative/M13-C3-binary-collider-and/findings_for_fabrizio.tex`.
This evidence remains groundwork, not a proof or implementation of full causal discovery.

Future target-wise fixtures use lowercase internal identifiers `a`, `b`, `c`, ... while
scientific descriptions may use (A,B,C,\ldots). Existing `xN` evidence is not renamed.
The Python bridge enforces safe Prolog atoms and keeps causal predicates distinct from
learner-generated `alpha_N` assumptions and `c_alpha_N` contraries; the inherited Prolog
engine is unchanged.

Milestone 1 is now **closed** (8 August 2026). The broader dimensions opened on 22 July —
missing/partial data, larger controlled graphs, category counts, non-discrete data, and
cross-target graph recovery — were not required for closure. They remain possible later
questions, but they are not unfinished Bucket-3 obligations and are not automatically part
of Milestone 2.

Milestone 2 is **open**. Its current priority is an intimate understanding of the
argumentative causal discovery paper and ArgCausalDisco code. Some forms of integration
with ABA Learning will then be tried and tested. No further procedure or architecture is
fixed by the milestone approach. See
`docs/research/milestone_plans/milestone2/README.md`.

## Research questions

- **RQ1** — Under which targets, data-availability conditions, graph/mechanism structures,
  and learning strategies can unguided ABA Learning recover mechanism-aligned local rules
  or support recovery of causal structure; what does it recover instead; and which failures
  are strategic versus observationally non-identifiable?
- **RQ2** — How, if at all, can argumentative causal discovery and ABA Learning be
  integrated usefully?
- **RQ3** — How should any integration that is actually developed be understood and
  evaluated relative to its intended purpose?

Milestone 1 closes the project's current empirical account of **RQ1**. Milestone 2 now
opens **RQ2**; RQ3 remains later evaluation work.

## Report / literature / background status

- Five report chapters are drafted under `docs/report/manuscript/` (authoritative `.tex` plus
  ChatGPT `.md` mirrors): `introduction`, `literature_review`, `background`, `experimentation`,
  `project_plan`.
- Literature Review and Background are drafted and reusable; the theory canon remains in
  `docs/theory/background.tex` and `docs/theory/literature_review.tex`.
- Experimentation is drafted from the QL1/QL2/QL3 records; the completed M1.3 synthesis is
  additional supervisor-facing evidence. The existing Project Plan's Milestones 1–6 and
  14-calendar-week schedule predate the M1 closure/M2 opening and require revision before
  final use.
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
- **Target-wise naming:** safe lowercase Prolog atoms are supported, including the new
  `a`, `b`, `c`, ... convention and the preserved `x0`, `x1`, ... convention. Current
  target-wise body diagnostics resolve variables against fixture metadata rather than
  the locked legacy `xN` metric parser.
- **ArgCausalDisco**: sibling repo, used only as a data-generation dependency
  (`simulate_discrete_data`, `simulate_linear_continuous_data`). The QL1–QL3 fixtures are
  purpose-built handcrafted tables, not generic ArgCausalDisco samples.
- **Environment**: verified locally (conda `aba-asp`, Python 3.10; SWI-Prolog 10.0.2;
  clingo 5.8.0) — see `environment_setup.md`.
- **Docs**: `repo_map.md`, `execution_guide.md`, `environment_setup.md` created.

## Milestone 1 experiment status (closed RQ1 groundwork)

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
- **M1.1 (M11)** — eight-cell metamorphic control; Stages 0–7 **closed**. nd: binary σ/π pass; cat3 σ fails (ablation-supported mechanism). Stage 7 greedy: binary matches nd; cat3 all supersets, rule-level σ restored. Record: `M1.1-parent-position.md`; findings: `milestone1_part1_m11_findings.tex`.

**Bounded conclusion.** The current target-wise pipeline can recover parent sets in selected
idealised cases (especially simple binary and fork cases) but recovery is not robust across
motifs, encodings or modest noisy scaling. **m1.1 (closed):** binary parent-role tracking with
full σ/π invariance under nd; cat3 parent-role tracking when parent feature wins first fold;
cat3 σ-invariance fails under default nd pipeline but is **accounted for** by BK serialisation
+ entailment + assumption commitment; greedy produces a distinct cat3 superset profile. This
characterises what unguided ABA Learning does before causal guidance is added; it does not
establish causal discovery.

**M1.3 Bucket-3 closure.** H0–H7b are complete and analysed. The cross-probe synthesis
records six bounded findings: Greedy enumerates positive value patterns and retains all
measured predictors; nd latches onto the first BK predictor; brave nd can accept
non-functional targets through ground assumption choices whereas cautious nd blocks the
tested construction; the current unary exact-value encoding makes larger folding-token
ceilings replay failed searches; distinct value patterns fix the recorded search while row
multiplicity adds cost; and `sechk` produces a first-predictor-only brave profile and a more
expensive cautious profile than `relto` on the tested cells. Canonical source:
`findings_for_fabrizio.tex`. These are bounded findings, not full causal-discovery results.

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
- Any later integration analysis must distinguish a learning-strategy failure from an
  **identifiability/information limitation**. Markov-equivalent or otherwise
  observationally indistinguishable structures cannot be separated merely by changing
  the learner.
- Future fixture design requires explicit graph–mechanism compatibility and verified
  marginal/conditional-independence statements. Fabrizio's 22 July fork/chain example
  remains a theory question to formalise, not a settled claim.
- Deterministic non-root mechanisms introduce structural zero-probability assignments.
  Root stochasticity and DAG factorisation do not by themselves establish ordinary
  faithfulness; every population fixture requires an exact, fixture-specific audit.
- Mechanism recoverability, predictive rule recovery, and graph-orientation recovery are
  distinct. In particular, the two-node copy relation (A \to B, B:=A) supports symmetric
  observational prediction and does not identify its direction without additional
  assumptions or graph structure.
- A future deterministic fixture must separate its full truth table, population-supported
  parent configurations, sample-observed configurations, and learner-visible inputs.
  Root targets have no deterministic causal rule over other observed variables.
- “Missing data” is not yet operationalised; missing rows, cell values, variables, and
  combinations are distinct interventions.

## Current milestone

**Milestone 1 is closed.** Its goal was a report-ready account of what causal structure
unguided ABA Learning can recover from controlled tabular data and which observed limits
are strategic, representational, data-driven, or informational.

- **M1.1** — closed.
- **M1.2 expanded (M12x)** — closed / analysed; fresh 18-cell run and Stage-3
  inspection 18/18.
- **M1.3** — closed. Bucket 1 has four locked claims; Bucket 2 has two locked claims;
  Bucket 3 H0–H7b are complete / analysed and consolidated into six cross-cutting
  findings in `findings_for_fabrizio.tex`. No separate locked Bucket-3 claim list was
  created.
- **M1.4** — does not exist.

**Milestone 2 is the active milestone.** The present task is to understand the
argumentative causal discovery paper and ArgCausalDisco intimately. Possible integrations
with ABA Learning will then be tried and tested. The milestone does not currently specify
an architecture, deliverable sequence, experimental method, or number of investigations.
Primary path: `docs/research/milestone_plans/milestone2/README.md`.
