# M2-S2 — mode-2 hunt: `baseline_cautious` on non-roots only

## Status

**run** (14 August 2026). Non-root outcome grid filled. Deltas and Prolog traces
retained. Not a locked claim. Not a Causal ABA integration result.

## Purpose

Ask whether failure mode 2 occurs: a **non-root** returns
`completed_no_solution` under `baseline_cautious` on exhaustive root-support
tables. Only that outcome would emit an `ext_source` fact for a node that is
not a DAG source.

Roots were not scored. 4-AND, majority-3, and mux were not run.

## Setup

- Learner: `configs/baseline_cautious_config.pl` (cautious nd, `relto`,
  `folding_steps(10)`).
- Encoding: exact-value, binary 1-vs-0.
- Tables: handwritten exhaustive combinations of **root** assignments.
- Non-root targets only.

Wave 0 cells are reused from M2-S1 (already `solved` on every non-root). Wave 1
and the leading-isolated 3-AND ran only target `c`.

## Fixtures

| Fixture id | Mechanism | Non-roots |
|---|---|---|
| `m2_support_and_collider` | \(C := A \land B\) | `c` |
| `m2_support_or_collider` | \(C := A \lor B\) | `c` |
| `m2_support_xor_collider` | \(C := A \oplus B\) | `c` |
| `m2_support_copy` | \(B := A\) | `b` |
| `m2_support_not` | \(B := \lnot A\) | `b` |
| `m2_support_copy_chain` | \(B := A\), \(C := B\) | `b`, `c` |
| `m2_support_fork_copy_not` | \(B := A\), \(C := \lnot A\) | `b`, `c` |
| `m2_support_and3` | \(C := A \land B \land D\) | `c` |
| `m2_support_or3` | \(C := A \lor B \lor D\) | `c` |
| `m2_support_and3_lead_iso` | isolated \(A\); \(C := B \land D \land E\) | `c` |

## Outcome grid

`solved` = a delta was accepted. `no-sol` = `completed_no_solution`.
`timeout` = Prolog wall-clock cap of 300s (not no-sol). `—` = variable absent.
`not run` = target not executed (non-root-only policy, or aborted all-target
run). Non-roots are marked with `*`. Times are `aba_learning_runtime_s`.

Mode 2 would be `no-sol` on a starred cell.

| Fixture | `a` | `b` | `c` | `d` | `e` | Mode 2 |
|---|---|---|---|---|---|---|
| AND collider | no-sol 26.3s | no-sol 26.2s | solved* 0.49s | — | — | no |
| OR collider | no-sol 23.1s | no-sol 22.7s | solved* 0.57s | — | — | no |
| XOR collider | solved 0.72s | solved 0.72s | solved* 0.73s | — | — | no |
| Copy | solved 0.27s | solved* 0.25s | — | — | — | no |
| NOT | solved 0.24s | solved* 0.25s | — | — | — | no |
| Copy chain | solved 0.25s | solved* 0.25s | solved* 0.24s | — | — | no |
| Fork copy+NOT | solved 0.24s | solved* 0.25s | solved* 0.27s | — | — | no |
| 3-AND | timeout 300s | timeout 300s | solved* 0.89s | timeout 300s | — | no |
| 3-OR | timeout 300s | timeout 300s | solved* 0.99s | not run | — | no |
| 3-AND + leading isolated | not run | not run | solved* 2.62s | not run | not run | no |

**Every scored non-root is `solved`.** No starred cell is `no-sol`. Mode 2 did
not occur on these tables.

3-OR `a`/`b` timeouts are leftovers from the aborted all-target run.

## Artefacts

Per-target traces and solutions:

`causal/outputs/aba_learning/targetwise/<fixture>/baseline_cautious/support/cells/target-<var>/output/`

Solved cells keep `prolog.stdout`, `delta.aba`, `bk.sol.aba`, `bk.sol.asp`, and
`bk.sol_chk.asp`.

The 3-OR folder also has leftover root timeouts from an aborted all-target run
(`a`, `b`); those are out of scope for this record. Leading-isolated roots were
not executed.

## Interpretation boundary

This record only answers whether non-roots failed to solve on these support
tables. It does not evaluate Causal ABA, Majority-PC, weighting, or an
`ext_source` pipeline. Deltas were not inspected beyond confirming they exist.
