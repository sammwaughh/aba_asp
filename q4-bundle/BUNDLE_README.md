# q4-bundle — QL4 (QI-004) interim-report handoff

Copies of the QL4 documentation and combined QL1–QL4 handoff, for Samuel/ChatGPT to use when
writing the QL4 interim-report subsection. These are **copies**; the canonical source files
live in the repo at the paths listed below. Do not treat the copies as authoritative if they
diverge from the repo.

Scope reminder: QL4 evaluates **target-wise parent-set recovery** under the current
`aba_asp/causal` implementation (target-wise ABA Learning pipeline). It does NOT evaluate full
Russo-style Causal ABA, graph recovery, d-separation, `arr`/`noe`/`indep`, or
stable-extension-as-DAG.

## Contents → source paths

| Bundle file | Source path |
|---|---|
| `QL_interim_handoff.md` | `docs/experiments/qualitative/QL_interim_handoff.md` |
| `QI004_scaled_motifs_n20_summary.md` | `docs/experiments/qualitative/QI004_scaled_motifs_n20_summary.md` (generated) |
| `QI004_scaled_motifs_n20/README.md` | `docs/experiments/qualitative/QI004_scaled_motifs_n20/README.md` |
| `QI004_scaled_motifs_n20/run_log.md` | `docs/experiments/qualitative/QI004_scaled_motifs_n20/run_log.md` |
| `QI004_scaled_motifs_n20/interpretation.md` | `docs/experiments/qualitative/QI004_scaled_motifs_n20/interpretation.md` |
| `QI004_scaled_motifs_n20/artefacts.md` | `docs/experiments/qualitative/QI004_scaled_motifs_n20/artefacts.md` |
| `QI004_scaled_motifs_n20/metrics.md` | `docs/experiments/qualitative/QI004_scaled_motifs_n20/metrics.md` |
| `QI004_scaled_motifs_n20/decision_record.md` | `docs/experiments/qualitative/QI004_scaled_motifs_n20/decision_record.md` |
| `QI004_scaled_motifs_n20/QI-004_high_level_record.md` | `docs/experiments/qualitative/QI-004.md` |
| `config/QI004_scaled_motifs_n20.yaml` | `causal/configs/experiments/QI004_scaled_motifs_n20.yaml` |
| `metrics_spec/METRICS.md` | `causal/aa-plans/METRICS.md` |

## QL4 one-line status

15/15 cells completed, no timeouts (`n=20`, 300 s). Outcomes: 1 solved, 12
completed_no_solution, 2 binary `unknown constant` errors. `clean_recovery = 0` for all 15
cells. The one solved cell (`qi004_chain_x1parent_binary`) learned an ancestor-contaminated
**superset** {x0, x1} of the true parent {x1}. QL4 is the canonical scaled/noisy run
(supersedes QL3 for feasibility) but its parent-recovery finding is null; canonical recovery
evidence remains QL1 + QL2.

## Not included (to avoid bloat)

QL1–QL3 generated summaries and dossiers are not copied here; `QL_interim_handoff.md`
reproduces their key facts inline. Their repo paths are listed in the handoff (§4, §9).
