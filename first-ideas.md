# First ideas — guiding ABA Learning toward mechanism-aligned rules

> **Historical brainstorming — not the Milestone-2 plan.** This file predates the
> completed M1.3 Bucket-3 investigation and the 8 August 2026 opening of Milestone 2.
> None of the proposals below is approved, validated, or scheduled. Several use oracle
> graphs or assumed Causal ABA outputs and therefore cannot be treated as discovery
> designs without a new justification. M2 begins by understanding the argumentative
> causal discovery paper and ArgCausalDisco intimately; possible integrations with ABA
> Learning will then be tried and tested without a prescribed form or sequence.
> See `docs/research/milestone_plans/milestone2/README.md`.

Grounded proposals for configuring ABA Learning (or making limited algorithm / pipeline
changes) so that the locked mechanism-aligned rules on the M1.2 fixtures are actually
learned. Each idea is tied to a concrete M1.2 failure mode and to something that can be
implemented and tested. None invents new Causal ABA semantics; they use existing Causal
ABA objects (`arr` / `noe` / `indep`, extensions-as-DAGs) or ordinary ABA Learning knobs
as **guidance** over the same tabular learning problem.

**Evidence base:** M1.2 two-arm grid (ECAI ASP-ABAlearnB + AAMAS Greedy ABA Learning),
10 cells; failure modes FM1 and FM3–FM7 in
`docs/experiments/qualitative/M1.2-config-comparison-cell-inspection.md`.

**Assumption (explicit):** using true \(G\) or oracle CI on toys is fine for *capability*
tests of guidance; for a discovery claim, replace that with Causal ABA extensions / CI
tests from data only.

---

### 1. Body-minimality preference among covering folds

**Problem:** FM4–FM6 (AAMAS keeps every safe co-occurring literal).

**Idea:** When several folds of a rote rule still bravely entail \(\langle E^+, E^- \rangle\),
prefer the one with **fewest body literals** (then fewest distinct base variables).
Greedy today prefers maximal BK specialization; invert that among *safe* folds.

**Implement:** In `FoldingWAsmIntro` / fold selection (`mgr` / `any`), rank candidate
folds by body length after the post-fold entailment check; keep shortest that SAT.
Config flag e.g. `folding_preference(min_body)`.

**Test:** Re-run AAMAS×{sep, fork, chain}. Success = exact locked rules (or at least
drop sibling/ancestor). Conj should stay exact.

---

### 2. Post-hoc literal-deletion compression (new transform, not Folding)

**Problem:** Same FM4–FM6; Folding cannot drop `x0_val_*` once you are at value-predicate
bodies.

**Idea:** After GEN stops, for each target rule try deleting body literals one-by-one
(or by set-cover search) **while** ASP brave coverage of \(\langle E^+, E^- \rangle\) is
preserved; also try merging sibling rules that become identical after deletion.

**Implement:** Python post-process on `bk.sol.aba` + `bk.sol.asp` using existing
`asp_answer_set_coverage`; or a Prolog `compress/1` after `genT`.

**Test:** Feed AAMAS sep’s three rules through the compressor → expect
`x2(A) :- x1_val_2(A).` Same for fork/chain. Disj is a harder OR-compression variant
(idea 3).

---

### 3. Rule-count / DNF-compression objective

**Problem:** FM3 (five-cell DNF vs two-rule OR).

**Idea:** Among frameworks that cover \(\langle E^+, E^- \rangle\), prefer fewer target
rules with the same head (and/or shorter total body size). That pushes toward compact OR
when it exists in the language (Stage-0 verified for `m12_disj`).

**Implement:** ASP `#minimize` over target-rule count / body atoms in a hypothesis
generator (RASP-style encoding already minimizes *rote* atoms; extend to intensional
rule complexity), or beam-search rewrite: replace a set of conjunctive rules by
candidate single-literal / two-literal covers and check coverage.

**Test:** AAMAS×disj and ECAI×disj. Success = exactly the two locked OR rules.
Negative control: conj must not collapse incorrectly.

---

### 4. Assumption-averse fold selection (fix FM1 without Causal ABA)

**Problem:** FM1 (ECAI wrong-column fold → α + contraries).

**Idea:** Prefer any fold that preserves coverage **without** assumption introduction
over a fold that needs `asm_intro`. Only introduce assumptions if no assumption-free
fold sequence works within budget.

**Implement:** Config / `lopt`: try all safe folds first; gate `asm_intro` behind “no
covering fold remains.” Closest published relative: entailment gate already exists;
this is selection order.

**Test:** ECAI×sep/conj/chain. Success = assumption-free bodies citing the true
separator (or at least no parent-only-in-contraries). Keep ECAI×fork exact.

---

### 5. Foldable-BK restricted by Causal ABA edge assumptions

**Problem:** FM4–FM6; distractors are foldable because they are in BK.

**Idea (primer Direction 2):** Run Russo-style Causal ABA (or a cheap CI oracle) on the
same table → take a stable extension’s accepted `arr_*` into the target. Restrict
folding so target rules for `x2` may only fold against features of variables `x` with
`arr_x,x2` accepted (or not `noe_x,x2`).

**Implement:** Stage A: Causal ABA / PC on fixtures → parent set \(P(x2)\). Stage B:
ABA Learning with `folding_space` = feature predicates of \(P\) only (or mark other
predicates non-foldable in BK comments / engine flag).

**Test:** On `m12_chain`, if \(P=\{x1\}\), AAMAS/ECAI should be forced toward
`x1_val_2`. On fork, \(P=\{x0\}\) should kill sibling citation. On sep, \(P=\{x1\}\)
should kill `x0` case-split. **Must not** claim this is “learning the graph via ABA
Learning”; it is graph-guided rule learning.

---

### 6. Independence assumptions as hard constraints on rule bodies

**Problem:** FM6 especially (`x0` retained on chain though \(x0 \perp x2 \mid x1\) under
the DGP).

**Idea:** From Causal ABA / CI tests, if `indep(x0,x2,{x1})` is accepted (or CI holds in
the finite table), forbid any learned `x2` rule whose body mentions `x0_*` while also
allowing bodies with only `x1_*` that still cover—or more simply: ban `x0_*` from `x2`
bodies when that indep holds.

**Implement:** Integrity constraints in the ASP check used after each fold:
`:- x2_rule_uses(x0), indep_accepted(x0,x2,x1).` Or filter fold candidates whose new
body atoms violate indep.

**Test:** `m12_chain` (should enable parent-only). `m12_sep` if you encode
\(x0 \perp x2\) (unconditional). Check fork carefully: sibling may still correlate;
indep structure differs—use the fixture’s true CI pattern, don’t overclaim.

---

### 7. Two-stage “graph hypotheses then mechanisms” bridge

**Problem:** Unguided ABA Learning optimizes coverage only (M1.3 L1 attribution).

**Idea:** Milestone-2-shaped pipeline: (1) Causal ABA learns/accepts DAG hypotheses as
stable extensions; (2) for each accepted parent set of the target, run ABA Learning
**only** to recover the mechanism rule within that parent scope (value predicates of
parents). Compare mechanisms across extensions if multiple DAGs remain.

**Implement:** Thin orchestrator: Causal ABA ASP → parent sets; loop
`run_prolog_aba_asp` with per-extension BK masks; score by exact match to locked rules
*and* by extension identity.

**Test:** All five fixtures with known \(G\). Success = locked rule recovered whenever
the true \(G\)’s extension is selected. Ablate: shuffle/wrong parent set → exact match
should fail (shows guidance is doing work).

---

### 8. Prefer folds aligned with d-connecting parents, not merely associated features

**Problem:** FM1/FM5/FM6—association ≠ parent.

**Idea:** Soft preference: score a candidate fold by whether every body variable is a
parent of the target in at least one Causal ABA extension (or by CI: dependent on
target given empty set, independent given true parents). Use as tie-break after
coverage.

**Implement:** Precompute a variable score table; plug into `folding_selection`. No
change to transformation soundness if it only reorders candidates that already pass
entailment.

**Test:** ECAI×sep (should prefer `x1` over `x0`). AAMAS×fork (prefer drop `x1`).
Report whether preference alone suffices vs hard mask (idea 5).

---

### 9. Encode “allowed mechanism schemas” as BK fold targets (still guided, not free invention)

**Problem:** Folding only generalises *to existing BK heads*.

**Idea:** If Causal ABA (or the declared \(G\) in toys) says parents are \(\{x1\}\), add
intentional BK schema rules that folding can target—e.g. aggregate parent
indicators—**only when justified by accepted `arr`**. Example for toys: a single
predicate `par_x2(A) :- x1_val_2(A).` as BK when `arr_x1_x2` is accepted, then folding
can hit `x2(A) :- par_x2(A).`

**Implement:** BK writer conditional on guidance graph; keep schemas minimal and
fixture-declared in experiments.

**Test:** sep/chain with and without schema. Without schema + min-body (idea 1) may
already suffice; schema is for when you need an explicit fold target. Flag clearly as
guidance encoding, not unguided ABA Learning.

---

### 10. Config-only search portfolio before new theory

**Problem:** Exactness was strategy×fixture coincidence (ECAI fork, AAMAS conj).

**Idea:** Don’t change the algorithm first—grid a **small portfolio** of
published-adjacent options aimed at FM1/FM4: e.g. `folding_mode(nd)` + shorter-body
preference; `folding_space(bk)` vs `all`; `asm_intro` delayed; `folding_steps` budget;
optional `ecai2024ALL` if available. Causal guidance can be layered later.

**Implement:** New YAMLs, same fixtures, same exact-match side-car.

**Test:** Same 10 cells + exact-match matrix. Anything that moves sep/fork/chain/disj
to Y without Causal ABA is an L2 (config) finding for M1.3; failures that remain under
all portfolios strengthen the case for ideas 5–8 (L1 → Milestone 2).

---

## Suggested priority sequence

1. **Idea 2 or 1** — cheapest test of “minimal separators are in the language; search
   stops early.”
2. **Idea 3** — specifically for disj/OR.
3. **Idea 4** — ECAI FM1 without Causal ABA.
4. **Idea 5 + 6** — first real Causal ABA **guidance** bridge on the five toys.
5. **Idea 7** — full two-stage story once 5/6 show signal.
