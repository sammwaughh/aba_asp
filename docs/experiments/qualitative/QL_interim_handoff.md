# QL1–QL4 interim-report handoff pack

> **Scope guard.** The qualitative investigations evaluate **target-wise parent-set
> recovery** under the **current `aba_asp/causal` implementation** (the **target-wise ABA
> Learning pipeline**). They do **not** evaluate full Russo-style Causal ABA, graph recovery,
> d-separation reasoning, `arr`/`noe`/`indep` assumptions, or stable-extension-as-DAG
> machinery. Prefer "parent-set recovery", "learned target-rule body", and "causal-adjacent
> structure" over "learned causality". Metrics diagnose alignment between **learned
> target-rule bodies** for `x2` and the known direct parents of `x2`; they do **not** prove
> causal discovery.

> **Status.** This pack synthesises **QL1 (QI-001)**, **QL2 (QI-002)**, **QL3 (QI-003)**, and
> **QL4 (QI-004)**. QL4 has now completed; its outputs
> (`causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20/`) and generated summary
> (`docs/experiments/qualitative/QI004_scaled_motifs_n20_summary.md`) exist and are
> incorporated below. This supersedes the earlier QL1–QL3-only pack
> (`QL1_QL3_interim_handoff.md`), in which all QL4 entries were placeholders.

> **Naming.** Report-side labels QL1/QL2/QL3/QL4 map to repo experiment IDs
> QI-001 / QI-002 / QI-003 / QI-004.

---

## 1. The qualitative investigation sequence (why each run followed the last)

1. **QL1 (QI-001) — initial motif × data-mode probe.** 9 cells (3 motifs × 3 data modes),
   target `x2`, all solved. Recovery was uneven: fork recovered cleanly in every mode (but
   fork's parent *is* `x0`, so this is confounded with a first-column preference); the
   collider recovered fully only in binary; the chain essentially never recovered its true
   parent `x1` (it cited `x0`). Two **design** problems surfaced: the **x0/first-column
   confound** and an **unjustified tiny sample size** (4–5 rows, so the true parent was not
   guaranteed to be the unique perfect rule).

2. **QL2 (QI-002) — principled minimal baseline.** Introduced to remove QL1's tiny-table
   weakness. Complete, noiseless truth tables (8 rows binary, 18 rows cat3) make the true
   parent the *unique* zero-error separator, so the perfect rule is learnable **in
   principle**. Result: clean recovery on only **half** the cells (binary 2/3, cat3 1/3); the
   collider fails even noiselessly (binary: no solution; cat3: subset) and the cat3 chain
   recovers the ancestor. The complete factorial is also a principled **data-level** correction
   against the x0 confound: it decorrelates non-parents from `x2` and makes the canonical chain
   cell (`x0 ⊥ x2`) a genuine probe of positional x0-preference (binary's clean `{x1}` recovery
   argues against a pure x0-bias; the cat3 chain's `x0` citation is consistent with an
   artefact). What QL2 does **not** provide is the *full symmetric* break — the fork's parent
   *is* `x0`, there is no correlated-ancestor test, and no within-structure parent-position
   swap; that is QL3/QL4's job.

3. **QL3 (QI-003) — scaled, noisy, confound-controlled attempt at `n=100`.** Added realistic
   scale + noise and **parent-position variants** (chain/fork in both orientations) so a
   learner that merely prefers `x0` would fail the `*_x1parent` cells. It hit a
   **computational-feasibility wall**: categorical/continuous cells timed out at 120 s and
   binary cells failed instantly on the all-zero-positive encoding limitation; **0 cells
   solved**. QL3 therefore contributes a documented feasibility/limitation result, not
   recovery evidence.

4. **QL4 (QI-004) — feasible re-run of the QL3 design.** Same conceptual design as QL3, with
   only `n` reduced to **20** and the Prolog timeout raised to **300 s**. It **completed all
   15 cells with no timeouts**, making the scaled/noisy design interpretable for the first
   time — but it recovered **no clean parent set in any cell** (`clean_recovery = 0` for all
   15). See §5.

---

## 2. Why QL4 followed QL3

QL3's `n=100` configuration was computationally infeasible under the available learner/timeout
budget: every categorical/continuous cell exceeded the 120 s Prolog timeout, and every binary
cell tripped the all-zero-positive encoding limitation, leaving 0 solved cells and no recovery
evidence. To examine the scaled/noisy and continuous/discretisation questions at all, QL4 keeps
the QL3 design but changes only the two feasibility settings (`n` 100→20, timeout 120→300 s).
The reduced sample size requires a new fixtures module (`handcrafted_qi004.py`) because the
`handcrafted_table` path uses the fixture's own table and ignores the grid `n`.

---

## 3. Final canonical evidence set

| Role | Canonical run(s) | Why |
|---|---|---|
| Encoding/motif sensitivity of recovery | **QL1 (QI-001)** | 9/9 solved; shows recovery varies by motif and data mode |
| Best-case (noiseless) learnability of the parent rule | **QL2 (QI-002)** | complete truth tables; clean_recovery 0.5; collider fails even ideally |
| Scaled/noisy feasibility + scaled-recovery (null) result | **QL4 (QI-004)** | completes 15/15 at `n=20`; recovers nothing clean |
| `n=100` computational-feasibility wall + binary encoding limitation | **QL3 (QI-003)** — audit/feasibility note only | 0 solved; preserved as a recorded limitation, not recovery evidence |

QL4 is the canonical *scaled/noisy* run (supersedes QL3 for that role). The canonical
*parent-recovery* evidence remains QL1 + QL2, because QL4's recovery finding is null.

---

## 4. Run-level summary table (QL1–QL4)

All runs: target `x2` only; target excluded from BK; learner = default non-deterministic
folding (`folding_mode: nd`, `folding_steps: 15`); `graph_type: handcrafted_table`; grid
`seed: [0]`; `bins: 3`, `bin_strategy: uniform` for continuous cells. Env `aba-asp`;
SWI-Prolog 10.0.2; clingo 5.8.0.

| Run | Experiment id | Cells | n | Timeout | Modes | Outcome distribution | Clean-recovery | Role |
|---|---|---|---|---|---|---|---|---|
| **QL1** | `QI001_motifs_modes` | 9 | 4–5 | 120 s | bin, cat3, cont3 | 9 solved | (rule-level metrics; no clean_recovery field) — fork clean all modes, collider binary clean, chain never clean | encoding/motif sensitivity |
| **QL2** | `QI002_minimal_motifs` | 6 | 8 (bin) / 18 (cat3) | 120 s | bin, cat3 | 5 solved, 1 no-solution | **0.500 (3/6)**; bin 2/3, cat3 1/3 | best-case learnability |
| **QL3** | `QI003_scaled_motifs` | 15 | 100 | 120 s | bin, cat3, cont3 | 0 solved; 8 timeout, 5 error (binary), partial/aborted | n/a (0 solved) | feasibility wall (audit only) |
| **QL4** | `QI004_scaled_motifs_n20` | 15 | 20 | 300 s | bin, cat3, cont3 | **1 solved, 12 no-solution, 2 error; 0 timeout** | **0.000 (0/15)** | scaled/noisy (null recovery) |

QL1/QL2/QL3 numbers are reproduced from `QL1_QL3_interim_handoff.md`; QL4 numbers are from
`QI004_scaled_motifs_n20_summary.md` and per-cell `metrics.json`.

---

## 5. QL4 result summary

- **Design.** 5 structural variants (`chain_x0parent {x0}`, `chain_x1parent {x1}`,
  `fork_x0parent {x0}`, `fork_x1parent {x1}`, `collider {x0,x1}`) × 3 data modes
  (binary, categorical-3, continuous-3-bin) × target `x2` = 15 cells, `n=20`, mild noise.
- **Feasibility.** 15/15 cells completed within the 300 s budget; **no timeouts** (max
  wall-clock 272.8 s). Every cell has `metrics.json`. This resolves the QL3 timeout wall.
- **Outcomes.** 1 `solved`, 12 `completed_no_solution`, 2 `error`. The 2 errors are binary
  (`fork_x0parent_binary`, `collider_binary`), each failing with `ERROR: unknown constant`
  (the recorded all-zero-positive binary encoding limitation).
- **Recovery.** `clean_recovery = 0` for all 15 cells (0 in every data mode). The only cell
  with any learned `x2` rule is `qi004_chain_x1parent_binary`:

```prolog
x2(A) :- alpha_1(A), x0(A).
x2(A) :- x1(A).
```

  It recovers the **superset** {x0, x1} (true parents {x1}): precision 0.5, recall 1.0,
  Jaccard 0.5, `ancestor_only_rate` 0.5, 1 assumption, 1 contrary. So it cites the true
  parent but also the ancestor `x0`.
- **Coverage.** Across all cells `cov_pl_pos = 0.000`, `cov_pl_neg = 1.000`; even the solved
  cell accepts none of its positive examples under Prolog-aware evaluation.
- **Continuous bin-health.** All 5 `*_cont3` cells had all three uniform bins non-empty for
  `x0` and `x1` (min bin counts 3–5), so continuous non-recovery is not a binning artefact.
- **Confound check.** Could **not** be exercised: only one cell solved, and it cites both
  columns, so "tracks the true parent column" vs "favours `x0`" is undetermined. The x0
  confound remains empirically unbroken.

Full per-cell table: `QI004_scaled_motifs_n20/run_log.md`; per-cell rules/metrics:
`QI004_scaled_motifs_n20_summary.md`; structured interpretation:
`QI004_scaled_motifs_n20/interpretation.md`.

---

## 6. Updated cautious claims

### Supported (verify against `docs/report/claims_ledger.md` before use)

- The current `aba_asp/causal` implementation **runs end-to-end** on small controlled motif
  fixtures and produces inspectable learned `x2` target rules (QL1: 9/9 solved; QL2: 5/6
  solved; QL4: 1/15 solved + 12 no-solution that still complete).
- Parent-set recovery is **sensitive to data encoding and motif**: under canonical
  orientation, fork (parent `x0`) recovers cleanly across modes while chain (parent `x1`) and
  collider recover poorly outside binary (QL1, QL2).
- **Even in the ideal noiseless complete-truth-table case, clean recovery is not guaranteed**
  (QL2: clean_recovery 0.5; collider binary no solution; cat3 chain recovers the ancestor).
- The `n=100` setting is **computationally infeasible** under the current learner/timeout
  budget (QL3: 0 solved; 8 timeouts, 5 binary encoding errors).
- At `n=20` with a 300 s timeout, the scaled/noisy design becomes **tractable** (QL4: 15/15
  complete, 0 timeouts), but the pipeline **recovers no clean parent set** in any motif/mode
  (QL4: clean_recovery 0/15); the one learned rule set is an **ancestor-contaminated
  superset**.
- The **binary all-zero-positive encoding limitation** is real and recurs at `n=20`
  (QL3: 5 binary errors at `n=100`; QL4: 2 binary errors at `n=20`).

### Not supported (explicitly excluded)

- ❌ Full Russo-style **Causal ABA** (no `arr`/`noe`/`indep`, no d-separation, no
  stable-extension-as-DAG in the code path).
- ❌ **Causal discovery / DAG recovery / edge orientation** of the motifs (learned bodies are
  predictor sets, not oriented edges).
- ❌ The **x0/first-column confound is *fully* broken**. (QL2 corrects it at the data level —
  the complete factorial decorrelates non-parents and turns the chain cell into a
  positional-bias probe, with binary `{x1}` recovery arguing against a pure x0-bias — but the
  full *symmetric* break, i.e. resolving the fork in isolation, testing against a correlated
  ancestor, and a within-structure parent-position swap, is not achieved; QL3 unsolved; QL4 had
  only one solved cell, citing both columns, so the `*_x0parent` vs `*_x1parent` comparison was
  never exercised.)
- ❌ **Parent recovery improves at scale under noise** (QL4: 0/15 clean).
- ❌ **Continuous/categorical recovery improved over QL1** (QL4 continuous/categorical cells
  recover nothing; they merely complete).
- ❌ The single QL4 solved rule "found the cause" (it over-includes the ancestor and has 0.0
  positive coverage).
- ❌ Anything derived from the **reserved** graph-level metrics (`skel_*`, `dir_*`, `shd`,
  `bridge_*`) — not computed.

---

## 7. Updated limitations

- **Conceptual.** Target-wise learned-rule / parent-set recovery, best treated as
  predictive-association recovery that *may* align with parents; not Causal ABA.
- **Confound (partially corrected; full break open).** QL2's complete factorial corrects the
  x0/first-column confound at the **data level** (non-parents decorrelated from `x2`; the chain
  cell becomes a positional-bias probe, and binary `{x1}` recovery argues against a pure
  x0-bias). The *full symmetric* break — fork-in-isolation, a correlated-ancestor test, and a
  within-structure parent-position swap — is still not empirically achieved (QL3 unsolved; QL4
  too few solved cells).
- **Scale.** Prolog learning does not complete within 120 s at `n=100`; at `n=20` it
  completes but the categorical/continuous cells still take tens to ~270 s each.
- **Recovery at the feasible scale is null.** At `n=20`, outcomes are dominated by
  `completed_no_solution`, limiting how much can be inferred about variable preference.
- **Encoding.** Binary all-zero-positive rows can trip `check_ep_consts_aux`
  (`unknown constant`); recorded, not fixed.
- **Coverage vs structure.** High negative exclusion (1.0) co-exists with 0.0 positive
  coverage even in the solved cell; coverage is behavioural, not structural.
- **Continuous handling.** Continuous variables are binned (3 uniform bins) before learning;
  recovery is over bin predicates.
- **Determinism / breadth.** Single seed (`seed: [0]`); deterministic fixtures; no
  greedy-vs-nd comparison (that is QN-001). Per-cell `interpretation.md` for QL1–QL3 remain
  templates; QL4's is filled from the summary.

---

## 8. What should be written in the interim report

> Provisional bullets — *what to write*, not finished prose. Final prose is drafted by ChatGPT
> from reviewed records and checked against `docs/report/claims_ledger.md`.

```latex
\subsection{Qualitative investigation: target-wise parent-set recovery}
```

- **Aim and scope.** Object = target-wise recovery of `x2`'s direct parents via the current
  `aba_asp/causal` implementation; explicitly *not* Causal ABA / graph recovery / d-separation
  / stable-extension-as-DAG. Success = learned `x2` rule body variables == true direct parents.
- **Setup.** 3 canonical 3-node motifs; target `x2` excluded from BK; data modes binary
  (bare predicates), categorical-3 (`_val_v`), continuous-3-bin (`_binK`); learner = inherited
  ABALearn, nd folding, `folding_steps: 15`; SWI-Prolog/clingo; env `aba-asp`.
- **Metrics and interpretation rule.** Lead with `clean_recovery` + variable-level
  precision/recall/Jaccard (QL2+); QL1 used rule-level body-parent metrics. State the rule:
  alignment with known parents, **not** causal discovery; coverage is behavioural; reserved
  graph metrics are not computed.
- **QL1 (QI-001).** 9 cells, all solved; fork clean everywhere, collider partial outside
  binary, chain cites `x0` not `x1`. Surface the x0 confound and the unjustified tiny `n`.
- **QL2 (QI-002).** Complete noiseless truth tables; perfect rule learnable in principle.
  Clean recovery 3/6 (binary 2/3, cat3 1/3); collider fails even noiselessly. The complete
  factorial is a data-level correction against the x0 confound (decorrelates non-parents; chain
  cell becomes a positional-bias probe — binary `{x1}` argues against a pure x0-bias); the full
  symmetric break (fork-in-isolation, correlated-ancestor test, parent-position swap) is still
  open and is QL3/QL4's job.
- **QL3 → QL4 (scaled continuous/discretisation check).** QL3: `n=100` feasibility wall
  (timeouts + binary encoding errors; 0 solved). QL4: `n=20`, 300 s; 15/15 complete, no
  timeouts, but **0/15 clean recovery**; continuous cells now complete yet recover nothing;
  the one learned rule is an ancestor-contaminated superset; confound still not decided.
- **Interim interpretation.** Recovery is encoding- and motif-sensitive (binary friendliest);
  even ideal noiseless conditions do not guarantee clean recovery; at the feasible scale
  (`n=20`) with noise the pipeline recovers nothing clean; the x0 confound is acknowledged but
  not empirically broken.
- **Limitations.** Implementation ≠ Causal ABA; predictor-set not oriented edges; binary
  encoding limitation; Prolog scaling limits; continuous binning; single seed; exploratory.
- **Decision for next quantitative work.** The unbroken confound and null scaled-recovery gate
  any quantitative parent-recovery benchmarking (cf. QN-001). Candidate design changes recorded
  but deferred: binary encoding fix; intermediate `n` / more positive examples; greedy-vs-nd.

---

## 9. Exact QL4 artefact paths

**Config**
- `causal/configs/experiments/QI004_scaled_motifs_n20.yaml` (`n=20` via fixtures,
  `prolog_timeout_s: 300`, 15 dgps, `seed: [0]`, `target: [x2]`)

**Fixtures / tests**
- `causal/experiments/handcrafted_qi004.py` (`_N=20`, `_BASE_SEED=20040002`; reuses N-agnostic
  helpers from `handcrafted_qi003.py`); registered in `causal/experiments/handcrafted.py`
- `causal/tests/test_qi004_fixtures.py`

**High-level record + operational dossier**
- `docs/experiments/qualitative/QI-004.md`
- `docs/experiments/qualitative/QI004_scaled_motifs_n20/` — `README.md`, `run_log.md`
  (full per-cell table + run-configuration audit), `interpretation.md` (8-section structured
  interpretation), `artefacts.md` (cell→run_id map), `metrics.md`, `decision_record.md`

**Generated summary**
- `docs/experiments/qualitative/QI004_scaled_motifs_n20_summary.md`

**Run outputs**
- `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20/` — `results.parquet`,
  `manifest.json`, and `cells/<run_id>/` per-cell dirs (`bk.aba`, `metrics.json`,
  `metrics.parquet`; `bk.sol.aba` only for the solved cell `d97c1b0c8c7c`)

**Metrics spec**
- `causal/aa-plans/METRICS.md` (variable-level metrics: §3.4b)

**Index / register**
- `docs/experiments/experiment_index.md`; `docs/research/experiment_register.md`

---

## 10. Remaining questions for Samuel / ChatGPT before interim-report writing

1. **Label mapping.** Report uses QL1–QL4 or repo QI-001…QI-004 (or both with a mapping
   note)? This pack assumes QL↔QI.
2. **QL1 metric basis.** QL1 used rule-level `body_parent_*`; QL2+ use
   `clean_recovery`/variable-level. Re-describe QL1 against the stricter metric, or report
   as-is with a footnote?
3. **QL4 framing.** Confirm QL4 should be framed as "feasibility achieved, recovery null":
   the headline is that the design now runs but recovers nothing clean at `n=20`.
4. **Confound emphasis.** How prominently to frame the still-unbroken x0/first-column confound,
   given neither QL3 nor QL4 could decide it?
5. **Collider failure.** Dedicated paragraph (it under-recovers even noiselessly in QL2 and
   produces nothing in QL4), or fold into the encoding-sensitivity point?
6. **Scope sentence.** Confirm exact wording for "parent-set recovery, not causal discovery"
   to standardise across the report (align with `claims_ledger.md`).
7. **Binary encoding limitation.** Report as a methods caveat now, or defer until a fix is
   scoped? (It recurs in both QL3 and QL4.)
8. **Next-step design.** Does the null QL4 result warrant a redesigned follow-up (intermediate
   `n`, more positives, encoding fix) before any quantitative work, or is the qualitative
   investigation concluded for the interim?
