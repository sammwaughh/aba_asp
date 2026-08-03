# M13-C3 — H2 irrelevant covariate (AAMAS target `c`)

## Status

**H2 run / analysed.** AAMAS probe on fixture
`m13_bucket3_binary_collider_and_iso_d` is complete and documented here
(Markdown) and in `h2_irrelevant_covariate.tex`.

- **Lead finding:** when learning deterministic child `c`, AAMAS **includes
  irrelevant `d`** (`d_val_0` / `d_val_1`) in the learned bodies
- H0 and H1 remain closed / unchanged
- **Not a Bucket 3 claim**
- H3 is **run / analysed** (`h3_bk_leading_distractor.md`); H4 and H4b are
  **run / analysed** (`h4_cautious_vs_brave.md`,
  `h4b_cautious_split_under_a.md`); H5 and H6 analysed
  (`h5_greedy_cautious.md`, `h6_folding_and_n_ablation.md`); H7 signposted
  (`future_probes.md`)

Companion records: `experiment.md` (hub); `future_probes.md` (probe catalogue);
`h1_support_ablation.md` (closed H1); `learning_analysis.md` (closed H0).

---

## Research question

> On an AND collider extended with an independent isolated binary root \(D\),
> does AAMAS learning of target `c` retain irrelevant `d_val_*` literals in the
> learned bodies rather than returning the evaluator-only \(D\)-free rule
> `c(A) :- a_val_1(A), b_val_1(A).`?

---

## Main finding (lead)

On frozen sample `n30_seed42`, AAMAS **solves** target `c` with:

```prolog
c(A) :- a_val_1(A), b_val_1(A), d_val_1(A).
c(A) :- a_val_1(A), b_val_1(A), d_val_0(A).
```

**Irrelevant \(D\) is included** in the learned representation of `c`. The run
is solvable, but the delta is **not** the minimal / mechanism-aligned \(D\)-free
AND.

| Object | Content |
|--------|---------|
| Evaluator-only reference for `c` | `c(A) :- a_val_1(A), b_val_1(A).` (**no `d`**) |
| AAMAS delta for `c` on `n30_seed42` | two rules, each body length 3, variables `a`, `b`, **`d`** |
| Among \(C{=}1\) rows on `n30` | both \(d{=}0\) and \(d{=}1\) appear (9 each) |

Brief H0 contrast: on the three-variable fixture without `d`, AAMAS `c` emitted
the \(D\)-free AND; with an extra BK block for isolated `d`, greedy retains `d`.

One-line corrective on “still solvable”: the failure mode under test is
**distractor retention / failure of minimality**, not unlearnability of `c`.

Procedural one-liner: AAMAS greedy with `folding_space(bk)` exhausts matching BK
literals including trailing `d`, so catalogue bodies keep `d_val_*` (see
`.../cells/target-c/output/prolog.stdout`).

Authoritative artefacts:
`.../aamas2025/n30_seed42/cells/target-c/output/delta.aba` and arm
`summary.md`.

---

## Fixture / setup

| Field | Value |
|-------|--------|
| Fixture ID | `m13_bucket3_binary_collider_and_iso_d` (new schema-2; **not** H0’s three-variable fixture) |
| Spec | `causal/fixtures/specs/m13_bucket3_binary_collider_and_iso_d.yaml` |
| DAG | \(A\to C\leftarrow B\); isolated \(D\sim\mathrm{Bernoulli}(1/2)\); \(C=A\land B\) |
| Names | `a`,`b`,`c`,`d` / display \(A,B,C,D\) (`d` last → target-`c` BK order `a`, `b`, trailing `d`) |
| Roots \(A,B\) | \(\mathrm{Bernoulli}(4/5)\), \(\mathrm{Bernoulli}(7/10)\), independent (as H0) |
| Certificate | ordinary faithfulness `verified_exactly`; Markov verified |
| Mechanism reference for `c` | `c(A) :- a_val_1(A), b_val_1(A).` (formal / population / sample) |
| Primary arm | AAMAS (`aamas2025`), brave / greedy / mgr / `folding_space(bk)` |
| Primary sample | `n30_seed42` |
| Primary target | **`c`** |

Paths:

```text
causal/outputs/causal_fixtures/m13_bucket3_binary_collider_and_iso_d/
causal/configs/targetwise/m13_bucket3_binary_collider_and_iso_d/aamas2025/n30_seed42.yaml
causal/outputs/aba_learning/targetwise/m13_bucket3_binary_collider_and_iso_d/aamas2025/n30_seed42/
```

Reproducible form:

```bash
python -m causal.targetwise.cli run \
  --config causal/configs/targetwise/m13_bucket3_binary_collider_and_iso_d/aamas2025/n30_seed42.yaml
```

---

## Secondary outcomes (same `n30` collection)

Infrastructure also ran roots `a`, `b` and isolated `d`. Compact summary only:

| Target | Outcome | Note |
|--------|---------|------|
| `c` | `solved` | **primary** — distractor inclusion (above) |
| `a` | `completed_no_solution` | secondary |
| `b` | `completed_no_solution` | secondary |
| `d` | `completed_no_solution` | stochastic root; `no_observed_parent_deterministic_rule` |

These secondary cells are not part of H2’s research question.

---

## H2c (also run; not the centre)

Also run: maximal nested seed-42 prefix where \(C{=}1\) realises only one value
of \(D\), namely `n=2` (`samples/n2_seed42.csv`; prefix of `n30_seed42`).

Collection:
`.../aamas2025/n2_seed42/`. Target `c` delta:

```prolog
c(A) :- a_val_1(A), b_val_1(A), d_val_1(A).
```

Extreme edge (1+/1- on `c`). Spuriously \(D\)-conditioned conjunction is
sample-adequate on that tiny prefix. **Not** the scientific centre of H2
relative to the main `n30` distractor-inclusion finding.

---

## Boundaries / non-claims

- **Not a Bucket 3 claim.**
- Inclusion of `d` is **not** causal recovery of a \(D\to C\) edge (there is none).
- Runner `solved` is **not** automatically correct / mechanism-aligned.
- Keep separate: population mechanism · finite-sample adequacy · learner output ·
  evaluator judgement.
- Covering-equivalence of the two-rule theory on the `n30` sample is a footnote
  to distractor retention, not the interesting result.
- H0/H1 artefacts and narratives are unchanged except for cross-links.
- H3 analysed separately (`h3_bk_leading_distractor.md`); H4 and H4b analysed
  (`h4_cautious_vs_brave.md`, `h4b_cautious_split_under_a.md`); H5 analysed (`h5_greedy_cautious.md`).

---

## Cross-links

- Investigation hub: `experiment.md`
- Closed H0: `learning_analysis.md` / `.tex`
- Closed H1: `h1_support_ablation.md` / `.tex`
- Probe catalogue: `future_probes.md` / `.tex`
- Bucket 3 planning hub: `../M1.3-bucket3-claims.md` (still **no claim**)

## Next

H2 documentation is complete. H3, H4 and H4b are run / analysed
(`h3_bk_leading_distractor.md`, `h4_cautious_vs_brave.md`,
`h4b_cautious_split_under_a.md`). H5 and H6 analysed
(`h5_greedy_cautious.md`, `h6_folding_and_n_ablation.md`); H7 is signposted only.
Still **no Bucket 3 claim**.
