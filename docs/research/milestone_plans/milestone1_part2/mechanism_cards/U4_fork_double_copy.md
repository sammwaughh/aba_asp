# U4 — Fork + double copy

**Unit ID:** U4  
**Fixture id (proposed):** `m12_u4_fork_double_copy`  
**Lesson:** Sibling distractor when the sibling is extensionally tied to the parent  
**Provenance:** Redesigned pilot `m12_fork` under the Approach regime (old asymmetric map dropped; both children are copy)  
**Cells:** 4 — each of \(\{x_1,x_2\}\) × {ECAI, AAMAS}

---

## 1. Graph

| | |
|--|--|
| **Nodes \(V\)** | \(\{x_0,x_1,x_2\}\) |
| **Edges \(E\)** | \(x_0 \to x_1\), \(x_0 \to x_2\) |
| **Sources \(S\)** | \(\{x_0\}\) |
| **Non-sources \(N\)** | \(\{x_1,x_2\}\) |

```text
      x1
     ↗
   x0
     ↘
      x2
```

---

## 2. Alphabet and mechanisms

- \(K=\{0,1,2\}\) for every variable.
- \(x_1 := \operatorname{copy}(x_0)\)
- \(x_2 := \operatorname{copy}(x_0)\)

Boolean nonzero sketch: \(\Phi_{x_1}=\Phi_{x_2}=z_0\). On \(\mathcal{D}\),
\(x_0=x_1=x_2\) in every row (perfect extensional tie among parent and both children).

---

## 3. Data \(\mathcal{D}\)

**Generation:** full source factorial over \(K^{|S|}\) (\(3^1=3\) rows), then both copies.
Sample ids are 1-based.

| id | \(x_0\) | \(x_1=\operatorname{copy}(x_0)\) | \(x_2=\operatorname{copy}(x_0)\) |
|---:|--------:|--------------------------------:|--------------------------------:|
| 1 | 0 | 0 | 0 |
| 2 | 1 | 1 | 1 |
| 3 | 2 | 2 | 2 |

No duplicate rows. Small table: inspectability preferred over size.

---

## 4. Target \(t = x_1\)

### 4.1 Structural sets

| Set | Members | Role |
|-----|---------|------|
| Ancestors of \(t\) | \(\{x_0\}\) | May appear in a good rule |
| Other distractors (non-ancestor, non-descendant) | \(\{x_2\}\) | Sibling; **included in BK**; citing it is a divergence |
| Descendants of \(t\) | \(\emptyset\) | — |

### 4.2 Background knowledge

Exclude **only** \(x_1\). Include \(x_0\) and sibling \(x_2\):

- `x0_val_*` + definitional `x0_nz`
- `x2_val_*` + definitional `x2_nz`

```prolog
x0_nz(A) :- x0_val_1(A).
x0_nz(A) :- x0_val_2(A).
x2_nz(A) :- x2_val_1(A).
x2_nz(A) :- x2_val_2(A).
```

### 4.3 Labels

| | Definition on \(\mathcal{D}\) | Row ids |
|--|------------------------------|---------|
| \(E^+\) | \(x_1 \neq 0\) | 2, 3 |
| \(E^-\) | \(x_1 = 0\) | 1 |

On \(\mathcal{D}\): \(x_1\neq 0\) iff \(x_0\neq 0\) iff \(x_2\neq 0\).

### 4.4 Reference hypothesis \(\mathcal{H}_{x_1}^\star\)

```prolog
x1(A) :- x0_nz(A).
```

### 4.5 Semantic success (inspection)

An intensional, general rule that correctly characterises \(x_1\neq 0\) using the
**parent** \(x_0\), without rote sample-id casework, and **without citing the sibling
\(x_2\)** even though \(x_2\) is extensionally equivalent on this table.

### 4.6 Divergences to watch

- Citing `x2_nz` / `x2_val_*` (sibling distractor; may be extensionally correct on \(\mathcal{D}\)).
- Rote / sample-id rules.
- Missing the parent.

---

## 5. Target \(t = x_2\)

### 5.1 Structural sets

| Set | Members | Role |
|-----|---------|------|
| Ancestors of \(t\) | \(\{x_0\}\) | May appear in a good rule |
| Other distractors (non-ancestor, non-descendant) | \(\{x_1\}\) | Sibling; **included in BK**; citing it is a divergence |
| Descendants of \(t\) | \(\emptyset\) | — |

### 5.2 Background knowledge

Exclude **only** \(x_2\). Include \(x_0\) and sibling \(x_1\):

- `x0_val_*` + definitional `x0_nz`
- `x1_val_*` + definitional `x1_nz`

```prolog
x0_nz(A) :- x0_val_1(A).
x0_nz(A) :- x0_val_2(A).
x1_nz(A) :- x1_val_1(A).
x1_nz(A) :- x1_val_2(A).
```

### 5.3 Labels

| | Definition on \(\mathcal{D}\) | Row ids |
|--|------------------------------|---------|
| \(E^+\) | \(x_2 \neq 0\) | 2, 3 |
| \(E^-\) | \(x_2 = 0\) | 1 |

On \(\mathcal{D}\): \(x_2\neq 0\) iff \(x_0\neq 0\) iff \(x_1\neq 0\).

### 5.4 Reference hypothesis \(\mathcal{H}_{x_2}^\star\)

```prolog
x2(A) :- x0_nz(A).
```

### 5.5 Semantic success (inspection)

Symmetric to \(x_1\): characterise \(x_2\neq 0\) via parent \(x_0\), without citing sibling
\(x_1\), without rote sample-id casework.

### 5.6 Divergences to watch

- Citing `x1_nz` / `x1_val_*` (sibling).
- Rote / sample-id rules.
- Missing the parent.

---

## 6. Non-collapse / relevance

Both children are mechanism-defined copies of the unique source. The scientific point is
not Boolean collapse of a source, but **sibling distraction under perfect correlation**:
the sibling is a valid extensional separator on \(\mathcal{D}\) yet is not an ancestor.
Old pilot asymmetric fork map is out of scope (not copy/min/max).

---

## 7. Cells

| Cell | Fixture | Target | Config |
|------|---------|--------|--------|
| U4-x1-ECAI | U4 | \(x_1\) | ECAI |
| U4-x1-AAMAS | U4 | \(x_1\) | AAMAS |
| U4-x2-ECAI | U4 | \(x_2\) | ECAI |
| U4-x2-AAMAS | U4 | \(x_2\) | AAMAS |

Inspection order: either child first (symmetric); both are sinks relative to each other.
