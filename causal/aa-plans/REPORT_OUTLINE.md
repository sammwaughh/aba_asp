# Interim Report — Outline and Claim/Evidence Map

**Read after:** [`meta-understanding-plan.md`](meta-understanding-plan.md) — **Phase 2** (report shape and claim map).

**Status:** living document. Last updated: 2026-05-24.
**Companion docs:** `EXPERIMENTS_PLAN.md`, `METRICS.md`, `INFRA.md`, `LIT_REVIEW_NOTES.md`.

This document is the **skeleton of the interim report** and the **contract** between experiments and claims. Every claim in the report is paired here with the figure/table that supports it, the experiment that produced that figure, and the spec doc that defines that experiment.

Target length: **5,000–10,000 words / 10–20 pages, 11 pt LaTeX**. We will aim for the **upper half (~8,000 words / ~15 pages)** because the audience is the supervisor + a literature-review mark, and breadth matters for the lit review and background sections.

---

## 1. Title (working)

> **Learning argumentative rules from data: an empirical study of ABA-ASP as a hint generator for argumentative causal discovery**
> *Interim Project Report*

(Subject to a tightening pass before submission.)

---

## 2. Section list with target word counts

| § | Section | Target words | Pages (≈) |
|---|---------|-------------:|----------:|
| 1 | Introduction | 700 | 1.0 |
| 2 | Literature review: causal discovery | 2,200 | 3.0 |
| 3 | Background: ABA, ABA-ASP learning, and Causal ABA | 1,500 | 2.0 |
| 4 | Methods | 1,000 | 1.5 |
| 5 | Experiments | 2,300 | 4.0 |
| 6 | Discussion | 700 | 1.0 |
| 7 | Plan for the remainder of the project | 600 | 1.0 |
| 8 | Conclusion | 250 | 0.5 |
| | **Total** | **~9,250** | **~14 pp** |
| App. | Appendices (configs, ablation tables, extra figures, reproducibility hashes) | (uncounted) | 2–4 |

The page totals are with 11 pt LaTeX, single-column, ≈600 words/page. Figures consume ~0.3–0.5 page each and are accounted for in the per-section breakdown.

---

## 3. Section-by-section plan

### §1 — Introduction (≈700 words)

**Purpose.** Set the problem and tee up the contributions.

**Beats:**

1. The causal-discovery problem in one paragraph: from observational data to (P)DAG; why it is hard (Markov equivalence; confounding; sample limits).
2. The argumentative angle: why arguments and defeasibility are a natural fit for noisy causal evidence (and a one-line nod to ABA / Causal ABA).
3. **The hypothesis of this project**: ABA-ASP, a symbolic learner that produces *rules* with assumptions and contraries, can serve as a **structural-hint generator** for Causal ABA, beyond what conditional-independence tests alone provide.
4. The three research questions (RQ1/RQ2/RQ3) as bullet points.
5. The contributions of this interim report:
   - C1: a literature survey of causal discovery situating argumentative methods.
   - C2: a self-contained background on ABA, ABA-ASP learning, and Causal ABA.
   - C3: a characterisation of ABA-ASP as a learner on five known DGPs with 30-seed variance bars and n-scaling curves.
   - C4: an implied-skeleton method that turns ABA-ASP δ-rules into a candidate graph, with baselines.
   - C5: a preliminary bridge experiment showing how δ-rule-derived hints interact with Causal ABA, plus a roadmap for completing the benchmark.
6. Outline of the rest of the document.

**Figures/tables in this section:** F1 — pipeline schematic (the canonical block diagram).

---

### §2 — Literature review: causal discovery (≈2,200 words)

**Purpose.** Situate the project; give the reader a self-contained map of causal-discovery families and where argumentative methods fit. See `LIT_REVIEW_NOTES.md` for the reading plan.

**Beats:**

1. Foundations: SCMs and DAGs (Pearl; Spirtes-Glymour-Scheines). Identifiability and Markov equivalence (~250 w).
2. Constraint-based discovery: PC and FCI; conditional-independence tests; faithfulness and its failures (~400 w).
3. Score-based discovery: GES, MMHC, NOTEARS; continuous optimisation tricks; pitfalls under non-Gaussianity (~400 w).
4. Hybrid and logical approaches: brief survey, ASP-based methods, MAXSAT formulations (~250 w).
5. **Argumentative causal discovery**: Causal ABA and its lineage; how arguments encode discovery decisions; comparison vs. constraint-based methods (~500 w). *This is the central paragraph block.*
6. ABA learning and our angle: ABA-ASP as a *learner* rather than a *reasoner*; its position vis-à-vis ILP and ASP-based learners (~250 w).
7. Closing paragraph: gap statement → the bridge we are testing.

**Figures/tables in this section:** none required; a small *families* table (T0) may help readers and is in scope if space allows.

**References needed:** see `LIT_REVIEW_NOTES.md §2` (reading list).

---

### §3 — Background: ABA, ABA-ASP learning, and Causal ABA (≈1,500 words)

**Purpose.** Give the reader enough formal background that §5 makes sense without external lookup.

**Beats:**

1. ABA in 200 words: assumptions, contraries, rules, the ABAF tuple, attacks, admissible/grounded extensions. (~200 w).
2. ABA-ASP learning: input (BK + E+ + E−), output (δ-rules and possibly new assumptions/contraries via folding/assumption-introduction). The folding-tokens budget; what `nd` folding does; what "No solution found" means (~500 w).
3. Causal ABA: input contract (CI facts; possibly preferences), output (graph or set of admissible graphs), semantics, and what makes it argumentative rather than purely constraint-based (~500 w).
4. The bridge we test (Alt 3): how a learned δ-rule body could be turned into a hint argument; what we expect to gain over CI-only (~300 w).

**Figures/tables in this section:** F-bg-1 — a tiny worked example of ABA-ASP learning on a 2-row table (handcrafted, derived from `test_simple_4_samples`). F-bg-2 — a tiny worked example of Causal ABA on a 3-node CI input (subject to Phase A of E10).

---

### §4 — Methods (≈1,000 words)

**Purpose.** Specify how we ran our experiments without dragging implementation detail into §5. Most of this content already lives in `METRICS.md` and `INFRA.md`; here we summarise.

**Beats:**

1. The DGP zoo (G3-chain, G3-fork, G3-collider, G4-forkchain, G4-hub) — Table T-meth-1 — with discrete vs continuous variants (~200 w).
2. Data generation: `simulate_discrete_data` / `simulate_linear_continuous_data`, noise, seed control (~150 w).
3. BK construction: `generate_aba_background_knowledge`, target exclusion, quantile binning, naming conventions (~200 w).
4. E+ / E− definition: `pick_target_variable` (discrete) vs **median split** (continuous), with the rationale (~150 w).
5. Learner: ABA-ASP via `run_prolog_aba_asp`, default `folding_steps=15`, `nd` folding (~100 w).
6. Metrics panel: outcome category, body-parent precision/recall/F1, off-graph rate, ancestor-only rate, Python-Horn vs Prolog-aware coverage, implied-skeleton metrics — point to Table T1 (defined in §5) (~150 w).
7. Variance and reporting: 30 seeds per cell, median + IQR, fraction-solved annotated on every aggregate (~50 w).

**Figures/tables in this section:** T-meth-1 (DGP zoo); F-meth-1 (sample BK + δ-rule, mini-example).

---

### §5 — Experiments (≈2,300 words)

**Purpose.** Answer RQ1, RQ2, and (preliminarily) RQ3. The structure mirrors the research questions.

#### §5.1 RQ1 — Existence: do δ-rule bodies cite the true parents? (~600 w)

- **Setup recap**: E01 — single seed per (DGP, target) qualitative case study; refers back to §4.
- **Cases discussed**:
  - G3-chain (continuous, n=8): the clean case — one δ-rule, perfect coverage. *(Already produced; `cont_collider_8_x2.bk.sol.aba` for analogue.)*
  - G3-fork (continuous, n=6, target x2): the **No-solution-found** case. Explain why and what it implies.
  - G3-collider (continuous, n=8, target x2): one clean δ-rule citing only one parent — discuss what gets *missed*.
  - One discrete contrast from `test_01_discrete_chain_6_samples` showing **value-specific** rules.
- **What we learn**: ABA-ASP can produce body-parent-correct rules but also produces *off-graph* and *no-solution* outcomes systematically; these are real findings, not bugs.

**Figures:** F2 — case-study panel: one mini-card per case (graph, δ-rules, body-parent indicator).

#### §5.2 RQ2 — Robustness (~900 w)

Three sub-sections, each one paragraph + one figure or table.

##### §5.2.1 Seed stability (E02). ~250 w.
- 30 seeds × 5 DGPs × 3 targets × n=25; report `body_parent_f1` and `fraction_solved`.
- **Claim**: variance is real and substantial at small n; some DGP/target combinations are bimodal.

**Figure:** F3 — boxplots of `body_parent_f1` per (DGP, target), with fraction-solved annotated.

##### §5.2.2 Sample-size scaling (E03). ~300 w.
- n ∈ {6, 12, 25, 50, 100, 200} across DGP zoo, 30 seeds.
- **Claim**: F1 increases with n; there is an elbow around n ≈ 25–50 for 3-node DGPs and ≈ 50–100 for 4-node DGPs. Wall-clock grows super-linearly with n at fixed `folding_steps`.

**Figure:** F4 — n-scaling curves of `body_parent_f1` (median + IQR), one panel per DGP.

##### §5.2.3 Structural sweep + ablations (E04, E06, E07). ~350 w.
- Across the DGP zoo at fixed n: how does `offgraph_rate` vary by structure (chain vs fork vs collider vs hub)?
- Ablations:
  - **Binning** (E06): `body_parent_f1` over `bins × strategy × example_split`.
  - **Learner** (E07): `body_parent_f1` over `folding_steps × folding_mode`.

**Figure:** F5 — structural-sweep bar chart: side-by-side `body_parent_f1` and `offgraph_rate` per DGP.
**Tables:**
- T1a — binning ablation.
- T1b — learner ablation.

#### §5.3 RQ3 — Bridge to Causal ABA (~800 w)

##### §5.3.1 Implied skeleton (E09). ~450 w.

- Method (defined in `METRICS.md §3.7`): union body-vars per target → undirected skeleton → directional rules D1 and D2 → P/R/F1 against G\*.
- Baselines on the same data: PC (with Fisher-z for continuous, χ² for discrete), and "fully connected" trivial baseline.
- **Claim**: implied-skeleton F1 tracks `body_parent_f1` but with a sharper structural interpretation; D2 (conservative direction) consistently beats D1 on confounder DGPs (because D1 over-orients).

**Figure:** F6 — implied-skeleton F1 vs n per DGP; D1 vs D2 vs PC baseline.

##### §5.3.2 Bridge preliminary (E10). ~350 w.

- Phase A: brief note on Causal ABA API and how we drive it (one short paragraph).
- Phase D: small slice — 1 DGP (G3-chain or G3-collider, depending on Phase A feasibility), n ∈ {25, 100}, 30 seeds, two bridge modes (`ci_only` vs `ci_plus_hints`).
- **Claim**: bridge hints *change* Ĝ in interpretable ways; the directional precision improves on a subset of cases; clear failure modes are listed.
- **Honest scope statement**: this is preliminary; the full benchmark is post-interim.

**Figure:** F7 — single panel: SHD or directed F1 vs DGP, `ci_only` vs `ci_plus_hints`, 30-seed boxplots.
**Table:** T2 — summary statistics for the bridge slice (median, IQR, fraction-solved, runtime).

**Roadmap call-out:** this section ends with an inset box listing exactly what remains to complete RQ3, pointing forward to §7.

---

### §6 — Discussion (≈700 words)

**Purpose.** Interpret the findings.

**Beats:**

1. When ABA-ASP behaves well: clean structures, sufficient n, binning that captures the signal.
2. When it fails *non-trivially*: confounder targets at small n produce No-solution-found; colliders produce "missing one parent"; small n produces value/bin-specific rules with low generality.
3. **The Python-Horn vs Prolog-aware coverage gap**: a finding in its own right; what it reveals about ABAF assumption machinery vs first-pass Horn entailment.
4. Implications for the bridge: where we expect δ-rule hints to help (structures where CI tests are weak: small n, weak edges) and where they may mislead (confounder targets with assumption-laden rules).
5. Threats to validity:
   - Tiny graphs (≤4 nodes) — see Limitations.
   - One simulator family (linear Gaussian, multinomial discrete).
   - One CI test family (in baselines).
   - Variable-stripping heuristic in `body_vars` is approximate.
6. What we are most confident in vs least confident in.

**Figures/tables:** none specific; may reuse F5 / F6 for emphasis.

---

### §7 — Plan for the remainder of the project (≈600 words)

**Purpose.** Show the supervisor a credible path from interim to final.

**Beats:**

1. Complete E10 benchmark: enlarge DGPs (4–6 nodes), enlarge n grid, multiple CI tests, full Causal ABA bridge.
2. Extend the bridge: weighted hints (confidence from `body_parent_f1` per cell), preference orderings in Causal ABA.
3. Stress-test under latent confounders (FCI territory).
4. Consider one real-world or semi-synthetic dataset.
5. Possible secondary contribution: a calibrated confidence score on δ-rules using Prolog-aware coverage and assumption count.

**Timetable:** rough Gantt-style table T-plan-1 with weeks remaining and milestones.

---

### §8 — Conclusion (≈250 words)

**Purpose.** Two short paragraphs restating contributions C1–C5 in the past tense, and one paragraph reasserting the central hypothesis as a near-term testable conjecture.

---

### Appendices (≈2–4 pages, uncounted)

- **A. Configurations.** Listings of the YAMLs for E01, E02, E03 in a compact form.
- **B. Extra ablation tables.** E05 (noise) and E08 (BK content) — the appendix-bound experiments.
- **C. Reproducibility.** Code commit, SWI-Prolog version, ArgCausalDisco commit, run hash, command lines.
- **D. Extended case studies.** Per-DGP δ-rule listings for the seed-mode of E02 (i.e. the most "typical" seed).
- **E. Implied-skeleton method.** Formal pseudocode for D1 and D2, with a worked example.

---

## 4. Figure and table inventory

### 4.1 Figures

| ID | Slug | Section | Source experiment | Source spec |
|----|------|---------|-------------------|-------------|
| F1 | `pipeline_schematic` | §1 | N/A (drawn) | — |
| F2 | `case_studies_panel` | §5.1 | E01 | `experiments/E01_sanity.md` |
| F3 | `seed_stability_box` | §5.2.1 | E02 | `experiments/E02_seed_robustness.md` |
| F4 | `n_scaling_curves` | §5.2.2 | E03 | `experiments/E03_sample_scaling.md` |
| F5 | `structural_sweep_bars` | §5.2.3 | E04 (data from E02) | `experiments/E04_structural_sweep.md` |
| F6 | `implied_skeleton_f1` | §5.3.1 | E09 | `experiments/E09_implied_skeleton.md` |
| F7 | `bridge_prelim` | §5.3.2 | E10 (Phase D) | `experiments/E10_bridge_to_causal_aba.md` |
| F-bg-1 | `aba_asp_worked_example` | §3 | N/A (handcrafted) | — |
| F-bg-2 | `causal_aba_worked_example` | §3 | N/A (post Phase A) | `experiments/E10_*.md` |
| F-meth-1 | `bk_and_delta_mini` | §4 | E01 | — |

### 4.2 Tables

| ID | Slug | Section | Source experiment | Source spec |
|----|------|---------|-------------------|-------------|
| T0 | `discovery_families` | §2 (optional) | N/A | — |
| T-meth-1 | `dgp_zoo` | §4 | N/A | `EXPERIMENTS_PLAN.md §7` |
| T1a | `binning_ablation` | §5.2.3 | E06 | `experiments/E06_binning.md` |
| T1b | `learner_ablation` | §5.2.3 | E07 | `experiments/E07_learner_ablation.md` |
| T2 | `bridge_summary` | §5.3.2 | E10 | `experiments/E10_*.md` |
| T-plan-1 | `remaining_timetable` | §7 | N/A | — |

### 4.3 Style and provenance

- All figures saved to `causal/experiments/figures/<ID>_<slug>.{png,pdf}`.
- All tables saved to `causal/experiments/tables/<ID>_<slug>.{csv,tex}`.
- Captions include the **experiment ID**, the **config hash**, and the **number of seeds**.
- Colour palette: ColorBrewer "Set2" for categorical; one consistent palette across the report.
- Font: 10pt for axis labels; 9pt for legends; 11pt for figure captions in LaTeX.

---

## 5. Claim → evidence map (the contract)

This table is the **single most important** part of this document. Each row says: "this claim in the report is justified by this evidence." If a claim has no row, it is not in the report.

| Claim (paraphrased) | §  | Figure/Table | Experiment | Spec |
|---------------------|----|--------------|------------|------|
| ABA-ASP can produce a perfectly body-parent-correct δ-rule on small clean data. | §5.1 | F2 | E01 (chain, collider) | `E01_sanity.md` |
| ABA-ASP frequently returns "No solution found" on confounder-target cells at small n. | §5.1 | F2; F3 fraction_solved | E01, E02 | `E01_*.md`, `E02_*.md` |
| Body-parent F1 has high seed variance at n=25; some DGP/target combos are bimodal. | §5.2.1 | F3 | E02 | `E02_*.md` |
| Body-parent F1 increases with n; elbow ≈ 25–50 for 3-node DGPs. | §5.2.2 | F4 | E03 | `E03_*.md` |
| Off-graph rate is structurally distributed (higher for confounder/collider targets). | §5.2.3 | F5 | E04 (data from E02) | `E04_*.md` |
| Binning at quantile-2 dominates other choices on body-parent F1. | §5.2.3 | T1a | E06 | `E06_*.md` |
| Folding budget > 15 buys little; nd vs greedy differ chiefly on `fraction_solved`. | §5.2.3 | T1b | E07 | `E07_*.md` |
| Python-Horn vs Prolog-aware coverage gap is non-zero when assumptions are present. | §6 | (number-callout) | E02 + E07 | `METRICS.md §3.5` |
| Implied skeleton from δ-rules has F1 above the trivial "fully connected" baseline. | §5.3.1 | F6 | E09 | `E09_*.md` |
| D2 (conservative direction) consistently beats D1 on confounder DGPs. | §5.3.1 | F6 | E09 | `E09_*.md` |
| Bridge hints **change** Ĝ in interpretable ways on a small slice. | §5.3.2 | F7, T2 | E10 (Phase D) | `E10_*.md` |
| Where bridge hints help most: structures with weak edges and small n. | §6 (discussion) | F7 + cross-ref to F4 | E10 + E03 | `E10_*.md`, `E03_*.md` |
| RQ3 is on track to be answered by the final report; here is the path. | §7 | T-plan-1 | N/A | `EXPERIMENTS_PLAN.md §5` |

If a result during P2/P3 contradicts a claim, we delete the claim or revise it — and update this table.

---

## 6. Writing order and review gates

A pragmatic writing order, so prose progresses while experiments run:

1. **§2 (literature review)** — written in parallel with P2 runs. Doesn't depend on experiment outcomes.
2. **§3 (background)** — written in parallel with §2. Self-contained.
3. **§4 (methods)** — written once `METRICS.md` and `INFRA.md` are finalised.
4. **§5 (experiments)** — written **after** each sub-experiment completes; do not start §5.1 until E01 figure is in `figures/`, etc.
5. **§1 (introduction)** — written last among the long sections, because it must reflect §5's actual findings.
6. **§6 (discussion)** and **§7 (plan)** — after §5 is complete.
7. **§8 (conclusion)** — at the very end.

**Internal review gates:**

- **Gate A (after §2 and §3):** supervisor read-through of literature and background.
- **Gate B (after §5):** supervisor read-through of experiments.
- **Gate C (full draft):** supervisor read-through of the whole report.

---

## 7. Open issues (parking lot)

- Should we include a small "decision graph" in §1 that walks the reader from the supervisor's pipeline (known DAG → data → learn → bridge) to our RQs? *Default: yes, as F1.*
- Should the literature review come **before** or **after** the background? *Default: before, so the reader sees the field first and then dives into our chosen tools.*
- Do we have space for a one-page comparison of Causal ABA against PC/GES on the same DGPs as a non-bridge baseline? *Default: only if space permits; appendix otherwise.*
- Should we adopt LaTeX style file `acmart` (or institutional template)? *Open; the institution's template wins by default.*

---

## 8. Drafting checklist (for Session B and later)

When we move into writing prose in agent mode:

- [ ] Each section's word count is within ±15% of the target.
- [ ] Every claim in §5 has a row in the claim/evidence table.
- [ ] Every figure has the experiment ID and seed count in its caption.
- [ ] Every table has the config hash in its footer.
- [ ] No undefined symbols; all formal notation introduced in §3 or §4.
- [ ] Bibliography compiled (target ≥ 30 references; see `LIT_REVIEW_NOTES.md`).
- [ ] All figures regenerable from `analysis.py` invocations recorded in `figures/MANIFEST.md`.
