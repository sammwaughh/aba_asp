# M1.3 — Live working claim list

**Role:** live, provisional list of scientific **claims** to investigate in M1.3.
**Status:** initial M12x evidence pass complete; provisional list ready for review
(2026-07-17).
**Approach:** [`milestone1_part3_approach.md`](milestone1_part3_approach.md)
**M1.2 vocabulary:** [`../milestone1_part2/milestone1_part2_expanded_approach.md`](../milestone1_part2/milestone1_part2_expanded_approach.md)

This document is deliberately **unordered**. Slugs identify patterns; they do not set
an investigation priority. Claims may be kept, refined, split, merged, or discarded as
M1.3 reads traces and runs claim-specific probes.

In this document, a **claim** is an assertion about how unguided ABA Learning behaves.
It is not the M1.2 reference hypothesis \(\mathcal{H}_t^\star\). Exact agreement with
\(\mathcal{H}_t^\star\) is not the main judgment. Each investigation must inspect the
learned ABA framework against the mechanism card's semantic success description.
Descendant citation always remains outside semantic success.

## Evidence base for the initial list

- `docs/experiments/qualitative/M1.2-expanded-cell-inspection.md`
- `causal/outputs/aba_learning/grid/M12x_summary.md` and `.json`
- `causal/outputs/aba_learning/grid/M12x_learned_rules.md`
- M12x mechanism cards U1–U7
- scripted invariant audits over all 22 `prolog.stdout` traces and final
  `bk.sol.aba` frameworks, plus manual reading of representative full traces/frameworks
- published config files:
  - ECAI: `folding_mode(nd)`, `folding_selection(any)`, `folding_space(all)`,
    `asm_intro(relto)`
  - AAMAS: `folding_mode(greedy)`, `folding_selection(mgr)`,
    `folding_space(bk)`, `asm_intro(relto)`

The list below records **M12x-visible starting claims**, not conclusions. Direct trace
observations are distinguished from causal explanations that still require
claim-specific interventions.

**Critical interpretation note:** the M12x Stage-3 “exact
\(\mathcal{H}_t^\star\)?” column is not a semantic-success verdict. In particular,
an ECAI target δ that appears to omit \(x_1\) can place the \(x_1\) condition in a
learned contrary. M1.3 must therefore inspect target rules, contrary-deriving rules,
assumption declarations, contrary mappings, and traces together before judging what
was learned. Attacks and stable-extension behaviour must be reconstructed from ABA
semantics; the traces do not print an attack graph or witness extension.

## Trace-reading convention for later claim work

- Use the block after `Current learning options:` as the effective config. The earlier
  block contains load-time defaults.
- A printed `folding result` is a candidate, not necessarily a committed
  transformation. Treat it as accepted only when the subsequent `gen2` entailment gate
  accepts it and the result is present in `bk.sol.aba`.
- In AAMAS traces, `gen: computing greedy foldings` is MGR precomputation. The fold
  sequence printed later under `gen1: folding selection` is the actual Gen path.
- `bk.sol.aba` is the authority for the returned framework. `Writing solution no. 1`
  records the returned solution number; it does not establish uniqueness.
- The post-hoc ASP side-car reports per-atom brave coverage. It does not print a single
  common stable extension witnessing all examples.

Exact read-only audit commands and outcome summaries are recorded in
`docs/experiments/qualitative/M1.3-failure-modes.md`.

---

## `ecai-x0-first-fold-and-defeasible-repair`

### Provisional claim

In every returned M12x ECAI first-solution path, the first attempted target fold
replaces the sample equality with an exact-value predicate for \(x_0\), the earliest
serialized BK variable. The post-folding \(E^\pm\) gate then separates two observed
paths:

- it passes immediately in four cells, leaving direct `x0_val_*` target rules;
- it fails in seven cells, after which the returned path introduces assumptions,
  rote-learns contrary instances, and eventually accepts contrary folds using
  `x1_val_0`.

The second path splits relevant conditions across target rules and contraries.
Consequently, reading learned target rules or target-body scope alone understates what
the learned ABA framework represents. On the min/max cells, the final
assumption-and-contrary structures are extensionally consistent on \(\mathcal{D}\)
with the relevant conjunctive or disjunctive condition; the stable-extension account
still requires explicit validation during this claim's investigation.

### M12x observations

- Every ECAI learned target δ has body-scope variable set \(\{x_0\}\).
- A scripted all-cell trace audit found `x0_val_*` as the first target fold in
  11/11 ECAI cells.
- The first post-folding test passes in exactly four cells:
  U4-\(x_1\), U4-\(x_2\), U5-\(x_1\), U5-\(x_2\).
  The first three are parent-aligned `val` expansions; U5-\(x_2\) instead uses the
  extensionally equivalent grandparent \(x_0\), so immediate passage is not itself a
  semantic-success criterion.
- The first test fails and Assumption Introduction follows in seven cells:
  U1-\(x_2\), U2-\(x_2\), U3-\(x_2\), U6-\(x_2\), U6-\(x_3\),
  U7-\(x_2\), U7-\(x_3\).
- In those returned paths:
  `folding [A=i] with x0_val_v` → post-folding entailment failure →
  `generating NEW assumption` → rote learning of a contrary.
- For the newly rote-learned contrary, the candidate
  `c_alpha_i(A) :- x0_val_v(A)` fails `entails`;
  `exists_assumption_relto` finds the existing assumption, `gen3` prints `KO`, and
  Prolog backtracks to an `x1_val_0` fold that passes the entailment check.
- A scripted solution audit found that every learned contrary in the seven cells has
  body `x1_val_0`; the number of contrary rules equals the number of assumptions.
- Entailment-relative subsumption is part of the ECAI path:
  `evaluating subsumption` / `* subsumed: deleted!` removes target rote seeds already
  covered by accepted rules. Across M12x, 50 target rote seeds become 26 final target
  rules.
- Every realised ND fold begins with token 1 and ends with `0: DONE`; no ECAI trace
  increases the folding-token count. This describes the realised path, not the cause
  of literal selection.
- U2-\(x_2\) learns target rules over nonzero `x0_val_1/2` guarded by assumptions;
  both assumptions have contraries derived from `x1_val_0`. Inspection of the
  learned framework suggests the intended AND condition on \(\mathcal{D}\), subject
  to stable-extension validation.
- U3-\(x_2\) learns unconditional rules for `x0_val_1/2` plus an
  assumption-guarded `x0_val_0` rule whose contrary is `x1_val_0`. This represents
  an extensionally equivalent OR condition on \(\mathcal{D}\), subject to the same
  validation.
- U6/U7-\(x_2\) repeat the parent-level min/max shapes. U6/U7-\(x_3\) instead encode
  the extensionally equivalent **source-level** AND/OR described in the cards, rather
  than isolating the local \(\{x_1,x_2\}\) parent mechanism.
- U1 uses the same contrary condition `x1_val_0`, so the full framework captures the
  unique parent's nonzero condition even though every target rule also partitions on
  the isolated \(x_0\). That unnecessary distractor still violates U1 semantic success.

### What is not yet established

- This is a description of the returned first-solution paths, not evidence that they
  are uniquely forced outcomes.
- BK rule order, one-token folding, `nd`, `any`, `all`, rule identifiers, cuts, and
  first-solution collection remain potential interacting causes.
- The stable-extension account and semantic-success judgment must be presented
  explicitly for each representative framework; brave coverage alone does not prove
  the claimed logical equivalence.
- BK reorder and other controlled interventions are required before attributing the
  \(x_0\)-first path or repeated `x1_val_0` repair to a specific control mechanism.

---

## `aamas-positive-row-saturation`

### Provisional claim

On all 11 M12x cells, the AAMAS configuration turns each positive example into a
separate variable-bearing but extensionally row-specific target rule on
\(\mathcal{D}\). Its body retains a complete exact-value description over every
non-target column, plus each derivable `nz` literal, and positive rows are not merged
into a smaller mechanism-level rule set. The resulting δ is therefore a value-level
DNF of the observed positive region rather than a compressed account of the nonzero
mechanism.

### M12x observations

- In every AAMAS cell, the number of target rules equals \(|E^+|\):
  6 (U1), 4 (U2), 8 (U3), 2 (U4/U5), 4 (U6), and 8 (U7).
- Every rule contains an exact `xj_val_v` literal for every non-target column in BK.
- Whenever that row has \(x_j\neq0\), the same rule also contains `xj_nz`; the exact
  value literal remains, so `nz` does not replace the value-level condition.
- An all-cell invariant audit confirms both properties above for every AAMAS rule:
  every rule has the complete per-cell variable scope, and no `nz` literal appears
  without its matching nonzero exact-value literal.
- In greedy folding, while scanning `A=id`, `fold_greedy_aux` accumulates every
  matching exact-value head. Those newly appended heads are subsequently scanned and
  matching `nz` heads are accumulated; earlier heads are retained rather than
  replaced.
- MGR precomputation occurs once per cell. No AAMAS trace contains the
  `is more general than` / `< deleted!` landmark, and the final target-rule count
  equals the initial target rote count.
- No M12x AAMAS final delta contains assumptions, contrary mappings, or
  `c_alpha_*` rules.
- An all-cell trace audit finds that the first post-folding test passes in 11/11
  AAMAS cells. The inference from the final rules is that the complete row
  descriptions are already selective enough on \(\mathcal{D}\) to preserve
  \(E^\pm\), so Assumption Introduction is never reached on M12x.
- The direct collider pairs make the config divergence concrete:
  U2 returns 2 target rules + 2 assumptions/contraries under ECAI versus 4
  assumption-free row rules under AAMAS; U3 returns 3 + 1 versus 8 + 0.
  U6/U7 repeat those rule-shape contrasts, with AAMAS additionally retaining the
  descendant for target \(x_2\).

### What is not yet established

- Whether “one target rule per positive row” persists once rows share only a subset of
  relevant features or under controlled changes to the BK predicates.
- Whether `mgr` selection, exhaustive greedy folding, `folding_space(bk)`, or their
  interaction prevents cross-row compression.
- How far these value-level rules satisfy the semantic success descriptions on
  parent-only cells U2/U3, as opposed to merely providing full-domain DNF casework.
  U2/U3 are counterexamples to **wrong-variable selection**: their rules use parents
  only and enumerate the correct Boolean region. They may still fail the intended
  degree of intensional generality.

---

## `descendant-retention-divergence`

### Provisional claim

In all three descendant-bearing M12x cells—each of which makes the descendant
deterministically tied to the target on \(\mathcal{D}\)—the configs diverge:
AAMAS's all-predictor greedy accumulation includes descendant predicates in every
target rule, whereas the returned ECAI path accepts an earlier \(x_0\)-based
representation and never includes the later descendant predicates. Relative to the
mechanism cards, AAMAS fails and ECAI passes the **specific no-descendant criterion**.

### M12x observations

- The three and only M12x targets with descendants in BK are:
  U5-\(x_1\) (copy), U6-\(x_2\) (min), U7-\(x_2\) (max).
- AAMAS cites the descendant in all three cells (3/3), in every target rule:
  `x2_*` for U5-\(x_1\), and `x3_*` for U6/U7-\(x_2\).
- ECAI cites descendants in none of the paired cells (0/3).
- AAMAS's greedy traces show the descendant exact-value and `nz` predicates being
  folded into the rule in the same way as ancestor predicates; no graph-role
  distinction is visible in those transformations.
- In the cleanest copy contrast, U4-\(x_1\), U4-\(x_2\), and U5-\(x_1\) return two
  parent-only `val` rules under ECAI, while AAMAS returns two four-literal rules
  containing the parent plus the tied sibling or descendant.
- The related U4 pair shows the same AAMAS retention pattern for a perfectly tied
  sibling, while ECAI omits the sibling. U1 is an important boundary case: ECAI does
  cite the early isolated \(x_0\), so its omission of later distractors cannot yet be
  interpreted as causal-role awareness.
- AAMAS also retains the sibling in U4 and the independent isolated \(x_0\) in U1.
  These controls indicate a broader complete-predictor pattern, not a learned
  preference for descendants.
- Passing the no-descendant criterion is not a complete semantic-success judgment:
  U5-\(x_1\) remains an inferior parent `val` expansion and U6/U7-\(x_2\) remain
  assumption-mediated representations requiring full-framework interpretation.

### What is not yet established

- The current traces support all-predictor greedy accumulation as AAMAS's immediate
  process; what remains unestablished is whether retention persists under changed BK
  scope, ordering, or predicate representation.
- The learner receives no graph-role labels, so ECAI's omission must not be described
  as recognising an ancestor. What remains open is whether omission changes when
  earlier folds, BK order, or BK scope are controlled.
- The controlled contrasts are deferred to this claim's investigation.

---

## `nz-without-abstraction`

### Provisional claim

Providing definitional `*_nz` predicates in BK does not by itself make either config's
returned M12x target rules use `nz` as a **replacement abstraction**. Returned ECAI
target folds replace `A=id` with one exact-value head; AAMAS derives `nz` heads but
retains the exact-value heads that entail them. The two configs therefore preserve
value-level distinctions through different immediate folding processes.

### M12x observations

- No ECAI target rule in the 11 cells contains an `*_nz` literal.
- ECAI uses `*_val_*` directly, with assumptions where those first folds
  overgeneralise.
- AAMAS includes `*_nz` for nonzero values, but always alongside the corresponding
  `*_val_1` or `*_val_2` literal; the `nz` literal is logically redundant in that body.
- This pattern holds across copy, min, and max mechanisms and across 3- and 4-node
  fixtures.
- In `fold_nd_wtc`, the exact-value head is accumulated in the ECAI fold output but is
  not requeued for another `val`→`nz` fold on this rule shape.
- In `fold_greedy_aux`, a newly produced exact-value head is appended to the scan list
  as well as retained in the output, allowing the later `val`→`nz` fold while keeping
  both heads.
- Absence of `nz` is not automatically semantic failure: U4-\(x_1\), U4-\(x_2\), and
  U5-\(x_1\) are ancestor-correct, distractor-free parent `val` expansions, although
  inferior to the compact reference form.

### What is not yet established

- BK ordering alone does not supply the missing recursive ND step for this rule shape;
  whether another folding mode or BK representation yields `nz` replacement requires
  intervention.
- The immediate implementation mechanisms are already distinct in `fold_nd_wtc` and
  `fold_greedy_aux`. What remains open is which config changes, if any, produce
  compressed `nz` target rules.
- The semantic importance of compression for each cell must be described rather than
  reduced to exact agreement with \(\mathcal{H}_t^\star\).

---

## `no-local-parent-preference`

### Provisional claim

On U5-\(x_2\), U6-\(x_3\), and U7-\(x_3\), local-parent and upstream/source
descriptions are extensionally indistinguishable on \(\mathcal{D}\), and neither
returned output isolates the card-defined local-parent boundary. The returned ECAI
first solution uses an extensionally equivalent upstream or source-level framework;
AAMAS greedy closure accumulates local-parent literals together with redundant
upstream literals. The configs therefore return extensionally adequate theories at
different structural scopes without isolating the local-parent boundary in their final
syntax.

### M12x observations

- U5-\(x_2\):
  ECAI learns only grandparent `x0_val_1/2`; AAMAS conjoins grandparent \(x_0\) and
  parent \(x_1\).
  In the ECAI trace, the first `x0_val_*` folds pass the entailment gate; no alternative
  `x1` target fold is printed in the returned path.
- U6-\(x_3\):
  ECAI represents the source-level AND through \(x_0\) target rules and \(x_1\)
  contraries; AAMAS includes \(x_0\), \(x_1\), and parent \(x_2\).
- U7-\(x_3\):
  ECAI represents the source-level OR through \(x_0\) target rules and \(x_1\)
  contraries; AAMAS includes \(x_0\), \(x_1\), and parent \(x_2\).
- The U6/U7 mechanism cards explicitly recognise the source-level AND/OR as
  extensionally equivalent alternatives to inspect, so this claim concerns **local
  parent preference**, not simple extensional correctness.
- In U6/U7-\(x_3\), accepted ECAI target folds use \(x_0\), accepted contrary folds
  use `x1_val_0`, and \(x_2\) does not appear in the returned delta.
- This claim is restricted to the three composed sink cells. ECAI does isolate the
  direct parent in U4-\(x_1\), U4-\(x_2\), and U5-\(x_1\).
- Parent/ancestor labels are post-hoc mechanism-card annotations. The Prolog learner
  receives BK and examples, not graph roles; the traces establish output structure,
  not an internal causal preference.

### What is not yet established

- Whether the absence of local-parent preference is an unavoidable identifiability
  limitation of these deterministic tables, a search-order effect, or both.
- Whether either config selects local parents when upstream equivalence is broken while
  the same graph and target are retained.
- How to qualify source-level alternatives under semantic success without treating
  \(\mathcal{H}_t^\star\) as the sole acceptable output.

---

## `coverage-without-semantic-discrimination`

### Provisional claim

For every M12x cell, the post-hoc ASP side-car reports that each positive atom is
bravely entailed and each negative atom is not bravely entailed. This per-atom signal
is identical across qualitatively different learned frameworks, including outputs
that violate explicit semantic criteria by citing descendants, siblings, or an
isolated variable. It therefore does not discriminate semantic success in M12x and is
insufficient for judging intensional or mechanism-aligned recovery.

### M12x observations

- ASP side-car coverage is complete in all 22 cells.
- The fully covering set includes:
  - AAMAS descendant citation in U5-\(x_1\), U6-\(x_2\), and U7-\(x_2\);
  - AAMAS sibling citation in both U4 cells;
  - isolated-variable citation under both configs in U1;
  - parent-only but value-expanded or assumption-mediated theories in U2/U3;
  - mixed parent/ancestor representations in U5/U6/U7 sink cells.
- In matched U5-\(x_1\), U6-\(x_2\), and U7-\(x_2\) pairs, both configs receive the
  same complete side-car result although AAMAS cites a descendant and ECAI does not.
- Complete coverage also accompanies structurally closer but inferior outputs, such
  as the three ECAI parent-only `val` expansions.
- The engine's in-run `gen2` gate jointly constrains \(E^\pm\) for an accepted
  candidate. The separate side-car result remains per-atom and does not record a
  common witness extension.

### What is not yet established

- This is a bounded M12x finding, not a claim that coverage is generally useless.
- It does not evaluate behaviour outside \(\mathcal{D}\), other label definitions, or
  other ABA Learning configurations.
- The semantic status of non-descendant, ancestor-only alternatives still requires
  claim-specific qualitative judgment.
- Neither `prolog.stdout` nor the side-car records the selected stable extension or an
  attack graph; those cannot be inferred from a complete fraction alone.

---

## Cross-claim boundaries to protect

- `ecai-x0-first-fold-and-defeasible-repair` owns the returned ECAI transformation
  path and the target-rule/contrary split; structural locality belongs below.
- `aamas-positive-row-saturation` concerns generality/compression across all AAMAS
  cells; `descendant-retention-divergence` concerns the causal-direction consequence
  on the three descendant-bearing targets and the paired config contrast.
- `nz-without-abstraction` concerns use of an explicitly supplied abstraction language;
  it should not be collapsed into “not exact \(\mathcal{H}^\star\).”
- `no-local-parent-preference` concerns parent locality under deterministic
  composition, not whether an ancestor-based theory is extensionally correct.
- `coverage-without-semantic-discrimination` concerns the weakness of the observed
  coverage signal; it must not replace the claim-specific semantic analyses above.

These boundaries are provisional. If investigation shows that two claims have the same
evidential burden and conclusion, they should be merged rather than written twice.

## Next state of this document

Samuel reviews the six provisional claims and their boundaries; only then is an
investigation order chosen. Do not open a `claim_<slug>.tex` until the corresponding
claim has been fully investigated and concluded.
