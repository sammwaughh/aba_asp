"""
Utilities for converting tabular data to ABA predicate files.

This module provides functions to translate tabular data (e.g., from pandas DataFrames,
numpy arrays, or CSV files) into ABA predicate file format suitable for use with
ABA-ASP solvers.

Format:
    - Binary variables: var(n) where var is the variable name and n is the sample id
    - Categorical variables: var_x(n) where var is the variable name, x is the categorical
      value, and n is the sample id
    - Continuous variables: binned into d categories using the categorical strategy above

Author: Fabrizio Russo
License: Same as ABA-ASP project
"""

import numpy as np
import pandas as pd
import logging
from typing import Union, List, Tuple, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


def infer_variable_types(data: pd.DataFrame) -> dict:
    """
    Infer variable types from a pandas DataFrame.
    
    Args:
        data (pd.DataFrame): Input data
        
    Returns:
        dict: Dictionary mapping column names to variable types:
            - 'binary': for binary variables (0/1, True/False)
            - 'categorical': for categorical/nominal variables
            - 'continuous': for numerical variables
    """
    var_types = {}
    
    for col in data.columns:
        dtype = data[col].dtype
        
        # Check if binary
        unique_values = data[col].dropna().unique()
        if len(unique_values) <= 2:
            var_types[col] = 'binary'
        # Check if categorical (object dtype or integer with few unique values)
        elif dtype == 'object' or (dtype in ['int32', 'int64'] and len(unique_values) < 20):
            var_types[col] = 'categorical'
        # Default to continuous
        else:
            var_types[col] = 'continuous'
    
    return var_types


def bin_continuous_variable(
    values: np.ndarray,
    n_bins: int = 5,
    strategy: str = 'quantile'
) -> Tuple[np.ndarray, List[Tuple[float, float]]]:
    """
    Bin a continuous variable into categorical bins.
    
    Args:
        values (np.ndarray): Continuous values to bin
        n_bins (int): Number of bins. Defaults to 5.
        strategy (str): Binning strategy:
            - 'quantile': equal-frequency binning (recommended)
            - 'uniform': equal-width binning
            
    Returns:
        Tuple[np.ndarray, List[Tuple[float, float]]]: 
            - Binned values (integers from 0 to n_bins-1)
            - List of bin edges as (lower, upper) tuples
    """
    # Handle NaN values
    mask = ~np.isnan(values)
    
    if strategy == 'quantile':
        # Equal-frequency binning
        bins = pd.qcut(values[mask], q=n_bins, duplicates='drop', retbins=True)[1]
    elif strategy == 'uniform':
        # Equal-width binning
        bins = np.linspace(values[mask].min(), values[mask].max(), n_bins + 1)
    else:
        raise ValueError(f"Unknown binning strategy: {strategy}")
    
    # Digitize returns bin indices (1-indexed), we use 0-indexed
    binned = np.digitize(values, bins) - 1
    
    # Ensure out-of-bounds values are clipped
    binned = np.clip(binned, 0, len(bins) - 2)
    
    # Create list of bin edges
    bin_ranges = [(bins[i], bins[i + 1]) for i in range(len(bins) - 1)]
    
    return binned, bin_ranges


def sanitize_predicate_name(name: str) -> str:
    """
    Sanitize a string to be a valid predicate name in ABA/ASP.
    
    Rules:
        - Replace spaces and special characters with underscores
        - Keep only alphanumeric characters and underscores
        - Ensure it starts with a lowercase letter
        
    Args:
        name (str): Original name
        
    Returns:
        str: Sanitized predicate name
    """
    # Convert to lowercase
    name = str(name).lower()
    
    # Replace spaces and special characters with underscores
    name = ''.join(c if c.isalnum() or c == '_' else '_' for c in name)
    
    # Remove leading numbers or underscores, add prefix if needed
    if name[0].isdigit() or name[0] == '_':
        name = f'v_{name}'
    
    # Remove consecutive underscores
    while '__' in name:
        name = name.replace('__', '_')
    
    return name


def dataframe_to_predicates(
    data: pd.DataFrame,
    var_types: Optional[dict] = None,
    continuous_bins: int = 5,
    bin_strategy: str = 'quantile',
    start_sample_id: int = 1,
    separate_samples: bool = True,
    sample_separator: str = '%'
) -> str:
    """Convert a pandas DataFrame to ABA predicate format.

    Args:
        data (pd.DataFrame): Input tabular data
        var_types (dict, optional): Dictionary mapping column names to types
            ('binary', 'categorical', 'continuous'). If None, will infer automatically.
        continuous_bins (int): Number of bins for continuous variables. Defaults to 5.
        bin_strategy (str): Strategy for binning continuous variables.
            Defaults to 'quantile'.
        start_sample_id (int): Starting sample ID (1-indexed). Defaults to 1.
        separate_samples (bool): Whether to add '%' separator between samples.
            Defaults to True.
        sample_separator (str): String to use as sample separator. Defaults to '%'.
        
    Returns:
        str: ABA predicate format string

    Example:
        >>> import pandas as pd
        >>> from aba_asp.utils.data_utils import dataframe_to_predicates
        >>> df = pd.DataFrame({
        ...     'symptom': [1, 0, 1],           # binary → symptom(1), symptom(3)
        ...     'diagnosis': ['flu','cold','flu'],  # categorical → diagnosis_flu(1)
        ...     'temperature': [38.5, 36.2, 39.1],  # continuous → temperature_binK(n)
        ... })
        >>> preds = dataframe_to_predicates(
        ...     df,
        ...     var_types={'symptom':'binary','diagnosis':'categorical','temperature':'continuous'},
        ...     continuous_bins=3,
        ... )
        >>> print(preds.splitlines()[0])
        symptom(1).
    """
    if var_types is None:
        var_types = infer_variable_types(data)
        logger.info(f"Inferred variable types: {var_types}")
    
    # Process continuous variables
    processed_data = data.copy()
    bin_ranges_dict = {}
    
    for col, var_type in var_types.items():
        if var_type == 'continuous':
            binned, bin_ranges = bin_continuous_variable(
                data[col].values,
                n_bins=continuous_bins,
                strategy=bin_strategy
            )
            processed_data[col] = binned
            bin_ranges_dict[col] = bin_ranges
            logger.info(f"Binned variable '{col}' into {continuous_bins} bins")
    
    # Generate predicates
    predicates = []
    
    for sample_idx, row in processed_data.iterrows():
        sample_id = start_sample_id + sample_idx
        
        for col, var_type in var_types.items():
            col_clean = sanitize_predicate_name(col)
            value = row[col]
            
            # Skip NaN values
            if pd.isna(value):
                continue
            
            if var_type == 'binary':
                # Binary: var(n) if true
                # Only add predicate if value is truthy (1, True, etc.)
                if value or (isinstance(value, (int, float)) and value != 0):
                    predicates.append(f"{col_clean}({sample_id}).")
            
            elif var_type == 'categorical':
                # Categorical: var_x(n)
                value_clean = sanitize_predicate_name(str(value))
                predicates.append(f"{col_clean}_{value_clean}({sample_id}).")
            
            elif var_type == 'continuous':
                # Continuous (binned): var_binX(n)
                bin_idx = int(value)
                predicates.append(f"{col_clean}_bin{bin_idx}({sample_id}).")
        
        # Add sample separator if requested
        if separate_samples:
            predicates.append(sample_separator)
    
    # Remove trailing separator if present
    if predicates and predicates[-1] == sample_separator:
        predicates.pop()
    
    return '\n'.join(predicates) + '\n'


def array_to_predicates(
    data: np.ndarray,
    column_names: Optional[List[str]] = None,
    var_types: Optional[dict] = None,
    continuous_bins: int = 5,
    bin_strategy: str = 'quantile',
    start_sample_id: int = 1,
    separate_samples: bool = True,
    sample_separator: str = '%'
) -> str:
    """Convert a numpy array to ABA predicate format.

    Args:
        data (np.ndarray): Input array of shape (n_samples, n_features)
        column_names (List[str], optional): Names for columns. If None, uses 'X0', 'X1', etc.
        var_types (dict, optional): Dictionary mapping column names to types.
        continuous_bins (int): Number of bins for continuous variables. Defaults to 5.
        bin_strategy (str): Strategy for binning. Defaults to 'quantile'.
        start_sample_id (int): Starting sample ID. Defaults to 1.
        separate_samples (bool): Whether to add '%' separator between samples.
        sample_separator (str): String to use as sample separator.
        
    Returns:
        str: ABA predicate format string

    Example:
        >>> import numpy as np
        >>> from aba_asp.utils.data_utils import array_to_predicates
        >>> data = np.array([[25.5, 1], [35.2, 1], [45.1, 0]])
        >>> preds = array_to_predicates(
        ...     data,
        ...     column_names=['age','employed'],
        ...     var_types={'age':'continuous','employed':'binary'},
        ...     continuous_bins=3,
        ... )
        >>> 'employed(1).' in preds
        True
    """
    if column_names is None:
        column_names = [f'X{i}' for i in range(data.shape[1])]
    
    df = pd.DataFrame(data, columns=column_names)
    return dataframe_to_predicates(
        df,
        var_types=var_types,
        continuous_bins=continuous_bins,
        bin_strategy=bin_strategy,
        start_sample_id=start_sample_id,
        separate_samples=separate_samples,
        sample_separator=sample_separator
    )


def csv_to_predicates(
    filepath: Union[str, Path],
    var_types: Optional[dict] = None,
    continuous_bins: int = 5,
    bin_strategy: str = 'quantile',
    start_sample_id: int = 1,
    separate_samples: bool = True,
    sample_separator: str = '%',
    **csv_kwargs
) -> str:
    """Convert a CSV file to ABA predicate format.

    Args:
        filepath (Union[str, Path]): Path to CSV file
        var_types (dict, optional): Dictionary mapping column names to types.
        continuous_bins (int): Number of bins for continuous variables.
        bin_strategy (str): Strategy for binning.
        start_sample_id (int): Starting sample ID.
        separate_samples (bool): Whether to add '%' separator between samples.
        sample_separator (str): String to use as sample separator.
        **csv_kwargs: Additional arguments to pass to pd.read_csv()
        
    Returns:
        str: ABA predicate format string

    Example:
        >>> from aba_asp.utils.data_utils import csv_to_predicates
        >>> preds = csv_to_predicates('data.csv', var_types={'x':'binary'})  # doctest: +SKIP
        >>> preds.splitlines()[0]  # doctest: +SKIP
        'x(1).'
    """
    df = pd.read_csv(filepath, **csv_kwargs)
    return dataframe_to_predicates(
        df,
        var_types=var_types,
        continuous_bins=continuous_bins,
        bin_strategy=bin_strategy,
        start_sample_id=start_sample_id,
        separate_samples=separate_samples,
        sample_separator=sample_separator
    )


def save_predicates_to_file(
    predicates: str,
    output_path: Union[str, Path]
) -> None:
    """
    Save predicate string to a file.
    
    Args:
        predicates (str): Predicate string to save
        output_path (Union[str, Path]): Path where to save the file
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write(predicates)
    
    logger.info(f"Saved predicates to {output_path}")


def convert_csv_to_predicates_file(
    input_csv: Union[str, Path],
    output_aba: Union[str, Path],
    var_types: Optional[dict] = None,
    continuous_bins: int = 5,
    bin_strategy: str = 'quantile',
    separate_samples: bool = True,
    **kwargs
) -> None:
    """Convenience function to convert a CSV file directly to an ABA predicate file.

    Args:
        input_csv (Union[str, Path]): Path to input CSV file
        output_aba (Union[str, Path]): Path where to save the ABA predicate file
        var_types (dict, optional): Dictionary mapping column names to types.
        continuous_bins (int): Number of bins for continuous variables.
        bin_strategy (str): Strategy for binning.
        separate_samples (bool): Whether to add '%' separator between samples.
        **kwargs: Additional arguments to pass to pd.read_csv()
    Example:
        >>> from aba_asp.utils.data_utils import convert_csv_to_predicates_file
        >>> convert_csv_to_predicates_file('in.csv','out.aba', var_types={'x':'binary'})  # doctest: +SKIP
    """
    logger.info(f"Converting {input_csv} to {output_aba}...")
    
    predicates = csv_to_predicates(
        input_csv,
        var_types=var_types,
        continuous_bins=continuous_bins,
        bin_strategy=bin_strategy,
        separate_samples=separate_samples,
        **kwargs
    )
    
    save_predicates_to_file(predicates, output_aba)
    logger.info(f"Conversion complete!")


def predict_predicate_count(
    n_samples: int,
    n_variables: int,
    var_types: dict,
    continuous_bins: Optional[int] = None,
    data: Optional[pd.DataFrame] = None,
) -> int:
    """
    Predict the number of predicates generated from a dataset.
    
    Binary predicates are emitted only when the value is truthy. If ``data`` is
    provided, the binary predicate count is the sum of truthy values per binary
    column. Without data, the function falls back to assuming a predicate per
    sample for binary variables.
    
    Args:
        n_samples: Number of samples in the dataset
        n_variables: Number of variables in the dataset
        var_types: Dictionary mapping variable names to types ('binary', 'categorical', 'continuous')
        continuous_bins: Unused placeholder (kept for API symmetry)
        data: Optional DataFrame to compute binary truth counts
    
    Returns:
        Expected number of non-separator predicates
    """
    predicate_total = 0

    for var_name, var_type in var_types.items():
        if var_type == 'binary':
            if data is not None and var_name in data.columns:
                # Count truthy values only
                truthy_mask = (data[var_name] != 0) & (~data[var_name].isna())
                predicate_total += int(truthy_mask.sum())
            else:
                predicate_total += n_samples  # pessimistic fallback
        elif var_type in ('categorical', 'continuous'):
            predicate_total += n_samples
        else:
            raise ValueError(f"Unknown variable type for {var_name}: {var_type}")

    return predicate_total


if __name__ == '__main__':
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    # Create sample data
    sample_data = pd.DataFrame({
        'age': [25, 35, 45, 28, 52],  # continuous
        'income': [50000, 75000, 120000, 55000, 95000],  # continuous
        'education': ['HS', 'BS', 'MS', 'HS', 'PhD'],  # categorical
        'employed': [1, 1, 0, 1, 1],  # binary
    })
    
    print("Sample input data:")
    print(sample_data)
    print("\n" + "="*60 + "\n")
    
    # Convert to predicates
    predicates = dataframe_to_predicates(sample_data, continuous_bins=3)
    print("Generated predicates:")
    print(predicates)
