# U7 — Fabrizio G1 + OR cone

**Unit ID:** U7  
**Fixture id (proposed):** `m12_u7_g1_or_cone`  
**Lesson:** Fabrizio 4-node DAG; intermediate on a two-level OR; descendant distractor when learning \(x_2\)  
**Provenance (graph):** Same G1 as U6 — `ArgCausalDisco/tests.py` — `four_node_shapPC_example` / README four-node example. **Mechanisms and DGP are project-chosen.**  
**Cells:** 4 — each of \(\{x_2,x_3\}\) × {ECAI, AAMAS}

---

## 1. Graph (Fabrizio G1)

| | |
|--|--|
| **Nodes \(V\)** | \(\{x_0,x_1,x_2,x_3\}\) (indices \(0,1,2,3\)) |
| **Edges \(E\)** | \(x_0\to x_2\), \(x_1\to x_2\), \(x_1\to x_3\), \(x_2\to x_3\) |
| **Sources \(S\)** | \(\{x_0,x_1\}\) |
| **Non-sources \(N\)** | \(\{x_2,x_3\}\) |

```text
x0 ----→ x2 ----→ x3
         ↗         ↗
       x1 --------┘
```

Same edge set as U6; mechanism differs (max vs min).

---

## 2. Alphabet and mechanisms

- \(K=\{0,1,2\}\) for every variable.
- \(x_2 := \max(x_0,x_1)\)
- \(x_3 := \max(x_1,x_2)\)

Boolean nonzero sketch (unit set): \(\Phi_{x_2}=\Phi_{x_3}=z_0\lor z_1\).

**Composition identity on \(\mathcal{D}\):**  
\(\max(x_1,\max(x_0,x_1))=\max(x_0,x_1)\), so \(x_3=x_2\) in every row under this
mechanism assignment. Descendant distractor is again extensionally strong when learning
\(x_2\).

---

## 3. Data \(\mathcal{D}\)

**Generation:** full source factorial over \(K^{|S|}\) (\(3^2=9\) rows), then propagate
in topological order (\(x_2\) then \(x_3\)). Sample ids are 1-based.

| id | \(x_0\) | \(x_1\) | \(x_2=\max(x_0,x_1)\) | \(x_3=\max(x_1,x_2)\) |
|---:|--------:|--------:|---------------------:|---------------------:|
| 1 | 0 | 0 | 0 | 0 |
| 2 | 0 | 1 | 1 | 1 |
| 3 | 0 | 2 | 2 | 2 |
| 4 | 1 | 0 | 1 | 1 |
| 5 | 1 | 1 | 1 | 1 |
| 6 | 1 | 2 | 2 | 2 |
| 7 | 2 | 0 | 2 | 2 |
| 8 | 2 | 1 | 2 | 2 |
| 9 | 2 | 2 | 2 | 2 |

Check: \(x_3=x_2\) on every row. No duplicate full rows.

---

## 4. Target \(t = x_2\) (intermediate — descendant \(x_3\) in BK)

### 4.1 Structural sets

| Set | Members | Role |
|-----|---------|------|
| Ancestors of \(t\) | \(\{x_0,x_1\}\) | May appear in a good rule |
| Other distractors (non-ancestor, non-descendant) | \(\emptyset\) | — |
| Descendants of \(t\) | \(\{x_3\}\) | **Included in BK as distractors**; citing them is an **explicit failure mode** |

### 4.2 Background knowledge

Exclude **only** \(x_2\). Include ancestors **and descendant \(x_3\)**:

- `x0_val_*` + definitional `x0_nz`
- `x1_val_*` + definitional `x1_nz`
- `x3_val_*` + definitional `x3_nz`

```prolog
x0_nz(A) :- x0_val_1(A).
x0_nz(A) :- x0_val_2(A).
x1_nz(A) :- x1_val_1(A).
x1_nz(A) :- x1_val_2(A).
x3_nz(A) :- x3_val_1(A).
x3_nz(A) :- x3_val_2(A).
```

**Critical:** \(x_3\) **must** appear in BK when learning \(x_2\).

### 4.3 Labels

| | Definition on \(\mathcal{D}\) | Row ids |
|--|------------------------------|---------|
| \(E^+\) | \(x_2 \neq 0\) | 2–9 (8 rows) |
| \(E^-\) | \(x_2 = 0\) | 1 only (1 row) |

On \(\mathcal{D}\): \(x_2\neq 0\) iff \(x_0\neq 0\) or \(x_1\neq 0\)  
(and iff \(x_3\neq 0\)).

### 4.4 Reference hypothesis \(\mathcal{H}_{x_2}^\star\)

```prolog
x2(A) :- x0_nz(A).
x2(A) :- x1_nz(A).
```

### 4.5 Semantic success (inspection)

An intensional, general OR-of-parents rule for \(x_2\neq 0\), without rote sample-id
casework, and **without citing descendant \(x_3\)** — even though \(x_3\) is
extensionally identical to \(x_2\) on \(\mathcal{D}\).

### 4.6 Divergences to watch

- Citing `x3_nz` / `x3_val_*` (**descendant failure mode**).
- AND-style / overly conjunctive rules (wrong for max; under-cover positives).
- Rote / sample-id rules.

---

## 5. Target \(t = x_3\) (sink)

### 5.1 Structural sets

| Set | Members | Role |
|-----|---------|------|
| Ancestors of \(t\) | \(\{x_0,x_1,x_2\}\) | Parents \(\{x_1,x_2\}\); \(x_0\) is also an ancestor via \(x_2\) |
| Other distractors (non-ancestor, non-descendant) | \(\emptyset\) | — |
| Descendants of \(t\) | \(\emptyset\) | (none; sink) |

### 5.2 Background knowledge

Exclude **only** \(x_3\). Include all other columns:

- `x0_val_*` + definitional `x0_nz`
- `x1_val_*` + definitional `x1_nz`
- `x2_val_*` + definitional `x2_nz`

```prolog
x0_nz(A) :- x0_val_1(A).
x0_nz(A) :- x0_val_2(A).
x1_nz(A) :- x1_val_1(A).
x1_nz(A) :- x1_val_2(A).
x2_nz(A) :- x2_val_1(A).
x2_nz(A) :- x2_val_2(A).
```

### 5.3 Labels

| | Definition on \(\mathcal{D}\) | Row ids |
|--|------------------------------|---------|
| \(E^+\) | \(x_3 \neq 0\) | 2–9 (8 rows) |
| \(E^-\) | \(x_3 = 0\) | 1 only (1 row) |

On \(\mathcal{D}\): \(x_3\neq 0\) iff \(x_1\neq 0\) or \(x_2\neq 0\)  
(equivalently iff \(x_0\neq 0\) or \(x_1\neq 0\)).

### 5.4 Reference hypothesis \(\mathcal{H}_{x_3}^\star\)

Mechanism-derived (parents of \(x_3\)):

```prolog
x3(A) :- x1_nz(A).
x3(A) :- x2_nz(A).
```

**Note:** the source-level OR

```prolog
x3(A) :- x0_nz(A).
x3(A) :- x1_nz(A).
```

is extensionally equivalent on \(\mathcal{D}\) (\(\Phi_{x_3}=z_0\lor z_1\)). Prefer the
parent-based form as \(\mathcal{H}^\star\); record source-level OR as an alternative to
inspect if recovered.

### 5.5 Semantic success (inspection)

An intensional, general rule that correctly characterises \(x_3\neq 0\) on \(\mathcal{D}\)
using ancestor / parent information appropriately (disjunction), without rote sample-id
casework. No descendants to cite.

### 5.6 Divergences to watch

- AND-style rules (wrong for max).
- Single literal that fails when only the other disjunct is nonzero (if that case arises under a bad rule shape).
- Rote / sample-id rules.

---

## 6. Non-collapse / relevance

Under this **homogeneous max/max** assignment, \(\Phi_{x_2}=\Phi_{x_3}=z_0\lor z_1\):
both sources remain Boolean-relevant. Same G1 graph as U6; OR vs AND is the contrast.
As in U6, \(x_3=x_2\) on \(\mathcal{D}\) strengthens the descendant-distractor test for
target \(x_2\) and does **not** justify removing \(x_3\) from BK.

---

## 7. Cells

| Cell | Fixture | Target | Config |
|------|---------|--------|--------|
| U7-x2-ECAI | U7 | \(x_2\) | ECAI |
| U7-x2-AAMAS | U7 | \(x_2\) | AAMAS |
| U7-x3-ECAI | U7 | \(x_3\) | ECAI |
| U7-x3-AAMAS | U7 | \(x_3\) | AAMAS |

Inspection order: \(x_2\) before \(x_3\).
