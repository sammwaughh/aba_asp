# ABA Learn + Causal Integration — Learning Plan

Personal study path for the `causal/` branch. Run everything from `aba_asp/causal/` with `conda activate aba-env`.

**Out of scope (unless needed later):** folding-mode sweeps (`TestFoldingModes`), BK-order tests (`TestBKOrderingSensitivity`), greedy folding classes, full `python test_aba_learning.py` suite. Causal ABA bridge / Experiment 1 comes **after** Phase 4.

---

## Phase 0 — Environment ✓

- Python 3.10 env, SWI-Prolog, Clingo, sibling repo `ArgCausalDisco`
- Smoke: `from argcausaldisco_integration import …` → `integration OK`; `test_simple_4_samples` passes

---

## Phase 1 — Handcrafted (traces + artifacts)

Understand BK vs E+/E− vs delta vs solution file; read Prolog trace when useful; use Python diagnostics (Coverage, Dependencies, Corr vs GT).

| Step | Test | Command |
|------|------|---------|
| **1a** ✓ | `TestSimpleHandcraftedLearning.test_simple_4_samples` | Perfect `x2 := x0`; one rule `x2(A) :- x0(A).` |
| **1b** | `TestAssumptionIntroduction.test_exception_triggers_assumption_intro` | Mostly `x2` follows `x0`; sample 3 counterexample → assumptions/contraries |

**Exit:** Explain BK, delta, and when ABA needs assumptions vs a single folded rule.

---

## Phase 2 — Discrete simulated (until routine)

Same pipeline; data from `simulate_discrete_data` + fixed DAG + seed.

| Order | Test | DAG |
|-------|------|-----|
| 1 | `TestMinimalDiscreteData.test_01_discrete_chain_6_samples` | X0→X1→X2 |
| 2 | `test_02_confounder_x0_to_x1_x2_all_targets` | X0→X1, X0→X2 |
| 3 | `test_03_collider_x0_x1_to_x2_all_targets` | X0→X2, X1→X2 |

**Per-run checklist:** RUN/DGP/DAG → `.csv` + `.bk.aba` → `aba_asp(E+,E−)` → delta + Coverage + Dependencies + Corr vs GT → “would true parents appear in the body?”

**Exit:** Predict plausible dependencies without re-reading the full Prolog trace; understand empty delta / weak `parent=` on small n.

---

## Phase 3 — Continuous simulated

| Order | Test | DAG |
|-------|------|-----|
| 1 | `TestMinimalContinuousData.test_continuous_8_samples` | X0→X1→X2 (n=8) |
| 2 | `test_continuous_confounder_x0_to_x1_x2_all_targets` | X0→X1, X0→X2 (n=6) |
| 3 | `test_continuous_collider_x0_x1_to_x2_all_targets` | X0→X2, X1→X2 (n=8) |

BK: **quantile bins** (`continuous_bins=2`); E+/E−: **median split** on the target column.

**Exit:** Read continuous BK (bins) and map back to high/low on a column; compare confounder/collider logs to discrete Phase 2.

---

## Phase 4 — Your own experiments

**Goal:** Fill gaps repo tests don’t cover; record predictions before runs.

### Notebook / log

Use `experiments/aba_learn_lab.ipynb` (or a markdown log). One row per experiment:

| Column | Content |
|--------|---------|
| `id` | e.g. `E01_fork_hand` |
| `DAG` | edges + sketch |
| `DGP` | handcrafted table or `simulate_*` + seed + n |
| `target` | e.g. `x2` |
| `E+ / E−` | definition |
| **Prediction** | vars in delta; assumptions? |
| **Outcome** | rules, Coverage, Dependencies, Corr vs GT |
| **Verdict** | match / partial / surprise |
| `artifacts` | path under `outputs/aba_learning/MyExperiments/<id>/` |

### Runner pattern

1. Copy test recipe: DataFrame → `generate_aba_background_knowledge` → pos/neg → `run_prolog_aba_asp` → `_extract_learned_rules` + diagnostics.
2. Artifacts: `data.csv`, `.bk.aba`, `.bk.sol.aba` per experiment id.
3. Optional later: thin `run_experiment.py` + YAML spec when copy-paste is tedious.

**Example gaps to fill:** own fork/collider handcrafted; larger n vs n=6; wrong-target study; continuous handcrafted; qualitative “arrow hint” notes for future Causal ABA bridge.

**Exit:** 3–5 logged experiments with prediction + outcome + artifacts; explain one failure mode from your own run.

---

## After Phase 4 (supervisor track)

1. Experiment 1 sanity check — known G* → data → learn per target → compare to G* (extend `Corr vs GT` style checks).
2. Bridge (Alt 3) — CI facts from data + directional hints from learned rules → Causal ABA → Ĝ vs G*.

---

## Quick commands

```bash
cd "/Users/samuelwaugh/Desktop/Causal ABA Learning/aba_asp/causal"
conda activate aba-env

# Phase 1b
python -m unittest test_aba_learning.TestAssumptionIntroduction.test_exception_triggers_assumption_intro -v

# Phase 2 (one at a time)
python -m unittest test_aba_learning.TestMinimalDiscreteData.test_01_discrete_chain_6_samples -v

# Phase 3 (one at a time)
python -m unittest test_aba_learning.TestMinimalContinuousData.test_continuous_8_samples -v
python -m unittest test_aba_learning.TestMinimalContinuousData.test_continuous_confounder_x0_to_x1_x2_all_targets -v
python -m unittest test_aba_learning.TestMinimalContinuousData.test_continuous_collider_x0_x1_to_x2_all_targets -v
```

Artifacts: `outputs/aba_learning/<TestClassName>/`.
