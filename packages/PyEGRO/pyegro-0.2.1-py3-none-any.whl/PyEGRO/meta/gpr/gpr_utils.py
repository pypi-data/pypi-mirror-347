"""
Utility classes for GPR model handling and device management in PyEGRO.
"""

import os
from typing import Tuple
import torch
import gpytorch
import numpy as np
import joblib
import warnings
from gpytorch.utils.warnings import GPInputWarning
from linear_operator.utils.warnings import NumericalWarning
warnings.filterwarnings("ignore", category=GPInputWarning)

class GPRegressionModel(gpytorch.models.ExactGP):
    """Gaussian Process Regression Model with configurable kernel."""
    
    def __init__(self, train_x: torch.Tensor, train_y: torch.Tensor, 
                 likelihood: gpytorch.likelihoods.Likelihood, kernel: str = 'matern15'):
        """
        Initialize GP regression model with configurable kernel.
        
        Args:
            train_x: Training input data
            train_y: Training target data
            likelihood: GP likelihood function
            kernel: Kernel type ('matern25', 'matern15', 'matern05', 'rbf', 'linear')
        """
        super().__init__(train_x, train_y, likelihood)
        self.mean_module = gpytorch.means.ConstantMean()
        
        # Select kernel based on user input
        if kernel == 'matern25':
            base_kernel = gpytorch.kernels.MaternKernel(nu=2.5, ard_num_dims=train_x.size(-1))
        elif kernel == 'matern15':
            base_kernel = gpytorch.kernels.MaternKernel(nu=1.5, ard_num_dims=train_x.size(-1))
        elif kernel == 'matern05':
            base_kernel = gpytorch.kernels.MaternKernel(nu=0.5, ard_num_dims=train_x.size(-1))
        elif kernel == 'rbf':
            base_kernel = gpytorch.kernels.RBFKernel(ard_num_dims=train_x.size(-1))
        else:
            # Default to Matern 1.5 if unknown kernel is specified
            base_kernel = gpytorch.kernels.MaternKernel(nu=1.5, ard_num_dims=train_x.size(-1))
        
        self.covar_module = gpytorch.kernels.ScaleKernel(base_kernel)

        # Initial Hyperparameters - keep standard settings
        if hasattr(self.covar_module.base_kernel, 'lengthscale'):
            self.covar_module.base_kernel.lengthscale = 1.0  
        self.covar_module.outputscale = 1.0  
        self.likelihood.noise_covar.noise = 1e-4  
        
        # Store the kernel type for reference
        self.kernel_type = kernel

    def forward(self, x: torch.Tensor) -> gpytorch.distributions.MultivariateNormal:
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        return gpytorch.distributions.MultivariateNormal(mean_x, covar_x)


class DeviceAgnosticGPR:
    """Device-agnostic handler for GPR models."""
    
    def __init__(self, prefer_gpu: bool = False):
        self.prefer_gpu = prefer_gpu
        self.device = self._get_device()
        self.model = None
        self.scaler_X = None
        self.scaler_y = None
        self.kernel = None
        
        self._print_device_info()
    
    def _get_device(self) -> torch.device:
        if self.prefer_gpu and torch.cuda.is_available():
            return torch.device("cuda")
        return torch.device("cpu")
    
    def _print_device_info(self):
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
                device_name = "Unknown CPU"
            
            memory_gb = psutil.virtual_memory().total / 1024**3
            print(f"\nUsing CPU: {device_name}")
            print(f"System Memory: {memory_gb:.1f} GB")
        
        print(f"PyTorch Version: {torch.__version__}")
        print(f"GPyTorch Version: {gpytorch.__version__}\n")

    def load_model(self, model_dir: str = 'RESULT_MODEL_GPR'):
        """Load model using state dict approach"""
        try:
            # Load scalers
            self.scaler_X = joblib.load(os.path.join(model_dir, 'scaler_X.pkl'))
            self.scaler_y = joblib.load(os.path.join(model_dir, 'scaler_y.pkl'))
            
            # Load state dict
            state_dict = torch.load(
                os.path.join(model_dir, 'gpr_model.pth'),
                map_location=self.device
            )
            
            # Get kernel type if available
            kernel = state_dict.get('kernel', 'matern15')
            self.kernel = kernel
            
            # Initialize model components
            likelihood = gpytorch.likelihoods.GaussianLikelihood()
            
            # Create new model instance with the right kernel
            train_x = state_dict['train_inputs'][0].to(self.device)
            train_y = state_dict['train_targets'].to(self.device)
            self.model = GPRegressionModel(train_x, train_y, likelihood, kernel=kernel)
            
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
            print(f"Model loaded successfully on {self.device}")
            print(f"Kernel: {kernel_desc}")
            return True
            
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            return False

    def predict(self, X: np.ndarray, batch_size: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """
        Make predictions with the loaded GPR model.
        
        Args:
            X: Input features (n_samples, n_features)
            batch_size: Batch size for processing large datasets
            
        Returns:
            Tuple of (mean_predictions, std_predictions) as numpy arrays
        """
        if self.model is None:
            raise ValueError("Model not loaded. Call load_model first.")
            
        n_samples = X.shape[0]
        mean_predictions = np.zeros((n_samples, 1))
        std_predictions = np.zeros((n_samples, 1))
        X_scaled = self.scaler_X.transform(X)
        
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