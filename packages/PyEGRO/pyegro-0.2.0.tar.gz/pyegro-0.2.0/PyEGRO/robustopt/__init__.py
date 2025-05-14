"""
PyEGRO Robust Optimization Module
--------------------------------
This module provides tools for robust optimization using various uncertainty 
quantification approaches including Monte Carlo Simulation (MCS), 
Polynomial Chaos Expansion (PCE), and Neural Network-accelerated Monte Carlo 
Simulation (NNMCS).

Available Methods:
----------------
1. Monte Carlo Simulation (MCS):
   - Direct sampling approach
   - Accurate but computationally intensive
   - Suitable for complex uncertainty distributions

2. Polynomial Chaos Expansion (PCE):
   - Efficient spectral method
   - Faster convergence for smooth responses
   - Better for low-dimensional problems

3. Neural Network-accelerated MCS (NNMCS):
   - Two-stage approach combining neural networks with MCS
   - Balances computational efficiency and accuracy
   - Uses neural networks as fast in robust design loop
"""

# Import MCS module components
from .method_mcs.mcs import (
    RobustOptimizationProblemMCS,
    setup_algorithm,
    run_robust_optimization as run_mcs_optimization,
    save_optimization_results as save_mcs_results
)

# Import PCE module components
from .method_pce.pce import (
    RobustOptimizationProblemPCE,
    PCESampler,
    run_robust_optimization as run_pce_optimization,
    save_optimization_results as save_pce_results
)

# Import NNMCS module components
from .method_nnmcs import (
    RobustOptimization as NNMCS_Optimization,
    ANNConfig,
    SamplingConfig,
    OptimizationConfig,
    PathConfig
)

__all__ = [
    # MCS optimization
    'RobustOptimizationProblemMCS',
    'setup_algorithm',
    'run_mcs_optimization',
    'save_mcs_results',
    
    # PCE optimization
    'RobustOptimizationProblemPCE',
    'PCESampler',
    'run_pce_optimization',
    'save_pce_results',
    
    # NNMCS optimization
    'NNMCS_Optimization',
    'ANNConfig',
    'SamplingConfig',
    'OptimizationConfig',
    'PathConfig'
]