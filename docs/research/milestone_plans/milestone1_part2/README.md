# Milestone 1, Part 2 — Published-configuration comparison (M1.2)

**Primary path:** [`../milestone1_high_level_path.md`](../milestone1_high_level_path.md)

**Status:** pilot analysed (Stages 0–3); **expanded design lock in progress**

| Phase | Status | Notes |
|-------|--------|-------|
| Pilot (5 minimal fixtures × ECAI/AAMAS) | Analysed | Historical artefacts below; to be redesigned under the Approach |
| Expanded design | Approach locked; graph/mechanism cards next | See Approach doc |
| Expanded implementation / runs | Not started | After every selected cell is specified |

**Expanded M1.2 Approach (use this while selecting graphs and mechanisms):**  
[`milestone1_part2_expanded_approach.md`](milestone1_part2_expanded_approach.md)

**Pilot artefacts** (provenance only until redesign)

- Fixtures: `causal/experiments/handcrafted_m12.py`
- Checks: `causal/tests/test_m12_fixtures.py`
- Config YAMLs: `causal/configs/experiments/M12_{ecai2024,aamas2025}.yaml`
- Summary: `causal/outputs/aba_learning/grid/M12_summary.md`
- Record: `docs/experiments/qualitative/M1.2-config-comparison.md`
- Cell inspection: `docs/experiments/qualitative/M1.2-config-comparison-cell-inspection.md`

**Locked expansion choices (summary)** — full detail in the Approach:

- Deterministic DGP: copy / min / max; full source factorial; \(k=3\); nonzero-positive labels.
- BK: `val` + definitional `nz` (not assumptions).
- Configs: ECAI and AAMAS only.
- Cells: (fixture, non-source target, config); descendants never predictors.
- Inspection-first acceptance; compact `nz` reference hypotheses preferred.

| Document | Purpose |
|----------|---------|
| [milestone1_part2_expanded_approach.md](milestone1_part2_expanded_approach.md) | **Locked Approach** for expanded M1.2 |
| [milestone1_part2_config_comparison.md](milestone1_part2_config_comparison.md) | Pilot detail plan (historical; update as expansion proceeds) |
| [../milestone1_high_level_path.md](../milestone1_high_level_path.md) | High-level path for finishing M1.2 then M1.3 |

**Parent index:** [milestone1-plan.md](../milestone1-plan.md)

**Next:** select graphs one at a time; write full mechanism cards against the Approach.
