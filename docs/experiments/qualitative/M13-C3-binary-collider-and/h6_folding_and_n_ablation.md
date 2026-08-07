# M13-C3 — H6 folding-steps and nested-`n` ablation (search cost)

## Status

**H6 run / analysed.** Bounded procedural investigation of **search cost** under
repository `baseline_cautious` (cautious + nd / any / all / `relto`) on fixture
`m13_bucket3_binary_collider_and`. Documented here (Markdown) and in
`h6_folding_and_n_ablation.tex`.

- **H6a lead:** at fixed `n30_seed42`, root (`a`/`b`) trace length is
  approximately **linearly proportional** to permitted `folding_steps(M)`;
  extra budget beyond the failed motif is **wasted search time**
- **H6b lead:** at fixed `folding_steps(2)`, root trace length is approximately
  **linearly proportional** to sample size `n` (topology fixed; per-band
  bookkeeping grows)
- Roots `a`/`b` are **procedural diagnostics** (evaluator
  `no_observed_parent_deterministic_rule`); only child `c` is a desirable
  deterministic mechanism target
- H0–H5 remain closed / unchanged (cross-linked only)
- **Not a Bucket 3 claim**
- H7a/H7b analysed (`h7a_relto_vs_sechk.md`, `h7b_cautious_relto_vs_sechk.md`)

Companion records: `experiment.md`; `h4_cautious_vs_brave.md` (long-root cost
being explained); `h5_greedy_cautious.md` (secondary cheaper no-sol via a
different search bundle); `future_probes.md`.

---

## Research question

> Under repository-baseline cautious + nd on the closed H0 AND-collider table,
> how do permitted `folding_steps(M)` (H6a) and nested sample size `n` at fixed
> `M=2` (H6b) drive search cost (trace length / runtime) for roots without
> recoverable deterministic parent rules, and what happens to control `c`?

---

## Main findings

### H6a — folding-steps ablation (lead)

On frozen `n30_seed42`, for roots `a`/`b`, `prolog.stdout` length grows roughly
linearly with `M ∈ {1,2,5,10}` (~549 → 1047 → 2541 → 5031 lines for `a`;
mirrored for `b`). Outcome stays `completed_no_solution` at every `M`. Control
`c` solves inside `tokens(1)` with **identical** delta and **unchanged** 134-line
/~1.3s trace at all four budgets.

**Why this is predictable.** `folding_steps(M)` does **not** mean “perform
exactly M folds.” Under nd, learning starts at `tokens(1)`. When a full attempt
under the current token budget fails, `gen.pl` may print
`* Increasing folding tokens to: T1` and retry while `T1 ≤ M`. On these roots,
each budget replays essentially the **same failed cautious motif** (~9 NEW
assumptions / ~500-line band). Higher `M` therefore multiplies failed-band
replays: `lines ≈ C_fixed + M · C_band`. There is no successful `M*` on these
no-solution roots through `M=10` — raising `M` does not buy a new theory; it
only replays failure (H4’s “wasted headroom”).

### H6b — nested sample-size ablation (lead)

At fixed `folding_steps(2)`, for roots `a`/`b`, trace length grows roughly with
`n ∈ {30,60,90}` (~1047 → 1641 → 2241 lines for `a`). Search **topology is
fixed** (NEW=18, KO=32; one token increase to 2 at all three `n`). What grows
is per-band bookkeeping (more grounded E⁺/E⁻ ids; larger rote/`ert` and
subsumption sweeps; larger contrary-batch cardinalities).

**Why this is predictable.** With motif × budget structure held fixed, cost per
band should scale roughly with grounding / example size → total length roughly
∝ `n` in this limited range. Support **presence** of the four atoms
`(0,0,0)/(0,1,0)/(1,0,0)/(1,1,1)` is already complete at n=30; multiplicities
and computational grounding size change. H6b is **not** “pure compute with
every statistical property fixed.” Line ratios are near-linear; runtime is
slightly more superlinear (ASP/consequence). Do not claim a universal
complexity law.

### Cross lead (one sentence)

H4’s long root traces (~5k lines / ~66–70s at n30×steps10) are primarily
**cumulative nd token-budget replays** of one cautiously failed motif (H6a),
with a secondary per-band cost that grows with `n` at fixed `M=2` (H6b);
control `c` stays solved and delta-stable; nothing here is root mechanism
recovery or an `n×steps` interaction result.

---

## Setup

| Field | Value |
|-------|--------|
| Fixture | `m13_bucket3_binary_collider_and` |
| Bundle | cautious + nd / any / all / `relto` / `check_ic` |
| Base Prolog | `configs/baseline_cautious_config.pl` (`folding_steps(10)`; unchanged) |
| Ablation Prolog | `configs/baseline_cautious_steps{1,2,5}_config.pl` (match baseline except `M`) |
| H6a | fixed `n30_seed42`; `M ∈ {1,2,5,10}` (steps10 = reused H4 collection) |
| H6b | fixed `M=2`; nested `n30`/`n60`/`n90` seed 42 |
| Timeout | 300s preserved; no budget inflation |
| Stance | roots = procedural cost diagnostics; `c` = control / only desirable det. target |

Sample nesting (verified): n30 ⊂ n60 ⊂ n90; n30 csv sha256
`1edae465d0f6b6b662b3c4ed4863af21c1d9b0c1cf428774731dd3f43282a8ca` unchanged.
Atom counts `(0,0,0)/(0,1,0)/(1,0,0)/(1,1,1)`: n30 2/4/7/17; n60 4/10/12/34;
n90 5/17/18/50.

### Collections

| Role | `configuration.id` | sample | `folding_steps` |
|------|--------------------|--------|-----------------|
| H6a | `baseline_cautious_steps1` | `n30_seed42` | 1 |
| H6a/H6b | `baseline_cautious_steps2` | `n30_seed42` | 2 |
| H6a | `baseline_cautious_steps5` | `n30_seed42` | 5 |
| H4 reuse | `baseline_cautious` | `n30_seed42` | 10 |
| H6b | `baseline_cautious_steps2` | `n60_seed42` | 2 |
| H6b | `baseline_cautious_steps2` | `n90_seed42` | 2 |

Paths:
`causal/outputs/aba_learning/targetwise/m13_bucket3_binary_collider_and/<config>/<sample>/`

YAMLs:
`causal/configs/targetwise/m13_bucket3_binary_collider_and/<config>/<sample>.yaml`

### Commands (representative)

```bash
python -m causal.targetwise.cli run \
  --config causal/configs/targetwise/m13_bucket3_binary_collider_and/baseline_cautious_steps1/n30_seed42.yaml
python -m causal.targetwise.cli run \
  --config causal/configs/targetwise/m13_bucket3_binary_collider_and/baseline_cautious_steps2/n30_seed42.yaml
python -m causal.targetwise.cli run \
  --config causal/configs/targetwise/m13_bucket3_binary_collider_and/baseline_cautious_steps5/n30_seed42.yaml
python -m causal.targetwise.cli run \
  --config causal/configs/targetwise/m13_bucket3_binary_collider_and/baseline_cautious_steps2/n60_seed42.yaml
python -m causal.targetwise.cli run \
  --config causal/configs/targetwise/m13_bucket3_binary_collider_and/baseline_cautious_steps2/n90_seed42.yaml
```

H4 steps-10 collection **reused** (not rerun):
`.../baseline_cautious/n30_seed42/` — `summary.json` sha256
`1e4b4199fe03a5a6208967b092450f67717d4e0dc788271f771c0d18b1ff23de`.

Engine gate (read-only): `gen.pl` increases `tokens(T)` while `T+1 ≤ M` under
`folding_mode(nd)`; initialisation is `tokens(1)` (`folding.pl` / `aba_asp.pl`).

---

## Verified outcome table

Recorder-verified against `metrics.json` (`aba_learning_runtime_s`) and
`output/prolog.stdout` (line counts; `Increasing folding tokens`;
`generating NEW assumption`; `KO`). Roots `a`/`b` mirrored; `c` control.

| sample | steps | t | outcome | runtime_s | lines | token increases | NEW asm | KO |
|--------|------:|---|----------|----------:|------:|-----------------|--------:|----:|
| n30 | 1 | a | completed_no_solution | 6.638 | 549 | none (stay at 1) | 9 | 16 |
| n30 | 1 | b | completed_no_solution | 6.797 | 555 | none | 9 | 16 |
| n30 | 1 | c | solved | 1.304 | 134 | — | 1 | 1 |
| n30 | 2 | a | completed_no_solution | 13.117 | 1047 | to 2 | 18 | 32 |
| n30 | 2 | b | completed_no_solution | 13.487 | 1062 | to 2 | 18 | 32 |
| n30 | 2 | c | solved | 1.279 | 134 | — | 1 | 1 |
| n30 | 5 | a | completed_no_solution | 32.775 | 2541 | to 2..5 | 45 | 80 |
| n30 | 5 | b | completed_no_solution | 32.825 | 2583 | to 2..5 | 45 | 80 |
| n30 | 5 | c | solved | 1.271 | 134 | — | 1 | 1 |
| n30 | 10 | a | completed_no_solution | 69.952 | 5031 | to 2..10 | 90 | 160 |
| n30 | 10 | b | completed_no_solution | 66.473 | 5118 | to 2..10 | 90 | 160 |
| n30 | 10 | c | solved | 1.288 | 134 | — | 1 | 1 |
| n60 | 2 | a | completed_no_solution | 22.169 | 1641 | to 2 | 18 | 32 |
| n60 | 2 | b | completed_no_solution | 22.617 | 1659 | to 2 | 18 | 32 |
| n60 | 2 | c | solved | 2.126 | 200 | — | 1 | 1 |
| n90 | 2 | a | completed_no_solution | 32.291 | 2241 | to 2 | 18 | 32 |
| n90 | 2 | b | completed_no_solution | 32.894 | 2262 | to 2 | 18 | 32 |
| n90 | 2 | c | solved | 3.033 | 266 | — | 1 | 1 |

Integrity (reconfirmed):

- H6a n30: learner-visible `bk.aba` / `examples.json` / `data.csv` **identical
  across steps 1/2/5/10** per target.
- Control `c` `delta.aba` **byte-identical** on all six H6 collections
  (sha256 `f9f75b60631b2a2aaac951521823e073bbfd5c73bd7aa96d259ca45cd426865a`):

```prolog
c(A) :- alpha_1(A), a_val_1(A).
c_alpha_1(A) :- b_val_0(A).
assumption(alpha_1(A)).
contrary(alpha_1(A),c_alpha_1(A)) :- assumption(alpha_1(A)).
```

---

## Analysis A — folding-step ablation (H6a)

### Mechanistic picture

Under nd, a failed attempt at current token budget `T` can bump to `T+1` if
`T+1 ≤ M` (`gen.pl`):

```prolog
retract(tokens(T)),
T1 is T+1,
lopt(folding_steps(M)),
( T1 > M -> fail ; true ),
write('* Increasing folding tokens to: '), write(T1), nl,
assert(tokens(T1)),
genT(...).
```

On these roots the **decisive cautious KO** already occurs inside the first
budget band (brave residual gadget refusal; same fork as H4):

```text
folding result: c_alpha_3(A) <- [b_val_0(A)]
found: alpha_2/1 ... KO, cannot introduce an assumption for [b_val_0(A)]
```

Canonical 9-assumption motif: `NEW = 9×M` (9, 18, 45, 90). Steps1 body from
after the `lopt(...)` dump equals steps2 band-0 for **522** lines; then steps1
prints `* No solution found!` while steps2 prints
`* Increasing folding tokens to: 2` (first increase at stdout line 549). Higher
`M` replays the same failed search at higher printed fold counters; still no
multi-literal fold bodies in these bands.

Rough linearity for target `a`: lines/M ≈ 549, 524, 508, 503 across M=1,2,5,10
— consistent with `C_fixed + M · C_band` and a ~500-line failed band.

### Cross-run trace audit (added 2026-08-07, no new learner runs)

The "same failed search" reading above was checked exactly across every
recorded nd trace, not only the H6a cells. Audit script:
`docs/experiments/qualitative/M13-C3-binary-collider-and/band_replay_audit.py`.

```bash
python docs/experiments/qualitative/M13-C3-binary-collider-and/band_replay_audit.py
```

Output summary:

```text
nd traces audited: 49
every folding call consumed exactly one token: True
total token-exhaustion failures across all nd traces: 0
total multi-atom to-be-folded lists: 0
traces that raised the token allowance: 14
  of those, every search attempt identical after normalisation: 14
  per-attempt size range: 497..9747 lines
```

Two facts recorded from this:

1. **Token saturation.** `fold_nd_wtc/7` prints ` C: folding …` before each step
   and ` C: DONE` on completion. In all 49 nd traces the DONE counter is exactly
   one below the folding counter, every to-be-folded list printed has a single
   atom, and the ` 0: FAIL - No more folding tokens left` diagnostic appears
   nowhere. Under the exact-value encoding the rote rule body is one row-id
   equality (`ert: a(A) <- [A=1]`) and each BK rule is `b_val_1(A) :- A=1`, so
   one step empties the fold list. `folding_steps(M)` therefore never widens the
   reachable fold space in these runs; it only permits restarts.
2. **Attempt identity.** Splitting each trace at `* Increasing folding tokens
   to:` and normalising `alpha_N`, `_N`, and the printed token counter, all M
   attempts within a trace are identical for all 14 cells that raised the
   allowance. For `baseline_cautious` target `a` at M=10: 5031 lines = 51-line
   preamble + 10×497-line attempts + 9 restart lines + 1 closing line
   (target `b`: 506-line attempts). Same holds under `nd_cautious_sechk`
   (1367 / 1376-line attempts) and on the H3 fixture (9467 / 9747-line
   attempts), so the multiplication is independent of per-attempt cost.

Outcome breakdown over the 49 nd cells: 30 `solved`, all inside `tokens(1)`;
19 `completed_no_solution`, of which 14 raised the allowance and 5 are
`folding_steps(1)` configurations where no restart is possible.

This audit supports Finding 4 of
`docs/experiments/qualitative/M13-C3-binary-collider-and/findings_for_fabrizio.tex`.
It is an audit of the recorded runs, not a proof about `fold_nd_wtc/7` for
arbitrary BK: BK rules with multi-atom bodies would leave atoms to fold after
the first step.

### Control `c` (H6a)

Solved every `M`; same delta (`α1` + `a_val_1`; contrary `b_val_0`); **134 lines
/ ~1.3s** at all n30 budgets; **no** token increases. Varying `M` does not
inflate the control trace when the learner finishes inside `tokens(1)`.

---

## Analysis B — nested sample-size ablation (H6b)

Fixed `M=2`. Root outcomes unchanged (`completed_no_solution`). Topology
unchanged: NEW=18, KO=32, single increase to tokens 2. Growth:

| n | `a` lines | `a` runtime_s | `c` lines | `c` runtime_s |
|--:|----------:|--------------:|----------:|--------------:|
| 30 | 1047 | 13.117 | 134 | 1.279 |
| 60 | 1641 | 22.169 | 200 | 2.126 |
| 90 | 2241 | 32.291 | 266 | 3.033 |

Line increments for `a`: +594 (30→60), +600 (60→90) — near-constant per +30
rows in this range. Runtime rises somewhat faster than lines (ASP/consequence
cost). Control `c` keeps the **same delta bytes**; its trace also lengthens
mildly with `n` (134→200→266) while remaining far cheaper than root no-sol
paths.

Preserve: support **presence** already at n=30; multiplicities change
(2/4/7/17 → 4/10/12/34 → 5/17/18/50). H6b measures grounding/bookkeeping
growth under fixed topology, not a new information regime that flips outcomes.

### Cross-n trace audit (added 2026-08-07, no new learner runs)

"Topology unchanged" was sharpened from matching event counts to an exact
ordered comparison. Audit script:
`docs/experiments/qualitative/M13-C3-binary-collider-and/support_vs_multiplicity_audit.py`.

```bash
python docs/experiments/qualitative/M13-C3-binary-collider-and/support_vs_multiplicity_audit.py
```

Output:

```text
Decision-sequence identity across nested sample sizes
 target                    decisions  identical
      a              [238, 238, 238]        yes
      b              [238, 238, 238]        yes
      c                 [14, 14, 14]        yes

Target a: total trace lines [1047, 1641, 2241]
  constant categories:  39, holding [513, 513, 513] lines
  growing categories:    5, holding [534, 1128, 1728] lines
       [192, 432, 672]  * subsumed: deleted!
       [166, 342, 518]  evaluating subsumption of a(A) <- [A=_]
        [96, 188, 286]  ert: c_alpha_N(A) <- [A=_]
        [56, 120, 184]  evaluating subsumption of c_alpha_N(A) <- [A=_]
          [24, 46, 68]  ert: a(A) <- [A=_]
```

Facts recorded:

1. **Decision identity.** The ordered sequence of `gen1`–`gen6` steps, folding
   results, assumption introductions, entailment checks, and token increases is
   *identical* at n=30/60/90 after normalising `_N` and `A=<row>`: 238 decisions
   for `a`, 238 for `b`, 14 for `c`. This is stronger than the NEW=18 / KO=32
   count match already recorded above.
2. **Where cost goes.** Lines split into 39 constant categories (exactly 513
   lines at every n, for both `a` and `b`; 63 for `c`) and 5 growing categories,
   all rote-rule creation and subsumption bookkeeping. `ert:` counts equal the
   positive-example multiplicities: `a` 24/46/68, `b` 21/44/67, `c` 17/34/50.

Caveat for target `c`: the audit also lists three singleton "Writing solution
no. # to targetwise_<hash>.sol.aba" categories. Those are per-run artefact
filenames, not growth.

This audit supports Finding 5 of
`docs/experiments/qualitative/M13-C3-binary-collider-and/findings_for_fabrizio.tex`.
It does **not** establish that deduplication is safe: H6b varies nested `n`, and
a support-compressed table would also renumber rows, which can interact with
`folding_selection(any)`. That remains an untested probe.

---

## Cross-analysis vs H4 and secondary H5

**vs H4.** H4’s ~5031/5118-line / ~70s root no-sols are the `M=10` endpoint of
H6a: ten failed-band replays of the cautious motif that already KO’s inside
budget 1. H6a explains that cost as **search-budget headroom**, not as
“cautious needing more folds to recover a root mechanism.”

**vs H5 (pointer only).** Experimental `greedy_cautious` on the same H0 root
`a` reaches the **same** `completed_no_solution` in ≈ **344 lines / 0.42s** via
a different search bundle (Greedy / `mgr` / `bk`). H4’s cost is therefore not
“cautious alone” — it is cautious **under the nd token ladder**. This is not a
single-knob `folding_mode` ablation (same framing as H5 Analysis B).

---

## Boundaries / non-claims

- **Not a Bucket 3 claim.**
- Not “cautious is better.”
- Root `completed_no_solution` is **not** mechanism recovery; roots have
  `no_observed_parent_deterministic_rule`.
- Budget-relative `completed_no_solution` ≠ proof of unlearnability at larger
  `folding_steps`.
- Control `c` delta stability / `solved` is **not** automatic causal recovery
  (still separate: procedural success · cover · mechanism-aligned string).
- Do **not** expand H6 into an `n × folding_steps` interaction claim (that
  grid was not run).
- Approximate / rough linearity only in these limited slices — not a universal
  complexity law.
- H7b analysed separately; H0–H5 scientific readings preserved.

---

## Cross-links

- Investigation hub: `experiment.md`
- H4 long-root story: `h4_cautious_vs_brave.md`
- H5 Greedy-cautious contrast: `h5_greedy_cautious.md`
- Probe catalogue: `future_probes.md` / `.tex`
- Bucket 3 planning hub: `../M1.3-bucket3-claims.md` (still **no claim**)
- Decision: `docs/research/decisions.md` (2026-08-03 H6 entry)

## Next

H6 documentation is complete. H7a is run / analysed
(`h7a_relto_vs_sechk.md`). H7b is run / analysed (`h7b_cautious_relto_vs_sechk.md`). Still **no Bucket 3 claim**.
