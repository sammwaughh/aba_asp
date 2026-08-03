# M13-C3 — H4 cautious vs brave (roots `a`/`b`)

## Status

**H4 run / analysed.** Repository `baseline_cautious` vs locked ECAI brave on
fixture `m13_bucket3_binary_collider_and` / `n30_seed42` is complete and
documented here (Markdown) and in `h4_cautious_vs_brave.tex`.

- **Lead finding:** switching to cautious **blocks the brave residual-assumption
  gadget** that had allowed roots `a`/`b` to `solved`; paths coincide through
  early \(\alpha_1\)–\(\alpha_3\) setup, then brave says **OK** and finishes
  while cautious says **KO** and returns **`completed_no_solution`**
- **Control:** child `c` **still solves** under cautious with a **byte-identical**
  delta string to locked ECAI `c`
- H0–H3 remain closed / unchanged
- **Not a Bucket 3 claim**
- H5 and H6 are **run / analysed** (`h5_greedy_cautious.md`,
  `h6_folding_and_n_ablation.md`); H7 is **signposted only** (`future_probes.md`)

Companion records: `experiment.md` (hub); `future_probes.md` (probe catalogue);
`learning_analysis.md` (closed H0); `h3_bk_leading_distractor.md`.

---

## Research question

> On the closed H0 AND-collider table, does repository-baseline cautious
> learning change the ECAI-brave root outcomes for `a`/`b` that relied on a
> residual per-row assumption gadget (rows 9 vs 26), and what happens to
> control `c`?

---

## Main finding (lead)

On frozen sample `n30_seed42`, locked **ECAI brave** solves roots `a`/`b` with
assumption-rich \(\alpha\)-nests. Repository **`baseline_cautious`** on the
**same** table returns **`completed_no_solution`** for both roots (no
`delta.aba`).

| Target | Locked ECAI brave | `baseline_cautious` |
|--------|-------------------|---------------------|
| `a` | `solved` (α-nest; ~11 delta lines) | `completed_no_solution` (~70s; ~5030-line stdout; no delta) |
| `b` | `solved` (mirror nest) | `completed_no_solution` (~66s; ~5117-line stdout; no delta) |
| `c` (control) | `solved` | `solved` (**byte-identical** delta; ~1.3s; audit SAT) |

**Learning-mode / entailment semantics change the root outcome** on the fixed
table by rejecting the 9-vs-26-style per-row assumption cover. This is **not**
“cautious never solves” (see control `c`).

---

## Decisive procedural fork

Both arms share the early nd / `folding_space(all)` / `asm_intro(relto)` path
for target `a` through \(\alpha_1\)–\(\alpha_3\) introduction. Table conflict:
row **9** is \(E^+\) \((1,0,0)\); row **26** is \(E^-\) \((0,0,0)\) — identical
BK literals `b_val_0`,`c_val_0`, opposite labels.

**Brave** (`.../ecai2024/.../cells/target-a/output/prolog.stdout`):

```text
folding result: c_alpha_3(A) <- [b_val_0(A)]
 found: alpha_2/1 ... OK, assumption introduction result: c_alpha_3(A) <- [alpha_2(A),b_val_0(A)]
```

then solution written. Closing nest in `delta.aba`:

```prolog
a(A) :- alpha_2(A), b_val_0(A).
c_alpha_2(A) :- alpha_3(A), c_val_0(A).
c_alpha_3(A) :- alpha_2(A), b_val_0(A).
```

**Cautious** (`.../baseline_cautious/.../cells/target-a/output/prolog.stdout`):

```text
folding result: c_alpha_3(A) <- [b_val_0(A)]
 found: alpha_2/1 ... KO, cannot introduce an assumption for [b_val_0(A)]
```

then further KOs, folding-budget exhaustion, and:

```text
* No solution found!
```

Target `b` mirrors with `a_val_*`. Paths **coincide until** the brave gadget;
semantics then diverge. Cautious emits **no** accepted root theory.

---

## Control `c`

Cautious `c` still **solves**. Delta string is **byte-identical** to locked
ECAI `c`:

```prolog
c(A) :- alpha_1(A), a_val_1(A).
c_alpha_1(A) :- b_val_0(A).
assumption(alpha_1(A)).
contrary(alpha_1(A),c_alpha_1(A)) :- assumption(alpha_1(A)).
```

Mode change is **selective**: it blocks the root residual α-reuse, not every
solve on this table. String match / `solved` is **not** claimed as causal or
evaluator-mechanism recovery (evaluator ref remains
`c(A) :- a_val_1(A), b_val_1(A).`; metrics body vars report `{a}`).

---

## Setup / paths

| Field | Value |
|-------|--------|
| Fixture / sample | `m13_bucket3_binary_collider_and` / `n30_seed42` (closed H0) |
| Sample hash | `sha256:1edae465d0f6b6b662b3c4ed4863af21c1d9b0c1cf428774731dd3f43282a8ca` |
| Brave arm | locked `ecai2024` (`configs/ecai2024_config.pl`, `learning_mode(brave)`) |
| Cautious arm | `baseline_cautious` (`configs/baseline_cautious_config.pl` — pinned defaults + `learning_mode(cautious)`; **not** ECAI, **not** AAMAS, **not** H5) |
| Primary targets | roots `a`, `b` |
| Control | `c` |
| Evaluator stance | roots = `no_observed_parent_deterministic_rule`; `c` ref = AND |

Paths:

```text
causal/configs/targetwise/m13_bucket3_binary_collider_and/baseline_cautious/n30_seed42.yaml
causal/outputs/aba_learning/targetwise/m13_bucket3_binary_collider_and/baseline_cautious/n30_seed42/
causal/outputs/aba_learning/targetwise/m13_bucket3_binary_collider_and/ecai2024/n30_seed42/
```

Key traces: `cells/target-{a,b,c}/output/prolog.stdout`; control
`cells/target-c/output/delta.aba`. Collection summary:
`.../baseline_cautious/n30_seed42/summary.md`.

---

## Semantic boundary

- Authoritative for acceptance: Prolog learner outcome under the selected
  `learning_mode` (`solved` / `completed_no_solution`; presence of solution /
  delta).
- Under cautious learning, SAT of `bk.sol_chk.asp` is an **existential
  final-artefact integrity witness**, not proof that every positive is a
  cautious consequence.
- Keep separate: population mechanism · finite-sample adequacy · learner
  output · evaluator judgement · audit SAT.

---

## Boundaries / non-claims

- **Not a Bucket 3 claim.**
- Cautious root `completed_no_solution` is **not** “correct root mechanism
  recovered” — it is absence of a cautiously acceptable covering theory over
  observed BK (roots have `no_observed_parent_deterministic_rule`).
- Brave root `solved` is **not** mechanism recovery (per-row assumption cover).
- Control `c` string match / `solved` is **not** causal recovery.
- Not a ranking of brave vs cautious as generally better.
- H0–H3 artefacts unchanged except cross-links.
- H5 and H6 analysed separately (`h5_greedy_cautious.md`,
  `h6_folding_and_n_ablation.md`).
- H6/H7 are **not** part of this H4 evidence body; H7 remains signposted only.

---

## Prompted follow-ups (signpost only; not this experiment)

**H5** is now **run / analysed** separately (`h5_greedy_cautious.md`).

**H6** (length drivers: `n`, `folding_steps` under fixed cautious) and **H7**
(brave `asm_intro(sechk)` vs `relto` on the 9/26 conflict) are **future probes
prompted by H4 traces**. They are not yet approved runs and are **not** part of
the H4 evidence body.

---

## Cross-links

- Investigation hub: `experiment.md`
- Closed H0 roots / 9-vs-26 exemplar: `learning_analysis.md`
- Probe catalogue: `future_probes.md` / `.tex`
- Bucket 3 planning hub: `../M1.3-bucket3-claims.md` (still **no claim**)

## Next

H4 documentation is complete. H4b and H5 are run / analysed separately
(`h4b_cautious_split_under_a.md`, `h5_greedy_cautious.md`). H6 is analysed
separately (`h6_folding_and_n_ablation.md`); H7 is signposted only. Still
**no Bucket 3 claim**.
