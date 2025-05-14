"""
Sensitivity Analysis Module for PyEGRO using Monte Carlo Simulation (MCS) with Sobol method 
based on "Saltelli's sampling method" Total evaluations = N × (D + 2).
Simplified version focusing on first-order and total-order indices only.
"""

import numpy as np
import pickle
import pandas as pd
import json
import torch
from typing import Any, Optional
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib import rcParams
from SALib.analyze.sobol import analyze
from SALib.sample.sobol import sample

# Setting plots - Font
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Times New Roman']
rcParams['font.size'] = 14
rcParams['axes.titlesize'] = 14
rcParams['axes.labelsize'] = 14
rcParams['xtick.labelsize'] = 14
rcParams['ytick.labelsize'] = 14

# Suppress warnings
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


class SensitivityVisualization:
    """Handles visualization of sensitivity analysis results."""
    
    def __init__(self, output_dir=None):
        self.output_dir = Path(output_dir) if output_dir else Path('RESULT_SA')
        self.output_dir.mkdir(exist_ok=True)

    def create_visualization(self, sensitivity_df: pd.DataFrame):
        """Create visualization for sensitivity indices."""
        plt.close('all')
        
        # Create figure with 2 separate plots (one for first-order, one for total-order)
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        
        # Get parameters in original order (no sorting)
        parameters = sensitivity_df['Parameter']
        x = np.arange(len(parameters))
        
        # Set grid first (so bars appear in front)
        axes[0].grid(True, linestyle='--', alpha=0.7, zorder=0)
        axes[1].grid(True, linestyle='--', alpha=0.7, zorder=0)
        
        # First-order indices (S1) - Left plot
        axes[0].bar(x, sensitivity_df['First-order'], color='cornflowerblue', zorder=3)
        axes[0].set_xlabel('Variables')
        axes[0].set_ylabel("First-order Sobol' Indices (S1)")
        axes[0].set_xticks(x)
        axes[0].set_xticklabels(parameters, rotation=45, ha='right')
        
        # Fix y-axis between 0 and 1
        axes[0].set_ylim(0, 1.0)
        
        ## ========== Add values on top of the bars for S1
        # for i, v in enumerate(sensitivity_df['First-order']):
        #     # Adjust the text position to be either above or inside the bar depending on height
        #     if v > 0.9:  # If bar is very tall, put text inside the bar
        #         text_y = v - 0.05
        #         text_color = 'white'
        #     else:
        #         text_y = v + 0.02
        #         text_color = 'black'
            
        #     axes[0].text(i, text_y, f'{v:.3f}', ha='center', fontsize=11, color=text_color)
        
        # Total-order indices (ST) - Right plot
        axes[1].bar(x, sensitivity_df['Total-order'], color='darkblue', zorder=3)
        axes[1].set_xlabel('Variables')
        axes[1].set_ylabel("Total-order Sobol' Indices (ST)")
        axes[1].set_xticks(x)
        axes[1].set_xticklabels(parameters, rotation=45, ha='right')
        
        # Fix y-axis between 0 and 1
        axes[1].set_ylim(0, 1.0)
        
        ## ========== Add values on top of the bars for ST
        # for i, v in enumerate(sensitivity_df['Total-order']):
        #     # Adjust the text position to be either above or inside the bar depending on height
        #     if v > 0.9:  # If bar is very tall, put text inside the bar
        #         text_y = v - 0.05
        #         text_color = 'white'
        #     else:
        #         text_y = v + 0.02
        #         text_color = 'black'
                
        #     axes[1].text(i, text_y, f'{v:.3f}', ha='center', fontsize=11, color=text_color)
        
        plt.tight_layout()
        
        # Save visualizations
        plt.savefig(self.output_dir / 'sensitivity_indices.png', dpi=300, bbox_inches='tight')
        
        with open(self.output_dir / 'sensitivity_indices.fig.pkl', 'wb') as fig_file:
            pickle.dump(fig, fig_file)
            
        plt.close(fig)

class MCSSensitivityAnalysis:
    """Main class for sensitivity analysis using Monte Carlo Simulation with Sobol method."""
    
    def __init__(self, 
                 data_info_path: str = "DATA_PREPARATION/data_info.json",
                 model_handler: Optional[Any] = None,
                 true_func: Optional[callable] = None, 
                 model_path: Optional[str] = None,
                 output_dir: str = "RESULT_SA",
                 show_variables_info: bool = True,
                 random_seed: int = 42):
        """Initialize MCSSensitivityAnalysis.
        
        Args:
            data_info_path: Path to the data configuration file
            model_handler: Model handler for surrogate model (if using surrogate)
            true_func: True objective function (if using direct evaluation)
            model_path: Path to trained GPR model (if using surrogate)
            output_dir: Directory for saving results
            show_variables_info: Whether to display variable information
            random_seed: Random seed for reproducibility
        """
        if true_func is None and model_handler is None and model_path is None:
            raise ValueError("Either true_func, model_handler, or model_path must be provided")
            
        # Set random seed
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
        self.visualizer = SensitivityVisualization(output_dir=output_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Display variable information if enabled
        if self.show_variables_info:
            self.display_variable_info()
    
    def from_initial_design(cls, 
                            design=None,
                            design_infos=None,
                            true_func=None, 
                            output_dir="RESULT_SA",
                            show_variables_info=True,
                            random_seed=42):
        """
        Create MCSSensitivityAnalysis instance directly from InitialDesign object.
        
        Args:
            design: InitialDesign instance
            design_infos: Alternative name for design (backward compatibility)
            true_func: Optional override for objective function
            output_dir: Directory for saving results
            show_variables_info: Whether to display variable information
            random_seed: Random seed for reproducibility
            
        Returns:
            MCSSensitivityAnalysis instance
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
        instance.visualizer = SensitivityVisualization(output_dir=output_dir)
        instance.output_dir = Path(output_dir)
        instance.output_dir.mkdir(exist_ok=True)
        
        # Set random seed
        np.random.seed(random_seed)
        torch.manual_seed(random_seed)
        
        # Case 1: If design_obj is a dictionary with 'variables' key, use it directly
        if isinstance(design_obj, dict) and 'variables' in design_obj:
            instance.variables = design_obj['variables']
        
        # Case 2: Process Variable objects in design_obj.variables
        elif hasattr(design_obj, 'variables'):
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
        
        # Case 3: If no variables found, try design_info attribute
        elif hasattr(design_obj, 'design_info') and isinstance(design_obj.design_info, dict):
            if 'variables' in design_obj.design_info:
                instance.variables = design_obj.design_info['variables']
        
        # Display variable information if enabled
        if instance.show_variables_info:
            instance.display_variable_info()
        
        return instance
        
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

    def _evaluate_samples(self, X_samples: np.ndarray) -> np.ndarray:
        """Evaluate samples using either true function or surrogate."""
        if self.model_handler:
            mean_pred, _ = self.model_handler.predict(X_samples)
            return mean_pred
        else:
            # Handle both single sample and batch evaluation
            if len(X_samples.shape) == 1:
                # Single sample as a 1D array - reshape to 2D with one row
                return self.true_func(X_samples.reshape(1, -1)).flatten()
            else:
                # Batch of samples
                return self.true_func(X_samples)

    def _normalize_samples(self, samples: np.ndarray) -> np.ndarray:
        """Normalize samples to [-1, 1] range for SALib compatibility."""
        # Create mapping from original variable ranges to [-1, 1]
        normalized_samples = np.zeros_like(samples)
        
        for i, var in enumerate(self.variables):
            if var['vars_type'] == 'design_vars':
                # Design variables use range_bounds
                lower, upper = var['range_bounds']
            else:
                # Environmental variables use distribution parameters
                if var['distribution'] == 'uniform':
                    lower, upper = var['low'], var['high']
                elif var['distribution'] == 'normal':
                    # For normal distributions, use mean ± 3*std as bounds
                    mean = var['mean']
                    std = mean * var['cov'] if 'cov' in var else var['std']
                    lower, upper = mean - 3*std, mean + 3*std
                else:
                    # Default fallback
                    lower, upper = 0, 1
            
            # Normalize to [-1, 1]
            normalized_samples[:, i] = 2 * (samples[:, i] - lower) / (upper - lower) - 1
            
        return normalized_samples

    def _denormalize_samples(self, normalized_samples: np.ndarray) -> np.ndarray:
        """Denormalize samples from [-1, 1] range to original variable ranges."""
        denormalized_samples = np.zeros_like(normalized_samples)
        
        for i, var in enumerate(self.variables):
            if var['vars_type'] == 'design_vars':
                # Design variables use range_bounds
                lower, upper = var['range_bounds']
            else:
                # Environmental variables use distribution parameters
                if var['distribution'] == 'uniform':
                    lower, upper = var['low'], var['high']
                elif var['distribution'] == 'normal':
                    # For normal distributions, use mean ± 3*std as bounds
                    mean = var['mean']
                    std = mean * var['cov'] if 'cov' in var else var['std']
                    lower, upper = mean - 3*std, mean + 3*std
                else:
                    # Default fallback
                    lower, upper = 0, 1
            
            # Denormalize from [-1, 1]
            denormalized_samples[:, i] = (normalized_samples[:, i] + 1) / 2 * (upper - lower) + lower
            
        return denormalized_samples

    def run_analysis(self, num_samples=1024, show_progress=True):
        """
        Run the Monte Carlo-based sensitivity analysis using Sobol method.
        
        Args:
            num_samples: Base sample size for Sobol sequence generation
                        (actual number of model evaluations will be N*(D+2))
            show_progress: Whether to show progress information
            
        Returns:
            DataFrame containing the sensitivity indices
        """
        if self.show_variables_info:
            print("\nAnalysis Configuration:")
            print(f"Number of base samples: {num_samples}")
            print(f"Using surrogate model: {self.use_surrogate}")
            
            # Calculate total samples required
            n_vars = len(self.variables)
            total_samples = num_samples * (n_vars + 2)
            print(f"Total model evaluations: {total_samples}\n")
            print("\nStarting analysis...\n")
        
        # Get all variable names
        variable_names = [var['name'] for var in self.variables]
        
        # Define the problem structure for SALib - FIXING THE BOUNDS FORMAT
        problem = {
            'num_vars': len(self.variables),
            'names': variable_names,
            # Create a proper 2D array of bounds - this is the key fix
            'bounds': np.array([[-1, 1] for _ in range(len(self.variables))])
        }
        
        try:
            # Generate samples using Sobol sequence - always set calc_second_order to False
            param_values = sample(problem, num_samples, calc_second_order=False)
            
            # Denormalize samples to original variable ranges for evaluation
            X_samples = self._denormalize_samples(param_values)
            
            # Evaluate model at sample points
            if show_progress:
                print(f"Evaluating {len(X_samples)} sample points...")
                
                # Simple progress tracking
                step = max(1, len(X_samples) // 20)
                Y = np.zeros(len(X_samples))
                
                for i, x in enumerate(X_samples):
                    Y[i] = self._evaluate_samples(x.reshape(1, -1))
                    if i % step == 0 and i > 0:
                        print(f"Progress: {i/len(X_samples)*100:.1f}% ({i}/{len(X_samples)})")
            else:
                # Evaluate all at once if no progress needed
                Y = self._evaluate_samples(X_samples)
            
            # Perform Sobol sensitivity analysis
            if show_progress:
                print("\nComputing sensitivity indices...")
                
            Si = analyze(problem, Y, calc_second_order=False, print_to_console=False)
            
            # Extract sensitivity indices
            first_order = Si['S1']
            total_order = Si['ST']
            conf_first = Si['S1_conf']
            conf_total = Si['ST_conf']
            
            # Create results dataframe
            results = {
                'Parameter': variable_names,
                'First-order': first_order,
                'Total-order': total_order,
                'First-order_conf': conf_first,
                'Total-order_conf': conf_total
            }
            
            # Create DataFrame
            results_df = pd.DataFrame(results)
            
            # Save results and create visualizations
            self._save_results(results_df)
            
            if self.show_variables_info:
                print("\nAnalysis completed!")
                print(f"Results saved in: {self.output_dir}")
            
            return results_df
        
        except Exception as e:
            print(f"\nError during sensitivity analysis: {str(e)}")
            print("Detailed error information:")
            import traceback
            traceback.print_exc()
            raise
    
    def _save_results(self, results_df: pd.DataFrame):
        """Save analysis results and create visualizations."""
        # Save CSV
        results_df.to_csv(self.output_dir / 'sensitivity_analysis_results.csv', index=False)
        
        # Create visualizations
        self.visualizer.create_visualization(results_df)
        
        # Save summary statistics
        summary_stats = {
            'most_influential_parameter': results_df.loc[results_df['Total-order'].idxmax(), 'Parameter'],
            'first_order_sum': float(np.sum(results_df['First-order'])),
            'max_total_order': float(np.max(results_df['Total-order'])),
            'min_total_order': float(np.min(results_df['Total-order'])),
            'interaction_strength': float(np.sum(results_df['Total-order']) - np.sum(results_df['First-order']))
        }
        
        with open(self.output_dir / 'analysis_summary.json', 'w') as f:
            json.dump(summary_stats, f, indent=4)


def run_sensitivity_analysis(
    data_info_path: str = "DATA_PREPARATION/data_info.json",
    true_func: Optional[callable] = None,
    model_handler: Optional[Any] = None,
    model_path: Optional[str] = None,
    num_samples: int = 1024,
    output_dir: str = "RESULT_SA",
    random_seed: int = 42,
    show_progress: bool = True
) -> pd.DataFrame:
    """
    Convenience function to run Monte Carlo-based sensitivity analysis with Sobol method.
    
    Args:
        data_info_path: Path to the data configuration file
        true_func: True objective function (if using direct evaluation)
        model_handler: Model handler for surrogate model
        model_path: Path to trained GPR model (if using surrogate)
        num_samples: Base sample size for Sobol sequence generation
        output_dir: Directory for saving results
        random_seed: Random seed for reproducibility
        show_progress: Whether to show progress bar
        
    Returns:
        DataFrame containing the sensitivity indices
    """
    analysis = MCSSensitivityAnalysis(
        data_info_path=data_info_path,
        true_func=true_func,
        model_handler=model_handler,
        model_path=model_path,
        output_dir=output_dir,
        random_seed=random_seed
    )
    
    return analysis.run_analysis(
        num_samples=num_samples,
        show_progress=show_progress
    )


