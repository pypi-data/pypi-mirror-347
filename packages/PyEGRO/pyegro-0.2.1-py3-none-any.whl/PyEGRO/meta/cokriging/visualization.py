import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import pandas as pd
import os

# Plot settings for professional visualization
rcParams['font.family'] = 'Serif'
rcParams['font.serif'] = 'Times New Roman'
rcParams['font.size'] = 16
rcParams['axes.titlesize'] = 16
rcParams['axes.labelsize'] = 16
rcParams['xtick.labelsize'] = 16
rcParams['ytick.labelsize'] = 16
rcParams['legend.fontsize'] = 16
rcParams['figure.titlesize'] = 18




def visualize_cokriging(meta, X_low, y_low, X_high, y_high, X_test=None, y_test=None, 
                       variable_names=None, bounds=None, savefig=False, output_dir=None):
    """
    Create comprehensive visualizations for Co-Kriging model performance.
    
    Args:
        meta: Trained MetaTrainingCoKriging instance
        X_low: Low-fidelity inputs
        y_low: Low-fidelity targets
        X_high: High-fidelity inputs
        y_high: High-fidelity targets
        X_test: Test inputs (optional)
        y_test: Test targets (optional)
        variable_names: Names of input variables (optional)
        bounds: Bounds of input variables for sampling (optional)
        savefig: Whether to save figures to disk
        output_dir: Directory to save figures (default: None, uses meta.output_dir)
        
    Returns:
        Dict of figure handles
    """
    
    # Setup output directory
    if output_dir is None:
        output_dir = os.path.join(meta.output_dir, 'visualizations')
    os.makedirs(output_dir, exist_ok=True)
    
    # Dictionary to store figure handles
    figures = {}
    
    # Ensure data is in the right format
    if isinstance(X_low, pd.DataFrame):
        X_low = X_low.values
    if isinstance(y_low, pd.DataFrame) or isinstance(y_low, pd.Series):
        y_low = y_low.values
    if isinstance(X_high, pd.DataFrame):
        X_high = X_high.values
    if isinstance(y_high, pd.DataFrame) or isinstance(y_high, pd.Series):
        y_high = y_high.values
    
    if X_test is not None and y_test is not None:
        if isinstance(X_test, pd.DataFrame):
            X_test = X_test.values
        if isinstance(y_test, pd.DataFrame) or isinstance(y_test, pd.Series):
            y_test = y_test.values
    
    # Ensure y is 2D
    if len(y_low.shape) == 1:
        y_low = y_low.reshape(-1, 1)
    if len(y_high.shape) == 1:
        y_high = y_high.reshape(-1, 1)
    if y_test is not None and len(y_test.shape) == 1:
        y_test = y_test.reshape(-1, 1)
    
    # Set variable names if not provided
    if variable_names is None and hasattr(meta, 'variable_names'):
        variable_names = meta.variable_names
    elif variable_names is None:
        variable_names = [f'X{i+1}' for i in range(X_low.shape[1])]
    
    # Make predictions
    y_low_pred, y_low_std = meta.predict(X_low, fidelity='low')
    y_high_pred, y_high_std = meta.predict(X_high, fidelity='high')
    
    # Calculate metrics
    low_rmse = np.sqrt(np.mean((y_low - y_low_pred) ** 2))
    high_rmse = np.sqrt(np.mean((y_high - y_high_pred) ** 2))
    
    R2_low = 1 - np.sum((y_low - y_low_pred) ** 2) / np.sum((y_low - np.mean(y_low)) ** 2)
    R2_high = 1 - np.sum((y_high - y_high_pred) ** 2) / np.sum((y_high - np.mean(y_high)) ** 2)
    
    if X_test is not None and y_test is not None:
        y_test_pred, y_test_std = meta.predict(X_test, fidelity='high')
        test_rmse = np.sqrt(np.mean((y_test - y_test_pred) ** 2))
        R2_test = 1 - np.sum((y_test - y_test_pred) ** 2) / np.sum((y_test - np.mean(y_test)) ** 2)
    
    # Figure 1: Actual vs Predicted
    cols = 3 if X_test is not None else 2
    fig1, axes = plt.subplots(1, cols, figsize=(cols*5, 5))
    
    # Low fidelity
    ax = axes[0]
    ax.scatter(y_low, y_low_pred, c='blue', s=50, alpha=0.7)
    
    min_val = min(y_low.min(), y_low_pred.min())
    max_val = max(y_low.max(), y_low_pred.max())
    ax.plot([min_val, max_val], [min_val, max_val], 'k--')
    
    ax.set_xlabel('Actual Values')
    ax.set_ylabel('Predicted Values')
    ax.set_title(f'Low Fidelity\nR² = {R2_low:.4f}, RMSE = {low_rmse:.4f}')
    ax.grid(True, alpha=0.3)
    
    # High fidelity
    ax = axes[1]
    ax.scatter(y_high, y_high_pred, c='red', s=50, alpha=0.7)
    
    min_val = min(y_high.min(), y_high_pred.min())
    max_val = max(y_high.max(), y_high_pred.max())
    ax.plot([min_val, max_val], [min_val, max_val], 'k--')
    
    ax.set_xlabel('Actual Values')
    ax.set_ylabel('Predicted Values')
    ax.set_title(f'High Fidelity\nR² = {R2_high:.4f}, RMSE = {high_rmse:.4f}')
    ax.grid(True, alpha=0.3)
    
    # Test data if available
    if X_test is not None and y_test is not None:
        ax = axes[2]
        ax.scatter(y_test, y_test_pred, c='green', s=50, alpha=0.7)
        
        min_val = min(y_test.min(), y_test_pred.min())
        max_val = max(y_test.max(), y_test_pred.max())
        ax.plot([min_val, max_val], [min_val, max_val], 'k--')
        
        ax.set_xlabel('Actual Values')
        ax.set_ylabel('Predicted Values')
        ax.set_title(f'Test Data\nR² = {R2_test:.4f}, RMSE = {test_rmse:.4f}')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    figures['actual_vs_predicted'] = fig1
    
    if savefig:
        fig1.savefig(os.path.join(output_dir, 'actual_vs_predicted.png'), dpi=300, bbox_inches='tight')
    
    # R² comparison plot
    fig2 = plt.figure(figsize=(8, 6))
    
    # Data for bar plot
    categories = ['Low Fidelity', 'High Fidelity']
    values = [float(R2_low), float(R2_high)]
    colors = ['blue', 'red']
    
    if X_test is not None and y_test is not None:
        categories.append('Test Data')
        values.append(float(R2_test))
        colors.append('green')
    
    # Create bar plot
    bars = plt.bar(categories, values, color=colors, alpha=0.7)
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.4f}', ha='center', va='bottom', fontsize=12)
    
    plt.ylim(0, 1.1)
    plt.xlabel('Model Type')
    plt.ylabel('R² Score')
    plt.title('Co-Kriging Model Performance')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    figures['r2_comparison'] = fig2
    
    if savefig:
        fig2.savefig(os.path.join(output_dir, 'r2_comparison.png'), dpi=300, bbox_inches='tight')
    
    # Create response surface based on input dimension
    input_dim = X_low.shape[1]
    
    if input_dim == 1:
        fig3 = _create_1d_viz(meta, X_low, y_low, X_high, y_high, X_test, y_test, 
                           variable_names, bounds, output_dir, savefig)
        figures['response_surface'] = fig3
    elif input_dim == 2:
        fig3 = _create_2d_viz(meta, X_low, y_low, X_high, y_high, X_test, y_test, 
                           variable_names, bounds, output_dir, savefig)
        figures['response_surface'] = fig3
    
    return figures


def _create_1d_viz(meta, X_low, y_low, X_high, y_high, X_test, y_test, 
                  variable_names, bounds, output_dir, savefig):
    """Create 1D visualization for Co-Kriging model."""
    import matplotlib.pyplot as plt
    import numpy as np
    import os
    
    fig = plt.figure(figsize=(8, 6))
    
    # Determine bounds
    if bounds is not None:
        x_min, x_max = bounds[0]
    else:
        all_x = np.vstack([X_low, X_high])
        if X_test is not None:
            all_x = np.vstack([all_x, X_test])
        x_min = all_x.min() - 0.1 * (all_x.max() - all_x.min())
        x_max = all_x.max() + 0.1 * (all_x.max() - all_x.min())
    
    # Create grid for visualization
    x_grid = np.linspace(x_min, x_max, 200).reshape(-1, 1)
    
    # Get predictions
    y_low_pred, y_low_std = meta.predict(x_grid, fidelity='low')
    y_high_pred, y_high_std = meta.predict(x_grid, fidelity='high')
    
    # Plot predictions with uncertainty
    plt.plot(x_grid, y_high_pred, 'r-', linewidth=2, label='High-fidelity prediction')
    plt.fill_between(x_grid.flatten(), 
                    (y_high_pred - 2*y_high_std).flatten(), 
                    (y_high_pred + 2*y_high_std).flatten(), 
                    alpha=0.2, color='red')
    
    plt.plot(x_grid, y_low_pred, 'b--', linewidth=1.5, label='Low-fidelity prediction')
    plt.fill_between(x_grid.flatten(), 
                    (y_low_pred - 2*y_low_std).flatten(), 
                    (y_low_pred + 2*y_low_std).flatten(), 
                    alpha=0.1, color='blue')
    
    # Plot data points
    plt.scatter(X_high, y_high, c='red', s=60, label='High-fidelity data', 
               marker='o', edgecolor='black', zorder=5)
    plt.scatter(X_low, y_low, c='blue', s=40, label='Low-fidelity data', 
               marker='s', alpha=0.7, zorder=4)
    
    if X_test is not None and y_test is not None:
        plt.scatter(X_test, y_test, c='green', s=70, label='Test data', 
                   marker='^', edgecolor='black', zorder=6)
    
    plt.xlabel(variable_names[0])
    plt.ylabel('Response')
    plt.title('1D Co-Kriging Response Surface')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend()
    
    plt.tight_layout()
    
    if savefig:
        plt.savefig(os.path.join(output_dir, '1d_response_surface.png'), dpi=300, bbox_inches='tight')
    
    return fig


def _create_2d_viz(meta, X_low, y_low, X_high, y_high, X_test, y_test, 
                  variable_names, bounds, output_dir, savefig):
    """Create 2D visualization for Co-Kriging model."""
    import matplotlib.pyplot as plt
    import numpy as np
    import os
    from matplotlib import cm
    
    fig = plt.figure(figsize=(10, 8))
    
    # Determine bounds
    if bounds is not None:
        x1_min, x1_max = bounds[0]
        x2_min, x2_max = bounds[1]
    else:
        all_x = np.vstack([X_low, X_high])
        if X_test is not None:
            all_x = np.vstack([all_x, X_test])
        
        x1_min, x2_min = all_x.min(axis=0) - 0.1 * (all_x.max(axis=0) - all_x.min(axis=0))
        x1_max, x2_max = all_x.max(axis=0) + 0.1 * (all_x.max(axis=0) - all_x.min(axis=0))
    
    # Create grid for visualization
    n_grid = 50
    x1 = np.linspace(x1_min, x1_max, n_grid)
    x2 = np.linspace(x2_min, x2_max, n_grid)
    X1, X2 = np.meshgrid(x1, x2)
    
    # Prepare grid points for prediction
    grid_points = np.column_stack([X1.flatten(), X2.flatten()])
    
    # Get high-fidelity predictions
    Z_pred, Z_std = meta.predict(grid_points, fidelity='high')
    Z_pred = Z_pred.reshape(X1.shape)
    
    # Create contour plot
    contour = plt.contourf(X1, X2, Z_pred, 20, cmap='viridis', alpha=0.8)
    plt.colorbar(contour, label='Predicted Response')
    
    # Add contour lines
    contour_lines = plt.contour(X1, X2, Z_pred, 10, colors='k', linewidths=0.5, alpha=0.5)
    plt.clabel(contour_lines, inline=True, fontsize=10, fmt='%.2f')
    
    # Plot data points
    plt.scatter(X_high[:, 0], X_high[:, 1], c='red', s=80, label='High-fidelity data', 
               marker='o', edgecolor='black', zorder=5)
    plt.scatter(X_low[:, 0], X_low[:, 1], c='blue', s=60, label='Low-fidelity data', 
               marker='s', alpha=0.7, zorder=4)
    
    if X_test is not None and y_test is not None:
        plt.scatter(X_test[:, 0], X_test[:, 1], c='green', s=100, label='Test data', 
                   marker='^', edgecolor='black', zorder=6)
    
    plt.xlabel(variable_names[0])
    plt.ylabel(variable_names[1])
    plt.title('2D Co-Kriging Response Surface')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend(loc='upper left')
    
    plt.tight_layout()
    
    if savefig:
        plt.savefig(os.path.join(output_dir, '2d_response_surface.png'), dpi=300, bbox_inches='tight')
    
    return fig



