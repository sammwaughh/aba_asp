# U7 — Diamond + noisy fork arms

**Unit ID:** U7  
**Fixture id:** `m12_u7_g1_or_cone`  
**Lesson:** Both-parent sink recovery when \(\mathrm{Pa}(x_3)=\{x_1,x_2\}\) are **correlated siblings** under a common cause; root and each sibling alone are imperfect separators (U5-style curated “noisy” arms)  
**Provenance:** Fresh U7 (2026-07-20). Replaces G1 double-max / OR cone. Fixture key kept for path stability.  
**Cells:** 2 — `(U7, x3, ECAI)`, `(U7, x3, AAMAS)`

---

## 1. Graph (diamond)

| | |
|--|--|
| **Nodes \(V\)** | \(\{x_0,x_1,x_2,x_3\}\) |
| **Edges \(E\)** | \(x_0\to x_1\), \(x_0\to x_2\), \(x_1\to x_3\), \(x_2\to x_3\) |
| **Sources \(S\)** | \(\{x_0\}\) |
| **Non-sources \(N\)** | \(\{x_1,x_2,x_3\}\) (learning target: \(x_3\) only) |

```text
      x1
     ↗  ↘
   x0      x3
     ↘  ↗
      x2
```

Parents: \(\mathrm{Pa}(x_1)=\{x_0\}\), \(\mathrm{Pa}(x_2)=\{x_0\}\), \(\mathrm{Pa}(x_3)=\{x_1,x_2\}\).

---

## 2. Alphabet and mechanisms

- \(K=\{0,1,2\}\) for every variable.
- **Curated support (not full source factorial; not single-valued in \(x_0\)):**  
  for each \(x_0\in K\),
  - \(x_1 := (x_0+1)\bmod 3\)
  - two rows for \(x_2\): \((x_0+2)\bmod 3\) (“siblings differ”) and \(x_1\) (“siblings collapse”)
- \(x_3 := |x_1-x_2|\)

On \(\mathcal{D}\): \(x_3\neq 0\) iff \(x_1\neq x_2\). Same \(x_0\) appears on both a positive and a negative row, so no `x0_val_*` union separates \(E^\pm\). Neither sibling alone separates; both parents are required.

---

## 3. Data \(\mathcal{D}\)

**Generation:** for \(x_0\in\{0,1,2\}\) in order, emit the differ row then the collapse row; then \(x_3=|x_1-x_2|\). Sample ids are 1-based.

| id | \(x_0\) | \(x_1\) | \(x_2\) | \(x_3=\|x_1-x_2\|\) |
|---:|--------:|--------:|--------:|-------------------:|
| 1 | 0 | 1 | 2 | 1 |
| 2 | 0 | 1 | 1 | 0 |
| 3 | 1 | 2 | 0 | 2 |
| 4 | 1 | 2 | 2 | 0 |
| 5 | 2 | 0 | 1 | 1 |
| 6 | 2 | 0 | 0 | 0 |

No duplicate full rows.

---

## 4. Target \(t = x_3\) (sink)

### 4.1 Structural sets

| Set | Members | Role |
|-----|---------|------|
| Ancestors of \(t\) | \(\{x_0,x_1,x_2\}\) | Parents \(\{x_1,x_2\}\); \(x_0\) is non-parent ancestor (common cause) |
| Other distractors (non-ancestor, non-descendant) | \(\emptyset\) | — |
| Descendants of \(t\) | \(\emptyset\) | (none; sink) |

### 4.2 Background knowledge

Exclude **only** \(x_3\). Include:

- `x0_val_0`, `x0_val_1`, `x0_val_2`
- `x1_val_0`, `x1_val_1`, `x1_val_2`
- `x2_val_0`, `x2_val_1`, `x2_val_2`

No `*_nz` predicates.

### 4.3 Labels

| | Definition on \(\mathcal{D}\) | Row ids |
|--|------------------------------|---------|
| \(E^+\) | \(x_3 \neq 0\) | 1, 3, 5 |
| \(E^-\) | \(x_3 = 0\) | 2, 4, 6 |

On \(\mathcal{D}\): \(x_3\neq 0\) iff \(x_1\neq x_2\).

**Separation contract:**

| Predictor set | Perfect `val`-union separator of \(E^\pm\)? |
|---------------|--------------------------------------------|
| \(\{x_0\}\) | No (each \(x_0\) on one pos and one neg) |
| \(\{x_1\}\) | No |
| \(\{x_2\}\) | No |
| \(\{x_1,x_2\}\) | Yes |

### 4.4 Reference hypothesis \(\mathcal{H}_{x_3}^\star\)

```prolog
x3(A) :- x1_val_1(A), x2_val_2(A).
x3(A) :- x1_val_2(A), x2_val_0(A).
x3(A) :- x1_val_0(A), x2_val_1(A).
```

### 4.5 Semantic success (inspection)

An intensional both-parent characterisation of \(x_1\neq x_2\), without rote sample-id
casework, and without substituting the common cause \(x_0\) for the sibling parents.

### 4.6 Divergences to watch

- Single-sibling rules.
- Root-only / root-contaminated rules.
- Rote / sample-id rules.

---

## 5. Non-collapse / relevance

U5-style multi-row support per \(x_0\) blocks the 3-row factorial escape
(`x0_val_*` case-split). The scientific gap filled vs U2/U3/U4/U6: **both-parent
recovery when parents are fork-correlated siblings**.

---

## 6. Cells

| Cell | Fixture | Target | Config |
|------|---------|--------|--------|
| U7-x3-ECAI | U7 | \(x_3\) | ECAI |
| U7-x3-AAMAS | U7 | \(x_3\) | AAMAS |
