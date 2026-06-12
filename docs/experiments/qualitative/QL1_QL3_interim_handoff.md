# QL1–QL3 interim-report handoff pack

> **Scope guard.** The qualitative investigations evaluate **target-wise parent-set
> recovery** under the current `aba_asp/causal` **ABA Learning bridge**. They do **not**
> evaluate full Russo-style Causal ABA, graph recovery, d-separation reasoning,
> `arr`/`noe`/`indep` assumptions, or stable-extension-as-DAG machinery. Throughout, prefer
> "parent-set recovery", "learned target-rule body", and "causal-adjacent structure" over
> "learned causality". Metrics diagnose alignment between learned rule bodies and known
> direct parents of `x2`; they do **not** prove causal discovery.

> **Status / dependency note.** This pack synthesises **QL1 (QI-001)**, **QL2 (QI-002)**,
> and **QL3 (QI-003)** only. **QL4 (QI-004)** is running elsewhere; its output directory
> (`causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20/`) and generated summary
> (`docs/experiments/qualitative/QI004_scaled_motifs_n20_summary.md`) do not yet exist.
> All QL4 entries below are **placeholders**. Do not write final conclusions that depend on
> QL4.

> **Naming.** The report-side labels QL1/QL2/QL3/QL4 map to the repo experiment IDs
> QI-001 / QI-002 / QI-003 / QI-004 respectively.

---

## 1. Inventory table (QL1–QL3)

| Investigation | Purpose | Config | Output dir | Summary | Status | Role in report |
|---|---|---|---|---|---|---|
| **QL1 = QI-001** (`QI001_motifs_modes`) | Initial motif-by-data-mode probe of parent-set recovery for `x2` across 3 motifs × 3 data modes | `causal/configs/experiments/QI001_motifs_modes.yaml` | `causal/outputs/aba_learning/grid/QI001_motifs_modes/` (exists; 9 cells) | `docs/experiments/qualitative/QI-001_summary.md` | **run** (9/9 solved); interpretation template pending | First qualitative probe; exposes encoding sensitivity and the x0/first-column confound |
| **QL2 = QI-002** (`QI002_minimal_motifs`) | Principled minimal **noiseless complete truth-table** baseline: is the perfect parent rule learnable in the ideal case? | `causal/configs/experiments/QI002_minimal_motifs.yaml` | `causal/outputs/aba_learning/grid/QI002_minimal_motifs/` (exists; 6 cells) | `docs/experiments/qualitative/QI002_minimal_motifs_summary.md` | **run** (clean-recovery 0.5 over 6 cells); interpretation pending | Best-case learnability baseline; removes QI-001's unjustified tiny-table confound |
| **QL3 = QI-003** (`QI003_scaled_motifs`) | Scaled noisy run (`n=100`) with **parent-position controls** to break the x0 confound | `causal/configs/experiments/QI003_scaled_motifs.yaml` | `causal/outputs/aba_learning/grid/QI003_scaled_motifs/` (exists; partial cells) | `docs/experiments/qualitative/QI003_scaled_motifs_summary.md` (shows "pending run" — not regenerated for the partial attempt) | **run — computational-feasibility attempt; 0 cells solved (timeouts + binary encoding errors); superseded for evidence by QL4** | Documents a feasibility wall (`n=100`) that motivates the reduced-`n` QL4 design |

### Supporting artefacts per investigation

**QL1 / QI-001**
- High-level record: `docs/experiments/qualitative/QI-001.md`
- Fixtures: `causal/experiments/handcrafted_qi001.py` (registered in `causal/experiments/handcrafted.py`)
- Fixture tests: `causal/tests/test_qi001_fixtures.py`; summary tests: `causal/tests/test_qi001_summary.py`
- Summary script: `causal/scripts/qi001_qualitative_summary.py`
- Operational dossier: `docs/experiments/qualitative/QI001_motifs_modes/` (`README.md`, `run_log.md`, `interpretation.md`, `artefacts.md`)
- Per-cell run dirs: `causal/outputs/aba_learning/grid/QI001_motifs_modes/cells/<run_id>/`

**QL2 / QI-002**
- High-level record: `docs/experiments/qualitative/QI-002.md`
- Fixtures: `causal/experiments/handcrafted_qi002.py`; tests: `causal/tests/test_qi002_fixtures.py`
- Summary script: `causal/scripts/motif_recovery_summary.py`
- Operational dossier: `docs/experiments/qualitative/QI002_minimal_motifs/` (`README.md`, `run_log.md`, `interpretation.md`, `metrics.md`, `decision_record.md`, `artefacts.md`)

**QL3 / QI-003**
- High-level record: `docs/experiments/qualitative/QI-003.md`
- Fixtures: `causal/experiments/handcrafted_qi003.py`; tests: `causal/tests/test_qi003_fixtures.py`
- Summary script: `causal/scripts/motif_recovery_summary.py`
- Operational dossier: `docs/experiments/qualitative/QI003_scaled_motifs/` (`README.md`, `run_log.md`, `interpretation.md`, `metrics.md`, `decision_record.md`, `artefacts.md`)

**QL4 / QI-004 (placeholder — running elsewhere)**
- High-level record: `docs/experiments/qualitative/QI-004.md`
- Config: `causal/configs/experiments/QI004_scaled_motifs_n20.yaml` (`n=20`, `prolog_timeout_s=300`)
- Fixtures: `causal/experiments/handcrafted_qi004.py`; tests: `causal/tests/test_qi004_fixtures.py`
- Operational dossier: `docs/experiments/qualitative/QI004_scaled_motifs_n20/`
- Output dir & summary: **not yet present.**

---

## 2. Report-ready factual summaries

All three share: target `x2` only; target excluded from BK; learner config = default
non-deterministic folding (`folding_mode: nd`, `folding_steps: 15`); `graph_type:
handcrafted_table`; grid `seed: [0]`; `bins: 3`, `bin_strategy: uniform` for continuous
cells. Conda env `aba-asp`; SWI-Prolog 10.0.2; clingo 5.8.0.

### QL1 / QI-001 — initial motif-by-data-mode run

- **Research question.** Do learned `x2` target-rule bodies coincide with the encoded
  direct parents of `x2` across 3 canonical 3-node motifs (chain, fork, collider) × 3 data
  representations (binary, categorical-3, continuous-3-bin)?
- **Why introduced.** First qualitative feasibility probe: inspect what the bridge actually
  recovers on small controlled cases, holding the motif fixed while varying the encoding.
- **Design.** 3 motifs × 3 data modes × target `x2` = **9 cells**.
- **Data modes.** binary `{0,1}` → bare predicates `x0(A)`; categorical-3 → `x0_val_v(A)`;
  continuous → 3 uniform-bin predicates `x0_binK(A)`.
- **Motifs / parents.** chain `x0→x1→x2` (parents `{x1}`); fork `x0→x1, x0→x2` (parents
  `{x0}`); collider `x0→x2, x1→x2` (parents `{x0,x1}`).
- **Sample size.** 4–5 rows per fixture (deterministic, hand-built; **not** derived from a
  separability requirement — a known design weakness).
- **Target variable.** `x2`. Positive class: `x2==1` (binary), `x2==2` (cat3), `x2>=0` (cont3).
- **Learner settings.** nd folding, `folding_steps: 15`, `prolog_timeout_s: 120`.
- **Metrics used.** outcome category; rule-level `body_parent_precision/recall/f1`;
  recovered body variables; recovery classification; Python-Horn and Prolog-aware coverage;
  assumptions/contraries counts. (QI-001 predates the stricter `clean_recovery` /
  variable-level metrics introduced for QI-002+.)
- **Raw result pattern** (from `QI-001_summary.md`; all 9 cells `solved`):
  - **fork**: `exact_parent_recovery` in all 3 modes — but the fork parent **is** `x0`, so
    this is confounded with a first-column preference.
  - **collider**: `binary` exact `{x0,x1}`; `cat3` and `cont3` `parent_subset` (recovered
    `{x0}` only, missing `x1`).
  - **chain**: never cleanly recovers `{x1}` — `binary` `parent_superset` `{x0,x1}`;
    `cat3` and `cont3` `non_parent_or_proxy` (recovered `{x0}`, which is the ancestor, not
    the parent).
  - Where assumptions were introduced (chain/collider non-binary cells), Prolog-aware
    positive coverage frequently dropped to 0.0 despite a `solved` outcome.
- **Known caveats.** (i) x0/first-column **confound** unbroken: "found the cause" and
  "prefers `x0`" are indistinguishable for fork (parent = `x0`) and chain (parent ≠ `x0`).
  (ii) Tiny, unjustified `n` (4–5 rows): the true parent is not guaranteed to be the unique
  perfect rule. (iii) `chain_cont3` fixture was degenerate (`x0`,`x1` identical), making
  parent-vs-ancestor undecidable. (iv) Per-cell `interpretation.md` is still a template
  (not yet hand-filled).

### QL2 / QI-002 — principled minimal truth-table baseline

- **Research question.** Under **complete, noiseless truth tables** where the true parent
  of `x2` is the unique zero-error separator, does the bridge learn an `x2` rule whose body
  variables equal the true direct parents?
- **Why introduced.** Replaces QI-001's ad-hoc 4–5 row tables with the smallest design that
  *guarantees* the parent is the unique perfect single-column rule — the "can it be learned
  at all, in the best case?" baseline.
- **Design.** 3 motifs × 2 data modes (binary, cat3) × target `x2` = **6 cells**. Complete
  factorial over `(x0,x1)` repeated ×2.
- **Data modes.** binary, categorical-3 (no continuous cells in QL2).
- **Motifs / parents.** Same canonical orientation as QI-001 (chain `{x1}`, fork `{x0}`,
  collider `{x0,x1}`).
- **Sample size.** binary **8 rows** (`2^2`×2); cat3 **18 rows** (`3^2`×2). Noiseless;
  targets are deterministic functions of the parents (chain `x2=x1`; fork `x2=x0`; collider
  `x2=x0 AND x1` binary, `x2=max(x0,x1)` cat3).
- **Target variable.** `x2`. Positive class: `x2==1` (binary), `x2==2` (cat3).
- **Learner settings.** nd folding, `folding_steps: 15`, `prolog_timeout_s: 120`.
- **Metrics used (headline).** `clean_recovery` (strict: recovered set == parent set);
  variable-level `var_parent_precision/recall/jaccard`; plus `ancestor_only_rate`,
  `body_parent_recall`, coverage, outcome, assumptions/contraries, folding tokens.
  `body_parent_f1` de-emphasised.
- **Raw result pattern** (from `QI002_minimal_motifs_summary.md`): overall clean-recovery
  **0.500 (3/6)**; binary **0.667 (2/3)**, cat3 **0.333 (1/3)**.
  - `qi002_chain_binary`: `exact_parent_recovery` `{x1}`, clean=1 (note: improves on
    QI-001's chain_binary superset — the complete table fixes it).
  - `qi002_fork_binary`: exact `{x0}`, clean=1.
  - `qi002_collider_binary`: **`completed_no_solution`** (no `x2` rule learned), clean=0.
  - `qi002_chain_cat3`: `non_parent_or_proxy` `{x0}` (ancestor), clean=0,
    `ancestor_only_rate=1.0`, 3 assumptions introduced.
  - `qi002_fork_cat3`: exact `{x0}`, clean=1.
  - `qi002_collider_cat3`: `parent_subset` `{x0}` only, clean=0, var P/R/J 1.0/0.5/0.5.
- **Known caveats.** (i) **Canonical orientation only** → does *not* break the x0 confound
  (a pure `x0`-preferrer looks right on fork, wrong on chain). (ii) Even in the ideal
  noiseless case, the collider is not cleanly recovered (binary: no solution; cat3: subset),
  and cat3 chain recovers the ancestor not the parent. (iii) `interpretation.md` still a
  template.

### QL3 / QI-003 — scaled noisy run with parent-position controls (feasibility attempt)

- **Research question.** With `n=100` noisy samples and the true parent placed in **either**
  column, does the bridge recover the true parent regardless of position, across
  binary/cat3/cont3?
- **Why introduced.** Adds (a) realistic scale + noise and (b) **parent-position variants**
  that generate chain and fork in both orientations, so a learner that merely prefers `x0`
  fails the `*_x1parent` cells — the decision-critical confound check.
- **Design.** 5 structural configs × 3 data modes × target `x2` = **15 cells**. Configs:
  `chain_x1parent {x1}`, `chain_x0parent {x0}`, `fork_x0parent {x0}`, `fork_x1parent {x1}`,
  `collider {x0,x1}`.
- **Data modes.** binary, cat3, cont3 (3 uniform bins).
- **Sample size.** `n = 100` per cell; mild stochastic noise (chain mid-flip ~0.2, target
  ~0.1 / Gaussian; fork sibling ~0.2 vs target ~0.1; collider independent parents).
  Deterministic per-fixture internal RNG seed.
- **Target variable.** `x2`. Positive class: `x2==1` (binary), `x2==2` (cat3), `x2>=0` (cont3).
- **Learner settings.** nd folding, `folding_steps: 15`, `prolog_timeout_s: 120`.
- **Metrics used (headline).** Same as QL2 (`clean_recovery` + variable-level P/R/Jaccard),
  read as the `*_x0parent` vs `*_x1parent` confound comparison; plus continuous bin-health.
- **Raw result pattern — feasibility outcome only (NOT recovery evidence).** The `n=100`
  run was **manually aborted after ~17 minutes**; **0 cells solved**. Of the 13 cells with
  `metrics.json` at abort:
  - **8 `timeout`** (Prolog exceeded 120 s) — all cat3/cont3 cells that ran;
  - **5 `error`** — all binary cells: the binary "positive-cases-only" BK encoding cannot
    declare a sample-id constant for an all-zero-feature row (`x0=0,x1=0`); target noise can
    flip such a row to a positive example whose constant is then undeclared, tripping
    `check_ep_consts_aux` in `aba_asp.pl` (`ERROR: unknown constant`, `wall_clock_s≈0.05`).
  - The generated `QI003_scaled_motifs_summary.md` still reports "pending run (no grid
    artefacts found)" because it was **not regenerated** for the partial attempt; partial
    per-cell artefacts nonetheless exist under `.../QI003_scaled_motifs/cells/`.
- **Known caveats.** QL3 yields **no parent-recovery evidence** — only two recorded failure
  modes (timeout for cat3/cont3; binary encoding limitation). It is preserved unchanged as a
  recorded feasibility wall. The conceptually identical but feasible follow-up is **QL4 /
  QI-004** (`n=20`, `prolog_timeout_s=300`). The binary all-zero-positive limitation is a
  recorded known limitation, deliberately **not** fixed in this line of runs.

---

## 3. The qualitative sequence (why each run followed the last)

1. **QL1 (QI-001) exposed initial behaviour** across the motif × data-mode grid. All 9 cells
   solved, but recovery was uneven: fork recovered cleanly in every mode, the collider was
   recovered only partially outside binary, and the chain essentially never recovered its
   true parent `x1` (it cited `x0` instead). Two **design** problems surfaced (independent of
   per-cell interpretation): the **x0/first-column confound** (fork's parent *is* `x0`, so a
   positional preference and genuine parent recovery are indistinguishable) and an
   **unjustified tiny sample size** (4–5 rows, so the true parent was not guaranteed to be
   the unique perfect rule).

2. **QL2 (QI-002) was introduced as a stricter minimal baseline** to remove the tiny-table
   confound from QL1. Using complete, noiseless truth tables (8 rows binary, 18 rows cat3),
   the true parent is the *unique* zero-error separator, so a perfect causal rule is
   learnable **in principle**. This isolates "can the perfect rule be learned at all, in the
   best case?". Result: clean recovery on only **half** the cells (binary 2/3, cat3 1/3),
   with the collider failing even noiselessly (binary: no solution; cat3: subset) and cat3
   chain recovering the ancestor. QL2 deliberately keeps the **canonical orientation only**,
   so it does **not** break the x0 confound — that is QL3/QL4's job.

3. **QL3 (QI-003) attempted a larger, noisier, confound-controlled setting** (`n=100`, both
   parent orientations) to test whether recovery tracks the true parent column rather than
   `x0`. It hit a **computational-feasibility wall**: cat3/cont3 cells timed out at 120 s and
   binary cells failed instantly on the all-zero-positive encoding limitation; **0 cells
   solved**. QL3 therefore contributes a documented feasibility/limitation result, not
   recovery evidence, and motivated a reduced-`n` redesign.

4. **QL4 (QI-004) is pending** (running elsewhere): same conceptual design as QL3 but
   `n=20` and `prolog_timeout_s=300` for tractability. It is intended to decide how much can
   be said about larger-sample continuous/discretised behaviour **and** to finally run the
   `*_x0parent` vs `*_x1parent` confound check. **QL4 is not yet known and must not be
   treated as known.**

---

## 4. Metric justification (qualitative investigation)

> These metrics diagnose **alignment between learned `x2` rule bodies and the known direct
> parents of `x2`**. They do **not** prove causal discovery, edge orientation, or DAG
> recovery. Full definitions: `causal/aa-plans/METRICS.md` (§3.4, §3.4b).

| Metric | What it measures | Why relevant | How to interpret | What it cannot show |
|---|---|---|---|---|
| **solved / timeout / no solution** (`outcome`) | Whether the learner produced a usable δ-rule set, hit the Prolog timeout, or returned no solution | Feasibility precondition; "no solution" is a real result, not an error | `solved` = rules to analyse; `timeout`/`error`/`completed_no_solution` = recovery metrics are 0/NaN and should not be read as evidence | Says nothing about *correctness* of a solved rule |
| **exact parent recovery** (classification) | Recovered body-variable set equals the parent set exactly | The qualitative success label per cell | One label per cell; `parent_subset`/`superset`/`non_parent_or_proxy`/`mixed`/`rote_or_sample_specific` describe near-misses | Does not quantify *how* wrong a near-miss is (use the variable-level metrics) |
| **clean_recovery** (`{0,1}`) | Strict flag: `1` iff recovered set == true parents (parents non-empty) | Aggregates into a clean-recovery rate across cells; the headline QL2+ success metric | Mean over cells = fraction perfectly recovered | Binary; hides partial credit and the *type* of error |
| **recovered body variables** | Union of base variables cited across non-trivial `x2` rules (suffixes stripped, e.g. `x0_bin0→x0`) | The raw object every other metric is computed from | Compare directly against expected parents | Predictor membership only — **not** edge direction |
| **var_parent_precision** | \|recovered ∩ parents\| / \|recovered\| | Penalises ancestor/off-graph/sibling contamination | 1.0 = no spurious variables; <1 = extra non-parents | NaN when nothing recovered; ignores missed parents |
| **var_parent_recall** | \|recovered ∩ parents\| / \|parents\| | Detects missing parents (e.g. collider citing only one parent) | 1.0 = all parents present; 0.5 = half (typical collider subset) | NaN for root targets; ignores spurious extras |
| **var_parent_jaccard** | \|recovered ∩ parents\| / \|recovered ∪ parents\| | Single overlap score combining both error types | 1.0 = exact; lower = either misses or extras | Does not say which error type dominates |
| **positive coverage** (`cov_*_pos`) | Fraction of `E+` the learned framework accepts | Whether the rule actually fires on intended positives | Low pos-coverage under a `solved` outcome is a red flag (seen in QL1 assumption cells) | Coverage ≠ parent correctness; a proxy can cover well |
| **negative exclusion** (`cov_*_neg`) | Fraction of `E-` correctly rejected | Whether the rule over-generalises | 1.0 = no false positives | Same caveat: coverage is behavioural, not structural |
| **learned target rules** (`x2(A) :- …`) | The actual rule bodies the learner produced | The qualitative object of the whole investigation; narratable examples | Inspect body variables and structure directly | A correct-looking body can still be a positional/proxy artefact |
| **assumptions / contraries** (`n_assumptions`, `n_contraries`) | ABA Learning structure (`alpha_*`, `c_alpha_*`) introduced via Assumption Introduction | Indicates the learner used exception machinery rather than a plain Horn rule | More assumptions ≈ more complex/conditional rules; often co-occurs with low Prolog-aware pos-coverage | Does not by itself indicate correctness or causality |
| **bin health / bin occupancy** (continuous) | Whether all 3 uniform bins are non-empty for `x0`/`x1` | Sparse/empty bins make the continuous predicate vocabulary degenerate | All bins populated = vocabulary trustworthy | Healthy bins don't imply correct recovery; only that the encoding is non-degenerate |
| **sample-specific / rote-looking rules** (`rote_or_sample_specific`, triviality counts) | Rules that cite no base variables or are head-equivalent | Distinguishes genuine generalisation from memorisation | Such rules mean recovery is effectively null even if "solved" | Cannot quantify partial generalisation |

**De-emphasised:** `body_parent_f1` — mixes a rule-level precision with a variable-level
recall (different denominators) and is lenient (a rule citing a parent *and* an ancestor
still scores a full parent hit). Retained in the schema for cross-experiment stability but
omitted from the motif-recovery summaries; prefer the variable-level metrics.

**Not computed (reserved):** graph-level skeleton/direction/bridge metrics
(`skel_*`, `dir_*`, `shd`, `bridge_*`) are NaN/None placeholders — they must **not** be
cited as results.

---

## 5. Interim-report section outline (qualitative half of Experimentation)

> Provisional bullets — *what to write*, not finished prose. Final prose is drafted by
> ChatGPT from reviewed records and checked against `docs/report/claims_ledger.md`.

```latex
\subsection{Qualitative investigation: target-wise parent-set recovery}
```

- **Aim and scope**
  - State the object: target-wise recovery of `x2`'s direct parents via the ABA Learning bridge.
  - Explicitly *not* full Causal ABA / graph recovery / d-separation / stable-extension-as-DAG.
  - Define the success notion: learned `x2` rule body variables == true direct parents.
- **Experimental setup**
  - 3 canonical 3-node motifs (chain/fork/collider); target `x2`; target excluded from BK.
  - Data modes: binary (bare predicates), categorical-3 (`_val_v`), continuous-3-bin (`_binK`).
  - Learner: inherited ABALearn, nd folding, `folding_steps: 15`; SWI-Prolog/clingo; env `aba-asp`.
  - Fixed E+/E- per fixture; deterministic handcrafted tables.
- **Metrics and interpretation rule**
  - Lead with `clean_recovery` + variable-level precision/recall/Jaccard (QL2+); QL1 used rule-level body-parent metrics.
  - State the interpretation rule: alignment with known parents, **not** causal discovery; coverage is behavioural; reserved graph metrics are not computed.
- **QL1: initial motif-by-data-mode probe (QI-001)**
  - 9 cells, all solved; fork clean everywhere, collider partial outside binary, chain cites `x0` not `x1`.
  - Surface the two design limitations: x0/first-column confound; unjustified tiny `n`.
- **QL2: principled minimal baseline (QI-002)**
  - Complete noiseless truth tables; perfect rule learnable in principle.
  - Clean recovery 3/6 (binary 2/3, cat3 1/3); collider fails even noiselessly; canonical orientation only (confound still open).
- **QL3/QL4: scaled continuous/discretisation check (QI-003 → QI-004)**
  - QL3: `n=100` feasibility wall — timeouts (cat3/cont3) + binary encoding errors; 0 solved.
  - QL4 (**placeholder**): `n=20`, `prolog_timeout_s=300`; will run the `*_x0parent` vs `*_x1parent` confound check. Mark all QL4 numbers as pending.
- **Interim interpretation** *(provisional; QL4-independent only)*
  - Recovery is **encoding- and motif-sensitive**, not uniform; binary is friendliest.
  - Even ideal noiseless conditions do not guarantee clean recovery (collider, cat3 chain).
  - The x0 confound is acknowledged but not yet empirically broken (pending QL4).
- **Limitations**
  - Bridge ≠ Causal ABA; predictor-set, not oriented edges.
  - Binary all-zero-positive encoding limitation; Prolog scaling limits at `n=100`.
  - Per-cell `interpretation.md` files are templates; classifications come from the generated summaries.
- **Decision for next quantitative work**
  - Whether the confound is broken (QL4) gates any quantitative parent-recovery benchmarking (cf. QN-001).
  - Note candidate fixes recorded but deferred: binary encoding limitation; learner timeout budget; greedy-vs-nd comparison.

---

## 6. Provisional claims supported by QL1–QL3

*(Provisional, QL4-independent. Verify against `docs/report/claims_ledger.md` before use.)*

- The current ABA Learning bridge **runs end-to-end** on small controlled motif fixtures and
  produces inspectable learned `x2` target rules (QL1: 9/9 solved; QL2: 5/6 solved).
- Parent-set recovery is **sensitive to data encoding and motif**: under canonical
  orientation, fork (parent `x0`) recovers cleanly across modes, while chain (parent `x1`)
  and collider recover poorly outside the binary mode (QL1, QL2).
- **Even in the ideal noiseless complete-truth-table case, clean recovery is not guaranteed**
  (QL2: clean_recovery 0.5; collider binary returns no solution; cat3 chain recovers the
  ancestor `x0`, not the parent `x1`).
- The complete-truth-table design **fixes the QL1 chain_binary superset** (QL2 chain_binary
  is exact `{x1}`), showing some QL1 failures were artefacts of tiny tables.
- The `n=100` setting is **computationally infeasible** under the current learner/timeout
  budget (QL3: 0 solved; 8 timeouts, 5 binary encoding errors), and the binary
  positive-cases-only BK encoding has a **documented all-zero-positive limitation**.

## 7. Claims NOT supported (explicitly excluded)

- ❌ The implementation performs full Russo-style **Causal ABA** (no `arr`/`noe`/`indep`,
  no d-separation, no stable-extension-as-DAG in the code path).
- ❌ **Causal discovery / DAG recovery** of the motifs.
- ❌ Learned rule **direction is causal** (bodies are predictor sets, not oriented edges).
- ❌ The **x0/first-column confound is broken** by QL1–QL3 (QL1/QL2 are confounded by design;
  QL3 produced no solved cells). This is the open question for QL4.
- ❌ Any conclusion about **larger-sample continuous/discretised** recovery (blocked on QL4).
- ❌ Anything derived from the **reserved** graph-level metrics (`skel_*`, `dir_*`, `shd`,
  `bridge_*`) — not computed.
- ❌ Noise is represented as ABA exceptions/assumptions in a principled way (assumptions seen
  in QL1/QL2 are not validated as a noise model).

## 8. Limitations

- **Conceptual.** The bridge is target-wise learned-rule / parent-set recovery, best treated
  as predictive-association recovery that *may* align with parents; it is not Causal ABA.
- **Confound (open).** x0/first-column preference vs genuine parent recovery is not yet
  distinguished (QL1/QL2 canonical-only; QL3 unsolved).
- **Scale.** Prolog learning does not complete within 120 s at `n=100` for cat3/cont3 cells.
- **Encoding.** Binary all-zero-positive rows can trip `check_ep_consts_aux`
  (`unknown constant`); recorded, not fixed.
- **Coverage vs structure.** High coverage can co-exist with wrong/partial parent sets; some
  QL1 `solved` cells show 0.0 Prolog-aware positive coverage.
- **Documentation state.** Per-cell `interpretation.md` files remain templates; the factual
  classifications in this pack are taken from the generated summaries, not hand interpretation.
- **Determinism / breadth.** Single seed (`seed: [0]`); deterministic fixtures; no
  greedy-vs-nd comparison (that is QN-001).

## 9. Exact artefact paths (consolidated)

**Configs**
- `causal/configs/experiments/QI001_motifs_modes.yaml`
- `causal/configs/experiments/QI002_minimal_motifs.yaml`
- `causal/configs/experiments/QI003_scaled_motifs.yaml`
- `causal/configs/experiments/QI004_scaled_motifs_n20.yaml` *(QL4)*

**Fixtures**
- `causal/experiments/handcrafted_qi001.py`, `..._qi002.py`, `..._qi003.py`, `..._qi004.py`
- Registration: `causal/experiments/handcrafted.py`

**Generated summaries**
- `docs/experiments/qualitative/QI-001_summary.md`
- `docs/experiments/qualitative/QI002_minimal_motifs_summary.md`
- `docs/experiments/qualitative/QI003_scaled_motifs_summary.md` *(shows "pending"; not regenerated for partial run)*
- `docs/experiments/qualitative/QI004_scaled_motifs_n20_summary.md` *(QL4 — does not exist yet)*

**High-level records**
- `docs/experiments/qualitative/QI-001.md`, `QI-002.md`, `QI-003.md`, `QI-004.md`

**Operational dossiers** (`README.md` + `run_log.md` + `interpretation.md` [+ `metrics.md`, `decision_record.md`, `artefacts.md`])
- `docs/experiments/qualitative/QI001_motifs_modes/`
- `docs/experiments/qualitative/QI002_minimal_motifs/`
- `docs/experiments/qualitative/QI003_scaled_motifs/`
- `docs/experiments/qualitative/QI004_scaled_motifs_n20/` *(QL4)*

**Run outputs**
- `causal/outputs/aba_learning/grid/QI001_motifs_modes/` (9 cells, complete)
- `causal/outputs/aba_learning/grid/QI002_minimal_motifs/` (6 cells, complete)
- `causal/outputs/aba_learning/grid/QI003_scaled_motifs/` (partial; feasibility attempt)
- `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20/` *(QL4 — not yet present)*

**Metrics & scripts**
- `causal/metrics.py`; spec `causal/aa-plans/METRICS.md`
- `causal/scripts/qi001_qualitative_summary.py`; `causal/scripts/motif_recovery_summary.py`

**Index / register**
- `docs/experiments/experiment_index.md`; `docs/research/experiment_register.md`

## 10. QL4 (QI-004) placeholders — fill after the run completes

- [ ] **Outcome distribution** over 15 cells (solved / timeout / error / no-solution): `TBD`
- [ ] **Overall clean_recovery rate**, and by data mode (binary / cat3 / cont3): `TBD`
- [ ] **Confound check**: `*_x0parent` vs `*_x1parent` `clean_recovery` per motif (chain, fork) × mode — verdict: parent-tracking vs x0-positional: `TBD`
- [ ] **Continuous bin-health** at `n=20` (all 3 bins non-empty for `x0`/`x1`): `TBD`
- [ ] **Binary all-zero-positive limitation** recurrence at `n=20`: `TBD`
- [ ] **Headline learned-rule examples** (narratable): `TBD`
- [ ] Path checks: `causal/outputs/aba_learning/grid/QI004_scaled_motifs_n20/` and `docs/experiments/qualitative/QI004_scaled_motifs_n20_summary.md` exist: `TBD`

## 11. Questions for Samuel / ChatGPT before final report writing

1. **Label mapping.** Should the report use QL1–QL4 or the repo QI-001…QI-004 IDs (or both, with a mapping note)? This pack assumes QL↔QI.
2. **QL1 metric basis.** QL1 was scored with rule-level `body_parent_*`; QL2+ use
   `clean_recovery`/variable-level. Should QL1 be re-described against the stricter metric
   for consistency, or reported as-is with a footnote?
3. **QL3 framing.** Confirm QL3 should be presented purely as a *computational-feasibility
   wall* (no recovery claims) that motivates QL4 — is that the intended narrative?
4. **Confound emphasis.** How prominently should the unbroken x0/first-column confound be
   framed in the interim report, given it is only resolvable by QL4?
5. **Collider failure.** The collider under-recovers even noiselessly (QL2). Worth a
   dedicated paragraph, or fold into the encoding-sensitivity point?
6. **Scope sentence.** Confirm the exact wording for "parent-set recovery, not causal
   discovery" to standardise across the report (align with `claims_ledger.md`).
7. **Binary encoding limitation.** Report it as a methods caveat now, or defer until a fix is
   scoped?
8. **Interpretation files.** Do you want the per-cell `interpretation.md` templates filled
   before ChatGPT drafts, or is this pack's summary-derived synthesis sufficient for the
   interim?
