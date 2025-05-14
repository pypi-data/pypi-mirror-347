"""
Utility classes for Co-Kriging model handling and multi-fidelity modeling in PyEGRO.
"""

import os
import torch
import gpytorch
import numpy as np
import joblib
import warnings
from copy import deepcopy
from typing import Tuple, Optional
from gpytorch.utils.warnings import GPInputWarning, NumericalWarning
warnings.filterwarnings("ignore", category=GPInputWarning)
warnings.filterwarnings("ignore", category=NumericalWarning)

class CoKrigingKernel(gpytorch.kernels.Kernel):
    """
    Custom kernel for Co-Kriging that handles multi-fidelity data.
    
    This kernel combines separate kernels for the low-fidelity data and the 
    difference between high and low fidelity data, following the auto-regressive 
    structure of the Kennedy & O'Hagan model.
    """
    def __init__(self, base_kernel, num_dims: int, active_dims: Optional[Tuple[int, ...]] = None):
        super().__init__(active_dims=active_dims)
        
        # Kernel for low-fidelity data (Ψc)
        self.kernel_c = gpytorch.kernels.ScaleKernel(
            base_kernel
        )

        # Kernel for difference between fidelities (Ψd)
        self.kernel_d = gpytorch.kernels.ScaleKernel(
            deepcopy(base_kernel)  
        )
        
        # Scaling parameter ρ (rho)
        self.register_parameter(
            name="raw_rho",
            parameter=torch.nn.Parameter(torch.tensor(0.5))
        )
        self.register_constraint(
            "raw_rho",
            gpytorch.constraints.Positive() 
        )

    @property
    def rho(self):
        """Get the constrained rho value."""
        return self.raw_rho_constraint.transform(self.raw_rho)
        
    def forward(self, x1: torch.Tensor, x2: torch.Tensor, diag: bool = False, **params):
        """
        Compute the covariance matrix between inputs x1 and x2.
        
        The covariance is computed based on the Kennedy & O'Hagan autoregressive 
        multi-fidelity formulation.
        """
        if x1.size(-1) != x2.size(-1):
            raise RuntimeError("Inputs must have the same number of dimensions")
            
        # Split inputs into locations and fidelity indicators
        x1_main, f1 = x1[..., :-1], x1[..., -1:]
        x2_main, f2 = x2[..., :-1], x2[..., -1:]
        
        # Identify fidelity of points
        is_high1 = (f1 > 0.5).float()
        is_high2 = (f2 > 0.5).float()
        
        # Compute base covariances
        if diag:
            K_c = self.kernel_c(x1_main, x2_main, diag=True)
            K_d = self.kernel_d(x1_main, x2_main, diag=True)
            
            # Calculate correlation based on fidelities
            same_fidelity = (is_high1 * is_high2) + ((1 - is_high1) * (1 - is_high2))
            diff_fidelity = 1 - same_fidelity
            
            covar = K_c * (
                same_fidelity.squeeze(-1) +
                diff_fidelity.squeeze(-1) * self.rho +
                (is_high1 * is_high2).squeeze(-1) * (self.rho ** 2)
            )
            
            covar = covar + K_d * (is_high1 * is_high2).squeeze(-1)
            return covar
        else:
            K_c = self.kernel_c(x1_main, x2_main).evaluate()
            K_d = self.kernel_d(x1_main, x2_main).evaluate()
            
            # Calculate correlation based on fidelities - matrix form
            same_fidelity = torch.matmul(is_high1, is_high2.transpose(-1, -2)) + \
                           torch.matmul(1 - is_high1, (1 - is_high2).transpose(-1, -2))
            diff_fidelity = 1 - same_fidelity
            
            high_fidelity_corr = torch.matmul(is_high1, is_high2.transpose(-1, -2))
            
            covar = K_c * (
                same_fidelity +
                diff_fidelity * self.rho +
                high_fidelity_corr * (self.rho ** 2)
            ) + K_d * high_fidelity_corr
            
            # Add small jitter to diagonal for numerical stability
            if covar.shape[-1] == covar.shape[-2]:
                covar = covar + torch.eye(covar.shape[-1], device=covar.device) * 1e-6
        
        return covar


class CoKrigingModel(gpytorch.models.ExactGP):
    """
    Gaussian Process model for Co-Kriging/multi-fidelity modeling.
    
    This model implements the Kennedy & O'Hagan (2000) approach to multi-fidelity
    modeling, allowing integration of low-fidelity (cheap) and high-fidelity
    (expensive) data.
    """
    def __init__(self, train_x: torch.Tensor, train_y: torch.Tensor, 
                 likelihood: gpytorch.likelihoods.Likelihood, kernel: str = 'matern15'):
        """
        Initialize Co-Kriging model with configurable kernel.
        
        Args:
            train_x: Training input data (with fidelity indicator as last column)
            train_y: Training target data
            likelihood: GP likelihood function
            kernel: Kernel type ('matern25', 'matern15', 'matern05', 'rbf')
        """
        super().__init__(train_x, train_y, likelihood)
        
        # Mean function
        self.mean_module = gpytorch.means.ConstantMean()
        self.mean_module.constant.data = train_y.mean()
        
        # Base kernel selection based on user input
        if kernel == 'matern25':
            base_kernel = gpytorch.kernels.MaternKernel(
                nu=2.5, 
                ard_num_dims=train_x.size(-1) - 1  # Exclude fidelity dimension
            )
        elif kernel == 'matern15':
            base_kernel = gpytorch.kernels.MaternKernel(
                nu=1.5, 
                ard_num_dims=train_x.size(-1) - 1  # Exclude fidelity dimension
            )
        elif kernel == 'matern05':
            base_kernel = gpytorch.kernels.MaternKernel(
                nu=0.5, 
                ard_num_dims=train_x.size(-1) - 1  # Exclude fidelity dimension
            )
        elif kernel == 'rbf':
            base_kernel = gpytorch.kernels.RBFKernel(
                ard_num_dims=train_x.size(-1) - 1  # Exclude fidelity dimension
            )
        else:
            # Default to Matern 1.5 if unknown kernel is specified
            base_kernel = gpytorch.kernels.MaternKernel(
                nu=1.5, 
                ard_num_dims=train_x.size(-1) - 1  # Exclude fidelity dimension
            )
        
        # Store kernel type for reference
        self.kernel_type = kernel
        
        # Co-Kriging kernel combining low and high fidelity data
        self.covar_module = CoKrigingKernel(
            base_kernel, 
            num_dims=train_x.size(-1)
        )

    def forward(self, x: torch.Tensor) -> gpytorch.distributions.MultivariateNormal:
        """
        Forward pass of the model.
        """
        mean = self.mean_module(x)
        covar = self.covar_module(x)
        return gpytorch.distributions.MultivariateNormal(mean, covar)


class DeviceAgnosticCoKriging:
    """
    Device-agnostic handler for Co-Kriging models.
    
    Provides functionality to load and utilize Co-Kriging models
    on both CPU and GPU devices.
    """
    def __init__(self, prefer_gpu: bool = False):
        self.prefer_gpu = prefer_gpu
        self.device = self._get_device()
        self.model = None
        self.scaler_X = None
        self.scaler_y = None
        self.kernel = None
        
        self._print_device_info()
    
    def _get_device(self) -> torch.device:
        """Determine the computational device to use."""
        if self.prefer_gpu and torch.cuda.is_available():
            return torch.device("cuda")
        return torch.device("cpu")
    
    def _print_device_info(self):
        """Print information about the computing environment."""
        if self.device.type == "cuda":
            device_name = torch.cuda.get_device_name(0)
            memory_gb = torch.cuda.get_device_properties(0).total_memory / 1024**3
            print(f"\nUsing GPU: {device_name}")
            print(f"GPU Memory: {memory_gb:.1f} GB")
            print(f"CUDA Version: {torch.version.cuda}")
        else:
            import psutil
            try:
                import cpuinfo
                cpu_info = cpuinfo.get_cpu_info()
                device_name = cpu_info.get('brand_raw', 'Unknown CPU')
            except ImportError:
                import platform
                device_name = platform.processor() or "Unknown CPU"
            
            memory_gb = psutil.virtual_memory().total / 1024**3
            print(f"\nUsing CPU: {device_name}")
            print(f"System Memory: {memory_gb:.1f} GB")
        
        print(f"PyTorch Version: {torch.__version__}")
        print(f"GPyTorch Version: {gpytorch.__version__}\n")

    def load_model(self, model_dir: str = 'RESULT_MODEL_COKRIGING'):
        """
        Load a trained Co-Kriging model from disk.
        """
        try:
            # Load scalers
            self.scaler_X = joblib.load(os.path.join(model_dir, 'scaler_X.pkl'))
            self.scaler_y = joblib.load(os.path.join(model_dir, 'scaler_y.pkl'))
            
            # Load state dict
            state_dict = torch.load(
                os.path.join(model_dir, 'cokriging_model.pth'),
                map_location=self.device
            )
            
            # Get kernel type if available
            kernel = state_dict.get('kernel', 'matern15')
            self.kernel = kernel
            
            # Initialize model components
            likelihood = gpytorch.likelihoods.GaussianLikelihood()
            
            # Create new model instance
            train_x = state_dict['train_inputs'][0].to(self.device)
            train_y = state_dict['train_targets'].to(self.device)
            self.model = CoKrigingModel(train_x, train_y, likelihood, kernel=kernel)
            
            # Load state dicts
            self.model.load_state_dict(state_dict['model'])
            self.model.likelihood.load_state_dict(state_dict['likelihood'])
            
            # Move to device
            self.model = self.model.to(self.device)
            self.model.likelihood = self.model.likelihood.to(self.device)
            
            # Set evaluation mode
            self.model.eval()
            self.model.likelihood.eval()
            
            # Print kernel info
            kernel_descriptions = {
                'matern25': 'Matérn 2.5',
                'matern15': 'Matérn 1.5',
                'matern05': 'Matérn 0.5',
                'rbf': 'Radial Basis Function (RBF)'
            }
            kernel_desc = kernel_descriptions.get(kernel, kernel)
            
            print(f"Co-Kriging model loaded successfully on {self.device}")
            print(f"Kernel: {kernel_desc}")
            return True
            
        except Exception as e:
            print(f"Error loading Co-Kriging model: {str(e)}")
            return False

    def predict(self, X: np.ndarray, fidelity='high', batch_size: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """
        Make predictions with the loaded Co-Kriging model.
        """
        if self.model is None:
            raise ValueError("Model not loaded. Call load_model first.")
            
        n_samples = X.shape[0]
        mean_predictions = np.zeros((n_samples, 1))
        std_predictions = np.zeros((n_samples, 1))
        
        # Add fidelity indicator
        if fidelity == 'high':
            X_with_fidelity = np.hstack([X, np.ones((X.shape[0], 1))])
        else:
            X_with_fidelity = np.hstack([X, np.zeros((X.shape[0], 1))])
        
        # Scale features (except fidelity indicator)
        X_scaled = np.hstack([
            self.scaler_X.transform(X_with_fidelity[:, :-1]),
            X_with_fidelity[:, -1:]
        ])
        
        self.model.eval()
        self.model.likelihood.eval()
        
        # Process in batches
        batch_iterator = range(0, n_samples, batch_size)
        
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=NumericalWarning)
            with gpytorch.settings.fast_pred_var(), \
                gpytorch.settings.cholesky_jitter(1e-3), \
                gpytorch.settings.max_cholesky_size(2000):
                
                for i in batch_iterator:
                    end_idx = min(i + batch_size, n_samples)
                    X_batch = torch.tensor(X_scaled[i:end_idx], dtype=torch.float32).to(self.device)
                    
                    with torch.no_grad():
                        try:
                            output = self.model(X_batch)
                            pred_dist = self.model.likelihood(output)
                            
                            # Get mean and variance
                            pred_mean = pred_dist.mean.cpu().numpy().reshape(-1, 1)
                            pred_var = pred_dist.variance.cpu().numpy().reshape(-1, 1)
                            
                            # Transform back to original scale
                            mean_predictions[i:end_idx] = self.scaler_y.inverse_transform(pred_mean)
                            std_predictions[i:end_idx] = np.sqrt(pred_var) * self.scaler_y.scale_
                            
                        except RuntimeError as e:
                            if "not positive definite" in str(e):
                                # Try with larger jitter
                                with gpytorch.settings.cholesky_jitter(1e-1):
                                    output = self.model(X_batch)
                                    pred_dist = self.model.likelihood(output)
                                    
                                    # Get mean and variance
                                    pred_mean = pred_dist.mean.cpu().numpy().reshape(-1, 1)
                                    pred_var = pred_dist.variance.cpu().numpy().reshape(-1, 1)
                                    
                                    # Transform back to original scale
                                    mean_predictions[i:end_idx] = self.scaler_y.inverse_transform(pred_mean)
                                    std_predictions[i:end_idx] = np.sqrt(pred_var) * self.scaler_y.scale_
                            else:
                                raise
        
        return mean_predictions, std_predictions