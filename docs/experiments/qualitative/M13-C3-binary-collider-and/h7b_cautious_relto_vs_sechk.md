# M13-C3 — H7b cautious `asm_intro(relto)` vs `asm_intro(sechk)`

## Status

**H7b run / analysed.** Bounded **implementation-behaviour** investigation of
inherited ABALearn `asm_intro` under **cautious nd** on fixtures
`m13_bucket3_binary_collider_and` (H0 / Fixture 1) and
`m13_bucket3_binary_bd_and_lead_a` (H3 / Fixture 2), frozen `n30_seed42`.
Documented here (Markdown) and in `h7b_cautious_relto_vs_sechk.tex`.

- **Lead (Q1–Q2):** on mechanism-relevant child `c`, both arms `solved` but
  learned deltas **differ** — same `gen.pl` fork as H7a, under **cautious**
  semantics
- **Not** H7a’s brave first-BK latch: cautious sechk on `c` **retains**
  mechanism parents `b`/`d` in the contrary layer (bounded observation)
- Comparator is locked **`baseline_cautious`** (H4 / H4b), **not** `ecai2024`
- Config `nd_cautious_sechk` is **experimental**; not a published ECAI/AAMAS
  method
- H0–H6 / H4 / H4b / H7a remain closed / unchanged (cross-linked only)
- **Not a Bucket 3 claim**

Companion records: `experiment.md`; `h7a_relto_vs_sechk.md` (brave-only);
`h4_cautious_vs_brave.md`; `h4b_cautious_split_under_a.md`;
`future_probes.md`.

---

## Research question

> Holding fixture, frozen sample, encoding, **cautious** semantics, nd folding,
> and all other learner options constant: how does changing `asm_intro(relto)`
> to `asm_intro(sechk)` affect what ABALearn learns and how search proceeds
> under cautious nd?

---

## Main finding — theory + trace contrast on child `c` (Q1–Q2)

### 1. They diverge on `c`

| Cell | Relto (`baseline_cautious`) | Sechk (`nd_cautious_sechk`) | Deltas |
|------|-----------------------------|-----------------------------|--------|
| Fixture 1 `c` | `solved` | `solved` | **differ** (Q1) |
| Fixture 2 `c` | `solved` | `solved` | **differ** (Q2) |

Learner-visible `bk.aba` / `examples.json` / `data.csv` are byte-identical
within each pair.

### 2. Why they diverge (same `gen.pl` fork as H7a; cautious `gen3`)

After a fold that does **not** already entail \(E^\pm\):

- **`relto`:** `looking for assumption relative to` →
  `exists_assumption_relto` → often `found: α … KO` under cautious `gen3` →
  backtrack to another fold literal; mint only if relative path fails.
- **`sechk`:** no relative-first clause → always `generating NEW assumption`
  → `gen4` sechk → `gen5` (look in stable extension) → keep via `gen6` or
  rebuild+`gen3` (often KO under cautious).

Under **cautious** `gen3`, reuse proposals often KO, so sechk can **still
reach** `b`/`d` covariates — but later / via deeper nests than relto. This is
why H7a’s brave “first-BK latch with no later covariates” does **not**
describe these cautious-`c` sechk deltas.

First substantive fork on solved `c` cells:

```text
relto:  gen2: ... looking for assumption relative to
sechk:  gen2: generating NEW assumption: alpha_1(A)
```

### 3. What that looks like on these tables

**Q1 (Fixture 1 `c`):** same outer `a`-gate; different contrary depth; closes
with **`b_val_0`** (relto) vs **`b_val_1`** (sechk) after an extra α nest.

**Q2 (Fixture 2 `c`):** both still cite `a`,`b`,`d`; sechk is thicker (more
αs / nests) and much longer search (~257 vs ~899 lines).

---

## Setup

| Field | Value |
|-------|--------|
| Relto comparator | `configs/baseline_cautious_config.pl` (`asm_intro(relto)`) — **H4 / H4b**; do **not** use `ecai2024` |
| Sechk arm | `configs/nd_cautious_sechk_config.pl` (`asm_intro(sechk)`) |
| Config id | `nd_cautious_sechk` (experimental) |
| Intervention | **only** `asm_intro` among learning-relevant options |
| Held fixed | cautious; nd; `folding_steps(10)`; any; all; `check_ic`; `post_folding_test_entailment(true)` |
| Fixtures | H0 `m13_bucket3_binary_collider_and`; H3 `m13_bucket3_binary_bd_and_lead_a` |
| Sample | frozen `n30_seed42` each |
| Timeout | 300s |
| Comparator collections (locked; not rerun) | `.../<fixture>/baseline_cautious/n30_seed42/` |
| Sechk collections | `.../<fixture>/nd_cautious_sechk/n30_seed42/` |
| Engine (read-only) | `gen.pl` `gen2`–`gen6`, `exists_assumption_relto`, `exists_assumption_sechk` |

### Role table

| Cell | Graph role | Notes |
|------|------------|-------|
| H0 / H3 `c` | child / only desirable det. mechanism target | Q1–Q2 lead |
| H0 `a` | parent of `c`; exogenous as learning target | not Q1–Q2 lead |
| H3 `b` | role-peer of H0 `a` (parent of `c` on H3) | Q4 non-comparable |
| H3 `a` | **isolated** distractor | Q5 non-comparable; ≠ H0 `a` |
| H0 `b` | parent of `c` | Q3 failed-search cost only |

### Commands / paths

```bash
python -m causal.targetwise.cli run \
  --config causal/configs/targetwise/m13_bucket3_binary_collider_and/nd_cautious_sechk/n30_seed42.yaml
python -m causal.targetwise.cli run \
  --config causal/configs/targetwise/m13_bucket3_binary_bd_and_lead_a/nd_cautious_sechk/n30_seed42.yaml
```

---

## Outcome scaffold (secondary)

| Cell | Relto (H4/H4b) | Sechk | Theory comparable? |
|------|----------------|-------|--------------------|
| Collider `c` | solved | solved | **yes — deltas ≠** (Q1 lead) |
| Collider `a`,`b` | no-sol | no-sol | no delta; cost differs (Q3 uses `b`) |
| H3 `c` | solved | solved | **yes — deltas ≠** (Q2 lead) |
| H3 `a`,`b`,`d` | timeout 300s | timeout 300s | **no** — empty stdout both arms (Q4–Q5) |

Verified from `metrics.json` and file presence. Runtimes are not the
scientific lead.

---

## Q1 — Fixture 1 (`a→c←b`), target `c` vs H4

**Paths:**
`.../m13_bucket3_binary_collider_and/{baseline_cautious,nd_cautious_sechk}/n30_seed42/cells/target-c/output/{delta.aba,prolog.stdout}`

**Deltas (verified):**

```prolog
% baseline_cautious / relto  (~134 lines)
c(A) :- alpha_1(A), a_val_1(A).
c_alpha_1(A) :- b_val_0(A).

% nd_cautious_sechk  (~200 lines)
c(A) :- alpha_1(A), a_val_1(A).
c_alpha_1(A) :- alpha_2(A), a_val_1(A).
c_alpha_2(A) :- b_val_1(A).
```

**Trace story:**

1. Both fold `c <- [a_val_1]`; neither entails; both end with gate
   `c :- α1, a_val_1` after first repair (relto via relative-miss→mint; sechk
   via immediate mint→`gen5`→`gen6`).
2. Fold `c_α1 <- [a_val_1]`:
   - **relto:** `found: alpha_1 … KO` → next fold `c_α1 <- [b_val_0]`
     **entails** (no new α). Stop.
   - **sechk:** mint `α2` → `gen5` empty → **`gen6` OK** (installs nest
     `c_α1 :- α2, a_val_1`). This is the decisive mismatch.
3. Sechk then folds `c_α2 <- [a_val_1]` → mint→`gen5`→**KO**; then
   `c_α2 <- [b_val_1]` entails.

**Phrase precisely:** sechk is not “ignoring `b`”. It inserts an **extra
assumption layer on the leading feature** before reaching `b`, and closes with
**`b_val_1`** rather than **`b_val_0`**.

**vs H7a (brave) on same fixture `c`:** brave sechk dropped `b` entirely
(α-nest on `a` only). Cautious sechk **retains** `b` in the contrary layer.
Bounded semantics-conditioned observation — not a general law.

---

## Q2 — Fixture 2 (isolated `a`, `b→c←d`), target `c` vs H4b

**Paths:**
`.../m13_bucket3_binary_bd_and_lead_a/{baseline_cautious,nd_cautious_sechk}/n30_seed42/cells/target-c/output/{delta.aba,prolog.stdout}`

**Shared:** both solve; both keep `a`-gates and cite mechanism parents `b` and
`d` somewhere in the contrary layer.

**Differ:**

| Arm | Assumptions in delta | stdout lines | Character |
|-----|---------------------:|-------------:|-----------|
| H4b relto | 3 (`α1`–`α3`) | 257 | lean; relative-KO → `b`/`d` closes |
| sechk | 5 (`α1`,`α2`,`α31`,`α38`,`α39`) | 899 | thicker nests; many NEW/`gen5`/KO cycles |

**Phrase precisely:** same `gen.pl` fork as Q1, **amplified** by the harder H3
table. Sechk never takes the relative-first shortcut, so contrary repair pays
mint→`gen5` (often cautious KO) before trying later literals — longer search
and a thicker final theory that is still covariate-informative, unlike brave
H7a sechk on `c`.

---

## Q3 — Fixture 1, target `b` vs H4 (failed-search cost)

No `delta.aba` either side. Both raise `folding_steps` 2…10 and end
`* No solution found!`. Sechk stdout far longer (**13817** vs **5117** lines by
`wc -l`; earlier revisions of this record printed 13818/5118 from a
newline-split count) with far denser NEW/`gen5` attempts inside the same token
ladder (NEW 620 vs 90; gen5 620 vs 0). Record as **failed-search cost
divergence**, not theory divergence. Roots remain evaluator
`no_observed_parent_deterministic_rule` — not mechanism recovery.

---

## Q4–Q5 — Fixture 2 targets `b` and `a` vs H4b (non-comparable)

| Cell | Relto | Sechk | stdout |
|------|-------|-------|--------|
| H3 `b` (Q4) | timeout@300s | timeout@300s | **0 bytes** both arms |
| H3 `a` (Q5) | timeout@300s | timeout@300s | **0 bytes** both arms |

Cannot compare theories or search paths. Artefact limit only — **not**
evidence that the arms “matched.”

---

## Cost comparison over all comparable cells (added 2026-08-07)

Q1–Q3 recorded cost cell by cell. Collected here as one table so the ordering
can be cited as a whole. `lines` is `wc -l` on `output/prolog.stdout`,
`s` is `aba_learning_runtime_s` from `metrics.json`, `#α` is the count of
`assumption(...)` declarations in `delta.aba`.

| Cell | Outcome (both arms) | relto lines | relto s | relto #α | sechk lines | sechk s | sechk #α |
|------|---------------------|------------:|--------:|---------:|------------:|--------:|---------:|
| Collider `a` | `completed_no_solution` | 5030 | 69.95 | – | 13730 | 167.62 | – |
| Collider `b` | `completed_no_solution` | 5117 | 66.47 | – | 13817 | 172.88 | – |
| Collider `c` | `solved` | 134 | 1.29 | 1 | 200 | 2.24 | 2 |
| H3 `c` | `solved` | 257 | 2.94 | 3 | 899 | 10.14 | 5 |
| H3 `a`,`b`,`d` | `timeout` @300s | 0 | 300.0 | – | 0 | 300.0 | – |

Sechk costs more on **every** cell where both arms terminate: 1.5×–3.5× trace
lines and 1.7×–3.5× runtime. The three H3 roots hit the 300s cap on both arms
and separate nothing.

On the two solved cells the arms cite the **same** variable set — `a,b` on
collider `c` and `a,b,d` on H3 `c` — so what sechk adds is assumption
structure (2 vs 1, 5 vs 3), not covariate coverage. Contrast brave H7a, where
sechk changed the variable set to a single variable.

**Caveat on the runtime column.** This record previously stated that runtimes
are not the scientific lead, and that still holds for runtime taken alone,
since these are wall-clock seconds from single runs on one machine. The cost
ordering is reported because trace length and runtime agree in direction and
in rough magnitude on all four comparable cells. Trace length is the
machine-independent quantity.

**Presentation decision.** Finding 6 of `findings_for_fabrizio.tex` uses this
table to state that `relto` is the setting to prefer under cautious nd, on the
grounds that sechk returns the same outcome over the same variables for a
longer search. That is a preference between configuration options, not a claim
about causal recovery.

---

## Why sechk is longer — control-flow event counts (added 2026-08-07)

Q1–Q3 described the cost gap. This section records the counts that account for
it, so the finding can explain the gap rather than only report it.

### Mechanism in `gen.pl`

- `gen2` clause 2 (lines 54–59) is guarded by `lopt(asm_intro(relto))`. It
  prints `gen2: ... looking for assumption relative to` and calls
  `exists_assumption_relto/3`. **A sechk run never enters this clause.**
- If a candidate is found, `gen3` (lines 73–82) tests `entails/5`. Success
  prints `OK, assumption introduction result`. Failure prints
  `KO, cannot introduce an assumption for` and **fails**, which backtracks into
  the `folding/3` choice point in `gen1` clause 1 (line 37), so another fold is
  tried and **no assumption is created**.
- `gen2` clause 3 (lines 61–71) is the shared fallback: `new_assumption/9`
  creates `alpha_N` plus its defining rule and contrary declaration, then
  `compute_conseq/2` enumerates stable extensions and `member(RgAS, Cs)` opens
  a choice point over them.
- `gen4` forks: relto cuts straight to `gen6` (lines 84–89); sechk goes to
  `gen5` (lines 91–94), an **extra attempt layer per candidate extension**
  (`exists_assumption_sechk`, then `gen3` again).
- `gen6` (lines 111–139) rote-learns the contrary and, **only under
  `learning_mode(cautious)`** (line 118), runs an extra `entails/5` check.

So relto has a stage at which a repair can be abandoned before any assumption
is created, and sechk does not.

### Counts (`grep -cF` on `output/prolog.stdout`)

| Trace event | H0 `c` relto | H0 `c` sechk | H3 `c` relto | H3 `c` sechk | H0 `b` relto | H0 `b` sechk |
|-------------|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| `gen1: folding selection` | 3 | 4 | 8 | 24 | 150 | 370 |
| `folding result:` (folds tried) | 3 | 4 | 14 | 58 | 300 | 740 |
| `gen2: extended ABA entails` (fold accepted) | 1 | 1 | 4 | 10 | 50 | 120 |
| `looking for assumption relative to` | 2 | **0** | 10 | **0** | 250 | **0** |
| `OK, assumption introduction result` | 0 | 0 | 0 | 0 | 0 | 10 |
| `KO, cannot introduce an assumption` | 1 | 1 | 7 | 35 | 160 | 380 |
| `generating NEW assumption` | 1 | 3 | 3 | **48** | 90 | **620** |
| `gen4: relto using current` | 1 | 0 | 3 | 0 | 90 | 0 |
| `gen4: sechk using current` | 0 | 3 | 0 | 48 | 0 | 620 |
| `gen5: ... assumption in the stable extension` | 0 | 3 | 0 | 48 | 0 | 620 |
| `gen6: rote learning` | 1 | 2 | 3 | 13 | 90 | 230 |
| `checking entailment ... OK` (cautious, gen6) | 1 | 2 | 3 | 13 | 90 | 230 |
| `checking entailment ... KO` (cautious, gen6) | 0 | 0 | 0 | 0 | 0 | 0 |
| `has no extensions` | 0 | 0 | 0 | 0 | 0 | 0 |

### Reading

1. **The reuse stage accounts for the gap in assumption creation.** Relto's
   entries into the stage split exactly into KO rejections plus mints:
   H0 `b` 250 = 160 + 90, H3 `c` 10 = 7 + 3. The 160 rejected repairs on H0 `b`
   ended after one cautious `entails/5` call with nothing added. Sechk enters
   the stage 0 times and mints 620 on the same cell (48 vs 3 on H3 `c`).
2. **Relto's benefit here is the cheap abort, not successful reuse.**
   `OK, assumption introduction result` is **0** on every relto cell, so
   `exists_assumption_relto` never produced an accepted repair under cautious
   learning. Do not write this up as "relto reuses assumptions and so does less
   work." Write it as "relto can abandon a repair before creating an
   assumption."
3. **Each mint compounds.** Every mint reaching `gen6` adds rote-learned
   contrary rules to the pool `folding/3` draws on, so folds tried rise with
   mints (14→58 on H3 `c`, 300→740 on H0 `b`), and every later `entails/5` and
   `compute_conseq/2` runs over a larger framework.
4. **`gen6`'s cautious check is not the failure point.**
   `checking entailment ... KO` is 0 everywhere. The rejections are all at
   `gen3`.
5. **`folding result` > `folding selection`** because `folding/3` at `gen1`
   line 37 is re-satisfied on backtracking while `select_foldable` stays
   committed behind the cut at line 35. Read `folding result` as folds tried
   and `folding selection` as rules committed to folding.
6. **Brave contrast.** All seven H7a brave cells finish in ≤1.72s on either
   arm, so this cost separation is specific to cautious learning, where a check
   over every stable extension rejects most repairs.

Reproduce with:

```bash
for pat in "looking for assumption relative to" "KO, cannot introduce an assumption" \
           "generating NEW assumption" "gen5: extended ABA does not entail" \
           "gen6: rote learning" "folding result:"; do
  for col in baseline_cautious nd_cautious_sechk; do
    grep -cF "$pat" \
      causal/outputs/aba_learning/targetwise/m13_bucket3_binary_collider_and/$col/n30_seed42/cells/target-b/output/prolog.stdout
  done
done
```

---

## What the switch changed / did not / left open

**Changed (on comparable `c` cells):** assumption-repair path; every final
`delta.aba`; contrary depth / closing literals (Q1); theory thickness and
search length (Q2); failed-search cost on Fixture 1 `b` (Q3).

**Did not change:** cautious+nd+steps10+any+all+check_ic otherwise;
learner-visible inputs within pairs; `solved` on both `c` cells; presence of
mechanism parents in cautious-`c` sechk contraries (unlike brave H7a).

**Left open:** whether any further H7 work is needed; no new probe invented
here. H4/H4b scientific leads unchanged.

---

## Boundaries / non-claims

- **Not a Bucket 3 claim.**
- Do **not** rank `relto` vs `sechk` as better/worse methods.
- `solved` / predictive cover ≠ mechanism recovery.
- Do **not** treat timeouts-with-empty-logs as matching-search evidence.
- Do **not** claim H7a’s brave first-BK latch carries over unchanged under
  cautious.
- Do **not** call `nd_cautious_sechk` a published method.
- Do **not** reinterpret H4 / H4b / H7a locked leads.
- H0–H6 scientific readings preserved.

---

## Cross-links

- Investigation hub: `experiment.md`
- H7a (brave nd only): `h7a_relto_vs_sechk.md`
- H4 roots / Fixture 1 cautious relto: `h4_cautious_vs_brave.md`
- H4b Fixture 2 `c` cautious relto: `h4b_cautious_split_under_a.md`
- Probe catalogue: `future_probes.md` / `.tex`
- Bucket 3 planning hub: `../M1.3-bucket3-claims.md` (still **no claim**)
- Decision log: `docs/research/decisions.md`

## Next

H7b documentation is complete. Orchestrator / Samuel decide whether any
further H7 work is needed. Still **no Bucket 3 claim**.
