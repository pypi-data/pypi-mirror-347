"""
Examples for using the PyEGRO GPR Module.

This file contains example functions demonstrating how to use the
Gaussian Process Regression module with different data sources.
"""

# ===================================================
# GPR --> synthetic data  
# ===================================================

import numpy as np
import matplotlib.pyplot as plt
import os
from PyEGRO.meta.gpr import MetaTraining
# Import visualization module
from PyEGRO.meta.gpr.visualization import visualize_gpr

def run_gpr_synthetic():
    """Run GPR with synthetic data example."""
    # Set random seed for reproducibility
    np.random.seed(42)

    # Define a true function to sample from
    def true_function(x):
        return x * np.sin(x)

    # Generate synthetic data
    # Training data
    n_train = 30
    X_train = np.random.uniform(0, 10, n_train).reshape(-1, 1)
    y_train = true_function(X_train) + 0.5 * np.random.randn(n_train, 1)  # Add noise

    # Testing data
    n_test = 50
    X_test = np.linspace(0, 12, n_test).reshape(-1, 1)
    y_test = true_function(X_test) + 0.25 * np.random.randn(n_test, 1)  # Add less noise

    # Define bounds for visualization
    bounds = np.array([[0, 12]])
    variable_names = ['x']

    # Initialize and train GPR model
    print("Training GPR model with synthetic data...")
    meta = MetaTraining(
        num_iterations=500,
        prefer_gpu=True,
        show_progress=True,
        output_dir='RESULT_MODEL_GPR_SYNTHETIC',
        kernel='matern05',
        learning_rate=0.01,
        patience=50
    )

    # Train model with synthetic data
    model, scaler_X, scaler_y = meta.train(
        X=X_train,
        y=y_train,
        X_test=X_test,
        y_test=y_test,
        feature_names=variable_names
    )

    # Generate visualization
    figures = visualize_gpr(
        meta=meta,
        X_train=X_train,
        y_train=y_train,
        X_test=X_test,
        y_test=y_test,
        variable_names=variable_names,
        bounds=bounds,
        savefig=True
    )
    
    return model, meta


# ===================================================
# GPR --> load .csv data 
# ===================================================

import numpy as np
import matplotlib.pyplot as plt
import json
import pandas as pd
import os
from PyEGRO.meta.gpr import MetaTraining
from PyEGRO.meta.gpr.visualization import visualize_gpr

def run_gpr_csv():
    """Run GPR with CSV data example."""
    # Load initial data and problem configuration
    with open('DATA_PREPARATION/data_info.json', 'r') as f:
        data_info = json.load(f)

    # Load training data
    training_data = pd.read_csv('DATA_PREPARATION/training_data.csv')

    # Load testing data
    test_data = pd.read_csv('DATA_PREPARATION/testing_data.csv')

    # Get problem configuration
    bounds = np.array(data_info['input_bound'])
    variable_names = [var['name'] for var in data_info['variables']]

    # Get target column name (default to 'y' if not specified)
    target_column = data_info.get('target_column', 'y')

    # Extract features and targets
    X_train = training_data[variable_names].values
    y_train = training_data[target_column].values.reshape(-1, 1)

    # Extract testing data
    X_test = test_data[variable_names].values
    y_test = test_data[target_column].values.reshape(-1, 1)

    # Initialize and train GPR model
    print("Training GPR model with CSV data...")
    meta = MetaTraining(
        num_iterations=500,
        prefer_gpu=True,
        show_progress=True,
        output_dir='RESULT_MODEL_GPR',
        kernel='matern05',
        learning_rate=0.01,
        patience=50
    )

    # Train model with testing data
    model, scaler_X, scaler_y = meta.train(
        X=X_train,
        y=y_train,
        X_test=X_test,
        y_test=y_test,
        feature_names=variable_names
    )

    # Generate visualization
    figures = visualize_gpr(
        meta=meta,
        X_train=X_train,
        y_train=y_train,
        X_test=X_test,
        y_test=y_test,
        variable_names=variable_names,
        bounds=bounds,
        savefig=True
    )
    
    return model, meta

# ===================================================
# Example runner
# ===================================================

# Example usage
if __name__ == "__main__":

    # print("Running GPR with CSV data example...")
    run_gpr_csv()

