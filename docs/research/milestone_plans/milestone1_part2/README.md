# Milestone 1, Part 2 — Published-configuration comparison (M1.2)

**Primary path:** [`../milestone1_high_level_path.md`](../milestone1_high_level_path.md)

**Status:** pilot analysed (Stages 0–3); **expanded grid constructed** (ready to run)

| Phase | Status | Notes |
|-------|--------|-------|
| Pilot (5 minimal fixtures × ECAI/AAMAS) | Analysed | Historical artefacts below (unchanged) |
| Expanded design | Approach + unit set + cards locked | Approach + unit set + [`mechanism_cards/`](mechanism_cards/) |
| Expanded implementation | **Constructed** | Fixtures `handcrafted_m12x.py`; YAMLs `M12x_{ecai2024,aamas2025}`; dry-run 11+11 cells |
| Expanded learning runs | Not started | Next: `run_grid` both arms |

**Expanded M1.2 Approach:**  
[`milestone1_part2_expanded_approach.md`](milestone1_part2_expanded_approach.md)  

**Accepted unit set (U1–U7):**  
[`milestone1_part2_expanded_unit_set.md`](milestone1_part2_expanded_unit_set.md)  

**Mechanism cards (U1–U7):**  
[`mechanism_cards/`](mechanism_cards/)

**Expanded grid artefacts (M12x)**

- Fixtures: `causal/experiments/handcrafted_m12x.py`
- Configs: `causal/configs/experiments/M12x_{ecai2024,aamas2025}.yaml` (no `grid.seed`; slug `{dgp}__target-{t}`)
- Checks: `causal/tests/test_m12x_fixtures.py`, `test_m12x_configs.py`
- Record: `docs/experiments/qualitative/M1.2-expanded.md`
- Output (after run): `causal/outputs/aba_learning/grid/M12x_{ecai2024,aamas2025}/`

**Pilot artefacts** (historical; unchanged)

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
- Cells: (fixture, non-source target, config); BK = all non-targets (descendants included as distractors; citing them in a learned rule is a failure mode).
- Inspection-first acceptance; compact `nz` reference hypotheses preferred.

| Document | Purpose |
|----------|---------|
| [milestone1_part2_expanded_approach.md](milestone1_part2_expanded_approach.md) | **Locked Approach** for expanded M1.2 |
| [milestone1_part2_expanded_unit_set.md](milestone1_part2_expanded_unit_set.md) | **Accepted units U1–U7** (22 cells) |
| [mechanism_cards/](mechanism_cards/) | **Mechanism cards U1–U7** (tables, BK, \(\mathcal{H}^\star\)) |
| [milestone1_part2_config_comparison.md](milestone1_part2_config_comparison.md) | Pilot detail plan (historical; update as expansion proceeds) |
| [../milestone1_high_level_path.md](../milestone1_high_level_path.md) | High-level path for finishing M1.2 then M1.3 |

**Parent index:** [milestone1-plan.md](../milestone1-plan.md)

**Next:** run both M12x arms → inspect against mechanism-card \(\mathcal{H}^\star\).
