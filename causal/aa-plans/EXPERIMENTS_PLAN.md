# Experiments Plan — Master Document

**Read after:** [`meta-understanding-plan.md`](meta-understanding-plan.md) — **Phase 1** (start here for the spec set).

**Status:** living document. Last updated: 2026-05-24.
**Owner:** Sam.
**Audience:** us (executing this plan in agent mode) and the supervisor (for sign-off).
**Companion docs:** `meta-understanding-plan.md` (reading guide), `METRICS.md`, `INFRA.md`, `REPORT_OUTLINE.md`, `LIT_REVIEW_NOTES.md`, and the per-experiment specs in `experiments/E0X_*.md`.

---

## 1. Vision

We are building, over the remainder of the project, a small but rigorous demonstration that **ABA-ASP learning can serve as a structural-hint generator for argumentative causal discovery (Causal ABA)**.

The **interim report** demonstrates three things:

1. We understand the **literature** of causal discovery and where argumentative approaches sit within it.
2. We have **characterised ABA-ASP as a learner** on small, known data-generating processes (DGPs), with proper variance bars and ablations.
3. We have **begun to test the bridge** from learner output to causal-graph recovery, and have a clear roadmap for finishing that bridge.

The pipeline we are studying is:

```
known DAG G*  →  simulate data  →  Background Knowledge (BK) + E+/E-
              →  ABA-ASP learning  →  δ-rules per target
              →  (RQ1/RQ2: characterise)
              →  (RQ3: bridge to Causal ABA → Ĝ; compare to G*)
```

This document sets out the **research questions**, the **doctrine** under which we will run experiments, the **phase plan**, the **milestone gates**, the **risks**, and an **index of the supporting specs**. It is the only place where the high-level commitments live; downstream docs refine them.

---

## 2. Research questions and success criteria

| RQ | Question | Interim-report success criterion |
|----|----------|-----------------------------------|
| **RQ1 (Recover)** | Given E+/E− derived from a known DGP, do ABA-ASP δ-rule **bodies cite the true causal parents** of the target? | We can show qualitatively (case studies) and quantitatively (body-parent precision/recall) that recovery happens for simple structures, with characteristic failure modes named for confounders/colliders and small n. |
| **RQ2 (Robust)** | How sensitive is RQ1 to **design choices and conditions**: seeds, sample size, graph structure, noise, binning, learner budget, BK content? | We have variance bars (≥30 seeds), n-scaling curves, a structural sweep across 5 DGPs, and at least binning + learner ablations in the body of the report. |
| **RQ3 (Bridge)** | Do learner outputs **improve causal-graph recovery via Causal ABA** beyond what CI facts alone can recover? | (i) E9 fully answered: implied skeletons from δ-rules vs G\*, across the DGP zoo and n grid. (ii) E10 *begun*: one figure + one table comparing "Causal ABA with rule-hints" vs "Causal ABA on CI facts alone" on a small slice, plus a clear written roadmap for completing the benchmark post-interim. |

Each RQ maps to a set of experiments (Section 5), which in turn map to figures in the report (`REPORT_OUTLINE.md`).

---

## 3. Glossary

These terms appear throughout the spec set; canonical definitions live here.

- **DGP**: data-generating process — a triple `(G*, mechanism, noise)` plus a sample size `n` and a seed.
- **BK** (background knowledge): the foldable `.bk.aba` file produced by `generate_aba_background_knowledge`. For continuous variables it encodes **quantile bins** like `x0_bin0(A)`.
- **E+ / E−**: positive and negative example sets for a target predicate. For discrete targets we use `pick_target_variable`. For continuous targets we use a **median split** on the raw value (see `_median_pos_neg_examples`).
- **δ-rule** (delta rule): a learned rule, extracted from the `.bk.sol.aba` solution file via `_extract_learned_rules`.
- **Target rule**: a δ-rule whose head is the target predicate of the current learning problem.
- **Body-parent**: a δ-rule whose body cites at least one variable that is a true parent of the target in G\*.
- **Off-graph hit**: a δ-rule body that cites a variable that is neither a parent nor an ancestor of the target.
- **Implied skeleton**: the undirected graph induced by collecting, for each node, the set of variables cited in its target-rule bodies.
- **Bridge**: the procedure that injects δ-rule-derived directional hints into Causal ABA alongside CI facts.
- **ABAF**: assumption-based argumentation framework; the structure (assumptions + contraries) that ABA-ASP may introduce when no clean folded rule covers all examples.

---

## 4. Doctrine — three rules we will obey everywhere

These are **non-negotiable** within this project; downstream specs must respect them.

1. **Interim, not final.** Depth beats breadth. We prefer ≤5 DGPs with 30 seeds each over 20 DGPs with one seed each. Anything that cannot be analysed with proper variance bars goes to the appendix or is cut.
2. **Every claim is traceable.** A claim in the report must be backed by (a) a metric defined in `METRICS.md`, (b) a YAML config under `causal/configs/experiments/`, (c) at least one artefact on disk under `causal/outputs/aba_learning/grid/...`, and (d) a row in the corresponding `results.parquet`. If any of these is missing, the claim is removed.
3. **RQ3 instrumentation comes last.** We do not start E9 or E10 until E1–E4 metrics are stable across seeds. Bridge failures must not be confused with upstream learner failures.

**Explicit non-goals for the interim period:**

- No new ABA-ASP backends, folding modes, or solver tuning beyond a single ablation (E07).
- No real-world datasets; simulated DGPs only.
- No graphs larger than 4 nodes.
- No comprehensive Causal ABA benchmark — E10 is intentionally small.

---

## 5. Phase plan

Each phase has explicit **entry** and **exit** criteria. Phases are gated: we do not proceed until the exit criterion is met.

### Phase P1 — Infrastructure (write-only, no runs)

- **Entry**: this document approved.
- **Work**: write `METRICS.md`, `INFRA.md`, then the per-experiment specs. Implement `causal/metrics.py`, `causal/experiments/run_grid.py`, `causal/experiments/analysis.py`, and a Prolog-aware coverage helper. Add unit tests for the metric functions.
- **Exit**: smoke run of E01 produces a `results.parquet` with the full metric panel, and the analysis notebook plots one figure from it.

### Phase P2 — RQ1 / RQ2 runs

- **Entry**: P1 exit criterion met.
- **Work**: execute E01–E04 (core), then E06 and E07 (ablations needed for the body of the report). E05 and E08 are appendix-bound and optional.
- **Exit**: F2–F5 (see `REPORT_OUTLINE.md`) regenerate end-to-end from `results.parquet` with a single notebook run, with seed counts and CI bars labelled.

### Phase P3 — RQ3 preliminary

- **Entry**: P2 exit criterion met.
- **Work**: execute E09 (implied-skeleton method + baselines). Then **Phase A of E10**: investigate Causal ABA's input contract, write `aa-plans/experiments/CAUSAL_ABA_API.md` if needed, and run their own examples end-to-end on the local environment. Then **Phase B–D of E10**: design and run the one-figure, one-table interim bridge experiment.
- **Exit**: F6 (E09) and F7 (E10 prelim) both render from `results.parquet`. E10 spec contains a written "next steps" section detailing what we'd run with another month.

### Phase P4 — Report assembly

- **Entry**: P3 exit criterion met.
- **Work**: write the interim report following `REPORT_OUTLINE.md`. Pull figures from `causal/experiments/figures/` (versioned). Cross-link every claim to its experiment spec and config hash.
- **Exit**: report compiles, supervisor read-through complete, decisions logged in Section 8 below.

### Parallel track P-Lit — Literature review

- Runs **in parallel** with P2 and P3.
- **Entry**: `LIT_REVIEW_NOTES.md` written (i.e. end of P1).
- **Work**: read and take notes on the papers listed there; produce one-pager notes per paper; draft §2 of the report.
- **Exit**: §2 of the report is complete in prose form.

---

## 6. Index of supporting specs

| Spec | Path | Purpose |
|------|------|---------|
| Metrics | `aa-plans/METRICS.md` | Outcome categories, metric formulas, code shape. |
| Infrastructure | `aa-plans/INFRA.md` | Runner, configs, results schema, artefact layout. |
| Report outline | `aa-plans/REPORT_OUTLINE.md` | Section-by-section interim report structure with figure/claim mapping. |
| Lit review plan | `aa-plans/LIT_REVIEW_NOTES.md` | Reading list, synthesis plan, note-taking template. |
| **E01 — Sanity** | `aa-plans/experiments/E01_sanity.md` | Promote existing Phase 1–3 tests to formal case studies (one per RQ1 DGP). |
| **E02 — Seed robustness** | `aa-plans/experiments/E02_seed_robustness.md` | 30 seeds per cell across DGP zoo. **Highest-leverage missing experiment.** |
| **E03 — Sample scaling** | `aa-plans/experiments/E03_sample_scaling.md` | n ∈ {6, 12, 25, 50, 100, 200} × DGP zoo × 30 seeds. |
| **E04 — Structural sweep** | `aa-plans/experiments/E04_structural_sweep.md` | Full DGP zoo (5 graphs). |
| **E05 — Noise / SNR** | `aa-plans/experiments/E05_noise.md` | Continuous noise scale ∈ {0.1, 0.5, 1.0, 2.0}. *Appendix-bound.* |
| **E06 — Binning ablation** | `aa-plans/experiments/E06_binning.md` | bins × strategy × E+/E− definition. |
| **E07 — Learner ablation** | `aa-plans/experiments/E07_learner_ablation.md` | `folding_steps`, `folding_mode`, BK ordering. |
| **E08 — BK content ablation** | `aa-plans/experiments/E08_bk_content.md` | Irrelevant-column injection, dropped-parent stress test. *Appendix-bound.* |
| **E09 — Implied skeleton** | `aa-plans/experiments/E09_implied_skeleton.md` | First answer to RQ3: skeleton from rule bodies vs G\* + baselines. |
| **E10 — Bridge to Causal ABA** | `aa-plans/experiments/E10_bridge_to_causal_aba.md` | Bridge prelim: rules + CI → Causal ABA → Ĝ. |

---

## 7. The DGP zoo (fixed)

Five DGPs, instantiated identically across discrete and continuous variants when applicable.

| ID | Name | Nodes | Edges | Notes |
|----|------|-------|-------|-------|
| G3-chain | Chain | 3 | x0 → x1 → x2 | Already in `test_01_discrete_chain_6_samples` / `test_continuous_8_samples`. |
| G3-fork | Confounder | 3 | x0 → x1, x0 → x2 | Already in `test_02_confounder_...` / `test_continuous_confounder_...`. |
| G3-collider | Collider | 3 | x0 → x2, x1 → x2 | Already in `test_03_collider_...` / `test_continuous_collider_...`. |
| G4-forkchain | Fork + chain | 4 | x0 → x1, x0 → x2, x2 → x3 | New for E04+. |
| G4-hub | Hub-of-4 | 4 | x0 → x1, x0 → x2, x0 → x3 | New for E04+; stress test of confounding fan-out. |

For continuous DGPs we use `simulate_linear_continuous_data` with `noise_type="gaussian"`. For discrete we use `simulate_discrete_data`. Both use `random_seed` controlled by the runner.

---

## 8. Doctrinal defaults (locked)

Reflecting the decisions made in chat on 2026-05-24:

| Setting | Value | Why |
|---------|-------|-----|
| Seeds per cell | **30** | Tight CIs on small grids without exploding compute. |
| Sample-size grid (E03) | **{6, 12, 25, 50, 100, 200}** | Spans "too small" through "comfortable"; the 6 and 12 align with current Phase 2–3 runs. |
| DGP zoo size | **5** (3×3-node + 2×4-node) | Sufficient breadth for RQ2 / E09 without overwhelming the report. |
| Continuous noise default | 1.0 (Gaussian) | Matches `simulate_linear_continuous_data` default. |
| Bin default | **2 bins, quantile** | Best behaviour observed empirically so far. |
| `folding_steps` default | **15** | Current test default; E07 sweeps {5, 10, 15, 30}. |
| Folding mode default | **`nd`** | Greedy enters via E07 only. |
| Results store | Single `results.parquet` per experiment, plus per-cell `metrics.json`. | Cheap and queryable. |
| Configs | YAML under `causal/configs/experiments/E0X.yaml`. | Human-editable; hashable for provenance. |
| Notebook | One umbrella `aba_learn_lab.ipynb` driven by `analysis.py`. | Notebook is presentational; logic lives in `.py` modules. |
| Compute | Local, single core. | Keep it boring. |
| Interim report length | **5,000–10,000 words / 10–20 pages, 11pt LaTeX.** | User-confirmed. |
| RQ3 interim ambition | E09 **answered**; E10 = **1 figure + 1 table + roadmap.** | User-confirmed. |
| ArgCausalDisco status | **Mostly working**; Phase A of E10 may include short debugging budget. | User-confirmed. |

---

## 9. Risk register

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|------------|--------|------------|
| R1 | Many cells return "No solution found" at small n, masking trends. | High | Medium | Treat as a first-class outcome category; report fraction-solved alongside conditional metrics. |
| R2 | Python-Horn coverage diverges from Prolog-aware coverage, confusing the narrative. | High | Medium | Report **both** and explain the gap as a finding (this is real ABAF behaviour). |
| R3 | ArgCausalDisco / Causal ABA API harder to drive than expected; E10 stalls. | Medium | High | Phase A of E10 is a separate investigation step with a fixed time-box (2 days). If blown, descope E10 to: rule-derived skeleton vs PC-skeleton comparison, no Causal ABA. |
| R4 | Body-parent precision is a poor proxy (rule bodies are bin-specific). | Medium | Medium | Always also report off-graph rate, ancestor-only rate, and implied-skeleton F1 (E09). |
| R5 | Compute blows up at n=200 across 30 seeds × 5 DGPs × 3 targets. | Medium | Medium | Pilot one cell, extrapolate; cap `folding_steps` aggressively in scaling sweep; allow resumable runs. |
| R6 | BK ordering / seed coupling silently affects results. | Low | Medium | Seeded BK ordering in E07; resumable runs cache per-cell metrics. |
| R7 | We over-fit our narrative to the toy DGPs (3–4 nodes). | Medium | Low for interim | Be explicit about scope in the limitations section. |
| R8 | Implied-skeleton directionality rule is ad-hoc and biases results. | Medium | Medium | Report **two** directional rules side-by-side in E09 (see `E09_*.md`). |

---

## 10. Decisions log

A short append-only log. Format: `YYYY-MM-DD | decision | rationale | by`.

```
2026-05-24 | Seeds per cell = 30 | Tight CIs without exploding compute | Sam
2026-05-24 | DGP zoo = 5 graphs (3×3-node + 2×4-node) | Breadth without bloat | Sam
2026-05-24 | E10 interim = 1 fig + 1 table + roadmap | Realistic for interim | Sam
2026-05-24 | Word budget 5–10k, 10–20pp, 11pt LaTeX | Report style fixed | Sam
2026-05-24 | Plans live in causal/aa-plans/ | Distinct from learning notes | Sam
```

Future decisions (e.g. final seed set, final figure list, exact CI test for Causal ABA) get appended here as they are made.

---

## 11. Out-of-scope guards

For the interim period these are explicitly out of scope. They are listed so that scope creep is recognisable:

- Higher-order graphs (>4 nodes).
- Latent confounders (FCI-style scenarios).
- Non-Gaussian or heavy-tailed noise.
- Other ABA learners or solver back-ends.
- Real-world datasets.
- Comprehensive Causal ABA benchmark (post-interim).
- Hyperparameter optimisation; we ablate, we don't tune.
- Symbolic equivalence between learned δ-rules and Causal ABA arguments (post-interim).

---

## 12. Where to start (operational)

**Human read-through:** use [`meta-understanding-plan.md`](meta-understanding-plan.md) (Phases 1–7) before implementation.

Order of writing in the next agent-mode sessions:

**Session A (this one):**

1. `EXPERIMENTS_PLAN.md` ← *this document*.
2. `METRICS.md`.
3. `INFRA.md`.
4. `REPORT_OUTLINE.md`.
5. `LIT_REVIEW_NOTES.md`.

**Session B (later):**

6. `experiments/E01_sanity.md`, `experiments/E02_seed_robustness.md`.
7. `experiments/E03_sample_scaling.md`, `experiments/E04_structural_sweep.md`.
8. `experiments/E06_binning.md`, `experiments/E07_learner_ablation.md`.
9. `experiments/E09_implied_skeleton.md`.
10. `experiments/E10_bridge_to_causal_aba.md`.
11. `experiments/E05_noise.md`, `experiments/E08_bk_content.md` (appendix-bound, written last).

**Session C and beyond:** implementation (`metrics.py`, `experiments/run_grid.py`, `analysis.py`, configs, then runs).

The aim by end of Session A is that anyone reading `aa-plans/` knows what we are doing, why, what success looks like, and what comes next — without reading any code.
