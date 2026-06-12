# QI-004 interpretation (QI004_scaled_motifs_n20)

> Scope: QL4 evaluates **target-wise parent-set recovery** under the **current `aba_asp/causal` implementation** (the **target-wise ABA Learning pipeline**). It does NOT evaluate full Russo-style Causal ABA, graph recovery, d-separation reasoning, `arr`/`noe`/`indep`, or stable-extension-as-DAG machinery. "Recovery" throughout means alignment between **learned target-rule bodies** for `x2` and the known direct parents of `x2`; it is not causal discovery.

Status: structured interpretation written from the generated summary (`../QI004_scaled_motifs_n20_summary.md`) and per-cell `metrics.json`. Learned rules are quoted exactly. Interpretation is factual and bounded; final report prose is left to Samuel/ChatGPT.

---

## 1. Purpose of QL4

QL4 (`QI004_scaled_motifs_n20`) was introduced after the QL3 (`QI003_scaled_motifs`, `n=100`) run proved computationally infeasible: under a 120 s Prolog timeout its categorical-3 / continuous-3 cells timed out and its binary cells failed instantly on an encoding limitation, so QL3 produced **0 solved cells** and no parent-recovery evidence (it is preserved only as a feasibility/limitation note).

QL4 keeps the QL3 design idea — **scaled, noisy motifs with parent-position controls**, across binary / categorical-3 / continuous-binned data modes — but changes only the two computational-feasibility settings:

- sample size reduced from `n=100` to **`n=20`**;
- Prolog timeout raised from 120 s to **300 s**.

The goal was to make the run tractable so that the continuous/discretisation question and the `*_x0parent` vs `*_x1parent` confound check could actually be examined on completed cells, rather than blocked behind timeouts.

---

## 2. Raw result summary

15 cells (5 structural variants × 3 data modes), target `x2`, `n=20`. All 15 cells completed within the 300 s budget (no timeouts; max wall-clock 272.8 s). Overall `clean_recovery` rate: **0.000 (0/15)**; by mode binary 0/5, cat3 0/5, cont3 0/5.

| Cell / source | Motif / variant | Mode | Expected parents | Recovered vars | Clean recovery | Jaccard | Precision | Recall | Outcome |
|---|---|---|---|---|---|---|---|---|---|
| `qi004_chain_x0parent_binary` | chain, x0=parent | binary | {x0} | {} | 0 | 0.00 | n/a | 0.00 | completed_no_solution |
| `qi004_chain_x0parent_cat3` | chain, x0=parent | cat3 | {x0} | {} | 0 | 0.00 | n/a | 0.00 | completed_no_solution |
| `qi004_chain_x0parent_cont3` | chain, x0=parent | cont3 | {x0} | {} | 0 | 0.00 | n/a | 0.00 | completed_no_solution |
| `qi004_chain_x1parent_binary` | chain, x1=parent | binary | {x1} | {x0, x1} | 0 | 0.50 | 0.50 | 1.00 | **solved** |
| `qi004_chain_x1parent_cat3` | chain, x1=parent | cat3 | {x1} | {} | 0 | 0.00 | n/a | 0.00 | completed_no_solution |
| `qi004_chain_x1parent_cont3` | chain, x1=parent | cont3 | {x1} | {} | 0 | 0.00 | n/a | 0.00 | completed_no_solution |
| `qi004_fork_x0parent_binary` | fork, x0=parent | binary | {x0} | {} | 0 | 0.00 | n/a | 0.00 | error (`unknown constant`) |
| `qi004_fork_x0parent_cat3` | fork, x0=parent | cat3 | {x0} | {} | 0 | 0.00 | n/a | 0.00 | completed_no_solution |
| `qi004_fork_x0parent_cont3` | fork, x0=parent | cont3 | {x0} | {} | 0 | 0.00 | n/a | 0.00 | completed_no_solution |
| `qi004_fork_x1parent_binary` | fork, x1=parent | binary | {x1} | {} | 0 | 0.00 | n/a | 0.00 | completed_no_solution |
| `qi004_fork_x1parent_cat3` | fork, x1=parent | cat3 | {x1} | {} | 0 | 0.00 | n/a | 0.00 | completed_no_solution |
| `qi004_fork_x1parent_cont3` | fork, x1=parent | cont3 | {x1} | {} | 0 | 0.00 | n/a | 0.00 | completed_no_solution |
| `qi004_collider_binary` | collider | binary | {x0, x1} | {} | 0 | 0.00 | n/a | 0.00 | error (`unknown constant`) |
| `qi004_collider_cat3` | collider | cat3 | {x0, x1} | {} | 0 | 0.00 | n/a | 0.00 | completed_no_solution |
| `qi004_collider_cont3` | collider | cont3 | {x0, x1} | {} | 0 | 0.00 | n/a | 0.00 | completed_no_solution |

The single solved cell's learned `x2` rules (quoted exactly):

```prolog
x2(A) :- alpha_1(A), x0(A).
x2(A) :- x1(A).
```

Its diagnostics: `parent_superset` (recovered {x0, x1} ⊃ true {x1}), `ancestor_only_rate=0.5`, `body_parent_recall=1.0`, 1 assumption, 1 contrary, 0 folding tokens.

**Continuous bin-health / occupancy.** All 5 `*_cont3` cells had all three uniform bins non-empty for both `x0` and `x1` (minimum bin counts: chain_x0parent 3, chain_x1parent 3, fork_x0parent 5, fork_x1parent 4, collider 4). The continuous predicate vocabulary was therefore non-degenerate; the absence of recovery is not attributable to empty bins.

**Coverage.** Across all 15 cells, Prolog-aware positive coverage `cov_pl_pos = 0.000` and negative exclusion `cov_pl_neg = 1.000`; accuracy ranged 0.40–0.75. Even the one solved cell has `cov_pl_pos = 0.000` (accuracy 0.55).

---

## 3. Motif-level interpretation

- **Chain variants (`x0parent`, `x1parent`).** Only one chain cell produced any rule: `chain_x1parent_binary` (solved), and it recovered the **superset** {x0, x1} rather than the true parent {x1} alone — it cites the true parent `x1` (recall 1.0) but also the ancestor/root `x0` (precision 0.5, `ancestor_only_rate=0.5`). The other five chain cells (both cat3, both cont3, and `chain_x0parent_binary`) returned `completed_no_solution`. So the chain motif yields at most a contaminated superset and otherwise no rule at `n=20`.
- **Fork variants (`x0parent`, `x1parent`).** No fork cell recovered anything: four returned `completed_no_solution` and `fork_x0parent_binary` errored on the binary encoding limitation. This contrasts with QL1/QL2, where fork (under canonical orientation, parent `x0`) recovered cleanly across modes.
- **Collider.** No recovery: `collider_binary` errored (`unknown constant`); `collider_cat3` and `collider_cont3` returned `completed_no_solution`.
- **Parent position vs x0 preference.** The intended confound check (does recovery track the true-parent column or favour `x0`?) **cannot be answered by QL4**, because only one cell solved and it is a `parent_superset` citing *both* columns. There is no cell where the pipeline recovered exactly `{x1}` or exactly `{x0}`, so "tracks the true parent" vs "favours x0" remains undetermined. The parent-position **fixtures** are correctly constructed (verified: the true parent sits in the asserted column for every cell), but the run did not yield enough solved cells to exercise the comparison.
- **Net.** At `n=20` with noise, the current pipeline almost always returns no `x2` rule; the only rule it did learn over-includes the ancestor.

---

## 4. Data-mode interpretation

- **Binary.** 5 cells: 1 solved (superset), 2 `completed_no_solution`, 2 `error` (the all-zero-positive `unknown constant` limitation, in `fork_x0parent_binary` and `collider_binary`). Binary is the only mode that produced any rule, consistent with QL1/QL2 where binary was the friendliest encoding — but here even binary does not produce a clean recovery.
- **Categorical-3.** 5 cells, all `completed_no_solution`; no rules, no recovery.
- **Continuous-binned (3 uniform bins).** 5 cells, all `completed_no_solution`; no rules. Crucially, **all continuous cells now complete** (no timeouts), which is the concrete improvement over QL3, where every cat3/cont3 cell timed out. So QL4 changes the continuous picture from "cannot be evaluated (timeout)" to "evaluated, and recovers nothing at `n=20`".
- **Binning / sample size.** Bin occupancy was healthy (Section 2), so the continuous non-recovery is not a binning-degeneracy artefact. The most visible remaining factor is sample size: at `n=20` with mild noise the learner overwhelmingly returns `completed_no_solution` rather than a parent rule. Whether this is driven by `n`, by noise, or by the learner/encoding interaction is not separable from QL4 alone.

---

## 5. Metric-level interpretation

- **Clean recovery.** 0/15 overall (0 in every mode). No cell's learned body equals the true parent set.
- **Jaccard / precision / recall.** Non-trivial only for the one solved cell: Jaccard 0.5, precision 0.5, recall 1.0 — the signature of a superset (all true parents present plus one spurious variable). All other cells are 0/NaN because no variables were recovered.
- **Coverage.** Uniformly `cov_pl_pos=0.000`, `cov_pl_neg=1.000`. The learned frameworks (where any exist) reject all negatives but accept none of the intended positives under Prolog-aware evaluation — coverage is behavioural and here indicates the rules do not fire on the positive examples as hoped, even in the solved cell.
- **Assumptions / contraries.** Only the solved cell introduced ABA Learning exception structure (1 assumption `alpha_1`, 1 contrary); all other cells introduced none. Folding tokens were 0 for the solved cell and 15 (the budget) for the `completed_no_solution` cells, and 0 for the instant errors.
- **Bin health / occupancy.** All continuous bins non-empty (Section 2); the encoding vocabulary was trustworthy.
- **Timeout / solve status.** 0 timeouts, 1 solved, 12 no-solution, 2 error.
- **What these metrics diagnose.** They measure whether **learned `x2` rule bodies align with the known direct parents of `x2`**, and whether the learner produced/covered rules at all. They do **not** measure causal discovery, edge orientation, or DAG recovery.

---

## 6. Consequence for the qualitative investigation

- **Does QL4 rescue the continuous analysis after QL3 timed out?** Partially. It removes the *feasibility* blocker — all continuous (and categorical) cells now complete within budget — so the continuous question is finally answerable. The answer at `n=20`, however, is that the pipeline recovers nothing in continuous mode (all `completed_no_solution`).
- **Does QL4 show the implementation can scale modestly?** Yes, in the narrow sense that `n=20` with a 300 s timeout completes 15/15 cells without timeouts (vs `n=100` timing out at 120 s). This is a feasibility result, not a recovery result.
- **Does QL4 show parent-position controls matter?** Not yet — the controls are correctly built, but only one cell solved, so the `*_x0parent` vs `*_x1parent` comparison could not be exercised. The confound remains empirically unbroken.
- **Does QL4 become the canonical scaled/noisy qualitative evidence?** Yes — QL4 is the canonical *scaled, noisy* run (it completes and is interpretable), superseding QL3 for that role. But its substantive recovery finding is essentially null (0/15 clean), so the canonical *recovery* evidence remains QL1 (encoding/motif sensitivity) and QL2 (best-case learnability, clean_recovery 0.5).
- **Does any QL3 evidence remain useful?** Only as an audit/feasibility note: QL3 documents the `n=100` computational wall and the binary encoding limitation that motivated QL4. It contributes no recovery evidence.

---

## 7. Limitations

- `n=20` is still **small**; results are exploratory and seed-specific (single grid seed; deterministic fixtures).
- This is **target-wise parent-set recovery**, not graph recovery, edge orientation, or causal discovery.
- Continuous variables are **binned (3 uniform bins) before ABA Learning**; recovery is over bin predicates, not raw continuous values.
- The run is **qualitative/exploratory**; outcomes are dominated by `completed_no_solution`, which limits how much can be inferred about *which* variables the pipeline prefers.
- Learned rules are **symbolic predictors**; a body matching the parents (or, here, over-including the ancestor) is alignment under favourable conditions, not evidence of learned causation.
- The **binary all-zero-positive encoding limitation** persists at `n=20` (2 cells errored with `unknown constant`); recorded, not fixed.
- **Computational feasibility remains a constraint**: the categorical/continuous cells that completed still required tens to ~270 s each at `n=20`; larger `n` is not currently tractable under this learner/timeout configuration.

---

## 8. Interim-report claims

### Claim candidates (supported)

| Claim candidate | Supported? | Evidence | Caveat |
|---|---|---|---|
| At `n=20` with a 300 s timeout, the target-wise ABA Learning pipeline completes all 15 scaled/noisy cells with no timeouts | Yes | 15/15 `metrics.json`; 0 timeouts; max wall-clock 272.8 s | A feasibility result only; says nothing about recovery |
| Reducing `n` from 100 to 20 (and raising the timeout) resolves the QL3 categorical/continuous timeout wall | Yes | QL3: all cat3/cont3 cells timed out; QL4: all cat3/cont3 cells complete | Recovery in those completed cells is null |
| At `n=20` with noise, the pipeline recovers no clean parent set for `x2` in any motif/mode | Yes | `clean_recovery=0` for all 15 cells | Bounded to this design, `n`, noise, learner config |
| The only learned `x2` rule set (chain_x1parent_binary) is a parent **superset** that also cites the ancestor `x0` | Yes | Recovered {x0,x1} vs parents {x1}; P/R/J 0.5/1.0/0.5; `ancestor_only_rate=0.5`; rules quoted in §2 | One cell; not generalisable |
| Continuous non-recovery at `n=20` is not caused by empty/degenerate bins | Yes | All 3 uniform bins non-empty for `x0`/`x1` in every `*_cont3` cell | Does not identify the actual cause |
| The binary all-zero-positive encoding limitation still occurs at `n=20` | Yes | 2 binary cells errored with `ERROR: unknown constant` (`fork_x0parent_binary`, `collider_binary`) | Known limitation; recorded, not fixed |
| QL4 is the canonical *scaled/noisy* qualitative run (supersedes QL3 for that role) | Yes | QL4 completes and is interpretable; QL3 is a feasibility attempt | Its recovery finding is null; canonical *recovery* evidence stays QL1/QL2 |

### Claims NOT supported

| Claim not supported | Reason |
|---|---|
| QL4 breaks the x0/first-column confound | Only 1 cell solved (a superset citing both columns); the `*_x0parent` vs `*_x1parent` comparison was not exercised |
| The pipeline recovers parents at scale under noise | 0/15 clean recovery at `n=20` |
| Continuous/categorical recovery improved over QL1 | QL4 continuous/categorical cells recover nothing (all `completed_no_solution`); QL1 at least produced rules (though imperfect) |
| QL4 demonstrates causal discovery / DAG recovery / edge orientation | Out of scope; target-wise parent-set recovery only; reserved graph metrics not computed |
| The single solved rule indicates the pipeline "found the cause" | It over-includes the ancestor `x0` and has 0.0 positive coverage; it is a contaminated predictor, not validated parent recovery |
| Results generalise beyond this seed/design | Single seed, deterministic fixtures, `n=20`, exploratory |
