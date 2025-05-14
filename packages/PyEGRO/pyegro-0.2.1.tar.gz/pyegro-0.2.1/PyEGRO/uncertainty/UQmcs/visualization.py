"""
Visualization module for Uncertainty Quantification.
Provides visualization tools for uncertainty analysis results.
"""

import numpy as np
import pickle
import pandas as pd
from typing import List, Dict, Any, Optional, Union, Tuple
from pathlib import Path
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy import stats

# Setting plots - Front
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Times New Roman']
rcParams['font.size'] = 16
rcParams['axes.titlesize'] = 16
rcParams['axes.labelsize'] = 16
rcParams['xtick.labelsize'] = 16
rcParams['ytick.labelsize'] = 16


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
        ax1.legend(loc='upper right')
        
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
                               cmap='jet',
                               alpha=1,
                               antialiased=True)
        
        self._format_3d_subplot(ax1, design_vars[0]['name'], design_vars[1]['name'], 
                              'Mean Response', surf1, 'Mean Value', 'Mean Response Surface')
        
        ax2 = fig.add_subplot(122, projection='3d')
        surf2 = ax2.plot_surface(x_grid, y_grid, z_std_grid,
                               cmap='jet',
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


    def create_pdf_visualization(self, 
                            design_point: Dict[str, Any], 
                            samples: np.ndarray, 
                            title: str = "Probability Density Function at Design Point",
                            filename: str = "pdf_visualization.png") -> plt.Figure:
        """
        Create PDF visualization for a specific design point.
        
        Args:
            design_point: Dictionary of design variable values
            samples: Array of samples from Monte Carlo simulation
            title: Title for the plot
            filename: Filename for saving the plot
            
        Returns:
            Matplotlib figure object
        """
        plt.close('all')
        
        # Ensure samples is a flattened 1D array
        samples = np.asarray(samples).flatten()
        
        # Compute statistics
        mean = np.mean(samples)
        std_dev = np.std(samples)
        percentiles = np.percentile(samples, [2.5, 25, 50, 75, 97.5])
        cov = std_dev / abs(mean) if mean != 0 else float('inf')
        
        # Create the figure
        fig = plt.figure(figsize=(8, 6))
        
        # Create main plotting area (left side of the figure)
        ax = plt.axes([0.1, 0.1, 0.65, 0.8])
        
        # Determine reasonable x-axis limits
        x_min = max(mean - 4*std_dev, min(samples))
        x_max = min(mean + 4*std_dev, max(samples))
        
        # Create KDE
        x_kde = np.linspace(x_min, x_max, 1000)
        kde = stats.gaussian_kde(samples)
        kde_values = kde(x_kde)
        
        # Plot the KDE curve
        ax.plot(x_kde, kde_values, 'darkblue', linewidth=2.5, label='Probability Density')
        
        # Highlight the area for 95% confidence interval
        ci_mask = (x_kde >= percentiles[0]) & (x_kde <= percentiles[4])
        ax.fill_between(x_kde[ci_mask], 0, kde_values[ci_mask], 
                    color='royalblue', alpha=0.5, 
                    label='95% Confidence Interval')
        

        # Formatting
        ax.set_title(title)
        ax.set_xlabel('Response Value')
        ax.set_ylabel('Probability Density')
        ax.grid(True, alpha=0.3, linestyle = '--')
        
        # Add legend
        ax.legend(loc='upper right', framealpha=0.9, fontsize=12)
        
        # Add statistics text box to the right side of the figure
        stats_text = (
            f"Mean: {mean:.4f}\n"
            f"Std Dev: {std_dev:.4f}\n"
            f"CoV: {cov:.4f}\n\n"
            f"95% CI: [{percentiles[0]:.4f}, {percentiles[4]:.4f}]"
        )
        
        # Create a text box for statistics on the right side
        props = dict(boxstyle='round', facecolor='white', alpha=0.9)
        fig.text(0.8, 0.5, stats_text, fontsize=12, 
                horizontalalignment='left', verticalalignment='center',
                bbox=props)
        
        # Save the figure
        plt.savefig(self.output_dir / filename, dpi=300, bbox_inches='tight')
        
        return fig

    def create_reliability_plot(self, 
                            samples: np.ndarray, 
                            threshold_values: np.ndarray, 
                            threshold_type: str = 'upper',
                            title: str = "Probability of Failure Curve",
                            filename: str = "reliability_analysis.png") -> plt.Figure:
        """
        Create reliability plot showing probability of exceedance vs threshold value.
        
        Args:
            samples: Array of samples from Monte Carlo simulation
            threshold_values: Array of threshold values to evaluate
            threshold_type: 'upper' for P(X > threshold) or 'lower' for P(X < threshold)
            title: Title for the plot
            filename: Filename for saving the plot
            
        Returns:
            Matplotlib figure object
        """
        plt.close('all')
        
        # Calculate exceedance probabilities
        exceedance_probs = np.zeros_like(threshold_values)
        
        for i, threshold in enumerate(threshold_values):
            if threshold_type == 'upper':
                exceedance_probs[i] = np.mean(samples > threshold)
            else:  # lower
                exceedance_probs[i] = np.mean(samples < threshold)
        
        # Create the figure
        fig, ax = plt.subplots(figsize=(7, 6))
        
        # Plot exceedance curve
        ax.plot(threshold_values, exceedance_probs, 'b-', linewidth=2)
        ax.fill_between(threshold_values, 0, exceedance_probs, alpha=0.3, color='royalblue')
        
        # Add simplified guidelines - only keep the most important ones
        key_probs = [0.01, 0.05, 0.5, 0.95, 0.99]
        for prob in key_probs:
            ax.axhline(y=prob, color='gray', linestyle=':', alpha=0.5)
            ax.text(threshold_values[0], prob, f"{prob:.2f}", verticalalignment='center', 
                fontsize=10, ha='right', alpha=0.7)
        
        # Formatting
        if threshold_type == 'upper':
            ax.set_ylabel('Probability of Exceedance P(X > threshold)')
            subtitle = 'Probability that response exceeds threshold value'
        else:
            ax.set_ylabel('Probability of Non-Exceedance P(X < threshold)')
            subtitle = 'Probability that response is less than threshold value'
            
        ax.set_xlabel('Threshold Value')
        ax.set_title(f"{title}\n{subtitle}")
        ax.grid(False, alpha=0.3)
        
        # Find key values (P=0.05, P=0.5, P=0.95)
        from scipy.interpolate import interp1d
        f_interp = interp1d(exceedance_probs, threshold_values, bounds_error=False, fill_value='extrapolate')
        key_thresholds = f_interp(key_probs[1:4])  # Only 0.05, 0.5, 0.95
        
        # Add key values to plot
        for prob, threshold in zip(key_probs[1:4], key_thresholds):
            ax.plot([threshold], [prob], 'ro', markersize=5)
            ax.text(threshold, prob, f" {threshold:.4f}", verticalalignment='center', fontsize=10)
        
        plt.tight_layout()
        
        # Save the figure
        plt.savefig(self.output_dir / filename, dpi=300, bbox_inches='tight')
        
        return fig


