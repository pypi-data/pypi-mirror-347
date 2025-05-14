"""
PyEGRO.SAmcs: Monte Carlo Simulation for Sensitivity Analysis
=============================================================

A sensitivity analysis module that uses Monte Carlo Simulation (MCS) with the Sobol method 
based on Saltelli's sampling approach for global sensitivity analysis.

This module implements a framework for analyzing how different input variables affect the 
output of a model or function. It focuses on calculating first-order and total-order 
sensitivity indices, which provide insights into both direct effects and interactions
among variables.

Key capabilities:
1. Supports both direct function evaluation and surrogate models
2. Handles both design variables and environmental/noise variables
3. Calculates first-order and total-order Sobol indices
4. Provides automatic visualization of sensitivity indices
5. Supports various distribution types for input variables

Main components:
- MCSSensitivityAnalysis: Main class for sensitivity analysis with MCS
- SensitivityVisualization: Class for generating visualizations of results
- run_sensitivity_analysis: Convenience function for running analysis
"""

from PyEGRO.sensitivity.SAmcs.samcs import (
    MCSSensitivityAnalysis,
    SensitivityVisualization,
    run_sensitivity_analysis
)

__all__ = [
    'MCSSensitivityAnalysis',
    'SensitivityVisualization',
    'run_sensitivity_analysis'
]