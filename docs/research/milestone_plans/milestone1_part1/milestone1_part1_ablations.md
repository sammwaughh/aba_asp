# Milestone 1, Part 1 — Ablation plan (m1.1 closure)

**Short name:** m1.1 ablations  
**Parent plan:** `docs/research/milestone_plans/milestone1_part1/milestone1_part1_parent_position.md`  
**Experiment record:** `docs/experiments/qualitative/M1.1-parent-position.md` (Stage 4 mechanism; Stage 6 ablation results)  
**Findings output:** `docs/report/findings/milestone1_part1_m11_findings.tex` (§Ablations + updated closure)  
**Status:** executed — 2026-06-22 (ABL-100–107; ABL-106 skipped)  
**Purpose:** Close m1.1 by **targeted, falsification-first** tests of the Stage 4 mechanistic claims.  
**Out of scope:** Full M1.2 greedy grid (deferred comparator); Russo-style Causal ABA; new DGPs beyond controlled interventions on m1.1 cat3 cells.

---

## 0. Why ablations now

Stage 4 (cat3 A vs B) gives a **mechanistic story**:

1. **H1 (order):** BK rule-ID order in the `fwt` table (`=/2` key) determines the first successful `select_rule` match for a rote equality literal.
2. **H2 (semantics):** That fold passes or fails **cautious entailment** depending on whether the chosen feature predicate is an exact E+/E− separator (parent) or also covers negatives (isolated predictor).
3. **H3 (commitment):** Failed entailment on the **first target fold** commits to **new assumption** (`relto` with no prior assumption) rather than backtracking `select_rule` to the next BK candidate; the rote equality is consumed and cannot later yield the parent singleton.

The eight-cell grid **correlates** σ (BK block order) with outcome. Ablations must **intervene** on one link at a time and report results that could **disprove** the story. Elegant CS practice: run the cheapest test that could falsify the strongest claim first.

---

## 1. Hypothesis register (falsifiable sub-claims)


| ID        | Claim                                                                                                                                                    | If false, we learn…                                                                          |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **H1**    | For cat3, first `select_rule` success for `[A=k]` is the lowest rule ID whose body subsumes `A=k` among all BK rules (order = `read_bk` / file order).   | Mechanism is not `fwt` ID order; look elsewhere (fold selection, different key, engine bug). |
| **H2**    | A’s first fold fails entailment because `x0_val_`* groups include negative row ids; B’s passes because `x1_val_2` matches E+ only.                       | Fork is not separator semantics; entailment or example encoding is wrong.                    |
| **H3**    | After failed target entailment on A, the run cannot reach `x2(A):-x1_val_2(A)` without changing inputs (order, engine options, or restart).              | Assumption path is not the lock-in; nd backtrack or later folds can recover parent rule.     |
| **Hπ**    | C vs D mirrors A vs B under parent swap (`x0` parent): parent-first BK → singleton; non-parent-first → assumptions.                                      | Story is x1-specific or σ-pair specific, not role-agnostic.                                  |
| **Hσ↔BK** | σ’s effect on cat3 is **fully explained** by BK serialisation order, not by an independent “column order” channel (given identical E+/E− and rule text). | Table column order or bridge has a separate effect beyond BK read order.                     |
| **Hbin**  | Binary σ passes because first-fold / separator structure differs from cat3 `val_`* granularity (moderator), not because H1–H3 fail on binary.            | Same mechanism should break binary σ; encoding interaction needs revision.                   |


Claims **M11-C-003** and **M11-C-006** in `docs/report/claims_ledger.md` map to H1–H3. Ablations upgrade or weaken them.

---

## 2. Execution principles

1. **Disprove first:** Order tests by “if this fails, we must rewrite Stage 4” before confirmatory checks.
2. **One lever per run:** Change only what the ablation targets (BK order, one rule prefix, one engine flag). Hold `data.csv`, E+/E−, `folding_mode: nd`, `folding_steps: 15`, timeouts, and seed fixed unless the ablation is explicitly about engine options.
3. **Same observables as Stage 4:** `prolog.stdout` line ~35 (first fold), `gen2` entailment line, `bk.sol.aba` target rule(s), ABA rule count, trace length.
4. **No inherited engine edits:** Intervene on **inputs** (BK file, optional lopt in generated wrapper) only — not `gen.pl` / `folding.pl` / `aba_asp.pl`.
5. **Record before run:** Each ablation gets a row in this plan + a short note in `M1.1-parent-position.md` Stage 6 before execution (research-logging rule).
6. **Artefact root:** `causal/outputs/aba_learning/grid/M11_ablations/<abl_id>/` (separate from the canonical eight-cell grid).

---

## 3. Recommended order (falsification-first)

```text
Tier 0  Audit only     →  Hπ, cheap; no new runs for C/D if traces suffice
Tier 1  Intervene BK   →  Hσ↔BK, H1, H2  (strongest causal test — do first among runs)
Tier 2  Minimal ID     →  H1 refined (single-rule prefix, not full block swap)
Tier 3  Symmetry       →  confirm Hπ on reverse flip
Tier 4  Engine falsify →  H3
Tier 5  Moderator      →  Hbin
Tier 6  Synthesis      →  findings.tex + m1.1 closure decision
```

**Rationale:** **ABL-101 (BK flip on cat3 A)** is the highest-value *run*. If parent-first BK on A’s data still yields assumptions, Stage 4 is wrong or incomplete — stop and re-audit before further ablations. **ABL-100 (C vs D audit)** costs minutes and can falsify **Hπ** before any code. **ABL-102 (minimal rule prefix)** separates “block order” from “lowest matching ID wins” if Tier 1 passes.

---

## 4. Ablation catalogue

### ABL-100 — cat3 C vs D trace audit (Tier 0)


| Field              | Detail                                                                                                                                                               |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**           | Confirmatory audit (existing artefacts)                                                                                                                              |
| **Tests**          | **Hπ**                                                                                                                                                               |
| **Falsifier**      | D’s first fold does **not** use non-parent feature at lowest ID, or C does **not** use parent feature — mechanism not role-agnostic.                                 |
| **Inputs**         | `cells/m11_cat3_C/`, `cells/m11_cat3_D/` under `M11_parent_position`                                                                                                 |
| **Procedure**      | Line-by-line mirror of Stage 4: compare traces from line 27 through first `gen2`; map to `select_rule` / entailment; write up in `M1.1-parent-position.md` §Stage 6. |
| **Expected**       | C: `x0_val_2` at ID 3, entailment pass, short trace. D: `x1_val_0` (or other non-parent) at ID 3, entailment fail, long trace.                                       |
| **Implementation** | Read-only; no runner.                                                                                                                                                |
| **Pass criterion** | Pattern matches A/B with parent/non-parent roles swapped.                                                                                                            |
| **If fail**        | Do not trust π-generalisation; investigate D/C-specific data or BK before Tier 1.                                                                                    |


---

### ABL-101 — BK block-order flip on cat3 A (Tier 1) ★ primary causal test


| Field                      | Detail                                                                                                                                                                                         |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**                   | Intervention                                                                                                                                                                                   |
| **Tests**                  | **Hσ↔BK**, **H1**, **H2**                                                                                                                                                                      |
| **Falsifier**              | Parent-first BK on **A’s** `data.csv` and E+/E− still produces assumption structure and/or `x0_val_`* first fold.                                                                              |
| **Baseline**               | cat3 A: `[x0,x1]` table; BK `x0_val_`* then `x1_val_*`; discrepant output.                                                                                                                     |
| **Intervention**           | Replace `bk.aba` with **block order** from cat3 B (`x1_val_`* block then `x0_val_*`), **unchanged rule text** (same 18 rules, permuted lines only).                                            |
| **Hold constant**          | `data.csv` from A; pos `x2(3),x2(6),x2(9)`; neg six others; nd + cautious + relto; same timeouts.                                                                                              |
| **Expected**               | Line 35: `x1_val_2`; line 38: entails E+/E−; `bk.sol.aba`: `x2(A):-x1_val_2(A).`; trace ~54 lines; 19 rules.                                                                                   |
| **Implementation options** | (a) Manual ablation dir: copy A’s `data.csv`, write flipped `bk.aba`, run Stage 3 via thin script; (b) fixture flag `bk_block_order: parent_first` in ablation helper (preferred if repeated). |
| **Pass criterion**         | Exact expected singleton; first fold = parent feature; σ-style failure **reversed** without σ on table.                                                                                        |
| **If pass**                | Strong evidence σ effect is **BK read order**, not a separate column-order channel.                                                                                                            |
| **If fail**                | Revise Stage 4; inspect whether bridge regenerates BK, wrong examples, or `select_rule` uses non-`fwt` logic.                                                                                  |


**Command sketch (after ablation runner exists):**

```bash
python -m causal.scripts.m11_ablation_run \
  --abl ABL-101 \
  --baseline m11_cat3_A \
  --bk-source m11_cat3_B \
  --bk-mode block_order_only
```

(Exact CLI to be implemented when executing plan; manual copy is acceptable for first run.)

---

### ABL-102 — Minimal BK prefix: single parent rule before x0 block (Tier 2)


| Field                            | Detail                                                                                                                                                                                                                                                                       |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**                         | Intervention (minimal)                                                                                                                                                                                                                                                       |
| **Tests**                        | **H1** refined — “lowest ID wins”, not merely “parent block first”                                                                                                                                                                                                           |
| **Falsifier**                    | Singleton recovered when only `**x1_val_2(A):-A=3.`** is inserted as rule ID 1, but **not** when full block swap (ABL-101) — would contradict clean H1 story (unlikely). More realistically: **prefix suffices** but full block swap fails → investigate partial file write. |
| **Baseline**                     | cat3 A table + default x0-first BK.                                                                                                                                                                                                                                          |
| **Intervention**                 | One file: default A `bk.aba` **plus** a single extra line at top: `x1_val_2(A) :- A=3.` (duplicate head/body pattern allowed if engine treats as separate ID 1; verify ID assignment). Alternatively: prepend only the three `x1_val_2` rules for rows 3,6,9.                |
| **Hold constant**                | A data and E+/E−.                                                                                                                                                                                                                                                            |
| **Expected**                     | First fold on `[A=3]` uses prepended `x1_val_2` rule (ID 1); entailment pass; singleton.                                                                                                                                                                                     |
| **Pass criterion**               | Parent singleton without reversing entire x1 block — proves **ID order** is the lever, not a vague “x1 first” narrative.                                                                                                                                                     |
| **If fail while ABL-101 passes** | Check duplicate-rule / `select_rule` behaviour when multiple rules subsume same literal.                                                                                                                                                                                     |


---

### ABL-103 — Reverse BK flip on cat3 C (Tier 3)


| Field                                | Detail                                                                                            |
| ------------------------------------ | ------------------------------------------------------------------------------------------------- |
| **Type**                             | Intervention (symmetry)                                                                           |
| **Tests**                            | **Hπ**, **Hσ↔BK**                                                                                 |
| **Falsifier**                        | Non-parent-first BK on C (parent `x0`) does **not** produce assumption structure.                 |
| **Baseline**                         | cat3 C: x0-first BK, singleton `x2(A):-x0_val_2(A).`                                              |
| **Intervention**                     | BK block order from D (`x1_val_`* then `x0_val_*`) with C’s `data.csv` and E+/E−.                 |
| **Expected**                         | First fold: non-parent `x1_val_`*; entailment fail; assumption patchwork citing `x1`; long trace. |
| **Pass criterion**                   | σ failure **induced** on the “good” cell by BK order alone.                                       |
| **If ABL-101 pass and ABL-103 fail** | Asymmetry between x1-parent and x0-parent cells — investigate cat3 row/id alignment for C.        |


---

### ABL-104 — Entailment micro-check (Tier 2, optional but cheap)


| Field              | Detail                                                                                                                                                           |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**           | Semantic verification                                                                                                                                            |
| **Tests**          | **H2**                                                                                                                                                           |
| **Falsifier**      | Cautious entailment accepts `x2:-x0_val_0` on A’s E+/E− or rejects `x2:-x1_val_2`.                                                                               |
| **Procedure**      | Construct minimal frameworks: BK from A + single learnt rule; run entailment check (or one-step Prolog call / inspect `asp.clingo` + `cc.pl` from a staged run). |
| **Expected**       | `x0_val_0` fold: negatives in consequences; `x1_val_2` fold: E+ only.                                                                                            |
| **Implementation** | Can piggyback on ABL-101 failure analysis or standalone script calling engine `entails/6` path.                                                                  |
| **Pass criterion** | Separator table from Stage 4 matches clingo outcome.                                                                                                             |


---

### ABL-105 — Engine option: `folding_mode(all)` on cat3 A (Tier 4)


| Field                      | Detail                                                                                                              |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Type**                   | Falsifier for **H3**                                                                                                |
| **Falsifier**              | With **unchanged** A BK, `folding_mode(all)` (or increased folding tokens) yields parent singleton without BK flip. |
| **Baseline**               | cat3 A, default BK.                                                                                                 |
| **Intervention**           | Only `folding_mode: all` (or `lazy` if supported) in Prolog wrapper; keep BK and data.                              |
| **Expected (if H3 holds)** | Still assumptions — first successful single-token fold still `x0_val_0`; commitment story unchanged.                |
| **If singleton**           | H3 weakened: alternate folds or multi-token folding reach parent rule before commitment; document trace path.       |
| **Note**                   | This is **not** M1.2 greedy grid; single-cell, single-option change.                                                |


---

### ABL-106 — Engine option: `asm_intro(sechk)` on cat3 A (Tier 4, optional)


| Field            | Detail                                                                                         |
| ---------------- | ---------------------------------------------------------------------------------------------- |
| **Type**         | Falsifier for assumption **branch** details                                                    |
| **Falsifier**    | Different assumption introduction changes first-fold literal or recovers singleton on same BK. |
| **Intervention** | `set_lopt(asm_intro(sechk))` in wrapper only.                                                  |
| **Expected**     | Likely still non-parent first fold; may change assumption timing — unlikely to fix σ alone.    |
| **Run if**       | ABL-105 inconclusive or supervisor asks about relto vs sechk.                                  |


---

### ABL-107 — Binary cat3 A first-fold audit (Tier 5)


| Field              | Detail                                                                                                                                                                                       |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**           | Moderator audit                                                                                                                                                                              |
| **Tests**          | **Hbin**                                                                                                                                                                                     |
| **Falsifier**      | Binary A trace shows same non-parent-first fold + failed entailment as cat3 A, yet σ still passes — binary σ success would contradict “same mechanism”.                                      |
| **Inputs**         | `m11_binary_A/prolog.stdout` vs `m11_binary_B`                                                                                                                                               |
| **Procedure**      | Record first fold literal on first rote positive; check whether x0-first BK tries isolated predictor and whether entailment would fail in isolation.                                         |
| **Expected**       | Binary A: first fold still picks parent or entailment succeeds despite x0-first order — explain via bare `x0`/`x1` predicates vs `val_`* granularity (documented moderator, not H1 failure). |
| **Implementation** | Read-only.                                                                                                                                                                                   |


---

## 5. Decision tree (after Tier 1)

```text
ABL-100 (C vs D audit)
    │
    ├─ pattern ≠ A/B mirror → stop; fix Stage 4 / data docs
    └─ pattern OK
           │
           ABL-101 (BK flip on A)
           │
           ├─ FAIL (still assumptions) → ABL-104 entailment check; re-read select_rule;
           │                            do NOT run M1.2; revise mechanism
           │
           └─ PASS (singleton)
                  │
                  ├─ ABL-102 (minimal prefix) → confirms ID-order lever
                  ├─ ABL-103 (reverse flip on C) → symmetry
                  ├─ ABL-105 (folding all) → H3
                  └─ ABL-107 (binary audit) → Hbin moderator paragraph
```

---

## 6. Implementation plan (minimal code)

**Preferred:** small ablation runner (does not modify eight-cell grid config).


| Component                               | Purpose                                                                                                                                                              |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `causal/scripts/m11_ablation_run.py`    | Copy baseline `data.csv`; build or copy `bk.aba` per ablation spec; call `ABASPRunner.run_prolog_aba_asp`; write `prolog.stdout`, `bk.sol.aba`, `abl_manifest.json`. |
| `causal/experiments/m11_ablations.yaml` | Declarative list of ABL-101…105 parameters (baseline dgp, bk_mode, lopt overrides).                                                                                  |
| `causal/tests/test_m11_ablation_bk.py`  | Prolog-free: flipped BK has same rule multiset; block order matches spec.                                                                                            |


**Manual fallback (acceptable for ABL-101 once):**

1. Create `M11_ablations/ABL-101_cat3_A_parent_first_bk/`.
2. Copy `m11_cat3_A/data.csv`.
3. Write `bk.aba` = cat3 B block order (verify 18 rules, same text as A multiset).
4. Run Prolog with same pos/neg as A fixture (`x2(3),x2(6),x2(9)` + negs).
5. Save stdout and sol files.

**Do not** change `handcrafted_m11.py` σ/π definitions for ablations — interventions are **post-hoc on BK** unless ABL-102 needs a documented duplicate-rule edge case.

---

## 7. Observables and recording template

For each ablation, record in `M1.1-parent-position.md` §Stage 6:


| Field                       | Value                            |
| --------------------------- | -------------------------------- |
| Ablation ID                 | ABL-10x                          |
| Date / commit               |                                  |
| Baseline cell               |                                  |
| Intervention                | one sentence                     |
| Command                     | exact                            |
| First fold (trace)          | predicate at line ~35            |
| gen2 entailment             | pass / fail                      |
| `bk.sol.aba` target rule(s) | normalised                       |
| Rule count                  |                                  |
| Trace lines                 |                                  |
| Verdict vs prediction       | pass / fail / partial            |
| Claim impact                | M11-C-003, M11-C-006, new claim? |


---

## 8. Closure criteria for m1.1

m1.1 moved to **`analysed`** when **all** of (June 2026 — **all met**):

1. **ABL-100** written up (C vs D). — **met** (audit_pass)
2. **ABL-101** executed — **pass** (singleton on cat3 A config). — **met**
3. **ABL-103** executed (symmetry). — **met** (pass)
4. At least one of **ABL-102** or **ABL-104** supports H1/H2. — **met** (both pass)
5. **ABL-105** (H3 addressed). — **met** (pass; assumption triple on unchanged A BK)
6. **ABL-107** binary moderator in findings. — **met** (audit_pass)
7. `milestone1_part1_m11_findings.tex` updated. — **met** (integrated conclusion)
8. `claims_ledger.md` — M11-C-003/006 updated; M11-C-007 added. — **met**
9. `experiments_summary.md` + `experiment_register.md` synced. — **met**

**M1.2:** unblocked; m1.1 Stage 7 greedy comparator complete (June 2026). m1.1 **closed**.
*(July 2026: M1.2 has since been re-scoped from a greedy grid to the published-configuration
comparison — see `../milestone1_part2/milestone1_part2_config_comparison.md`.)*

---

## 9. Findings document outline (post-ablation)

Add to `milestone1_part1_m11_findings.tex`:

1. **§Ablations** — table: ID, intervention, prediction, outcome.
2. **§Revised mechanism** — one paragraph integrating ABL-101/103 if pass (causal BK-order claim).
3. **§Encoding moderator** — binary vs cat3 (ABL-107).
4. **§Closure** — bounded answers to m1.1 research question:
  - Parent-role tracking: binary yes; cat3 yes **when parent feature wins first fold**.
  - σ-invariance: fails on cat3 under default pipeline; **explained by** BK serialisation order under fixed nd+relto (if ablations pass).
5. **§Limitations** — ablations test input order, not engine fix; no causal discovery claim.

---

## 10. Claims to update (preview)


| Claim                     | Expected after successful Tier 1–3                                                                                                                                 |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| M11-C-003                 | Upgrade from bounded to **ablation-supported**: BK ID order causes first fold.                                                                                     |
| M11-C-006                 | **Confirmed** or refined if ABL-105 finds recovery path.                                                                                                           |
| New M11-C-007 (candidate) | Cat3 σ-invariance failure is **fully accounted for** by BK read order + entailment + assumption commitment on default nd config (conditional on ABL-101/103 pass). |


Do not add M11-C-007 until ablation evidence exists.

---

## 11. Schedule (suggested)


| Step                     | Effort  | Blocker                 |
| ------------------------ | ------- | ----------------------- |
| ABL-100 write-up         | ~1 h    | None                    |
| ABL-101 manual or script | ~2 h    | Optional runner script  |
| Decision point           | —       | Required before Tier 2+ |
| ABL-102, 103             | ~2 h    | ABL-101 pass            |
| ABL-104                  | ~1 h    | Optional                |
| ABL-105, 106             | ~1 h    | After Tier 1            |
| ABL-107                  | ~30 min | Anytime                 |
| Findings + registers     | ~2 h    | All required ablations  |


---

## 12. References

- Stage 4 mechanism: `docs/experiments/qualitative/M1.1-parent-position.md`
- Engine: `asp_utils.pl` (`read_bk`, `update_fwt`); `folding.pl` (`select_rule`); `gen.pl` (`gen2`, `nonintensional/1`)
- Canonical grid artefacts: `causal/outputs/aba_learning/grid/M11_parent_position/cells/`
- Supervisor guidance: qualitative inspection before ablations — **satisfied** by Stage 4; ablations now authorised by this plan.

---

## 13. Samuel review checklist (before executing)

- [x] Order agrees: falsify Hσ↔BK/H1 first among runs (ABL-101 after ABL-100).
- [x] Tier 1 failure stops the line — no M1.2 distraction.
- [x] Each ablation changes one lever.
- [x] Artefact path `M11_ablations/` agreed.
- [x] Manual vs script fallback acceptable for first ABL-101.
- [x] Closure criteria in §8 are sufficient for m1.1 sign-off.
- [x] Findings §outline matches report workflow (facts only; no polished prose).

---

## 14. Post-execution summary (22 June 2026)

**Command:** `python -m causal.scripts.m11_ablation_run --all-required` (commit `93d51bf`).

**Artefacts:** `causal/outputs/aba_learning/grid/M11_ablations/`; summary `summary/abl_results.md`.

| ABL | Verdict | Key outcome |
|-----|---------|-------------|
| 100 | audit_pass | C singleton / D assumptions (π mirror of A/B) |
| 101 | pass | BK flip on cat3 A → singleton `x2:-x1_val_2` |
| 102 | pass | Prepend parent rule at ID 1 → same singleton |
| 103 | pass | BK flip on C → D-like assumptions |
| 104 | audit_pass | Grid A fail / B pass entailment |
| 105 | pass | `folding_mode(all)` still assumptions (H3) |
| 106 | skipped | ABL-105 conclusive |
| 107 | audit_pass | Binary σ-invariant |

**Closure:** m1.1 status **`analysed`**. Integrated conclusion:
`docs/report/findings/milestone1_part1_m11_findings.tex` §Integrated conclusion.