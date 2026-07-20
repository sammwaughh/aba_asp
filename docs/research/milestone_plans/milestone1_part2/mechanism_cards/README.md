# Expanded M1.2 — Mechanism cards (U1–U7)

**Role:** per-unit design cards locking graph, mechanisms, table \(\mathcal{D}\),
per-target BK sets, \(E^\pm\), reference \(\mathcal{H}_t^\star\), and semantic success
criteria before implementation.

**Status:** locked (2026-07-20) — U1–U7; 18-cell grid; fixture keys renamed to match mechanisms  
**Approach:** [`../milestone1_part2_expanded_approach.md`](../milestone1_part2_expanded_approach.md)  
**Unit set:** [`../milestone1_part2_expanded_unit_set.md`](../milestone1_part2_expanded_unit_set.md)  
**Compiled catalogue (all seven units in one PDF-ready `.tex`):**
[`../m12x_units_reference.tex`](../m12x_units_reference.tex)

| ID | File | Graph | Cells |
|----|------|-------|------:|
| U1 | [`U1_separator_copy.md`](U1_separator_copy.md) | sep + isolated \(x_0\) | 2 |
| U2 | [`U2_collider_min.md`](U2_collider_min.md) | collider | 2 |
| U3 | [`U3_collider_max.md`](U3_collider_max.md) | collider | 2 |
| U4 | [`U4_fork_asymmetric.md`](U4_fork_asymmetric.md) | fork (asymmetric maps) | 4 |
| U5 | [`U5_chain_curated.md`](U5_chain_curated.md) | chain (pilot correlated ancestor) | 2 |
| U6 | [`U6_g1_min_diff.md`](U6_g1_min_diff.md) | G1 (min then \(x_1-x_2\)) | 4 |
| U7 | [`U7_diamond_noisy.md`](U7_diamond_noisy.md) | diamond (noisy fork arms) | 2 |

**Total: 7 units, 18 cells** (each learning target × {ECAI, AAMAS}).

## Shared regime (do not restate differently on cards)

- Alphabet \(K=\{0,1,2\}\).
- **Table construction:** full source factorial over \(K^{|S|}\) then topological
  propagation for U1–U4 and U6; **curated multi-row support** for U5 and U7 (see those cards).
- Labels: \(E^+=\{t\neq 0\}\), \(E^-=\{t=0\}\) unless a unit card overrides.
- BK: for every column except \(t\), exact-value predicates `*_val_0/1/2`.
- **Descendants of \(t\) stay in BK** as distractors; citing them in a learned rule is a failure mode.
- Only \(t\) itself is excluded from feature BK.
- Learning targets are those listed on each card (not automatically every non-source).
- Configs: ECAI (`configs/ecai2024_config.pl`), AAMAS (`configs/aamas2025_config.pl`).
- Acceptance is inspection-first against \(\mathcal{H}_t^\star\) / the semantic description; no precise pre-enumerated \(\mathcal{A}_t\).
- Intended \(\mathcal{H}_t^\star\) is stated in the `val` language on each card.

## Next

Fresh 18-cell learning run (`--no-resume` both arms → `m12x_summary`), then Stage-3
inspection. Prior M12x outputs were deleted (2026-07-20).