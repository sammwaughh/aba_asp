# ArgCausalDisco reference (for aba_asp experiment planning)

## Purpose

This is the **source of truth** about the parts of the sibling **ArgCausalDisco** repo
that `aba_asp` actually depends on, written so experiments can be planned **without
opening the ArgCausalDisco repo**. It is a focused reference, not a mirror of the whole
project.

Scope: aba_asp uses ArgCausalDisco **only as a data-generation library** — specifically
two synthetic simulators in `ArgCausalDisco/utils/data_utils.py`. Everything else in
ArgCausalDisco (the argumentative causal-discovery algorithm `abapc.py`/`causalaba.py`,
the clingo encodings, the baseline wrappers, the paper experiment drivers) is **not used**
by aba_asp and is summarised only briefly at the end for orientation.

For how this fits the wider project (engine vs bridge, what is implemented vs theory-only)
see [`repo_map.md`](repo_map.md). For environment/import mechanics see
[`environment_setup.md`](environment_setup.md). For running pipelines see
[`execution_guide.md`](execution_guide.md). Where those overlap with this file, treat the
API details here as authoritative for the simulators.

> Naming caution: ArgCausalDisco is the home of **Russo-style Causal ABA** (argumentative
> causal discovery). That algorithm is **theory-only from aba_asp's perspective — aba_asp
> does not call it.** aba_asp only borrows the data simulators. Do not assume importing
> from ArgCausalDisco brings any Causal ABA encoding into aba_asp.

## Location and layout

```
Causal ABA Learning/            # workspace root
  aba_asp/                      # our project
  ArgCausalDisco/               # SIBLING repo (NOT inside aba_asp)
    utils/
      data_utils.py             # <- the only file aba_asp imports from
      helpers.py                # random_stability (pulled in transitively)
      graph_utils.py            # is_dag (lazy-imported by simulate_dag)
    abapc.py, causalaba.py      # Causal ABA discovery algorithm (UNUSED by aba_asp)
    cd_algorithms/, encodings/  # baselines + ASP encodings (UNUSED by aba_asp)
    experiments*.py, tests.py   # paper drivers (UNUSED by aba_asp)
    datasets/, results/         # paper data/outputs (UNUSED by aba_asp)
    requirements.txt            # FULL paper stack — do NOT install for aba_asp work
```

ArgCausalDisco is a **sibling** of `aba_asp`, resolved by aba_asp scripts as
`repo_root.parent / "ArgCausalDisco"`.

## What aba_asp imports

Two functions, in exactly these call sites:

```python
from ArgCausalDisco.utils.data_utils import (
    simulate_discrete_data,
    simulate_linear_continuous_data,
    simulate_dag,            # imported by the legacy script only; never CALLED
)
```

- `causal/experiments/run_grid.py` imports `simulate_discrete_data` and
  `simulate_linear_continuous_data` (the **grid** path — this is what real experiments use).
- `causal/argcausaldisco_integration.py` and `causal/test_aba_learning.py` import the same
  two (plus `simulate_dag`, which is imported but not invoked).

No other ArgCausalDisco symbol is used by aba_asp.

---

## API: the two simulators (authoritative)

Both live in `ArgCausalDisco/utils/data_utils.py`. Both **return a bare NumPy array and
nothing else** — no column names, no graph object, no metadata. The caller is responsible
for naming columns (`x0..x{n-1}`) and for holding the ground-truth edge set separately.

### `simulate_discrete_data(num_of_nodes, sample_size, truth_DAG_directed_edges, random_seed=None)`

Discrete **Bayesian-network** sampler (from the causal-learn lineage), built on
`pgmpy` (`DiscreteBayesianNetwork` + `TabularCPD` + `BayesianModelSampling.forward_sample`).

- **Data mode:** non-binary categorical / discrete. **Cardinalities are RANDOM per node**
  (`_simulate_cards()`): each node gets `randint(2, …)`, with smaller cardinalities forced
  on nodes that have many parents (to keep CPT enumeration tractable). A node's column is
  binary **only if its drawn cardinality happens to be 2** — there is no "binary" mode and
  no way to force binary from this function alone.
- **CPDs:** drawn from a Dirichlet (`alpha ~ U(1,5)`), so dependencies are probabilistic,
  not deterministic.
- **`truth_DAG_directed_edges`:** an iterable/set of **0-based integer index pairs**, e.g.
  `{(0,1),(1,2)}`. Builds the adjacency internally; also adds isolated nodes if an index in
  `range(num_of_nodes)` never appears in an edge.
- **`random_seed`:** if given, saves the global NumPy RNG state, seeds with this value, then
  **restores** the prior state on exit (so it does not leak global RNG side effects). Uses
  `np.random` globally — not a private `Generator`.
- **Returns:** `np.ndarray`, `dtype=int64`, shape `(sample_size, num_of_nodes)`, columns
  reordered to topological order so column `i` corresponds to node `i`.
- **Gotcha:** very small `sample_size` (e.g. 6–8 in the smoke configs) gives noisy,
  sometimes degenerate columns; a column can come out constant, which then yields empty
  E+/E− downstream.

Example (as aba_asp calls it):
```python
data = simulate_discrete_data(num_of_nodes=3, sample_size=8,
                              truth_DAG_directed_edges={(0,1),(1,2)}, random_seed=0)
df = pd.DataFrame(data, columns=["x0","x1","x2"])   # caller names columns
```

### `simulate_linear_continuous_data(num_of_nodes, sample_size, truth_DAG_directed_edges, noise_type="gaussian", random_seed=None, linear_weight_minabs=0.5, linear_weight_maxabs=0.9, linear_weight_netative_prob=0.5)`

Continuous **linear SEM** (linear Gaussian / linear non-Gaussian) sampler.

- **Data mode:** continuous. Model is `X = (I − W)^{-1} · noise`, where `W` is the weighted
  adjacency. Edge weights are drawn `U(0.5, 0.9)` in absolute value, with ~50% sign flips
  (`linear_weight_netative_prob`). [Note the upstream typo "netative" in the kwarg name.]
- **`noise_type`:** `"gaussian"` (default) or `"exponential"`. Anything else raises
  `NotImplementedError`. aba_asp always passes `"gaussian"`.
- **`truth_DAG_directed_edges`, `random_seed`:** same conventions as the discrete sampler
  (0-based int pairs; global RNG saved/seeded/restored).
- **Returns:** `np.ndarray`, float, shape `(sample_size, num_of_nodes)`. Column `i` = node `i`.
- **Gotcha:** values are unbounded floats; aba_asp must bin them (BK features) and/or
  threshold them (target E+/E−) before ABA Learning sees them.

### `simulate_dag(d, s0, graph_type)` — available but UNUSED

Random-DAG **adjacency-matrix** generator (from the NOTEARS repo). `graph_type` ∈
`{"ER","SF","BP"}` (Erdős–Rényi, scale-free Barabási–Albert, bipartite). Returns a `[d,d]`
binary adjacency matrix. Lazily imports `is_dag` from `utils.graph_utils`.

- It is **imported** by `causal/argcausaldisco_integration.py` but **never called**, and the
  grid runner does not import it. **No experiment config wires it in.** If you want random
  graph topologies rather than the hand-listed motifs, this is the existing building block,
  but it returns an adjacency matrix (you would convert to an edge set for the simulators).
- Defined **twice** in `data_utils.py` (duplicate); behaviour identical.

---

## Other DGPs in the file (not used, but real options)

`ArgCausalDisco/utils/data_utils.py` also contains, for completeness:

- **`load_bn_from_BIF(...)` / `load_bnlearn_data_dag(dataset_name, data_path, sample_size, seed=1, standardise=True, ...)`**
  — load a real bnlearn benchmark Bayesian network from a `.bif` file and sample from it.
  Supported names (`BIF_FOLDER_MAP`): `cancer`, `earthquake`, `survey`, `asia`, `sachs`
  (small); `alarm`, `child`, `insurance` (medium); `hailfinder`, `hepar2` (large).
  Returns `(data, B_true)` — i.e. **both data and the true adjacency matrix** (unlike the two
  synthetic simulators). Requires the BIF files under a data path and the `pgmpy` `BIFReader`.
  **Unused by aba_asp**, but this is the one DGP here that hands back ground-truth structure
  directly, if richer/realistic discrete benchmarks are ever wanted.
- **`simulate_data_and_run_PC(...)`** — convenience that simulates discrete data and runs the
  PC algorithm; pulls in `cd_algorithms.models.pc` (heavy). **Unused by aba_asp.**

---

## Ground truth: where it comes from

The simulators **do not return the graph.** In aba_asp, the ground-truth DAG is held
separately (in `causal/experiments/dgp.py`, `handcrafted.py`, or the YAML `edges`) and is
the **same edge set passed into the simulator**. The metric layer
(`causal/metrics.py :: GroundTruth`) reconstructs `parents_of` / `ancestors_of` from that
edge set.

Implication for planning: there is **no validation** that the sampled data actually reflects
the requested edges (especially at the small sample sizes used in smoke configs). "Ground
truth" = "the edges we asked for", not "the edges present in this particular sample".

---

## Dependencies and import mechanics (critical)

### Do NOT install `ArgCausalDisco/requirements.txt`
That file targets full paper reproduction and pulls heavy/fragile packages: `torch`,
`causal-learn`, `gcastle`, `notears` (git), `python-javabridge`, `pmlb`, `rustworkx`, etc.
The two simulators need only: **`numpy`, `pandas`, `pgmpy`, `scikit-learn`, `networkx`,
`igraph`, `pillow`** (most already in the aba-asp env). `igraph`/`networkx`/`pillow` are
needed because of module-level imports in `data_utils.py`, not because the simulators use
them directly.

### The `utils` namespace collision
Both repos have a top-level `utils` package:
- `aba_asp/utils/` → imported as `aba_asp.utils.*`
- `ArgCausalDisco/utils/` → ArgCausalDisco uses **bare** `from utils.helpers import ...` and
  `from utils.graph_utils import is_dag`.

Because of this, **do not set a global `PYTHONPATH`** — whichever `utils` wins becomes
order-dependent and fragile. aba_asp scripts instead insert, at runtime, in order:
`aba_asp/` repo root, the workspace root, and `ArgCausalDisco/`. For manual one-liners you
must add **both** the workspace root and `ArgCausalDisco/` to `sys.path` (see the smoke test
in [`environment_setup.md`](environment_setup.md) §6).

### Module-level import surface of `data_utils.py`
At import time the module runs: `numpy`, `pandas`, `networkx`, `igraph`,
`pgmpy.readwrite.BIFReader`, `PIL.Image`, `sklearn.preprocessing`, and
`from utils.helpers import random_stability`. The heaviest baselines
(`cd_algorithms.models.pc`, `utils.graph_utils.is_dag`) were moved to **lazy/in-function
imports** so importing the simulators does not drag in torch/gcastle/notears. (See
[`environment_setup.md`](environment_setup.md) §5 "Compatibility edit".) `random_stability`
(in `utils/helpers.py`) just seeds `PYTHONHASHSEED`, `random`, and `numpy`; it is used by the
BN loaders, not by the two simulators.

### Expected harmless warning
A `pgmpy` `FutureWarning` (about `StructureScore`) may print on import; it can be ignored.

---

## How aba_asp uses the output (handoff contract)

This is the boundary aba_asp depends on; planning new experiments only needs to respect it:

1. **Sample:** `simulate_*` → `ndarray (n, d)`.
2. **Name:** wrap as `pd.DataFrame(data, columns=[f"x{i}" for i in range(d)])`.
3. **Declare types:** grid sets every column `"continuous"` (continuous DGP) or
   `"categorical"` (discrete DGP). `"binary"` is never declared as a type in the grid path.
4. **BK features** (`generate_aba_background_knowledge`, with the target column excluded):
   - 0/1 column → positive-only `x_i(A) :- A=n.` (no `_val_0`).
   - ≥3-valued column → `x_i_val_v(A) :- A=n.` for each value.
   - continuous column → quantile/uniform binned `x_i_bin_k(A) :- A=n.`
5. **Target E+/E−** come from **raw** values, independent of BK binning: continuous uses a
   median split; discrete uses 0-vs-nonzero (else min-vs-rest) via `pick_target_variable`.

So the simulators feed a pipeline that **bins/encodes features but binarises the target from
raw data** — the two thresholds are unrelated. Continuous magnitudes are never seen by the
learner (binned only).

---

## Planning notes / caveats specific to the simulators

- **Discrete cardinality is uncontrolled.** If an experiment needs strictly binary data, you
  cannot get it from `simulate_discrete_data` arguments alone — post-process the array, or use
  a handcrafted/pinned table. Conversely, a "discrete" run may silently mix binary and
  multi-valued columns across nodes/seeds.
- **Determinism is by `random_seed` only**, and via the **global** NumPy RNG (saved/restored).
  Two cells with the same `(num_of_nodes, sample_size, edges, random_seed)` reproduce exactly.
  The grid's per-cell `np.random.RandomState(seed)` is constructed but not what drives the
  simulator — the simulator's own `random_seed` governs the draw.
- **Small n is fragile.** Constant or near-constant columns at n≈6–8 lead to empty E+/E−
  (cell `skipped`) or degenerate splits. Larger n is safer for any quantitative claim.
- **No mixed-type DGP.** Each simulator emits one mode for all columns. There is no
  built-in mixed continuous+discrete generator (mixed handling exists only in the *converter*
  `aba_asp/utils/data_utils.py`, not in any wired DGP).
- **Edge direction matters and is 0-based.** `{(0,1)}` means `x0 → x1`. Indices must lie in
  `range(num_of_nodes)`.

---

## Quick reference table

| Item | `simulate_discrete_data` | `simulate_linear_continuous_data` | `simulate_dag` |
|---|---|---|---|
| File | `ArgCausalDisco/utils/data_utils.py` | same | same (defined twice) |
| Used by aba_asp grid? | **Yes** | **Yes** | No (imported, never called) |
| Data mode | discrete BN (random cardinalities) | continuous linear SEM | adjacency matrix only |
| Binary? | only if a node's card = 2 | no | n/a |
| Graph input | `truth_DAG_directed_edges` (0-based int pairs) + `num_of_nodes` | same | `d`, `s0`, `graph_type∈{ER,SF,BP}` |
| Samples / seed | `sample_size`, `random_seed` | `sample_size`, `random_seed` | n/a (`s0`=expected #edges) |
| Extra knobs | — | `noise_type∈{gaussian,exponential}`, weight bounds | — |
| Output | `int64 ndarray (n,d)` | `float ndarray (n,d)` | `[d,d]` binary adj matrix |
| Returns graph/meta? | No (table only) | No (table only) | adjacency only, no data |
| Column names | none (caller adds `x0..`) | none | n/a |

## Rest of ArgCausalDisco (orientation only — NOT used by aba_asp)

For awareness when reading the upstream paper/repo; none of this is invoked by aba_asp:

- `abapc.py`, `causalaba.py` — the **Causal ABA / ABAPC** argumentative causal-discovery
  algorithm (the actual research contribution of ArgCausalDisco).
- `encodings/` — clingo/ASP encodings for that algorithm.
- `cd_algorithms/` — wrappers for baseline discovery methods (PC, NOTEARS, etc.).
- `utils/cit.py`, `utils/graph_utils.py`, `utils/compare_sid.py`, `utils/plotting.py` —
  conditional-independence tests, graph metrics (SHD/SID), plotting.
- `experiments.py`, `experiments_bnlearn.py`, `eval_aspcr.py`, `tests.py` — paper experiment
  drivers and their (large) test suite.
- `datasets/`, `results/` — benchmark inputs and the paper's recorded outputs.

## Related docs

- [`repo_map.md`](repo_map.md) — engine vs bridge; implemented vs theory-only.
- [`environment_setup.md`](environment_setup.md) — env, import/path rules, smoke tests.
- [`execution_guide.md`](execution_guide.md) — running pipelines and expected outputs.
