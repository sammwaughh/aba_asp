# Literature Review — Reading and Synthesis Plan

**Status:** living document. Last updated: 2026-05-24.
**Companion docs:** `EXPERIMENTS_PLAN.md`, `REPORT_OUTLINE.md` (§2).

This document is the **plan** for the literature review, not the prose itself. It defines: what we will read, in what order, how we will take notes, what each paper must contribute to the report, and the word budgets that constrain depth per topic.

The target output is **§2 of the interim report** — *Literature review: causal discovery* — at roughly **2,200 words / ~3 pages**, with a coherent narrative arc from foundations through argumentative methods, plus a closing gap statement that motivates our bridge.

This document is also the **bibliography backbone**: by the end, every reference cited in the report comes from one of the entries here.

---

## 1. Goals of the lit review (and what to avoid)

**Goals.**

1. Give the reader, in a self-contained way, the **vocabulary** of causal discovery: DAGs, faithfulness, Markov equivalence, identifiability.
2. Survey the **main families** of methods (constraint-based, score-based, hybrid/logical) with one canonical paper each.
3. Situate **argumentative causal discovery** (Causal ABA) and its lineage — this is the central paragraph block.
4. Position **ABA learning** vs. ILP and ASP-based learners — this motivates our learner choice.
5. Close with an explicit **gap statement** that introduces the bridge we test in §5.3.

**Non-goals.**

- A comprehensive survey. We are not writing a survey paper; we are writing a positioning section.
- Algorithmic depth on every method. One sentence on what PC does is enough; we do not derive its termination.
- Coverage of latent-confounder methods beyond a name-drop of FCI — these are not in scope for the interim project.
- A separate ABA primer here. The *formal* background lives in §3 of the report; this section is *positioning*, not formal definitions.

---

## 2. Topics, word budgets, and structural arc

This mirrors `REPORT_OUTLINE.md §3 — §2` and is the contract for length:

| Sub-topic | Target words | Source papers (must read) | Source papers (skim) |
|-----------|-------------:|---------------------------|---------------------|
| 2.1 Foundations: SCMs, DAGs, identifiability, Markov equivalence | 250 | Pearl 2009 (book ch. 1–2); Peters-Janzing-Schölkopf 2017 (book ch. 6) | Spirtes-Glymour-Scheines (SGS) 2000 (book ch. 1) |
| 2.2 Constraint-based discovery: PC, FCI | 400 | Spirtes-Glymour 1991 (PC); Spirtes-Meek-Richardson 1995 (FCI) | Colombo-Maathuis 2014 (stable PC) |
| 2.3 Score-based discovery: GES, NOTEARS, etc. | 400 | Chickering 2002 (GES); Zheng et al. 2018 (NOTEARS) | Tsamardinos et al. 2006 (MMHC); Vowels-Camgoz-Bowden 2022 (survey) |
| 2.4 Hybrid and logical approaches | 250 | Hyttinen-Eberhardt-Järvisalo 2014 (ASP-based) | Magliacane et al. 2017 (ASP causal selection); Triantafillou-Tsamardinos 2015 |
| 2.5 Argumentative causal discovery | 500 | **Rapberger et al. (Causal ABA paper — `argumentative-causal-discovery.pdf`)** | Bondarenko-Dung-Kowalski-Toni 1997 (ABA); Dung 1995 (AAFs) |
| 2.6 ABA learning vs. ILP / ASP learners | 250 | **Proietti-Toni (ABA-ASP — `aba-learning-via-asp-paper.pdf`)**; Muggleton-De Raedt 1994 (ILP) | Law-Russo-Broda 2018 (ILASP); Sakama 2005 (induction in ASP) |
| 2.7 Gap statement and our bridge | 150 | (synthesis) | — |
| **Total** | **2,200 w** | | |

**Narrative arc:** "From IID samples to a DAG is hard. PC tests independencies. GES scores DAGs. ASP encodes acyclicity logically. Argumentative methods do this with arguments and admissibility. ABA learning produces *rules*. Our project asks whether those rules, fed back into Causal ABA, beat CI tests alone."

---

## 3. Reading list (seeded)

Each entry has: (i) why we are reading it, (ii) what to extract for the report, (iii) priority (★ = must-read, ◦ = skim).

### 3.1 Foundations

- **Pearl (2009).** *Causality: Models, Reasoning, and Inference* (2nd ed.). Chs. 1–2. ★
  - Extract: SCM definition; intervention vs. observation; do-calculus in one sentence.
  - Use: §2.1 first paragraph.
- **Peters, Janzing, Schölkopf (2017).** *Elements of Causal Inference*. Ch. 6 (graphical models). ★
  - Extract: Markov property; faithfulness; identifiability up to MEC.
  - Use: §2.1 closing.
- **Spirtes, Glymour, Scheines (2000).** *Causation, Prediction, and Search* (2nd ed.). Ch. 1. ◦
  - Extract: historical lineage of constraint-based methods.
  - Use: optional citation in §2.1 footnote.

### 3.2 Constraint-based discovery

- **Spirtes, Glymour (1991).** "An algorithm for fast recovery of sparse causal graphs." *Social Science Computer Review.* ★
  - Extract: PC algorithm's three phases; skeleton, v-structures, orientation propagation.
  - Use: §2.2 first half.
- **Spirtes, Meek, Richardson (1995).** "Causal inference in the presence of latent variables and selection bias." *UAI.* ★
  - Extract: FCI's PAG output; latent confounders.
  - Use: §2.2 second half; one sentence on why we stop here for the interim.
- **Colombo, Maathuis (2014).** "Order-independent constraint-based causal structure learning." *JMLR.* ◦
  - Extract: PC-stable; why ordering matters in practice — relevant to **E07 (BK ordering ablation)**.

### 3.3 Score-based discovery

- **Chickering (2002).** "Optimal structure identification with greedy search." *JMLR.* ★
  - Extract: GES idea, score-equivalence, asymptotic optimality under DAG assumptions.
  - Use: §2.3 first paragraph.
- **Zheng, Aragam, Ravikumar, Xing (2018).** "DAGs with NO TEARS: continuous optimization for structure learning." *NeurIPS.* ★
  - Extract: smooth acyclicity constraint; reformulation as continuous opt; pitfalls.
  - Use: §2.3 second paragraph + a comment on linear-Gaussian assumptions (relevant to our DGP zoo).
- **Tsamardinos, Brown, Aliferis (2006).** "The max-min hill-climbing Bayesian network structure learning algorithm." *Machine Learning.* ◦
  - Extract: hybrid PC+GES — useful as a name-drop bridge to §2.4.
- **Vowels, Camgoz, Bowden (2022).** "D'ya like DAGs? A survey on structure learning and causal discovery." *ACM Computing Surveys.* ◦
  - Extract: high-level taxonomy; recent NN-based methods.
  - Use: one sentence acknowledging the breadth we are not surveying.

### 3.4 Hybrid and logical approaches

- **Hyttinen, Eberhardt, Järvisalo (2014).** "Constraint-based causal discovery: conflict resolution with answer set programming." *UAI.* ★
  - Extract: ASP encoding of (in)dependence constraints; conflict handling. *This is the closest non-ABA logical neighbour.*
  - Use: §2.4 paragraph; one sentence comparing ABA's argumentative semantics to ASP's stable-model semantics.
- **Magliacane et al. (2017).** "Ancestral causal inference." *NeurIPS.* ◦
  - Extract: ASP-based ancestral selection; selects what is *robustly* causal.
- **Triantafillou, Tsamardinos (2015).** "Constraint-based causal discovery from multiple interventions over overlapping variable sets." *JMLR.* ◦
  - Extract: SAT/ASP-style aggregation of evidence — broader logical-methods context.

### 3.5 Argumentative causal discovery (central)

- **Causal ABA paper.** Local copy: `argumentative-causal-discovery.pdf`. ★★ (read twice)
  - Extract:
    - The argumentation framework over CI claims.
    - Input contract (CI facts and any preference/priority structure).
    - Output semantics (graph, set of admissible graphs, PAG-equivalent?).
    - Empirical comparison to PC/FCI/etc., if any.
  - Use: §2.5 — the central paragraph block; **this is where we tell the reader where our bridge lives**.
- **Dung (1995).** "On the acceptability of arguments and its fundamental role in nonmonotonic reasoning..." *AIJ.* ★
  - Extract: abstract argumentation frameworks, admissible/grounded/preferred extensions in one paragraph.
  - Use: §2.5 — primer paragraph; or in §3 (background).
- **Bondarenko, Dung, Kowalski, Toni (1997).** "An abstract, argumentation-theoretic approach to default reasoning." *AIJ.* ★
  - Extract: ABA's definition (assumptions, contraries, rules, attack via contrary).
  - Use: §2.5 — primer; rest goes to §3 (background).
- **Cyras, Toni, et al.** (recent surveys/papers on ABA applications). ◦
  - Skim for citations and to find more recent argumentative-discovery work.

### 3.6 ABA learning vs. ILP and ASP-based learning

- **ABA-ASP learning paper.** Local copy: `aba-learning-via-asp-paper.pdf`. ★★
  - Extract:
    - Input/output format.
    - Folding, assumption introduction, contrary introduction.
    - "No solution found" semantics.
    - Empirical evaluation, if any.
  - Use: §2.6; also forward-referenced in §3 (background) and §4 (methods).
- **Muggleton, De Raedt (1994).** "Inductive logic programming: theory and methods." *J. Logic Programming.* ★
  - Extract: the ILP paradigm; positive/negative examples; rule learning under BK.
  - Use: §2.6 — paragraph contrasting ABA learning with classical ILP (defeasibility vs monotonic).
- **Law, Russo, Broda (2018).** "The complexity and generality of learning answer set programs." *AIJ.* ◦
  - Extract: ILASP positioning; relation to ABA-ASP.
- **Sakama (2005).** "Induction from answer sets in nonmonotonic logic programs." *ACM Trans. Comput. Logic.* ◦
  - Extract: induction in ASP context; one-sentence comparison to ABA-ASP.
- **De Raedt (2008).** *Logical and Relational Learning.* ◦
  - Use as backup citation for ILP foundations.

### 3.7 Wildcards / "if time permits"

- **Shimizu et al. (2006).** "A linear non-Gaussian acyclic model for causal discovery." *JMLR* (LiNGAM). ◦
  - Useful in §6 (discussion) when we note that linear Gaussian DGPs are friendly cases.
- **Glymour, Zhang, Spirtes (2019).** "Review of causal discovery methods based on graphical models." *Frontiers in Genetics.* ◦
  - Useful overview for §2.3–§2.4.
- **Mooij, Magliacane, Claassen (2020).** "Joint causal inference from multiple contexts." *JMLR.* ◦
  - Cite if §6 mentions extensions.

---

## 4. Reading order

The reading order is **foundations first, then by family, then argumentative, then ABA learning** — i.e., the same order as §2 of the report itself. We read what we need to write in roughly the order we will write it.

**Week-by-week reading plan** (assumes ~6 hours/week on lit review during P2 runs):

| Week | Reads | Output |
|------|-------|--------|
| W1 | Pearl ch. 1–2; PJS ch. 6 | §2.1 prose draft; 3 paper notes |
| W2 | PC + FCI + Chickering | §2.2, §2.3 prose drafts; 3 paper notes |
| W3 | NOTEARS + MMHC; ASP papers (Hyttinen et al.) | §2.4 prose draft; 3 paper notes |
| W4 | Causal ABA (twice); Dung; ABA foundations | §2.5 prose draft (the central section); 3 paper notes |
| W5 | ABA-ASP paper (twice); ILP/ILASP/Sakama | §2.6 prose draft; 3 paper notes |
| W6 | Gap statement + revisions + bibliography | §2.7 + tidy entire §2 |

After W6, §2 is "complete in prose" — i.e., Phase P-Lit exit criterion is met (see `EXPERIMENTS_PLAN.md §5`).

---

## 5. Note-taking template

For each paper, create a one-page note at `causal/lit/<short-id>.md`. Suggested filename pattern: `pearl-2009-causality.md`, `spirtes-glymour-1991-pc.md`, etc.

Template:

```markdown
# <short-id>

- **Full citation:** ...
- **Why we read it:** (one sentence)
- **Section it serves:** §2.x
- **Priority:** ★★ / ★ / ◦
- **Date read:** YYYY-MM-DD
- **Re-read?** yes/no, and when

## Claim in 3 sentences

(What is the paper saying? Resist the urge to copy the abstract.)

## Method in 5 bullets

- ...
- ...

## What we borrow

(Specific facts, definitions, or framings we will use.)

## What we contrast with

(Where does our project differ or extend? Crucial for §2.7.)

## Quotable / citable lines

(With page numbers, for paraphrase only — we do not lift direct quotes.)

## Open questions / follow-ups

- ...
```

This template forces the synthesis step that lit reviews usually skip — "what do we *borrow* from this paper, what do we *contrast* with."

---

## 6. Synthesis principles

Three rules for the prose:

1. **One paragraph per family, one canonical method named per paragraph.** Resist the urge to list five algorithms; pick one, cite it, then add a "see also" pointer.
2. **Always close each paragraph with a sentence that points forward.** E.g. PC paragraph ends with: "Constraint-based methods do not, by themselves, resolve conflicts between contradictory CI tests — a gap that motivates §2.4 and §2.5." This is what carries the reader through the section.
3. **Every claim is cited.** No "it is well known that..." without a citation.

---

## 7. Bibliography mechanics

- Target ≥ 30 references in the interim report; ≈ 20 in §2 alone.
- BibTeX file at `causal/lit/refs.bib`. Keys lowercase-hyphenated by first-author-year, e.g. `spirtes-glymour-1991`.
- Use `\citep` and `\citet` consistently (natbib).
- All PDFs that we have local copies of go in `causal/lit/pdfs/` (gitignored if licensing requires).

---

## 8. Connection to §3 (background)

`LIT_REVIEW_NOTES.md` covers **positioning**. The **formal definitions** of ABA, ABA-ASP, and Causal ABA live in §3 of the report and have their own (shorter) reading list:

- ABA-ASP paper — for §3 we want the precise definitions of folding steps, assumption introduction, and contrary introduction.
- Causal ABA paper — for §3 we want the precise input/output contract (this also feeds **Phase A of E10**).
- Dung 1995 + Bondarenko et al. 1997 — for §3's ABA primer.

These are the same papers as above, but **re-read with a different question in mind**: "what definition do I need to give the reader so §5 makes sense?"

---

## 9. Risks specific to the lit review

| # | Risk | Mitigation |
|---|------|------------|
| L1 | Time sink: lit review balloons to 4000 words and crowds out experiments. | Hard cap at 2,500 words. Move overflow to an appendix or cut. |
| L2 | Causal ABA paper is harder to read than expected; positioning suffers. | Allocate **two** weeks (W4 + half of W5) and pair with a re-read after writing the §2.6 draft. |
| L3 | Bibliography drift: we cite papers we have not actually read. | Use the `lit/<short-id>.md` notes as a gating check — a paper can only be cited if its note exists. |
| L4 | Over-claiming novelty of the bridge. | Drafted §2.7 gap statement is reviewed against the notes for §2.5 and §2.6 before submission. |

---

## 10. Out-of-scope for the interim

- Causal discovery on **time series** (Granger / PCMCI / SVAR).
- **Interventional** discovery beyond a name-drop.
- **Federated / privacy-preserving** causal discovery.
- **Neuro-symbolic** discovery (DAG-GNN, etc.).
- Latent-confounder methods beyond mentioning FCI.

These are noted here so we recognise scope creep when it appears.

---

## 11. Output checklist (when §2 is "done")

- [ ] Word count 2,000–2,400.
- [ ] Each sub-topic has at least one citation.
- [ ] Each paragraph ends with a forward-pointing sentence.
- [ ] At least 18 distinct citations.
- [ ] Every cited paper has a note under `causal/lit/`.
- [ ] §2.7 (gap statement) names our bridge in one sentence and forward-points to §5.3.
- [ ] No section-internal repetition (the same fact cited twice in different paragraphs).
- [ ] Supervisor read-through complete (Gate A in `REPORT_OUTLINE.md §6`).

When all eight are ticked, §2 is ready for the body of the report.
