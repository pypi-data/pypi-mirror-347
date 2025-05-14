"""
PyEGRO.robustopt.method_mcs.mcs: Monte Carlo Simulation for Robust Optimization
==========================================================================

A robust optimization module that uses Monte Carlo Simulation (MCS) for uncertainty 
quantification in multi-objective optimization problems.

This module implements a framework for handling both epistemic uncertainty (model 
uncertainty) and aleatory uncertainty (inherent variability) in optimization problems.
It uses NSGA-II for solving the multi-objective problem of maximizing performance while
minimizing sensitivity to uncertainty.

Key capabilities:
1. Supports both direct function evaluation and surrogate models
2. Handles both design variables and environmental/noise variables
3. Implements effective Monte Carlo sampling for uncertainty quantification
4. Provides robust optimization metrics and visualizations
5. Uses adaptive sampling strategies for efficient uncertainty propagation

Main components:
- RobustOptimizationProblemMCS: Problem formulation for robust optimization
- run_robust_optimization: Main optimization function with MCS
- save_optimization_results: Saving and visualizing optimization results
"""

from PyEGRO.robustopt.method_mcs.mcs import (
    RobustOptimizationProblemMCS,
    setup_algorithm,
    run_robust_optimization,
    save_optimization_results
)

__all__ = [
    'RobustOptimizationProblemMCS',
    'setup_algorithm',
    'run_robust_optimization',
    'save_optimization_results'
]