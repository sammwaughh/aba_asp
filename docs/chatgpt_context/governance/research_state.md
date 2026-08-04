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

The current empirical implementation remains a **target-wise ABA Learning** pipeline that
converts a data table into ABA background predicates and learns a framework for a chosen target.
The completed work used parent-set and expected-rule comparisons as diagnostic proxies. Under
Fabrizio's 31 July guidance, the immediate RQ1 investigation now studies binary causal
fixtures with non-degenerate stochastic roots and deterministic non-root mechanisms. For
each bounded case, the mechanism/rule reference is fixed before all-target ABALearn runs,
after which the learned rules and traces are described against what the population and
finite sample made available. This remains groundwork, not a proof or implementation of
full causal discovery.

Future target-wise fixtures use lowercase internal identifiers `a`, `b`, `c`, ... while
scientific descriptions may use (A,B,C,\ldots). Existing `xN` evidence is not renamed.
The Python bridge enforces safe Prolog atoms and keeps causal predicates distinct from
learner-generated `alpha_N` assumptions and `c_alpha_N` contraries; the inherited Prolog
engine is unchanged.

The broader dimensions opened on 22 July — missing/partial data, larger controlled graphs,
category counts, non-discrete data, and cross-target graph recovery — remain possible later
Bucket 3 work but are deferred while this deterministic-mechanism foundation is developed.

## Research questions

- **RQ1** — Under which targets, data-availability conditions, graph/mechanism structures,
  and learning strategies can unguided ABA Learning recover mechanism-aligned local rules
  or support recovery of causal structure; what does it recover instead; and which failures
  are strategic versus observationally non-identifiable?
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
- **M1.1 (M11)** — eight-cell metamorphic control; Stages 0–7 **closed**. nd: binary σ/π pass; cat3 σ fails (ablation-supported mechanism). Stage 7 greedy: binary matches nd; cat3 all supersets, rule-level σ restored. Record: `M1.1-parent-position.md`; findings: `milestone1_part1_m11_findings.tex`.

**Bounded conclusion.** The current target-wise pipeline can recover parent sets in selected
idealised cases (especially simple binary and fork cases) but recovery is not robust across
motifs, encodings or modest noisy scaling. **m1.1 (closed):** binary parent-role tracking with
full σ/π invariance under nd; cat3 parent-role tracking when parent feature wins first fold;
cat3 σ-invariance fails under default nd pipeline but is **accounted for** by BK serialisation
+ entailment + assumption commitment; greedy produces a distinct cat3 superset profile. This
characterises what unguided ABA Learning does before causal guidance is added; it does not
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
- The expanded M1.3 must distinguish a learning-strategy failure from an
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

## Next milestone

Milestone 1's goal is a **report-ready account of what causal structure unguided ABA
Learning can recover from controlled tabular data, under which targets, data-availability
conditions, graph/mechanism structures, and learning strategies — and which limitations
are informational rather than strategic**. The completed categorical target-wise work
remains the foundation; the new scope does not yet imply a full causal-discovery
implementation. Primary working path:
`docs/research/milestone_plans/milestone1_high_level_path.md`.  
Expanded Approach:
`docs/research/milestone_plans/milestone1_part2/milestone1_part2_expanded_approach.md`.

- **M1.1** — closed.
- **M1.2 expanded (M12x)** — **closed / analysed:** fresh 18-cell run + Stage-3
  inspection **18/18** (2026-07-20). Record: `docs/experiments/qualitative/M1.2-expanded.md`.
  Inspection: `M1.2-expanded-cell-inspection.md`.
- **M1.3** — **in progress:** Bucket 1 **written / locked**; Bucket 2
  **locked / closed** with Claims 1–2 from M13-C1/C2; Bucket 3 baseline
  **M13-C3 H0 closed**; probes **H1–H7a run / analysed** (**no claim**; includes
  H4b). H5 experimental `greedy_cautious` is **run / analysed**
  (`h5_greedy_cautious.md`); H6 search-cost ablation is **run / analysed**
  (`h6_folding_and_n_ablation.md`); H7a relto vs sechk is **run / analysed**
  (`h7a_relto_vs_sechk.md`); H7b is not started in
  `future_probes.md`. Method:
  `milestone1_part3_approach.md`. Records:
  `docs/experiments/qualitative/M1.3-bucket1-claims.md` (locked);
  `docs/experiments/qualitative/M1.3-bucket2-claims.md` (locked);
  `docs/experiments/qualitative/M1.3-bucket3-claims.md`;
  `docs/experiments/qualitative/M13-C3-binary-collider-and/experiment.md`;
  `docs/experiments/qualitative/M13-C3-binary-collider-and/learning_analysis.md`;
  `docs/experiments/qualitative/M13-C3-binary-collider-and/h1_support_ablation.md`;
  `docs/experiments/qualitative/M13-C3-binary-collider-and/h2_irrelevant_covariate.md`;
  `docs/experiments/qualitative/M13-C3-binary-collider-and/h3_bk_leading_distractor.md`;
  `docs/experiments/qualitative/M13-C3-binary-collider-and/h4_cautious_vs_brave.md`;
  `docs/experiments/qualitative/M13-C3-binary-collider-and/h4b_cautious_split_under_a.md`;
  `docs/experiments/qualitative/M13-C3-binary-collider-and/h5_greedy_cautious.md`.
- **No M1.4** — the widened work remains M1.3. Later large-scale external evaluation
  remains deferred beyond this supervisor-driven controlled investigation.

Then **Milestone 2** (Causal-ABA-guided ABA Learning bridge), informed by the expanded
M1.3. Milestone 2 has not started.
