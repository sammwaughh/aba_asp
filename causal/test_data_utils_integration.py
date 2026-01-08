#!/usr/bin/env python3
"""
Comprehensive unit tests for causal data integration with ABA-ASP.

This module tests:
1. Predicate generation from causal data (discrete and continuous)
2. Predicate count validation against expected values
3. Predicate format correctness
4. Variable type inference

Usage:
    pytest test_causal_predicates.py -v
    OR
    python -m pytest test_causal_predicates.py -v
    OR (basic execution)
    python test_causal_predicates.py

Author: Fabrizio Russo
License: Same as ABA-ASP project
"""

import sys
import unittest
import logging
from pathlib import Path
from typing import Tuple, Dict
import tempfile
import re

import numpy as np
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add paths to import from parent directories
ABA_ASP_PATH = Path(__file__).parent.parent
ARGCAUSALDISCO_PATH = ABA_ASP_PATH.parent / 'ArgCausalDisco'
sys.path.insert(0, str(ABA_ASP_PATH.parent))
sys.path.insert(0, str(ARGCAUSALDISCO_PATH.parent))

try:
    from aba_asp.utils.data_utils import (
        dataframe_to_predicates,
        infer_variable_types,
        predict_predicate_count,
        save_predicates_to_file,
    )
except ImportError as e:
    logger.error(f"Failed to import aba_asp utils: {e}")
    sys.exit(1)

try:
    from ArgCausalDisco.utils.data_utils import (
        simulate_discrete_data,
        simulate_linear_continuous_data,
    )
except ImportError as e:
    logger.error(f"Failed to import ArgCausalDisco utils: {e}")
    sys.exit(1)


class TestBinaryVariableEncoding(unittest.TestCase):
    """Test binary (0/1) variable encoding in ABA-ASP background knowledge generation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.output_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
    
    def test_binary_encoding_only_positive_cases(self):
        """Test that binary 0/1 variables only generate predicates for true cases.
        
        This is a critical optimization: for binary variables, we should only encode
        x0(A) :- A=1, A=2 (for true cases), NOT x0_val_0(A) :- A=3, A=4.
        
        This produces simpler learned rules like x2(A) :- x0(A) instead of
        more complex rules that would distinguish between x0_val_0 and x0_val_1.
        """
        logger.info("\n" + "="*70)
        logger.info("TEST: Binary Variable Encoding")
        logger.info("="*70)
        
        try:
            from argcausaldisco_integration import generate_aba_background_knowledge
        except ImportError as e:
            self.skipTest(f"Could not import generate_aba_background_knowledge: {e}")
        
        # Create test data with known binary values
        df = pd.DataFrame({
            'x0': [1, 1, 0, 0],
            'x1': [1, 0, 1, 0],
            'x2': [1, 1, 0, 0],
        })
        var_types = {c: "categorical" for c in df.columns}
        
        # Generate BK
        bk_path = generate_aba_background_knowledge(
            df, var_types, "test_binary", self.output_dir
        )
        
        # Read and parse the generated BK
        content = bk_path.read_text()
        logger.info(f"Generated BK file ({len(content)} chars):")
        logger.info(content)
        
        # Verify x0: should only have predicates for samples 1,2 (where x0=1)
        lines_x0 = [l for l in content.split('\n') if l.startswith('x0(A)')]
        logger.info(f"\nExtracted x0 rules: {lines_x0}")
        self.assertEqual(len(lines_x0), 2,
                        f"Binary x0 should generate 2 predicates (for value=1), got {len(lines_x0)}")
        self.assertTrue(all('A=1' in l or 'A=2' in l for l in lines_x0),
                       "x0 predicates should only be for samples 1,2 (where x0=1)")
        
        # Verify x1: should have predicates for samples 1,3 (where x1=1)
        lines_x1 = [l for l in content.split('\n') if l.startswith('x1(A)')]
        logger.info(f"Extracted x1 rules: {lines_x1}")
        self.assertEqual(len(lines_x1), 2,
                        f"Binary x1 should generate 2 predicates (for value=1), got {len(lines_x1)}")
        self.assertTrue(all('A=1' in l or 'A=3' in l for l in lines_x1),
                       "x1 predicates should only be for samples 1,3 (where x1=1)")
        
        # Verify x2: should have predicates for samples 1,2 (where x2=1)
        lines_x2 = [l for l in content.split('\n') if l.startswith('x2(A)')]
        logger.info(f"Extracted x2 rules: {lines_x2}")
        self.assertEqual(len(lines_x2), 2,
                        f"Binary x2 should generate 2 predicates (for value=1), got {len(lines_x2)}")
        self.assertTrue(all('A=1' in l or 'A=2' in l for l in lines_x2),
                       "x2 predicates should only be for samples 1,2 (where x2=1)")
        
        # Verify NO *_val_0 predicates are generated (the old inefficient encoding)
        has_val_0 = any('_val_0' in l for l in content.split('\n'))
        self.assertFalse(has_val_0,
                        "Binary variables should NOT generate _val_0 predicates (only positive cases)")
        
        logger.info("✓ Binary encoding test PASSED: only positive cases encoded\n")
    
    def test_binary_vs_nonbinary_discrete(self):
        """Test that binary and non-binary discrete variables are encoded differently."""
        logger.info("\n" + "="*70)
        logger.info("TEST: Binary vs Non-Binary Discrete Encoding")
        logger.info("="*70)
        
        try:
            from argcausaldisco_integration import generate_aba_background_knowledge
        except ImportError as e:
            self.skipTest(f"Could not import generate_aba_background_knowledge: {e}")
        
        # Create mixed data: binary (0/1) and non-binary (0,1,2) variables
        df = pd.DataFrame({
            'binary_x0': [1, 1, 0, 0],     # binary: only 0,1
            'nonbinary_x1': [0, 1, 2, 0], # non-binary: has 0,1,2
        })
        var_types = {c: "categorical" for c in df.columns}
        
        # Generate BK
        bk_path = generate_aba_background_knowledge(
            df, var_types, "test_mixed", self.output_dir
        )
        
        content = bk_path.read_text()
        logger.info(f"Generated BK:\n{content}")
        
        # Binary variable: should have NO _val_ suffixes
        binary_lines = [l for l in content.split('\n') if l.startswith('binary_x0(')]
        logger.info(f"Binary variable predicates: {binary_lines}")
        self.assertTrue(all('_val' not in l for l in binary_lines),
                       "Binary variable should not use _val suffix")
        self.assertEqual(len(binary_lines), 2,
                        "Binary variable should generate 2 predicates (for value=1 cases)")
        
        # Non-binary variable: SHOULD have _val_ suffixes
        nonbinary_lines = [l for l in content.split('\n') if l.startswith('nonbinary_x1_val_')]
        logger.info(f"Non-binary variable predicates: {nonbinary_lines}")
        self.assertGreater(len(nonbinary_lines), 0,
                          "Non-binary variable should use _val suffix")
        self.assertTrue(any('_val_0' in l for l in nonbinary_lines),
                       "Non-binary should include _val_0 predicates")
        self.assertTrue(any('_val_1' in l for l in nonbinary_lines),
                       "Non-binary should include _val_1 predicates")
        self.assertTrue(any('_val_2' in l for l in nonbinary_lines),
                       "Non-binary should include _val_2 predicates")
        
        logger.info("✓ Binary vs non-binary encoding test PASSED\n")

class TestDiscretePredicateGeneration(unittest.TestCase):
    """Test predicate generation from discrete causal data."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.output_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
    
    def test_discrete_causal_data_shape(self):
        """Test that discrete causal data has correct shape."""
        n_samples = 12
        n_nodes = 3
        
        data = simulate_discrete_data(
            num_of_nodes=n_nodes,
            sample_size=n_samples,
            truth_DAG_directed_edges={(0, 1), (1, 2)},
            random_seed=42
        )
        
        self.assertEqual(data.shape[0], n_samples, 
                        f"Expected {n_samples} samples, got {data.shape[0]}")
        self.assertEqual(data.shape[1], n_nodes,
                        f"Expected {n_nodes} variables, got {data.shape[1]}")
    
    def test_discrete_predicate_generation(self):
        """Test predicate generation from discrete data."""
        n_samples = 12
        n_nodes = 3
        
        data_array = simulate_discrete_data(
            num_of_nodes=n_nodes,
            sample_size=n_samples,
            truth_DAG_directed_edges={(0, 1), (1, 2)},
            random_seed=42
        )
        
        df = pd.DataFrame(data_array, columns=['x0', 'x1', 'x2'])
        var_types = {col: 'categorical' for col in df.columns}
        
        predicates = dataframe_to_predicates(
            df,
            var_types=var_types,
            separate_samples=True,
            sample_separator='%'
        )
        
        # Verify predicates are non-empty
        self.assertTrue(len(predicates) > 0,
                       "Predicates string should not be empty")
        
        # Verify separators are present
        separator_count = predicates.count('%')
        expected_separators = n_samples - 1  # separators between samples
        self.assertGreater(separator_count, 0,
                          "Should have sample separators")
        
        self.assertEqual(separator_count, expected_separators,
                        f"Expected {expected_separators} separators, got {separator_count}")
        
        logger.info(f"Generated {separator_count} sample separators for {n_samples} samples")
    
    def test_discrete_predicate_count(self):
        """Test that predicate count matches expected value."""
        n_samples = 12
        n_nodes = 3
        
        data_array = simulate_discrete_data(
            num_of_nodes=n_nodes,
            sample_size=n_samples,
            truth_DAG_directed_edges={(0, 1), (1, 2)},
            random_seed=42
        )
        
        df = pd.DataFrame(data_array, columns=['x0', 'x1', 'x2'])
        var_types = {col: 'categorical' for col in df.columns}
        
        predicates = dataframe_to_predicates(
            df,
            var_types=var_types,
            separate_samples=True,
            sample_separator='%'
        )
        
        # Count non-separator lines
        predicate_lines = [line.strip() for line in predicates.split('\n')
                          if line.strip() and line.strip() != '%']
        
        # Expected: n_samples * n_nodes (one categorical predicate per variable per sample)
        expected_count = n_samples * n_nodes
        
        self.assertEqual(len(predicate_lines), expected_count,
                        f"Expected {expected_count} predicates, got {len(predicate_lines)}")
        
        logger.info(f"✓ Discrete: {len(predicate_lines)} predicates for {n_samples} samples × {n_nodes} variables")
    
    def test_discrete_predicate_format(self):
        """Test that predicates follow correct format."""
        data_array = simulate_discrete_data(
            num_of_nodes=3,
            sample_size=5,
            truth_DAG_directed_edges={(0, 1), (1, 2)},
            random_seed=42
        )
        
        df = pd.DataFrame(data_array, columns=['x0', 'x1', 'x2'])
        var_types = {col: 'categorical' for col in df.columns}
        
        predicates = dataframe_to_predicates(
            df,
            var_types=var_types,
            separate_samples=False
        )
        
        predicate_lines = [line.strip() for line in predicates.split('\n')
                          if line.strip() and line.strip() != '%']
        
        # Check format: var_value(sample_id).
        # Pattern: lowercase_alphanumeric_underscore(digits).
        pattern = r'^[a-z0-9_]+\(\d+\)\.$'
        
        for pred in predicate_lines[:10]:  # Check first 10
            self.assertIsNotNone(re.match(pattern, pred),
                                f"Predicate '{pred}' doesn't match expected format")
        
        logger.info(f"✓ Discrete predicates follow correct format: {predicate_lines[0]}")


class TestContinuousPredicateGeneration(unittest.TestCase):
    """Test predicate generation from continuous causal data."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.output_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
    
    def test_continuous_causal_data_shape(self):
        """Test that continuous causal data has correct shape."""
        n_samples = 16
        n_nodes = 3
        
        data = simulate_linear_continuous_data(
            num_of_nodes=n_nodes,
            sample_size=n_samples,
            truth_DAG_directed_edges={(0, 1), (1, 2)},
            random_seed=123
        )
        
        self.assertEqual(data.shape[0], n_samples,
                        f"Expected {n_samples} samples, got {data.shape[0]}")
        self.assertEqual(data.shape[1], n_nodes,
                        f"Expected {n_nodes} variables, got {data.shape[1]}")
    
    def test_continuous_predicate_generation(self):
        """Test predicate generation from continuous data."""
        n_samples = 16
        n_nodes = 3
        n_bins = 4
        
        data_array = simulate_linear_continuous_data(
            num_of_nodes=n_nodes,
            sample_size=n_samples,
            truth_DAG_directed_edges={(0, 1), (1, 2)},
            random_seed=123,
            noise_type='gaussian'
        )
        
        df = pd.DataFrame(data_array, columns=['x0', 'x1', 'x2'])
        var_types = {col: 'continuous' for col in df.columns}
        
        predicates = dataframe_to_predicates(
            df,
            var_types=var_types,
            continuous_bins=n_bins,
            separate_samples=True,
            sample_separator='%'
        )
        
        # Verify predicates are non-empty
        self.assertTrue(len(predicates) > 0,
                       "Predicates string should not be empty")
        
        # Verify format uses bin notation (e.g., x0_bin0)
        self.assertIn('bin', predicates,
                     "Continuous predicates should contain 'bin' notation")
        
        logger.info(f"Generated continuous predicates with bin notation")
    
    def test_continuous_predicate_count(self):
        """Test that continuous predicate count matches expected value."""
        n_samples = 16
        n_nodes = 3
        n_bins = 4
        
        data_array = simulate_linear_continuous_data(
            num_of_nodes=n_nodes,
            sample_size=n_samples,
            truth_DAG_directed_edges={(0, 1), (1, 2)},
            random_seed=123,
            noise_type='gaussian'
        )
        
        df = pd.DataFrame(data_array, columns=['x0', 'x1', 'x2'])
        var_types = {col: 'continuous' for col in df.columns}
        
        predicates = dataframe_to_predicates(
            df,
            var_types=var_types,
            continuous_bins=n_bins,
            separate_samples=True,
            sample_separator='%'
        )
        
        # Count non-separator lines
        predicate_lines = [line.strip() for line in predicates.split('\n')
                          if line.strip() and line.strip() != '%']
        
        # Expected: n_samples * n_nodes (one binned predicate per variable per sample)
        expected_count = n_samples * n_nodes
        
        self.assertEqual(len(predicate_lines), expected_count,
                        f"Expected {expected_count} predicates, got {len(predicate_lines)}")
        
        logger.info(f"✓ Continuous: {len(predicate_lines)} predicates for {n_samples} samples × {n_nodes} variables")
    
    def test_continuous_predicate_format(self):
        """Test that continuous predicates have correct bin format."""
        data_array = simulate_linear_continuous_data(
            num_of_nodes=3,
            sample_size=8,
            truth_DAG_directed_edges={(0, 1), (1, 2)},
            random_seed=123,
            noise_type='gaussian'
        )
        
        df = pd.DataFrame(data_array, columns=['x0', 'x1', 'x2'])
        var_types = {col: 'continuous' for col in df.columns}
        
        predicates = dataframe_to_predicates(
            df,
            var_types=var_types,
            continuous_bins=4,
            separate_samples=False
        )
        
        predicate_lines = [line.strip() for line in predicates.split('\n')
                          if line.strip() and line.strip() != '%']
        
        # Check format: var_binX(sample_id).
        # Pattern: x#_bin#(digits).
        pattern = r'^x\d+_bin\d+\(\d+\)\.$'
        
        for pred in predicate_lines:
            self.assertIsNotNone(re.match(pattern, pred),
                                f"Continuous predicate '{pred}' doesn't match format x#_bin#(id).")
        
        logger.info(f"✓ Continuous predicates follow correct format: {predicate_lines[0]}")


class TestPredicateCountPrediction(unittest.TestCase):
    """Test predicate count prediction function."""
    
    def test_predict_count_discrete(self):
        """Test predicate count prediction for discrete data."""
        n_samples = 12
        n_nodes = 3
        
        var_types = {f'x{i}': 'categorical' for i in range(n_nodes)}
        data = pd.DataFrame({
            'x0': np.arange(n_samples),
            'x1': np.arange(n_samples) + 1,
            'x2': np.arange(n_samples) + 2,
        })

        predicted_count = predict_predicate_count(
            n_samples=n_samples,
            n_variables=n_nodes,
            var_types=var_types,
            data=data,
        )
        
        expected_count = n_samples * n_nodes
        
        self.assertEqual(predicted_count, expected_count,
                        f"Predicted {predicted_count}, expected {expected_count}")
        
        logger.info(f"✓ Prediction matches: {predicted_count} == {expected_count}")
    
    def test_predict_count_continuous(self):
        """Test predicate count prediction for continuous data."""
        n_samples = 16
        n_nodes = 3
        
        var_types = {f'x{i}': 'continuous' for i in range(n_nodes)}
        data = pd.DataFrame({
            'x0': np.random.randn(n_samples),
            'x1': np.random.randn(n_samples),
            'x2': np.random.randn(n_samples),
        })

        predicted_count = predict_predicate_count(
            n_samples=n_samples,
            n_variables=n_nodes,
            var_types=var_types,
            continuous_bins=5,
            data=data,
        )
        
        # For continuous: n_samples * n_nodes (one bin per variable per sample)
        expected_count = n_samples * n_nodes
        
        self.assertEqual(predicted_count, expected_count,
                        f"Predicted {predicted_count}, expected {expected_count}")
        
        logger.info(f"✓ Continuous prediction matches: {predicted_count} == {expected_count}")
    
    def test_predict_count_mixed(self):
        """Test predicate count prediction for mixed variable types."""
        n_samples = 10
        
        var_types = {
            'x0': 'binary',      # 1 predicate per sample
            'x1': 'categorical', # 1 predicate per sample
            'x2': 'continuous'   # 1 predicate per sample
        }

        data = pd.DataFrame({
            'x0': [1, 0, 1, 1, 0, 0, 1, 1, 0, 1],  # truthy count = 6
            'x1': [f'c{i%2}' for i in range(n_samples)],
            'x2': np.linspace(0, 1, n_samples),
        })

        predicted_count = predict_predicate_count(
            n_samples=n_samples,
            n_variables=3,
            var_types=var_types,
            continuous_bins=5,
            data=data,
        )

        expected_count = 6 + n_samples * 2  # binary truths + cat + continuous
        
        self.assertEqual(predicted_count, expected_count,
                        f"Predicted {predicted_count}, expected {expected_count}")
        
        logger.info(f"✓ Mixed prediction matches: {predicted_count} == {expected_count}")


class TestIntegrationDiscreteExample(unittest.TestCase):
    """Integration test with actual discrete causal data."""
    
    def test_full_discrete_pipeline(self):
        """Test complete pipeline: data generation → predicates → validation."""
        logger.info("\n" + "="*70)
        logger.info("INTEGRATION TEST: Discrete Causal Data Pipeline")
        logger.info("="*70)
        
        # Parameters matching test_causal_integration.py
        n_samples = 12
        n_nodes = 3
        edges = {(0, 1), (1, 2)}
        seed = 42
        
        # Generate causal data
        logger.info(f"Generating discrete data: {n_samples} samples, {n_nodes} nodes, edges={edges}")
        data_array = simulate_discrete_data(
            num_of_nodes=n_nodes,
            sample_size=n_samples,
            truth_DAG_directed_edges=edges,
            random_seed=seed
        )
        
        df = pd.DataFrame(data_array, columns=['x0', 'x1', 'x2'])
        
        # Infer and verify types
        var_types = {col: 'categorical' for col in df.columns}
        logger.info(f"Variable types: {var_types}")
        
        # Generate predicates
        predicates = dataframe_to_predicates(
            df,
            var_types=var_types,
            continuous_bins=3,
            separate_samples=True,
            sample_separator='%'
        )
        
        # Count predicates
        predicate_lines = [line.strip() for line in predicates.split('\n')
                          if line.strip() and line.strip() != '%']
        
        # Predict expected count
        predicted_count = predict_predicate_count(
            n_samples=n_samples,
            n_variables=n_nodes,
            var_types=var_types
        )
        
        logger.info(f"Generated predicates: {len(predicate_lines)}")
        logger.info(f"Predicted predicates: {predicted_count}")
        logger.info(f"Sample predicates (first 5): {predicate_lines[:5]}")
        
        # Assertions
        self.assertEqual(len(predicate_lines), predicted_count,
                        f"Generated {len(predicate_lines)} predicates, predicted {predicted_count}")
        
        self.assertEqual(len(predicate_lines), n_samples * n_nodes,
                        f"Expected {n_samples * n_nodes} predicates")
        
        logger.info("✓ Integration test PASSED for discrete data\n")


class TestIntegrationContinuousExample(unittest.TestCase):
    """Integration test with actual continuous causal data."""
    
    def test_full_continuous_pipeline(self):
        """Test complete pipeline: data generation → predicates → validation."""
        logger.info("\n" + "="*70)
        logger.info("INTEGRATION TEST: Continuous Causal Data Pipeline")
        logger.info("="*70)
        
        # Parameters matching test_causal_integration.py
        n_samples = 16
        n_nodes = 3
        edges = {(0, 1), (1, 2)}
        n_bins = 4
        seed = 123
        
        # Generate causal data
        logger.info(f"Generating continuous data: {n_samples} samples, {n_nodes} nodes, edges={edges}")
        data_array = simulate_linear_continuous_data(
            num_of_nodes=n_nodes,
            sample_size=n_samples,
            truth_DAG_directed_edges=edges,
            random_seed=seed,
            noise_type='gaussian'
        )
        
        df = pd.DataFrame(data_array, columns=['x0', 'x1', 'x2'])
        
        # Set explicit types
        var_types = {col: 'continuous' for col in df.columns}
        logger.info(f"Variable types: {var_types}")
        
        # Generate predicates
        predicates = dataframe_to_predicates(
            df,
            var_types=var_types,
            continuous_bins=n_bins,
            separate_samples=True,
            sample_separator='%'
        )
        
        # Count predicates
        predicate_lines = [line.strip() for line in predicates.split('\n')
                          if line.strip() and line.strip() != '%']
        
        # Predict expected count
        predicted_count = predict_predicate_count(
            n_samples=n_samples,
            n_variables=n_nodes,
            var_types=var_types,
            continuous_bins=n_bins
        )
        
        logger.info(f"Generated predicates: {len(predicate_lines)}")
        logger.info(f"Predicted predicates: {predicted_count}")
        logger.info(f"Sample predicates (first 5): {predicate_lines[:5]}")
        
        # Assertions
        self.assertEqual(len(predicate_lines), predicted_count,
                        f"Generated {len(predicate_lines)} predicates, predicted {predicted_count}")
        
        self.assertEqual(len(predicate_lines), n_samples * n_nodes,
                        f"Expected {n_samples * n_nodes} predicates")
        
        # Verify bin notation
        has_bin_notation = any('bin' in p for p in predicate_lines)
        self.assertTrue(has_bin_notation,
                       "Continuous predicates should use bin notation")
        
        logger.info("✓ Integration test PASSED for continuous data\n")


def run_tests():
    """Run all tests with detailed output."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestBinaryVariableEncoding))
    suite.addTests(loader.loadTestsFromTestCase(TestDiscretePredicateGeneration))
    suite.addTests(loader.loadTestsFromTestCase(TestContinuousPredicateGeneration))
    suite.addTests(loader.loadTestsFromTestCase(TestPredicateCountPrediction))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationDiscreteExample))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationContinuousExample))
    
    # Run with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    logger.info("\n" + "="*70)
    logger.info("TEST SUMMARY")
    logger.info("="*70)
    logger.info(f"Tests run: {result.testsRun}")
    logger.info(f"Failures: {len(result.failures)}")
    logger.info(f"Errors: {len(result.errors)}")
    logger.info(f"Success: {result.wasSuccessful()}")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
