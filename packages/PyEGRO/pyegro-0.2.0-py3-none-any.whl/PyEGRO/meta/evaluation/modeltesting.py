#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Model testing module for PyEGRO package to evaluate trained GPyTorch models on unseen data.
This module supports both GPR and CoKriging models.
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import joblib
import torch
import warnings
import importlib.util
import logging


# Configure matplotlib
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['font.size'] = 20
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['axes.labelsize'] = 20
plt.rcParams['xtick.labelsize'] = 20
plt.rcParams['ytick.labelsize'] = 20


class ModelTester:
    """Class for testing trained models on unseen data."""
    
    def __init__(self, model_dir='RESULT_MODEL_GPR', model_name=None, model_path=None, logger=None):
        """
        Initialize the model tester.
        
        Args:
            model_dir: Directory containing trained model files
            model_name: Base name of the model file without extension
            model_path: Direct path to the model file
            logger: Logger object for logging messages
        """
        self.model_dir = model_dir
        self.model_name = model_name
        self.model_path = model_path
        self.logger = logger
        self.model = None
        self.model_type = None  # 'gpr' or 'cokriging'
        self.model_handler = None
        self.scaler_X = None
        self.scaler_y = None
        self.test_results = None
        
        # If model_path is provided directly, extract model_dir and model_name from it
        if self.model_path is not None:
            self.model_dir = os.path.dirname(self.model_path)
            file_name = os.path.basename(self.model_path)
            # Remove extension to get model_name
            self.model_name = os.path.splitext(file_name)[0]
            self._log(f"Using model path: {self.model_path}")
            self._log(f"Extracted model_dir: {self.model_dir}, model_name: {self.model_name}")
        elif self.model_name is None:
            # Infer model name from directory if not provided
            if 'GPR' in self.model_dir:
                self.model_name = 'gpr_model'
                self.model_type = 'gpr'
            elif 'COKRIGING' in self.model_dir:
                self.model_name = 'cokriging_model'
                self.model_type = 'cokriging'
            else:
                self.model_name = 'model'  # Default name
                
        # Determine model type from name if not already set
        if self.model_type is None:
            if 'gpr' in self.model_name.lower():
                self.model_type = 'gpr'
            elif 'cokriging' in self.model_name.lower() or 'cokrig' in self.model_name.lower():
                self.model_type = 'cokriging'
    
    def _log(self, message, level='info'):
        """Log a message if logger is available."""
        if self.logger:
            if level == 'info':
                self.logger.info(message)
            elif level == 'error':
                self.logger.error(message)
            elif level == 'warning':
                self.logger.warning(message)
        else:
            print(message)
    
    def load_model(self):
        """Load the trained model and scalers from disk."""
        self._log(f"Loading {self.model_type} model '{self.model_name}' from {self.model_dir}")
        
        # Determine file path for model
        if hasattr(self, 'model_path') and self.model_path is not None:
            model_path = self.model_path
        else:
            model_path = os.path.join(self.model_dir, f"{self.model_name}.pth")
            
        self._log(f"Model file path: {model_path}")
        
        # Check for scaler files
        try:
            scaler_x_path = os.path.join(self.model_dir, 'scaler_X.pkl')
            if not os.path.exists(scaler_x_path):
                scaler_x_path = os.path.join(self.model_dir, 'scaler_x.pkl')
                
            scaler_y_path = os.path.join(self.model_dir, 'scaler_y.pkl')
            if not os.path.exists(scaler_y_path):
                scaler_y_path = os.path.join(self.model_dir, 'scaler_Y.pkl')
                
            self._log(f"X scaler path: {scaler_x_path}")
            self._log(f"Y scaler path: {scaler_y_path}")
            
            # Load model using appropriate handler
            if self.model_type == 'gpr':
                try:
                    # Try to import DeviceAgnosticGPR
                    spec = importlib.util.find_spec("PyEGRO.meta.gpr.gpr_utils")
                    if spec is not None:
                        gpr_utils = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(gpr_utils)
                        self._log("Imported gpr_utils from PyEGRO.meta.gpr")
                        self.model_handler = gpr_utils.DeviceAgnosticGPR(prefer_gpu=False)
                    else:
                        # Try local import
                        from ..gpr.gpr_utils import DeviceAgnosticGPR
                        self._log("Imported gpr_utils locally")
                        self.model_handler = DeviceAgnosticGPR(prefer_gpu=False)
                        
                    self.model_handler.load_model(self.model_dir)
                    self.model = self.model_handler.model
                    self.scaler_X = self.model_handler.scaler_X
                    self.scaler_y = self.model_handler.scaler_y
                    
                except Exception as e:
                    self._log(f"Error loading GPR model with handler: {str(e)}", level='error')
                    raise
                    
            elif self.model_type == 'cokriging':
                try:
                    # Try to import DeviceAgnosticCoKriging
                    spec = importlib.util.find_spec("PyEGRO.meta.cokriging.cokriging_utils")
                    if spec is not None:
                        cokriging_utils = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(cokriging_utils)
                        self._log("Imported cokriging_utils from PyEGRO.meta.cokriging")
                        self.model_handler = cokriging_utils.DeviceAgnosticCoKriging(prefer_gpu=False)
                    else:
                        # Try local import
                        from ..cokriging.cokriging_utils import DeviceAgnosticCoKriging
                        self._log("Imported cokriging_utils locally")
                        self.model_handler = DeviceAgnosticCoKriging(prefer_gpu=False)
                        
                    self.model_handler.load_model(self.model_dir)
                    self.model = self.model_handler.model
                    self.scaler_X = self.model_handler.scaler_X
                    self.scaler_y = self.model_handler.scaler_y
                    
                except Exception as e:
                    self._log(f"Error loading CoKriging model with handler: {str(e)}", level='error')
                    raise
            else:
                self._log(f"Unknown model type: {self.model_type}", level='error')
                raise ValueError(f"Unknown model type: {self.model_type}")
            
            self._log("Model and scalers loaded successfully")
            
        except Exception as e:
            self._log(f"Error loading model: {str(e)}", level='error')
            raise
            
        return self
    
    def load_test_data(self, data_path=None, feature_cols=None, target_col='y', n_samples=100, n_features=2):
        """
        Load test data from CSV file or generate synthetic test data.
        
        Args:
            data_path: Path to the CSV file containing test data
            feature_cols: List of feature column names
            target_col: Target column name
            n_samples: Number of samples for synthetic data
            n_features: Number of features for synthetic data
            
        Returns:
            X_test: Test features
            y_test: Test targets
        """
        if data_path and os.path.exists(data_path):
            self._log(f"Loading test data from {data_path}")
            try:
                df = pd.read_csv(data_path)
                
                if not feature_cols:
                    # If features not specified, use all columns except target
                    feature_cols = [col for col in df.columns if col != target_col]
                
                # Check if target_col exists
                if target_col not in df.columns:
                    self._log(f"Target column '{target_col}' not found in CSV. Available columns: {df.columns.tolist()}", level='error')
                    raise ValueError(f"Target column '{target_col}' not found in CSV")
                
                # Check if all feature_cols exist
                missing_cols = [col for col in feature_cols if col not in df.columns]
                if missing_cols:
                    self._log(f"Feature columns {missing_cols} not found in CSV. Available columns: {df.columns.tolist()}", level='error')
                    raise ValueError(f"Feature columns {missing_cols} not found in CSV")
                
                X_test = df[feature_cols].values
                y_test = df[target_col].values.reshape(-1, 1)
                
            except Exception as e:
                self._log(f"Error loading CSV data: {str(e)}", level='error')
                self._log("Falling back to synthetic data generation")
                X_test, y_test = self._generate_synthetic_data(n_samples, n_features)
        else:
            if data_path:
                self._log(f"Data file not found at {data_path}", level='warning')
            self._log("Generating synthetic test data")
            X_test, y_test = self._generate_synthetic_data(n_samples, n_features)
        
        self._log(f"Test data prepared: {X_test.shape[0]} samples with {X_test.shape[1]} features")
        return X_test, y_test
    
    def _generate_synthetic_data(self, n_samples=100, n_features=2):
        """Generate synthetic test data."""
        self._log(f"Generating {n_samples} synthetic samples with {n_features} features")
        
        # Create random features
        X_test = np.random.rand(n_samples, n_features)
        
        # Generate synthetic targets with some noise
        true_func = lambda X: np.sin(X[:, 0]) + np.cos(X[:, 1]) if n_features > 1 else np.sin(X.flatten())
        y_test = true_func(X_test) + 0.1 * np.random.randn(n_samples)
        y_test = y_test.reshape(-1, 1)
        
        return X_test, y_test
    
    def evaluate(self, X_test, y_test):
        """
        Evaluate the model performance on test data.
        
        Args:
            X_test: Test features
            y_test: Test targets
            
        Returns:
            self with updated test_results
        """
        if self.model_handler is None:
            self.load_model()
        
        self._log("Making predictions with model")
        
        try:
            if self.model_type == 'gpr':
                # Use the DeviceAgnosticGPR prediction method
                y_pred, std_dev = self.model_handler.predict(X_test)
            elif self.model_type == 'cokriging':
                # Use the DeviceAgnosticCoKriging prediction method
                y_pred, std_dev = self.model_handler.predict(X_test, fidelity='high')
            else:
                self._log(f"Unknown model type: {self.model_type}", level='error')
                raise ValueError(f"Unknown model type: {self.model_type}")
            
        except Exception as e:
            self._log(f"Error making predictions: {str(e)}", level='error')
            raise
        
        # Calculate metrics
        r2 = r2_score(y_test, y_pred)
        mse = np.mean((y_test - y_pred) ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(y_test - y_pred))
        
        self._log(f"Test R² Score: {r2:.4f}")
        self._log(f"Test RMSE: {rmse:.4f}")
        self._log(f"Test MAE: {mae:.4f}")
        
        self.test_results = {
            'r2': r2,
            'mse': mse,
            'rmse': rmse,
            'mae': mae,
            'y_test': y_test,
            'y_pred': y_pred,
            'std_dev': std_dev,
            'model_type': self.model_type
        }
        
        return self
    
    def save_results(self, output_dir='test_results'):
        """
        Save test results and generate plots.
        
        Args:
            output_dir: Directory to save results
            
        Returns:
            self
        """
        if self.test_results is None:
            raise ValueError("No test results available. Run evaluate() first.")
        
        # Create model-specific output directory
        model_output_dir = os.path.join(output_dir, self.model_name)
        os.makedirs(model_output_dir, exist_ok=True)
        
        # Save metrics to file
        metrics_file = os.path.join(model_output_dir, f'{self.model_name}_metrics.txt')
        with open(metrics_file, 'w', encoding='utf-8') as f:  # Add explicit UTF-8 encoding
            f.write(f"Model: {self.model_name}\n")
            f.write(f"Type: {self.model_type}\n")
            f.write(f"Directory: {self.model_dir}\n")
            f.write(f"Test R² Score: {self.test_results['r2']:.4f}\n")
            f.write(f"Test RMSE: {self.test_results['rmse']:.4f}\n")
            f.write(f"Test MAE: {self.test_results['mae']:.4f}\n")
        
        # Save predictions to CSV
        pred_df = pd.DataFrame({
            'y_true': self.test_results['y_test'].flatten(),
            'y_pred': self.test_results['y_pred'].flatten()
        })
        
        if self.test_results['std_dev'] is not None:
            pred_df['std_dev'] = self.test_results['std_dev'].flatten()
            
        pred_df.to_csv(os.path.join(model_output_dir, f'{self.model_name}_predictions.csv'), index=False)
        
        self._log(f"Results saved to {model_output_dir}")
        return self
    
    def plot_results(self, output_dir='test_results', show_plots=True, save_plots=True, 
                    smooth=True, smooth_window=11):
        """
        Generate and optionally save plots of test results.
        
        Args:
            output_dir: Directory to save plots
            show_plots: Whether to display plots
            save_plots: Whether to save plots to disk
            smooth: Whether to apply smoothing to uncertainty plots
            smooth_window: Window size for smoothing filter
            
        Returns:
            Dictionary of figure objects
        """
        if self.test_results is None:
            raise ValueError("No test results available. Run evaluate() first.")
        
        # Create model-specific output directory
        model_output_dir = os.path.join(output_dir, self.model_name)
        if save_plots:
            os.makedirs(model_output_dir, exist_ok=True)
        
        figures = {}
        
        # Prediction vs Actual plot
        fig1 = self._plot_prediction_vs_actual(
            self.test_results['y_test'], 
            self.test_results['y_pred'],
            title=f"Test Predictions (R² = {self.test_results['r2']:.4f})"
        )
        figures['predictions'] = fig1
        
        if save_plots:
            fig1.savefig(os.path.join(model_output_dir, f'{self.model_name}_predictions.png'), dpi=300, bbox_inches='tight')
        
        # Residuals plot
        fig2 = self._plot_residuals(
            self.test_results['y_test'], 
            self.test_results['y_pred'],
            title=f"Test Residuals"
        )
        figures['residuals'] = fig2
        
        if save_plots:
            fig2.savefig(os.path.join(model_output_dir, f'{self.model_name}_residuals.png'), dpi=300, bbox_inches='tight')
        
        # Uncertainty plot if available
        if self.test_results['std_dev'] is not None:
            fig3 = self._plot_prediction_uncertainty(
                self.test_results['y_test'],
                self.test_results['y_pred'],
                self.test_results['std_dev'],
                title=f"Predictions with Uncertainty",
                smooth=smooth,
                smooth_window=smooth_window
            )
            figures['uncertainty'] = fig3
            
            if save_plots:
                fig3.savefig(os.path.join(model_output_dir, f'{self.model_name}_uncertainty.png'), dpi=300, bbox_inches='tight')
        
        if show_plots:
            plt.show()
        
        return figures
    

    def _plot_prediction_vs_actual(self, y_true, y_pred, title="Predictions vs Actual", figsize=(5.5, 5)):
        """Create a scatter plot of predicted vs actual values with a perfect prediction line."""
        fig, ax = plt.subplots(figsize=figsize)
        
        # Flatten arrays if needed
        y_true = y_true.flatten()
        y_pred = y_pred.flatten()
        
        # Plot scatter of predictions
        ax.scatter(y_true, y_pred, alpha=1, edgecolors='black', color='black', label='Predictions')
        
        # Calculate limits for the identity line
        min_val = min(np.min(y_true), np.min(y_pred))
        max_val = max(np.max(y_true), np.max(y_pred))
        
        # Add some padding
        range_val = max_val - min_val
        min_val -= range_val * 0.05
        max_val += range_val * 0.05
        
        # Plot identity line (perfect predictions)
        ax.plot([min_val, max_val], [min_val, max_val], 'r-', label='Perfect Prediction')
        
        ax.set_xlabel('Actual Values')
        ax.set_ylabel('Predicted Values')
        ax.set_title(title)
        ax.legend(fontsize = 12)
        #ax.grid(True, alpha=0.3, linestyle = '--')
        

        plt.tight_layout()
        return fig
    
    def _plot_residuals(self, y_true, y_pred, title="Residuals", figsize=(5.5, 5)):
        """Create a residual plot (residuals vs predicted values)."""
        # Calculate residuals
        residuals = y_true.flatten() - y_pred.flatten()
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot residuals
        ax.scatter(y_pred.flatten(), residuals, edgecolors='black', alpha=0.6, color='green')
        
        # Add horizontal line at y=0
        ax.axhline(y=0, color='r', linestyle='-', alpha=0.7)
        
        ax.set_xlabel('Predicted Values')
        ax.set_ylabel('Residuals')
        ax.set_title(title)
        #ax.grid(True, alpha=0.3, linestyle = '--')
        
        plt.tight_layout()
        return fig
    
    def _plot_prediction_uncertainty(self, y_true, y_pred, std_dev, title="Predictions with Uncertainty", 
                                figsize=(5.5, 5), smooth=True, smooth_window=11):
        """
        Create a plot of predictions with uncertainty visualization.
        
        Args:
            y_true: Array of true target values
            y_pred: Array of predicted target values
            std_dev: Array of standard deviations for predictions
            title: Plot title
            figsize: Figure size
            smooth: Whether to apply smoothing
            smooth_window: Window size for smoothing filter
            
        Returns:
            matplotlib Figure object
        """
        import numpy as np
        import matplotlib.pyplot as plt
        from matplotlib.collections import PolyCollection
        from scipy.signal import savgol_filter
        
        # Sort by true values for better visualization
        indices = np.argsort(y_true.flatten())
        y_true_sorted = y_true.flatten()[indices]
        y_pred_sorted = y_pred.flatten()[indices]
        std_dev_sorted = std_dev.flatten()[indices] if std_dev is not None else None
        
        # Apply smoothing if requested
        if smooth and len(y_pred_sorted) > smooth_window:
            # Make sure window size is odd (required for Savitzky-Golay filter)
            if smooth_window % 2 == 0:
                smooth_window += 1
                
            # Apply Savitzky-Golay filter for smoothing
            try:
                # For predictions
                y_pred_smooth = savgol_filter(y_pred_sorted, smooth_window, 2)
                
                # For confidence intervals
                if std_dev_sorted is not None:
                    std_dev_smooth = savgol_filter(std_dev_sorted, smooth_window, 2)
                    # Ensure std dev remains positive
                    std_dev_smooth = np.maximum(std_dev_smooth, 0.0001)
                else:
                    std_dev_smooth = None
            except ValueError:
                # If Savitzky-Golay fails (e.g., window too large), fall back to original data
                self._log("Smoothing failed, using original data.", level='warning')
                y_pred_smooth = y_pred_sorted
                std_dev_smooth = std_dev_sorted
        else:
            # Use original data
            y_pred_smooth = y_pred_sorted
            std_dev_smooth = std_dev_sorted
        
        # Sample indices (x-axis)
        x_indices = np.arange(len(y_true_sorted))
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Calculate the confidence interval bounds
        if std_dev_smooth is not None:
            upper_bound = y_pred_smooth + 2 * std_dev_smooth
            lower_bound = y_pred_smooth - 2 * std_dev_smooth
            
            # Create vertices for the polygon (confidence interval region)
            vertices = []
            for i in range(len(x_indices)):
                vertices.append((x_indices[i], lower_bound[i]))
            for i in range(len(x_indices)-1, -1, -1):
                vertices.append((x_indices[i], upper_bound[i]))
            
            # Create a PolyCollection
            poly = PolyCollection([vertices], alpha=0.2, facecolor='b', edgecolor='none')
            ax.add_collection(poly)
        
        # Plot true values as a line with points
        ax.plot(x_indices, y_true_sorted, 'ko-', label='True Values', alpha=0.7, markersize = 5, linewidth=1.5)
        
        # Plot smoothed prediction mean line (no markers for cleaner look)
        ax.plot(x_indices, y_pred_smooth, 'b--', label='Predicted Mean', linewidth=2, alpha=0.8)
        
        # Add a legend item for the confidence interval
        ax.plot([], [], color='b', alpha=0.2, linewidth=10, label='95% Confidence Interval')
        
        # Customize the plot
        ax.set_xlabel('Sample Index (sorted)')
        ax.set_ylabel('Value')
        ax.set_title(title)
        ax.legend(fontsize = 12)
        #ax.grid(True, alpha=0.3, linestyle='--')
        
        # Add minor grid lines
        # ax.grid(True, which='minor', alpha=0.15, linestyle=':')
        # ax.minorticks_on()
        
        plt.tight_layout()
        return fig


# Convenience functions for direct usage
def load_and_test_model(data_path=None, model_dir=None, model_name=None, model_path=None, 
                        output_dir='test_results', feature_cols=None, target_col='y', 
                        logger=None, show_plots=True, smooth=True, smooth_window=11):
    """
    Convenience function to load a model and test it in one call.
    
    Args:
        data_path: Path to the CSV file containing test data
        model_dir: Directory containing trained model files
        model_name: Base name of the model file without extension
        model_path: Direct path to the model file (overrides model_dir and model_name if provided)
        output_dir: Directory to save results
        feature_cols: List of feature column names
        target_col: Target column name
        logger: Logger object for logging messages
        show_plots: Whether to display plots
        smooth: Whether to apply smoothing to uncertainty plots
        smooth_window: Window size for smoothing filter
        
    Returns:
        Dictionary of test results
    """
    # Sanity checks
    if model_path is None and model_dir is None:
        error_msg = "Either model_path or model_dir must be provided"
        if logger:
            logger.error(error_msg)
        else:
            print(error_msg)
        raise ValueError(error_msg)
    
    # Create tester instance with appropriate parameters
    if model_path is not None:
        tester = ModelTester(model_path=model_path, logger=logger)
    else:
        tester = ModelTester(model_dir=model_dir, model_name=model_name, logger=logger)
    
    try:
        tester.load_model()
    except Exception as e:
        if logger:
            logger.error(f"Error loading model: {str(e)}")
        else:
            print(f"Error loading model: {str(e)}")
        raise
    
    try:
        X_test, y_test = tester.load_test_data(
            data_path=data_path,
            feature_cols=feature_cols,
            target_col=target_col
        )
    except Exception as e:
        if logger:
            logger.error(f"Error loading test data: {str(e)}")
        else:
            print(f"Error loading test data: {str(e)}")
        raise
    
    try:
        tester.evaluate(X_test, y_test)
        tester.save_results(output_dir=output_dir)
        tester.plot_results(output_dir=output_dir, show_plots=show_plots, 
                           smooth=smooth, smooth_window=smooth_window)
    except Exception as e:
        if logger:
            logger.error(f"Error during evaluation: {str(e)}")
        else:
            print(f"Error during evaluation: {str(e)}")
        raise
    
    return tester.test_results


