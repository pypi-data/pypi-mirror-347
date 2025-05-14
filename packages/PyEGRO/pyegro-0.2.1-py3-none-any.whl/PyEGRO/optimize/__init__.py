"""
PyEGRO Optimization Module - Genetic Algorithm (GA)
--------------------------------------------------
Deterministic optimization using Genetic Algorithm

This module provides deterministic optimization functionality using
Genetic Algorithm for single-objective optimization problems.
"""

from .GA import (
    DeterministicOptimizationProblemGA,
    setup_algorithm,
    run_deterministic_optimization,
    save_optimization_results,
    print_variable_information
)

__all__ = [
    'DeterministicOptimizationProblemGA',
    'setup_algorithm',
    'run_deterministic_optimization',
    'save_optimization_results',
    'print_variable_information'
]