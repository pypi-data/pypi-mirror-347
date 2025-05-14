"""
PyEGRO Surrogate Modeling Package

This package provides  Co-Kriging functionality for the PyEGRO package.
It offers tools for training, testing, and visualizing surrogate models with different data sources.
"""

# Co-Kriging Module imports
from .cokriging import MetaTrainingCoKriging
from .cokriging_utils import CoKrigingModel, CoKrigingKernel, DeviceAgnosticCoKriging
from .visualization import visualize_cokriging

__all__ = [
    # Co-Kriging classes and functions
    'MetaTrainingCoKriging',
    'CoKrigingModel',
    'CoKrigingKernel',
    'DeviceAgnosticCoKriging',
    'visualize_cokriging'
]