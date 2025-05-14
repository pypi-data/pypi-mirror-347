"""
PyEGRO Design of Experiments (DOE) Module
----------------------------------------
A Python module for generating initial design samples with support for multiple
sampling methods and both design and environmental variables.

Available Sampling Methods
------------------------
- Latin Hypercube Sampling (LHS): Good space-filling properties
- Sobol Sequence: Low-discrepancy sequence with excellent uniformity
- Halton Sequence: Low-discrepancy sequence with good uniformity
- Random Sampling: Simple uniform random sampling

"""

from .initial_design import InitialDesign
from .sampling import AdaptiveDistributionSampler, Variable

__version__ = "1.0.0"
__author__ = "Thanasak Wanglomklang"
__email__ = "thanasak.wang@gmail.com"

def get_version():
    """Return the current version of the module."""
    return __version__

def get_citation():
    """Return citation information for the module."""
    citation = """
To cite this work, please use:

@software{PyEGRO_initial_design,
    title={PyEGRO: Python Efficient Global Robust Optimization},
    author={Thanasak Wanglomklang},
    year={2024},
    version={""" + __version__ + """},
    url={https://github.com/twanglom/PyEGRO}
}
"""
    return citation

__all__ = [
    'InitialDesign',
    'AdaptiveDistributionSampler',
    'Variable',
    'get_version',
    'get_citation'
]