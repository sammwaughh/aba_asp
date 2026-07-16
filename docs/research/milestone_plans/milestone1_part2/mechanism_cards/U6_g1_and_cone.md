# U6 — Fabrizio G1 + AND cone

**Unit ID:** U6  
**Fixture id (proposed):** `m12_u6_g1_and_cone`  
**Lesson:** Fabrizio 4-node DAG; intermediate on a two-level AND; descendant distractor when learning \(x_2\)  
**Provenance (graph):** `ArgCausalDisco/tests.py` — `four_node_shapPC_example` / README four-node example (edge set G1). **Mechanisms and DGP are project-chosen**, not from ArgCausalDisco.  
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

Parents: \(\mathrm{Pa}(x_2)=\{x_0,x_1\}\), \(\mathrm{Pa}(x_3)=\{x_1,x_2\}\).

---

## 2. Alphabet and mechanisms

- \(K=\{0,1,2\}\) for every variable.
- \(x_2 := \min(x_0,x_1)\)
- \(x_3 := \min(x_1,x_2)\)

Boolean nonzero sketch (unit set): \(\Phi_{x_2}=\Phi_{x_3}=z_0\land z_1\).
Both sources remain Boolean-relevant for both targets.

**Composition identity on \(\mathcal{D}\):**  
\(\min(x_1,\min(x_0,x_1))=\min(x_0,x_1)\), so \(x_3=x_2\) in every row under this
mechanism assignment. That is expected; it makes the descendant distractor
extensionally strong when learning \(x_2\).

---

## 3. Data \(\mathcal{D}\)

**Generation:** full source factorial over \(K^{|S|}\) (\(3^2=9\) rows), then propagate
in topological order (\(x_2\) then \(x_3\)). Sample ids are 1-based.

| id | \(x_0\) | \(x_1\) | \(x_2=\min(x_0,x_1)\) | \(x_3=\min(x_1,x_2)\) |
|---:|--------:|--------:|---------------------:|---------------------:|
| 1 | 0 | 0 | 0 | 0 |
| 2 | 0 | 1 | 0 | 0 |
| 3 | 0 | 2 | 0 | 0 |
| 4 | 1 | 0 | 0 | 0 |
| 5 | 1 | 1 | 1 | 1 |
| 6 | 1 | 2 | 1 | 1 |
| 7 | 2 | 0 | 0 | 0 |
| 8 | 2 | 1 | 1 | 1 |
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

**Critical:** \(x_3\) **must** appear in BK when learning \(x_2\). Omitting it would make
the descendant-citation failure mode untestable.

### 4.3 Labels

| | Definition on \(\mathcal{D}\) | Row ids |
|--|------------------------------|---------|
| \(E^+\) | \(x_2 \neq 0\) | 5, 6, 8, 9 (4 rows) |
| \(E^-\) | \(x_2 = 0\) | 1, 2, 3, 4, 7 (5 rows) |

On \(\mathcal{D}\): \(x_2\neq 0\) iff \(x_0\neq 0\) and \(x_1\neq 0\)  
(and iff \(x_3\neq 0\), by the composition identity).

### 4.4 Reference hypothesis \(\mathcal{H}_{x_2}^\star\)

```prolog
x2(A) :- x0_nz(A), x1_nz(A).
```

### 4.5 Semantic success (inspection)

An intensional, general AND-of-parents rule for \(x_2\neq 0\), without rote sample-id
casework, and **without citing descendant \(x_3\)** — even though \(x_3\) is
extensionally identical to \(x_2\) on \(\mathcal{D}\).

### 4.6 Divergences to watch

- Citing `x3_nz` / `x3_val_*` (**descendant failure mode**).
- OR-style / single-parent rules (wrong for min).
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
| \(E^+\) | \(x_3 \neq 0\) | 5, 6, 8, 9 (4 rows) |
| \(E^-\) | \(x_3 = 0\) | 1, 2, 3, 4, 7 (5 rows) |

On \(\mathcal{D}\): \(x_3\neq 0\) iff \(x_1\neq 0\) and \(x_2\neq 0\)  
(equivalently iff \(x_0\neq 0\) and \(x_1\neq 0\)).

### 5.4 Reference hypothesis \(\mathcal{H}_{x_3}^\star\)

Mechanism-derived (parents of \(x_3\)):

```prolog
x3(A) :- x1_nz(A), x2_nz(A).
```

**Note:** `x3(A) :- x0_nz(A), x1_nz(A).` is extensionally equivalent on \(\mathcal{D}\)
(Boolean \(\Phi_{x_3}=z_0\land z_1\)). Prefer the parent-based form as \(\mathcal{H}^\star\);
record source-level AND as an alternative intensional form to inspect if recovered.

### 5.5 Semantic success (inspection)

An intensional, general rule that correctly characterises \(x_3\neq 0\) on \(\mathcal{D}\)
using ancestor / parent information appropriately (conjunction), without rote sample-id
casework. No descendants to cite.

### 5.6 Divergences to watch

- OR-style rules (wrong for min).
- Rules that drop a needed conjunct and cover negatives.
- Rote / sample-id rules.

---

## 6. Non-collapse / relevance

Under this **homogeneous min/min** assignment, \(\Phi_{x_2}=\Phi_{x_3}=z_0\land z_1\):
both sources remain Boolean-relevant for both targets.  
**Contrast (excluded from unit set):** mixed min/max on G1 can make \(\Phi_{x_3}\) ignore
a source — that collapse is why mixed G1 is not carded.

The equality \(x_3=x_2\) on \(\mathcal{D}\) does **not** justify removing \(x_3\) from BK
when learning \(x_2\); it strengthens the descendant-distractor test.

---

## 7. Cells

| Cell | Fixture | Target | Config |
|------|---------|--------|--------|
| U6-x2-ECAI | U6 | \(x_2\) | ECAI |
| U6-x2-AAMAS | U6 | \(x_2\) | AAMAS |
| U6-x3-ECAI | U6 | \(x_3\) | ECAI |
| U6-x3-AAMAS | U6 | \(x_3\) | AAMAS |

Inspection order: \(x_2\) (nearer sources) before \(x_3\) (sink).
