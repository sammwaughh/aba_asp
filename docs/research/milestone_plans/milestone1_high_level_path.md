# Milestone 1 — High-level path to completion

**Role:** primary working reference for finishing Milestone 1.  
**Parent index:** [`milestone1-plan.md`](milestone1-plan.md)  
**Status:** active (2026-08-03) — **M12x closed**; M1.3 Buckets 1–2 **locked**;
Bucket 3 H0–H4 complete / analysed; H5 cautious Greedy deferred; H6/H7
signposted; **no Bucket 3 claim**

Organising question for all of Milestone 1:

> Across controlled targets, data-availability conditions, graph/mechanism structures,
> and learning strategies, what causal structure can unguided ABA Learning recover,
> what does it recover instead, and which limits are informational rather than
> strategic?

No Causal ABA integration in this milestone. M1.3 may add larger **controlled** fixtures
under Bucket 3; large-scale / bnlearn evaluation remains reserved for a later phase
against any Causal-ABA-informed solution.

---

## Where we are

| Part | Status | What exists |
|------|--------|-------------|
| **M1.1** | Closed | Parent-position / representation-order control; ordering mechanism established |
| **M1.2 pilot** | Analysed (historical) | 10-cell pilot; superseded as primary evidence by M12x |
| **M1.2 expanded (M12x)** | **Closed / analysed** | Fresh 18-cell run + Stage-3 inspection **18/18** (2026-07-20); evidence package locked for M1.3 |
| **M1.3** | **In progress** | Buckets 1–2 locked; Bucket 3 H0–H4 complete / analysed; H5 deferred; H6/H7 signposted; no Bucket 3 claim |
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

## Path (M1.3 now)

### 1–2. Expanded M1.2 — **closed**

Design (U1–U7, val-only BK, 18 cells) locked; both arms run (`--no-resume`);
`m12x_summary` regenerated; Stage-3 inspection written (**18/18**).  
Working catalogue: [`milestone1_part2/m12x_units_reference.tex`](milestone1_part2/m12x_units_reference.tex).  
Prior wiped M12x outputs remain void.

### 3. Do M1.3 (claims + probes) — **in progress**

Method: [`milestone1_part3/milestone1_part3_approach.md`](milestone1_part3/milestone1_part3_approach.md).  
Bucket 1 (**locked**): `docs/experiments/qualitative/M1.3-bucket1-claims.md`
(TeX: `docs/report/findings/milestone1_part3_bucket1_claims.tex`).  
Bucket 2 (**locked / closed; two claims**): `docs/experiments/qualitative/M1.3-bucket2-claims.md`
(TeX: `docs/report/findings/milestone1_part3_bucket2_claims.tex`).  
Probe records: `M13-C1-causal-role-underdetermination/experiment.md`;
`M13-C2-bk-feature-order/experiment.md`.  
Bucket 3 (**H0–H4 complete / analysed; no claim**):
`docs/experiments/qualitative/M1.3-bucket3-claims.md`.

**Immediate next step:** Orchestrator / Samuel decide among deferred H5 and
signposted H6/H7. H4 is run / analysed; its repository-baseline cautious arm
blocks the brave root residual-assumption gadget while control `c` retains the
same delta as locked ECAI. The remaining 22 July dimensions are retained but
deferred.
No Bucket 3 claim, fixture portfolio, or run matrix is approved.

### 4. Close Milestone 1

Consolidate findings into a Milestone 1 write-up answering the organising question, and list which limits (if any) motivate Causal ABA guidance in Milestone 2.

---

## One-line discipline

**M12x + Buckets 1–2 locked** → **one certified deterministic Bucket 3 case at a
time** → Milestone 1 synthesis → Milestone 2 guidance design → later large-scale
evaluation.
