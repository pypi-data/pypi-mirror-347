"""
PyEGRO.sensitivity: Sensitivity Analysis Module
==============================================

This module provides tools for global sensitivity analysis using different approaches
to analyze how input variables affect the output of computational models.

Available Methods:
-----------------
1. Monte Carlo Simulation (SAmcs):
   - Uses Sobol method with Saltelli's sampling approach
   - Direct sampling for model-agnostic analysis
   - Provides first-order and total-order Sobol indices

2. Polynomial Chaos Expansion (SApce):
   - Spectral method for efficient sensitivity analysis
   - Requires fewer function evaluations than sampling methods
   - Particularly effective for smooth response surfaces
"""

# Import from SAmcs submodule
from PyEGRO.sensitivity.SAmcs.samcs import (
    MCSSensitivityAnalysis as MCSAnalysis,
    SensitivityVisualization as MCSVisualization,
    run_sensitivity_analysis as run_mcs_analysis
)

# Import from SApce submodule
from PyEGRO.sensitivity.SApce.sapce import (
    PCESensitivityAnalysis as PCEAnalysis,
    SensitivityVisualization as PCEVisualization,
    run_sensitivity_analysis as run_pce_analysis
)

__all__ = [
    # Monte Carlo Simulation (MCS) components
    'MCSAnalysis',
    'MCSVisualization',
    'run_mcs_analysis',
    
    # Polynomial Chaos Expansion (PCE) components
    'PCEAnalysis',
    'PCEVisualization',
    'run_pce_analysis'
]