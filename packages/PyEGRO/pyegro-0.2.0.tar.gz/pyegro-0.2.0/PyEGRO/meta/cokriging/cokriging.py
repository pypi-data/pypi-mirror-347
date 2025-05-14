"""
Co-Kriging (multi-fidelity) modeling for PyEGRO with enhanced testing and visualization.

This module provides tools for training and managing Co-Kriging models
that can combine low-fidelity (cheap) and high-fidelity (expensive) data
for more efficient surrogate modeling, with added testing data evaluation.
"""

import os
import torch
import gpytorch
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from sklearn.preprocessing import StandardScaler
from typing import Tuple, Optional, Dict, List, Union

# Rich progress bar imports
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn
from rich.progress import TimeRemainingColumn, TimeElapsedColumn, SpinnerColumn
from rich.console import Console
import platform

# Import CoKriging kernel and model from utilities
from .cokriging_utils import CoKrigingModel, CoKrigingKernel

# Suppress warnings
import warnings
from gpytorch.utils.warnings import GPInputWarning, NumericalWarning
warnings.filterwarnings("ignore", category=GPInputWarning)
warnings.filterwarnings("ignore", category=NumericalWarning)


class MetaTrainingCoKriging:
    """
    Meta-training manager for Co-Kriging (multi-fidelity) models.
    
    This class provides comprehensive functionality for training Co-Kriging models
    that combine low and high fidelity data sources, with built-in visualization,
    progress tracking, and hardware optimization.
    """
    def __init__(self,
                 num_iterations: int = 1000,
                 prefer_gpu: bool = True,
                 show_progress: bool = True,
                 show_hardware_info: bool = True,
                 show_model_info: bool = True,
                 output_dir: str = 'RESULT_MODEL_COKRIGING',
                 kernel: str = 'matern25',
                 learning_rate: float = 0.01,
                 patience: int = 50):
        """
        Initialize MetaTrainingCoKriging with configuration.
        
        Args:
            num_iterations: Number of training iterations (default: 1000)
            prefer_gpu: Whether to use GPU if available (default: True)
            show_progress: Whether to show detailed progress (default: True)
            show_hardware_info: Whether to show system hardware info (default: True)
            show_model_info: Whether to show model architecture info (default: True)
            output_dir: Directory for saving results (default: 'RESULT_MODEL_COKRIGING')
            kernel: Kernel to use for base GPR model (default: 'matern25', options: 'matern25', 'matern15', 'matern05', 'rbf')
            learning_rate: Learning rate for optimizer (default: 0.01)
            patience: Number of iterations to wait for improvement before early stopping (default: 50)
        """
        self.num_iterations = num_iterations
        self.show_progress = show_progress
        self.show_hardware_info = show_hardware_info
        self.show_model_info = show_model_info
        self.output_dir = output_dir
        self.kernel = kernel
        self.learning_rate = learning_rate
        self.patience = patience
        
        # Setup device
        self.device = torch.device("cuda" if torch.cuda.is_available() and prefer_gpu else "cpu")
        self.console = Console()
        
        # Initialize model components
        self.model = None
        self.likelihood = None
        self.scaler_X = None
        self.scaler_y = None
        
        # Track feature names
        self.variable_names = None
        
        # Store metrics
        self.metrics = {}

    def print_device_info(self):
        """Print information about the computing device being used."""
        if self.device.type == "cuda":
            device_name = torch.cuda.get_device_name(0)
            memory_gb = torch.cuda.get_device_properties(0).total_memory / 1024**3
            cuda_version = torch.version.cuda
            
            self.console.print("\n[green]Hardware Configuration[/green]")
            self.console.print(f"[white]• Device:[/white] GPU - {device_name}")
            self.console.print(f"[white]• GPU Memory:[/white] {memory_gb:.1f} GB")
            self.console.print(f"[white]• CUDA Version:[/white] {cuda_version}")
        else:
            import psutil
            device_name = platform.processor() or "Unknown CPU"
            memory_gb = psutil.virtual_memory().total / 1024**3
            cpu_cores = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq().max if psutil.cpu_freq() else "Unknown"
            
            self.console.print("\n[green]Hardware Configuration[/green]")
            self.console.print(f"[white]• Device:[/white] CPU - {device_name}")
            self.console.print(f"[white]• CPU Cores:[/white] {cpu_cores}")
            self.console.print(f"[white]• CPU Frequency:[/white] {cpu_freq:.2f} MHz" if isinstance(cpu_freq, (int, float)) else f"[white]• CPU Frequency:[/white] {cpu_freq}")
            self.console.print(f"[white]• System Memory:[/white] {memory_gb:.1f} GB")
        
        self.console.print(f"[white]• PyTorch Version:[/white] {torch.__version__}")
        self.console.print(f"[white]• GPyTorch Version:[/white] {gpytorch.__version__}")
        self.console.print(f"[white]• NumPy Version:[/white] {np.__version__}")
        self.console.print(f"[white]• Operating System:[/white] {platform.system()} {platform.version()}\n")

    def print_model_info(self, input_shape_low, input_shape_high):
        """Print information about the model architecture and training setup."""
        self.console.print("\n[green]Model Configuration[/green]")
        self.console.print(f"[white]• Model Type:[/white] Co-Kriging (Multi-fidelity GPR)")
        
        # Map kernel names to readable descriptions
        kernel_descriptions = {
            'matern25': 'Matérn 2.5 with ARD',
            'matern15': 'Matérn 1.5 with ARD',
            'matern05': 'Matérn 0.5 with ARD',
            'rbf': 'Radial Basis Function (RBF) with ARD'
        }
        kernel_desc = kernel_descriptions.get(self.kernel, self.kernel)
        self.console.print(f"[white]• Kernel:[/white] Co-Kriging Kernel with {kernel_desc}")
        
        self.console.print(f"[white]• Input Features:[/white] {input_shape_low[1]}")
        self.console.print(f"[white]• Low-fidelity Samples:[/white] {input_shape_low[0]}")
        self.console.print(f"[white]• High-fidelity Samples:[/white] {input_shape_high[0]}")
        self.console.print(f"[white]• Total Samples:[/white] {input_shape_low[0] + input_shape_high[0]}")
        self.console.print(f"[white]• Max Iterations:[/white] {self.num_iterations}")
        self.console.print(f"[white]• Optimizer:[/white] Adam")
        self.console.print(f"[white]• Learning Rate:[/white] {self.learning_rate} with ReduceLROnPlateau")
        self.console.print(f"[white]• Early Stopping:[/white] Yes (patience={self.patience})")
        
        if hasattr(self, 'variable_names') and self.variable_names:
            self.console.print("\n[green]Features:[/green]")
            for i, name in enumerate(self.variable_names, 1):
                self.console.print(f"[white]• {i}. {name}[/white]")
        self.console.print("")

    def train(self, X_low, y_low, X_high, y_high, X_test=None, y_test=None, feature_names=None):
        """
        Train the Co-Kriging model with low and high fidelity data.
        
        Args:
            X_low: Low-fidelity inputs
            y_low: Low-fidelity targets
            X_high: High-fidelity inputs
            y_high: High-fidelity targets
            X_test: Test inputs for model evaluation (optional)
            y_test: Test targets for model evaluation (optional)
            feature_names: Optional list of feature names
            
        Returns:
            Tuple: Trained model, X scaler, and y scaler
        """
        if any(x is None for x in [X_low, y_low, X_high, y_high]):
            raise ValueError("Both low and high fidelity data must be provided")
        
        # Process inputs
        X_low, y_low = self._prepare_input_data(X_low, y_low)
        X_high, y_high = self._prepare_input_data(X_high, y_high)
        
        # Process test data if provided
        has_test_data = False
        if X_test is not None and y_test is not None:
            X_test, y_test = self._prepare_input_data(X_test, y_test)
            has_test_data = True
        
        # Set feature names
        if feature_names is not None:
            self.variable_names = feature_names
        elif isinstance(X_low, pd.DataFrame):
            self.variable_names = X_low.columns.tolist()
        else:
            self.variable_names = [f'X{i}' for i in range(X_low.shape[1])]
        
        # Print hardware and model info if enabled
        if self.show_hardware_info:
            self.print_device_info()
        if self.show_model_info:
            self.print_model_info(X_low.shape, X_high.shape)
            
        # Add fidelity indicators (0 for low, 1 for high)
        X_low_with_fidelity = np.hstack([X_low, np.zeros((X_low.shape[0], 1))])
        X_high_with_fidelity = np.hstack([X_high, np.ones((X_high.shape[0], 1))])
        
        # Combine datasets
        X = np.vstack([X_low_with_fidelity, X_high_with_fidelity])
        y = np.vstack([y_low, y_high])
        
        # Scale data - important to scale only the feature dimensions, not the fidelity indicator
        self.scaler_X = StandardScaler().fit(X[:, :-1])
        self.scaler_y = StandardScaler().fit(y)
        
        # Apply scaling
        X_train_scaled = np.hstack([
            self.scaler_X.transform(X[:, :-1]),
            X[:, -1:]  # Keep fidelity indicator as is
        ])
        y_train_scaled = self.scaler_y.transform(y)
        
        # Convert to tensors
        X_train_tensor = torch.tensor(X_train_scaled, dtype=torch.float32).to(self.device)
        y_train_tensor = torch.tensor(y_train_scaled.flatten(), dtype=torch.float32).to(self.device)
        
        # Initialize model components
        self.likelihood = gpytorch.likelihoods.GaussianLikelihood(
            noise_constraint=gpytorch.constraints.Positive(initial_value=torch.tensor(0.01))
        ).to(self.device)
        
        self.model = CoKrigingModel(
            X_train_tensor,
            y_train_tensor,
            self.likelihood,
            kernel=self.kernel
        ).to(self.device)
        
        # Training setup
        self.model.train()
        self.likelihood.train()
        
        optimizer = torch.optim.Adam([
            {'params': self.model.parameters(), 'lr': self.learning_rate}
        ])
        
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer,
            mode='min',
            factor=0.5,
            patience=self.patience,
            min_lr=1e-5
        )
        
        mll = gpytorch.mlls.ExactMarginalLogLikelihood(self.likelihood, self.model)
        
        # Train with or without progress bar
        if self.show_progress:
            self._train_with_progress(optimizer, scheduler, mll, X_train_tensor, y_train_tensor)
        else:
            self._train_without_progress(optimizer, scheduler, mll, X_train_tensor, y_train_tensor)
        
        # Save model
        self._save_model()

        # Calculate metrics
        if has_test_data:
            # Make predictions
            y_low_pred, _ = self.predict(X_low, fidelity='low')
            y_high_pred, _ = self.predict(X_high, fidelity='high')
            y_test_pred, _ = self.predict(X_test, fidelity='high')
            
            # Calculate metrics
            low_rmse = np.sqrt(np.mean((y_low - y_low_pred) ** 2))
            high_rmse = np.sqrt(np.mean((y_high - y_high_pred) ** 2))
            test_rmse = np.sqrt(np.mean((y_test - y_test_pred) ** 2))
            
            R2_low = 1 - np.sum((y_low - y_low_pred) ** 2) / np.sum((y_low - np.mean(y_low)) ** 2)
            R2_high = 1 - np.sum((y_high - y_high_pred) ** 2) / np.sum((y_high - np.mean(y_high)) ** 2)
            R2_test = 1 - np.sum((y_test - y_test_pred) ** 2) / np.sum((y_test - np.mean(y_test)) ** 2)
            
            # Store metrics
            self.metrics = {
                'low_rmse': float(low_rmse),
                'low_r2': float(R2_low),
                'train_rmse': float(high_rmse),
                'train_r2': float(R2_high),
                'test_rmse': float(test_rmse),
                'test_r2': float(R2_test)
            }
        else:
            # Only calculate training metrics if no test data
            y_low_pred, _ = self.predict(X_low, fidelity='low')
            y_high_pred, _ = self.predict(X_high, fidelity='high')
            
            low_rmse = np.sqrt(np.mean((y_low - y_low_pred) ** 2))
            high_rmse = np.sqrt(np.mean((y_high - y_high_pred) ** 2))
            
            R2_low = 1 - np.sum((y_low - y_low_pred) ** 2) / np.sum((y_low - np.mean(y_low)) ** 2)
            R2_high = 1 - np.sum((y_high - y_high_pred) ** 2) / np.sum((y_high - np.mean(y_high)) ** 2)
            
            self.metrics = {
                'low_rmse': float(low_rmse),
                'low_r2': float(R2_low),
                'train_rmse': float(high_rmse),
                'train_r2': float(R2_high)
            }
        
        # Print hyperparameters and metrics automatically if progress display is enabled
        if self.show_progress:
            self.print_hyperparameters()
            
            # Print performance results
            self.console.print("\n[green]Model Performance[/green]")
            self.console.print(f"[white]• Low-fidelity RMSE: {self.metrics['low_rmse']:.4f}[/white]")
            self.console.print(f"[white]• Low-fidelity R²: {self.metrics['low_r2']:.4f}[/white]")
            self.console.print(f"[white]• High-fidelity RMSE: {self.metrics['train_rmse']:.4f}[/white]")
            self.console.print(f"[white]• High-fidelity R²: {self.metrics['train_r2']:.4f}[/white]")
            
            if has_test_data:
                self.console.print(f"[white]• Test RMSE: {self.metrics['test_rmse']:.4f}[/white]")
                self.console.print(f"[white]• Test R²: {self.metrics['test_r2']:.4f}[/white]")
        
        return self.model, self.scaler_X, self.scaler_y
        
    def _prepare_input_data(self, X, y):
        """Prepare and standardize input data format."""
        # Handle DataFrame inputs
        if isinstance(X, pd.DataFrame):
            X = X.values
        if isinstance(y, pd.DataFrame) or isinstance(y, pd.Series):
            y = y.values
            
        # Ensure y is 2D
        if len(y.shape) == 1:
            y = y.reshape(-1, 1)
            
        return X, y

    def _train_with_progress(self, optimizer, scheduler, mll, X_train_tensor, y_train_tensor):
        """Training loop with rich progress bar."""
        best_loss = float('inf')
        patience_counter = 0
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            TextColumn("[cyan]{task.fields[loss]}"),
            TextColumn("[magenta]{task.fields[best_loss]}"),
            TextColumn("[yellow]{task.fields[lr]}"),
        ) as progress:
            task = progress.add_task(
                "[cyan]Training Co-Kriging Model",
                total=self.num_iterations,
                loss="Loss: N/A",
                best_loss="Best: N/A",
                lr=f"LR: {self.learning_rate}"
            )

            with gpytorch.settings.cholesky_jitter(1e-4):
                for i in range(self.num_iterations):
                    # Get current learning rate
                    current_lr = optimizer.param_groups[0]['lr']
                    
                    # Training step
                    optimizer.zero_grad()
                    
                    with gpytorch.settings.max_cholesky_size(2000):
                        output = self.model(X_train_tensor)
                        loss = -mll(output, y_train_tensor)
                    
                    loss.backward()
                    torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
                    optimizer.step()
                    current_loss = loss.item()
                    scheduler.step(current_loss)
                    
                    if current_loss < best_loss:
                        best_loss = current_loss
                        patience_counter = 0
                    else:
                        patience_counter += 1
                    
                    progress.update(
                        task,
                        advance=1,
                        loss=f"Loss: {current_loss:.4f}",
                        best_loss=f"Best: {best_loss:.4f}",
                        lr=f"LR: {current_lr:.6f}"
                    )
                    
                    if patience_counter >= self.patience:
                        progress.update(task, description="[yellow]Early stopping triggered[/yellow]")
                        break
                        
    def _train_without_progress(self, optimizer, scheduler, mll, X_train_tensor, y_train_tensor):
        """Training loop without progress bar for headless environments."""
        best_loss = float('inf')
        patience_counter = 0
        
        for i in range(self.num_iterations):
            optimizer.zero_grad()
            
            with gpytorch.settings.max_cholesky_size(2000), gpytorch.settings.cholesky_jitter(1e-4):
                output = self.model(X_train_tensor)
                loss = -mll(output, y_train_tensor)
            
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            optimizer.step()
            current_loss = loss.item()
            scheduler.step(current_loss)
            
            if current_loss < best_loss:
                best_loss = current_loss
                patience_counter = 0
            else:
                patience_counter += 1
                
            if patience_counter >= self.patience:
                print(f"Early stopping triggered after {i+1} iterations")
                break

    def _save_model(self):
        """Save the trained model and scalers to disk."""
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Save scalers
        joblib.dump(self.scaler_X, os.path.join(self.output_dir, 'scaler_X.pkl'))
        joblib.dump(self.scaler_y, os.path.join(self.output_dir, 'scaler_y.pkl'))
        
        # Move model to CPU and save
        model_cpu = self.model.cpu()
        likelihood_cpu = self.likelihood.cpu()
        
        state_dict = {
            'model': model_cpu.state_dict(),
            'likelihood': likelihood_cpu.state_dict(),
            'train_inputs': [x.cpu() for x in model_cpu.train_inputs],
            'train_targets': model_cpu.train_targets.cpu(),
            'input_size': model_cpu.train_inputs[0].shape[1],
            'variable_names': self.variable_names,
            'metrics': self.metrics,
            'kernel': self.kernel,
            'learning_rate': self.learning_rate,
            'patience': self.patience
        }
        
        torch.save(state_dict, os.path.join(self.output_dir, 'cokriging_model.pth'))
        
        # Move model back to original device
        self.model = self.model.to(self.device)
        self.likelihood = self.likelihood.to(self.device)
        
        if self.show_progress:
            self.console.print(f"[green]Model saved to {self.output_dir}[/green]")

    def predict(self, X, fidelity='high'):
        """
        Make predictions with the trained Co-Kriging model.
        
        Args:
            X: Input features for prediction
            fidelity: 'high' or 'low' to specify which fidelity level to predict
            
        Returns:
            Tuple: Mean predictions and standard deviations
        """
        if self.model is None:
            raise RuntimeError("Model not trained. Call train() first.")
        
        # Prepare input data
        if isinstance(X, pd.DataFrame):
            X = X.values
            
        # Scale input features
        X_scaled = self.scaler_X.transform(X)
        
        # Add fidelity indicator (0 for low, 1 for high)
        fidelity_indicator = 1.0 if fidelity.lower() == 'high' else 0.0
        X_with_fidelity = np.hstack([X_scaled, np.ones((X.shape[0], 1)) * fidelity_indicator])
        
        # Convert to tensor
        X_tensor = torch.tensor(X_with_fidelity, dtype=torch.float32).to(self.device)
        
        # Get predictions
        self.model.eval()
        self.likelihood.eval()
        
        with torch.no_grad(), gpytorch.settings.fast_pred_var():
            output = self.model(X_tensor)
            predictions = self.likelihood(output)
            
        # Extract mean and variance
        mean = predictions.mean.cpu().numpy().reshape(-1, 1)
        variance = predictions.variance.cpu().numpy().reshape(-1, 1)
        std = np.sqrt(variance)
        
        # Unscale predictions
        mean_unscaled = self.scaler_y.inverse_transform(mean)
        std_unscaled = std * self.scaler_y.scale_
        
        return mean_unscaled, std_unscaled

    def load_model(self, model_path=None):
        """
        Load a trained model from disk.
        
        Args:
            model_path: Path to the saved model file. If None, uses the default path.
            
        Returns:
            Loaded model
        """
        if model_path is None:
            model_path = os.path.join(self.output_dir, 'cokriging_model.pth')
            
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file {model_path} not found.")
            
        # Load scalers
        scaler_X_path = os.path.join(os.path.dirname(model_path), 'scaler_X.pkl')
        scaler_y_path = os.path.join(os.path.dirname(model_path), 'scaler_y.pkl')
        
        if os.path.exists(scaler_X_path) and os.path.exists(scaler_y_path):
            self.scaler_X = joblib.load(scaler_X_path)
            self.scaler_y = joblib.load(scaler_y_path)
        else:
            raise FileNotFoundError("Scaler files not found.")
        
        # Load model state
        state_dict = torch.load(model_path, map_location=self.device)
        
        # Extract model parameters
        train_inputs = state_dict['train_inputs']
        train_targets = state_dict['train_targets']
        
        # Get kernel type if available, otherwise use default
        kernel = state_dict.get('kernel', 'matern25')
        self.kernel = kernel
        
        # Get learning rate and patience if available
        if 'learning_rate' in state_dict:
            self.learning_rate = state_dict['learning_rate']
        if 'patience' in state_dict:
            self.patience = state_dict['patience']
        
        # Initialize model and likelihood
        self.likelihood = gpytorch.likelihoods.GaussianLikelihood().to(self.device)
        self.model = CoKrigingModel(
            train_inputs[0], 
            train_targets, 
            self.likelihood,
            kernel=kernel
        ).to(self.device)
        
        # Load state dictionaries
        self.model.load_state_dict(state_dict['model'])
        self.likelihood.load_state_dict(state_dict['likelihood'])
        
        # Load variable names if available
        if 'variable_names' in state_dict:
            self.variable_names = state_dict['variable_names']
        
        # Load metrics if available
        if 'metrics' in state_dict:
            self.metrics = state_dict['metrics']
        
        return self.model

    def print_hyperparameters(self):
        """Print the learned hyperparameters of the model."""
        if self.model is None:
            self.console.print("[red]Model not trained. No hyperparameters to display.[/red]")
            return
            
        self.console.print("\n[green]Model Hyperparameters[/green]")
        
        try:
            # Generic approach - print all scalar parameters from the model
            param_count = 0
            for name, param in self.model.named_parameters():
                if param.requires_grad:
                    if param.numel() == 1:
                        # Single scalar parameter
                        value = param.item()
                        self.console.print(f"[white]• {name}: {value:.6f}[/white]")
                        param_count += 1
                    elif 'lengthscale' in name:
                        # Lengthscales for each input dimension
                        values = param.detach().cpu().numpy()
                        if values.ndim == 1 or (values.ndim == 2 and values.shape[0] == 1):
                            # Flatten if it's a 2D array with a single row
                            if values.ndim == 2:
                                values = values.flatten()
                            
                            self.console.print("[white]Lengthscales:[/white]")
                            for i, val in enumerate(values):
                                # Get feature name if available
                                feat_name = self.variable_names[i] if i < len(self.variable_names) else f"Feature {i+1}"
                                self.console.print(f"[white]• {feat_name}: {val:.6f}[/white]")
                            param_count += 1
            
            # Always try to extract the noise parameter from the likelihood
            noise = self.likelihood.noise.cpu().detach().numpy().item()
            self.console.print(f"\n[white]Noise variance: {noise:.6f}[/white]")
            param_count += 1
            
            # Directly try to access common parameters in co-kriging models
            if hasattr(self.model.covar_module, 'rho'):
                rho = self.model.covar_module.rho.cpu().detach().numpy().item()
                self.console.print(f"[white]Fidelity correlation (rho): {rho:.4f}[/white]")
                param_count += 1
                
            if hasattr(self.model.covar_module, 'outputscale'):
                outputscale = self.model.covar_module.outputscale.cpu().detach().numpy().item()
                self.console.print(f"[white]Output scale: {outputscale:.4f}[/white]")
                param_count += 1
                
            # If no parameters were extracted, provide more specific guidance
            if param_count == 0:
                self.console.print("[yellow]No hyperparameters could be extracted.[/yellow]")
                self.console.print("[yellow]Try inspecting your model structure to identify parameter names:[/yellow]")
                self.console.print("[white]Available modules:[/white]")
                for name, module in self.model.named_modules():
                    self.console.print(f"[white]• {name}[/white]")
                
        except Exception as e:
            self.console.print(f"[yellow]Could not extract all hyperparameters: {e}[/yellow]")
            
            # Provide debugging information to help identify parameter structure
            self.console.print("[white]Model structure:[/white]")
            for name, module in self.model.named_modules():
                self.console.print(f"[white]• {name}[/white]")
        
        self.console.print("")