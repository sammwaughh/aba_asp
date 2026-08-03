# M13-C3 — H5 Greedy-cautious vs Greedy-brave

## Status

**H5 run / analysed.** Experimental `greedy_cautious` vs locked `aamas2025` on
all five completed deterministic Bucket 3 AAMAS collections (18 cells) is
complete and documented here (Markdown) and in `h5_greedy_cautious.tex`.

- **Lead (Analysis A):** on all **18** paired cells, Greedy-cautious matches
  Greedy-brave on **every outcome and every solved delta** (byte-identical);
  traces isomorphic aside from entailment-logging surface differences; mean
  runtime ≈ **1.84×** (still sub-second)
- **Secondary (Analysis B):** large contrasts appear only vs repository
  **`baseline_cautious`** (nd bundle) where that arm already exists — **search
  strategy**, not the brave→cautious flip inside Greedy
- Config is **experimental**; **not** a published AAMAS method; **not**
  `aamas_cautious`; **not** `baseline_cautious`
- H0–H4b remain closed / unchanged
- **Not a Bucket 3 claim**
- H6/H7 signposted only (`future_probes.md`)

Companion records: `experiment.md`; `h4_cautious_vs_brave.md`;
`h4b_cautious_split_under_a.md`; `future_probes.md`.

---

## Research question

> Under the AAMAS Greedy search bundle on the completed deterministic Bucket 3
> tables, does switching from brave to cautious learning change outcomes,
> deltas, or search paths; and how does Greedy-cautious compare to repository
> nd-cautious where that arm already exists?

---

## Main finding (Analysis A — lead)

On all **18** paired cells across the five completed deterministic Bucket 3
AAMAS collections, experimental **`greedy_cautious`** (Greedy / `mgr` / `bk` /
`relto` + `learning_mode(cautious)`) matches locked **`aamas2025`**
Greedy-brave on **every outcome and every solved delta** (byte-identical).
Learning traces are isomorphic aside from entailment-logging surface
differences (`OPTIMUM FOUND` vs `checking entailment ... OK`). Flipping
brave→cautious **inside the Greedy bundle does not change accepted or rejected
theories** on these tables.

**Verdict:** semantic-mode flip under Greedy is **inert** here; runtime is the
main observable cost (~1.6–2.3×, still sub-second; mean ≈ 1.84×).

Quoted no-sol close (H0 `a`; same under both; GC shown):

```text
folding result: a(A) <- [b_val_0(A),c_val_0(A)]
…
found: alpha_1/1 ... KO, cannot introduce an assumption for [b_val_0(A),c_val_0(A)]
* No solution found!
```

Quoted `c` success (H0; no assumption path):

```text
folding result: c(A) <- [a_val_1(A),b_val_1(A)]
gen2: extended ABA entails <E+,E-> - using folding
gen1: nothing to fold.
```

---

## Setup

| Field | Value |
|-------|--------|
| Config id | `greedy_cautious` (experimental) |
| Prolog | `configs/greedy_cautious_config.pl` (`aamas2025_config.pl` unchanged) |
| Bundle | Greedy / `mgr` / `folding_space(bk)` / `relto` / `check_ic` |
| Intervention (A) | `learning_mode(brave)` → `cautious` only |
| Pair integrity | `data.csv` / `bk.aba` / `examples.json` byte-identical AAMAS↔GC (16 non-skipped cells; H2c skips empty E±) |
| Timeout policy | 300s preserved; no budget inflation; no GC timeouts |

Five collections (18 cells):

| Probe | Fixture | Sample | Targets |
|-------|---------|--------|---------|
| H0 | `m13_bucket3_binary_collider_and` | `n30_seed42` | a,b,c |
| H1 | same | `n25_seed42` | a,b,c |
| H2 | `m13_bucket3_binary_collider_and_iso_d` | `n30_seed42` | a,b,c,d |
| H2c | same | `n2_seed42` | a,b,c,d |
| H3 | `m13_bucket3_binary_bd_and_lead_a` | `n30_seed42` | a,b,c,d |

Paths: `causal/outputs/aba_learning/targetwise/<fixture>/{aamas2025,greedy_cautious}/<sample>/`

---

## Compact outcome summary (Analysis A)

| Probe | Outcomes (both arms) | Solved Δ identical | Runtime ratio (GC/A) |
|-------|----------------------|--------------------|----------------------|
| H0 | a,b no-sol; c solved | yes (c) | ~1.8–2.0 |
| H1 | a,b,c all solved | yes | ~1.6–1.8 |
| H2 | a,b,d no-sol; c solved | yes (c) | ~1.7–1.9 |
| H2c | a,d skipped; b,c solved | yes | ~1.9–2.3 |
| H3 | a,b,d no-sol; c solved | yes (c) | ~1.6–1.9 |

Aggregate: **18/18** outcome match; **0** final assumptions in any delta; all GC
runtimes sub-second.

---

## `c` and guardrail notes

Evaluator refs remain evaluator-only. Classification of identical GC/AAMAS `c`
deltas:

| Probe | GC/AAMAS `c` delta | Class vs evaluator |
|-------|--------------------|--------------------|
| H0/H1 | `c :- a_val_1, b_val_1` | mechanism-aligned string (not automatic causal claim) |
| H2 | AND × trailing `d_val_*` | distractor-retaining predictive |
| H3 | leading `a_val_*` × `b_val_1,d_val_1` | distractor-retaining predictive |
| H1 roots | co-occurrence Horn | **spurious** (H1 stance: root `solved` incorrect) |

Only desirable deterministic target is **`c`**. Root/isolated `solved` may be
spurious; `completed_no_solution` may be the correct guardrail.

---

## Analysis B (secondary) — GC vs `baseline_cautious`

Hold **cautious**; compare **search-strategy bundles**
(`greedy+mgr+bk` vs `nd+any+all`). **Not** a single-knob `folding_mode`
ablation. Only where `baseline_cautious` already exists (H0 and H3 `n30`).

| Cell | `greedy_cautious` | `baseline_cautious` |
|------|-------------------|---------------------|
| H0 a/b | no-sol ~344/311 lines / ~0.4s | no-sol ~5031/5118 lines / ~70s |
| H0 c | Horn AND (mechanism string) | α-rich (`c :- α1, a_val_1` + contrary) |
| H3 a/b/d | short no-sol | **timeout@300s** |
| H3 c | Horn `a_val_*`×BD | H4b α-theory (`a` gates + `α3` + `d_val_1` close) |

Same outcome on H0 roots; GC reaches it via a **short greedy path**, not the
nd token ladder (H4). Different **theories** on H0/H3 `c` are search-bundle
effects under the same cautious mode.

---

## Semantics vs search-strategy

| Difference | Driver |
|------------|--------|
| GC ≡ AAMAS on all H5 pairs | **Learning mode** does not fork Greedy here |
| GC short no-sol vs baseline 5k-line no-sol (H0 roots) | **Search bundle** |
| GC Horn AND `c` vs baseline α-theory (H0/H3 `c`) | **Search bundle** |
| H3 baseline timeouts on a/b/d | **nd+all** exploration cost under cautious |

---

## Boundaries / non-claims

- **Not a Bucket 3 claim.**
- Not “cautious is better” / not mechanism recovery from `solved` or string
  match alone.
- Not an AAMAS-paper cautious algorithm; do not call the config
  `aamas_cautious`.
- Do not conflate H5 with H4/H4b (different search bundles / interventions).
- Analysis B is not a brave→cautious effect.
- H6/H7 unchanged (signposted only).

---

## Cross-links

- Investigation hub: `experiment.md`
- H4 (nd-cautious roots): `h4_cautious_vs_brave.md`
- H4b (nd-cautious on H3 `c`): `h4b_cautious_split_under_a.md`
- Probe catalogue: `future_probes.md` / `.tex`
- Bucket 3 planning hub: `../M1.3-bucket3-claims.md` (still **no claim**)

## Next

H5 documentation is complete. H6/H7 remain signposted only. Orchestrator /
Samuel decides the next move. Still **no Bucket 3 claim**.
