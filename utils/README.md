# ABA-ASP Data Utils

Utilities for turning tabular data into ABA predicates used by the ABA-ASP solvers.

## Quick Reference
- **Binary (0/1)**: `var(id)` for value==1 only.
- **Categorical/Discrete**: `var_val(id)` (e.g., `diagnosis_flu(3).`).
- **Continuous**: binned to `var_binK(id)` (quantile or uniform strategy).
- Samples can be separated with `%` markers for readability.

## Core API
- `dataframe_to_predicates(df, var_types, continuous_bins=5, bin_strategy='quantile', start_sample_id=1, separate_samples=True, sample_separator='%')`
  - Detect types (or pass `var_types`), bin continuous, and emit predicates as a string.
- `infer_variable_types(df)`: quick type inference (binary/categorical/continuous).
- `save_predicates_to_file(predicates, path)`: write out `.aba` files.
- Helpers: `array_to_predicates`, `csv_to_predicates`, `convert_csv_to_predicates_file`, `bin_continuous_variable`, `sanitize_predicate_name`.

## Minimal Examples
```python
import pandas as pd
from aba_asp.utils import dataframe_to_predicates, save_predicates_to_file

df = pd.DataFrame({
    'symptom': [1, 0, 1],          # binary → symptom(1), symptom(3)
    'diagnosis': ['flu', 'cold', 'flu'],  # categorical → diagnosis_flu(1)
    'temperature': [38.5, 36.2, 39.1],    # continuous → temperature_binK(n)
})

var_types = {
    'symptom': 'binary',
    'diagnosis': 'categorical',
    'temperature': 'continuous',
}

preds = dataframe_to_predicates(df, var_types=var_types, continuous_bins=3)
save_predicates_to_file(preds, 'output.aba')
```

One-liner CSV conversion:
```python
from aba_asp.utils import convert_csv_to_predicates_file

convert_csv_to_predicates_file(
    'input.csv', 'output.aba',
    var_types={'age': 'continuous', 'dx': 'categorical', 'employed': 'binary'},
    continuous_bins=5,
)
```

## Notes
- Missing/NaN values are skipped for that variable/sample.
- Predicate names are sanitized to lowercase with underscores; leading digits get prefixed.
- Works directly with ArgCausalDisco generators (`simulate_discrete_data`, `simulate_linear_continuous_data`).
- Docs in this README cover the former QUICK_REFERENCE; no separate document needed.

