# U1 — Separator + copy

**Unit ID:** U1  
**Fixture id (proposed):** `m12_u1_separator_copy`  
**Lesson:** Unique parent / copy with an isolated distractor  
**Provenance:** Redesigned pilot `m12_sep` under the Approach regime  
**Cells:** 2 — `(U1, x2, ECAI)`, `(U1, x2, AAMAS)`

---

## 1. Graph

| | |
|--|--|
| **Nodes \(V\)** | \(\{x_0,x_1,x_2\}\) |
| **Edges \(E\)** | \(x_1 \to x_2\) only |
| **Sources \(S\)** | \(\{x_0,x_1\}\) |
| **Non-sources \(N\)** | \(\{x_2\}\) |

```text
x0          (isolated; no incident edges)

x1 ----→ x2
```

---

## 2. Alphabet and mechanisms

- \(K=\{0,1,2\}\) for every variable.
- \(x_2 := \operatorname{copy}(x_1)\) (allowed: unique parent).

Boolean nonzero sketch: \(\Phi_{x_2}=z_1\). Isolated \(x_0\) does not enter the mechanism.

---

## 3. Data \(\mathcal{D}\)

**Generation:** full source factorial over \(K^{|S|}\) (\(3^2=9\) rows), then
\(x_2=x_1\). Sample ids are 1-based in the order below (outer \(x_0\), inner \(x_1\)).

| id | \(x_0\) | \(x_1\) | \(x_2=\operatorname{copy}(x_1)\) |
|---:|--------:|--------:|----------------------------------:|
| 1 | 0 | 0 | 0 |
| 2 | 0 | 1 | 1 |
| 3 | 0 | 2 | 2 |
| 4 | 1 | 0 | 0 |
| 5 | 1 | 1 | 1 |
| 6 | 1 | 2 | 2 |
| 7 | 2 | 0 | 0 |
| 8 | 2 | 1 | 1 |
| 9 | 2 | 2 | 2 |

No duplicate rows. Sink fixture: no variables beyond \(x_2\).

---

## 4. Target \(t = x_2\)

### 4.1 Structural sets

| Set | Members | Role |
|-----|---------|------|
| Ancestors of \(t\) | \(\{x_1\}\) | May appear in a good rule |
| Other distractors (non-ancestor, non-descendant) | \(\{x_0\}\) | Isolated column in BK; citing it is a divergence |
| Descendants of \(t\) | \(\emptyset\) | (none; sink) |

### 4.2 Background knowledge

Exclude **only** \(x_2\). Include **both** \(x_0\) and \(x_1\) (distractor stays in BK):

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
| \(E^+\) | \(x_2 \neq 0\) | 2, 3, 5, 6, 8, 9 (6 rows) |
| \(E^-\) | \(x_2 = 0\) | 1, 4, 7 (3 rows) |

On \(\mathcal{D}\): \(x_2\neq 0\) iff \(x_1\neq 0\) (independent of \(x_0\)).

### 4.4 Reference hypothesis \(\mathcal{H}_{x_2}^\star\)

```prolog
x2(A) :- x1_nz(A).
```

Compact `nz` form preferred. A correct `val`-expansion of “\(x_1\in\{1,2\}\)” is
extensionally acceptable but inferior.

### 4.5 Semantic success (inspection)

An intensional, general rule that correctly characterises \(x_2\neq 0\) on \(\mathcal{D}\)
using the unique parent \(x_1\), without rote sample-id casework, and **without citing the
isolated distractor \(x_0\)**.

### 4.6 Divergences to watch

- Citing `x0_nz` / `x0_val_*` (isolated distractor).
- Rules that depend on a particular \(x_0\) value coinciding with positives.
- Rote / sample-id rules.
- Missing the parent \(x_1\).

---

## 5. Non-collapse / relevance

Mechanism depends only on \(x_1\). Column \(x_0\) is intentionally irrelevant to \(f_{x_2}\)
and is present so the learner can be tested on ignoring it. \(x_1\) remains the unique
relevant ancestor.

---

## 6. Cells

| Cell | Fixture | Target | Config |
|------|---------|--------|--------|
| U1-ECAI | U1 | \(x_2\) | ECAI |
| U1-AAMAS | U1 | \(x_2\) | AAMAS |

Inspection order: only one target (sink).
