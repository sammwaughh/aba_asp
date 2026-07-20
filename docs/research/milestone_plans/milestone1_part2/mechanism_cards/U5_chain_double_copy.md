# U5 — Chain + correlated ancestor (pilot)

**Unit ID:** U5  
**Fixture id:** `m12_u5_chain_double_copy`  
**Lesson:** Parent vs correlated ancestor (sink); when learning the intermediate, a **descendant stays in BK** as a distractor  
**Provenance:** Restored pilot `m12_chain` support under the Approach regime (nonzero-positive labels; `val`-only BK/\(\mathcal{H}^\star\); 2026-07-20)  
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

## 4. Target \(t = x_1\) (intermediate — descendant distractor cell)

### 4.1 Structural sets

| Set | Members | Role |
|-----|---------|------|
| Ancestors of \(t\) | \(\{x_0\}\) | Imperfect separator under nonzero labelling |
| Other distractors (non-ancestor, non-descendant) | \(\emptyset\) | — |
| Descendants of \(t\) | \(\{x_2\}\) | **Included in BK as distractors**; citing them is an **explicit failure mode** |

### 4.2 Background knowledge

Exclude **only** \(x_1\). Include parent \(x_0\) **and descendant \(x_2\)**:

- `x0_val_0`, `x0_val_1`, `x0_val_2`
- `x2_val_0`, `x2_val_1`, `x2_val_2`

No `*_nz` predicates.

**Do not** omit \(x_2\) from BK. The point of this cell is to test whether the learner
cites the descendant.

### 4.3 Labels

| | Definition on \(\mathcal{D}\) | Row ids |
|--|------------------------------|---------|
| \(E^+\) | \(x_1 \neq 0\) | 2, 3, 4, 5 |
| \(E^-\) | \(x_1 = 0\) | 1, 6 |

On \(\mathcal{D}\): \(x_1\neq 0\) iff \(x_2\neq 0\) (because \(x_2=x_1\)). Parent \(x_0\) is
**imperfect** (\(x_0=0\): id 1 neg / id 2 pos; \(x_0=2\): id 5 pos / id 6 neg).

### 4.4 Reference hypothesis \(\mathcal{H}_{x_1}^\star\)

**None (parent-aligned).** There is no perfect separator among ancestor `x0_val_*`
predicates. The unique perfect separator in BK is the **descendant** \(x_2\), which must
**not** be the reference.

Do not treat descendant rules as \(\mathcal{H}^\star\). Inspection is failure-mode first
(descendant citation), not `exact_hstar`.

### 4.5 Semantic success (inspection)

Prefer rules that do **not** cite descendant \(x_2\). Perfect coverage via `x2_val_*`
alone is extensionally available on \(\mathcal{D}\) and counts as the **descendant
failure mode**.

### 4.6 Divergences to watch

- Citing `x2_val_*` (**descendant failure mode**; extensionally perfect on \(\mathcal{D}\)).
- Rote / sample-id rules.
- Ancestor-only attempts that fail coverage (expected under imperfect \(x_0\)).

---

## 5. Target \(t = x_2\) (sink — parent vs ancestor)

### 5.1 Structural sets

| Set | Members | Role |
|-----|---------|------|
| Ancestors of \(t\) | \(\{x_0,x_1\}\) | Parent \(x_1\) preferred; grandparent \(x_0\) is correlated but imperfect |
| Other distractors (non-ancestor, non-descendant) | \(\emptyset\) | — |
| Descendants of \(t\) | \(\emptyset\) | (none; sink) |

### 5.2 Background knowledge

Exclude **only** \(x_2\). Include both ancestors:

- `x0_val_0`, `x0_val_1`, `x0_val_2`
- `x1_val_0`, `x1_val_1`, `x1_val_2`

No `*_nz` predicates.

### 5.3 Labels

| | Definition on \(\mathcal{D}\) | Row ids |
|--|------------------------------|---------|
| \(E^+\) | \(x_2 \neq 0\) | 2, 3, 4, 5 |
| \(E^-\) | \(x_2 = 0\) | 1, 6 |

On \(\mathcal{D}\): \(x_2\neq 0\) iff \(x_1\in\{1,2\}\). Ancestor \(x_0\) is imperfect
(same mixed rows as in §4.3).

### 5.4 Reference hypothesis \(\mathcal{H}_{x_2}^\star\)

Prefer the **direct parent**:

```prolog
x2(A) :- x1_val_1(A).
x2(A) :- x1_val_2(A).
```

**Note (parent vs ancestor):** no `x0_val_*`-only rule set matches this labelling
perfectly. Ancestor-only or ancestor-contaminated bodies are parent-vs-ancestor
divergences to inspect.

### 5.5 Semantic success (inspection)

An intensional, general rule that correctly characterises \(x_2\neq 0\) on \(\mathcal{D}\)
using the direct parent \(x_1\), without rote sample-id casework, and without relying on
the imperfect ancestor alone.

### 5.6 Divergences to watch

- Grandparent / ancestor citation when parent is available (parent vs ancestor cut).
- Rote / sample-id rules.
- Empty / vacuous rules.

---

## 6. Non-collapse / relevance

The curated support keeps \(x_0\) associated with \(x_2\) without making it a perfect
separator. Sink recovery has a clean parent-aligned \(\mathcal{H}^\star\). Intermediate
learning stresses **descendant-in-BK** under a table where the descendant is
extensionally tied to the target.

---

## 7. Cells

| Cell | Fixture | Target | Config |
|------|---------|--------|--------|
| U5-x1-ECAI | U5 | \(x_1\) | ECAI |
| U5-x1-AAMAS | U5 | \(x_1\) | AAMAS |
| U5-x2-ECAI | U5 | \(x_2\) | ECAI |
| U5-x2-AAMAS | U5 | \(x_2\) | AAMAS |

Inspection order (Approach): nearer sources first — inspect \(x_1\) cells before \(x_2\).
