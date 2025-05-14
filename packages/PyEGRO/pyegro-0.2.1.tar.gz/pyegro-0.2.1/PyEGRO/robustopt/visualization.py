"""
Visualization and display utilities for PyEGRO robust optimization.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.ticker import FormatStrFormatter
import pandas as pd
from typing import List, Dict, Optional

# Set plotting style
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Times New Roman']
rcParams['font.size'] = 14
rcParams['axes.titlesize'] = 16
rcParams['axes.labelsize'] = 14
rcParams['xtick.labelsize'] = 14
rcParams['ytick.labelsize'] = 14

class ParameterInformationDisplay:
    """Handles the display of parameter information before optimization."""
    
    @staticmethod
    def print_variable_information(variables: List[Dict]):
        """Display detailed information about all variables."""
        print("\nVariable Information Summary:")
        print("=" * 80)
        
        design_vars = []
        env_vars = []
        
        for var in variables:
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


class OptimizationVisualizer:
    """Handles visualization of optimization results."""
    
    def __init__(self, save_dir: str):
        """Initialize visualizer with save directory."""
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)

    def plot_pareto_front(self, pareto_front: np.ndarray):
        """Plot the Pareto front showing mean vs standard deviation."""
        fig, ax = plt.subplots(figsize=(6, 5), tight_layout=True)
        
        ax.scatter(pareto_front[:, 0], pareto_front[:, 1], 
                  color='b', edgecolors='k', s=30, marker='s')
        ax.set_xlabel('Mean Performance')
        ax.set_ylabel('Standard Deviation')
        ax.grid(True, linestyle='--')
        
        #ax.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
        #ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        
        plt.savefig(os.path.join(self.save_dir, 'pareto_front.png'), dpi=300)
        plt.close()

    def plot_decision_variables(self, pareto_set: np.ndarray, 
                              variable_names: List[str]):
        """Plot the distribution of decision variables in the Pareto set."""
        n_vars = pareto_set.shape[1]
        fig, axs = plt.subplots(n_vars, 1, figsize=(10, 2*n_vars), 
                               tight_layout=True)
        
        if n_vars == 1:
            axs = [axs]
        
        for i, ax in enumerate(axs):
            ax.scatter(pareto_set[:, i], np.zeros_like(pareto_set[:, i]),
                      color='blue', edgecolors='k', s=30,
                      label=f'Decision Variable: {variable_names[i]}')
            ax.set_xlabel(f'Value of {variable_names[i]}')
            ax.set_yticks([0])
            ax.grid(True, linestyle='--')
            ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        
        plt.savefig(os.path.join(self.save_dir, 'pareto_set.png'), dpi=300)
        plt.close()


    def plot_convergence(self, n_evals: List[int], metric_values: List[float], 
                         metric_type: str = 'hv'):
        """Plot convergence history of the optimization metric.
        
        Args:
            n_evals: List of evaluation numbers
            metric_values: List of metric values
            metric_type: Type of metric (e.g., 'hv' for hypervolume)
        """
        plt.figure(figsize=(8, 6))
        # plt.plot(n_evals, metric_values, 
        #         'b-', marker='o', markersize=5, markevery=5,
        #         label=f"{metric_type.upper()} Value")

        plt.plot(n_evals, metric_values, 'b-')
        
        plt.xlabel('Number of Evaluations')
        plt.ylabel(f"{metric_type.upper()} Value")
        plt.title(f"{metric_type.upper()} Convergence History")
        plt.grid(True, linestyle='--', alpha=0.7)


        plt.savefig(os.path.join(self.save_dir, 'convergence_plot.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()

    def create_all_visualizations(self, results_df: pd.DataFrame, 
                                convergence_history: Optional[Dict] = None):
        """Create all visualizations for optimization results.
        
        Args:
            results_df: DataFrame containing Pareto solutions
            convergence_history: Optional dictionary containing convergence data
        """
        # Plot Pareto front and decision variables
        pareto_front = results_df[['Mean', 'StdDev']].values
        variable_columns = [col for col in results_df.columns 
                          if col not in ['Mean', 'StdDev']]
        pareto_set = results_df[variable_columns].values
        
        self.plot_pareto_front(pareto_front)
        self.plot_decision_variables(pareto_set, variable_columns)
        
        # Plot convergence history if available
        if convergence_history is not None:
            self.plot_convergence(
                n_evals=convergence_history['n_evals'],
                metric_values=convergence_history['metric_values'],
                metric_type=convergence_history['metric_type']
            )

