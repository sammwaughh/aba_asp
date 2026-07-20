# Approach — Expanded M1.2

**Role:** locked design reference for the expanded M1.2 (M12x) grid — graphs, mechanisms,
BK/labelling regime, and \(\mathcal{H}^\star\) acceptance.  
**Status:** design vocabulary retained; **U1–U7 mechanisms locked** (2026-07-20) —
first M12x run historical; re-run on 20-cell grid next.  
**Primary path:** [`../milestone1_high_level_path.md`](../milestone1_high_level_path.md)  
**Parent index:** [`../milestone1-plan.md`](../milestone1-plan.md)

Evidence package: `docs/experiments/qualitative/M1.2-expanded.md`;
`M1.2-expanded-cell-inspection.md`; `causal/outputs/aba_learning/grid/M12x_summary.md`.

---

## Question

When and how do the ECAI and AAMAS published ABA Learning configurations recover correct,
general, intensional rules from deterministic categorical mechanisms—and what do they
recover instead?

This is unguided ABA Learning **rule recovery**, not parent-set scoring and not Causal ABA.
Graphs come from Fabrizio; the DGP does not.

## Published learner configurations

| Config | File |
|--------|------|
| ECAI | `configs/ecai2024_config.pl` |
| AAMAS | `configs/aamas2025_config.pl` |

No RuleML. Prefer the word **config**, not “arm”.

## Fixture construction

For each selected DAG \(G=(V,E)\):

- Alphabet always \(K=\{0,1,2\}\).
- Sources \(S\): nodes with no parents.
- Non-sources \(N\): all other nodes.
- For each \(y\in N\), fix one deterministic mechanism \(y=f_y(\mathrm{Pa}(y))\).
  Multi-parent nodes use \(\min\) or \(\max\). Single-parent maps are unit-specific
  (e.g. \(\operatorname{copy}\) on U1; asymmetric indicators on U4).
  U5 is an exception: pilot curated \((x_0,x_1)\) support with \(x_2:=\operatorname{copy}(x_1)\)
  (not full source factorial; \(x_1\) not single-valued in \(x_0\)).
  U7 is an exception: curated diamond support (noisy \(x_2\) given \(x_0\); \(x_3:=|x_1-x_2|\)).
- Table \(\mathcal{D}\): **full source factorial** over \(K^{|S|}\), then propagate in
  topological order (U5/U7: curated multi-row support instead).
- Mix mechanisms so composition is nontrivial and nodes remain relevant.

The original five pilot fixtures are **redesigned inside this same regime** (not preserved
as a separate older DGP/label story).

Fabrizio provenance for candidate graphs (sibling repo
`ArgCausalDisco/tests.py`): G1 / G1a / G1c / G1d / G3 / G4 / G5, etc. Exclude random
graphs, bnlearn networks, and cycles.

## Labelling

For target \(t\):

- \(E^+\): rows with \(t\neq 0\)
- \(E^-\): rows with \(t=0\)

## Background knowledge

**Predictors** = every column except the learning target \(t\) (see next section). For
each such variable \(x\):

- exact-value predicates `x_val_0`, `x_val_1`, `x_val_2` only.

No definitional `*_nz` predicates in BK.

## Predictors for a target \(t\)

**BK includes every variable except the target \(t\)** (full table columns minus \(t\)),
with `val` predicates for each. That includes **ancestors, siblings, and
descendants**. Distractors are left in the BK on purpose.

For each \((G,t)\), record explicitly:

| Set | Role in BK | Role in a *good* learned rule |
|-----|------------|-------------------------------|
| **Ancestors of \(t\)** | Included | May appear |
| **Non-ancestor non-descendants** (e.g. siblings, isolated) | Included as distractors | Citing them is a divergence to inspect |
| **Descendants of \(t\)** | **Included as distractors** | Citing them is an **explicit failure mode** (wrong causal direction) |

Rules:

- Exclude from BK **only** the target \(t\) itself.
- **Do include descendants** of \(t\) in BK when they exist. The point of the experiment
  is to test whether the learner **ignores** them. Fabrizio wants descendant citation
  tested as a failure mode; excluding them from BK would make that test impossible.
- In the intended reading, non-target literals in a good intensional rule should be
  **ancestors of \(t\)**, not siblings or descendants.

## Experimental cell

\[
(\text{fixture},\ \text{target }t\in N,\ \text{config}\in\{\text{ECAI},\text{AAMAS}\})
\]

All cells are defined up front and run in one batch. Inspection order: targets nearer
sources first, sinks last.

## Reference hypothesis vs post-run judgment

For each \((G,t)\), design a **reference hypothesis** \(\mathcal{H}_t^\star\): a compact
intensional rule set in the `val` language that separates \(E^\pm\) on \(\mathcal{D}\)
(e.g. U1: `x2(A) :- x1_val_1(A).` and `x2(A) :- x1_val_2(A).` under nonzero-positive
labelling).

There is **no precisely pre-enumerated acceptable set**. Acceptance is judged **after the
run** by inspection, against a semantic description such as:

> an intensional, general rule that correctly characterises \(t\neq 0\) on \(\mathcal{D}\),
> using ancestor information appropriately, without rote sample-id casework and without
> citing descendants.

The scientific instrument is: define inputs clearly → run → inspect outputs → observe how
and whether they match what we wanted.

## What each mechanism card must contain

Before coding a graph:

1. Fabrizio provenance (file/method for the edge set).
2. Nodes, edges, sources \(S\), non-sources \(N\).
3. \(k=3\); every \(f_y\) for \(y\in N\).
4. Full \(\mathcal{D}\) (or an unambiguous generation rule = full source factorial).
5. For every target \(t\in N\): ancestors / sibling-or-other distractors / **descendant
   distractors (in BK)**; \(E^\pm\); \(\mathcal{H}_t^\star\); short semantic success
   description.
6. Non-collapse / relevance notes (why the mechanism mix does not make nodes irrelevant).

## What we record per cell (after runs)

- Inputs as above; BK path; config.
- Outputs: learned δ, assumptions/contraries, ASP coverage, `prolog.stdout` trace.
- Inspection: how and whether the output matches \(\mathcal{H}_t^\star\) / the semantic
  description, and what was recovered instead.

No single pre-ranked “main failure”. Patterns are induced from the runs and feed M1.3.

## Worked template (max collider)

Graph: \(x_0\to x_2\leftarrow x_1\); sources \(\{x_0,x_1\}\); \(x_2:=\max(x_0,x_1)\);
\(K=\{0,1,2\}\); 9-row source factorial; \(E^+=\{x_2\neq 0\}\), \(E^-=\{x_2=0\}\).

Reference:

```prolog
x2(A) :- x0_nz(A).
x2(A) :- x1_nz(A).
```

BK: `x0`/`x1` value predicates + definitional `*_nz`; target excluded. (No descendants
on this one-target sink fixture.)

Cells: `(max_collider, x2, ECAI)`, `(max_collider, x2, AAMAS)`.

## Current design lock status

| Item | Status |
|------|--------|
| DGP family (deterministic; full source factorial; unit-specific single-parent maps) | **Updating** |
| Labelling (nonzero-positive); \(k=3\) | Locked (for now; per-unit overrides allowed later) |
| BK (`val` only; no definitional `*_nz`) | **Updated 2026-07-20** |
| Configs (ECAI, AAMAS) | Locked |
| Predictor policy (all non-targets in BK; descendant citation = failure) | Locked (corrected 2026-07-16) |
| Inspection-first acceptance (no precise pre-enumerated \(\mathcal{A}_t\)) | Locked |
| Graph × mechanism unit set | **Updated** — U1–U7 redesigned (20-cell grid) |
| Mechanism cards U1–U7 | **Updated** — U7 diamond replaces OR cone |
| LaTeX unit catalogue | **Updated** — U1–U7 |
| Fixtures + grid (M12x) | **First run historical — redesign** (`definitional_nz: false`; 20 cells) |
| Summary matrix + cell reports | **First run historical — redesign** |

## Next step

Re-run M12x on the redesigned 20-cell grid; then Stage-3 inspection.
M1.3 stays paused until the redesigned grid is locked.
Separation-contract Stage-0 checks across U1–U6 are a follow-on (not blocking U7 lock).