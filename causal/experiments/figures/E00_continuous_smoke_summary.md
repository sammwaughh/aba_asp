# E00_continuous_smoke - results summary

- Total cells: **36**
- Outcome counts: completed_no_solution=32, solved=4
- Overall solved: **4/36** (11%)
- Solve rate on targets **with true parents**: **15%** (3/20)
- Root targets (no parents) correctly rejected (no spurious rule): **15/16**

| DGP | target | true parents | role | solved/seeds | median body-F1 | timeouts | median wall (s) |
|---|---|---|---|---|---|---|---|
| G3-chain | x0 | (none) | ROOT (expect none) | 0/4 | - | 0 | 73.9 |
| G3-chain | x1 | x0 | has parents | 0/4 | - | 0 | 81.5 |
| G3-chain | x2 | x1 | has parents | 0/4 | - | 0 | 71.5 |
| G3-collider | x0 | (none) | ROOT (expect none) | 0/4 | - | 0 | 58.1 |
| G3-collider | x1 | (none) | ROOT (expect none) | 1/4 | - | 0 | 64.3 |
| G3-collider | x2 | x0,x1 | has parents | 1/4 | 0.67 | 0 | 59.3 |
| G3-fork | x0 | (none) | ROOT (expect none) | 0/4 | - | 0 | 55.3 |
| G3-fork | x1 | x0 | has parents | 1/4 | 1.00 | 0 | 69.4 |
| G3-fork | x2 | x0 | has parents | 1/4 | 1.00 | 0 | 68.6 |

## How to read this

- **Targets with parents** are the real learning task; solved + body-F1=1.00 means the learner recovered exactly the true parent set.
- **ROOT targets** have no parents, so `completed_no_solution` is the *correct* answer (the learner declines to invent a spurious rule).
- **timeouts** are search blow-ups, not wrong answers; they should be ~0 in this small discrete regime.
