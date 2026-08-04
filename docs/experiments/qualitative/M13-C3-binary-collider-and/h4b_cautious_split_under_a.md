# M13-C3 — H4b cautious split under leading `a` (target `c`)

## Status

**H4b run / analysed.** Bounded follow-up to H3/H4: repository
`baseline_cautious` vs locked H3 ECAI brave on fixture
`m13_bucket3_binary_bd_and_lead_a` / `n30_seed42`, focus target `c`. Documented
here (Markdown) and in `h4b_cautious_split_under_a.tex`.

- **Lead (Layer B):** cautious **only** changes the \(\alpha_3\) close —
  rejects brave residual `c_alpha_3 :- alpha_1, a_val_1` and accepts
  `c_alpha_3 :- d_val_1`; both arms `solved`
- **Shared (Layer A — not a cautious effect):** both arms still gate on
  BK-leading `a` and keep the persistent \(\alpha_1\)-nest vs \(\alpha_2\)-flat
  contrary split
- **Not H5** at the time of H4b (H4b is nd-cautious on H3 `c`; H5 is the
  separate Greedy-cautious probe — now **run / analysed**:
  `h5_greedy_cautious.md`)
- H0–H4 remain closed / unchanged
- **Not a Bucket 3 claim**
- H6 analysed (`h6_folding_and_n_ablation.md`); H7a analysed
  (`h7a_relto_vs_sechk.md`, `h7b_cautious_relto_vs_sechk.md`)

Companion records: `experiment.md` (hub); `h3_bk_leading_distractor.md` (locked
brave); `h4_cautious_vs_brave.md` (H4 roots contrast); `future_probes.md`.

---

## Research question

> On the H3 BD AND + BK-leading-`a` table, under otherwise shared nd/`relto`
> settings, does switching from ECAI brave to repository-baseline cautious
> change how the split beneath the `a` gates is closed — in particular the
> attack on `alpha_3` — and what stays the same?

---

## Main finding (Layer B — lead)

On frozen sample `n30_seed42`, target `c`, both arms **solve**. The string
difference is **exactly one rule** — the body of `c_alpha_3`:

```prolog
% H3 ECAI brave:    c_alpha_3(A) :- alpha_1(A), a_val_1(A).
% H4b cautious:     c_alpha_3(A) :- d_val_1(A).
```

Decisive fork (`.../baseline_cautious/.../cells/target-c/output/prolog.stdout`):

```text
folding result: c_alpha_3(A) <- [a_val_1(A)]
 found: alpha_1/1 ... KO, cannot introduce an assumption for [a_val_1(A)]
 folding result: c_alpha_3(A) <- [d_val_1(A)]
```

Locked brave at the same fold (`.../ecai2024/.../target-c/output/prolog.stdout`):

```text
folding result: c_alpha_3(A) <- [a_val_1(A)]
 found: alpha_1/1 ... OK, assumption introduction result: c_alpha_3(A) <- [alpha_1(A),a_val_1(A)]
```

Brave never folds `d_*` on this close. Cautious rejects the residual gadget and
accepts explicit `d_val_1`.

**Lead:** repository `baseline_cautious` keeps H3’s leading-`a` gates and the
persistent \(\alpha_1\)-nest vs \(\alpha_2\)-flat contrary split; it **only**
changes the \(\alpha_3\) close. Both arms `solved`.

Versus H4 (one sentence): H4 blocked a brave residual gadget on **roots** →
`completed_no_solution`; H4b blocks *this* residual gadget on **child `c`** →
still `solved`, with an explicit `d_val_1` close.

---

## Shared background (Layer A — not attributed to cautious)

Both H3 ECAI brave and H4b cautious still:

1. **Gate target rules on BK-leading `a`:**
   - `c :- alpha_1, a_val_1`
   - `c :- alpha_2, a_val_0`  
   Distractor gating remains. Evaluator `c :- b_val_1, d_val_1` is **not**
   recovered. Metrics body variables for target rules still report `{a}`.

2. **Build asymmetric contrary skeletons under those gates** (identical through
   \(\alpha_3\) introduction):

| Gate | Contrary structure (both arms) |
|------|--------------------------------|
| \(\alpha_1\) (`a=1`) | **Nested:** `c_alpha_1 :- b_val_0` **plus** `c_alpha_1 :- alpha_3, b_val_1` |
| \(\alpha_2\) (`a=0`) | **Flat:** `c_alpha_2 :- d_val_0` and `c_alpha_2 :- b_val_0` |

**Persistent procedural reason (search — not cautious):**

1. `c_alpha_1` is repaired **before** `c_alpha_2` (BK-leading `a`; first \(E^+\)
   has `a=1`).
2. Under `a=1`, first contrary seed is \((b,d)=(0,1)\) → commit **`b_val_0`**;
   residuals are `(1,0)`.
3. On those residuals, fold **`b_val_1`** overgeneralises → cover-and-repair
   **mints `alpha_3`** instead of backtracking to flat `{b_val_0, d_val_0}`.
4. Under `a=0`, search later tries **`b_val_1`** → **`alpha_3` already exists**
   → **`relto` KO** → falls through to **`d_val_0` then `b_val_0`**.

Depends on contrary-set composition, `b`-before-`d` fold order, cover-and-repair,
`asm_intro(relto)`, and gate repair order — **not** on brave vs cautious.

Do **not** read Layer A as: “cautious symmetrised the splits,” “cautious removed
the nest under `a=1`,” or “cautious fixed the \(\alpha_1\neq\alpha_2\) asymmetry.”

---

## Brave vs cautious table

| Layer | Object | H3 ECAI brave | H4b cautious |
|-------|--------|---------------|--------------|
| **A** | Target gates | `α1,a_val_1` / `α2,a_val_0` | **same** |
| **A** | `c_alpha_1` | nest (`b_val_0` + `α3,b_val_1`) | **same** |
| **A** | `c_alpha_2` | flat (`d_val_0`, `b_val_0`) | **same** |
| **B** | `c_alpha_3` | `alpha_1, a_val_1` | **`d_val_1`** |
| — | Outcome | `solved` | `solved` (~2.9s; audit SAT) |

---

## Setup / paths

| Field | Value |
|-------|--------|
| Fixture / sample | `m13_bucket3_binary_bd_and_lead_a` / `n30_seed42` (same as H3) |
| Sample hash | `sha256:48bd0da0df696e29fb91e16e79bf30592b55c6dc16f34ee72e74aa36cc52db05` |
| Brave arm | locked H3 `ecai2024` |
| Cautious arm | `baseline_cautious` (`configs/baseline_cautious_config.pl`) |
| Focus | target `c` |
| Intervention | ECAI brave → repository-baseline cautious; **not** H5 |

Paths:

```text
causal/configs/targetwise/m13_bucket3_binary_bd_and_lead_a/baseline_cautious/n30_seed42.yaml
causal/outputs/aba_learning/targetwise/m13_bucket3_binary_bd_and_lead_a/baseline_cautious/n30_seed42/
causal/outputs/aba_learning/targetwise/m13_bucket3_binary_bd_and_lead_a/ecai2024/n30_seed42/cells/target-c/
```

**Incidental:** collection targets `a`/`b`/`d` **timed out** at 300s (empty
stdout). Outside H4b’s scientific focus; not expanded here.

---

## Semantic boundary

- Authoritative for acceptance: Prolog learner outcome under the selected
  `learning_mode`.
- Under cautious learning, SAT of `bk.sol_chk.asp` is an **existential
  final-artefact integrity witness**, not proof that every positive is a
  cautious consequence.
- Keep separate: population mechanism · finite-sample adequacy · learner
  output · evaluator judgement · audit SAT.

---

## Boundaries / non-claims

- **Not a Bucket 3 claim.** **Not H5.**
- Neither delta is mechanism recovery; evaluator BD AND is not recovered.
- Layer A (`a`-gating; \(\alpha_1\)-nest vs \(\alpha_2\)-flat) is **shared with
  H3** and is **not** a cautious effect.
- Forbidden misreadings: “cautious symmetrised / removed the nest / fixed the
  asymmetry.”
- Not a ranking of brave vs cautious as generally better.
- H0–H4 artefacts unchanged except cross-links.
- H5 and H6 analysed separately (`h5_greedy_cautious.md`,
  `h6_folding_and_n_ablation.md`); H7a analysed separately
  (`h7a_relto_vs_sechk.md`, `h7b_cautious_relto_vs_sechk.md`).

---

## Relation to H3 / H4

- **H3:** established BK-leading-`a` distraction and the brave residual under
  \(\alpha_3\) (`h3_bk_leading_distractor.md`).
- **H4:** on the *other* fixture (H0 roots), cautious blocked a residual gadget
  → root `completed_no_solution`.
- **H4b:** same H3 table/target `c`; Layer A unchanged; Layer B changes only
  the \(\alpha_3\) close → still `solved`.

---

## Cross-links

- Investigation hub: `experiment.md`
- Locked H3: `h3_bk_leading_distractor.md`
- H4 roots contrast: `h4_cautious_vs_brave.md`
- Probe catalogue: `future_probes.md` / `.tex`
- Bucket 3 planning hub: `../M1.3-bucket3-claims.md` (still **no claim**)

## Next

H4b documentation is complete. H5 is run / analysed
(`h5_greedy_cautious.md`). H6 is analysed (`h6_folding_and_n_ablation.md`);
H7a is analysed (`h7a_relto_vs_sechk.md`); H7b is analysed separately
(`h7b_cautious_relto_vs_sechk.md`). Still **no Bucket 3 claim**.
