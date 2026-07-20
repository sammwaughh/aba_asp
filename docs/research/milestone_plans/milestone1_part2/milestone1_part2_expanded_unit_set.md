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
| **Lesson** | Conjunctive / both parents nonzero (min; `val` \(\mathcal{H}^\star\)) |
| **Cells** | 2 |
| **Provenance** | Redesigned pilot `m12_conj` (same graph as U3) |

### U3 — Collider + max

| | |
|--|--|
| **Graph** | Same as U2: \(x_0 \to x_2 \leftarrow x_1\) |
| **Sources \(S\)** | \(\{x_0,x_1\}\) → 9 rows |
| **Mechanisms** | \(x_2 := \max(x_0,x_1)\) |
| **Targets \(N\)** | \(\{x_2\}\) |
| **Lesson** | Disjunctive / either parent nonzero (max; `val` \(\mathcal{H}^\star\)) |
| **Cells** | 2 |
| **Provenance** | Redesigned pilot `m12_disj` |

### U4 — Fork + asymmetric maps

| | |
|--|--|
| **Graph** | \(x_0 \to x_1\), \(x_0 \to x_2\) |
| **Sources \(S\)** | \(\{x_0\}\) → 3 rows |
| **Mechanisms** | \(x_1 := 2\cdot\mathbf{1}_{x_0\neq 2}\), \(x_2 := 2\cdot\mathbf{1}_{x_0\neq 0}\) |
| **Targets \(N\)** | \(\{x_1,x_2\}\) |
| **Lesson** | Parent vs sibling distractor (sibling correlated but imperfect separator) |
| **Cells** | 4 |
| **Provenance** | Option B redesign of pilot `m12_fork` (2026-07-20) |

### U5 — Chain + correlated ancestor (pilot)

| | |
|--|--|
| **Graph** | \(x_0 \to x_1 \to x_2\) |
| **Sources \(S\)** | \(\{x_0\}\) (curated support; not full factorial) → 6 rows |
| **Mechanisms** | Pilot \((x_0,x_1)\) pairs; \(x_2 := \operatorname{copy}(x_1)\) |
| **Targets \(N\)** | \(\{x_1,x_2\}\) |
| **Lesson** | Parent vs correlated ancestor (sink); descendant-in-BK when learning intermediate |
| **Cells** | 4 |
| **Provenance** | Restored pilot `m12_chain` (2026-07-20); nonzero-positive; `val`-only |

### U6 — Fabrizio G1 + min then difference

| | |
|--|--|
| **Graph (G1)** | \(0\to 2\), \(1\to 2\), \(1\to 3\), \(2\to 3\) |
| **Sources \(S\)** | \(\{0,1\}\) → 9 rows |
| **Mechanisms** | \(x_2 := \min(x_0,x_1)\), \(x_3 := x_1-x_2\) |
| **Targets \(N\)** | \(\{x_2,x_3\}\) |
| **Lesson** | Intermediate min (U2-style); sink \(x_3\neq 0\iff x_1>x_2\) needs both parents; imperfect descendant distractor |
| **Cells** | 4 |
| **Provenance** | G1 graph from ArgCausalDisco; mechanisms redesigned 2026-07-20 |

### U7 — Diamond + noisy fork arms

| | |
|--|--|
| **Graph** | \(x_0\to x_1\), \(x_0\to x_2\), \(x_1\to x_3\), \(x_2\to x_3\) |
| **Sources \(S\)** | \(\{x_0\}\) (curated multi-row support) → 6 rows |
| **Mechanisms** | For each \(x_0\): \(x_1:=(x_0+1)\bmod 3\); \(x_2\in\{(x_0+2)\bmod 3,\,x_1\}\); \(x_3:=\|x_1-x_2\|\) |
| **Targets \(N\)** | \(\{x_3\}\) |
| **Lesson** | Both-parent sink under correlated siblings; root/sibling alone imperfect |
| **Cells** | 2 |
| **Provenance** | Fresh U7 (2026-07-20); replaces G1 OR cone |

---

## Summary table

| ID | Graph | Mechanisms | \|S\| | rows | \|N\| | cells |
|----|-------|------------|-----:|-----:|-----:|------:|
| U1 | sep (+ isolated \(x_0\)) | \(x_2=\mathrm{copy}(x_1)\) | 2 | 9 | 1 | 2 |
| U2 | collider | \(x_2=\min\) | 2 | 9 | 1 | 2 |
| U3 | collider | \(x_2=\max\) | 2 | 9 | 1 | 2 |
| U4 | fork | \(x_1=2\cdot 1_{x_0\neq 2},\ x_2=2\cdot 1_{x_0\neq 0}\) | 1 | 3 | 2 | 4 |
| U5 | chain | pilot \((x_0,x_1)\) support; \(x_2=\mathrm{copy}(x_1)\) | 1 | 6 | 2 | 4 |
| U6 | Fabrizio G1 | \(x_2=\min,\ x_3=x_1-x_2\) | 2 | 9 | 2 | 4 |
| U7 | diamond | noisy fork arms; \(x_3=\|x_1-x_2\|\) | 1 | 6 | 1 | 2 |

**Total: 7 units, 20 cells.**

---

## Explicitly excluded (do not card unless the set is revised)

| Candidate | Why |
|-----------|-----|
| G1 with mixed min/max | Algebraic projection \(x_3=x_1\); superseded by U6 difference sink |
| G1 double min/max | \(x_3=x_2\) collapse; superseded by U6 redesign |
| G1 OR cone / max-then-difference U7 | Semantic overlap with U3/U6; superseded by diamond U7 |
| G1a / G1c / G1d | No new Boolean lesson beyond U6 for this wave |
| G3 sprinkler | Single source + unary copy only ⇒ Boolean-trivial under Approach toolkit |
| G4 Colombo / G5 six-node | Poor inspectability vs lesson gained |
| Path-mixed stretch (\(\|S\|=3\)) | Deferred; min/max already covered across U2/U3/U6 |
| Pilot fork asymmetric map | Superseded by U4 Option B overlapping supports |
| Chain double copy (3-row tie) | Superseded by U5 pilot correlated-ancestor support |

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
| Fixtures + grid (M12x) | Constructed |
| Learning runs | Done — 22/22 solved |
| Inspection vs \(\mathcal{H}^\star\) | **Done** — `M1.2-expanded-cell-inspection.md` |
