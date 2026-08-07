# M13-C3 — H7a `asm_intro(relto)` vs `asm_intro(sechk)` under brave nd

## Status

**H7a run / analysed.** Bounded **implementation-behaviour** investigation of
inherited ABALearn `asm_intro` under **brave nd** on fixtures
`m13_bucket3_binary_collider_and` (H0) and `m13_bucket3_binary_bd_and_lead_a`
(H3), frozen `n30_seed42`. Documented here (Markdown) and in
`h7a_relto_vs_sechk.tex`.

- **Lead:** on all **seven** paired cells both arms `solved`, but **every
  delta differs** — `relto` vs `sechk` is a genuine control-flow fork that
  systematically changes what is learned
- **Pattern of the divergence:** under sechk, deltas latch onto the **first
  BK predictor** and close with an α-chain on that variable alone; under
  relto, later BK covariates more often enter the contrary layer
- Config `nd_brave_sechk` is **experimental**; **not** `ecai2024_sechk`; **not**
  a published ECAI method
- H0–H6 / H4b remain closed / unchanged (cross-linked only)
- **Not a Bucket 3 claim**
- H7b **run / analysed** separately (`h7b_cautious_relto_vs_sechk.md`; cautious nd)

Companion records: `experiment.md`; `h3_bk_leading_distractor.md`;
`h4_cautious_vs_brave.md`; `h4b_cautious_split_under_a.md`;
`learning_analysis.md`; `future_probes.md`.

---

## Research question

> Holding fixture, frozen sample, encoding, brave semantics, nd folding, and
> all other learner options constant: how does changing `asm_intro(relto)` to
> `asm_intro(sechk)` affect what ABALearn learns and how search proceeds under
> brave nd?

---

## Main finding — the relto ↔ sechk contrast

### 1. They diverge (learned theories)

On all **seven** pairs (`ecai2024`/`relto` vs `nd_brave_sechk`/`sechk`):

| Fact | Verification |
|------|----------------|
| Outcome | both arms **`solved`** on every cell |
| Deltas | **all differ** within pair (byte-distinct `delta.aba`) |
| Inputs | `bk.aba` / `examples.json` / `data.csv` byte-identical within each pair |

Especially for mechanism-relevant child `c`:

| Cell | Relto (abbrev.) | Sechk (abbrev.) |
|------|-----------------|-----------------|
| H0 `c` | gate `a` + contrary **`b_val_0`** | gate `a` + α-nest on **`a` only** — **no `b`** |
| H3 `c` | gate `a` + contraries **`b`/`d`** (+ nest) | gate `a` + α-nest on **`a` only** — **no `b`/`d`** |

For child `c`, sechk is **less covariate-informative** than relto on these
runs: relto still brings mechanism parents into the contrary layer; sechk
drops them. Non-`c` cells show the same form of contrast (relto admits later
BK covariates into contraries; sechk collapses to an α-chain on the first
folded predictor).

### 2. Why they diverge (procedural)

Different assumption-repair control flow in `gen.pl` after a failed
post-fold entailment check:

- **Relto** (`exists_assumption_relto`): look for an assumption relative to the
  folded body in current rules (` found:` OK/KO). After **`KO`**, search can
  **backtrack to another fold literal** (e.g. `b_val_0`, `c_val_0`,
  `d_val_0`). That backtrack is how later covariates enter these relto deltas.
- **Sechk** (`exists_assumption_sechk`): **always mint** a provisional α first,
  then `gen4`→`gen5` may replace it from a stable extension, else `gen6` keeps
  it. On these traces that path often **never reaches** the alternative
  covariate folds that relto takes after `KO`.

First substantive fork (every checked pair, after early shared folding):

```text
relto:  gen2: ... looking for assumption relative to
sechk:  gen2: generating NEW assumption: alpha_1(A)
```

This fork is genuine control-flow, not cosmetic logging. Sechk reuse surfaces
via `gen5` / stable-extension messages, not relto’s ` found:` lines.

### 3. Consistent pattern of the divergence (7/7 sechk cells)

Under brave nd + `sechk` on these two frozen tables, every solved sechk delta:

1. cites **exactly one** observed BK predictor — the **first** predictor block
   in that target’s BK order;
2. builds an **assumption–contrary chain** on that variable’s `*_val_*`
   literals;
3. does **not** bring later BK covariates into the final contrary layer.

Phrase as: **first-BK latch + α-chain under sechk vs richer contrary
covariates under relto** — not “always gate on `a`” (counterexample: sechk
target `a` uses only `b`).

**Cross-fixture coincidence:** H0 sechk `a` delta is byte-identical to H3
sechk `a`; H0 sechk `b` byte-identical to H3 sechk `b`. Same sechk template /
shared learner-visible preference — **not** shared causal role of `a` (H0
parent of `c` vs H3 isolated).

**Bounded brave-nd expectation (not a claim):** on these tables, under brave
nd, switching to `sechk` is expected to produce theories that attach to the
first BK predictor and close with α-structure on that variable alone, in
contrast to `relto` theories that more often cite later BK variables after
`KO`. H7b analyses the cautious-nd counterpart separately; this H7a statement
remains bounded to brave nd.

### 4. Whole-delta variable audit (added 2026-08-07)

Item 1 above was re-checked as a count over the **entire** `delta.aba`, so the
count includes ordinary target rules, contrary rules, and `assumption(...)` /
`contrary(...)` declarations rather than target rules alone. Distinct observed
variables were taken as the distinct `X` in every `X_val_*` literal in the
file, and BK order was read from `% Predictor block:` comments in
`input/bk.aba`.

| Arm | Cells | Distinct observed variables per delta | First BK predictor cited |
|-----|------:|--------------------------------------|--------------------------|
| `ecai2024` (relto) | 7/7 solved | 2 of 2 available (H0), 3 of 3 (H3) | 7/7 |
| `nd_brave_sechk` | 7/7 solved | **exactly 1** in all seven | 7/7 |

Per-cell (`BK order → variables in whole delta`):

```
collider_and  ecai2024        a: b,c   b: a,c   c: a,b
collider_and  nd_brave_sechk  a: b     b: a     c: a
bd_and_lead_a ecai2024        a: b,c,d b: a,c,d c: a,b,d d: a,b,c
bd_and_lead_a nd_brave_sechk  a: b     b: a     c: a     d: a
```

Consequence recorded for write-up use: a brave `sechk` delta is confined to
one variable, so on the collider child (mechanism `A ∧ B`) the accepted theory
has no literal naming parent `b` anywhere, including its contrary layer. Under
`relto` the same target rule appears and `c_alpha_1(A) :- b_val_0(A).` brings
`b` in. This is the H7a fact used in Finding 6 of
`findings_for_fabrizio.tex`, alongside the Finding 2 latch.

---

## Setup

| Field | Value |
|-------|--------|
| Relto comparator | `configs/ecai2024_config.pl` (`asm_intro(relto)`) |
| Sechk arm | `configs/nd_brave_sechk_config.pl` (`asm_intro(sechk)`) |
| Config id | `nd_brave_sechk` (experimental; **not** `ecai2024_sechk`) |
| Intervention | **only** `asm_intro` among learning-relevant options |
| Held fixed | brave; nd; `folding_steps(10)`; any; all; `check_ic`; post-fold entailment |
| Fixtures | H0 `m13_bucket3_binary_collider_and`; H3 `m13_bucket3_binary_bd_and_lead_a` |
| Sample | `n30_seed42` each |
| Timeout | 300s preserved |

### Role table (must keep distinct)

| Cell | Graph role | Notes |
|------|------------|-------|
| H0 / H3 `c` | child / only desirable det. mechanism target | evaluator-approved AND (H0: parents `a`,`b`; H3: parents `b`,`d`) |
| H0 `a` | genuine parent of `c`; exogenous as learning target | predictive `solved` ≠ root-mechanism recovery |
| H3 `b` | role-peer of H0 `a` (parent of `c` on H3) | do **not** equate with H3 `a` |
| H3 `a` | **isolated** distractor | BK-leading; **not** a parent of `c` |
| H0 `b` | parent of `c` (supporting) | mirror of H0 `a` pattern |
| H3 `d` | parent of `c` (supporting) | |

Primary objects: H0 `c`,`a`; H3 `c`,`a`,`b`. Supporting: H0 `b`, H3 `d`.

### Commands / paths

```bash
python -m causal.targetwise.cli run \
  --config causal/configs/targetwise/m13_bucket3_binary_collider_and/nd_brave_sechk/n30_seed42.yaml
python -m causal.targetwise.cli run \
  --config causal/configs/targetwise/m13_bucket3_binary_bd_and_lead_a/nd_brave_sechk/n30_seed42.yaml
```

Relto collections (locked ECAI; not rerun for H7a):
`.../<fixture>/ecai2024/n30_seed42/`

Sechk collections:
`.../<fixture>/nd_brave_sechk/n30_seed42/`

Engine (read-only): `gen.pl` `gen2`–`gen6`, `exists_assumption_relto`,
`exists_assumption_sechk`.

---

## Seven-cell paired summary

Recorder-verified: outcomes from `metrics.json`; delta identity via sha256;
BK order from metrics provenance `predictor_order`; observed `*_val_*` from
`delta.aba`.

| Cell | BK order | Outcome | Δ identical? | Sechk sole var | Relto also uses (observed) |
|------|----------|---------|--------------|----------------|----------------------------|
| H0 `a` | `b`,`c` | both solved | no | `b` | `b` + `c_val_0` |
| H0 `b` | `a`,`c` | both solved | no | `a` | `a` + `c_val_0` |
| H0 `c` | `a`,`b` | both solved | no | `a` | `a` + **`b_val_0`** |
| H3 `a` | `b`,`c`,`d` | both solved | no | `b` | `b` + `c`/`d` |
| H3 `b` | `a`,`c`,`d` | both solved | no | `a` | `a` + `c`/`d` |
| H3 `c` | `a`,`b`,`d` | both solved | no | `a` | `a` + **`b`/`d`** |
| H3 `d` | `a`,`b`,`c` | both solved | no | `a` | `a` + `b`/`c` |

Runtimes all sub-~2s on both arms (not the scientific focus).

---

## Primary contrast deep-dives

### H0 `c` (mechanism-relevant)

**Relto** (`.../ecai2024/.../target-c/output/delta.aba`):

```prolog
c(A) :- alpha_1(A), a_val_1(A).
c_alpha_1(A) :- b_val_0(A).
```

**Sechk** (`.../nd_brave_sechk/.../target-c/output/delta.aba`):

```prolog
c(A) :- alpha_1(A), a_val_1(A).
c_alpha_1(A) :- alpha_2(A), a_val_1(A).
c_alpha_2(A) :- alpha_1(A), a_val_1(A).
```

Same outer gate on `a_val_1`; relto’s contrary cites mechanism-parent
**`b_val_0`**, sechk’s contrary layer never leaves **`a`**. First fork matches
the global pattern (`looking for assumption relative to` vs
`generating NEW assumption: alpha_1`).

### H0 `a` (parent-of-`c` as learning target)

Both solve with dual `b_val_1` / `b_val_0` target gates. Relto puts
**`c_val_0`** into contraries (and an α-nest involving `b`); sechk builds a
four-α chain using **only `b_*`**. Predictive cover ≠ root-mechanism recovery.

### H3 `c` (mechanism-relevant; BK-leading isolated `a`)

**Relto** retains leading-`a` gates and brings **`b`/`d`** into the contrary
layer (H3-locked reading: distractor-retaining predictive theory — see
`h3_bk_leading_distractor.md`). **Sechk** keeps dual `a_val_*` gates but
closes with an α-nest on **`a` only** — mechanism parents `b`/`d` absent from
the final contrary layer. Same `solved` outcome; sharply different covariates.

### H3 `a` (isolated) vs H3 `b` (parent; role-peer of H0 `a`)

- H3 sechk `a`: sole var **`b`** (first BK predictor) — byte-identical to H0
  sechk `a`.
- H3 sechk `b`: sole var **`a`** — byte-identical to H0 sechk `b`.
- Relto on both cells admits later covariates (`c`/`d`).

Do **not** read the H0↔H3 sechk-`a` identity as shared causal role of `a`.

### Supporting: H0 `b`, H3 `d`

Same contrast form: sechk first-BK latch (`a` for both); relto adds further
covariates (`c` on H0 `b`; `b`/`c` on H3 `d`).

---

## Cross-fixture synthesis (by graph role)

| Role | Relto tendency here | Sechk tendency here |
|------|---------------------|---------------------|
| Child `c` | gate on first BK (`a`) **plus** mechanism parents in contraries | gate on first BK (`a`) **only**; α-chain; parents dropped |
| Parent-as-target (H0 `a`, H3 `b`) | first predictor + later covariates in contraries | first predictor α-chain only |
| Isolated (H3 `a`) | first predictor + later covariates | first predictor α-chain only (same template as H0 `a`) |

The switch changes **which observed variables appear in the theory**, not
whether brave nd can `solved` these tables.

---

## What the switch changed / did not / left open

**Changed:** assumption-repair path; every final `delta.aba`; covariate
content of contrary layers (especially loss of `b`/`d` on `c` under sechk).

**Did not change:** brave+nd+steps10+any+all+check_ic; learner-visible inputs
within pairs; `solved` outcomes on these seven cells.

**Resolved separately, not inside H7a:** H7b cautious nd (`sechk` vs `relto`)
is run / analysed in `h7b_cautious_relto_vs_sechk.md`. This H7a record remains
brave-only and does not absorb H7b's cautious finding.

---

## Boundaries / non-claims

- **Not a Bucket 3 claim.**
- `solved` ≠ causal or mechanism-aligned recovery.
- Do **not** claim sechk is better or worse as a general method.
- Pattern on these tables ≠ universal law for all future tables.
- Do **not** conflate H3 `a` (isolated) with H0 `a` (parent); role-peer of
  H0 `a` is H3 `b`.
- Do **not** call `nd_brave_sechk` an ECAI-paper config.
- H7b analysed separately; H0–H6 / H4b scientific readings preserved.

---

## Cross-links

- Investigation hub: `experiment.md`
- H3 BK-leading `c`: `h3_bk_leading_distractor.md`
- H4 brave residual gadget (relto context): `h4_cautious_vs_brave.md`
- H4b cautious α3 close: `h4b_cautious_split_under_a.md`
- Closed H0 learning: `learning_analysis.md`
- Probe catalogue: `future_probes.md` / `.tex`
- Bucket 3 planning hub: `../M1.3-bucket3-claims.md` (still **no claim**)
- Decision: `docs/research/decisions.md` (2026-08-04 H7a entry)

## Next

H7a documentation is complete. H7b is run / analysed
(`h7b_cautious_relto_vs_sechk.md`). Still **no Bucket 3 claim**.
