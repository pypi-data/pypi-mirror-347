"""
PyEGRO.uncertainty.UQmcs - Uncertainty Quantification with Monte Carlo Simulation.

This module provides tools to perform uncertainty propagation analysis using
Monte Carlo Simulation methods. It allows users to evaluate the impact of input
uncertainties on the response of engineering models.

Classes:
--------
UncertaintyPropagation : Main class for setting up and running uncertainty propagation analysis
DistributionGenerator : Utility class for generating samples from various probability distributions

Functions:
----------
run_uncertainty_analysis : Convenience function for running a complete uncertainty analysis

Example:
--------
import numpy as np
from PyEGRO.uncertainty.UQmcs import run_uncertainty_analysis

# Define a test function
def my_function(X):
    return X[:, 0]**2 + 2*X[:, 1]

# Run analysis with provided data_info
results = run_uncertainty_analysis(
    data_info_path="path/to/data_info.json",
    true_func=my_function,
    num_design_samples=500,
    num_mcs_samples=10000,
    output_dir="RESULT_UQ"
)
"""

from .uqmcs import UncertaintyPropagation, run_uncertainty_analysis

__all__ = [
    'UncertaintyPropagation',
    'DistributionGenerator',
    'run_uncertainty_analysis',
]