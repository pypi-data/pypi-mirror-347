"""
PyEGRO.meta.egogpr: Efficient Global Optimization with Gaussian Process Regression
=================================================================================

A Python library for building accurate surrogate models through efficient adaptive sampling.

Efficient Global Optimization (EGO) is specifically designed for scenarios where:
1. Function evaluations are expensive or time-consuming (e.g., simulations, physical experiments)
2. The accuracy of the surrogate model is critically important
3. Resources for sampling are limited and must be used optimally

This package provides a comprehensive implementation of EGO algorithms with various
acquisition functions that intelligently select new sampling points to maximize
the improvement of metamodel accuracy with minimal evaluations.

Main components:
- EfficientGlobalOptimization: Main adaptive sampling framework
- AcquisitionFunction: Various sampling strategies (EI, LCB, PI, E³I, etc.)
- GPRegressionModel: Gaussian Process Regression metamodel
- Visualization: Tools for analyzing metamodel accuracy and sampling decisions

Example:
    >>> from PyEGRO.meta.egogpr import EfficientGlobalOptimization
    >>> import numpy as np
    >>> 
    >>> # Define objective function
    >>> def objective(x):
    ...     return np.sin(x) + np.sin(10*x/3)
    >>> 
    >>> # Define bounds and variable names
    >>> bounds = np.array([[0, 10]])
    >>> var_names = ['x']
    >>> 
    >>> # Initialize optimizer
    >>> ego = EfficientGlobalOptimization(objective, bounds, var_names)
    >>> 
    >>> # Run optimization
    >>> history = ego.run()
"""

# Import main classes for easy access
from .training import EfficientGlobalOptimization
from .model import GPRegressionModel
from .config import TrainingConfig
from .acquisition import (
    ExpectedImprovement,
    LowerConfidenceBound,
    PredictiveVariance,
    ProbabilityImprovement,
    ExpectedImprovementGlobalFit,
    Criterion3,
    ExplorationEnhancedEI,
    create_acquisition_function,
    propose_location
)
from .utils import (
    setup_directories,
    evaluate_model_performance,
    save_model_data,
    load_model_data
)
from .visualization import (
    EGOAnimator,
    ModelVisualizer
)

# Define package version
__version__ = '0.1.0'