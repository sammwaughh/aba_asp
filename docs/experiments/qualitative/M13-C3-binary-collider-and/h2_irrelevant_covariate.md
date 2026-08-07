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
  (`h5_greedy_cautious.md`, `h6_folding_and_n_ablation.md`); H7a analysed
  (`h7a_relto_vs_sechk.md`, `h7b_cautious_relto_vs_sechk.md`)

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

## Cross-probe Greedy audit (added 2026-08-07, no new learner runs)

Distractor retention here generalises to a stronger statement about what a
completed Greedy delta *is*, checked across every recorded `aamas2025` cell (so
this section is cross-probe, spanning H0–H3, not H2-only). Audit script:
`docs/experiments/qualitative/M13-C3-binary-collider-and/greedy_pattern_law_audit.py`.

```bash
python docs/experiments/qualitative/M13-C3-binary-collider-and/greedy_pattern_law_audit.py
```

Define the **value pattern** of a row as the conjunction of every non-target
column at that row's value. Output summary:

```text
cells by outcome: {'completed_no_solution': 12, 'solved': 8, 'skipped': 2}

solved cells: 8
  delta equals the distinct positive pattern set:   8/8
  every rule body cites every predictor column:     8/8
  deltas containing an assumption or contrary line: 0/8
  positive and negative pattern sets disjoint:      8/8

completed_no_solution cells: 12
  sharing at least one pattern between labels:      12/12
```

Facts recorded:

1. **What a solved Greedy delta is.** In all 8 solved cells the rule-body set of
   `delta.aba` equals the set of distinct positive value patterns computed from
   that cell's own `input/data.csv`. Every body cites every predictor column, and
   no solved delta contains an assumption or contrary. Mechanism: rote learning
   gives one rule per positive row (body = row id), greedy folding with
   `folding_space(bk)` accumulates every matching BK head, exact-value BK offers
   exactly one value predicate per column per row, and `mgr` / subsumption delete
   whole rules only. No transformation deletes a body literal.
2. **What predicts the solved / no-solution split.** A full-pattern body is
   satisfied by exactly the rows carrying that pattern, so it covers a negative
   example iff a negative row repeats a positive row's pattern. Observed: all 8
   solved cells have disjoint positive/negative pattern sets, all 12
   `completed_no_solution` cells share ≥1 pattern. 20/20 over cells where the
   learner ran.
3. **Skipped cells.** The two `n=2` cells (`collider_and_iso_d` targets `a`, `d`)
   have `n_negative = 0`, outcome `skipped`, 0.0s runtime and empty stdout. The
   learner never ran, so they are outside the biconditional above.

Counting consequence, and the base of an untested prediction: the H0 child needs
1 rule; adding isolated `d` (this record's fixture) gives 2, one per observed `d`
value. This is the `k=1` case of a `2^k` conjecture for `k` isolated binary
predictors.

Interpretation carried into Finding 1, marked **tentative and untested**: because
disjointness of the positive/negative pattern sets is what admits a solution, and
extra columns can only refine patterns and so reduce sharing, a wide enough table
should let Greedy return a completed solution for a target the other observed
variables do not determine, with the delta amounting to the positive rows
restated. On that reading Greedy is unsuitable for causal recovery under this
encoding. No run yet exhibits this. At `k=1` the H2 root target `a` still shares
the pattern `(b=0, c=0, d=1)` across labels (3 positive rows, 2 negative rows).
Do not turn either conjecture into a probe until Samuel approves one.

This audit supports Finding 1 of `findings_for_fabrizio.tex`. The 22 audited
cells include 4 from the earlier positive-stochastic diamond fixture, used here
as evidence about learner behaviour only.

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
(`h5_greedy_cautious.md`, `h6_folding_and_n_ablation.md`); H7a analysed
(`h7a_relto_vs_sechk.md`, `h7b_cautious_relto_vs_sechk.md`).
Still **no Bucket 3 claim**.
