# Milestone 1 — Closure record

**Role:** final navigation and closure record for Milestone 1.
**Parent index:** [`milestone1-plan.md`](milestone1-plan.md)  
**Status:** **closed** (2026-08-08) — M1.1 closed; M12x closed; M1.3 closed;
no M1.4. Active successor: [`milestone2/README.md`](milestone2/README.md).

Organising question for all of Milestone 1:

> Across controlled targets, data-availability conditions, graph/mechanism structures,
> and learning strategies, what causal structure can unguided ABA Learning recover,
> what does it recover instead, and which limits are informational rather than
> strategic?

No Causal ABA integration was implemented in this milestone. Larger controlled fixtures
and large-scale / bnlearn evaluation were not required for closure.

---

## Where we are

| Part | Status | What exists |
|------|--------|-------------|
| **M1.1** | Closed | Parent-position / representation-order control; ordering mechanism established |
| **M1.2 pilot** | Analysed (historical) | 10-cell pilot; superseded as primary evidence by M12x |
| **M1.2 expanded (M12x)** | **Closed / analysed** | Fresh 18-cell run + Stage-3 inspection **18/18** (2026-07-20); evidence package locked for M1.3 |
| **M1.3** | **Closed** | Buckets 1–2 retain six locked claims; Bucket 3 H0–H7b complete / analysed and consolidated into six cross-cutting findings in `findings_for_fabrizio.tex`; no separate locked Bucket-3 claim list |
| **M1.4** | Does not exist | Expanded controlled investigation remains within M1.3 |

**Expanded M1.2 Approach:**  
[`milestone1_part2/milestone1_part2_expanded_approach.md`](milestone1_part2/milestone1_part2_expanded_approach.md)  

**Accepted unit set (U1–U7):**  
[`milestone1_part2/milestone1_part2_expanded_unit_set.md`](milestone1_part2/milestone1_part2_expanded_unit_set.md)

**M12x Stage-3 inspection (canonical evidence):**  
`docs/experiments/qualitative/M1.2-expanded-cell-inspection.md`  
LaTeX companion: `docs/report/findings/milestone1_part2_m12x_cell_inspection.tex`

Pilot artefacts (keep for provenance; not the expanded design):  
`docs/experiments/qualitative/M1.2-config-comparison.md`,  
`docs/experiments/qualitative/M1.2-config-comparison-cell-inspection.md`,  
`causal/outputs/aba_learning/grid/M12_*`.

---

## Completed path

### 1–2. Expanded M1.2 — **closed**

Design (U1–U7, val-only BK, 18 cells) locked; both arms run (`--no-resume`);
`m12x_summary` regenerated; Stage-3 inspection written (**18/18**).  
Working catalogue: [`milestone1_part2/m12x_units_reference.tex`](milestone1_part2/m12x_units_reference.tex).  
Prior wiped M12x outputs remain void.

### 3. M1.3 (claims + probes) — **closed**

Method: [`milestone1_part3/milestone1_part3_approach.md`](milestone1_part3/milestone1_part3_approach.md).  
Bucket 1 (**locked**): `docs/experiments/qualitative/M1.3-bucket1-claims.md`
(TeX: `docs/report/findings/milestone1_part3_bucket1_claims.tex`).  
Bucket 2 (**locked / closed; two claims**): `docs/experiments/qualitative/M1.3-bucket2-claims.md`
(TeX: `docs/report/findings/milestone1_part3_bucket2_claims.tex`).  
Probe records: `M13-C1-causal-role-underdetermination/experiment.md`;
`M13-C2-bk-feature-order/experiment.md`.  
Bucket 3 (**closed; H0–H7b complete / analysed, including H4b**):
`docs/experiments/qualitative/M1.3-bucket3-claims.md`. Cross-cutting closure
synthesis:
`docs/experiments/qualitative/M13-C3-binary-collider-and/findings_for_fabrizio.tex`.

No separate locked Bucket-3 claim list was created. The completed synthesis records six
bounded findings. Unused 22 July dimensions are deferred beyond M1 rather than remaining
open Bucket-3 work.

### 4. Close Milestone 1 — **done (2026-08-08)**

The Milestone-1 synthesis answers the organising question at the level supported by the
completed evidence and records which learner behaviours may be relevant to investigation
of possible integrations in Milestone 2.

Canonical synthesis:
`docs/experiments/qualitative/M13-C3-binary-collider-and/findings_for_fabrizio.tex`.

## Successor

Milestone 2 is open. Its deliberately agnostic approach begins with intimate study of the
argumentative causal discovery paper and ArgCausalDisco code, after which possible
integrations with ABA Learning will be tried and tested. See
[`milestone2/README.md`](milestone2/README.md).

---

## One-line discipline

**M12x + Buckets 1–2 locked** → **certified deterministic Bucket-3 probes H0–H7b**
→ **six-finding Milestone-1 synthesis** → **M2 paper/ArgCausalDisco understanding**
→ possible integrations tried and tested, with the form left open.
