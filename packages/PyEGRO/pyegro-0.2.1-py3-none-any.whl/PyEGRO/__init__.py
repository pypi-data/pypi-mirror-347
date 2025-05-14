"""
PyEGRO: Python Efficient Global Robust Optimization
------------------------------------------------
A comprehensive Python library for efficient global robust optimization,
featuring initial design sampling, surrogate modeling, and sensitivity analysis.

Available Modules:
----------------
1. Initial Design (doe):
   - Latin Hypercube, Sobol, Halton sampling methods
   - Support for design and environmental variables
   - Adaptive distribution sampling

2. Efficient Global Optimization (ego):
   - Multiple acquisition functions (EI, PI, LCB, E3I, EIGF, CRI3)
   - Comprehensive training configuration
   - Built-in visualization tools

3. MetaTraining (meta):
   - Gaussian Process Regression training
   - Co-Kriging model (Multi-Fidelity modeling)
   - Hardware optimization (CPU/GPU)
   - Progress tracking and visualization

4. Robust Optimization (robustopt):
   - Monte Carlo Simulation (MCS)
   - Polynomial Chaos Expansion (PCE)
   - Two-Stage Using Neural Network (NN)
   - Support for both direct on function and surrogate evaluation

5. Sensitivity Analysis (sensitivity):
   - Sobol indices calculation  (Monte Carlo Simulaiton, Polynomial Chaos Expansion)
   - Support for true functions and surrogates
   - Convergence analysis and visualization

6. Uncertainty Quantification (uq):
   - Uncertainty Propagation
   - Distribution Analysis
"""

from . import doe
from . import meta
from . import robustopt
from . import sensitivity
from . import uncertainty

__version__ = "1.0.0"
__author__ = "Thanasak Wanglomklang"
__email__ = "thanasak.wang@gmail.com"

# Rest of the code remains the same...

# Update __all__
__all__ = [
    # Main modules
    'doe',
    'meta',
    'robustopt',
    'sensitivity',
    'uncertainty',
    
    # Utility functions
    'get_version',
    'get_citation',
    'print_usage'
]