# Milestone 1, Part 2 — Published-configuration comparison (M1.2)

**Primary path:** [`../milestone1_high_level_path.md`](../milestone1_high_level_path.md)

**Status:** pilot analysed (Stages 0–3); **expansion next**

| Phase | Status | Notes |
|-------|--------|-------|
| Pilot (5 minimal fixtures × ECAI/AAMAS) | Analysed | Records and artefacts below |
| Expanded (Fabrizio small DAGs × chosen DGP(s)) | Not started | Lock design before runs; see high-level path §1–2 |

**Pilot artefacts**

- Fixtures: `causal/experiments/handcrafted_m12.py`
- Checks: `causal/tests/test_m12_fixtures.py`
- Arm YAMLs: `causal/configs/experiments/M12_{ecai2024,aamas2025}.yaml`
- Summary: `causal/outputs/aba_learning/grid/M12_summary.md`
- Record: `docs/experiments/qualitative/M1.2-config-comparison.md`
- Cell inspection: `docs/experiments/qualitative/M1.2-config-comparison-cell-inspection.md`

**Scope for the expansion**

- Graphs: Fabrizio’s usable small DAGs; exclude random graphs, bnlearn, cycles.
- DGPs: decide which and how many before implementing.
- Intended learned rules: locked per cell before any run.
- Arms: ECAI and AAMAS only (no RuleML).
- Criteria: intended-rule match and ASP coverage kept separate; primary instrument is qualitative trace inspection.

| Document | Purpose |
|----------|---------|
| [milestone1_part2_config_comparison.md](milestone1_part2_config_comparison.md) | Detail plan for the pilot and (to be updated) expansion |
| [../milestone1_high_level_path.md](../milestone1_high_level_path.md) | High-level path for finishing M1.2 then M1.3 |

**Parent index:** [milestone1-plan.md](../milestone1-plan.md)
