# Approach — Expanded M1.2

**Role:** locked design reference for selecting graphs, assigning mechanisms, and defining
cells before any expanded M1.2 implementation or run.  
**Status:** active (2026-07-16) — still within “Lock the expanded M1.2 design”.  
**Primary path:** [`../milestone1_high_level_path.md`](../milestone1_high_level_path.md)  
**Parent index:** [`../milestone1-plan.md`](../milestone1-plan.md)

Use this document together when designing each graph × mechanism card. Do not implement
or run the expanded grid until every selected cell has the inputs listed below.

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
- For each \(y\in N\), fix one deterministic mechanism
  \[
  y=f_y(\mathrm{Pa}(y))\in\{\operatorname{copy},\min,\max\},
  \]
  with **copy only when** \(|\mathrm{Pa}(y)|=1\).
- Table \(\mathcal{D}\): **full source factorial** over \(K^{|S|}\), then propagate in
  topological order.
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

- exact-value predicates `x_val_0`, `x_val_1`, `x_val_2`;
- definitional nonzero rules (**facts**, not assumptions):

```prolog
x_nz(A) :- x_val_1(A).
x_nz(A) :- x_val_2(A).
```

No contrary/assumption encoding of nonzero: nonzero is observed fact, not defeasible
knowledge.

## Predictors for a target \(t\)

**BK includes every variable except the target \(t\)** (full table columns minus \(t\)),
with `val` + definitional `nz` for each. That includes **ancestors, siblings, and
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
intensional rule set in the `nz` language derived from the mechanisms
(e.g. max collider: `t(A) :- a_nz(A).` and `t(A) :- b_nz(A).`).

Because `nz` is in BK, a correct compact `nz` rule is preferred; an equivalent
`val`-expansion is considered inferior.

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
| DGP family (deterministic copy/min/max; full source factorial) | Locked |
| Labelling (nonzero-positive); \(k=3\) | Locked |
| BK (`val` + definitional `nz`) | Locked |
| Configs (ECAI, AAMAS) | Locked |
| Predictor policy (all non-targets in BK; descendant citation = failure) | Locked (corrected 2026-07-16) |
| Inspection-first acceptance (no precise pre-enumerated \(\mathcal{A}_t\)) | Locked |
| Graph × mechanism unit set | **Accepted** — [`milestone1_part2_expanded_unit_set.md`](milestone1_part2_expanded_unit_set.md) (U1–U7, 22 cells) |
| Mechanism cards U1–U7 | **Written** — [`mechanism_cards/`](mechanism_cards/) |
| Fixtures + 22-cell grid (M12x) | **Constructed** — `handcrafted_m12x.py`, `M12x_{ecai2024,aamas2025}.yaml` |

## Next step

Run both M12x arms (`run_grid`), then inspect against mechanism-card \(\mathcal{H}^\star\).
