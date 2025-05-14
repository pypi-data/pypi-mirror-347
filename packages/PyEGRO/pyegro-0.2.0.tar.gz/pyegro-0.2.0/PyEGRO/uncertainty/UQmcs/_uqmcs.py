
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
from ...doe.sampling import AdaptiveDistributionSampler
from typing import List, Dict, Any, Optional
from pathlib import Path
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from matplotlib import rcParams 
from rich.progress import Progress, BarColumn, TimeElapsedColumn, TimeRemainingColumn, TaskProgressColumn

# Setting plots - Front
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Times New Roman']
rcParams['font.size'] = 16
rcParams['axes.titlesize'] = 16
rcParams['axes.labelsize'] = 16
rcParams['xtick.labelsize'] = 16
rcParams['ytick.labelsize'] = 16

# Suppress warning GP
import warnings
from gpytorch.utils.warnings import GPInputWarning
warnings.filterwarnings("ignore", category=GPInputWarning)

from ...doe.initial_design import InitialDesign


class InformationVisualization:
    """Handles visualization of uncertainty analysis results."""
    
    def __init__(self, output_dir=None):
        self.output_dir = Path(output_dir) if output_dir else Path('RESULT_QOI')
        self.output_dir.mkdir(exist_ok=True)


    def create_visualization(self, results_df: pd.DataFrame, design_vars: List[Dict[str, Any]]):
        """Create appropriate visualization based on number of design variables."""
        plt.close('all')
        
        n_design_vars = len(design_vars)
        
        if n_design_vars == 1:
            fig = self._create_1d_visualization(results_df, design_vars)
        elif n_design_vars == 2:
            fig = self._create_2d_visualization(results_df, design_vars)
        else:
            fig = self._create_correlation_matrix(results_df, design_vars)

        self._save_visualizations(fig)

    def _create_1d_visualization(self, results_df: pd.DataFrame, design_vars: List[Dict[str, Any]]):
        """Create 1D visualization with uncertainty bounds."""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8), height_ratios=[2, 2])
        
        sorted_data = results_df.sort_values(by=design_vars[0]['name'])
        x_var = design_vars[0]['name']
        
        # Mean with uncertainty bounds
        ax1.plot(sorted_data[x_var], sorted_data['Mean'],
                color='blue', label='Mean Response', linewidth=1.5)
        
        upper_bound = sorted_data['Mean'] + 2*sorted_data['StdDev']
        lower_bound = sorted_data['Mean'] - 2*sorted_data['StdDev']
        
        ax1.fill_between(sorted_data[x_var],
                        lower_bound,
                        upper_bound,
                        alpha=0.2, color='blue',
                        label='Mean ± 2σ')
        
        ax1.set_xlabel(x_var)
        ax1.set_ylabel('Mean Response')
        ax1.set_title('Mean Response with Uncertainty Bounds')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Standard Deviation
        ax2.plot(sorted_data[x_var], sorted_data['StdDev'],
                color='red', label='Standard Deviation', linewidth=1.5)
        
        ax2.set_xlabel(x_var)
        ax2.set_ylabel('Standard Deviation')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        return fig

    def _create_2d_visualization(self, results_df: pd.DataFrame, design_vars: List[Dict[str, Any]]):
        """Create 2D visualization with surface plots."""
        fig = plt.figure(figsize=(15, 6))
        plt.subplots_adjust(wspace=0.4)
        
        x = results_df[design_vars[0]['name']]
        y = results_df[design_vars[1]['name']]
        z_mean = results_df['Mean']
        z_std = results_df['StdDev']
        
        x_unique = np.linspace(x.min(), x.max(), 100)
        y_unique = np.linspace(y.min(), y.max(), 100)
        x_grid, y_grid = np.meshgrid(x_unique, y_unique)
        
        z_mean_grid = griddata((x, y), z_mean, (x_grid, y_grid), method='cubic')
        z_std_grid = griddata((x, y), z_std, (x_grid, y_grid), method='cubic')
        
        ax1 = fig.add_subplot(121, projection='3d')
        surf1 = ax1.plot_surface(x_grid, y_grid, z_mean_grid, 
                               cmap='viridis',
                               alpha=1,
                               antialiased=True)
        
        self._format_3d_subplot(ax1, design_vars[0]['name'], design_vars[1]['name'], 
                              'Mean Response', surf1, 'Mean Value', 'Mean Response Surface')
        
        ax2 = fig.add_subplot(122, projection='3d')
        surf2 = ax2.plot_surface(x_grid, y_grid, z_std_grid,
                               cmap='plasma',
                               alpha=1,
                               antialiased=True)
        
        self._format_3d_subplot(ax2, design_vars[0]['name'], design_vars[1]['name'], 
                              'Std Dev', surf2, 'Standard Deviation Value', 
                              'Standard Deviation Surface')
        
        return fig

    def _format_3d_subplot(self, ax, xlabel, ylabel, zlabel, surf, colorbar_label, title):
        """Format 3D subplots."""
        ax.set_xlabel(xlabel, labelpad=10)
        ax.set_ylabel(ylabel, labelpad=10)
        ax.set_zlabel(zlabel, labelpad=10)
        ax.view_init(elev=20, azim=45)
        ax.grid(True, alpha=0.3)
        
        cbar = plt.colorbar(surf, ax=ax, pad=0.1)
        cbar.set_label(colorbar_label)
        ax.set_title(title, pad=20)

    def _create_correlation_matrix(self, results_df: pd.DataFrame, design_vars: List[Dict[str, Any]]):
        """Create correlation matrix visualization."""
        fig = plt.figure(figsize=(10, 8))
        correlation_data = results_df[[var['name'] for var in design_vars] + ['Mean', 'StdDev']].corr()
        plt.imshow(correlation_data, cmap='RdBu', aspect='auto')
        plt.colorbar(label='Correlation Coefficient')
        plt.xticks(range(len(correlation_data.columns)), correlation_data.columns, rotation=45)
        plt.yticks(range(len(correlation_data.columns)), correlation_data.columns)
        plt.title('Correlation Matrix of Design Variables and Response')
        return fig

    def _save_visualizations(self, fig):
        """Save visualizations."""
        plt.savefig(self.output_dir / 'uncertainty_analysis.png',
                   dpi=300, 
                   bbox_inches='tight',
                   pad_inches=0.05)
        
        with open(self.output_dir / 'uncertainty_analysis.fig.pkl', 'wb') as fig_file:
            pickle.dump(fig, fig_file)
        
        plt.close(fig)


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
        self.visualizer = InformationVisualization(output_dir=output_dir) 
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
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
                # Changed to use range_bounds instead of range
                range_bounds = var.get('range_bounds')
                if range_bounds:
                    print(f"Range: [{range_bounds[0]}, {range_bounds[1]}]")
                print(f"Coefficient of Variation (CoV): {var.get('cov', 0)}")
                print(f"Distribution: {var.get('distribution', 'normal')}")
                if var.get('cov', 0) > 0:
                    print("Type: Uncertain")
                else:
                    print("Type: Deterministic")
        
        # Display Environmental Variables
        if env_vars:
            print("\nEnvironmental Variables:")
            print("-" * 40)
            for var in env_vars:
                print(f"\nName: {var['name']}")
                print(f"Description: {var.get('description', 'Not provided')}")
                print(f"Distribution: {var['distribution']}")
                if var['distribution'] == 'uniform':
                    print(f"Range: [{var.get('low')}, {var.get('high')}]")
                elif var['distribution'] == 'normal':
                    print(f"Mean: {var.get('mean')}")
                    print(f"Standard Deviation: {var.get('std')}")
        
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
        from ...doe.sampling import AdaptiveDistributionSampler
        instance.sampler = AdaptiveDistributionSampler()
        instance.visualizer = InformationVisualization()
        instance.output_dir = Path(output_dir)
        instance.output_dir.mkdir(exist_ok=True)
        
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
                    
                    # Add CoV if present
                    if hasattr(var, 'cov'):
                        var_dict["cov"] = var.cov
                        if var.cov > 0:
                            var_dict["distribution"] = getattr(var, 'distribution', 'normal')
                
                # Process env variables
                else:  # env_vars
                    var_dict["distribution"] = getattr(var, 'distribution', 'uniform')
                    
                    # Add distribution-specific parameters
                    if getattr(var, 'distribution', '') == "uniform":
                        var_dict["low"] = getattr(var, 'low', 0)
                        var_dict["high"] = getattr(var, 'high', 1)
                    elif getattr(var, 'distribution', '') == "normal":
                        var_dict["mean"] = getattr(var, 'mean', 0)
                        if hasattr(var, 'cov'):
                            var_dict["cov"] = var.cov
                        else:
                            var_dict["std"] = getattr(var, 'std', 1)
                
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

    # Fixed method to generate environmental samples properly
    def _generate_env_samples(self, var: Dict[str, Any], size: int) -> np.ndarray:
        """Generate samples for an environmental variable."""
        if var['distribution'] == 'uniform':
            return np.random.uniform(
                low=var['low'],
                high=var['high'],
                size=size
            )
        elif var['distribution'] == 'normal':
            mean = var['mean']
            std = mean * var['cov'] if 'cov' in var else var['std']
            return np.random.normal(
                loc=mean,
                scale=std,
                size=size
            )
        elif var['distribution'] == 'lognormal':
            mean = var['mean']
            cov = var['cov']
            mu = np.log(mean / np.sqrt(1 + cov**2))
            sigma = np.sqrt(np.log(1 + cov**2))
            return np.random.lognormal(
                mean=mu,
                sigma=sigma,
                size=size
            )
        else:
            raise ValueError(f"Unknown distribution: {var['distribution']}")

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
                    
                    if var.get('cov', 0) > 0:  # Uncertain design variable
                        lower, upper = var['range_bounds']
                        X_samples[:, i] = self.sampler.generate_samples(
                            distribution=var.get('distribution', 'normal'),
                            mean=base_value,
                            cov=var['cov'],
                            lower=lower,
                            upper=upper,
                            size=num_mcs_samples
                        )
                    else:  # Deterministic design variable
                        X_samples[:, i] = base_value
                    
                    design_var_idx += 1
                
            else:  # Environmental variable
                # Use our fixed method instead of the sampler's method
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







