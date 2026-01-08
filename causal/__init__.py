"""
ABA-ASP Causal Integration Package

This package provides utilities for integrating causal discovery with ABA-ASP learning.

Modules:
    test_causal_integration: End-to-end integration test suite
"""

__version__ = '0.1.0'
__author__ = 'ABA-ASP Team'
__license__ = 'Same as ABA-ASP'

# Import main functions for convenience
try:
    from .test_causal_integration import (
        create_discrete_causal_example,
        create_continuous_causal_example,
        convert_to_aba_predicates,
        apply_pc_algorithm,
        run_integration_tests,
    )
    __all__ = [
        'create_discrete_causal_example',
        'create_continuous_causal_example',
        'convert_to_aba_predicates',
        'apply_pc_algorithm',
        'run_integration_tests',
    ]
except ImportError:
    # If running as standalone module
    pass
