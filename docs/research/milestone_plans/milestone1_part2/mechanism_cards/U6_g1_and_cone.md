# U6 — Fabrizio G1 + min then difference

**Unit ID:** U6  
**Fixture id:** `m12_u6_g1_and_cone`  
**Lesson:** Four-node G1; intermediate min (both parents); sink \(x_3\neq 0\iff x_1>x_2\) needs both \(\mathrm{Pa}(x_3)\); imperfect descendant distractor when learning \(x_2\)  
**Provenance (graph):** `ArgCausalDisco/tests.py` — `four_node_shapPC_example` / README four-node example (edge set G1). **Mechanisms and DGP are project-chosen**, not from ArgCausalDisco. Redesign 2026-07-20 (replace double-min collapse).  
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
- \(x_3 := x_1 - x_2\)

On \(\mathcal{D}\), \(x_2\le x_1\) always, so \(x_3\in\{0,1,2\}\). Nonzero sink labelling
is the strict inequality concept: \(x_3\neq 0\) iff \(x_1>x_2\). Neither parent alone
separates that concept; \(\mathcal{H}_{x_3}^\star\) needs both.

No double-min composition identity: \(x_3\not\equiv x_2\) and \(x_3\not\equiv x_1\).

---

## 3. Data \(\mathcal{D}\)

**Generation:** full source factorial over \(K^{|S|}\) (\(3^2=9\) rows), then propagate
in topological order (\(x_2\) then \(x_3\)). Sample ids are 1-based.

| id | \(x_0\) | \(x_1\) | \(x_2=\min(x_0,x_1)\) | \(x_3=x_1-x_2\) |
|---:|--------:|--------:|---------------------:|---------------:|
| 1 | 0 | 0 | 0 | 0 |
| 2 | 0 | 1 | 0 | 1 |
| 3 | 0 | 2 | 0 | 2 |
| 4 | 1 | 0 | 0 | 0 |
| 5 | 1 | 1 | 1 | 0 |
| 6 | 1 | 2 | 1 | 1 |
| 7 | 2 | 0 | 0 | 0 |
| 8 | 2 | 1 | 1 | 0 |
| 9 | 2 | 2 | 2 | 0 |

Rows with \(x_3\neq x_2\): 2, 3, 5, 6, 8, 9. No duplicate full rows.

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

- `x0_val_0`, `x0_val_1`, `x0_val_2`
- `x1_val_0`, `x1_val_1`, `x1_val_2`
- `x3_val_0`, `x3_val_1`, `x3_val_2`

No `*_nz` predicates.

**Critical:** \(x_3\) **must** appear in BK when learning \(x_2\).

### 4.3 Labels

| | Definition on \(\mathcal{D}\) | Row ids |
|--|------------------------------|---------|
| \(E^+\) | \(x_2 \neq 0\) | 5, 6, 8, 9 (4 rows) |
| \(E^-\) | \(x_2 = 0\) | 1, 2, 3, 4, 7 (5 rows) |

On \(\mathcal{D}\): \(x_2\neq 0\) iff \(x_0\neq 0\) and \(x_1\neq 0\).  
Descendant \(x_3\neq 0\) on ids 2, 3, 6 only — **imperfect** separator of \(E^\pm\).

### 4.4 Reference hypothesis \(\mathcal{H}_{x_2}^\star\)

```prolog
x2(A) :- x0_val_1(A), x1_val_1(A).
x2(A) :- x0_val_1(A), x1_val_2(A).
x2(A) :- x0_val_2(A), x1_val_1(A).
x2(A) :- x0_val_2(A), x1_val_2(A).
```

Same min/nonzero pattern as U2. Do not cite descendant \(x_3\).

### 4.5 Semantic success (inspection)

An intensional both-parents rule for \(x_2\neq 0\), without rote sample-id casework,
and **without citing descendant \(x_3\)**.

### 4.6 Divergences to watch

- Citing `x3_val_*` (**descendant failure mode**; imperfect on this table).
- Single-parent / OR-style rules (wrong for min).
- Rote / sample-id rules.

---

## 5. Target \(t = x_3\) (sink)

### 5.1 Structural sets

| Set | Members | Role |
|-----|---------|------|
| Ancestors of \(t\) | \(\{x_0,x_1,x_2\}\) | Parents \(\{x_1,x_2\}\); \(x_0\) is a non-parent ancestor via \(x_2\) |
| Other distractors (non-ancestor, non-descendant) | \(\emptyset\) | — |
| Descendants of \(t\) | \(\emptyset\) | (none; sink) |

### 5.2 Background knowledge

Exclude **only** \(x_3\). Include:

- `x0_val_0`, `x0_val_1`, `x0_val_2`
- `x1_val_0`, `x1_val_1`, `x1_val_2`
- `x2_val_0`, `x2_val_1`, `x2_val_2`

No `*_nz` predicates.

### 5.3 Labels

| | Definition on \(\mathcal{D}\) | Row ids |
|--|------------------------------|---------|
| \(E^+\) | \(x_3 \neq 0\) | 2, 3, 6 (3 rows) |
| \(E^-\) | \(x_3 = 0\) | 1, 4, 5, 7, 8, 9 (6 rows) |

On \(\mathcal{D}\): \(x_3\neq 0\) iff \(x_1>x_2\). Neither \(x_1\) alone nor \(x_2\) alone
is a perfect separator.

### 5.4 Reference hypothesis \(\mathcal{H}_{x_3}^\star\)

Parent-based case split of \(x_1>x_2\):

```prolog
x3(A) :- x1_val_1(A), x2_val_0(A).
x3(A) :- x1_val_2(A), x2_val_0(A).
x3(A) :- x1_val_2(A), x2_val_1(A).
```

Do not treat single-parent or \(x_0\)-only rules as \(\mathcal{H}^\star\).

### 5.5 Semantic success (inspection)

An intensional rule that characterises \(x_1>x_2\) using **both** parents \(x_1\) and
\(x_2\), without rote sample-id casework. Prefer parent scope over non-parent ancestor
\(x_0\).

### 5.6 Divergences to watch

- Single-parent rules (neither parent alone separates).
- Rules that drop a needed conjunct and cover negatives.
- Non-parent ancestor \(x_0\) contamination.
- Rote / sample-id rules.

---

## 6. Non-collapse / relevance

Difference avoids the double-min identity \(x_3=x_2\) and the alternating min/max
projection \(x_3=x_1\). Sink nonzero labelling is a genuine two-parent concept
(\(x_1>x_2\)). Intermediate retains the U2-style min lesson with an **imperfect**
descendant distractor.

---

## 7. Cells

| Cell | Fixture | Target | Config |
|------|---------|--------|--------|
| U6-x2-ECAI | U6 | \(x_2\) | ECAI |
| U6-x2-AAMAS | U6 | \(x_2\) | AAMAS |
| U6-x3-ECAI | U6 | \(x_3\) | ECAI |
| U6-x3-AAMAS | U6 | \(x_3\) | AAMAS |

Inspection order: \(x_2\) (nearer sources) before \(x_3\) (sink).
