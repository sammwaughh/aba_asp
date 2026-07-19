# Claim working doc — `ecai-x0-first-fold-and-defeasible-repair`

Working document for investigating this claim and writing
`claim_ecai-x0-first-fold-and-defeasible-repair.tex`.
M1.3 Approach: [`milestone1_part3_approach.md`](milestone1_part3_approach.md).
M12x vocabulary: [`../milestone1_part2/milestone1_part2_expanded_approach.md`](../milestone1_part2/milestone1_part2_expanded_approach.md).

**Status:** Step 1 — state the claim (wording under review).

---

## Scope and notation

This claim concerns the eleven learning cells run under the published **ECAI**
configuration on the locked expanded Milestone 1 Part 2 grid (**M12x**). Each cell is a
triple \((\text{fixture},\, t,\, \mathrm{ECAI})\), where the fixture is one of the
mechanism cards U1–U7, \(t\) is a non-source learning target, and ECAI denotes
`configs/ecai2024_config.pl` (in particular `learning_mode(brave)`,
`folding_mode(nd)`, `folding_selection(any)`, `folding_space(all)`,
`asm_intro(relto)`).

For a cell with table \(\mathcal{D}\) and target \(t\):

- \(E^+\) is the set of positive examples (rows with \(t \neq 0\));
- \(E^-\) is the set of negative examples (rows with \(t = 0\));
- the background knowledge (BK) contains, for every column other than \(t\), the
  exact-value predicates `x_val_0`, `x_val_1`, `x_val_2` and the definitional
  nonzero rules for `x_nz`.

ABA Learning starts from an initial framework encoding this BK and transforms it by
Rote Learning, Folding, Assumption Introduction, and Subsumption
\cite{proietti2022learning,de2023aba,de2024learning}. Under **brave** learning, a
framework \(\mathcal{F}'\) solves the task when there exists a stable extension
\(\Delta\) such that every \(e \in E^+\) is accepted in \(\Delta\) and no
\(e \in E^-\) is accepted in \(\Delta\). After each candidate Folding step, the
implementation checks whether the resulting framework still bravely entails
\(\langle E^+, E^-\rangle\). If that check fails, the published ECAI strategy may
apply **Assumption Introduction**: a folded rule \(H \leftarrow B\) is replaced by
\(H \leftarrow B, \alpha\) for a new assumption \(\alpha\), after which rules for the
contrary \(\overline{\alpha}\) are learnt so that exceptions undercut \(\alpha\).

On M12x, columns are serialised into BK in index order \(x_0, x_1, \ldots\). Under the
returned ECAI first-solution paths, the first Folding step applied to a target rote
rule always uses an `x0_val_*` body literal. The scientific interest of this claim is
what happens **after** that step: when brave entailment is preserved, when it is
broken, what governs the split, and how the broken class is repaired.

---

## Provisional claim

On the eleven returned M12x ECAI first-solution paths, the first target Folding step
uses an `x0_val_*` literal. Immediate checking of brave entailment of
\(\langle E^+, E^-\rangle\) then partitions the cells into two classes.

**Class P — brave entailment preserved (4 cells).**
U4-\(x_1\), U4-\(x_2\), U5-\(x_1\), and U5-\(x_2\).
In these cells an intensional target theory whose bodies mention only \(x_0\) already
separates \(E^+\) from \(E^-\) on \(\mathcal{D}\). The returned path therefore keeps
direct `x0_val_*` target rules and never enters Assumption Introduction.

**Class B — brave entailment broken (7 cells).**
U1-\(x_2\), U2-\(x_2\), U3-\(x_2\), U6-\(x_2\), U6-\(x_3\), U7-\(x_2\), and
U7-\(x_3\).
Here an \(x_0\)-only fold overgeneralises: some negative examples become covered, or
some positives are lost, under the brave check. The returned path then applies
Assumption Introduction, Rote-learns instances of the new contrary, and eventually
accepts Folding of those contrary rules with body `x1_val_0`. The conditions that make
the solution work are therefore distributed across target rules, assumptions, and
contrary-deriving rules. Inspecting only the bodies of the learnt target rules
understates what the returned framework \(\mathcal{F}'\) represents.

**Governing pattern.** The partition is explained by a single extensional criterion on
\(\mathcal{D}\): whether the nonzero-positive labelling of \(t\) is already separable
by conditions on \(x_0\) alone.

- If every row with \(t \neq 0\) can be distinguished from every row with \(t = 0\)
  using only the value of \(x_0\), then Folding to `x0_val_*` preserves brave
  entailment and the cell falls in Class P. This holds for the copy mechanisms in
  which \(t\) is a (possibly indirect) deterministic function of \(x_0\) on the locked
  table: U4’s children copy \(x_0\); U5-\(x_1\) copies \(x_0\); and U5-\(x_2\) copies
  \(x_1\) but, on \(\mathcal{D}\), is tied to \(x_0\) through the chain, so an
  \(x_0\)-only theory still separates \(E^\pm\).
- If no such \(x_0\)-only separation exists, the same Folding step breaks brave
  entailment and the cell falls in Class B. This holds for the two-parent min/max
  mechanisms (U2, U3, and the corresponding targets in U6 and U7), where the label of
  \(t\) depends on both parents, and for U1-\(x_2\), whose unique parent is \(x_1\)
  while \(x_0\) is an isolated distractor.

This criterion is stated at the level of \(E^\pm\) on \(\mathcal{D}\). It does not
coincide with the M1.2 semantic-success descriptions on the mechanism cards. The
clearest illustration is U5-\(x_2\): Class P membership is correct under the brave
check, yet the card prefers an intensional account in terms of the local parent
\(x_1\) rather than the grandparent \(x_0\).

**Broken-class repair.** In all seven Class B cells, every contrary-deriving rule in
the returned `bk.sol.aba` has body `x1_val_0`, and the number of such rules equals the
number of introduced assumptions. On the collider min and max cells, reading the full
framework suggests that this repair recovers the intended conjunctive or disjunctive
nonzero condition extensionally on \(\mathcal{D}\): U2 (and U6-\(x_2\)) use
assumption-guarded nonzero `x0_val_*` rules whose contraries fire when \(x_1 = 0\);
U3 (and U7-\(x_2\)) use unconditional rules for `x0_val_1`/`x0_val_2` together with an
assumption-guarded `x0_val_0` rule whose contrary is again `x1_val_0`. Those logical
readings still require an explicit stable-extension argument; they are part of what
this claim’s investigation must confirm.

**Contrast with AAMAS.** Under the published AAMAS configuration on the same eleven
M12x tasks, post-Folding brave entailment of \(\langle E^+, E^-\rangle\) is preserved
in every cell, and no returned solution contains assumptions. AAMAS therefore never
enters the Class B repair path. The solutions it returns are built by greedy
accumulation of selective row-level bodies over the non-target columns, which remain
sufficiently discriminating for \(E^\pm\) without Assumption Introduction. The point of
the contrast is that the preserve/break split and the subsequent defeasible repair are
characteristic of the returned ECAI paths on this grid, rather than of the M12x tasks
alone.

---

## Evidence already on record

The class membership, the uniform first `x0_val_*` Folding step on ECAI paths, the
`x1_val_0` contrary bodies in all Class B solutions, and the AAMAS contrast (11/11
post-Folding entailment preserved; zero assumptions) are taken from the closed M12x
Stage-3 package: cell traces under
`causal/outputs/aba_learning/grid/M12x_ecai2024/` and
`M12x_aamas2025/`, the summary matrix, and the scripted audits recorded in
`docs/experiments/qualitative/M1.3-failure-modes.md`.

---

## What remains to establish

1. Confirm, cell by cell for representative members of Classes P and B, that the
   extensional \(x_0\)-separability criterion above matches the brave-entailment
   outcome after the first Folding step, using the locked tables and example sets.
2. Give stable-extension readings of the Class B frameworks that justify the
   conjunctive and disjunctive interpretations suggested for U2 and U3 (and their
   U6/U7 analogues).
3. Test whether BK reorder moves cells between Classes P and B, and whether Class B
   still repairs via contrary Folding with `x1_val_0` whenever the first Folding step
   overgeneralises under the reordered BK.
