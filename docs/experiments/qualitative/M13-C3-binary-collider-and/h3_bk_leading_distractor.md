# M13-C3 — H3 BK-leading distractor (ECAI target `c`)

## Status

**H3 run / analysed.** ECAI (primary) and AAMAS (secondary) probes on fixture
`m13_bucket3_binary_bd_and_lead_a` / `n30_seed42` are complete and documented
here (Markdown) and in `h3_bk_leading_distractor.tex`.

- **Lead finding:** BK-leading isolated `a` is pulled into ECAI’s theory for
  deterministic child `c` (first fold selects `a_val_*`; delta conditioned on
  `a`; not the evaluator BD AND)
- **Secondary finding:** brave `solved` can rely on per-row assumption choice
  where BK underdetermines the target (nested `a=1` / \(\alpha_1\)–\(\alpha_3\))
- H0–H2 remain closed / unchanged
- **Not a Bucket 3 claim**
- H4 is **run / analysed** (`h4_cautious_vs_brave.md`); H4b is **run /
  analysed** (`h4b_cautious_split_under_a.md`); H5 remains deferred;
  H6/H7 signposted only (`future_probes.md`)

Companion records: `experiment.md` (hub); `future_probes.md` (probe catalogue);
`h2_irrelevant_covariate.md` (closed H2); `h1_support_ablation.md`;
`learning_analysis.md` (closed H0).

---

## Research question

> On a BD AND collider with BK-leading independent isolated root \(A\), does
> ECAI learning of target `c` select `a` in the first fold and retain `a` in the
> final ABA framework rather than returning the evaluator-only rule
> `c(A) :- b_val_1(A), d_val_1(A).`?

---

## Main finding (lead)

On frozen sample `n30_seed42`, ECAI **solves** target `c`, but the BK-leading
isolated variable **`a` is pulled into the learned theory**.

Decisive first fold (`.../ecai2024/.../cells/target-c/output/prolog.stdout`):

```text
folding result: c(A) <- [a_val_1(A)]
```

then assumption introduction of \(\alpha_1\). Both ordinary target rules remain
conditioned on `a`. Emitted delta (`delta.aba`):

```prolog
c(A) :- alpha_1(A), a_val_1(A).
c(A) :- alpha_2(A), a_val_0(A).
c_alpha_1(A) :- b_val_0(A).
c_alpha_1(A) :- alpha_3(A), b_val_1(A).
c_alpha_2(A) :- d_val_0(A).
c_alpha_2(A) :- b_val_0(A).
c_alpha_3(A) :- alpha_1(A), a_val_1(A).
assumption(alpha_1(A)).
assumption(alpha_2(A)).
assumption(alpha_3(A)).
contrary(alpha_1(A),c_alpha_1(A)) :- assumption(alpha_1(A)).
contrary(alpha_2(A),c_alpha_2(A)) :- assumption(alpha_2(A)).
contrary(alpha_3(A),c_alpha_3(A)) :- assumption(alpha_3(A)).
```

| Object | Content |
|--------|---------|
| Evaluator-only reference for `c` | `c(A) :- b_val_1(A), d_val_1(A).` (**no `a`**) |
| ECAI metrics body variables for `c` | `{a}` |
| ECAI delta | assumption-rich; both target rules involve `a` |
| Sample among \(C{=}1\) | all 15 have \((b,d)=(1,1)\); both values of `a` appear (10 with \(a{=}1\), 5 with \(a{=}0\)) |

**Distractor inclusion / first-fold distraction** away from the mechanism-aligned
\(B,D\) AND. Runner `solved` with artefact-audit SAT does **not** mean the
evaluator BD rule was recovered.

---

## Secondary finding (brave residual / underdetermining delta)

ECAI brave `solved` can be sample-adequate via **per-row assumption choice**
even when BK features do not determine the target. The ungrounded delta
underdetermines where the residual split occurs. That only becomes clear after
grounding.

On H3 ECAI `c`, this is concentrated in the nested \(a{=}1\) /
\(\alpha_1\)–\(\alpha_3\) repair: rows that look the same on `a`/`b` but differ
on `c`/`d` require different assumption atoms across answer sets. By contrast,
the \(a{=}0\) / \(\mathtt{c\_alpha\_2}\) side is more BK-readable
(`d_val_0` / `b_val_0` contraries without a further nested \(\alpha\)).

Clearer prior exemplar of the same brave-split phenomenon: H0 ECAI target `a`
on `m13_bucket3_binary_collider_and` / `n30_seed42`, rows **9** vs **26**
(identical BK literals `b_val_0`,`c_val_0`; opposite labels). See
`learning_analysis.md` and
`.../m13_bucket3_binary_collider_and/ecai2024/n30_seed42/cells/target-a/`.

Bound: **`solved` + audit SAT ≠ BK→target predictor recovered / mechanism-aligned.**

---

## Fixture / setup

| Field | Value |
|-------|--------|
| Fixture ID | `m13_bucket3_binary_bd_and_lead_a` (new schema-2; **not** H0 or H2) |
| Spec | `causal/fixtures/specs/m13_bucket3_binary_bd_and_lead_a.yaml` |
| DAG | \(B\to C\leftarrow D\); isolated \(A\sim\mathrm{Bernoulli}(1/2)\); \(C=B\land D\) |
| Roots | \(B\sim\mathrm{Bernoulli}(4/5)\), \(D\sim\mathrm{Bernoulli}(7/10)\), independent of \(A\) |
| Names | `a`,`b`,`c`,`d` / display \(A,B,C,D\) |
| BK order for target `c` | predictors **`a`, then `b`, then `d`** (leading distractor) |
| Evaluator ref for `c` | `c(A) :- b_val_1(A), d_val_1(A).` |
| Certificate | ordinary faithfulness `verified_exactly`; Markov verified |
| Sample | `n30_seed42` (hash `sha256:48bd0da0df696e29fb91e16e79bf30592b55c6dc16f34ee72e74aa36cc52db05`) |
| Primary arm | **ECAI** (`ecai2024`), focus target `c` |
| Secondary arm | **AAMAS** on the **same** frozen table |

Paths:

```text
causal/outputs/causal_fixtures/m13_bucket3_binary_bd_and_lead_a/
causal/configs/targetwise/m13_bucket3_binary_bd_and_lead_a/{ecai2024,aamas2025}/n30_seed42.yaml
causal/outputs/aba_learning/targetwise/m13_bucket3_binary_bd_and_lead_a/{ecai2024,aamas2025}/n30_seed42/
```

Reproducible form (primary):

```bash
python -m causal.targetwise.cli run \
  --config causal/configs/targetwise/m13_bucket3_binary_bd_and_lead_a/ecai2024/n30_seed42.yaml
```

---

## AAMAS contrast (in scope; shorter)

Same sample hash. AAMAS **solves** `c` with:

```prolog
c(A) :- a_val_1(A), b_val_1(A), d_val_1(A).
c(A) :- a_val_0(A), b_val_1(A), d_val_1(A).
```

So AAMAS also **retains `a_val_*`** in both Horn bodies (distractor omission
failure). Shape differs from ECAI’s assumption-rich theory: here greedy maximal
co-occurrence simply keeps leading `a` alongside the true parents.

Versus H2: H2 placed trailing isolated `d` on parents `a`,`b` under AAMAS and
retained `d_val_*`. H3 places **leading** isolated `a` on parents `b`,`d` and
retains `a` under both ECAI (first-fold) and AAMAS (greedy bodies).

---

## Secondary targets (compact)

| Arm | `a` | `b` | `c` | `d` |
|-----|-----|-----|-----|-----|
| ECAI | `solved` | `solved` | `solved` (**primary**) | `solved` |
| AAMAS | `completed_no_solution` | `completed_no_solution` | `solved` (contrast) | `completed_no_solution` |

Other targets are infrastructure retention only. They are not part of H3’s
research question.

---

## Boundaries / non-claims

- **Not a Bucket 3 claim.**
- Inclusion of `a` is **not** causal recovery of an \(A\to C\) edge (there is none).
- Runner `solved` / `sol_chk` SAT is **not** automatically correct /
  mechanism-aligned.
- Keep separate: population mechanism · finite-sample adequacy · learner output ·
  evaluator judgement.
- “ECAI always solves” on these cells is true so far but is **not** the H3
  question.
- H0–H2 artefacts and narratives are unchanged except for cross-links.
- H4 analysed separately (`h4_cautious_vs_brave.md`); H5 deferred; H6/H7
  signposted only.

---

## Cross-links

- Investigation hub: `experiment.md`
- Closed H0 / H1 / H2: `learning_analysis.md`, `h1_support_ablation.md`,
  `h2_irrelevant_covariate.md`
- Probe catalogue: `future_probes.md` / `.tex`
- Bucket 3 planning hub: `../M1.3-bucket3-claims.md` (still **no claim**)
- H0 brave-split exemplar: ECAI `target-a` under
  `m13_bucket3_binary_collider_and` / `n30_seed42`

## Next

H3 documentation is complete. H4 and H4b are run / analysed
(`h4_cautious_vs_brave.md`, `h4b_cautious_split_under_a.md`). H5 remains
deferred; H6/H7 are signposted only. Still **no Bucket 3 claim**.
