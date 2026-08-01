# M13-C3 — Signposted future probes (H1–H4)

## Status

Follow-up probes **motivated by closed baseline H0**, and **not** part of H0
itself. H0 is the completed six-cell AAMAS+ECAI investigation on fixture
`m13_bucket3_binary_collider_and` / `n30_seed42`, documented in
`learning_analysis.md` / `.tex` and summarised in `experiment.md`.

- H0: **closed** (see `learning_analysis.md`; not redefined here)
- H1 / H2: **`approved` / not yet implemented / not tested / not claims**
- H3: **`design approved` / not yet implemented / not tested / not a Bucket 3 claim**
  (fixture YAML not yet built)
- H4: **`proposed` / blocked on target-wise cautious support / not tested / not a Bucket 3 claim**
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
   `m13_bucket3_binary_collider_and` and from the intended H2 id
   `m13_bucket3_binary_collider_and_iso_d` (when H2 is authored).
4. **AAMAS contrast in scope** for the H3 write-up (secondary to primary ECAI
   inspection of target `c`; valuable as a related but distinct check from H2).

**H4** is signposted only; it is **not** approved for implementation and is
**blocked** until target-wise cautious learning is supported (see H4 section).

No probe in this file has been implemented or run under this record. Approvals
authorise investigation; they do not create a Bucket 3 claim or a run matrix.
Planned first frozen sample for H3 (to confirm at build): `n30_seed42`.



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

\subsection Motivation addendum (ECAI arm of closed H0 — for H3)

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
under ECAI, on a new fixture. H3 design is now approved (see Status); it is
still **not** a Bucket 3 claim and is **not yet built**.

## Ordering

1. **H1 first** — nested-prefix / missing-\((0,0,0)\) ablation on the existing
   fixture and AAMAS config (seed 42). **Investigation approved.**
2. **H2 second** — separate schema-2 fixture with isolated covariate \(D\) on
   the \(A\to C\leftarrow B\) AND collider. **Design approved;** intended id
   `m13_bucket3_binary_collider_and_iso_d` (author when H2 is built); sample
   \(n\)/seed still to lock at H2 authorship.
3. **H3** — separate schema-2 fixture
   `m13_bucket3_binary_bd_and_lead_a` with BK-leading independent \(A\) and
   AND collider \(B\to C\leftarrow D\). **Design approved;** primary ECAI
   target `c`; **AAMAS contrast in scope**. YAML / sample / learning not yet
   produced.
4. **H4 (proposed)** — same fixture/`n30_seed42`; ECAI **root** targets under
   **cautious** vs locked brave; **blocked** on target-wise cautious support.
   Not approved for run until infra is designed and approved.

Do not expand any family into a broader run matrix beyond these approved probes
(and a later-approved H4) without a further Samuel decision.

### Relation among probe families (keep distinct)

| Probe | Focus |
|-------|--------|
| H1 | AAMAS roots; missing negative witness / both-0 over-generalisation on the **current** three-variable fixture |
| H2 | AAMAS target `c`; irrelevant covariate enters **greedy maximal** co-occurrence bodies (minimality vs solvability); intended id `m13_bucket3_binary_collider_and_iso_d` |
| H3 | **ECAI** target `c` (primary); **BK order** puts independent distractor **first**; nd first-fold / repair path; **AAMAS contrast in scope**; id `m13_bucket3_binary_bd_and_lead_a` |
| **H4** | **Same fixture/sample**; ECAI **root** targets `a`/`b`; **brave → cautious**; **requires target-wise learning-mode support** |

H3 is not a duplicate of H2: different DAG, different distractor placement/name,
different primary config (ECAI nd vs AAMAS greedy), and distinct fixture ids.
The in-scope AAMAS arm on H3 still differs from H2 because the irrelevant
variable is BK-leading `a` and the mechanism parents are `b`,`d`.

H4 is not a duplicate of H1 or H3: it holds the table fixed and varies
**entailment / learning mode** on the target-wise path for **roots**.



---

## Probe family H1 — support sensitivity on AAMAS root targets

Status: **`approved` / not yet implemented / not tested / not a claim**.

### H1a — spurious root rule under missing negative witness

On this fixture, AAMAS, target `a` (symmetrically `b`), seed 42: if the table
is a nested prefix that **omits all \((0,0,0)\) rows** (e.g. \(n=25\)), learning
is predicted to **solve** with a delta that includes the both-0 co-occurrence
rule

```prolog
a(A) :- b_val_0(A), c_val_0(A).
```

(respectively `b(A) :- a_val_0(A), c_val_0(A).`), which is **false** as a
population implication and is blocked on the approved \(n=30\) table by \(E^-\)
rows 26 and 30.

Nested-prefix fact on the approved sample (seed 42): rows 1–25 contain no
\((0,0,0)\) atom; rows 26 and 30 are the only \((0,0,0)\) observations in
\(n=30\).

### H1b — negative witness in the unsafe cell

If the sample contains at least one opposite-label row in that both-0 predictor
cell, the both-0 rule fails brave entailment under the observed AAMAS path. On
approved \(n=30\) this manifested as **`completed_no_solution`**, not as
emission of only the safe both-1 rule.

### Explicit non-claims for H1

- Full support does **not** imply AAMAS will emit a “correct” deterministic root
  mechanism rule: roots have
  `no_observed_parent_deterministic_rule` in the evaluator reference.
- “One of each population atom” is a sufficient practical condition on this
  approved sample, but the operational point is a **label conflict inside the
  greedy candidate body cell**, not a generic demand for full joint support.
- H1 does not claim that omitting \((0,0,0)\) is the only way AAMAS can emit a
  spurious root rule, nor that every seed behaves identically.

### Planned investigation (H1)

**Approved.** Nested-prefix / missing-\((0,0,0)\) ablation on the existing
fixture `m13_bucket3_binary_collider_and` and AAMAS config, seed 42
(illustrative first cut: \(n=25\)), comparing root-target outcomes and deltas
to the approved \(n=30\) baseline. No broader matrix beyond this probe without
further approval.

---

## Probe family H2 — irrelevant isolated covariate on AAMAS target `c`

Status: **`design approved` / not yet implemented / not tested / not a claim**.
Requires a **new** schema-2 fixture before any learning run.

### H2a — irrelevant covariate enters greedy bodies

Extend the AND collider with an isolated binary root
\(D\sim\mathrm{Bernoulli}(1/2)\), independent of \(\{A,B,C\}\). Under AAMAS,
when both values of \(D\) appear among \(E^+\) for `c`, greedy catalogue bodies
are predicted to **include a `d_val_*` literal**; the learner is **not**
expected to return the \(D\)-free evaluator-form rule

```prolog
c(A) :- a_val_1(A), b_val_1(A).
```

even if an equivalent covering theory exists.

### H2b — learnability vs minimality

On that extension, AAMAS target `c` **may still solve** (e.g. two
\(D\)-conditioned rules covering \(d=0\) and \(d=1\) with \(a=b=1\), or an
assumption repair). The failure mode under test is **failure to omit an
irrelevant predictor / recover the minimal AND form**, not necessarily
`completed_no_solution`.

Do **not** record the strong claim “`c` becomes unlearnable” as the primary
hypothesis. Treat strong “unlearnable” wording as a probe that may be
**refuted**.

### H2c — sample-edge (**in scope**)

If \(E^+\) for `c` realise only one value of \(D\), AAMAS may emit a single
spuriously \(D\)-conditioned conjunction that is sample-adequate but
population-inadequate.

**Decision:** H2c is **in scope** for the first H2 write-up (not deferred).

### Planned investigation (H2)

**Design approved (2026-08-01).** Remaining implementation steps (not performed
by this documentation update):

1. Lock remaining fixture parameters as needed (sample \(n\) and seed; intended
   id **`m13_bucket3_binary_collider_and_iso_d`**) and author a separate
   schema-2 YAML with variables `a`,`b`,`c`,`d` and isolated
   \(D\sim\mathrm{Bernoulli}(1/2)\) on \(A\to C\leftarrow B\).
   Do **not** collide with H3 id `m13_bucket3_binary_bd_and_lead_a`.
2. Certify population / mechanism reference as for M13-C3.
3. Run AAMAS target-wise on `c` (and optionally roots) to test **H2a/H2b**,
   and include **H2c** in the first H2 write-up (construct or select a sample
   edge if it does not arise naturally).
4. No portfolio or multi-fixture matrix until that single extension is inspected.

---

## Probe family H3 — ECAI first-fold distraction by BK-leading independent variable

Status: **`design approved` / not yet implemented / not tested / not a Bucket 3 claim**.
Fixture YAML **not yet built**. Do not reuse or alter
`m13_bucket3_binary_collider_and`.

### Approved fixture design

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
| Planned first sample | `n30_seed42` (confirm at build) |
| Primary learning arm | **ECAI** target `c` |
| Secondary arm | **AAMAS** on the same frozen sample (**in scope**) |

Naming is part of the probe: under exact-value encoding, `a` precedes the
mechanism parents in BK.

### Scientific question

When learning target `c` under **ECAI** (`folding_mode(nd)`, one-step folds,
`folding_selection(any)`, etc.) on a frozen sample from this fixture, does
BK-leading independent `a` **distract** the first fold (and/or the final ABA
shape) away from the mechanism-aligned \(B,D\) conjunction?

Secondary (in scope): on the **same** sample under **AAMAS**, does greedy
maximal co-occurrence include `a_val_*` in bodies for target `c`, and how does
that compare to the ECAI path and to H2 (where the distractor is trailing `d`
on parents `a`,`b`)?

Motivated by the completed ECAI `c` cell on `m13_bucket3_binary_collider_and`
(see Motivation addendum above).

### Working hypothesis (signpost only; not a claim)

Under ECAI on target `c`, the first nd fold is predicted to match an `a_val_*`
literal from an early \(E^+\) row because `a` precedes `b` and `d` in BK. That
one-literal body is not a valid covering rule for \(C=B\land D\). Subsequent
assumption/contrary repair may still solve, but the learned framework is
predicted to **retain `a` in the ABA presentation** and **not** coincide with
the evaluator string `c :- b_val_1, d_val_1`, unless later steps drop `a`
(to be observed, not assumed).

Under AAMAS on the same sample, greedy bodies for \(E^+\) rows with \(C=1\)
(hence \(B=D=1\)) are predicted to cite the co-occurring value of `a` as well,
so the \(A\)-free evaluator form is not expected as the emitted delta
(learnability vs minimality / distractor inclusion — related to but distinct
from H2).

### Explicit non-claims for H3

- H3 does not assert that ECAI or AAMAS cannot solve, nor that `a` can never be
  dropped later in the transformation sequence.
- H3 does not reuse H2’s intended graph (\(A\to C\leftarrow B\) with isolated
  \(D\)); the distractor here is **\(A\)**, and parents of \(C\) are **\(B,D\)**.
- Completing H3 would still not by itself approve a Bucket 3 claim.

### Planned investigation (H3)

**Design approved (2026-08-01).** Remaining implementation steps (not performed
by this documentation update):

1. Author schema-2 YAML `m13_bucket3_binary_bd_and_lead_a` with the parameters
   above; planned sample `n30_seed42`.
2. Build population/certificate/mechanism reference; confirm evaluator
   reference for `c` omits `a`.
3. Run **ECAI** target-wise on the frozen sample with primary inspection of
   **target `c`** (BK order, first fold in `prolog.stdout`, `delta.aba` vs
   evaluator reference).
4. Run **AAMAS** on the same frozen sample as an **in-scope** secondary contrast
   (distractor inclusion under greedy maximal bodies; distinct from H2’s
   trailing-`d` design).
5. No portfolio or multi-fixture matrix beyond this approved H3 package without
   further approval.

---

## Probe family H4 — cautious vs brave on ECAI root targets

Status: **`proposed` / blocked on target-wise cautious support / not tested /
not a Bucket 3 claim**.

Uses the **existing** fixture and frozen sample
`m13_bucket3_binary_collider_and` / `n30_seed42`. Does **not** require a new
DAG. Cannot be executed with today’s target-wise validator as-is.

### Motivation (verified facts)

On ECAI **brave** (`configs/ecai2024_config.pl`:
`learning_mode(brave)`), targets `a` and `b` **solved** with assumption-rich
deltas (summary: 11 delta rules, 3 assumptions each). Artefacts:

- `.../ecai2024/n30_seed42/cells/target-a/` (`delta.aba`, `prolog.stdout`,
  `bk.sol_chk.asp`)
- mirror: `.../cells/target-b/`
- collection summary: `.../ecai2024/n30_seed42/summary.md`

Verified sample atoms (seed 42):

| Row | \((A,B,C)\) | Role for target `a` |
|-----|-------------|---------------------|
| 9 | \((1,0,0)\) | \(E^+\) |
| 26 | \((0,0,0)\) | \(E^-\) |

Rows 9 and 26 share identical BK literals `b_val_0`, `c_val_0`. No deterministic
rule over \((B,C)\) assigns both labels. The brave delta for `a` includes the
`alpha_2` / `alpha_3` nest (verified in `delta.aba`):

```prolog
a(A) :- alpha_2(A), b_val_0(A).
c_alpha_2(A) :- alpha_3(A), c_val_0(A).
c_alpha_3(A) :- alpha_2(A), b_val_0(A).
```

Trace/fixture integration reading (for the signpost): this is a **per-row
assumption choice gadget** — one stable model can Hold at 9 and Reject at 26
because ground assumption atoms differ. Runner `solved` means brave coverage of
\(E^+\)/\(E^-\), **not** recovery of a functional root mechanism
(`no_observed_parent_deterministic_rule`).

Engine fact (`asp_engine.pl`, `entails/5`): brave entailment requires existence
of a stable model under joint \(E^+\)/\(E^-\) constraints; cautious entailment
requires \(E^+\) atoms to lie in **cautious consequences** (true in every
answer set) and \(E^-\) atoms not to. Under that reading, the current brave
delta should **fail** cautious entailment: e.g. `a(9)` is not true in every
stable model of the choice gadget. Cautious re-check after contrary rote is
invoked in `gen.pl` (`gen6`).

### Infrastructure prerequisite (**required before H4 can run; not yet done**)

H4 is **not** “point YAML at a cautious `.pl` and run.” The **target-wise** path
currently **hard-requires brave**.

Verified code fact (`causal/targetwise/config.py`, `_read_learning_mode`): the
runner reads `set_lopt(learning_mode(...))` from the Prolog config and
**rejects** any mode other than `brave`, with an error that the current
target-wise runner supports brave learning only. The target-wise README states
that the supported regime selects brave learning. Existing configs only supply
`learner.prolog_config` (e.g. `configs/ecai2024_config.pl`); learning mode is
**not** a free YAML field — it is derived from the consulted `.pl` file and then
validated.

**Two-stage plan:**

1. **Infrastructure / config design (prerequisite, careful, small)**  
   Decide how cautious mode is exposed for target-wise without breaking existing
   brave collections or hashes. Likely pieces (for the record; final design needs
   Samuel/implementation approval):
   - a **new** Prolog options file (do **not** edit `configs/ecai2024_config.pl`
     in place), e.g. an ECAI-cautious twin that keeps nd / any / all / relto /
     `check_ic` but sets `learning_mode(cautious)`;
   - relax or extend `causal/targetwise/config.py` (and README/tests) so
     `learning_mode(cautious)` is an **explicitly allowed** target-wise mode when
     selected that way;
   - a **new** `configuration.id` and output directory so brave `ecai2024`
     artefacts remain untouched;
   - confirm what `check_ic` / `.sol_chk.asp` / the post-run artefact audit mean
     under cautious learning (joint existential SAT vs cautious consequences) so
     diagnostics are not misread.  
   Mode is coupled to Prolog consult, config hashing, manifests, and the
   brave-only validator. Do not imply that only a YAML one-liner is required.

2. **Scientific run (only after the above)**  
   Target-wise collection on the existing fixture/`n30_seed42` for roots `a`/`b`
   (optional `c` control) under the new cautious configuration.

### Precise hypotheses (not claims)

**H4a (current delta is brave-specific).**  
The serialized ECAI brave delta for target `a` on this sample does **not**
cautiously entail the \(E^+\)/\(E^-\) set: in particular, both-0 \(E^+\) such as
`a(9)` are not cautious consequences of that framework.

**H4b (cautious learning changes the root outcome).**  
Once target-wise cautious mode is supported, re-running target `a` (and
symmetrically `b`) on the **same** frozen sample with ECAI-like folding options
but **`learning_mode(cautious)`** yields an outcome **different** from the brave
solve: either `completed_no_solution`, or a solved delta **qualitatively
different** from the 11-clause `alpha_2`/`alpha_3` choice gadget (e.g. more rote
residual structure on the ambiguous \((\textit{other},c)=(0,0)\) cell). The brave
choice-gadget solution is **not** expected to reappear unchanged.

**H4c (fixture link — non-claim).**  
Interpret any difference against the AND-collider fact that roots have **no**
deterministic mechanism over the other observed variables, and that
\((B,C)=(0,0)\) (resp. \((A,C)=(0,0)\)) is label-ambiguous for the root target.
H4 tests **learning-mode / entailment semantics** on the target-wise path, not
DAG recovery.

### Explicit non-claims for H4

- Not claimed that cautious mode is “better” for causal recovery.
- Not claimed that cautious mode will recover a correct root mechanism rule
  (none exists).
- Not a ranking of brave vs cautious as general ABALearn policy beyond this
  controlled probe.
- Not claimed that the probe can be executed with today’s target-wise validator
  as-is.

### Planned investigation (when H4 is started)

**Not approved now.** When Samuel opens H4, proceed in two stages after
resolving the deferred decisions below:

1. **Infra:** implement cautious support for target-wise (new `.pl` +
   validator/README/tests + distinct `configuration.id`); leave brave
   `ecai2024` outputs immutable.
2. Optionally cheap **H4a** pre-check: cautious-consequence inspection of the
   existing brave framework without a full re-learn.
3. **H4b run:** target-wise cautious collection on `n30_seed42` for `a`/`b`
   (optional `c`).
4. Compare outcomes, deltas, and trace entailment KO points to the locked brave
   ECAI cells.

### Decisions deferred until H4 begins (flagged; not decided now)

These must be resolved **when H4 is started**, not in the current H1–H3 work.
They are recorded here so the infra prerequisite is not forgotten:

1. **Cautious Prolog filename** — e.g. a twin such as
   `configs/ecai2024_cautious_config.pl` (illustrative only); do **not** edit
   `configs/ecai2024_config.pl` in place.
2. **New target-wise `configuration.id`** and output path so brave `ecai2024`
   collections and hashes remain immutable.
3. **Validator change** — approve relaxing
   `causal/targetwise/config.py` (`_read_learning_mode`) so
   `learning_mode(cautious)` is explicitly allowed when selected via that `.pl`;
   update README/tests accordingly.
4. **`check_ic` / `.sol_chk.asp` / post-run artefact audit** under cautious
   learning — how to interpret joint existential SAT vs cautious consequences
   so diagnostics are not misread.
5. **H4a pre-check in scope?** — optional cautious-consequence inspection of the
   locked brave framework before a full re-learn.
6. **Optional target `c` control** on the cautious collection, or roots `a`/`b`
   only.

Until those are decided and infra lands, H4 remains **proposed / infra-blocked /
not tested / not a claim**.

---

## Boundary distinctions to preserve

Keep separate throughout any future probe write-up:

| Object | Role |
|--------|------|
| AAMAS strategy / greedy maximal co-occurrence search | procedural learner behaviour (H1/H2) |
| ECAI nd first-fold / BK serialisation order | procedural learner behaviour (H3) |
| Brave vs cautious entailment / learning mode | procedural / semantic learner behaviour (H4) |
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
- Research decision log: `docs/research/decisions.md` (2026-08-01 H1–H3 entries)
- Fixture pre-run bundle:
  `causal/outputs/causal_fixtures/m13_bucket3_binary_collider_and/`
- AAMAS baseline:
  `causal/outputs/aba_learning/targetwise/m13_bucket3_binary_collider_and/aamas2025/n30_seed42/`
- ECAI baseline (H3/H4 motivation):
  `causal/outputs/aba_learning/targetwise/m13_bucket3_binary_collider_and/ecai2024/n30_seed42/`
- Target-wise brave-only validator: `causal/targetwise/config.py`
- Entailment implementation: `asp_engine.pl` (`entails/5`)

## Decisions recorded

| Item | Decision | Date |
|------|----------|------|
| H1 nested-prefix / missing-\((0,0,0)\) AAMAS ablation | **Approved** | 2026-08-01 |
| H2 four-variable isolated-\(D\) fixture design | **Approved** | 2026-08-01 |
| H2c in first H2 write-up | **In scope** | 2026-08-01 |
| H3 graph/naming; \(B\) 80/20, \(D\) 70/30; id `m13_bucket3_binary_bd_and_lead_a`; AAMAS contrast | **Design approved** | 2026-08-01 |
| H4 cautious vs brave on ECAI roots | **Proposed only** (blocked on infra) | — |

## Remaining before implementation

- **H1:** execute the approved ablation and record outcomes.
- **H2:** author `m13_bucket3_binary_collider_and_iso_d` (or confirm that id);
  lock sample \((n,\mathrm{seed})\); certify; run AAMAS including H2c.
- **H3:** author `m13_bucket3_binary_bd_and_lead_a`; build planned `n30_seed42`;
  certify; run **ECAI** (primary) and **AAMAS** (in-scope contrast) with
  inspection of target `c`.
- **H4:** deferred until H4 is opened. Infra/config decisions are **flagged** in
  the H4 section (“Decisions deferred until H4 begins”) and are **not** to be
  resolved during current H1–H3 work. No cautious collection until then.
- Still **no** Bucket 3 claim and **no** expanded run matrix without a further
  Samuel decision.
