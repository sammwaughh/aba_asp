# U3 — Collider + max

**Unit ID:** U3  
**Fixture id:** `m12_u3_collider_max`  
**Lesson:** Disjunctive / either parent nonzero (max)  
**Provenance:** Redesigned pilot `m12_disj` under the Approach regime (graph retained; DGP/labels/BK redesigned)  
**Cells:** 2 — `(U3, x2, ECAI)`, `(U3, x2, AAMAS)`

---

## 1. Graph

| | |
|--|--|
| **Nodes \(V\)** | \(\{x_0,x_1,x_2\}\) |
| **Edges \(E\)** | \(x_0 \to x_2\), \(x_1 \to x_2\) |
| **Sources \(S\)** | \(\{x_0,x_1\}\) |
| **Non-sources \(N\)** | \(\{x_2\}\) |

```text
x0 ----→ x2 ←---- x1
```

Same edge set as U2; mechanism differs.

---

## 2. Alphabet and mechanisms

- \(K=\{0,1,2\}\) for every variable.
- \(x_2 := \max(x_0,x_1)\).

On \(\mathcal{D}\): \(x_2\neq 0\) iff at least one parent is nonzero.

---

## 3. Data \(\mathcal{D}\)

**Generation:** full source factorial over \(K^{|S|}\) (\(3^2=9\) rows), then
\(x_2=\max(x_0,x_1)\). Sample ids are 1-based in the order below.

| id | \(x_0\) | \(x_1\) | \(x_2=\max\) |
|---:|--------:|--------:|-------------:|
| 1 | 0 | 0 | 0 |
| 2 | 0 | 1 | 1 |
| 3 | 0 | 2 | 2 |
| 4 | 1 | 0 | 1 |
| 5 | 1 | 1 | 1 |
| 6 | 1 | 2 | 2 |
| 7 | 2 | 0 | 2 |
| 8 | 2 | 1 | 2 |
| 9 | 2 | 2 | 2 |

No duplicate rows. Sink fixture: no variables beyond \(x_2\).

---

## 4. Target \(t = x_2\)

### 4.1 Structural sets

| Set | Members | Role |
|-----|---------|------|
| Ancestors of \(t\) | \(\{x_0,x_1\}\) | May appear in a good rule |
| Other distractors (non-ancestor, non-descendant) | \(\emptyset\) | — |
| Descendants of \(t\) | \(\emptyset\) | (none; sink) |

### 4.2 Background knowledge

Exclude **only** \(x_2\). Include:

- `x0_val_0`, `x0_val_1`, `x0_val_2`
- `x1_val_0`, `x1_val_1`, `x1_val_2`

No `*_nz` predicates.

### 4.3 Labels

| | Definition on \(\mathcal{D}\) | Row ids |
|--|------------------------------|---------|
| \(E^+\) | \(x_2 \neq 0\) | 2–9 (8 rows) |
| \(E^-\) | \(x_2 = 0\) | 1 only (1 row) |

On \(\mathcal{D}\): \(x_2\neq 0\) iff \(x_0\neq 0\) or \(x_1\neq 0\).

### 4.4 Reference hypothesis \(\mathcal{H}_{x_2}^\star\)

```prolog
x2(A) :- x0_val_1(A).
x2(A) :- x0_val_2(A).
x2(A) :- x1_val_1(A).
x2(A) :- x1_val_2(A).
```

`val` expansion of “either parent nonzero” (no `*_nz` in BK).

### 4.5 Semantic success (inspection)

An intensional, general rule that correctly characterises \(x_2\neq 0\) on \(\mathcal{D}\)
as the disjunction of the two parents being nonzero, without rote sample-id casework.
No descendants exist to cite on this sink fixture.

### 4.6 Divergences to watch

- Conjunctive / AND-style rule (wrong mechanism; under-covers positives).
- Single-parent rule that fails on rows where only the other parent is nonzero.
- Rote / sample-id rules.

---

## 5. Non-collapse / relevance

Either parent being nonzero suffices. Both sources remain relevant (each alone can force
\(x_2\neq 0\)). Same graph as U2; mechanism differs.

---

## 6. Cells

| Cell | Fixture | Target | Config |
|------|---------|--------|--------|
| U3-ECAI | U3 | \(x_2\) | ECAI |
| U3-AAMAS | U3 | \(x_2\) | AAMAS |

Inspection order: only one target (sink).
