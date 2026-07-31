# Approach — M1.3

**Role:** working reference for Milestone 1 Part 3 — investigating **claims** about how
unguided ABA Learning behaves on the locked M1.2 regime.
**Status:** Bucket 1 **locked**; Bucket 2 **locked / closed** with Claims 1–2;
Bucket 3's immediate deterministic-mechanism direction is approved (2026-07-31), while
its first research fixture and claims remain pending. M12x and Buckets 1–2 remain fixed
evidence. The earlier method below records the completed Bucket 1/2 workflow.
**Primary path:** [`../milestone1_high_level_path.md`](../milestone1_high_level_path.md)
**Parent index:** [`../milestone1-plan.md`](../milestone1-plan.md)

**M1.2 Approach (vocabulary source):**
[`../milestone1_part2/milestone1_part2_expanded_approach.md`](../milestone1_part2/milestone1_part2_expanded_approach.md)

**M12x evidence base (locked):**
`docs/experiments/qualitative/M1.2-expanded.md`;
`docs/experiments/qualitative/M1.2-expanded-cell-inspection.md` (18/18);
`causal/outputs/aba_learning/grid/M12x_summary.md`

---

## 22 July 2026 scope expansion

Following Fabrizio's review, M1.3 now continues beyond the fixed M12x regime through a
new Bucket 3. The supervisor-defined planning dimensions are: target variation and
target-agnostic analysis; partial data availability; larger controlled graphs;
graph–mechanism validity; explicit correlation, marginal/conditional independence, and
Markov equivalence; attribution of strategy failures versus information/data
limitations; and possible category-count or non-discrete extensions.

This section is a scope record, not an experiment design. No Bucket 3 claim list,
fixture portfolio, or run matrix is approved. See
`docs/experiments/qualitative/M1.3-bucket3-claims.md` and the 22 July section of
`docs/research/supervisor_guidance.md`.

## 31 July 2026 immediate approach

Fabrizio's follow-up review made the near-term object more specific: study what ABALearn
does when stochasticity is confined to independent non-degenerate roots and non-root
variables are deterministic functions of their causal parents. The remaining 22 July
dimensions are retained but deferred.

Proceed one causal fixture at a time:

1. **Fix graph and mechanisms.** State the DAG, root distributions, deterministic
   structural functions, node roles, and graph-theoretic MEC/CPDAG. These are
   evaluator-only. Use (A,B,C,\ldots) as mathematical labels and the corresponding
   lowercase `a`, `b`, `c`, ... as learner-safe YAML/CSV/predicate identifiers; do not
   rename existing `xN` evidence.
2. **Derive the population.** Factorise the exact finite distribution, enumerate its
   positive-probability support and structural zeros, and verify the causal Markov
   condition and ordinary faithfulness for this fixture. Do not infer faithfulness from
   determinism.
3. **Fix the evaluator reference.** Record each full non-root truth table; distinguish
   formal, population-supported, and later sample-observed parent configurations; derive
   canonical positive-state exact-value rules. Record that root targets have no
   deterministic causal rule over other observed variables.
4. **Freeze one target-free sample.** Sample the stochastic roots IID with an explicit
   seed and propagate deterministic descendants. Choose sample size only after the
   population/support reference is understood.
5. **Run all targets on that table.** Changing target creates a new learning task, not a
   new sample. Keep the evaluator graph and mechanism reference outside BK and examples.
6. **Inspect before extending.** Describe outcome, trace, learned delta, assumptions,
   contraries, and rule bodies for every target. Compare them with the evaluator
   reference semantically and attribute discrepancies to strategy, representation,
   finite-sample support, population information, or observational identifiability as the
   evidence permits.
7. **Write the bounded case and reassess.** Only then decide which contrasting mechanism
   is needed next. Do not precommit a fixture portfolio or run matrix.

The two-node copy relation is an explicit orientation warning: dependence between
$A$ and $B:=A$ does not identify $A\to B$ rather than $B\to A$. Whether a larger
graph supplies orientation information is fixture-dependent and must be analysed rather
than assumed.

The existing positive-stochastic diamond and its target-wise runs are retained as
pre-pivot exploratory/infrastructure artefacts. They are not part of the deterministic
case sequence and do not yet support a Bucket 3 claim.

---

## Relation to M1.2

M1.3 starts only once the M1.2 / M12x regime, cells, \(\mathcal{H}_t^\star\), and
semantic success descriptions are locked. M1.3 does **not** redesign that regime. It
investigates **claims** about how unguided ABA Learning behaves on it, using M1.2
vocabulary.

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
| \(\mathcal{H}_t^\star\) | Reference `val`-language rule set only — not the interesting metric |
| Semantic success description | Inspection-first acceptance criterion from M1.2 |
| Learned δ, traces | What was recovered and how |
| **Claim** \(C_i\) | Assertion about how ABA Learning learns — **not** \(\mathcal{H}_t^\star\) |

---

## Judgment

- Acceptance remains **inspection-first** against the M1.2 semantic success description.
- **Descendant citation** is always outside semantic success.
- Exact match to \(\mathcal{H}_t^\star\) may be noted once; it is mostly uninteresting as
  a metric. Claims work at a **more specific** level of what was recovered and whether
  it is acceptable / inferior / divergent under the semantic description.

---

## Claims

- Initial claims come only from **visible M12x patterns** (at least 3, at most 10;
  cover what is worth saying; little overlap).
- Include **specific** ECAI–AAMAS divergence claims where warranted; each must name
  and explain that particular divergence.
- **No claim investigation order until the list exists.** Order is chosen after the
  list is generated.
- A **dedicated live working claim list** (created when drafting begins) holds the
  current set of claims.
- Each active claim also has its **own live working doc**. When that claim is
  finished, write `claim_<slug>.tex` (slug tied to the pattern). Then move to the
  next claim.

---

## Role of M12x Stage-3

Base for thinking up and initially validating the claim list. Cursor does an
intelligent pass over M12x (inspection + patterns) to help generate that list — not a
full re-trace of all cells under the M1.3 trace standard before claiming.

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

Buckets 1–2 provide non-overlapping insight into the locked categorical target-wise
regime. Under Fabrizio's 31 July direction, Bucket 3 first needs a mechanism-by-mechanism
account of deterministic non-root causal models before the broader 22 July dimensions or
Causal ABA integration are pursued. Any Milestone 2 guidance must be motivated by
diagnosed learner behaviour and explicit information/identifiability limits rather than
by the fixed M12x regime alone.

---

## Document layout (expected)

| Artefact | Purpose |
|----------|---------|
| This file | M1.3 Approach (point of reference) |
| Live claim list (when drafting starts) | Unordered list of \(C_i\); subject to change |
| Live working doc per claim | Experimentation notes while \(C_i\) is open |
| `claim_<slug>.tex` | Frozen findings chapter after \(C_i\) is done |
| `docs/experiments/qualitative/M1.3-bucket1-claims.md` | Bucket 1 claims (**locked**) |
| `docs/report/findings/milestone1_part3_bucket1_claims.tex` | TeX companion for Bucket 1 |
| `docs/experiments/qualitative/M1.3-bucket2-claims.md` | Bucket 2 claims (**locked**) |
| `docs/report/findings/milestone1_part3_bucket2_claims.tex` | TeX companion for Bucket 2 |
| `docs/experiments/qualitative/M1.3-bucket3-claims.md` | Bucket 3 scope / planning record |
| M12x Stage-3 inspection | Observational base for the initial claim list |
