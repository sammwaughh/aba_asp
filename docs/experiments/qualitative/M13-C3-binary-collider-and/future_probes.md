# M13-C3 — Probe catalogue (H1–H7)

## Status

Follow-up probes **motivated by closed baseline H0**, and **not** part of H0
itself. H0 is the completed six-cell AAMAS+ECAI investigation on fixture
`m13_bucket3_binary_collider_and` / `n30_seed42`, documented in
`learning_analysis.md` / `.tex` and summarised in `experiment.md`.

- H0: **closed** (see `learning_analysis.md`; not redefined here)
- H1: **`run / analysed`** — nested-prefix AAMAS ablation on `n25_seed42`.
  Record: `h1_support_ablation.md` / `.tex`. **Not a Bucket 3 claim.**
- H2: **`run / analysed`** — isolated-\(D\) AAMAS target `c` retains irrelevant
  `d`. Record: `h2_irrelevant_covariate.md` / `.tex`. **Not a Bucket 3 claim.**
- H3: **`run / analysed`** — BK-leading isolated `a` distracts ECAI target `c`
  from BD AND. Record: `h3_bk_leading_distractor.md` / `.tex`. **Not a Bucket 3
  claim.**
- H4: **`run / analysed`** — repository `baseline_cautious` blocks brave root
  residual α-gadget on the H0 table. Record: `h4_cautious_vs_brave.md` /
  `.tex`. **Not a Bucket 3 claim.**
- H4b: **`run / analysed`** — on the H3 fixture, cautious changes only the
  \(\alpha_3\) close under shared leading-`a` gates (Layer B); Layer A shared
  with H3. Record: `h4b_cautious_split_under_a.md` / `.tex`. **Not H5. Not a
  Bucket 3 claim.**
- H5: **`run / analysed`** — experimental `greedy_cautious` matches AAMAS
  Greedy-brave on all 18 cells (Analysis A inert under Greedy). Record:
  `h5_greedy_cautious.md` / `.tex`. **Not a Bucket 3 claim.** **Not** an
  AAMAS-paper config.
- H6 / H7: **signposted only** (prompted by H4 traces; not approved runs; not
  this catalogue’s evidence body beyond a one-line pointer).
- **Not** approved Bucket 3 claims
- **Not** locked Bucket 1/2 claim content
- **Not** report-facing prose (`docs/report/findings/` is out of scope)
- Working LaTeX twin: `future_probes.tex`

**Samuel decision (2026-08-01) — H1 / H2:**

1. **H1 approved** — nested-prefix / missing-\((0,0,0)\) AAMAS ablation on this
   fixture (e.g. \(n=25\), seed 42, targets `a` and `b`) against the approved
   \(n=30\) baseline.
2. **H2 design approved** — separate schema-2 fixture with isolated
   \(D\sim\mathrm{Bernoulli}(1/2)\) (variables `a`,`b`,`c`,`d`).
3. **H2c in scope** for the first H2 write-up.

**Samuel decision (2026-08-01) — H3:**

1. Graph/naming sketch **approved**.
2. Root parameters **approved:** \(B\sim\mathrm{Bernoulli}(4/5)\)
   (\(P(B{=}1)=4/5\), \(P(B{=}0)=1/5\)); \(D\sim\mathrm{Bernoulli}(7/10)\)
   (\(P(D{=}1)=7/10\), \(P(D{=}0)=3/10\));
   \(A\sim\mathrm{Bernoulli}(1/2)\) as previously sketched.
3. Fixture id **locked:** `m13_bucket3_binary_bd_and_lead_a`
   (AND of parents `b`,`d`; BK-leading isolated `a`). Distinct from
   `m13_bucket3_binary_collider_and` and from the completed H2 fixture id
   `m13_bucket3_binary_collider_and_iso_d`.
4. **AAMAS contrast in scope** for the H3 write-up (secondary to primary ECAI
   inspection of target `c`; valuable as a related but distinct check from H2).

**Samuel decision (2026-08-03) — H4 / H5:**

1. Add a repository-baseline cautious target-wise configuration, named
   `baseline_cautious`, which explicitly pins the existing engine defaults and
   keeps `check_ic` for output generation.
2. Permit explicit `brave` and `cautious` modes in the target-wise runner while
   leaving the published ECAI and AAMAS configurations unchanged.
3. Prepare H4 on the closed H0 fixture and sample, with all targets generated
   automatically; roots `a`/`b` are primary and child `c` is a control.
4. Do **not** run H4 as part of the infrastructure change.
5. Defer any cautious Greedy ABA Learning design to **H5**. No
   `aamas_cautious` configuration is approved.

H1–H5 have been run and analysed (`h1_support_ablation.md`,
`h2_irrelevant_covariate.md`, `h3_bk_leading_distractor.md`,
`h4_cautious_vs_brave.md`, `h4b_cautious_split_under_a.md`,
`h5_greedy_cautious.md`). Approvals do not
create a Bucket 3 claim or a run matrix.



## Motivation (verified facts from the AAMAS arm of closed H0)

On the approved frozen sample `n30_seed42`, configuration `aamas2025`
(greedy / `folding_selection(mgr)` / `folding_space(bk)` / brave / `check_ic`):

| Target | Outcome | Delta (if any) |
|--------|---------|----------------|
| `c` | `solved` | `c(A) :- a_val_1(A), b_val_1(A).` (assumption-free) |
| `a` | `completed_no_solution` | empty |
| `b` | `completed_no_solution` | empty |

Sources:

- collection summary:
  `causal/outputs/aba_learning/targetwise/m13_bucket3_binary_collider_and/aamas2025/n30_seed42/summary.md`
- target `c` delta:
  `.../cells/target-c/output/delta.aba`
- target `a` / `b` reports and `prolog.stdout` under
  `.../cells/target-{a,b}/`

For target `c`, the learned delta string coincides with the evaluator-only
positive-state reference in
`causal/outputs/causal_fixtures/m13_bucket3_binary_collider_and/mechanism_reference.json`.
Record that as **syntactic coincidence**, not as a causal-recovery verdict.

Procedural reading of the AAMAS root-target path (verified in
`.../cells/target-a/output/prolog.stdout`; target `b` is symmetric):

1. Greedy folding builds **maximal co-occurrence bodies** from BK for each
   \(E^+\) row (not a minimal-parent search).
2. The both-1 co-occurrence body
   `a(A) :- b_val_1(A), c_val_1(A)` is accepted under brave entailment.
3. The both-0 co-occurrence body
   `a(A) :- b_val_0(A), c_val_0(A)` over-generalises; assumption/contrary repair
   is attempted.
4. Contrary rote learning cites rows **26** and **30** — the only sample atoms
   \((0,0,0)\) in `samples/n30_seed42.csv` — and contrary folding then fails,
   yielding `completed_no_solution`.

These facts from closed H0 motivate probe families H1 and H2. They do not by
themselves approve a Bucket 3 claim.

### Motivation addendum: ECAI arm of closed H0 for H3

On the same frozen sample `n30_seed42`, configuration `ecai2024`
(`folding_mode(nd)`, `folding_selection(any)`, brave / `check_ic`), target `c`
**solved** with delta (verified):

```prolog
c(A) :- alpha_1(A), a_val_1(A).
c_alpha_1(A) :- b_val_0(A).
assumption(alpha_1(A)).
contrary(alpha_1(A),c_alpha_1(A)) :- assumption(alpha_1(A)).
```

In `.../ecai2024/n30_seed42/cells/target-c/output/prolog.stdout`, the first nd
fold on an early \(E^+\) row replaces the sample id by **`a_val_1(A)`** (the
first BK predictor under declared order `a`, `b` for that cell), then assumption
repair retains `a` in the ordinary target body while the second parent enters via
a contrary. Collection summary:
`.../ecai2024/n30_seed42/summary.md`.

This motivates **H3**: put an *independent* distractor first in BK by naming,
under ECAI, on a new fixture. H3 is now **run / analysed**
(`h3_bk_leading_distractor.md`); it is still **not** a Bucket 3 claim.

## Ordering

1. **H1** — nested-prefix / missing-\((0,0,0)\) ablation on the existing
   fixture and AAMAS config (seed 42). **Run / analysed**
   (`h1_support_ablation.md`).
2. **H2** — separate schema-2 fixture with isolated covariate \(D\) on
   the \(A\to C\leftarrow B\) AND collider. **Run / analysed**
   (`h2_irrelevant_covariate.md`). Lead: AAMAS `c` retains `d_val_*`.
3. **H3** — separate schema-2 fixture
   `m13_bucket3_binary_bd_and_lead_a` with BK-leading independent \(A\) and
   AND collider \(B\to C\leftarrow D\). **Run / analysed**
   (`h3_bk_leading_distractor.md`). Lead: ECAI first-folds to `a` and retains
   `a` in the theory for `c`.
4. **H4** — same fixture/`n30_seed42`; compare locked brave ECAI with
   repository `baseline_cautious`; roots `a`/`b` primary; `c` control.
   **Run / analysed** (`h4_cautious_vs_brave.md`). Lead: cautious KO on the
   brave residual α-reuse; roots `completed_no_solution`; control `c` still
   solves with identical delta.
4b. **H4b** — H3 fixture/`n30_seed42`; `baseline_cautious` on target `c`.
   **Run / analysed** (`h4b_cautious_split_under_a.md`). Lead (Layer B): only
   `c_alpha_3` close changes (`d_val_1` vs brave residual); Layer A shared
   with H3. **Not H5.**
5. **H5** — experimental `greedy_cautious` counterparts of all completed
   AAMAS collections. **Run / analysed** (`h5_greedy_cautious.md`). Lead:
   brave→cautious under Greedy is inert on these 18 cells.
6. **H6 / H7 (signposted only)** — prompted by H4 traces; not approved runs
   (see short note under H4 Outcome).

Do not expand any family into a broader run matrix beyond these bounded probes
without a further Samuel decision.

### Relation among probe families (keep distinct)

| Probe | Focus |
|-------|--------|
| H1 | AAMAS roots; missing negative witness / both-0 over-generalisation on the **current** three-variable fixture |
| H2 | AAMAS target `c`; irrelevant covariate enters **greedy maximal** co-occurrence bodies (minimality vs solvability); fixture id `m13_bucket3_binary_collider_and_iso_d` |
| H3 | **ECAI** target `c` (primary); **BK order** puts independent distractor **first**; nd first-fold / repair path; **AAMAS contrast in scope**; id `m13_bucket3_binary_bd_and_lead_a` |
| **H4** | **Same fixture/sample**; locked ECAI brave vs repository `baseline_cautious`; roots `a`/`b` primary; `c` control; **run / analysed** |
| **H4b** | **H3 fixture/sample**; `baseline_cautious` on target `c`; Layer B = \(\alpha_3\) close only; Layer A shared with H3; **run / analysed**; **not H5** |
| **H5** | Experimental `greedy_cautious` vs AAMAS brave on 18 cells; Analysis A inert; **run / analysed**; not AAMAS-paper config |
| H6 / H7 | Signposted only (H4-prompted); length drivers under cautious; brave `asm_intro(sechk)` vs `relto` |

H3 is not a duplicate of H2: different DAG, different distractor placement/name,
different primary config (ECAI nd vs AAMAS greedy), and distinct fixture ids.
The in-scope AAMAS arm on H3 still differs from H2 because the irrelevant
variable is BK-leading `a` and the mechanism parents are `b`,`d`.

H4 is not a duplicate of H1 or H3: it holds the table fixed and changes the
learning mode while retaining the engine's baseline nd/any/all/relto options.
H5 was kept separate because a cautious Greedy learner needed a paper- and
algorithm-level specification before its experimental configuration could be
interpreted.



---

## Probe family H1 — support sensitivity on AAMAS root targets

Status: **`run / analysed` / not a claim**.
Evidence record: `h1_support_ablation.md` / `h1_support_ablation.tex`.

**Evaluative stance (locked for H1 reading).** Roots have
`no_observed_parent_deterministic_rule`. H0 AAMAS root `completed_no_solution`
is the **desired / correct** outcome. H1 AAMAS root `solved` with co-occurrence
Horn rules is an **incorrect / spurious** finite-sample solution.

### H1a — spurious root rule under missing negative witness

On this fixture, AAMAS, target `a` (symmetrically `b`), seed 42: the nested
prefix \(n=25\) **omits all \((0,0,0)\) rows**. Learning **solved** with a delta
that includes the both-0 co-occurrence rule

```prolog
a(A) :- b_val_0(A), c_val_0(A).
```

(respectively `b(A) :- a_val_0(A), c_val_0(A).`), which is **false** as a
population implication and is blocked on the closed H0 \(n=30\) table by \(E^-\)
rows 26 and 30.

Nested-prefix fact (seed 42): rows 1–25 contain no \((0,0,0)\) atom; rows 26
and 30 are the only \((0,0,0)\) observations in \(n=30\). Verified:
`n25_seed42.csv` is a row-for-row prefix of `n30_seed42.csv`.

### H1b — negative witness in the unsafe cell

If the sample contains at least one opposite-label row in that both-0 predictor
cell, the both-0 rule fails brave entailment under the observed AAMAS path. On
closed H0 \(n=30\) this manifested as **`completed_no_solution`**, not as
emission of only the safe both-1 rule. That H0 outcome is the **correct**
reading for roots under the H1 stance.

### Explicit non-claims for H1

- Full support does **not** imply AAMAS will emit a “correct” deterministic root
  mechanism rule: roots have
  `no_observed_parent_deterministic_rule` in the evaluator reference.
- “One of each population atom” is a sufficient practical condition on this
  approved sample, but the operational point is a **label conflict inside the
  greedy candidate body cell**, not a generic demand for full joint support.
- H1 does not claim that omitting \((0,0,0)\) is the only way AAMAS can emit a
  spurious root rule, nor that every seed behaves identically.
- H1 does **not** claim that root `solved` on \(n=25\) is progress or mechanism
  recovery.

### Outcome (H1)

**Run / analysed.** Nested-prefix ablation executed on
`m13_bucket3_binary_collider_and` / AAMAS / seed 42 / \(n=25\). Roots `a`/`b`
**incorrectly** solved with both-1 and both-0 co-occurrence rules. Child `c`
remained AND-solved as a control. Full narrative: `h1_support_ablation.md`.

---

## Probe family H2 — irrelevant isolated covariate on AAMAS target `c`

Status: **`run / analysed` / not a claim**.
Evidence record: `h2_irrelevant_covariate.md` / `h2_irrelevant_covariate.tex`.

**Lead finding.** On fixture `m13_bucket3_binary_collider_and_iso_d` /
`n30_seed42`, AAMAS solves target `c` with

```prolog
c(A) :- a_val_1(A), b_val_1(A), d_val_1(A).
c(A) :- a_val_1(A), b_val_1(A), d_val_0(A).
```

so **irrelevant \(D\) is included**. The evaluator-only reference remains the
\(D\)-free AND `c(A) :- a_val_1(A), b_val_1(A).`. Failure mode: distractor
retention / minimality, not unlearnability.

### H2a — irrelevant covariate enters greedy bodies

Observed as predicted: when both values of \(D\) appear among \(E^+\) for `c`
(9 each on `n30`), greedy catalogue bodies **include `d_val_*`**.

### H2b — learnability vs minimality

`c` **still solved** (two \(D\)-conditioned rules). Confirms that the
interesting failure is retention of an irrelevant predictor, not
`completed_no_solution`.

### H2c — sample-edge (also run; not the centre)

Nested `n=2` prefix where \(C{=}1\) realises only \(d{=}1\): single rule
`c :- a_val_1, b_val_1, d_val_1`. Extreme edge. Documented briefly in
`h2_irrelevant_covariate.md`. Not the scientific centre of H2.

### Outcome (H2)

**Run / analysed.** Fixture authored and certified; AAMAS `n30_seed42` primary
target `c` shows distractor inclusion; H2c `n2` also run. Full record:
`h2_irrelevant_covariate.md`.

---

## Probe family H3 — ECAI first-fold distraction by BK-leading independent variable

Status: **`run / analysed` / not a claim**.
Evidence record: `h3_bk_leading_distractor.md` / `h3_bk_leading_distractor.tex`.

**Lead finding.** On fixture `m13_bucket3_binary_bd_and_lead_a` / `n30_seed42`,
ECAI first-folds to `a_val_*` and retains `a` in both target rules for `c`.
The emitted delta does **not** coincide with the evaluator-only BD AND
`c(A) :- b_val_1(A), d_val_1(A).`. Failure mode: BK-leading distractor
inclusion / first-fold distraction, not unlearnability.

### Fixture (as run)

| Field | Value |
|-------|--------|
| Fixture id | `m13_bucket3_binary_bd_and_lead_a` |
| Internal / display | `a`,`b`,`c`,`d` / \(A,B,C,D\) |
| DAG | \(B \rightarrow C \leftarrow D\); **no edges** involving \(A\) |
| \(A\) | \(\mathrm{Bernoulli}(1/2)\); independent of \(\{B,C,D\}\) |
| \(B\) | \(\mathrm{Bernoulli}(4/5)\) — \(P(B{=}0)=1/5\), \(P(B{=}1)=4/5\) |
| \(D\) | \(\mathrm{Bernoulli}(7/10)\) — \(P(D{=}0)=3/10\), \(P(D{=}1)=7/10\) |
| \(C\) | deterministic \(C = B \land D\) |
| Evaluator reference for `c` | `c(A) :- b_val_1(A), d_val_1(A).` (`a` must not appear) |
| BK order for target `c` | predictors **`a`, then `b`, then `d`** (irrelevant first) |
| Frozen sample | `n30_seed42` |
| Primary learning arm | **ECAI** target `c` |
| Secondary arm | **AAMAS** on the same frozen sample (**in scope**) |

### Scientific question (answered)

When learning target `c` under **ECAI** on this frozen sample, does BK-leading
independent `a` **distract** the first fold and/or the final ABA shape away
from the mechanism-aligned \(B,D\) conjunction?

**Answer (bounded):** yes — first fold selects `a_val_1`; both target rules
retain `a`; metrics body vars `{a}`. Secondary: AAMAS also retains `a_val_*` in
both Horn bodies (vs H2’s trailing-`d` inclusion).

### Secondary finding (in scope; not the lead)

Brave residual / underdetermining delta on the nested \(a{=}1\) /
\(\alpha_1\)–\(\alpha_3\) side. Cross-link H0 ECAI target-`a` rows 9 vs 26.
Reinforces: **`solved` + audit SAT ≠ mechanism-aligned**.

### Explicit non-claims for H3

- Inclusion of `a` is **not** causal recovery of an \(A\to C\) edge.
- Runner `solved` is **not** automatically correct / mechanism-aligned.
- H3 does not reuse H2’s graph; distractor here is **\(A\)**, parents **\(B,D\)**.
- Completing H3 does **not** approve a Bucket 3 claim.

### Outcome (H3)

**Run / analysed.** Fixture authored and certified; ECAI `n30_seed42` primary
target `c` shows BK-leading `a` distraction; AAMAS contrast also retains `a`.
Full record: `h3_bk_leading_distractor.md`.

---

## Probe family H4 — repository-baseline cautious vs published ECAI brave

Status: **`run / analysed` / not a claim**.
Evidence record: `h4_cautious_vs_brave.md` / `h4_cautious_vs_brave.tex`.

**Lead finding.** On the closed H0 table `m13_bucket3_binary_collider_and` /
`n30_seed42`, switching from locked **ECAI brave** to repository
**`baseline_cautious`** **blocks the brave residual-assumption gadget** that
had allowed roots `a`/`b` to `solved`. Paths coincide through early
\(\alpha_1\)–\(\alpha_3\) setup; at the closing step
`c_alpha_3 :- alpha_2, …` brave says **OK** and finishes, cautious says
**KO**, then exhausts the folding budget and returns
**`completed_no_solution`** (no delta). Control `c` still solves with a
byte-identical delta to locked ECAI `c`.

### Fixture / arms (as run)

| Field | Value |
|-------|--------|
| Fixture / sample | `m13_bucket3_binary_collider_and` / `n30_seed42` |
| Sample hash | `sha256:1edae465…a8ca` |
| Brave arm | locked `ecai2024` |
| Cautious arm | `baseline_cautious` (`configs/baseline_cautious_config.pl`) |
| Primary | roots `a`, `b` |
| Control | `c` |

### Scientific question (answered)

Does repository-baseline cautious learning change the ECAI-brave root outcomes
that relied on a residual per-row assumption gadget (rows 9 vs 26), and what
happens to control `c`?

**Answer (bounded):** yes for roots — cautious KO at the brave closing α-reuse;
`completed_no_solution`. Control `c` still `solved` with identical delta.
Reinforces: mode change is selective; root no-solution ≠ mechanism recovery.

### Explicit non-claims for H4

- Not claimed that cautious mode is “better” for causal recovery.
- Not claimed that cautious root no-solution recovers a correct root mechanism
  (none exists).
- Not a ranking of brave vs cautious as general ABALearn policy.
- Control `c` string match / `solved` is not causal recovery.
- Under cautious learning, SAT of `bk.sol_chk.asp` is an existential
  final-artefact integrity witness, not a cautious-consequence proof.

### Outcome (H4)

**Run / analysed.** Collection at
`.../baseline_cautious/n30_seed42/`: `a`/`b` =
`completed_no_solution`; `c` = `solved` (identical delta to ECAI). Full
record: `h4_cautious_vs_brave.md`.

### Prompted follow-ups (signpost only; not H4 evidence)

- **H5** is now **run / analysed** separately (`h5_greedy_cautious.md`).
- **H6** (length drivers: `n`, `folding_steps` under fixed cautious) and
  **H7** (brave `asm_intro(sechk)` vs `relto` on the 9/26 conflict) are
  future probes prompted by H4 traces — not approved runs in this update.

---

## Probe family H4b — cautious \(\alpha_3\) close under H3 leading-`a` gates

Status: **`run / analysed` / not a claim**. **Not H5.**
Evidence record: `h4b_cautious_split_under_a.md` /
`h4b_cautious_split_under_a.tex`.

**Lead finding (Layer B).** On H3 fixture
`m13_bucket3_binary_bd_and_lead_a` / `n30_seed42` target `c`, repository
`baseline_cautious` keeps H3’s leading-`a` gates and the persistent
\(\alpha_1\)-nest vs \(\alpha_2\)-flat contrary split; it **only** changes the
\(\alpha_3\) close — rejecting brave residual
`c_alpha_3 :- alpha_1, a_val_1` and accepting `c_alpha_3 :- d_val_1`.
Both arms `solved`.

**Layer A (shared with H3; not a cautious effect):** `a`-gating of target
rules; nested `c_alpha_1` vs flat `c_alpha_2`; procedural reason is search
order / `relto` / cover-and-repair (see `h4b_cautious_split_under_a.md`).

### Outcome (H4b)

**Run / analysed.** Collection:
`.../m13_bucket3_binary_bd_and_lead_a/baseline_cautious/n30_seed42/`;
target `c` `solved` (~2.9s; audit SAT). Incidental: `a`/`b`/`d` timed out
(outside focus). Full record: `h4b_cautious_split_under_a.md`.

---

## Probe family H5 — experimental Greedy + cautious (`greedy_cautious`)

Status: **`run / analysed` / not a claim**.
Evidence record: `h5_greedy_cautious.md` / `h5_greedy_cautious.tex`.

**Lead finding (Analysis A).** On all **18** paired cells across the five
completed deterministic Bucket 3 AAMAS collections, experimental
`greedy_cautious` matches locked `aamas2025` on every outcome and every solved
delta (byte-identical). Traces are isomorphic aside from entailment-logging
surface differences. Flipping brave→cautious **inside the Greedy bundle does
not change accepted or rejected theories** on these tables. Mean runtime
≈ 1.84× (still sub-second).

**Secondary (Analysis B).** Large contrasts appear only vs repository
`baseline_cautious` (nd bundle) on H0/H3 `n30` — **search-strategy**, not the
brave→cautious flip. Not a single-knob `folding_mode` ablation.

Config: `configs/greedy_cautious_config.pl` (experimental; **not** published
AAMAS; do not call it `aamas_cautious`). Collections:
`causal/outputs/aba_learning/targetwise/<fixture>/greedy_cautious/<sample>/`.

### Outcome (H5)

**Run / analysed.** Full narrative: `h5_greedy_cautious.md`.

---

## Boundary distinctions to preserve

Keep separate throughout any future probe write-up:

| Object | Role |
|--------|------|
| AAMAS strategy / greedy maximal co-occurrence search | procedural learner behaviour (H1/H2) |
| ECAI nd first-fold / BK serialisation order | procedural learner behaviour (H3) |
| Brave vs cautious entailment / learning mode | procedural / semantic learner behaviour (H4) |
| Experimental Greedy+cautious (`greedy_cautious`) vs AAMAS brave | procedural / semantic probe (H5); not an AAMAS-paper config |
| Finite-sample support and label conflicts in candidate body cells | sample information |
| Mechanism correspondence for `c` (AND) | evaluator-only interpretation of a non-root |
| Absence of deterministic root mechanisms | evaluator reference status |
| Syntactic delta = reference string | coincidence, not automatic causal verdict |
| Runner `solved` under brave | brave coverage of \(E^\pm\), not mechanism recovery |

Do not treat predictive rules for roots as mechanism recovery.

## Cross-links

- Investigation record: `experiment.md`
- Mathematical fixture dossier: `fixture_dossier.tex`
- Bucket 3 planning hub: `../M1.3-bucket3-claims.md` (still **no claim**)
- Research decision log: `docs/research/decisions.md` (2026-08-01 H1–H3
  entries; 2026-08-03 H4/H5 entry)
- Fixture pre-run bundle:
  `causal/outputs/causal_fixtures/m13_bucket3_binary_collider_and/`
- AAMAS baseline:
  `causal/outputs/aba_learning/targetwise/m13_bucket3_binary_collider_and/aamas2025/n30_seed42/`
- ECAI baseline (H3/H4 motivation):
  `causal/outputs/aba_learning/targetwise/m13_bucket3_binary_collider_and/ecai2024/n30_seed42/`
- Repository cautious baseline: `configs/baseline_cautious_config.pl`
- H4 config:
  `causal/configs/targetwise/m13_bucket3_binary_collider_and/baseline_cautious/n30_seed42.yaml`
- H4 collection:
  `causal/outputs/aba_learning/targetwise/m13_bucket3_binary_collider_and/baseline_cautious/n30_seed42/`
- Target-wise explicit brave/cautious validator: `causal/targetwise/config.py`
- Entailment implementation: `asp_engine.pl` (`entails/5`)

## Decisions recorded

| Item | Decision | Date |
|------|----------|------|
| H1 nested-prefix / missing-\((0,0,0)\) AAMAS ablation | **Approved** then **run / analysed** | 2026-08-01 / 2026-08-02 |
| H2 four-variable isolated-\(D\) fixture + AAMAS `c` | **Approved** then **run / analysed** | 2026-08-01 / 2026-08-02 |
| H2c in first H2 write-up | **In scope** (run; brief note only) | 2026-08-01 / 2026-08-02 |
| H3 graph/naming; \(B\) 80/20, \(D\) 70/30; id `m13_bucket3_binary_bd_and_lead_a`; AAMAS contrast | **Design approved** then **run / analysed** | 2026-08-01 / 2026-08-02 |
| H4 repository-baseline cautious vs published ECAI brave | **Infrastructure ready** then **run / analysed** | 2026-08-03 |
| H4b cautious \(\alpha_3\) close on H3 leading-`a` target `c` | **Run / analysed** (not H5) | 2026-08-03 |
| H5 experimental `greedy_cautious` AAMAS counterparts (18 cells) | **Run / analysed** | 2026-08-03 |
| H6 / H7 (H4-prompted) | **Signposted only; not approved runs** | 2026-08-03 |

## Current status and remaining work

- **H1:** **complete** (`h1_support_ablation.md`). Not a claim.
- **H2:** **complete** (`h2_irrelevant_covariate.md`). Lead: AAMAS `c` retains
  irrelevant `d`. Not a claim.
- **H3:** **complete** (`h3_bk_leading_distractor.md`). Lead: ECAI `c`
  first-folds to / retains BK-leading `a` (not BD AND). Not a claim.
- **H4:** **complete** (`h4_cautious_vs_brave.md`). Lead: cautious blocks
  brave root residual α-gadget; roots `completed_no_solution`; control `c`
  still solves. Not a claim.
- **H4b:** **complete** (`h4b_cautious_split_under_a.md`). Lead (Layer B):
  only `c_alpha_3` close changes under shared Layer A. Not a claim; not H5.
- **H5:** **complete** (`h5_greedy_cautious.md`). Lead: Greedy brave→cautious
  inert on 18 cells; Analysis B contrasts are search-bundle. Not a claim; not
  AAMAS-paper config.
- **H6 / H7:** signposted only (prompted by H4); not approved for run here.
- Still **no** Bucket 3 claim and **no** expanded run matrix without a further
  Samuel decision.
