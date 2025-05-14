"""
PyEGRO Meta Package

This package provides surrogate modeling capabilities for the PyEGRO package,
including Gaussian Process Regression (GPR), Co-Kriging, using EGO technique for metamodel improvement
and model testing functionality.
"""

# Import submodules
from . import gpr
from . import cokriging
from . import egogpr
from . import egocokriging
from .evaluation import modeltesting

__all__ = [
    # Submodules
    'gpr',
    'cokriging',
    'modeltesting',
    'egogpr',
    'egocokriging',
    'modeltesting'
]