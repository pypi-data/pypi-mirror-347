
"""
Uncertainty Quantification Module for PyEGRO using Monte Carlo Simulation.
"""

import numpy as np
import pickle
import pandas as pd
import os
import json
import joblib
from pyDOE import lhs
import torch
import gpytorch
from typing import List, Dict, Any, Optional, Union, Tuple
from pathlib import Path
import matplotlib.pyplot as plt
from scipy import stats

# Import visualization module
from .visualization import InformationVisualization

# Suppress warning GP
import warnings
from gpytorch.utils.warnings import GPInputWarning
warnings.filterwarnings("ignore", category=GPInputWarning)

# Import from PyEGRO.doe
from ...doe.sampling import AdaptiveDistributionSampler

class UncertaintyPropagation:
    """Main class for uncertainty propagation analysis."""
    
    def __init__(self, 
                 data_info_path: str = "DATA_PREPARATION/data_info.json",
                 model_handler: Optional[Any] = None,
                 true_func: Optional[callable] = None,
                 model_path: Optional[str] = None,
                 use_gpu: bool = True,
                 output_dir: str = "RESULT_QOI",
                 show_variables_info: bool = True,
                 random_seed: int = 42):
        """Initialize UncertaintyPropagation.
        
        Args:
            data_info_path: Path to the data configuration file
            model_handler: Model handler for surrogate model (if using surrogate)
            true_func: True objective function (if using direct evaluation)
            model_path: Path to trained GPR model (if using surrogate)
            use_gpu: Whether to use GPU if available for surrogate model
            output_dir: Directory for saving results
            show_variables_info: Whether to display variable information
            random_seed: Random seed for reproducibility
        """
        if true_func is None and model_handler is None and model_path is None:
            raise ValueError("Either true_func, model_handler, or model_path must be provided")
            
        np.random.seed(random_seed)
        torch.manual_seed(random_seed)
        
        # Load data info
        with open(data_info_path, 'r') as f:
            data_info = json.load(f)
        self.variables = data_info['variables']
        
        # Set evaluation function and display settings
        self.true_func = true_func
        self.use_surrogate = true_func is None
        self.show_variables_info = show_variables_info
        self.model_handler = model_handler
          
        # Initialize tools
        self.sampler = AdaptiveDistributionSampler()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.visualizer = InformationVisualization(output_dir=output_dir)
        
        # Display variable information if enabled
        if self.show_variables_info:
            self.display_variable_info()

    def display_variable_info(self):
        """Display detailed information about all variables."""
        print("\nVariable Information Summary:")
        print("=" * 80)
        
        design_vars = []
        env_vars = []
        
        for var in self.variables:
            if var['vars_type'] == 'design_vars':
                design_vars.append(var)
            else:
                env_vars.append(var)
        
        # Display Design Variables
        if design_vars:
            print("\nDesign Variables:")
            print("-" * 40)
            for var in design_vars:
                print(f"\nName: {var['name']}")
                print(f"Description: {var.get('description', 'Not provided')}")
                
                # Support for multiple keys for range bounds
                range_bounds = var.get('range_bounds')
                if range_bounds:
                    print(f"Range: [{range_bounds[0]}, {range_bounds[1]}]")
                
                # Display uncertainty info if available
                has_uncertainty = False
                
                if var.get('cov') is not None:
                    print(f"Coefficient of Variation (CoV): {var.get('cov')}")
                    has_uncertainty = True
                
                if var.get('std') is not None:
                    print(f"Standard Deviation: {var.get('std')}")
                    has_uncertainty = True
                
                if var.get('delta') is not None:
                    print(f"Delta (half-width): {var.get('delta')}")
                    has_uncertainty = True
                
                print(f"Distribution: {var.get('distribution', 'normal')}")
                print(f"Type: {'Uncertain' if has_uncertainty else 'Deterministic'}")
        
        # Display Environmental Variables
        if env_vars:
            print("\nEnvironmental Variables:")
            print("-" * 40)
            for var in env_vars:
                print(f"\nName: {var['name']}")
                print(f"Description: {var.get('description', 'Not provided')}")
                print(f"Distribution: {var['distribution']}")
                
                if var['distribution'] == 'uniform':
                    # Support both min/max and low/high
                    min_val = var.get('min', var.get('low'))
                    max_val = var.get('max', var.get('high'))
                    print(f"Range: [{min_val}, {max_val}]")
                
                elif var['distribution'] in ['normal', 'lognormal']:
                    print(f"Mean: {var.get('mean')}")
                    
                    # Display either std or cov, whichever is provided
                    if var.get('std') is not None:
                        print(f"Standard Deviation: {var.get('std')}")
                    elif var.get('cov') is not None:
                        print(f"Coefficient of Variation (CoV): {var.get('cov')}")
                        print(f"Implied Std Dev: {var.get('cov') * var.get('mean')}")
        
        print("\n" + "=" * 80)
        
    @classmethod
    def from_initial_design(cls, 
                        design=None,
                        design_infos=None,
                        true_func=None, 
                        output_dir="RESULT_QOI",
                        use_gpu=True,
                        show_variables_info=True,
                        random_seed=42):
        """
        Create UncertaintyPropagation instance directly from InitialDesign object.
        
        Args:
            design: InitialDesign instance
            design_infos: Alternative name for design (backward compatibility)
            true_func: Optional override for objective function
            output_dir: Directory for saving results
            use_gpu: Whether to use GPU if available
            show_variables_info: Whether to display variable information
            random_seed: Random seed for reproducibility
            
        Returns:
            UncertaintyPropagation instance
        """
        # Support both 'design' and 'design_infos' parameter names
        design_obj = design if design is not None else design_infos
        if design_obj is None:
            raise ValueError("Either 'design' or 'design_infos' must be provided")
        
        # Get the objective function - prefer explicit true_func if provided
        objective_function = true_func if true_func is not None else getattr(design_obj, 'objective_function', None)
        
        # Create a new instance
        instance = cls.__new__(cls)
        
        # Initialize basic attributes
        instance.use_surrogate = objective_function is None
        instance.show_variables_info = show_variables_info
        instance.true_func = objective_function
        instance.model_handler = None  # No model handler in this case
        instance.variables = []  # Will be populated from design_obj
        
        # Initialize tools
        instance.sampler = AdaptiveDistributionSampler()
        instance.output_dir = Path(output_dir)
        instance.output_dir.mkdir(exist_ok=True)
        instance.visualizer = InformationVisualization(output_dir=output_dir)
        
        # Set random seed
        np.random.seed(random_seed)
        torch.manual_seed(random_seed)
        
        # Process Variable objects in a safer way
        if hasattr(design_obj, 'variables'):
            for var in design_obj.variables:
                var_dict = {}
                
                # Get attribute values safely
                var_dict["name"] = getattr(var, 'name', '')
                var_dict["vars_type"] = getattr(var, 'vars_type', '')
                var_dict["description"] = getattr(var, 'description', '')
                
                # Process design variables
                if getattr(var, 'vars_type', '') == 'design_vars':
                    var_dict["range_bounds"] = getattr(var, 'range_bounds', [0, 1])
                    
                    # Add uncertainty parameters if present
                    has_uncertainty = False
                    
                    if hasattr(var, 'cov') and var.cov is not None and var.cov > 0:
                        var_dict["cov"] = var.cov
                        has_uncertainty = True
                    
                    if hasattr(var, 'std') and var.std is not None and var.std > 0:
                        var_dict["std"] = var.std
                        has_uncertainty = True
                    
                    if hasattr(var, 'delta') and var.delta is not None and var.delta > 0:
                        var_dict["delta"] = var.delta
                        has_uncertainty = True
                    
                    if has_uncertainty:
                        var_dict["distribution"] = getattr(var, 'distribution', 'normal')
                
                # Process env variables
                else:  # env_vars
                    var_dict["distribution"] = getattr(var, 'distribution', 'uniform')
                    
                    # Add distribution-specific parameters
                    if getattr(var, 'distribution', '') == "uniform":
                        # Support both min/max and low/high
                        if hasattr(var, 'min') and var.min is not None:
                            var_dict["min"] = var.min
                        elif hasattr(var, 'low') and var.low is not None:
                            var_dict["low"] = var.low
                            
                        if hasattr(var, 'max') and var.max is not None:
                            var_dict["max"] = var.max
                        elif hasattr(var, 'high') and var.high is not None:
                            var_dict["high"] = var.high
                            
                    elif getattr(var, 'distribution', '') in ["normal", "lognormal"]:
                        var_dict["mean"] = getattr(var, 'mean', 0)
                        
                        # Support both std and cov
                        if hasattr(var, 'std') and var.std is not None:
                            var_dict["std"] = var.std
                        elif hasattr(var, 'cov') and var.cov is not None:
                            var_dict["cov"] = var.cov
                
                instance.variables.append(var_dict)
        
        # If no variables found, try design_info
        elif hasattr(design_obj, 'design_info') and isinstance(design_obj.design_info, dict):
            if 'variables' in design_obj.design_info:
                instance.variables = design_obj.design_info['variables']
        
        # Display variable information if enabled
        if instance.show_variables_info:
            instance.display_variable_info()
        
        return instance

    def _evaluate_samples(self, X_samples: np.ndarray) -> np.ndarray:
        """Evaluate samples using either true function or surrogate."""
        if self.model_handler:
            mean_pred, _ = self.model_handler.predict(X_samples)
            return mean_pred
        else:
            return self.true_func(X_samples)

    def _generate_env_samples(self, var: Dict[str, Any], size: int) -> np.ndarray:
        """Generate samples for an environmental variable."""
        return self.sampler.generate_env_samples(var, size)

    def _process_design_point(self, 
                            design_point: np.ndarray, 
                            num_mcs_samples: int) -> np.ndarray:
        """Process a single design point with Monte Carlo sampling."""
        X_samples = np.zeros((num_mcs_samples, len(self.variables)))
        design_var_idx = 0
        
        for i, var in enumerate(self.variables):
            if var['vars_type'] == 'design_vars':
                # Only process if we have design variables
                if len(design_point) > 0:
                    base_value = design_point[design_var_idx]
                    
                    # Check for uncertainty parameters
                    has_uncertainty = False
                    
                    # Case 1: Using CoV
                    if var.get('cov') is not None and var.get('cov') > 0:
                        lower, upper = var['range_bounds']
                        X_samples[:, i] = self.sampler.generate_samples(
                            distribution=var.get('distribution', 'normal'),
                            mean=base_value,
                            cov=var['cov'],
                            lower=lower,
                            upper=upper,
                            size=num_mcs_samples
                        )
                        has_uncertainty = True
                    
                    # Case 2: Using std
                    elif var.get('std') is not None and var.get('std') > 0:
                        lower, upper = var['range_bounds']
                        X_samples[:, i] = self.sampler.generate_samples(
                            distribution=var.get('distribution', 'normal'),
                            mean=base_value,
                            std=var['std'],
                            lower=lower,
                            upper=upper,
                            size=num_mcs_samples
                        )
                        has_uncertainty = True
                    
                    # Case 3: Using delta for uniform
                    elif var.get('delta') is not None and var.get('delta') > 0:
                        if var.get('distribution') == 'uniform':
                            X_samples[:, i] = self.sampler.generate_samples(
                                distribution='uniform',
                                mean=base_value,
                                delta=var['delta'],
                                size=num_mcs_samples
                            )
                        else:
                            # Treat delta as std for non-uniform distributions
                            lower, upper = var['range_bounds']
                            X_samples[:, i] = self.sampler.generate_samples(
                                distribution=var.get('distribution', 'normal'),
                                mean=base_value,
                                std=var['delta'],
                                lower=lower,
                                upper=upper,
                                size=num_mcs_samples
                            )
                        has_uncertainty = True
                    
                    # Deterministic case
                    if not has_uncertainty:
                        X_samples[:, i] = base_value
                    
                    design_var_idx += 1
                
            else:  # Environmental variable
                # Use AdaptiveDistributionSampler for env variables
                X_samples[:, i] = self._generate_env_samples(var, num_mcs_samples)
        
        Y_samples = self._evaluate_samples(X_samples)
        
        stats = {
            'mean': np.mean(Y_samples),
            'std': np.std(Y_samples),
            'percentiles': np.percentile(Y_samples, [2.5, 97.5])
        }
        
        # Return appropriate result format depending on whether we have design variables
        design_var_count = len([var for var in self.variables if var['vars_type'] == 'design_vars'])
        if design_var_count > 0:
            return np.concatenate((
                design_point,
                [stats['mean'], stats['std'], stats['percentiles'][0], stats['percentiles'][1]]
            ))
        else:
            # Just return the statistics without design points
            return np.array([stats['mean'], stats['std'], stats['percentiles'][0], stats['percentiles'][1]])

    def run_analysis(self,
                    true_func: Optional[callable] = None,
                    num_design_samples: int = 1000,
                    num_mcs_samples: int = 100000,
                    show_progress: bool = True) -> pd.DataFrame:
        """
        Run the uncertainty propagation analysis.
        
        Args:
            true_func: Optional override for the true function
            num_design_samples: Number of design points to evaluate
            num_mcs_samples: Number of Monte Carlo samples per design point
            show_progress: Whether to show progress bar
            
        Returns:
            DataFrame containing the analysis results
        """
        # Override true_func if provided
        if true_func is not None:
            original_true_func = self.true_func
            self.true_func = true_func
            
        if self.show_variables_info:
            print("\nAnalysis Configuration:")
            print(f"Number of design samples: {num_design_samples}")
            print(f"Number of Monte Carlo samples per design point: {num_mcs_samples}")
            print(f"Using surrogate model: {self.use_surrogate}")
            print("\nStarting analysis...\n")
        
        # Get design variables
        design_vars = [var for var in self.variables if var['vars_type'] == 'design_vars']
        
        # Handle case with no design variables
        if not design_vars:
            # When there are no design variables, we just need one "design point"
            # Create a dummy design point (empty array)
            dummy_design_point = np.array([])
            
            # Process this single point with Monte Carlo sampling for env variables
            result = self._process_design_point(dummy_design_point, num_mcs_samples)
            results = [result]
            
            # Create results DataFrame - only Mean, StdDev, and CI columns since no design vars
            columns = ['Mean', 'StdDev', 'CI_Lower', 'CI_Upper']
            results_df = pd.DataFrame([result], columns=columns)
        else:
            # Normal case with design variables - use LHS
            design_bounds = np.array([var['range_bounds'] for var in design_vars])
            
            # Generate LHS samples for design variables
            lhs_design = lhs(len(design_vars), samples=num_design_samples)
            lhs_design = lhs_design * (design_bounds[:, 1] - design_bounds[:, 0]) + design_bounds[:, 0]
            
            # Process samples
            results = []
            if show_progress:
                from rich.progress import Progress, BarColumn, TimeElapsedColumn, TimeRemainingColumn, TaskProgressColumn
                with Progress(
                    "[progress.description]{task.description}",
                    BarColumn(),
                    TaskProgressColumn(),
                    TimeElapsedColumn(),
                    TimeRemainingColumn(),
                ) as progress:
                    task = progress.add_task(
                        f"[green]Processing {num_design_samples} design points...", 
                        total=num_design_samples
                    )
                    
                    for i in range(num_design_samples):
                        result = self._process_design_point(
                            lhs_design[i],
                            num_mcs_samples
                        )
                        results.append(result)
                        progress.advance(task)
            else:
                for i in range(num_design_samples):
                    result = self._process_design_point(
                        lhs_design[i],
                        num_mcs_samples
                    )
                    results.append(result)
            
            # Create results DataFrame
            columns = ([var['name'] for var in design_vars] +
                    ['Mean', 'StdDev', 'CI_Lower', 'CI_Upper'])
            results_df = pd.DataFrame(results, columns=columns)
        
        # Save results and create visualizations
        self._save_results(results_df)
        
        if self.show_variables_info:
            print("\nAnalysis completed!")
            print(f"Results saved in: {self.output_dir}")
        
        # Restore original true_func if it was temporarily overridden
        if true_func is not None:
            self.true_func = original_true_func
            
        return results_df
    
    def _save_results(self, results_df: pd.DataFrame):
        """Save analysis results and create visualizations."""
        # Save CSV
        results_df.to_csv(self.output_dir / 'uncertainty_propagation_results.csv', index=False)
        
        # Create visualizations
        design_vars = [var for var in self.variables if var['vars_type'] == 'design_vars']
        self.visualizer.create_visualization(results_df, design_vars)
        
        # Save summary statistics
        summary_stats = {
            'mean_range': [float(results_df['Mean'].min()), float(results_df['Mean'].max())],
            'stddev_range': [float(results_df['StdDev'].min()), float(results_df['StdDev'].max())],
            'ci_width_range': [
                float((results_df['CI_Upper'] - results_df['CI_Lower']).min()),
                float((results_df['CI_Upper'] - results_df['CI_Lower']).max())
            ]
        }
        
        with open(self.output_dir / 'analysis_summary.json', 'w') as f:
            json.dump(summary_stats, f, indent=4)

    def analyze_specific_point(self,
                             design_point: Dict[str, float],
                             env_vars_override: Optional[Dict[str, Dict[str, float]]] = None,
                             num_mcs_samples: int = 100000,
                             create_pdf: bool = True,
                             create_reliability: bool = True) -> Dict[str, Any]:
        """
        Analyze uncertainty at a specific design point with customized env variables.
        
        Args:
            design_point: Dictionary of design variable values {var_name: value}
            env_vars_override: Optional dictionary to override env variable distributions
                              Format: {var_name: {'mean': val, 'std': val}} or
                                     {var_name: {'min': val, 'max': val}} or
                                     {var_name: {'low': val, 'high': val}}
            num_mcs_samples: Number of Monte Carlo samples
            create_pdf: Whether to create PDF visualization
            create_reliability: Whether to create reliability plot
            
        Returns:
            Dictionary containing analysis results
        """
        # Validate design point variables
        design_vars = [var for var in self.variables if var['vars_type'] == 'design_vars']
        design_var_names = [var['name'] for var in design_vars]
        
        for var_name in design_point:
            if var_name not in design_var_names:
                raise ValueError(f"Design variable '{var_name}' not found in model variables")
        
        # Check if all design variables are provided
        for var_name in design_var_names:
            if var_name not in design_point:
                raise ValueError(f"Missing design variable '{var_name}' in design_point")
        
        # Create design point array in the correct order
        design_point_array = np.array([design_point[var['name']] for var in design_vars])
        
        # Override env variable distributions if provided
        original_env_vars = None
        if env_vars_override:
            # Store original env vars for restoration later
            original_env_vars = [var.copy() for var in self.variables if var['vars_type'] == 'env_vars']
            
            # Update env variables with overrides
            for i, var in enumerate(self.variables):
                if var['vars_type'] == 'env_vars' and var['name'] in env_vars_override:
                    override = env_vars_override[var['name']]
                    for key, value in override.items():
                        # Handle both min/max and low/high consistently
                        if key == 'min' and 'low' in self.variables[i]:
                            self.variables[i]['low'] = value
                        elif key == 'max' and 'high' in self.variables[i]:
                            self.variables[i]['high'] = value
                        elif key == 'low' and 'min' in self.variables[i]:
                            self.variables[i]['min'] = value
                        elif key == 'high' and 'max' in self.variables[i]:
                            self.variables[i]['max'] = value
                        else:
                            self.variables[i][key] = value
        
        # Generate samples for analysis
        X_samples = np.zeros((num_mcs_samples, len(self.variables)))
        
        # Set design variables to fixed values
        design_var_idx = 0
        for i, var in enumerate(self.variables):
            if var['vars_type'] == 'design_vars':
                base_value = design_point_array[design_var_idx]
                
                # Check which uncertainty parameter to use
                has_uncertainty = False
                
                # Case 1: Using CoV
                if var.get('cov') is not None and var.get('cov') > 0:
                    lower, upper = var['range_bounds']
                    X_samples[:, i] = self.sampler.generate_samples(
                        distribution=var.get('distribution', 'normal'),
                        mean=base_value,
                        cov=var['cov'],
                        lower=lower,
                        upper=upper,
                        size=num_mcs_samples
                    )
                    has_uncertainty = True
                
                # Case 2: Using std
                elif var.get('std') is not None and var.get('std') > 0:
                    lower, upper = var['range_bounds']
                    X_samples[:, i] = self.sampler.generate_samples(
                        distribution=var.get('distribution', 'normal'),
                        mean=base_value,
                        std=var['std'],
                        lower=lower,
                        upper=upper,
                        size=num_mcs_samples
                    )
                    has_uncertainty = True
                
                # Case 3: Using delta for uniform
                elif var.get('delta') is not None and var.get('delta') > 0:
                    if var.get('distribution') == 'uniform':
                        X_samples[:, i] = self.sampler.generate_samples(
                            distribution='uniform',
                            mean=base_value,
                            delta=var['delta'],
                            size=num_mcs_samples
                        )
                    else:
                        # Treat delta as std for non-uniform distributions
                        lower, upper = var['range_bounds']
                        X_samples[:, i] = self.sampler.generate_samples(
                            distribution=var.get('distribution', 'normal'),
                            mean=base_value,
                            std=var['delta'],
                            lower=lower,
                            upper=upper,
                            size=num_mcs_samples
                        )
                    has_uncertainty = True
                
                # Deterministic case
                if not has_uncertainty:
                    X_samples[:, i] = base_value
                
                design_var_idx += 1
            else:  # Environmental variable
                X_samples[:, i] = self._generate_env_samples(var, num_mcs_samples)
        
        # Evaluate samples
        Y_samples = self._evaluate_samples(X_samples)
        
        # Compute statistics
        mean = np.mean(Y_samples)
        std = np.std(Y_samples)
        percentiles = np.percentile(Y_samples, [2.5, 25, 50, 75, 97.5])
        
        # Create PDF visualization if requested
        if create_pdf:
            pdf_title = f"Probability Density Function at Design Point"
            self.visualizer.create_pdf_visualization(
                design_point=design_point,
                samples=Y_samples,
                title=pdf_title,
                filename="point_specific_pdf.png"
            )
        
        # Create reliability plot if requested
        if create_reliability:
            # Generate range of threshold values
            threshold_min = min(mean - 3*std, np.min(Y_samples))
            threshold_max = max(mean + 3*std, np.max(Y_samples))
            threshold_values = np.linspace(threshold_min, threshold_max, 100)
            
            # Create reliability plot
            self.visualizer.create_reliability_plot(
                samples=Y_samples,
                threshold_values=threshold_values,
                threshold_type='upper',  # Default to exceedance probability
                title="Probability of Failure Curve",
                filename="point_specific_reliability.png"
            )
        
        
        # Restore original env vars if they were overridden
        if original_env_vars:
            env_idx = 0
            for i, var in enumerate(self.variables):
                if var['vars_type'] == 'env_vars':
                    self.variables[i] = original_env_vars[env_idx]
                    env_idx += 1
        
        # Compile results
        results = {
            'design_point': design_point,
            'statistics': {
                'mean': mean,
                'std': std,
                'cov': std / abs(mean) if mean != 0 else float('inf'),
                'percentiles': {
                    '2.5': percentiles[0],
                    '25': percentiles[1],
                    '50': percentiles[2],
                    '75': percentiles[3],
                    '97.5': percentiles[4]
                }
            },
            'reliability': {
                'p_exceed_mean': np.mean(Y_samples > mean),
                'p_below_mean': np.mean(Y_samples < mean)
            }
        }
    
        # Save results to JSON
        with open(self.output_dir / 'point_specific_analysis.json', 'w') as f:
            json.dump(results, f, indent=4, default=lambda x: float(x) if isinstance(x, np.float32) or isinstance(x, np.float64) else x)
        
        return results
    



def run_uncertainty_analysis(
    data_info_path: str = "DATA_PREPARATION/data_info.json",
    true_func: Optional[callable] = None,
    model_handler: Optional[Any] = None,
    model_path: Optional[str] = None,
    num_design_samples: int = 1000,
    num_mcs_samples: int = 100000,
    use_gpu: bool = True,
    output_dir: str = "RESULT_QOI",
    random_seed: int = 42,
    show_progress: bool = True
) -> pd.DataFrame:
    """
    Convenience function to run uncertainty propagation analysis.
    
    Args:
        data_info_path: Path to the data configuration file
        true_func: True objective function (if using direct evaluation)
        model_handler: Model handler for surrogate model
        model_path: Path to trained GPR model (if using surrogate)
        num_design_samples: Number of design points to evaluate
        num_mcs_samples: Number of Monte Carlo samples per design point
        use_gpu: Whether to use GPU if available for surrogate model
        output_dir: Directory for saving results
        random_seed: Random seed for reproducibility
        show_progress: Whether to show progress bar
        
    Returns:
        DataFrame containing the analysis results
    """
    propagation = UncertaintyPropagation(
        data_info_path=data_info_path,
        true_func=true_func,
        model_handler=model_handler,
        model_path=model_path,
        use_gpu=use_gpu,
        output_dir=output_dir,
        random_seed=random_seed
    )
    
    return propagation.run_analysis(
        num_design_samples=num_design_samples,
        num_mcs_samples=num_mcs_samples,
        show_progress=show_progress
    )


def analyze_specific_point(
    data_info_path: str,
    design_point: Dict[str, float],
    true_func: Optional[callable] = None,
    model_handler: Optional[Any] = None,
    env_vars_override: Optional[Dict[str, Dict[str, float]]] = None,
    num_mcs_samples: int = 100000,
    output_dir: str = "RESULT_QOI_POINT",
    random_seed: int = 42,
    create_pdf: bool = True,
    create_reliability: bool = True
) -> Dict[str, Any]:
    """
    Convenience function to analyze uncertainty at a specific design point.
    
    Args:
        data_info_path: Path to the data configuration file
        design_point: Dictionary of design variable values {var_name: value}
        true_func: True objective function (if using direct evaluation)
        model_handler: Model handler for surrogate model
        env_vars_override: Optional dictionary to override env variable distributions
                          Format: {var_name: {'mean': val, 'std': val}} or
                                 {var_name: {'min': val, 'max': val}}
        num_mcs_samples: Number of Monte Carlo samples
        output_dir: Directory for saving results
        random_seed: Random seed for reproducibility
        create_pdf: Whether to create PDF visualization
        create_reliability: Whether to create reliability plot
        
    Returns:
        Dictionary containing analysis results
    """
    propagation = UncertaintyPropagation(
        data_info_path=data_info_path,
        true_func=true_func,
        model_handler=model_handler,
        output_dir=output_dir,
        random_seed=random_seed
    )
    
    return propagation.analyze_specific_point(
        design_point=design_point,
        env_vars_override=env_vars_override,
        num_mcs_samples=num_mcs_samples,
        create_pdf=create_pdf,
        create_reliability=create_reliability
    )