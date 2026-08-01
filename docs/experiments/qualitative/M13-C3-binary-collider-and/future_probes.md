# M13-C3 — Signposted future probes (H1, H2)

## Status

**Approved near-term probes** for the M13-C3 target-wise investigation
(`m13_bucket3_binary_collider_and`).

- Investigation status of H1 / H2: **`approved` / not yet implemented / not tested / not claims**
- **Not** approved Bucket 3 claims
- **Not** locked Bucket 1/2 claim content
- **Not** report-facing prose (`docs/report/findings/` is out of scope)
- Working LaTeX twin: `future_probes.tex`

**Samuel decision (2026-08-01):**

1. **H1 approved** — nested-prefix / missing-\((0,0,0)\) AAMAS ablation on this
   fixture (e.g. \(n=25\), seed 42, targets `a` and `b`) against the approved
   \(n=30\) baseline.
2. **H2 design approved** — separate schema-2 fixture with isolated
   \(D\sim\mathrm{Bernoulli}(1/2)\) (variables `a`,`b`,`c`,`d`).
3. **H2c in scope** for the first H2 write-up.

No probe in this file has been implemented or run under this record. Approval
authorises investigation; it does not create a Bucket 3 claim or a run matrix.

## Motivation (verified facts from the AAMAS arm)

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

These facts motivate two near-term probe families. They do not by themselves
approve a Bucket 3 claim.

## Ordering

1. **H1 first** — nested-prefix / missing-\((0,0,0)\) ablation on the existing
   fixture and AAMAS config (seed 42). **Investigation approved.**
2. **H2 second** — separate schema-2 fixture with isolated covariate \(D\).
   **Design approved;** fixture YAML / sample / learning remain to be produced
   by the Causal Fixture / target-wise workflow after locking remaining
   implementation parameters (exact fixture id, sample \(n\)/seed).

Do not expand either family into a broader run matrix beyond the approved probes
without a further Samuel decision.

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

1. Lock remaining fixture parameters as needed (exact fixture id; sample \(n\)
   and seed) and author a separate schema-2 YAML with variables `a`,`b`,`c`,`d`
   and isolated \(D\sim\mathrm{Bernoulli}(1/2)\).
2. Certify population / mechanism reference as for M13-C3.
3. Run AAMAS target-wise on `c` (and optionally roots) to test **H2a/H2b**,
   and include **H2c** in the first H2 write-up (construct or select a sample
   edge if it does not arise naturally).
4. No portfolio or multi-fixture matrix until that single extension is inspected.

---

## Boundary distinctions to preserve

Keep separate throughout any future probe write-up:

| Object | Role |
|--------|------|
| AAMAS strategy / greedy maximal co-occurrence search | procedural learner behaviour |
| Finite-sample support and label conflicts in candidate body cells | sample information |
| Mechanism correspondence for `c` (AND) | evaluator-only interpretation of a non-root |
| Absence of deterministic root mechanisms for `a`/`b` | evaluator reference status |
| Syntactic delta = reference string | coincidence, not automatic causal verdict |

Do not treat predictive rules for roots as mechanism recovery.

## Cross-links

- Investigation record: `experiment.md`
- Mathematical fixture dossier: `fixture_dossier.tex`
- Bucket 3 planning hub: `../M1.3-bucket3-claims.md` (still **no claim**)
- Research decision log: `docs/research/decisions.md` (2026-08-01 entry)
- Fixture pre-run bundle:
  `causal/outputs/causal_fixtures/m13_bucket3_binary_collider_and/`
- AAMAS baseline:
  `causal/outputs/aba_learning/targetwise/m13_bucket3_binary_collider_and/aamas2025/n30_seed42/`

## Decisions recorded

| Item | Decision | Date |
|------|----------|------|
| H1 nested-prefix / missing-\((0,0,0)\) AAMAS ablation | **Approved** | 2026-08-01 |
| H2 four-variable isolated-\(D\) fixture design | **Approved** | 2026-08-01 |
| H2c in first H2 write-up | **In scope** | 2026-08-01 |

## Remaining before implementation (not research blockers for approval)

- **H1:** execute the approved ablation and record outcomes (Fixture/target-wise
  agents; not this documentation pass).
- **H2:** choose exact fixture id and baseline sample \((n,\mathrm{seed})\);
  author YAML; certify; then run AAMAS including H2c coverage in the write-up.
- Still **no** Bucket 3 claim and **no** expanded run matrix without a further
  Samuel decision.
