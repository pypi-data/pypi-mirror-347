"""
PyEGRO Uncertainty Quantification Module
--------------------------------------
This module provides tools for uncertainty quantification and propagation using
Monte Carlo Simulation with support for both direct evaluation and surrogate models.
"""

from .UQmcs import UncertaintyPropagation, run_uncertainty_analysis

"""
This module provides comprehensive tools for uncertainty quantification and propagation 
using Monte Carlo Simulation, supporting both direct function evaluation and surrogate models.
"""


# Module level documentation
__all__ = [
    'UncertaintyPropagation',
    'run_uncertainty_analysis'
]

