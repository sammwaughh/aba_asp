# QI-001 interpretation (QI001_motifs_modes)

> QI-001 is a qualitative parent-set recovery investigation using the current ABA Learning bridge. It is not full Russo-style Causal ABA, graph recovery, d-separation reasoning, or stable-extension-as-DAG machinery.

Status: pending review. The first ABALearn run completed on 2026-06-12 (9/9 cells `solved`); see `run_log.md` and `../QI-001_summary.md`. This is a human-filled template — interpretation has not been written yet. Complete one section per cell after reviewing `../QI-001_summary.md` and the per-cell artefacts (see `artefacts.md`). Do not fill these in from assumptions; copy learned rules exactly from `bk.sol.aba` / the generated summary.

## Classification vocabulary

Use one label per cell (matching the summary script):

- `exact_parent_recovery` — recovered body variables equal the expected parents.
- `parent_subset` — recovered variables are all parents but miss at least one.
- `parent_superset` — recovered variables include all parents plus extras.
- `non_parent_or_proxy` — recovered variables are disjoint from the parents.
- `mixed_parent_and_non_parent` — some parents and some non-parents recovered.
- `rote_or_sample_specific` — target rules exist but cite no base variables (sample-specific bodies).
- `no_solution` — learner produced no usable solution.
- `no_output_yet` — no metrics for this cell yet.
- `parser_or_metric_failure` — solved but rules/metrics could not be parsed.

---

## qi001_chain_binary (chain, binary 0/1)

- Expected parents of x2: {x1}
- Learned rules:

```text
TBD
```

- Recovered body variables: `TBD`
- Classification: `TBD`
- Interpretation: `TBD`
- Limitation: `TBD`
- Next decision: `TBD`

---

## qi001_fork_binary (fork, binary 0/1)

- Expected parents of x2: {x0}
- Learned rules:

```text
TBD
```

- Recovered body variables: `TBD`
- Classification: `TBD`
- Interpretation: `TBD`
- Limitation: `TBD`
- Next decision: `TBD`

---

## qi001_collider_binary (collider, binary 0/1)

- Expected parents of x2: {x0, x1}
- Learned rules:

```text
TBD
```

- Recovered body variables: `TBD`
- Classification: `TBD`
- Interpretation: `TBD`
- Limitation: `TBD`
- Next decision: `TBD`

---

## qi001_chain_cat3 (chain, categorical 3 values)

- Expected parents of x2: {x1}
- Learned rules:

```text
TBD
```

- Recovered body variables: `TBD`
- Classification: `TBD`
- Interpretation: `TBD`
- Limitation: `TBD`
- Next decision: `TBD`

---

## qi001_fork_cat3 (fork, categorical 3 values)

- Expected parents of x2: {x0}
- Learned rules:

```text
TBD
```

- Recovered body variables: `TBD`
- Classification: `TBD`
- Interpretation: `TBD`
- Limitation: `TBD`
- Next decision: `TBD`

---

## qi001_collider_cat3 (collider, categorical 3 values)

- Expected parents of x2: {x0, x1}
- Learned rules:

```text
TBD
```

- Recovered body variables: `TBD`
- Classification: `TBD`
- Interpretation: `TBD`
- Limitation: `TBD`
- Next decision: `TBD`

---

## qi001_chain_cont3 (chain, continuous 3 uniform bins)

- Expected parents of x2: {x1}
- Learned rules:

```text
TBD
```

- Recovered body variables: `TBD`
- Classification: `TBD`
- Interpretation: `TBD`
- Limitation: `TBD`
- Next decision: `TBD`

---

## qi001_fork_cont3 (fork, continuous 3 uniform bins)

- Expected parents of x2: {x0}
- Learned rules:

```text
TBD
```

- Recovered body variables: `TBD`
- Classification: `TBD`
- Interpretation: `TBD`
- Limitation: `TBD`
- Next decision: `TBD`

---

## qi001_collider_cont3 (collider, continuous 3 uniform bins)

- Expected parents of x2: {x0, x1}
- Learned rules:

```text
TBD
```

- Recovered body variables: `TBD`
- Classification: `TBD`
- Interpretation: `TBD`
- Limitation: `TBD`
- Next decision: `TBD`

---

## Cross-cell summary (fill after all cells)

- Recovery by data mode (binary / categorical / continuous): `TBD`
- Recovery by motif (chain / fork / collider): `TBD`
- Overall limitation note: `TBD`
- Next decision for the project: `TBD`

## Findings that motivate follow-up runs (QI-002, QI-003)

Two limitations of the QI-001 design (independent of how the per-cell
interpretation comes out) motivate the follow-up experiments. These are design
observations, not results claims.

1. **x0 / first-column confound (unbroken in QI-001).** In QI-001 the true
   parent of `x2` coincided with the first column (`x0`) for the fork and
   opposed it for the chain. So "the learner found the cause" and "the learner
   prefers `x0`" make identical predictions in some cells and cannot be told
   apart. QI-001 cannot, on its own, distinguish genuine parent recovery from a
   positional preference for `x0`. This is addressed in
   [QI-003](../QI-003.md) via **parent-position variants**: chain and fork are
   each generated in both orientations (true parent in `x0` for some cells, in
   `x1` for others), so a position-preferring learner fails the `*_x1parent`
   cells.

2. **Tiny, unjustified sample size.** QI-001 used 4-5 row tables whose size was
   not derived from any separability requirement, so even a correct learner had
   little to work with and a perfect causal rule was not guaranteed to be the
   unique solution. This is addressed by two principled follow-ups:
   [QI-002](../QI-002.md) uses *complete truth tables* (8 rows binary, 18 rows
   cat3) so the true parent is the unique zero-error separator (the baseline
   "can it be learned at all?"), and [QI-003](../QI-003.md) scales to `n=100`
   with mild noise (the realistic "does it still pick the cause?").

Related: the QI-001 `chain_cont3` fixture was degenerate (`x0` and `x1`
identical), making parent-vs-ancestor undecidable; QI-003's chain mechanism adds
an intermediate flip so the parent column differs from its ancestor.
