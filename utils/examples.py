#!/usr/bin/env python
"""
Example: Converting simulated causal data to ABA predicate format.

This script demonstrates how to use the data_utils module to convert
data from ArgCausalDisco into ABA format for argumentation mining.
"""

import sys
from pathlib import Path

# Add paths if needed
# sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pandas as pd
import numpy as np
from data_utils import (
    dataframe_to_predicates,
    array_to_predicates,
    save_predicates_to_file,
    convert_csv_to_predicates_file,
)


def example_1_basic_dataframe():
    """Example 1: Convert a simple DataFrame to predicates."""
    print("=" * 70)
    print("Example 1: Basic DataFrame Conversion")
    print("=" * 70)
    
    # Create sample data
    data = pd.DataFrame({
        'symptom1': [1, 0, 1, 1, 0],  # binary
        'symptom2': [1, 1, 0, 1, 1],  # binary
        'severity': ['mild', 'severe', 'moderate', 'severe', 'mild'],  # categorical
        'temperature': [36.5, 39.2, 37.8, 40.1, 36.9],  # continuous
    })
    
    print("\nInput data:")
    print(data)
    
    var_types = {
        'symptom1': 'binary',
        'symptom2': 'binary',
        'severity': 'categorical',
        'temperature': 'continuous',
    }
    
    predicates = dataframe_to_predicates(data, var_types=var_types, continuous_bins=3)
    
    print("\nGenerated ABA predicates:")
    print(predicates)
    
    return predicates


def example_2_auto_detection():
    """Example 2: Automatic variable type detection."""
    print("\n" + "=" * 70)
    print("Example 2: Automatic Variable Type Detection")
    print("=" * 70)
    
    # Create sample data with mixed types
    data = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'approved': [True, False, True, True, False],  # binary
        'department': ['HR', 'IT', 'HR', 'Finance', 'IT'],  # categorical
        'salary': [45000, 75000, 50000, 65000, 80000],  # continuous
    })
    
    print("\nInput data:")
    print(data)
    print(f"\nData types:\n{data.dtypes}")
    
    # Auto-detect types (no var_types specified)
    predicates = dataframe_to_predicates(data, continuous_bins=4)
    
    print("\nGenerated ABA predicates:")
    print(predicates)
    
    return predicates


def example_3_numpy_array():
    """Example 3: Convert numpy array to predicates."""
    print("\n" + "=" * 70)
    print("Example 3: Numpy Array Conversion")
    print("=" * 70)
    
    # Create synthetic causal data (simulating output from ArgCausalDisco)
    np.random.seed(42)
    n_samples = 5
    
    # Simulate a causal structure: X0 -> X1 -> X2
    X0 = np.random.normal(0, 1, n_samples)
    X1 = 2 * X0 + np.random.normal(0, 0.5, n_samples)
    X2 = -1.5 * X1 + np.random.normal(0, 0.5, n_samples)
    
    data = np.column_stack([X0, X1, X2])
    
    print(f"\nSynthetic causal data (shape: {data.shape}):")
    print(pd.DataFrame(data, columns=['X0', 'X1', 'X2']))
    
    var_types = {f'X{i}': 'continuous' for i in range(3)}
    
    predicates = array_to_predicates(
        data,
        column_names=['X0', 'X1', 'X2'],
        var_types=var_types,
        continuous_bins=3
    )
    
    print("\nGenerated ABA predicates:")
    print(predicates)
    
    return predicates


def example_4_mixed_binning():
    """Example 4: Different binning strategies."""
    print("\n" + "=" * 70)
    print("Example 4: Binning Strategies Comparison")
    print("=" * 70)
    
    data = pd.DataFrame({
        'value': [1.0, 2.0, 3.0, 4.0, 100.0],  # Note the outlier
    })
    
    print("\nInput data:")
    print(data)
    
    var_types = {'value': 'continuous'}
    
    print("\n--- Quantile binning (equal-frequency) ---")
    predicates_quantile = dataframe_to_predicates(
        data,
        var_types=var_types,
        continuous_bins=3,
        bin_strategy='quantile',
        separate_samples=False
    )
    print(predicates_quantile)
    
    print("\n--- Uniform binning (equal-width) ---")
    predicates_uniform = dataframe_to_predicates(
        data,
        var_types=var_types,
        continuous_bins=3,
        bin_strategy='uniform',
        separate_samples=False
    )
    print(predicates_uniform)


def example_5_save_to_file():
    """Example 5: Save predicates to file."""
    print("\n" + "=" * 70)
    print("Example 5: Saving to File")
    print("=" * 70)
    
    data = pd.DataFrame({
        'a1': [1, 1, 1],
        'a2': [1, 0, 1],
        'diagnosis': ['autism', 'normal', 'autism'],
    })
    
    var_types = {
        'a1': 'binary',
        'a2': 'binary',
        'diagnosis': 'categorical',
    }
    
    predicates = dataframe_to_predicates(data, var_types=var_types)
    
    output_file = Path(__file__).parent / 'example_output.aba'
    save_predicates_to_file(predicates, output_file)
    
    print(f"\nSaved predicates to: {output_file}")
    print(f"File contents:")
    print(output_file.read_text())
    
    # Clean up
    output_file.unlink()
    print("(File cleaned up for this example)")


def example_6_custom_start_id():
    """Example 6: Custom sample IDs and separators."""
    print("\n" + "=" * 70)
    print("Example 6: Custom Sample IDs and Separators")
    print("=" * 70)
    
    data = pd.DataFrame({
        'feature1': [1, 0, 1],
        'feature2': ['A', 'B', 'A'],
    })
    
    var_types = {
        'feature1': 'binary',
        'feature2': 'categorical',
    }
    
    print("\nWith start_sample_id=100 and no separators:")
    predicates = dataframe_to_predicates(
        data,
        var_types=var_types,
        start_sample_id=100,
        separate_samples=False
    )
    print(predicates)
    
    print("\nWith start_sample_id=1000 and custom separator '---':")
    predicates = dataframe_to_predicates(
        data,
        var_types=var_types,
        start_sample_id=1000,
        separate_samples=True,
        sample_separator='---'
    )
    print(predicates)


if __name__ == '__main__':
    # Run all examples
    example_1_basic_dataframe()
    example_2_auto_detection()
    example_3_numpy_array()
    example_4_mixed_binning()
    example_5_save_to_file()
    example_6_custom_start_id()
    
    print("\n" + "=" * 70)
    print("All examples completed!")
    print("=" * 70)
