# sampling.py
from scipy.stats import truncnorm, qmc
import numpy as np
from typing import List, Dict, Any, Optional, Union
from pyDOE import lhs
from dataclasses import dataclass

@dataclass
class Variable:
    """
    Class to represent a variable in the design space.
    
    Attributes
    ----------
    name : str
        Name of the variable
    vars_type : str
        Type of variable ('design_vars' or 'env_vars')
    distribution : str
        Distribution type ('uniform', 'normal', or 'lognormal')
    description : str
        Description of the variable (optional)
    range_bounds : List[float], optional
        [min, max] bounds for design variables
    cov : float, optional
        Coefficient of variation for design variables or env variables (optional)
    std : float, optional
        Standard deviation for design variables or env variables (optional)
    delta : float, optional
        Half-width for uniform distribution (for design variables with uncertainty)
    mean : float, optional
        Mean value for environmental variables
    min : float, optional
        Lower bound for environmental variables (uniform distribution)
    max : float, optional
        Upper bound for environmental variables (uniform distribution)
    low : float, optional
        Alias for min (for backward compatibility)
    high : float, optional
        Alias for max (for backward compatibility)
    """
    name: str
    vars_type: str  # 'design_vars' or 'env_vars'
    distribution: str  # 'uniform', 'normal', or 'lognormal'
    description: str = ""
    
    # For design variables
    range_bounds: Optional[List[float]] = None
    cov: Optional[float] = None
    std: Optional[float] = None
    delta: Optional[float] = None
    
    # For environmental variables
    mean: Optional[float] = None
    min: Optional[float] = None
    max: Optional[float] = None
    low: Optional[float] = None  # Alias for min (backward compatibility)
    high: Optional[float] = None  # Alias for max (backward compatibility)

class AdaptiveDistributionSampler:
    """
    Class for generating samples using various sampling methods.
    
    Supported Methods
    ----------------
    - Random: Simple random sampling
    - LHS: Latin Hypercube Sampling
    - Sobol: Sobol sequence (low-discrepancy)
    - Halton: Halton sequence (low-discrepancy)
    """
    
    SAMPLING_METHODS = ['random', 'lhs', 'sobol', 'halton']
    
    @staticmethod
    def generate_samples(
        distribution: str,
        mean: Optional[float] = None,
        cov: Optional[float] = None,
        std: Optional[float] = None,
        delta: Optional[float] = None,
        lower: Optional[float] = None,
        upper: Optional[float] = None,
        size: int = 1000
    ) -> np.ndarray:

        """
        Generate samples for a given distribution type.

        Parameters
        ----------
        distribution : str
            Type of distribution ('uniform', 'normal', or 'lognormal')
        mean : float, optional
            Mean value for normal/lognormal distributions
        cov : float, optional
            Coefficient of variation for normal/lognormal distributions
        std : float, optional
            Standard Deviation for normal/lognormal distributions
        delta : float, optional
            Half-width for uniform distribution (around mean)
        lower : float, optional
            Lower bound for the distribution
        upper : float, optional
            Upper bound for the distribution
        size : int, optional
            Number of samples to generate (default: 1000)

        Returns
        -------
        numpy.ndarray
            Generated samples
        """
        if distribution == 'uniform':
            # Handle the case where delta is provided for design variable with uncertainty
            if delta is not None and mean is not None:
                return np.random.uniform(mean - delta, mean + delta, size)
            # Standard uniform sampling between lower and upper bounds
            return np.random.uniform(lower, upper, size)
        
        elif distribution == 'normal':
            # Determine the standard deviation based on available parameters
            if std is None:
                if cov is not None:
                    if mean is None:
                        raise ValueError("Mean value is required when using 'cov' for normal distribution.")
                    
                    # Handle near-zero mean safely
                    if abs(mean) < 1e-8:
                        # Use a small absolute std for near-zero means instead of multiplication
                        std = 0.01 if cov < 0.5 else 0.05
                    else:
                        std = abs(mean * cov)
                else:
                    raise ValueError("You must specify either 'cov' or 'std' for normal distribution.")
            
            # Ensure std is positive
            std = abs(std)
            
            # Set default bounds if not provided
            if lower is None:
                lower = mean - 3 * std if mean is not None else -np.inf
            if upper is None:
                upper = mean + 3 * std if mean is not None else np.inf

            a = (lower - mean) / std
            b = (upper - mean) / std

            samples = truncnorm.rvs(a, b, loc=mean, scale=std, size=size)
            return np.clip(samples, lower, upper)
        
        elif distribution == 'lognormal':
            if std is None and cov is not None:
                sigma = np.sqrt(np.log(1 + cov**2))
            elif std is not None and mean is not None:
                # Convert std to equivalent cov for lognormal
                cov_equiv = std / mean
                sigma = np.sqrt(np.log(1 + cov_equiv**2))
            else:
                raise ValueError("For lognormal distribution, you must provide either 'std' and 'mean' or 'cov'")
                
            mu = np.log(mean) - 0.5 * sigma**2
            
            if lower is not None and upper is not None:
                log_lower = np.log(max(lower, 1e-10))
                log_upper = np.log(upper)
                a = (log_lower - mu) / sigma
                b = (log_upper - mu) / sigma
                log_samples = truncnorm.rvs(a, b, loc=mu, scale=sigma, size=size)
                samples = np.exp(log_samples)
            else:
                samples = np.random.lognormal(mu, sigma, size)
            
            return np.clip(samples, lower, upper)
        
        else:
            raise ValueError(f"Unsupported distribution: {distribution}")

    @staticmethod
    def generate_design_samples(
        design_vars: List[Variable], 
        num_samples: int,
        method: str = 'lhs',
        criterion: Optional[str] = 'maximin'
    ) -> np.ndarray:
        """
        Generate samples for design variables using specified method.

        Parameters
        ----------
        design_vars : List[Variable]
            List of design variables
        num_samples : int
            Number of samples to generate
        method : str, optional
            Sampling method to use (default: 'lhs')
        criterion : str, optional
            Criterion for LHS sampling (default: 'maximin')

        Returns
        -------
        numpy.ndarray
            Generated samples scaled to variable bounds
        """
        if method not in AdaptiveDistributionSampler.SAMPLING_METHODS:
            raise ValueError(f"Unsupported sampling method: {method}. "
                           f"Available methods: {AdaptiveDistributionSampler.SAMPLING_METHODS}")
        
        design_bounds = np.array([var.range_bounds for var in design_vars])
        dim = len(design_vars)
        
        if method == 'random':
            base_samples = np.random.random((num_samples, dim))
            
        elif method == 'lhs':
            base_samples = lhs(dim, samples=num_samples, criterion=criterion)
            
        elif method == 'sobol':
            sampler = qmc.Sobol(d=dim, scramble=True)
            base_samples = sampler.random_base2(m=int(np.ceil(np.log2(num_samples))))[:num_samples]
            
        elif method == 'halton':
            sampler = qmc.Halton(d=dim, scramble=True)
            base_samples = sampler.random(n=num_samples)
            
        # Scale samples to design bounds
        return base_samples * (design_bounds[:, 1] - design_bounds[:, 0]) + design_bounds[:, 0]

    @staticmethod
    def generate_env_samples(var: Union[Variable, Dict[str, Any]], num_samples: int) -> np.ndarray:
        """
        Generate samples for an environmental variable.

        Parameters
        ----------
        var : Union[Variable, Dict[str, Any]]
            Environmental variable to sample (either Variable object or dictionary)
        num_samples : int
            Number of samples to generate

        Returns
        -------
        numpy.ndarray
            Generated samples
        """
        # Handle both Variable objects and dictionaries
        if isinstance(var, dict):
            # If var is a dictionary
            if var['distribution'] == 'uniform':
                # Support both min/max and low/high keys for uniform distribution
                low = var.get('min', var.get('low'))
                high = var.get('max', var.get('high'))
                return np.random.uniform(low, high, num_samples)
            
            elif var['distribution'] in ['normal', 'lognormal']:
                # Get bounds if specified
                lower = var.get('min', var.get('low'))
                upper = var.get('max', var.get('high'))
                
                # Support both std and cov specifications
                return AdaptiveDistributionSampler.generate_samples(
                    distribution=var['distribution'],
                    mean=var.get('mean'),
                    cov=var.get('cov'),
                    std=var.get('std'),
                    lower=lower,
                    upper=upper,
                    size=num_samples
                )
        else:
            # If var is a Variable object
            if var.distribution == 'uniform':
                # Use min/max if available, fall back to low/high
                low = var.min if var.min is not None else var.low
                high = var.max if var.max is not None else var.high
                return np.random.uniform(low, high, num_samples)
            
            elif var.distribution in ['normal', 'lognormal']:
                # Get bounds if specified
                lower = var.min if var.min is not None else var.low
                upper = var.max if var.max is not None else var.high
                
                return AdaptiveDistributionSampler.generate_samples(
                    distribution=var.distribution,
                    mean=var.mean,
                    cov=var.cov,
                    std=var.std,
                    lower=lower,
                    upper=upper,
                    size=num_samples
                )

    @classmethod
    def generate_all_samples(
        cls,
        variables: List[Variable],
        num_samples: int,
        method: str = 'lhs',
        criterion: Optional[str] = None
    ) -> np.ndarray:
        """
        Generate samples for all variables.

        Parameters
        ----------
        variables : List[Variable]
            List of all variables (design and environmental)
        num_samples : int
            Number of samples to generate
        method : str, optional
            Sampling method for design variables (default: 'lhs')
        criterion : str, optional
            Criterion for LHS sampling (default: None)

        Returns
        -------
        numpy.ndarray
            Generated samples for all variables
        """
        all_samples = np.zeros((num_samples, len(variables)))
        
        # Handle design variables
        design_vars = [var for var in variables if var.vars_type == 'design_vars']
        if design_vars:
            design_samples = cls.generate_design_samples(
                design_vars,
                num_samples,
                method=method,
                criterion=criterion
            )
            design_idx = 0
            for i, var in enumerate(variables):
                if var.vars_type == 'design_vars':
                    all_samples[:, i] = design_samples[:, design_idx]
                    design_idx += 1
        
        # Handle environmental variables
        for i, var in enumerate(variables):
            if var.vars_type == 'env_vars':
                all_samples[:, i] = cls.generate_env_samples(var, num_samples)
        
        return all_samples

    @staticmethod
    def calculate_input_bounds(variables: List[Variable]) -> List[List[float]]:
        """
        Calculate input bounds for all variables.

        Parameters
        ----------
        variables : List[Variable]
            List of all variables

        Returns
        -------
        List[List[float]]
            List of [min, max] bounds for each variable
        """
        bounds = []
        for var in variables:
            if var.vars_type == 'design_vars':
                bounds.append(var.range_bounds)
            elif var.vars_type == 'env_vars':
                if var.distribution == 'uniform':
                    # Support both min/max and low/high
                    low = var.min if var.min is not None else var.low
                    high = var.max if var.max is not None else var.high
                    bounds.append([low, high])
                elif var.distribution == 'normal':
                    # Support both std and cov
                    if var.std is not None:
                        std = var.std
                    elif var.cov is not None:
                        std = var.mean * var.cov
                    else:
                        std = 1.0  # Default fallback
                    bounds.append([var.mean - 3*std, var.mean + 3*std])
                elif var.distribution == 'lognormal':
                    # Support both std and cov
                    if var.std is not None:
                        cov_equiv = var.std / var.mean
                    else:
                        cov_equiv = var.cov
                        
                    log_std = np.sqrt(np.log(1 + cov_equiv**2))
                    log_mean = np.log(var.mean) - 0.5 * log_std**2
                    bounds.append([
                        np.exp(log_mean - 3*log_std),
                        np.exp(log_mean + 3*log_std)
                    ])
        return bounds