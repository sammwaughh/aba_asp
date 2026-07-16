# Expanded M1.2 — Accepted unit set

**Role:** frozen list of \((G,\{f_y\})\) units to turn into mechanism cards, then implement.  
**Status:** accepted 2026-07-16  
**Approach:** [`milestone1_part2_expanded_approach.md`](milestone1_part2_expanded_approach.md)  
**Primary path:** [`../milestone1_high_level_path.md`](../milestone1_high_level_path.md)

**Unit** = graph + full mechanism assignment on every non-source.  
Targets, \(\mathcal{D}\), BK predictor sets, and \(\mathcal{H}_t^\star\) are derived from the unit (see Approach).

Do not add or drop units without updating this file and the Approach lock status.

---

## Inclusion gate (summary)

Include only if: distinct lesson; inspectable (\(|S|\le 2\) preferred); non-collapse under copy/min/max; portfolio coverage; pilot continuity; Fabrizio only when earned; no near-duplicates; relevant failure modes; honest cell cost.

---

## Accepted units (core)

Alphabet \(k=3\) always. Configs: ECAI, AAMAS. Cells per unit \(= 2\times|N|\).

### U1 — Separator + copy

| | |
|--|--|
| **Graph** | \(x_1 \to x_2\); \(x_0\) isolated (no incident edges) |
| **Sources \(S\)** | \(\{x_0,x_1\}\) → 9 rows |
| **Mechanisms** | \(x_2 := \operatorname{copy}(x_1)\) |
| **Targets \(N\)** | \(\{x_2\}\) |
| **Lesson** | Unique parent/copy with an isolated distractor |
| **Cells** | 2 |
| **Provenance** | Redesigned pilot `m12_sep` |

### U2 — Collider + min

| | |
|--|--|
| **Graph** | \(x_0 \to x_2 \leftarrow x_1\) |
| **Sources \(S\)** | \(\{x_0,x_1\}\) → 9 rows |
| **Mechanisms** | \(x_2 := \min(x_0,x_1)\) |
| **Targets \(N\)** | \(\{x_2\}\) |
| **Lesson** | Conjunctive / AND nonzero rule |
| **Cells** | 2 |
| **Provenance** | Redesigned pilot `m12_conj` (same graph as U3) |

### U3 — Collider + max

| | |
|--|--|
| **Graph** | Same as U2: \(x_0 \to x_2 \leftarrow x_1\) |
| **Sources \(S\)** | \(\{x_0,x_1\}\) → 9 rows |
| **Mechanisms** | \(x_2 := \max(x_0,x_1)\) |
| **Targets \(N\)** | \(\{x_2\}\) |
| **Lesson** | Disjunctive / OR nonzero rule |
| **Cells** | 2 |
| **Provenance** | Redesigned pilot `m12_disj` |

### U4 — Fork + double copy

| | |
|--|--|
| **Graph** | \(x_0 \to x_1\), \(x_0 \to x_2\) |
| **Sources \(S\)** | \(\{x_0\}\) → 3 rows |
| **Mechanisms** | \(x_1 := \operatorname{copy}(x_0)\), \(x_2 := \operatorname{copy}(x_0)\) |
| **Targets \(N\)** | \(\{x_1,x_2\}\) |
| **Lesson** | Sibling distractor when sibling is extensionally tied to the parent |
| **Cells** | 4 |
| **Provenance** | Redesigned pilot `m12_fork` (old asymmetric map dropped; not copy/min/max) |

### U5 — Chain + double copy

| | |
|--|--|
| **Graph** | \(x_0 \to x_1 \to x_2\) |
| **Sources \(S\)** | \(\{x_0\}\) → 3 rows |
| **Mechanisms** | \(x_1 := \operatorname{copy}(x_0)\), \(x_2 := \operatorname{copy}(x_1)\) |
| **Targets \(N\)** | \(\{x_1,x_2\}\) |
| **Lesson** | Parent vs ancestor cut; depth so descendant distractors appear in BK when learning intermediates |
| **Cells** | 4 |
| **Provenance** | Redesigned pilot `m12_chain` |

### U6 — Fabrizio G1 + AND cone

| | |
|--|--|
| **Graph (G1)** | \(0\to 2\), \(1\to 2\), \(1\to 3\), \(2\to 3\) |
| **Sources \(S\)** | \(\{0,1\}\) → 9 rows |
| **Mechanisms** | \(x_2 := \min(x_0,x_1)\), \(x_3 := \min(x_1,x_2)\) |
| **Targets \(N\)** | \(\{x_2,x_3\}\) |
| **Boolean** | \(\Phi_{x_2}=\Phi_{x_3}=z_0\land z_1\) (sources remain relevant) |
| **Lesson** | Fabrizio 4-node; intermediate on a two-level AND |
| **Cells** | 4 |
| **Provenance** | `ArgCausalDisco/tests.py` — `four_node_shapPC_example` / README four-node example |

### U7 — Fabrizio G1 + OR cone

| | |
|--|--|
| **Graph** | Same G1 as U6 |
| **Sources \(S\)** | \(\{0,1\}\) → 9 rows |
| **Mechanisms** | \(x_2 := \max(x_0,x_1)\), \(x_3 := \max(x_1,x_2)\) |
| **Targets \(N\)** | \(\{x_2,x_3\}\) |
| **Boolean** | \(\Phi_{x_2}=\Phi_{x_3}=z_0\lor z_1\) |
| **Lesson** | Fabrizio 4-node; intermediate on a two-level OR |
| **Cells** | 4 |
| **Provenance** | Same G1 as U6 |

---

## Summary table

| ID | Graph | Mechanisms | \|S\| | rows | \|N\| | cells |
|----|-------|------------|-----:|-----:|-----:|------:|
| U1 | sep (+ isolated \(x_0\)) | \(x_2=\mathrm{copy}(x_1)\) | 2 | 9 | 1 | 2 |
| U2 | collider | \(x_2=\min\) | 2 | 9 | 1 | 2 |
| U3 | collider | \(x_2=\max\) | 2 | 9 | 1 | 2 |
| U4 | fork | \(x_1=\mathrm{copy}(x_0),\ x_2=\mathrm{copy}(x_0)\) | 1 | 3 | 2 | 4 |
| U5 | chain | \(x_1=\mathrm{copy}(x_0),\ x_2=\mathrm{copy}(x_1)\) | 1 | 3 | 2 | 4 |
| U6 | Fabrizio G1 | \(x_2=\min,\ x_3=\min\) | 2 | 9 | 2 | 4 |
| U7 | Fabrizio G1 | \(x_2=\max,\ x_3=\max\) | 2 | 9 | 2 | 4 |

**Total: 7 units, 22 cells.**

---

## Explicitly excluded (do not card unless the set is revised)

| Candidate | Why |
|-----------|-----|
| G1 with mixed min/max | Non-collapse fails: \(\Phi_{x_3}\) ignores a source |
| G1a / G1c / G1d | No new Boolean lesson beyond U6/U7 for this wave |
| G3 sprinkler | Single source + unary copy only ⇒ Boolean-trivial under Approach toolkit |
| G4 Colombo / G5 six-node | Poor inspectability vs lesson gained |
| Path-mixed stretch (\(\|S\|=3\)) | Deferred; min/max already covered across U2/U3/U6/U7 |
| Pilot fork asymmetric map | Not copy/min/max; replaced by U4 |

---

## Mechanism cards

**Written:** [`mechanism_cards/`](mechanism_cards/) (U1–U7 + README).

Each card includes: provenance; nodes/edges/\(S\)/\(N\); every \(f_y\); full \(\mathcal{D}\);
per-target ancestors / other distractors / **descendant distractors (included in BK)**;
\(E^\pm\); \(\mathcal{H}_t^\star\); semantic success description; non-collapse note.

---

## Status

| Item | Status |
|------|--------|
| Approach | Locked |
| Unit set (this file) | **Accepted** |
| Mechanism cards U1–U7 | **Written** — [`mechanism_cards/`](mechanism_cards/) |
| Fixtures + grid (M12x) | **Constructed** — ready to run |
| Learning runs / inspection | Next |
