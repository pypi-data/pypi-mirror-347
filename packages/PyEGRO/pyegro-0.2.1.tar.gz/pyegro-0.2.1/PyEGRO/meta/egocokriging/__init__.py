"""
PyEGRO.meta.egocokriging: Efficient Global Optimization with Co-Kriging Support
==============================================================================

A Python library for multi-fidelity surrogate modeling using Co-Kriging and efficient adaptive sampling.

This module extends the standard Efficient Global Optimization approach to handle multi-fidelity data,
where simulations or experiments can be run at different levels of accuracy and computational cost.
Co-Kriging models leverage correlations between low-fidelity (cheap) and high-fidelity (expensive)
data to build more accurate surrogate models with fewer high-fidelity evaluations.

Key benefits of multi-fidelity optimization:
1. Leverages cheaper, lower-fidelity evaluations to guide expensive high-fidelity sampling
2. Reduces overall computational cost while maintaining high accuracy
3. Automatically learns correlation between fidelity levels
4. Efficiently balances exploration vs exploitation across fidelity levels

Main components:
- EfficientGlobalOptimization: Multi-fidelity adaptive sampling framework
- CoKrigingModel: Co-Kriging surrogate model for multiple fidelity levels
- AcquisitionFunction: Acquisition strategies with multi-fidelity support
- Visualization: Tools for analyzing multi-fidelity model accuracy

Example:
    >>> from PyEGRO.meta.egocokriging import EfficientGlobalOptimization
    >>> import numpy as np
    >>> 
    >>> # Define high and low fidelity objective functions
    >>> def high_fidelity_func(x):
    ...     return np.sin(8*x) + x
    >>> 
    >>> def low_fidelity_func(x):
    ...     return 0.8*np.sin(8*x) + 1.2*x  # Less accurate but cheaper
    >>> 
    >>> # Define bounds and variable names
    >>> bounds = np.array([[0, 1]])
    >>> var_names = ['x']
    >>> 
    >>> # Initialize optimizer with both functions
    >>> ego = EfficientGlobalOptimization(
    ...     objective_func=high_fidelity_func,
    ...     bounds=bounds,
    ...     variable_names=var_names,
    ...     low_fidelity_func=low_fidelity_func
    ... )
    >>> 
    >>> # Run optimization
    >>> history = ego.run()
"""

# Import main classes for easy access
from .training import EfficientGlobalOptimization
from .model import CoKrigingModel, CoKrigingKernel
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
    load_model_data,
    train_ck_model,
    check_rho_convergence,
    prepare_data_with_fidelity
)
from .visualization import (
    EGOAnimator,
    ModelVisualizer
)

# Define package version
__version__ = '0.1.0'