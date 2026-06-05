# E00_discrete_smoke - results summary

- Total cells: **36**
- Outcome counts: completed_no_solution=7, error=1, solved=27, timeout=1
- Overall solved: **27/36** (75%)
- Solve rate on targets **with true parents**: **85%** (17/20)
- Root targets (no parents) correctly rejected (no spurious rule): **4/16**

| DGP | target | true parents | role | solved/seeds | median body-F1 | timeouts | median wall (s) |
|---|---|---|---|---|---|---|---|
| G3-chain | x0 | (none) | ROOT (expect none) | 3/4 | - | 0 | 0.6 |
| G3-chain | x1 | x0 | has parents | 4/4 | 1.00 | 0 | 0.6 |
| G3-chain | x2 | x1 | has parents | 4/4 | 0.00 | 0 | 0.4 |
| G3-collider | x0 | (none) | ROOT (expect none) | 1/4 | - | 0 | 6.1 |
| G3-collider | x1 | (none) | ROOT (expect none) | 2/4 | - | 1 | 6.2 |
| G3-collider | x2 | x0,x1 | has parents | 1/4 | 1.00 | 0 | 14.8 |
| G3-fork | x0 | (none) | ROOT (expect none) | 4/4 | - | 0 | 0.4 |
| G3-fork | x1 | x0 | has parents | 4/4 | 1.00 | 0 | 0.5 |
| G3-fork | x2 | x0 | has parents | 4/4 | 1.00 | 0 | 0.6 |

## How to read this

- **Targets with parents** are the real learning task; solved + body-F1=1.00 means the learner recovered exactly the true parent set.
- **ROOT targets** have no parents, so `completed_no_solution` is the *correct* answer (the learner declines to invent a spurious rule).
- **timeouts** are search blow-ups, not wrong answers; they should be ~0 in this small discrete regime.
