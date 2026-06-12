# greedy-rerun-bundle

Handoff bundle for the greedy-folding reruns of QL1/QL2/QL4 (QI-001, QI-002, QI-004). Compares non-deterministic (nd) vs **greedy** folding for target-wise parent-set recovery under the current `aba_asp/causal` implementation.

**Caution.** This compares two ABA Learning folding settings for parent-set recovery. It does **not** establish causal discovery by either setting (no graph recovery, d-separation, arr/noe/indep, or stable-extension-as-DAG).

Single conceptual change per pair: `defaults.folding_mode: nd -> greedy`. QL3 excluded (superseded by QI-004).

## Start here

- `greedy_vs_nd_qualitative_handoff.md` — the synthesis (run-level, recovery, and claim tables; headline verdict).

## File -> source map

| Bundle file | Source path |
|---|---|
| `greedy_vs_nd_qualitative_handoff.md` | `docs/experiments/qualitative/greedy_vs_nd_qualitative_handoff.md` |
| `configs/QI001_motifs_modes_greedy.yaml` | `causal/configs/experiments/QI001_motifs_modes_greedy.yaml` |
| `configs/QI002_minimal_motifs_greedy.yaml` | `causal/configs/experiments/QI002_minimal_motifs_greedy.yaml` |
| `configs/QI004_scaled_motifs_n20_greedy.yaml` | `causal/configs/experiments/QI004_scaled_motifs_n20_greedy.yaml` |
| `summaries/QI001_motifs_modes_greedy_summary.md` | `docs/experiments/qualitative/QI001_motifs_modes_greedy_summary.md` |
| `summaries/QI002_minimal_motifs_greedy_summary.md` | `docs/experiments/qualitative/QI002_minimal_motifs_greedy_summary.md` |
| `summaries/QI004_scaled_motifs_n20_greedy_summary.md` | `docs/experiments/qualitative/QI004_scaled_motifs_n20_greedy_summary.md` |
| `summaries_nd/QI002_minimal_motifs_summary.md` | `docs/experiments/qualitative/QI002_minimal_motifs_summary.md` (nd baseline) |
| `summaries_nd/QI004_scaled_motifs_n20_summary.md` | `docs/experiments/qualitative/QI004_scaled_motifs_n20_summary.md` (nd baseline) |
| `dossiers/QI001_motifs_modes_greedy/*` | `docs/experiments/qualitative/QI001_motifs_modes_greedy/*` |
| `dossiers/QI002_minimal_motifs_greedy/*` | `docs/experiments/qualitative/QI002_minimal_motifs_greedy/*` |
| `dossiers/QI004_scaled_motifs_n20_greedy/*` | `docs/experiments/qualitative/QI004_scaled_motifs_n20_greedy/*` |
| `METRICS.md` | `causal/aa-plans/METRICS.md` |

Note: QL1 nd has no generated summary on disk (its `metrics.json` predates the `clean_recovery` field); its nd baseline is described qualitatively in `QL_interim_handoff.md` and inside the handoff document.

## Headline

Greedy vs nd is **mixed-leaning-better**: strictly faster everywhere (QL4 ~120x: 1233 s -> 10 s), higher solve rate (QI-002 collider_binary: no-solution -> solved), net higher clean recovery (QI-002 3/6 -> 4/6; QI-001 colliders clean in all modes), one cell regression (QI-002 fork_cat3), and no recovery change at the noisy n=20 scale (QL4 0/15 both). No further rerun needed.
