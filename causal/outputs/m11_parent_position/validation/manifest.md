# m1.1 fixture validation manifest

- Experiment: `M11_parent_position`
- Generated (UTC): 2026-06-18T22:35:40.137199+00:00
- Scope: Stage-0 fixture validation (pre-learning); parent-set recovery proxy, not Russo-style Causal ABA.
- All cells pass: **True**; all orbit relations pass: **True**

| Encoding | Cell | Parent | Requested order | Table order | BK order | Target excluded | Fixture checks |
|---|---|---|---|---|---|---|---|
| binary | A | `x1` | [x0, x1] | [x0, x1] | [x0, x1] | True | PASS |
| binary | B | `x1` | [x1, x0] | [x1, x0] | [x1, x0] | True | PASS |
| binary | C | `x0` | [x0, x1] | [x0, x1] | [x0, x1] | True | PASS |
| binary | D | `x0` | [x1, x0] | [x1, x0] | [x1, x0] | True | PASS |
| cat3 | A | `x1` | [x0, x1] | [x0, x1] | [x0, x1] | True | PASS |
| cat3 | B | `x1` | [x1, x0] | [x1, x0] | [x1, x0] | True | PASS |
| cat3 | C | `x0` | [x0, x1] | [x0, x1] | [x0, x1] | True | PASS |
| cat3 | D | `x0` | [x1, x0] | [x1, x0] | [x1, x0] | True | PASS |

## Orbit relations

| Relation | Holds |
|---|---|
| `binary:sigma(A->B)` | True |
| `binary:sigma(D->C)` | True |
| `binary:pi(A->D)` | True |
| `binary:pi(B->C)` | True |
| `cat3:sigma(A->B)` | True |
| `cat3:sigma(D->C)` | True |
| `cat3:pi(A->D)` | True |
| `cat3:pi(B->C)` | True |

## Per-cell check detail

### binary cell A

- PASS `row_count`
- PASS `every_assignment_present`
- PASS `x2_equals_parent`
- PASS `requested_equals_table_order`
- PASS `examples_partition_rows`
- PASS `parent_is_zero_error_separator`
- PASS `non_parent_has_no_separator`
- PASS `bk_order_matches_requested`
- PASS `target_excluded_from_bk`

### binary cell B

- PASS `row_count`
- PASS `every_assignment_present`
- PASS `x2_equals_parent`
- PASS `requested_equals_table_order`
- PASS `examples_partition_rows`
- PASS `parent_is_zero_error_separator`
- PASS `non_parent_has_no_separator`
- PASS `bk_order_matches_requested`
- PASS `target_excluded_from_bk`

### binary cell C

- PASS `row_count`
- PASS `every_assignment_present`
- PASS `x2_equals_parent`
- PASS `requested_equals_table_order`
- PASS `examples_partition_rows`
- PASS `parent_is_zero_error_separator`
- PASS `non_parent_has_no_separator`
- PASS `bk_order_matches_requested`
- PASS `target_excluded_from_bk`

### binary cell D

- PASS `row_count`
- PASS `every_assignment_present`
- PASS `x2_equals_parent`
- PASS `requested_equals_table_order`
- PASS `examples_partition_rows`
- PASS `parent_is_zero_error_separator`
- PASS `non_parent_has_no_separator`
- PASS `bk_order_matches_requested`
- PASS `target_excluded_from_bk`

### cat3 cell A

- PASS `row_count`
- PASS `every_assignment_present`
- PASS `x2_equals_parent`
- PASS `requested_equals_table_order`
- PASS `examples_partition_rows`
- PASS `parent_is_zero_error_separator`
- PASS `non_parent_has_no_separator`
- PASS `bk_order_matches_requested`
- PASS `target_excluded_from_bk`

### cat3 cell B

- PASS `row_count`
- PASS `every_assignment_present`
- PASS `x2_equals_parent`
- PASS `requested_equals_table_order`
- PASS `examples_partition_rows`
- PASS `parent_is_zero_error_separator`
- PASS `non_parent_has_no_separator`
- PASS `bk_order_matches_requested`
- PASS `target_excluded_from_bk`

### cat3 cell C

- PASS `row_count`
- PASS `every_assignment_present`
- PASS `x2_equals_parent`
- PASS `requested_equals_table_order`
- PASS `examples_partition_rows`
- PASS `parent_is_zero_error_separator`
- PASS `non_parent_has_no_separator`
- PASS `bk_order_matches_requested`
- PASS `target_excluded_from_bk`

### cat3 cell D

- PASS `row_count`
- PASS `every_assignment_present`
- PASS `x2_equals_parent`
- PASS `requested_equals_table_order`
- PASS `examples_partition_rows`
- PASS `parent_is_zero_error_separator`
- PASS `non_parent_has_no_separator`
- PASS `bk_order_matches_requested`
- PASS `target_excluded_from_bk`
