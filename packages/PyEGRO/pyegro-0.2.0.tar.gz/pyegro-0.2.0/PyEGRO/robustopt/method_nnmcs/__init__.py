"""
PyEGRO.robustopt.method_nnmcs - Two-Stage Approach using Neural Networks and MCS

This module provides a two-stage approach for robust optimization in PyEGRO:
1. Train neural networks to approximate the mean and standard deviation
2. Use neural networks in optimization loop for fast evaluations
3. Verify final solutions with high-fidelity MCS
"""

from .nnmcs import (
    RobustOptimization,
    ANNConfig,
    SamplingConfig,
    OptimizationConfig,
    PathConfig
)

__all__ = [
    'RobustOptimization',
    'ANNConfig',
    'SamplingConfig',
    'OptimizationConfig',
    'PathConfig'
]