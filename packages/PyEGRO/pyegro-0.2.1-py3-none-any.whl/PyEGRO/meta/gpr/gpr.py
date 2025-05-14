


"""
Gaussian Process Regression (GPR) modeling for PyEGRO with enhanced testing and visualization.

This module provides tools for training and managing GPR models

"""

import os
import torch
import gpytorch
import joblib
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from typing import Dict, List, Tuple, Optional, Union

# Rich progress bar imports
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn
from rich.progress import TimeRemainingColumn, TimeElapsedColumn, SpinnerColumn
from rich.console import Console
from rich.panel import Panel
import platform

# Import the GPRegressionModel from gpr_utils
from .gpr_utils import GPRegressionModel

# Suppress warnings
import warnings
from gpytorch.utils.warnings import GPInputWarning, NumericalWarning
warnings.filterwarnings("ignore", category=GPInputWarning)
warnings.filterwarnings("ignore", category=NumericalWarning)

class MetaTraining:
    def __init__(self,
                 test_size: float = 0.3,
                 num_iterations: int = 1000,
                 prefer_gpu: bool = True,
                 show_progress: bool = True,
                 show_hardware_info: bool = True,
                 show_model_info: bool = True,
                 output_dir: str = 'RESULT_MODEL_GPR',
                 data_dir: str = 'DATA_PREPARATION',
                 data_info_file: str = None,
                 data_training_file: str = None,
                 kernel: str = 'matern15',
                 learning_rate: float = 0.01,
                 patience: int = 50):
        """
        Initialize MetaTraining with configuration.
        
        Args:
            test_size: Fraction of data to use for testing if no test data is provided (default: 0.3)
            num_iterations: Number of training iterations (default: 1000)
            prefer_gpu: Whether to use GPU if available (default: True)
            show_progress: Whether to show detailed progress (default: True)
            show_hardware_info: Whether to show system hardware info (default: True)
            show_model_info: Whether to show model architecture info (default: True)
            output_dir: Directory for saving results (default: 'RESULT_MODEL_GPR')
            data_dir: Directory containing input data (default: 'DATA_PREPARATION')
            data_info_file: Path to data info JSON file (default: None)
            data_training_file: Path to training data CSV file (default: None)
            kernel: Kernel to use for GPR model (default: 'matern15', options: 'matern25', 'matern15', 'matern05', 'rbf')
            learning_rate: Learning rate for optimizer (default: 0.01)
            patience: Number of iterations to wait for improvement before early stopping (default: 50)
        """
        self.test_size = test_size
        self.num_iterations = num_iterations
        self.show_progress = show_progress
        self.show_hardware_info = show_hardware_info
        self.show_model_info = show_model_info
        self.output_dir = output_dir
        self.data_dir = data_dir
        self.data_info_file = data_info_file
        self.data_training_file = data_training_file
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

    def print_model_info(self, input_shape, test_shape=None):
        """Print information about the model architecture and training setup."""
        self.console.print("\n[green]Model Configuration[/green]")
        self.console.print(f"[white]• Model Type:[/white] Gaussian Process Regression")
        
        # Map kernel names to readable descriptions
        kernel_descriptions = {
            'matern25': 'Matérn 2.5 with ARD',
            'matern15': 'Matérn 1.5 with ARD',
            'matern05': 'Matérn 0.5 with ARD',
            'rbf': 'Radial Basis Function (RBF) with ARD'
        }
        kernel_desc = kernel_descriptions.get(self.kernel, self.kernel)
        self.console.print(f"[white]• Kernel:[/white] {kernel_desc}")
        
        self.console.print(f"[white]• Input Features:[/white] {input_shape[1]}")
        self.console.print(f"[white]• Training Samples:[/white] {input_shape[0]}")
        if test_shape is not None:
            self.console.print(f"[white]• Test Samples:[/white] {test_shape[0]}")
        else:
            self.console.print(f"[white]• Test Size:[/white] {self.test_size * 100:.0f}%")
        self.console.print(f"[white]• Max Iterations:[/white] {self.num_iterations}")
        self.console.print(f"[white]• Optimizer:[/white] Adam")
        self.console.print(f"[white]• Learning Rate:[/white] {self.learning_rate} with ReduceLROnPlateau")
        self.console.print(f"[white]• Early Stopping:[/white] Yes (patience={self.patience})")
        
        if hasattr(self, 'variable_names') and self.variable_names:
            self.console.print("\n[green]Features:[/green]")
            for i, name in enumerate(self.variable_names, 1):
                self.console.print(f"[white]• {i}. {name}[/white]")
        self.console.print("")

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

    def train(self, X=None, y=None, X_test=None, y_test=None, feature_names=None, custom_data=False):
        """
        Train the GPR model with more flexible data options.
        
        Args:
            X: Training features or path to training data CSV
            y: Training targets (only needed if custom_data=True)
            X_test: Optional test features
            y_test: Optional test targets
            feature_names: Optional list of feature names
            custom_data: Whether using custom data instead of loading from files
            
        Returns:
            Tuple: Trained model, X scaler, and y scaler
        """
        # MODIFIED: If X is provided along with y_test, assume custom data mode
        if X is not None and y is not None:
            custom_data = True
            
        if not custom_data:
            # Load data from files
            if X is None and (self.data_info_file is not None and self.data_training_file is not None):
                data_info_path = self.data_info_file
                training_data_path = self.data_training_file
            else:
                # Determine file paths
                if isinstance(X, str):
                    self.data_training_file = X
                
                data_info_path = (self.data_info_file if self.data_info_file 
                                else os.path.join(self.data_dir, 'data_info.json'))
                training_data_path = (self.data_training_file if self.data_training_file 
                                    else os.path.join(self.data_dir, 'training_data.csv'))
            
            # MODIFIED: Try different file names if the default ones don't exist
            if not os.path.exists(data_info_path):
                alt_data_info_path = os.path.join(self.data_dir, 'data_info.json')
                if os.path.exists(alt_data_info_path):
                    data_info_path = alt_data_info_path
                    
            if not os.path.exists(training_data_path):
                # Try alternative file names
                alt_training_paths = [
                    os.path.join(self.data_dir, 'training.csv'),
                    os.path.join(self.data_dir, 'train.csv'),
                    os.path.join(self.data_dir, 'train_data.csv')
                ]
                
                for alt_path in alt_training_paths:
                    if os.path.exists(alt_path):
                        training_data_path = alt_path
                        break
            
            # Check for file existence
            if not os.path.exists(data_info_path) or not os.path.exists(training_data_path):
                raise FileNotFoundError(
                    f"Required files not found:\n"
                    f"Data info file: {data_info_path}\n"
                    f"Training data file: {training_data_path}"
                )
            
            # Load data info
            with open(data_info_path, 'r') as f:
                data_info = json.load(f)
            
            variables = data_info['variables']
            self.variable_names = [var['name'] for var in variables]
            
            # Load training data
            data = pd.read_csv(training_data_path)
            X = data[self.variable_names].values
            y = data[data_info.get('target_column', 'y')].values.reshape(-1, 1)
            
            # Check for testing data file
            testing_data_path = os.path.join(self.data_dir, 'testing_data.csv')
            # MODIFIED: Try alternative testing file names
            if not os.path.exists(testing_data_path):
                alt_testing_paths = [
                    os.path.join(self.data_dir, 'testing.csv'),
                    os.path.join(self.data_dir, 'test.csv'),
                    os.path.join(self.data_dir, 'test_data.csv')
                ]
                
                for alt_path in alt_testing_paths:
                    if os.path.exists(alt_path):
                        testing_data_path = alt_path
                        break
                        
            if os.path.exists(testing_data_path) and X_test is None and y_test is None:
                self.console.print(f"[cyan]Testing data file found at {testing_data_path}. Using it instead of splitting.[/cyan]")
                test_data = pd.read_csv(testing_data_path)
                X_test = test_data[self.variable_names].values
                y_test = test_data[data_info.get('target_column', 'y')].values.reshape(-1, 1)
        else:
            # Using user-provided data
            if y is None:
                raise ValueError("Target values 'y' must be provided when custom_data=True")
            
            # Set variable names if provided or derive from DataFrame
            if feature_names is not None:
                self.variable_names = feature_names
            elif isinstance(X, pd.DataFrame):
                self.variable_names = X.columns.tolist()
                X = X.values
            else:
                self.variable_names = [f'X{i}' for i in range(X.shape[1])]
            
            # Process inputs to numpy arrays
            X, y = self._prepare_input_data(X, y)
            if X_test is not None and y_test is not None:
                X_test, y_test = self._prepare_input_data(X_test, y_test)

        # Split data if test data not provided
        if X_test is None or y_test is None:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.test_size, random_state=42)
        else:
            X_train, y_train = X, y
        
        # Print hardware and model info if enabled
        if self.show_hardware_info:
            self.print_device_info()
        if self.show_model_info:
            self.print_model_info(X_train.shape, X_test.shape)
        
        # Scale data
        self.scaler_X = StandardScaler().fit(X_train)
        self.scaler_y = StandardScaler().fit(y_train)
        
        X_train_scaled = self.scaler_X.transform(X_train)
        y_train_scaled = self.scaler_y.transform(y_train)
        X_test_scaled = self.scaler_X.transform(X_test)
        y_test_scaled = self.scaler_y.transform(y_test)
        
        # Convert to tensors
        X_train_tensor = torch.tensor(X_train_scaled, dtype=torch.float32).to(self.device)
        y_train_tensor = torch.tensor(y_train_scaled.flatten(), dtype=torch.float32).to(self.device)
        X_test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32).to(self.device)
        y_test_tensor = torch.tensor(y_test_scaled.flatten(), dtype=torch.float32).to(self.device)
        
        # Initialize model components
        self.likelihood = gpytorch.likelihoods.GaussianLikelihood(
            noise_constraint=gpytorch.constraints.Positive(initial_value=torch.tensor(0.01))
        ).to(self.device)
        
        self.model = GPRegressionModel(
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
        y_train_pred, _ = self.predict(X_train)
        y_test_pred, _ = self.predict(X_test)
        
        train_rmse = np.sqrt(np.mean((y_train - y_train_pred) ** 2))
        test_rmse = np.sqrt(np.mean((y_test - y_test_pred) ** 2))
        
        R2_train = 1 - np.sum((y_train - y_train_pred) ** 2) / np.sum((y_train - np.mean(y_train)) ** 2)
        R2_test = 1 - np.sum((y_test - y_test_pred) ** 2) / np.sum((y_test - np.mean(y_test)) ** 2)
        
        # Store metrics
        self.metrics = {
            'train_rmse': float(train_rmse),
            'train_r2': float(R2_train),
            'test_rmse': float(test_rmse),
            'test_r2': float(R2_test)
        }
        
        # Print hyperparameters and metrics automatically if progress display is enabled
        if self.show_progress:
            self.print_hyperparameters()
            
            # Print performance results
            self.console.print("\n[green]Model Performance[/green]")
            self.console.print(f"[white]• Training RMSE: {self.metrics['train_rmse']:.4f}[/white]")
            self.console.print(f"[white]• Training R²: {self.metrics['train_r2']:.4f}[/white]")
            self.console.print(f"[white]• Test RMSE: {self.metrics['test_rmse']:.4f}[/white]")
            self.console.print(f"[white]• Test R²: {self.metrics['test_r2']:.4f}[/white]")
        
        return self.model, self.scaler_X, self.scaler_y

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
                "[cyan]Training GPR Model",
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
        
        torch.save(state_dict, os.path.join(self.output_dir, 'gpr_model.pth'))
        
        # Move model back to original device
        self.model = self.model.to(self.device)
        self.likelihood = self.likelihood.to(self.device)
        
        if self.show_progress:
            self.console.print(f"[green]Model saved to {self.output_dir}[/green]")

    def predict(self, X):
        """
        Make predictions using the trained model.
        
        Args:
            X: Input features (numpy array or DataFrame)
            
        Returns:
            Tuple of predictions and their standard deviations
        """
        if self.model is None:
            raise RuntimeError("Model not trained. Call train() first.")
            
        if isinstance(X, pd.DataFrame):
            X = X.values
            
        self.model.eval()
        self.likelihood.eval()
        
        with torch.no_grad(), gpytorch.settings.fast_pred_var():
            X_scaled = self.scaler_X.transform(X)
            X_tensor = torch.tensor(X_scaled, dtype=torch.float32).to(self.device)
            predictions = self.likelihood(self.model(X_tensor))
            
            mean = self.scaler_y.inverse_transform(
                predictions.mean.cpu().numpy().reshape(-1, 1)
            )
            std = predictions.variance.sqrt().cpu().numpy().reshape(-1, 1) * self.scaler_y.scale_
            
        return mean, std

    def load_model(self, model_path=None):
        """
        Load a trained model from disk.
        
        Args:
            model_path: Path to the saved model file. If None, uses the default path.
            
        Returns:
            Loaded model
        """
        if model_path is None:
            model_path = os.path.join(self.output_dir, 'gpr_model.pth')
            
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
        kernel = state_dict.get('kernel', 'matern15')
        self.kernel = kernel
        
        # Get learning rate and patience if available
        if 'learning_rate' in state_dict:
            self.learning_rate = state_dict['learning_rate']
        if 'patience' in state_dict:
            self.patience = state_dict['patience']
        
        # Initialize model and likelihood
        self.likelihood = gpytorch.likelihoods.GaussianLikelihood().to(self.device)
        self.model = GPRegressionModel(
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
            
            # Directly try to access common parameters in GP models
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