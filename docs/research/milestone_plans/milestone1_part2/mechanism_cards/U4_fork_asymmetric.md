# U4 — Fork + asymmetric maps

**Unit ID:** U4  
**Fixture id:** `m12_u4_fork_asymmetric`  
**Lesson:** Parent vs sibling distractor (sibling correlated but imperfect separator)  
**Provenance:** Redesigned from pilot `m12_fork`; Option B overlapping-support maps (2026-07-20)  
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
- \(x_1 := 2\) if \(x_0 \neq 2\), else \(0\)
- \(x_2 := 2\) if \(x_0 \neq 0\), else \(0\)

Parent is the unique perfect separator of each child’s nonzero labelling; the sibling is
associated via \(x_0\) but imperfect (same sibling value on a positive and a negative row).

---

## 3. Data \(\mathcal{D}\)

**Generation:** full source factorial over \(K^{|S|}\) (\(3^1=3\) rows), then both maps.
Sample ids are 1-based.

| id | \(x_0\) | \(x_1\) | \(x_2\) |
|---:|--------:|--------:|--------:|
| 1 | 0 | 2 | 0 |
| 2 | 1 | 2 | 2 |
| 3 | 2 | 0 | 2 |

No duplicate rows. No perfect tie among \(x_0\), \(x_1\), \(x_2\).

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

- `x0_val_0`, `x0_val_1`, `x0_val_2`
- `x2_val_0`, `x2_val_1`, `x2_val_2`


### 4.3 Labels

| | Definition on \(\mathcal{D}\) | Row ids |
|--|------------------------------|---------|
| \(E^+\) | \(x_1 \neq 0\) | 1, 2 |
| \(E^-\) | \(x_1 = 0\) | 3 |

On \(\mathcal{D}\): \(x_1\neq 0\) iff \(x_0\in\{0,1\}\). Sibling \(x_2=2\) on id 2 (pos) and id 3 (neg).

### 4.4 Reference hypothesis \(\mathcal{H}_{x_1}^\star\)

```prolog
x1(A) :- x0_val_0(A).
x1(A) :- x0_val_1(A).
```

Do not cite sibling \(x_2\).

### 4.5 Semantic success (inspection)

An intensional rule that characterises \(x_1\neq 0\) via the **parent** \(x_0\)
(\(x_0\neq 2\)), without rote sample-id casework, and **without citing the sibling**.

### 4.6 Divergences to watch

- Citing `x2_val_*` (sibling distractor).
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

- `x0_val_0`, `x0_val_1`, `x0_val_2`
- `x1_val_0`, `x1_val_1`, `x1_val_2`


### 5.3 Labels

| | Definition on \(\mathcal{D}\) | Row ids |
|--|------------------------------|---------|
| \(E^+\) | \(x_2 \neq 0\) | 2, 3 |
| \(E^-\) | \(x_2 = 0\) | 1 |

On \(\mathcal{D}\): \(x_2\neq 0\) iff \(x_0\neq 0\). Sibling \(x_1=2\) on id 1 (neg) and id 2 (pos).

### 5.4 Reference hypothesis \(\mathcal{H}_{x_2}^\star\)

```prolog
x2(A) :- x0_val_1(A).
x2(A) :- x0_val_2(A).
```

Do not cite sibling \(x_1\).

### 5.5 Semantic success (inspection)

Characterise \(x_2\neq 0\) via parent \(x_0\) (\(x_0\neq 0\)), without citing sibling
\(x_1\), without rote sample-id casework.

### 5.6 Divergences to watch

- Citing `x1_val_*` (sibling).
- Rote / sample-id rules.
- Missing the parent.

---

## 6. Non-collapse / relevance

The two children use different deterministic maps of \(x_0\), so parent and sibling are
not extensionally equivalent. The scientific point is **sibling distraction under
imperfect correlation**: the sibling is associated with the target via the common cause
but is not a zero-error separator of \(E^\pm\).

---

## 7. Cells

| Cell | Fixture | Target | Config |
|------|---------|--------|--------|
| U4-x1-ECAI | U4 | \(x_1\) | ECAI |
| U4-x1-AAMAS | U4 | \(x_1\) | AAMAS |
| U4-x2-ECAI | U4 | \(x_2\) | ECAI |
| U4-x2-AAMAS | U4 | \(x_2\) | AAMAS |

Inspection order: \(x_2\) (parent-nonzero lesson) then \(x_1\) (parent-not-2 lesson), or either.
