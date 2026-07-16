# U2 — Collider + min

**Unit ID:** U2  
**Fixture id (proposed):** `m12_u2_collider_min`  
**Lesson:** Conjunctive / AND nonzero rule  
**Provenance:** Redesigned pilot `m12_conj` under the Approach regime (graph retained; DGP/labels/BK redesigned)  
**Cells:** 2 — `(U2, x2, ECAI)`, `(U2, x2, AAMAS)`

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

---

## 2. Alphabet and mechanisms

- \(K=\{0,1,2\}\) for every variable.
- \(x_2 := \min(x_0,x_1)\).

Boolean nonzero sketch: \(\Phi_{x_2}=z_0\land z_1\) (both parents nonzero).

---

## 3. Data \(\mathcal{D}\)

**Generation:** full source factorial over \(K^{|S|}\) (\(3^2=9\) rows), then
\(x_2=\min(x_0,x_1)\). Sample ids are 1-based in the order below.

| id | \(x_0\) | \(x_1\) | \(x_2=\min\) |
|---:|--------:|--------:|-------------:|
| 1 | 0 | 0 | 0 |
| 2 | 0 | 1 | 0 |
| 3 | 0 | 2 | 0 |
| 4 | 1 | 0 | 0 |
| 5 | 1 | 1 | 1 |
| 6 | 1 | 2 | 1 |
| 7 | 2 | 0 | 0 |
| 8 | 2 | 1 | 1 |
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

- `x0_val_0`, `x0_val_1`, `x0_val_2` and definitional `x0_nz`
- `x1_val_0`, `x1_val_1`, `x1_val_2` and definitional `x1_nz`

```prolog
x0_nz(A) :- x0_val_1(A).
x0_nz(A) :- x0_val_2(A).
x1_nz(A) :- x1_val_1(A).
x1_nz(A) :- x1_val_2(A).
```

### 4.3 Labels

| | Definition on \(\mathcal{D}\) | Row ids |
|--|------------------------------|---------|
| \(E^+\) | \(x_2 \neq 0\) | 5, 6, 8, 9 (4 rows) |
| \(E^-\) | \(x_2 = 0\) | 1, 2, 3, 4, 7 (5 rows) |

On \(\mathcal{D}\): \(x_2\neq 0\) iff \(x_0\neq 0\) and \(x_1\neq 0\).

### 4.4 Reference hypothesis \(\mathcal{H}_{x_2}^\star\)

```prolog
x2(A) :- x0_nz(A), x1_nz(A).
```

Compact `nz` form preferred. A correct `val`-expansion of the same conjunction is
extensionally acceptable but inferior.

### 4.5 Semantic success (inspection)

An intensional, general rule that correctly characterises \(x_2\neq 0\) on \(\mathcal{D}\)
as the conjunction of both parents being nonzero, without rote sample-id casework.
No descendants exist to cite on this sink fixture.

### 4.6 Divergences to watch

- Missing one parent (covers some negatives, or under-covers positives).
- Disjunctive / OR-style rule (wrong mechanism; would cover \(E^-\) rows where only one parent is nonzero).
- Rote / sample-id rules.
- Exact-value casework that fails to generalise the nonzero pattern.

---

## 5. Non-collapse / relevance

Both parents are needed for \(\Phi_{x_2}=z_0\land z_1\). Neither source is Boolean-irrelevant.
Same graph as U3; mechanism differs (min vs max).

---

## 6. Cells

| Cell | Fixture | Target | Config |
|------|---------|--------|--------|
| U2-ECAI | U2 | \(x_2\) | ECAI |
| U2-AAMAS | U2 | \(x_2\) | AAMAS |

Inspection order: only one target (sink).
