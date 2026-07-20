# U5 — Chain + correlated ancestor (pilot)

**Unit ID:** U5  
**Fixture id:** `m12_u5_chain_curated`  
**Lesson:** Parent vs correlated ancestor on the sink  
**Provenance:** Restored pilot `m12_chain` support under the Approach regime (nonzero-positive labels; `val`-only BK/\(\mathcal{H}^\star\); 2026-07-20). Intermediate \(x_1\) is **not** a learning target (no parent-aligned \(\mathcal{H}^\star\); tied descendant would dominate).  
**Cells:** 2 — \(x_2\) × {ECAI, AAMAS}

---

## 1. Graph

| | |
|--|--|
| **Nodes \(V\)** | \(\{x_0,x_1,x_2\}\) |
| **Edges \(E\)** | \(x_0 \to x_1\), \(x_1 \to x_2\) |
| **Sources \(S\)** | \(\{x_0\}\) |
| **Non-sources \(N\)** | \(\{x_1,x_2\}\) (learning target: \(x_2\) only) |

```text
x0 ----→ x1 ----→ x2
```

---

## 2. Alphabet and mechanisms

- \(K=\{0,1,2\}\) for every variable.
- **Support (not full source factorial):** for each \(x_0\in K\), include the two pairs
  \((x_0,x_1)=(x_0,x_0)\) and \((x_0,(x_0+1)\bmod 3)\).
- \(x_2 := \operatorname{copy}(x_1)\).

So \(x_1\) is **not** a single-valued function of \(x_0\) on \(\mathcal{D}\); the table is the
pilot correlated-ancestor construction. Sink \(x_2\) is deterministic given \(x_1\).

---

## 3. Data \(\mathcal{D}\)

**Generation:** curated 6-row support (pilot `m12_chain`), then \(x_2:=x_1\).
Sample ids are 1-based.

| id | \(x_0\) | \(x_1\) | \(x_2=\operatorname{copy}(x_1)\) |
|---:|--------:|--------:|--------------------------------:|
| 1 | 0 | 0 | 0 |
| 2 | 0 | 1 | 1 |
| 3 | 1 | 1 | 1 |
| 4 | 1 | 2 | 2 |
| 5 | 2 | 2 | 2 |
| 6 | 2 | 0 | 0 |

No duplicate rows. Parent \(x_1\) uniquely separates nonzero labelling of \(x_2\);
ancestor \(x_0\) is associated but imperfect.

---

## 4. Target \(t = x_2\) (sink — parent vs ancestor)

### 4.1 Structural sets

| Set | Members | Role |
|-----|---------|------|
| Ancestors of \(t\) | \(\{x_0,x_1\}\) | Parent \(x_1\) preferred; grandparent \(x_0\) is correlated but imperfect |
| Other distractors (non-ancestor, non-descendant) | \(\emptyset\) | — |
| Descendants of \(t\) | \(\emptyset\) | (none; sink) |

### 4.2 Background knowledge

Exclude **only** \(x_2\). Include both ancestors:

- `x0_val_0`, `x0_val_1`, `x0_val_2`
- `x1_val_0`, `x1_val_1`, `x1_val_2`


### 4.3 Labels

| | Definition on \(\mathcal{D}\) | Row ids |
|--|------------------------------|---------|
| \(E^+\) | \(x_2 \neq 0\) | 2, 3, 4, 5 |
| \(E^-\) | \(x_2 = 0\) | 1, 6 |

On \(\mathcal{D}\): \(x_2\neq 0\) iff \(x_1\in\{1,2\}\). Ancestor \(x_0\) is imperfect
(\(x_0=0\): id 1 neg / id 2 pos; \(x_0=2\): id 5 pos / id 6 neg).

### 4.4 Reference hypothesis \(\mathcal{H}_{x_2}^\star\)

Prefer the **direct parent**:

```prolog
x2(A) :- x1_val_1(A).
x2(A) :- x1_val_2(A).
```

**Note (parent vs ancestor):** no `x0_val_*`-only rule set matches this labelling
perfectly. Ancestor-only or ancestor-contaminated bodies are parent-vs-ancestor
divergences to inspect.

### 4.5 Semantic success (inspection)

An intensional, general rule that correctly characterises \(x_2\neq 0\) on \(\mathcal{D}\)
using the direct parent \(x_1\), without rote sample-id casework, and without relying on
the imperfect ancestor alone.

### 4.6 Divergences to watch

- Grandparent / ancestor citation when parent is available (parent vs ancestor cut).
- Rote / sample-id rules.
- Assumption-mediated casework that obscures the parent copy concept.

---

## 5. Cells

| Cell id | Unit | Target | Config |
|---------|------|--------|--------|
| U5-x2-ECAI | U5 | \(x_2\) | ECAI |
| U5-x2-AAMAS | U5 | \(x_2\) | AAMAS |
