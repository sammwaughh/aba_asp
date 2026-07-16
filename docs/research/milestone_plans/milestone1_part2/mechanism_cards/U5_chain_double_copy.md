# U5 — Chain + double copy

**Unit ID:** U5  
**Fixture id (proposed):** `m12_u5_chain_double_copy`  
**Lesson:** Parent vs ancestor cut; when learning the intermediate, a **descendant stays in BK** as a distractor  
**Provenance:** Redesigned pilot `m12_chain` under the Approach regime  
**Cells:** 4 — each of \(\{x_1,x_2\}\) × {ECAI, AAMAS}

---

## 1. Graph

| | |
|--|--|
| **Nodes \(V\)** | \(\{x_0,x_1,x_2\}\) |
| **Edges \(E\)** | \(x_0 \to x_1\), \(x_1 \to x_2\) |
| **Sources \(S\)** | \(\{x_0\}\) |
| **Non-sources \(N\)** | \(\{x_1,x_2\}\) |

```text
x0 ----→ x1 ----→ x2
```

---

## 2. Alphabet and mechanisms

- \(K=\{0,1,2\}\) for every variable.
- \(x_1 := \operatorname{copy}(x_0)\)
- \(x_2 := \operatorname{copy}(x_1)\)

Boolean nonzero sketch: \(\Phi_{x_1}=\Phi_{x_2}=z_0\). On \(\mathcal{D}\),
\(x_0=x_1=x_2\) in every row (perfect extensional tie along the chain).

---

## 3. Data \(\mathcal{D}\)

**Generation:** full source factorial over \(K^{|S|}\) (\(3^1=3\) rows), then propagate
in topological order. Sample ids are 1-based.

| id | \(x_0\) | \(x_1=\operatorname{copy}(x_0)\) | \(x_2=\operatorname{copy}(x_1)\) |
|---:|--------:|--------------------------------:|--------------------------------:|
| 1 | 0 | 0 | 0 |
| 2 | 1 | 1 | 1 |
| 3 | 2 | 2 | 2 |

No duplicate rows.

---

## 4. Target \(t = x_1\) (intermediate — descendant distractor cell)

### 4.1 Structural sets

| Set | Members | Role |
|-----|---------|------|
| Ancestors of \(t\) | \(\{x_0\}\) | May appear in a good rule |
| Other distractors (non-ancestor, non-descendant) | \(\emptyset\) | — |
| Descendants of \(t\) | \(\{x_2\}\) | **Included in BK as distractors**; citing them is an **explicit failure mode** |

### 4.2 Background knowledge

Exclude **only** \(x_1\). Include parent \(x_0\) **and descendant \(x_2\)**:

- `x0_val_*` + definitional `x0_nz`
- `x2_val_*` + definitional `x2_nz`

```prolog
x0_nz(A) :- x0_val_1(A).
x0_nz(A) :- x0_val_2(A).
x2_nz(A) :- x2_val_1(A).
x2_nz(A) :- x2_val_2(A).
```

**Do not** omit \(x_2\) from BK. The point of this cell is to test whether the learner
ignores the descendant.

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
**parent** \(x_0\), without rote sample-id casework, and **without citing the descendant
\(x_2\)** — even though \(x_2\) is extensionally equivalent on this table.

### 4.6 Divergences to watch

- Citing `x2_nz` / `x2_val_*` (**descendant failure mode**; may be extensionally correct on \(\mathcal{D}\)).
- Rote / sample-id rules.
- Missing the parent.

---

## 5. Target \(t = x_2\) (sink — parent vs ancestor)

### 5.1 Structural sets

| Set | Members | Role |
|-----|---------|------|
| Ancestors of \(t\) | \(\{x_0,x_1\}\) | Parent \(x_1\) preferred; grandparent \(x_0\) is also an ancestor |
| Other distractors (non-ancestor, non-descendant) | \(\emptyset\) | — |
| Descendants of \(t\) | \(\emptyset\) | (none; sink) |

### 5.2 Background knowledge

Exclude **only** \(x_2\). Include both ancestors:

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

On \(\mathcal{D}\): \(x_2\neq 0\) iff \(x_1\neq 0\) iff \(x_0\neq 0\).

### 5.4 Reference hypothesis \(\mathcal{H}_{x_2}^\star\)

Prefer the **direct parent**:

```prolog
x2(A) :- x1_nz(A).
```

**Note (parent vs ancestor):** `x2(A) :- x0_nz(A).` is extensionally correct on
\(\mathcal{D}\) but uses the grandparent rather than the parent. Treat that as a
parent-vs-ancestor divergence to inspect, not as the reference \(\mathcal{H}^\star\).

### 5.5 Semantic success (inspection)

An intensional, general rule that correctly characterises \(x_2\neq 0\) on \(\mathcal{D}\)
using ancestor information appropriately — ideally the direct parent \(x_1\) — without
rote sample-id casework. No descendants to cite.

### 5.6 Divergences to watch

- Grandparent-only rule (`x0_nz`) when parent is available (parent vs ancestor cut).
- Rote / sample-id rules.
- Empty / vacuous rules.

---

## 6. Non-collapse / relevance

Along the chain every variable is mechanism-defined and Boolean-tied to \(z_0\). The
lessons are structural: (i) when learning \(x_1\), **keep \(x_2\) in BK** and check
whether it is cited; (ii) when learning \(x_2\), prefer parent over grandparent under
perfect correlation.

---

## 7. Cells

| Cell | Fixture | Target | Config |
|------|---------|--------|--------|
| U5-x1-ECAI | U5 | \(x_1\) | ECAI |
| U5-x1-AAMAS | U5 | \(x_1\) | AAMAS |
| U5-x2-ECAI | U5 | \(x_2\) | ECAI |
| U5-x2-AAMAS | U5 | \(x_2\) | AAMAS |

Inspection order (Approach): nearer sources first — inspect \(x_1\) cells before \(x_2\).
