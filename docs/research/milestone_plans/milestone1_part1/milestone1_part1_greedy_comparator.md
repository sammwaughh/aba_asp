# Milestone 1, Part 1 — Greedy comparator (Stage 7)

**Experiment ID:** M11-G (addendum to M11 / m1.1)  
**Parent plan:** [milestone1_part1_parent_position.md](milestone1_part1_parent_position.md)  
**Status:** `analysed` — executed 2026-06-22; see M1.1 record §Stage 7 and `M11_parent_position_greedy/summary/compare_nd_greedy.md`.  
**Claim under test:** M11-C-004 (greedy vs cat3 representation-order sensitivity)

---

## 1. Purpose and position in Milestone 1

Milestone 1 Part 1 (m1.1) is **`analysed`** for non-deterministic folding (`folding_mode: nd`). Stages 0–6 established that cat3 σ-invariance fails under nd because BK block serialisation order fixes the first `select_rule` match on the first target fold, cautious entailment either passes or fails, and a failed test commits the run to assumptions without backtracking to the parent separator. That account is ablation-supported (ABL-100–107).

Stage 7 asks a **narrow, separate question**: on the **same** eight target-mechanism cells, with **identical** data and examples, does switching only `folding_mode` to **greedy** change learnt rules or metamorphic verdicts?

This is an **m1.1 addendum**, not Milestone 1 Part 2 (M1.2). Part 2 will compare greedy and nd more broadly (QI fixtures, runtime, strategy default). Stage 7 provides the **control-grid anchor** for Part 2 without reopening the nd mechanism closure.

Supervisor guidance (June 2026): nd vs greedy is **not sufficient** to explain cat3 σ failure. An informal greedy smoke test on m1.1 returned an outcome **materially different from both** nd cat3 A (assumption triple) and nd cat3 B (parent singleton). That smoke test is **not formally recorded** and must not be cited until reproduced under the standard grid pipeline.

---

## 2. Research questions

Answer in order (efficient decision tree):

| # | Question | Information sought |
|---|----------|-------------------|
| Q1 | **Sanity (binary):** Does greedy match nd on all four binary cells (exact singleton; σ and π hold)? | Comparator pipeline works; encoding moderator (ABL-107) is strategy-stable. |
| Q2 | **σ repair (cat3 A/D):** Does greedy recover the pre-specified parent singleton on cat3 A and D **without** BK reorder? | Direct test of M11-C-004 (“greedy fixes σ”). |
| Q3 | **σ invariance (cat3):** Does the full cat3 transformation square pass under greedy? | Whether representation-order sensitivity is folding-strategy-specific. |
| Q4 | **Mechanism (conditional):** If greedy cat3 A differs from **both** nd A and nd B, what is the third outcome class? | Whether `fold_greedy/2` follows the nd entailment-commitment story or needs a new failure class. |

**Secondary observables (always record):** `status`, exact vs discrepant classification, wall time per cell, total grid time vs nd, trace length, assumption count where applicable.

---

## 3. Scope boundary

### In scope

| Dimension | Value |
|-----------|--------|
| Fixtures | Eight m1.1 cells: binary/cat3 × A/B/C/D (`causal/experiments/handcrafted_m11.py`) |
| Data / examples | Same `data.csv`, E+/E−, seed 0, target `x2` as nd grid |
| **Single change** | `defaults.folding_mode: nd` → `greedy` |
| Other defaults | Match `M11_parent_position.yaml`: `folding_steps: 15`, `prolog_timeout_s: 120`, cautious + relto (engine defaults) |
| Comparisons | Per-cell outcome; σ/π square; runtime; conditional trace on cat3 A if outcome is novel |
| Claims | Primarily M11-C-004; M11-C-007 only if mechanism clearly shared |

### Out of scope

- Greedy ablations (no BK reorder under greedy unless post-run trace is genuinely ambiguous)
- QI-001/002/004 reruns (Part 2)
- Noise, continuous DGP, new motifs (Parts 3–4)
- Russo-style Causal ABA claims
- Treating greedy as the **primary explanation** of nd cat3 σ failure

---

## 4. Experimental design

### Paired comparison

| Arm | Config | Artefact root |
|-----|--------|---------------|
| Reference (done) | `M11_parent_position.yaml` (`folding_mode: nd`) | `causal/outputs/aba_learning/grid/M11_parent_position/cells/` |
| Comparator | `M11_parent_position_greedy.yaml` (`folding_mode: greedy`) | `causal/outputs/aba_learning/grid/M11_parent_position_greedy/cells/` |

Both arms use the same DGP sources, grid (`seed: [0]`, `target: [x2]`, `cell_dir: dgp`), and engine options except folding mode.

### Success criteria (reuse m1.1 definitions)

- **Exact:** returned solution matches pre-specified one-literal parent singleton (modulo normalisation).
- **Discrepant but solved:** Prolog `solved` but not the expected singleton (e.g. assumption triple citing non-parent).
- **σ-invariance holds** on pair (A↔B, D↔C) when normalised target rules agree.
- **π-equivariance holds** on pair when rules transform as under π.

Expected singletons (unchanged from Part 1):

| Encoding | Parent | Expected rule |
|----------|--------|---------------|
| binary, parent x1 | x1 | `x2(A)<-x1(A)` |
| binary, parent x0 | x0 | `x2(A)<-x0(A)` |
| cat3, parent x1 | x1 | `x2(A)<-x1_val_2(A)` |
| cat3, parent x0 | x0 | `x2(A)<-x0_val_2(A)` |

---

## 5. Pre-registered hypotheses

We do **not** assume greedy trivially fixes cat3 σ (ABL-105 falsified `folding_mode(all)` without BK reorder).

| ID | Hypothesis | Predicted greedy outcome on cat3 A | Effect on M11-C-004 |
|----|------------|-----------------------------------|---------------------|
| H-G-nd | BK-order / search path under greedy still favours non-parent first | Assumption triple (like nd A) | Reject “greedy fixes σ” |
| H-G-fix | Greedy avoids nd first-fold commitment | Parent singleton (like nd B) | Support M11-C-004 |
| H-G-third | Distinct greedy path (informal smoke-test hint; QI-002 `chain_cat3` superset precedent) | Parent **superset** or mixed structure | Weaken “greedy fixes σ” and “same mechanism as nd”; trace follow-up |
| H-G-fail | Strategy regression | no-solution / timeout | Record; contrast with QI collider gains |

**Moderate-confidence expectations before run:**

- Binary A–D: match nd (4/4 exact; σ/π hold).
- Cat3 B, C: match nd (exact singleton).
- Cat3 A, D: **uncertain** (H-G-nd / H-G-fix / H-G-third live).
- Runtime: greedy ≤ nd per cell (likely much faster; QI precedent).

---

## 6. Implementation

### Config

File: `causal/configs/experiments/M11_parent_position_greedy.yaml`  
`experiment_id: M11_parent_position_greedy`  
Copy of `M11_parent_position.yaml` with `folding_mode: greedy` only.

### Prolog-free test

Extend `causal/tests/test_greedy_configs.py`:

```python
("M11_parent_position", "M11_parent_position_greedy", 8),
```

### Run command

```bash
conda activate aba-asp
cd "/Users/samuelwaugh/Desktop/Causal ABA Learning/aba_asp"
python -m causal.experiments.run_grid \
  --config causal/configs/experiments/M11_parent_position_greedy.yaml \
  --no-resume
```

Record: git commit hash, SWI-Prolog/clingo versions, `done:` summary line.

### Comparison workflow

1. Classify each greedy cell against expected singleton (same rules as M1.1 Stage 2).
2. Build paired table: nd class vs greedy class; evaluate σ/π edges for greedy arm.
3. Pull wall times from `metrics.json` or grid summary.

Optional later: `causal/scripts/m11_compare_nd_greedy.py` → `M11_parent_position_greedy/summary/compare_nd_greedy.md` (defer unless manual pass is error-prone).

---

## 7. Analysis protocol

### Post-run decision tree

```
Run 8-cell greedy grid
  → Binary matches nd?  If no → trace + investigate pipeline
  → Cat3 A outcome?
       singleton     → evaluate full cat3 σ square
       assumption    → H-G-nd likely; evaluate σ square
       other         → trace cat3 A greedy vs nd A/B (Q4)
  → Close Stage 7; update M11-C-004
  → Feed results into Part 2 planning doc
```

### Conditional trace follow-up

**Trigger:** greedy cat3 A outcome ∉ {nd A outcome, nd B outcome, expected singleton}.

**Action:** Compare `prolog.stdout` for greedy cat3 A vs nd cat3 A and nd cat3 B. Note greedy uses `begin greedy folding` and `fold_greedy/2` in `folding.pl` (position-ordered walk over rote literals + `fwt` ID lists), not nd’s `fold_nd_wtc` + `select_rule` on the first target fold alone.

**Do not** run greedy ablations in the first pass.

---

## 8. Expected outputs and claim mapping

| Outcome pattern | M11-C-004 | M11-C-007 | Report action |
|-----------------|-----------|-----------|---------------|
| Greedy matches nd on all 8 cells | Reject “greedy fixes σ”; strategy-independent on this grid | Unchanged | Short addendum: greedy does not change m1.1 verdicts |
| Greedy fixes cat3 A/D singleton; σ passes | **Active** (bounded) | Possible refinement | Fill findings §Greedy; note mechanism |
| Greedy third outcome on cat3 A | **Weakened** | May need extension | Trace account; new failure class if warranted |
| Binary greedy ≠ nd | Pipeline bug or unexpected | Revisit | Trace before any claim |

---

## 9. Report integration checklist

After execution, update in order:

- [x] `docs/experiments/qualitative/M1.1-parent-position.md` — Stage 7 section
- [x] `docs/report/findings/milestone1_part1_m11_findings.tex` — §Greedy table and interpretation
- [x] `docs/report/claims_ledger.md` — M11-C-004 resolution
- [x] `docs/experiments/experiments_summary.md`, `docs/research/experiment_register.md`, `docs/report/report_state.md`
- [x] `docs/research/milestone_plans/milestone1-plan.md` — Part 1 Stage 7 note

---

## 10. Explicit non-claims

- Greedy fixes cat3 σ on m1.1 (until Q2–Q3 support it).
- Greedy explains nd cat3 σ failure (nd mechanism remains primary in Part 1).
- Greedy should be the Milestone 1 default strategy (Part 2 decision).
- Causal discovery or Russo-style Causal ABA results.

---

## 11. Execution checklist

| Step | Gate | Status |
|------|------|--------|
| 1. Config + test | `pytest causal/tests/test_greedy_configs.py -k M11` passes | done |
| 2. Run grid | 8/8 cells complete; artefacts under `M11_parent_position_greedy/` | done (2026-06-22) |
| 3. Paired compare | Table in `summary/compare_nd_greedy.md` | done |
| 4. Conditional trace | cat3 A novel outcome → trace note in M1.1 record §Stage 7 | done |
| 5. Documentation | Stage 7 + findings + claims ledger | done |
| 6. Part 2 input | m1.1 anchor summarised in Part 2 README | done |

---

## Relationship to M1.2 (Part 2)

| Stage 7 (this plan) | Full M1.2 |
|---------------------|-----------|
| Same 8 cells, one lever | QI grids + broader motifs |
| Closes M11-C-004 on control grid | Strategy default (C-006 scope) |
| May show greedy ≠ nd on cat3 A | When greedy helps/hurts across tasks |

Stage 7 **feeds** Part 2; it does **not** substitute for it.
