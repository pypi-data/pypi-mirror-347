"""
Examples for using the PyEGRO Co-Kriging Module.

This file contains example functions demonstrating how to use the
Co-Kriging module with different data sources.
"""

# ===================================================
# Cokriging --> synthetic data 
# ===================================================

import numpy as np
import matplotlib.pyplot as plt
import os
from PyEGRO.meta.cokriging import MetaTrainingCoKriging
from PyEGRO.meta.cokriging.visualization import visualize_cokriging

def run_cokriging_synthetic():
    """Run Co-Kriging with synthetic data example."""
    # Set random seed for reproducibility
    np.random.seed(42)

    # Define high and low fidelity functions
    def high_fidelity_function(x):
        return (6*x - 2)**2 * np.sin(12*x - 4)

    def low_fidelity_function(x):
        return 0.5 * high_fidelity_function(x) + 10 * (x - 0.5) - 5

    # Generate synthetic data
    # Low fidelity: more samples but less accurate
    n_low = 80
    X_low = np.random.uniform(0, 1, n_low).reshape(-1, 1)
    y_low = low_fidelity_function(X_low) + np.random.normal(0, 1.0, X_low.shape)  # More noise

    # High fidelity: fewer samples but more accurate
    n_high = 20
    X_high = np.random.uniform(0, 1, n_high).reshape(-1, 1)
    y_high = high_fidelity_function(X_high) + np.random.normal(0, 0.5, X_high.shape)  # Less noise

    # Test data
    n_test = 40
    X_test = np.linspace(0, 1, n_test).reshape(-1, 1)
    y_test = high_fidelity_function(X_test) + np.random.normal(0, 0.3, X_test.shape)  # Even less noise

    # Define bounds and variable names
    bounds = np.array([[0, 1]])
    variable_names = ['x']

    # Initialize and train Co-Kriging model
    print("Training Co-Kriging model with synthetic data...")
    meta = MetaTrainingCoKriging(
        num_iterations=300,
        prefer_gpu=True,
        show_progress=True,
        output_dir='RESULT_MODEL_COKRIGING_SYNTHETIC'
    )

    # Train model with synthetic data
    model, scaler_X, scaler_y = meta.train(
        X_low=X_low, 
        y_low=y_low, 
        X_high=X_high, 
        y_high=y_high,
        X_test=X_test,
        y_test=y_test,
        feature_names=variable_names
    )

    # Generate visualization
    figures = visualize_cokriging(
        meta=meta,
        X_low=X_low,
        y_low=y_low,
        X_high=X_high,
        y_high=y_high,
        X_test=X_test,
        y_test=y_test,
        variable_names=variable_names,
        bounds=bounds,
        savefig=True
    )
    
    return model, meta


# ===================================================
# Cokriging --> load .csv data 
# ===================================================

import numpy as np
import matplotlib.pyplot as plt
import json
import pandas as pd
import os
from PyEGRO.meta.cokriging import MetaTrainingCoKriging
from PyEGRO.meta.cokriging.visualization import visualize_cokriging

def run_cokriging_csv():
    """Run Co-Kriging with CSV data example."""
    # Load initial data and problem configuration
    with open('DATA_PREPARATION/data_info.json', 'r') as f:
        data_info = json.load(f)

    # Load high and low fidelity training data
    high_fidelity_data = pd.read_csv('DATA_PREPARATION/training_data_high.csv')
    low_fidelity_data = pd.read_csv('DATA_PREPARATION/training_data_low.csv')

    # Load testing data
    test_data = pd.read_csv('DATA_PREPARATION/testing_data.csv')

    # Add fidelity indicators
    high_fidelity_data['fidelity'] = 1  # Numeric fidelity indicator (1 for high)
    low_fidelity_data['fidelity'] = 0   # Numeric fidelity indicator (0 for low)

    # Get problem configuration
    bounds = np.array(data_info['input_bound'])
    variable_names = [var['name'] for var in data_info['variables']]

    # Get target column name (default to 'y' if not specified)
    target_column = data_info.get('target_column', 'y')

    # Extract features and targets
    X_high = high_fidelity_data.drop(['fidelity', target_column], axis=1, errors='ignore').values
    y_high = high_fidelity_data[target_column].values.reshape(-1, 1)

    X_low = low_fidelity_data.drop(['fidelity', target_column], axis=1, errors='ignore').values
    y_low = low_fidelity_data[target_column].values.reshape(-1, 1)

    # Extract testing data
    X_test = test_data.drop([target_column], axis=1, errors='ignore').values
    y_test = test_data[target_column].values.reshape(-1, 1)

    # Initialize and train model
    print("Training Co-Kriging model with testing data evaluation...")
    meta = MetaTrainingCoKriging(
        num_iterations=300,
        prefer_gpu=True,
        show_progress=True,
        output_dir='RESULT_MODEL_COKRIGING'
    )

    # Train model with testing data
    model, scaler_X, scaler_y = meta.train(
        X_low=X_low, 
        y_low=y_low, 
        X_high=X_high, 
        y_high=y_high,
        X_test=X_test,
        y_test=y_test,
        feature_names=variable_names
    )

    # Standard visualization including test data
    figures = visualize_cokriging(
        meta=meta,
        X_low=X_low,
        y_low=y_low,
        X_high=X_high,
        y_high=y_high,
        X_test=X_test,
        y_test=y_test,
        variable_names=variable_names,
        bounds=bounds,
        savefig=True
    )
    
    return model, meta


# ===================================================
# Example with 2D inputs
# ===================================================

def run_cokriging_2d_synthetic():
    """Run Co-Kriging with 2D synthetic data example."""
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Define high and low fidelity 2D functions
    def high_fidelity_function(x1, x2):
        return np.sin(x1) * np.cos(x2) + 0.2 * x1 * x2
    
    def low_fidelity_function(x1, x2):
        return 0.5 * high_fidelity_function(x1, x2) + 0.2 * x1 - 0.1 * x2 + 0.5
    
    # Generate synthetic data
    # Low fidelity: more samples but less accurate
    n_low = 100
    X1_low = np.random.uniform(-2, 2, n_low)
    X2_low = np.random.uniform(-2, 2, n_low)
    X_low = np.column_stack([X1_low, X2_low])
    y_low = low_fidelity_function(X1_low, X2_low).reshape(-1, 1) + np.random.normal(0, 0.1, (n_low, 1))
    
    # High fidelity: fewer samples but more accurate
    n_high = 25
    X1_high = np.random.uniform(-2, 2, n_high)
    X2_high = np.random.uniform(-2, 2, n_high)
    X_high = np.column_stack([X1_high, X2_high])
    y_high = high_fidelity_function(X1_high, X2_high).reshape(-1, 1) + np.random.normal(0, 0.05, (n_high, 1))
    
    # Test data: grid for visualization
    n_test = 16
    X1_test = np.linspace(-2, 2, 4)
    X2_test = np.linspace(-2, 2, 4)
    X1_grid, X2_grid = np.meshgrid(X1_test, X2_test)
    X1_test = X1_grid.flatten()
    X2_test = X2_grid.flatten()
    X_test = np.column_stack([X1_test, X2_test])
    y_test = high_fidelity_function(X1_test, X2_test).reshape(-1, 1) + np.random.normal(0, 0.02, (n_test, 1))
    
    # Define bounds and variable names
    bounds = np.array([[-2, 2], [-2, 2]])
    variable_names = ['x1', 'x2']
    
    # Initialize and train Co-Kriging model
    print("Training Co-Kriging model with 2D synthetic data...")
    meta = MetaTrainingCoKriging(
        num_iterations=300,
        prefer_gpu=True,
        show_progress=True,
        output_dir='RESULT_MODEL_COKRIGING_2D'
    )
    
    # Train model with synthetic data
    model, scaler_X, scaler_y = meta.train(
        X_low=X_low, 
        y_low=y_low, 
        X_high=X_high, 
        y_high=y_high,
        X_test=X_test,
        y_test=y_test,
        feature_names=variable_names
    )
    
    # Generate visualization
    figures = visualize_cokriging(
        meta=meta,
        X_low=X_low,
        y_low=y_low,
        X_high=X_high,
        y_high=y_high,
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

if __name__ == "__main__":
    import sys
    
    # Handle command line arguments if provided
    if len(sys.argv) > 1:
        example = sys.argv[1].lower()
        
        if example == "synthetic":
            print("Running Co-Kriging with synthetic data example...")
            run_cokriging_synthetic()
        elif example == "csv":
            print("Running Co-Kriging with CSV data example...")
            run_cokriging_csv()
        elif example == "2d":
            print("Running Co-Kriging with 2D synthetic data example...")
            run_cokriging_2d_synthetic()
        else:
            print(f"Unknown example: {example}")
            print("Available examples: synthetic, csv, 2d")
    else:
        # Run all examples by default
        print("Running all examples...\n")
        
        print("\n=== Co-Kriging with synthetic data ===")
        try:
            run_cokriging_synthetic()
            print("Completed successfully!")
        except Exception as e:
            print(f"Error: {e}")
        
        print("\n=== Co-Kriging with CSV data ===")
        try:
            run_cokriging_csv()
            print("Completed successfully!")
        except FileNotFoundError:
            print("Required data files not found. Make sure DATA_PREPARATION directory exists with necessary files.")
        except Exception as e:
            print(f"Error: {e}")
        
        print("\n=== Co-Kriging with 2D synthetic data ===")
        try:
            run_cokriging_2d_synthetic()
            print("Completed successfully!")
        except Exception as e:
            print(f"Error: {e}")
        
        print("\nAll examples have been run. Check the respective output directories for results.")