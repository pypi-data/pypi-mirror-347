"""
Co-Kriging model implementation for EGO.

This module provides the Co-Kriging model implementation used in the EGO process
for multi-fidelity optimization.
"""

import torch
import gpytorch
from typing import Dict, Union, List, Tuple, Optional
import warnings
from gpytorch.utils.warnings import GPInputWarning, NumericalWarning
from copy import deepcopy
warnings.filterwarnings("ignore", category=GPInputWarning)
warnings.filterwarnings("ignore", category=NumericalWarning)


class CoKrigingKernel(gpytorch.kernels.Kernel):
    """Co-Kriging kernel for multi-fidelity Gaussian process modeling.
    
    This kernel combines two kernel components:
    - kernel_c: Kernel for cheap code (Ψc)
    - kernel_d: Kernel for the difference between fidelities (Ψd)
    
    It also includes a scaling parameter ρ that controls the correlation
    between fidelity levels.
    """
    
    def __init__(self, base_kernel, num_dims: int, active_dims: Optional[Tuple[int, ...]] = None):
        """Initialize Co-Kriging kernel.
        
        Args:
            base_kernel: Base kernel to use for both kernel_c and kernel_d
            num_dims: Number of input dimensions
            active_dims: Dimensions to apply kernel to (optional)
        """
        super().__init__(active_dims=active_dims)
        
        # Kernel for cheap code (Ψc)
        self.kernel_c = gpytorch.kernels.ScaleKernel(
            base_kernel
        )

        # Kernel for difference (Ψd)
        self.kernel_d = gpytorch.kernels.ScaleKernel(
            deepcopy(base_kernel)  
        )
        
        # Scaling parameter ρ
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
        """Get transformed rho parameter."""
        return self.raw_rho_constraint.transform(self.raw_rho)
        
    def forward(self, x1: torch.Tensor, x2: torch.Tensor, diag: bool = False, **params):
        """Forward pass to compute kernel matrix.
        
        Args:
            x1: First input tensor
            x2: Second input tensor
            diag: Whether to return only diagonal elements
            
        Returns:
            Kernel matrix
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
            # Implement full covariance matrix
            same_fidelity = torch.matmul(is_high1, is_high2.transpose(-1, -2)) + \
                           torch.matmul(1 - is_high1, (1 - is_high2).transpose(-1, -2))
            diff_fidelity = 1 - same_fidelity
            
            high_fidelity_corr = torch.matmul(is_high1, is_high2.transpose(-1, -2))
            
            covar = K_c * (
                same_fidelity +
                diff_fidelity * self.rho +
                high_fidelity_corr * (self.rho ** 2)
            ) + K_d * high_fidelity_corr
            
            if covar.shape[-1] == covar.shape[-2]:
                covar = covar + torch.eye(covar.shape[-1], device=covar.device) * 1e-6
        
        return covar


class CoKrigingModel(gpytorch.models.ExactGP):
    """Co-Kriging Gaussian Process Model for multi-fidelity optimization.
    
    This model uses a specialized Co-Kriging kernel that models the relationship
    between low and high fidelity data.
    
    Attributes:
        mean_module: Mean function for GP
        covar_module: Co-Kriging covariance function
        kernel_type: Type of base kernel used
    """
    
    def __init__(self, train_x: torch.Tensor, train_y: torch.Tensor, 
                 likelihood: gpytorch.likelihoods.Likelihood, kernel: str = 'matern15'):
        """Initialize Co-Kriging GP model.
        
        Args:
            train_x: Training input data with fidelity indicator in last column
            train_y: Training target data
            likelihood: GPyTorch likelihood
            kernel: Kernel type ('matern25', 'matern15', 'matern05', 'rbf')
        """
        super().__init__(train_x, train_y, likelihood)
        
        # Store kernel type
        self.kernel_type = kernel
        
        # Define mean module
        self.mean_module = gpytorch.means.ConstantMean()
        self.mean_module.constant.data = train_y.mean()
        
        # Create base kernel based on specified type
        if kernel == 'matern25':
            base_kernel = gpytorch.kernels.MaternKernel(
                nu=2.5, 
                ard_num_dims=train_x.size(-1) - 1
            )
        elif kernel == 'matern15':
            base_kernel = gpytorch.kernels.MaternKernel(
                nu=1.5, 
                ard_num_dims=train_x.size(-1) - 1
            )
        elif kernel == 'matern05':
            base_kernel = gpytorch.kernels.MaternKernel(
                nu=0.5, 
                ard_num_dims=train_x.size(-1) - 1
            )
        elif kernel == 'rbf':
            base_kernel = gpytorch.kernels.RBFKernel(
                ard_num_dims=train_x.size(-1) - 1
            )
        else:
            # Default to Matérn 1.5 if unknown kernel type
            base_kernel = gpytorch.kernels.MaternKernel(
                nu=1.5, 
                ard_num_dims=train_x.size(-1) - 1
            )
                
        # Create Co-Kriging kernel
        self.covar_module = CoKrigingKernel(
            base_kernel, 
            num_dims=train_x.size(-1)
        )
        
        # Set initial hyperparameters
        self.initialize_hyperparameters()

    def initialize_hyperparameters(self):
        """Set initial values for model hyperparameters."""
        if hasattr(self.covar_module.kernel_c.base_kernel, 'lengthscale'):
            self.covar_module.kernel_c.base_kernel.lengthscale = 1.0
            self.covar_module.kernel_d.base_kernel.lengthscale = 1.0
            
        self.covar_module.kernel_c.outputscale = 1.0
        self.covar_module.kernel_d.outputscale = 0.1
        self.likelihood.noise_covar.noise = 1e-3

    def forward(self, x: torch.Tensor) -> gpytorch.distributions.MultivariateNormal:
        """Forward pass of Co-Kriging model.
        
        Args:
            x: Input data with fidelity indicator in last column
            
        Returns:
            MultivariateNormal distribution representing GP predictions
        """
        mean = self.mean_module(x)
        covar = self.covar_module(x)
        return gpytorch.distributions.MultivariateNormal(mean, covar)
    
    def get_hyperparameters(self) -> Dict[str, Union[float, List[float]]]:
        """Get current hyperparameter values.
        
        Returns:
            Dictionary containing the current values of all hyperparameters
        """
        hyperparameters = {
            'kernel_type': self.kernel_type,
            'outputscale_c': float(self.covar_module.kernel_c.outputscale.detach().cpu().numpy()),
            'outputscale_d': float(self.covar_module.kernel_d.outputscale.detach().cpu().numpy()),
            'rho': float(self.covar_module.rho.detach().cpu().numpy()),
            'noise': float(self.likelihood.noise_covar.noise.detach().cpu().numpy())
        }
        
        # Add lengthscales if present
        if hasattr(self.covar_module.kernel_c.base_kernel, 'lengthscale'):
            hyperparameters['lengthscales_c'] = self.covar_module.kernel_c.base_kernel.lengthscale.detach().cpu().numpy().tolist()
            hyperparameters['lengthscales_d'] = self.covar_module.kernel_d.base_kernel.lengthscale.detach().cpu().numpy().tolist()
            
        return hyperparameters
        
    def predict(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Make predictions with the Co-Kriging model.
        
        Args:
            x: Input points to make predictions at, with fidelity indicator in last column
            
        Returns:
            Tuple of (mean predictions, standard deviations)
        """
        self.eval()
        with torch.no_grad(), gpytorch.settings.fast_pred_var():
            observed_pred = self.likelihood(self(x))
            return observed_pred.mean, observed_pred.stddev