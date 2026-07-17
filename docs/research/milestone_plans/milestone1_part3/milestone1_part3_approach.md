# Approach — M1.3

**Role:** working reference for Milestone 1 Part 3 — investigating **claims** about how
unguided ABA Learning behaves on the locked M1.2 regime.
**Status:** active (2026-07-17) — initial claim list ready for review; no order set.
**Primary path:** [`../milestone1_high_level_path.md`](../milestone1_high_level_path.md)
**Parent index:** [`../milestone1-plan.md`](../milestone1-plan.md)

**M1.2 Approach (locked; vocabulary source):**
[`../milestone1_part2/milestone1_part2_expanded_approach.md`](../milestone1_part2/milestone1_part2_expanded_approach.md)

**M12x evidence base:**
`docs/experiments/qualitative/M1.2-expanded.md`;
`docs/experiments/qualitative/M1.2-expanded-cell-inspection.md`;
`causal/outputs/aba_learning/grid/M12x_summary.md`

---

## Relation to M1.2

The M1.2 Approach is locked (regime, cells, \(\mathcal{H}_t^\star\), semantic success
description, M12x). M1.3 does **not** redesign it. It investigates **claims** about how
unguided ABA Learning behaves on that regime, using M1.2 vocabulary.

In M1.2, **hypothesis** means the design artefact \(\mathcal{H}_t^\star\).
In M1.3, say **claim** for a scientific assertion about how ABA Learning learns. Those
are different objects.

---

## Question

When and how do configs \(\{\mathrm{ECAI},\mathrm{AAMAS}\}\) recover correct, general,
intensional rules from the locked deterministic categorical regime — and what do they
recover instead?

---

## Vocabulary

Keep M1.2 notation:

| Term | Meaning in M1.3 |
|------|------------------|
| Cell \((\text{fixture},\,t,\,\text{config})\) | Experimental unit |
| \(\mathcal{D}\), \(E^\pm\), BK | Locked inputs from M1.2 Approach |
| \(\mathcal{H}_t^\star\) | Reference compact-`nz` rule set only — not the interesting metric |
| Semantic success description | Inspection-first acceptance criterion from M1.2 |
| Learned δ, traces | What was recovered and how |
| **Claim** \(C_i\) | Assertion about how ABA Learning learns — **not** \(\mathcal{H}_t^\star\) |

---

## Judgment

- Acceptance remains **inspection-first** against the M1.2 semantic success description.
- **Descendant citation** is always outside semantic success.
- Exact match to \(\mathcal{H}_t^\star\) may be noted once (e.g. 0/22 on M12x); it is
  mostly uninteresting as a metric. Claims work at a **more specific** level of what was
  recovered and whether it is acceptable / inferior / divergent under the semantic
  description.

---

## Claims

- Initial claims come only from **visible M12x patterns** (at least 3, at most 10;
  cover what is worth saying; little overlap).
- Include **specific** ECAI–AAMAS divergence claims where warranted; each must name
  and explain that particular divergence.
- **No claim investigation order until the list exists.** Order is chosen after the
  list is generated.
- A **dedicated live working claim list** (editable as work proceeds) holds the
  current set of claims.
- Each active claim also has its **own live working doc**. When that claim is
  finished, write `claim_<slug>.tex` (slug tied to the pattern). Then move to the
  next claim.

---

## Role of M12x Stage-3

Base for thinking up and initially validating the claim list. Cursor does an
intelligent pass over M12x (inspection + patterns) to help generate that list — not a
full re-trace of all 22 cells under the M1.3 trace standard before claiming.

---

## Method (one claim at a time)

1. State \(C_i\) from M12x with clear scope.
2. In Cursor: read `prolog.stdout`, extract and interpret what matters, design and run
   probes as that claim needs, store artefacts.
   - BK reorder is in scope (M1.1 established representation-order effects).
   - Other contrasts (including whether to remove distractors from BK) are chosen
     **per claim**, not fixed in this Approach.
3. For cells that bear on \(C_i\): qualitative account of what was learned **and how** —
   relevant transformations, chosen literals/assumptions, final δ; present only the
   relevant trace material, in correct notation.
4. Keep / refine / discard \(C_i\) with theory, description, and evidence.
5. Write `claim_<slug>.tex` **only when that claim is done**; then the next claim.

---

## Final write-up

Ordered `claim_<slug>.tex` chapters + an overarching conclusion. Nuanced and
evidence-qualified; no headline-driven framing.

---

## M2-readiness

Kept claims give non-overlapping insight into unguided recovery on this principled cell
class — enough to begin Causal ABA integration. No reusable eval protocol in M1.3. No
fixed stop rule beyond covering the interesting M12x patterns.

---

## Document layout (expected)

| Artefact | Purpose |
|----------|---------|
| This file | M1.3 Approach (point of reference) |
| [`milestone1_part3_claim_list.md`](milestone1_part3_claim_list.md) | Live, unordered list of \(C_i\); subject to change |
| Live working doc per claim | Experimentation notes while \(C_i\) is open |
| `claim_<slug>.tex` | Frozen findings chapter after \(C_i\) is done |
| `docs/experiments/qualitative/M1.3-failure-modes.md` | Experiment record for M1.3 |
| M12x Stage-3 inspection | Observational base for the initial claim list |
