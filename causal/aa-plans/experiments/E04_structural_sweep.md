# E04 — Structural Sweep

**Status:** analysis-only spec (no new Prolog runs). Executes after E02 (and optionally E03) complete.
**Companion docs:** `EXPERIMENTS_PLAN.md`, `METRICS.md`, `INFRA.md`, `REPORT_OUTLINE.md` (F5).
**Role in the plan:** the *structural* read of E02's data; produces Figure F5 and a discrete companion appendix figure.

---

## 1. Question

Holding sample size and learner knobs fixed, how does ABA-ASP's behaviour vary **across causal structures**?

Specifically:

- Is `body_parent_f1` **structurally distributed** (chain > collider/fork > hub) at n=25?
- Is `offgraph_rate` **higher** on confounder / collider / hub DGPs than on the chain?
- Are the **per-target asymmetries within a DGP** systematic? (E.g., in `G3-fork`, target x0 should behave very differently from x1/x2.)

E04 is *analysis-only*: it consumes the same `results.parquet` rows produced by E02 (and, for sensitivity, E03's n=25 slice).

---

## 2. Hypothesis

1. `body_parent_f1` (median, over solved seeds) **ranks**: chain > collider ≥ forkchain > fork ≈ hub. The chain wins because its parent → child mechanism is sharpest; hub loses because targets are confounded through a single common cause and the binning compresses the signal.
2. `offgraph_rate` is **highest on `G4-hub` x1/x2/x3** (each child target gets x0 as the only true parent but the learner often cites siblings).
3. **`fraction_solved`** ranks: chain > forkchain > collider ≈ fork > hub.
4. **Per-target asymmetry**:
   - In `G3-fork`, target x0 (root) cannot have body-parent F1 ≠ NaN (no parents); we report `offgraph_rate` and rule complexity instead.
   - In `G3-collider`, x2 should achieve `body_parent_recall ≤ 0.5` even when solved (often only one of two parents is cited).
   - In `G4-hub`, child targets behave similarly to each other — a useful internal control.

---

## 3. DGPs included

Same DGP zoo as E02 (continuous): `G3-chain`, `G3-fork`, `G3-collider`, `G4-forkchain`, `G4-hub`.

A **discrete companion** subsection uses `E02-disc`'s data if available (same DGPs, `graph_type: discrete`). Otherwise the companion is skipped.

---

## 4. Factors varied (the grid)

E04 introduces **no new factor**. The "grid" is the cross-section of E02's grid at fixed (n, knobs):

- `dgp` ∈ DGP zoo.
- `target` ∈ all variables of each DGP.
- `seed` ∈ 0…29 (aggregated over).

All other factors fixed to E02 defaults (n=25, bins=2, etc.).

---

## 5. Factors held fixed

Identical to E02. Listed here for self-contained readability:

- graph_type: continuous; noise: Gaussian, scale 1.0; bins 2 quantile; example_split median.
- folding_steps 15, folding_mode nd; prolog_timeout 120 s.

---

## 6. Seeds

**30 (reused from E02).** No new Prolog calls.

---

## 7. Metrics & outputs

### Aggregate

`groupby(dgp, target)`; reduce over seed via median + IQR for ratios, fraction-mean for outcome categories.

Two structural views:

1. **DGP-level view**: pool over targets within DGP for a coarse comparison.
2. **(DGP, target)-level view**: the standard fine-grained view used for F5.

### Figures

- **F5 — Structural-sweep bar chart**:
  - Left panel: `body_parent_f1` (median, IQR error bars) per (DGP, target). Bars grouped by DGP.
  - Right panel: `offgraph_rate` (median, IQR) per (DGP, target).
  - Annotation per bar: `fraction_solved (#solved/30)`.
  - Bars with `fraction_solved == 0` rendered as ghosts.
- **F-app-1 — Discrete companion** (appendix). Same layout as F5, using `E02-disc` data.

### Tables

- An appendix table T-app-E04 lists, per (DGP, target): `body_parent_f1` median, IQR, `offgraph_rate` median, `fraction_solved`, `n_seeds_solved`, and median `n_target_rules`.

---

## 8. "Configuration"

No YAML — E04 is purely an analysis step. The structural view is produced by `analysis.py` functions:

```python
# causal/experiments/analysis.py
def aggregate_structural(df: pd.DataFrame) -> pd.DataFrame: ...
def plot_structural_bars(agg, out_dir: Path) -> Path: ...   # writes F5
```

The pipeline is:

```bash
python -m causal.experiments.analysis \
    --experiment E02 \
    [--include-experiment E02_disc] \
    --figure F5
```

---

## 9. Estimated cost

Negligible — single-digit seconds. The cost was paid by E02.

---

## 10. Pass / learn criteria

E04 passes if:

- [ ] F5 renders from `results.parquet` (E02) via `analysis.py`.
- [ ] Each bar's annotation matches the underlying `fraction_solved` rounded to two decimals.
- [ ] The discrete companion (F-app-1) renders if `E02-disc` is available; otherwise the missing data is logged.

Learn:

- The actual structural ranking of `body_parent_f1` and `offgraph_rate` — do they match the predicted ordering?
- Which (DGP, target) combinations are the most informative for §6's discussion of failure modes.

---

## 11. Connection to other experiments

- **Reuses:** E02 `results.parquet`. Optionally `E02-disc`.
- **Feeds:** F5 (report §5.2.3); structural commentary in §6.
- **Depends on:** E02 complete and validated.
- **Blocks:** nothing — E04 is a leaf experiment.

---

## 12. Risks & contingencies

| # | Risk | Mitigation |
|---|------|------------|
| R-E04-1 | The structural ranking does not match the hypothesis (e.g. fork outperforms chain). | Report honestly; this is a *finding*. The discussion in §6 is rewritten accordingly. |
| R-E04-2 | Too many ghost bars (`fraction_solved == 0`) makes F5 illegible. | Add a fraction_solved panel as a third sub-plot; consider lowering n in a follow-up but not in interim. |
| R-E04-3 | Internal control fails: `G4-hub` children do **not** behave similarly. | Add a one-paragraph note: heterogeneity across "equivalent" targets is itself meaningful information about the learner's stability. |

---

## 13. Open questions

- Should the per-target view in F5 be reordered by `body_parent_f1` median for readability, rather than by node index? *Default: ordered by node index within DGP for consistency across panels.*
- Should we include a "DGP-pooled" summary bar per DGP alongside the per-target bars? *Default: yes — adds a coarse comparison without doubling the figure size.*
- Should we visualise root-target cells (where `body_parent_recall = NaN`) at all? *Default: yes, using `offgraph_rate` only; mark explicitly in the caption.*

Resolutions append to the Decisions log in `EXPERIMENTS_PLAN.md`.
