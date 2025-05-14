"""
PyEGRO.SApce: Polynomial Chaos Expansion for Sensitivity Analysis
================================================================

A sensitivity analysis module that uses Polynomial Chaos Expansion (PCE) for
efficient global sensitivity analysis of computational models.

This module implements a framework for analyzing how different input variables affect the 
output of a model or function. It leverages PCE to construct a surrogate model that
enables efficient computation of sensitivity indices with fewer function evaluations
compared to sampling-based methods.

Key capabilities:
1. Supports both direct function evaluation and surrogate models
2. Handles both design variables and environmental/noise variables
3. Calculates first-order and total-order Sobol indices using PCE
4. Provides automatic visualization of sensitivity indices
5. Requires fewer function evaluations than traditional Monte Carlo methods

Main components:
- PCESensitivityAnalysis: Main class for sensitivity analysis with PCE
- SensitivityVisualization: Class for generating visualizations of results
- run_sensitivity_analysis: Convenience function for running analysis
"""

from PyEGRO.sensitivity.SApce.sapce import (
    PCESensitivityAnalysis,
    SensitivityVisualization,
    run_sensitivity_analysis
)

__all__ = [
    'PCESensitivityAnalysis',
    'SensitivityVisualization',
    'run_sensitivity_analysis'
]