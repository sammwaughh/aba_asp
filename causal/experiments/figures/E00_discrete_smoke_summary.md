# E00_discrete_smoke - results summary

- Total cells: **36**
- Outcome counts: completed_no_solution=12, error=1, solved=21, timeout=2
- Overall solved: **21/36** (58%)
- Solve rate on targets **with true parents**: **60%** (12/20)
- Root targets (no parents) correctly rejected (no spurious rule): **6/16**

| DGP | target | true parents | role | solved/seeds | median body-F1 | timeouts | median wall (s) |
|---|---|---|---|---|---|---|---|
| G3-chain | x0 | (none) | ROOT (expect none) | 3/4 | - | 0 | 0.8 |
| G3-chain | x1 | x0 | has parents | 4/4 | 1.00 | 0 | 0.7 |
| G3-chain | x2 | x1 | has parents | 1/4 | 0.00 | 2 | 113.7 |
| G3-collider | x0 | (none) | ROOT (expect none) | 1/4 | - | 0 | 11.7 |
| G3-collider | x1 | (none) | ROOT (expect none) | 1/4 | - | 0 | 21.1 |
| G3-collider | x2 | x0,x1 | has parents | 0/4 | - | 0 | 30.0 |
| G3-fork | x0 | (none) | ROOT (expect none) | 4/4 | - | 0 | 0.7 |
| G3-fork | x1 | x0 | has parents | 3/4 | 1.00 | 0 | 0.8 |
| G3-fork | x2 | x0 | has parents | 4/4 | 1.00 | 0 | 0.7 |

## How to read this

- **Targets with parents** are the real learning task; solved + body-F1=1.00 means the learner recovered exactly the true parent set.
- **ROOT targets** have no parents, so `completed_no_solution` is the *correct* answer (the learner declines to invent a spurious rule).
- **timeouts** are search blow-ups, not wrong answers; they should be ~0 in this small discrete regime.
