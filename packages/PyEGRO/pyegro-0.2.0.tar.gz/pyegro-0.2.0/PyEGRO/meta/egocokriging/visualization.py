
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from sklearn.metrics import r2_score
import os
from PIL import Image
import torch
import gpytorch
from typing import List, Optional, Dict, Any, Union
from matplotlib import rcParams
from matplotlib.colors import LinearSegmentedColormap


# Create plots
rcParams['font.family'] = 'Serif'
rcParams['font.serif'] = 'Times New Roman'
rcParams['font.size'] = 18
rcParams['axes.titlesize'] = 18
rcParams['axes.labelsize'] = 18
rcParams['xtick.labelsize'] = 18
rcParams['ytick.labelsize'] = 18


class EGOAnimator:
    def __init__(self, save_dir: str = 'RESULT_MODEL_COKRIGING/animation', frame_duration: int = 500):
        self.save_dir = save_dir
        self.frames_dir = f'{save_dir}/frames'
        self.frames = []  # Initialize frames list
        self.frame_duration = frame_duration
        os.makedirs(self.frames_dir, exist_ok=True)
        self.device = torch.device('cpu')  # Always use CPU for visualization

    def _prepare_model_for_prediction(self, model, likelihood):
        """Prepare model and likelihood for prediction on CPU."""
        model = model.cpu()
        likelihood = likelihood.cpu()
        model.eval()
        likelihood.eval()
        return model, likelihood

    def _batch_predict(self, model, likelihood, X_batch, scaler_x, scaler_y, fidelity=1):
        """Make predictions for a batch of points."""
        X_scaled = scaler_x.transform(X_batch)
        
        # Check if model is multi-fidelity
        is_multi_fidelity = hasattr(model.covar_module, 'rho')
        
        if is_multi_fidelity:
            # Add fidelity column
            fidelity_col = np.ones((X_scaled.shape[0], 1)) * fidelity
            X_scaled = np.hstack((X_scaled, fidelity_col))
        
        X_tensor = torch.tensor(X_scaled, dtype=torch.float32).to(self.device)
        
        with torch.no_grad(), gpytorch.settings.fast_pred_var():
            predictions = likelihood(model(X_tensor))
            mean = predictions.mean.numpy()
            std = predictions.variance.sqrt().numpy() if hasattr(predictions, 'variance') else None
            
        return mean, std

    def save_2D_frame(self,
                    model: gpytorch.models.ExactGP,
                    likelihood: gpytorch.likelihoods.GaussianLikelihood,
                    X_train: np.ndarray,
                    y_train: np.ndarray,
                    scaler_x: object,
                    scaler_y: object,
                    bounds: np.ndarray,
                    iteration: int,
                    variable_names: List[str],
                    n_initial_samples: int,
                    n_points: int = 50,
                    batch_size: int = 1000,
                    device: torch.device = None,
                    fidelities: Optional[np.ndarray] = None):
        """Save a 2D visualization frame with memory-efficient computation."""
        frame_path = os.path.join(self.frames_dir, f'frame_{iteration:04d}.png')
        
        try:
            # Prepare model for prediction
            model, likelihood = self._prepare_model_for_prediction(model, likelihood)
            
            # Check if model is multi-fidelity
            is_multi_fidelity = hasattr(model.covar_module, 'rho')
            
            # Create mesh grid
            x1 = np.linspace(bounds[0, 0], bounds[0, 1], n_points)
            x2 = np.linspace(bounds[1, 0], bounds[1, 1], n_points)
            X1, X2 = np.meshgrid(x1, x2)
            X_test = np.vstack((X1.flatten(), X2.flatten())).T
            
            # Process predictions in batches
            mean_predictions = np.zeros(len(X_test))
            
            for i in range(0, len(X_test), batch_size):
                batch_end = min(i + batch_size, len(X_test))
                X_batch = X_test[i:batch_end]
                
                # Always use high fidelity for predictions
                batch_mean, _ = self._batch_predict(model, likelihood, X_batch, scaler_x, scaler_y, fidelity=1)
                mean_predictions[i:batch_end] = batch_mean
            
            # Transform predictions back to original scale
            mean_predictions = scaler_y.inverse_transform(mean_predictions.reshape(-1, 1)).flatten()
            mean_predictions = mean_predictions.reshape(n_points, n_points)
            
            # Create the plot
            fig, ax = plt.subplots(figsize=(8, 6))
            cf = ax.contourf(X1, X2, mean_predictions, levels=20, cmap='jet')
            
            # Filter to use high fidelity points only if multi-fidelity
            if is_multi_fidelity and fidelities is not None:
                # Find high fidelity points (treat as the ones to display)
                high_fid_mask = fidelities.flatten() >= 0.5
                display_X = X_train[high_fid_mask]
                n_initial_high = sum(high_fid_mask[:n_initial_samples])
                
                # Plot initial samples (high fidelity)
                if n_initial_high > 0:
                    initial_indices = np.where(high_fid_mask[:n_initial_samples])[0]
                    ax.scatter(X_train[initial_indices, 0], X_train[initial_indices, 1], 
                            c='black', s=70, label='Initial samples')
                
                # Plot added samples (high fidelity)
                if len(display_X) > n_initial_high:
                    added_indices = np.where(high_fid_mask[n_initial_samples:-1])[0] + n_initial_samples
                    if len(added_indices) > 0:
                        ax.scatter(X_train[added_indices, 0], X_train[added_indices, 1],
                                c='white', s=70, edgecolors='black', label='Added samples')
                
                # Latest sample (if high fidelity)
                if fidelities[-1][0] >= 0.5:
                    ax.scatter(X_train[-1, 0], X_train[-1, 1], c='red', s=80, label='Latest sample')
            else:
                # Original behavior for single fidelity or all points
                ax.scatter(X_train[:n_initial_samples, 0], X_train[:n_initial_samples, 1], 
                        c='black', s=70, label='Initial samples')
                
                if len(X_train) > n_initial_samples:
                    ax.scatter(X_train[n_initial_samples:-1, 0], X_train[n_initial_samples:-1, 1],
                            c='white', s=70, edgecolors='black', label='Added samples')
                
                ax.scatter(X_train[-1, 0], X_train[-1, 1], c='red', s=80, label='Latest sample')
            
            ax.set_xlabel(variable_names[0])
            ax.set_ylabel(variable_names[1])
            ax.set_title(f'Model Prediction - Iteration {iteration}')
            plt.colorbar(cf, label='Predicted Value')
            
            # Only add legend entries that exist
            handles, labels = ax.get_legend_handles_labels()
            if handles:
                ax.legend(loc='upper right')
            
            plt.tight_layout()
            plt.savefig(frame_path, facecolor='white', edgecolor='none', 
                       bbox_inches='tight', dpi=150)
            plt.close()
            
            self.frames.append(frame_path)
            
        except Exception as e:
            print(f"Error in save_2D_frame: {str(e)}")
            plt.close()
            raise
            
        finally:
            # Clean up
            torch.cuda.empty_cache() if torch.cuda.is_available() else None


    def save_1D_frame(self, 
                        model: gpytorch.models.ExactGP,
                        likelihood: gpytorch.likelihoods.GaussianLikelihood,
                        X_train: np.ndarray,
                        y_train: np.ndarray,
                        scaler_x: object,
                        scaler_y: object,
                        bounds: np.ndarray,
                        iteration: int,
                        variable_names: List[str],
                        device: torch.device = None,
                        true_function: Optional[callable] = None,
                        batch_size: int = 1000,
                        fidelities: Optional[np.ndarray] = None):
        """Save a 1D visualization frame with memory-efficient computation."""
        frame_path = os.path.join(self.frames_dir, f'frame_{iteration:04d}.png')
        
        try:
            # Prepare model for prediction
            model, likelihood = self._prepare_model_for_prediction(model, likelihood)
            
            # Check if model is multi-fidelity
            is_multi_fidelity = hasattr(model.covar_module, 'rho')
            
            # Generate test points
            X_test = np.linspace(bounds[0, 0], bounds[0, 1], 200).reshape(-1, 1)
            
            # Initialize arrays for predictions
            mean_predictions = np.zeros(len(X_test))
            std_predictions = np.zeros(len(X_test))
            
            # Process predictions in batches
            for i in range(0, len(X_test), batch_size):
                batch_end = min(i + batch_size, len(X_test))
                X_batch = X_test[i:batch_end]
                
                # Always use high fidelity predictions (fidelity=1)
                batch_mean, batch_std = self._batch_predict(model, likelihood, X_batch, scaler_x, scaler_y, fidelity=1)
                mean_predictions[i:batch_end] = batch_mean.flatten()  # Ensure 1D array
                std_predictions[i:batch_end] = batch_std.flatten() if batch_std is not None else 0
            
            # Transform predictions back to original scale
            mean_predictions = scaler_y.inverse_transform(mean_predictions.reshape(-1, 1)).flatten()
            std_predictions = std_predictions * scaler_y.scale_  # Remove reshape here
            
            # Determine number of subplots
            if is_multi_fidelity and hasattr(model.covar_module, 'rho'):
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))
                fig.suptitle(f'Model Prediction - Iteration {iteration}', fontsize=14)
                
                # Add rho value to title
                current_rho = float(model.covar_module.rho.detach().cpu().numpy())
                subtitle = f'Co-Kriging Model (ρ = {current_rho:.4f})'
                fig.text(0.5, 0.91, subtitle, ha='center', fontsize=12)

            else:
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))
                fig.suptitle(f'Model Prediction - Iteration {iteration}', fontsize=14)
            
            # Plot prediction with uncertainty
            ax1.plot(X_test.flatten(), mean_predictions, 'b-', label='Prediction', linewidth=2)
            ax1.fill_between(X_test.flatten(), 
                        mean_predictions - 2 * std_predictions,  # Keep as 1D arrays
                        mean_predictions + 2 * std_predictions, 
                        color='b', alpha=0.2, label='95% Confidence')
            
            # Filter to high fidelity points only if multi-fidelity
            if is_multi_fidelity and fidelities is not None:
                # Use only high fidelity points for visualization
                high_fid_mask = fidelities.flatten() >= 0.5
                high_X = X_train[high_fid_mask]
                high_y = y_train[high_fid_mask]
                
                ax1.scatter(high_X, high_y, c='r', marker='o', label='Training Points', zorder=5, s=50)
                
                if iteration > 0 and fidelities[-1][0] >= 0.5:
                    ax1.scatter(X_train[-1:], y_train[-1:], c='g', marker='*', s=200, 
                             label='Latest Point', zorder=6)
            else:
                # Original behavior - show all points
                ax1.scatter(X_train, y_train, c='r', marker='o', label='Training Points', zorder=5, s=50)
                
                if iteration > 0:
                    ax1.scatter(X_train[-1:], y_train[-1:], c='g', marker='*', s=200, 
                             label='Latest Point', zorder=6)
            
            if true_function is not None and callable(true_function):
                try:
                    y_true = true_function(X_test)
                    ax1.plot(X_test, y_true, 'g--', label='True Function', linewidth=2)
                except Exception as e:
                    print(f"Warning: Error plotting true function - {str(e)}")
            
            ax1.set_xlabel(variable_names[0])
            ax1.set_ylabel('Response')
            ax1.legend(fontsize=10)
            ax1.grid(True, alpha=0.3)
            
            # Plot uncertainty
            ax2.plot(X_test.flatten(), std_predictions, 'r-', label='Uncertainty', linewidth=2)
            if iteration > 0:
                ax2.axvline(X_train[-1], color='g', linestyle='--', alpha=0.5)
            ax2.set_xlabel(variable_names[0])
            ax2.set_ylabel('Prediction Uncertainty')
            ax2.legend(fontsize=10)
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(frame_path, bbox_inches='tight', dpi=150)
            plt.close()
            
            self.frames.append(frame_path)
            
        except Exception as e:
            print(f"Error in save_1D_frame: {str(e)}")
            plt.close()
            raise
            
        finally:
            # Clean up
            torch.cuda.empty_cache() if torch.cuda.is_available() else None


    def create_gif(self, duration: Optional[int] = None):
        """Create GIF animation from saved frames with error handling.
        
        Args:
            duration: Duration for each frame in milliseconds. If None, uses default frame_duration
        """
        try:
            if not self.frames:
                print("No frames found to create animation")
                return
                
            # Use provided duration or default
            gif_duration = duration if duration is not None else self.frame_duration
            
            frames = []
            for frame_path in sorted(self.frames):
                if os.path.exists(frame_path):
                    try:
                        frames.append(Image.open(frame_path))
                    except Exception as e:
                        print(f"Warning: Could not open frame {frame_path}: {str(e)}")
                        continue
            
            if frames:
                output_path = os.path.join(self.save_dir, 'optimization_progress.gif')
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                try:
                    frames[0].save(
                        output_path,
                        save_all=True,
                        append_images=frames[1:],
                        duration=gif_duration,
                        loop=0
                    )
                    #print(f"Animation saved to {output_path} with frame duration {gif_duration}ms")
                except Exception as e:
                    print(f"Error saving animation: {str(e)}")
            else:
                print("No valid frames found to create animation")
                
        except Exception as e:
            print(f"Error creating animation: {str(e)}")














class ModelVisualizer:
    """Handles final model visualization and assessment with multi-fidelity support."""
    def __init__(self, model, likelihood, scaler_x, scaler_y, bounds, variable_names, history,
                 device, save_dir='RESULT_MODEL_COKRIGING', multi_fidelity=False, rho_history=None):
        self.model = model
        self.likelihood = likelihood
        self.scaler_x = scaler_x
        self.scaler_y = scaler_y
        self.bounds = bounds
        self.variable_names = variable_names
        self.device = device
        self.history = history
        self.save_dir = save_dir
        self.multi_fidelity = multi_fidelity
        self.rho_history = rho_history
        
        os.makedirs(save_dir, exist_ok=True)
        os.makedirs(os.path.join(save_dir, 'plots'), exist_ok=True)  
        
        # Ensure model and likelihood are on the correct device
        self.model = self.model.to(self.device)
        self.likelihood = self.likelihood.to(self.device)
    
    def predict(self, X, fidelity=1):
        """Make predictions with the model."""
        self.model.eval()
        self.likelihood.eval()
        
        X_scaled = self.scaler_x.transform(X)
        
        # Add fidelity indicator if model requires it
        if self.multi_fidelity:
            fidelity_col = np.ones((X_scaled.shape[0], 1)) * fidelity
            X_scaled = np.hstack((X_scaled, fidelity_col))
            
        X_tensor = torch.tensor(X_scaled, dtype=torch.float32).to(self.device)
        
        with torch.no_grad(), gpytorch.settings.fast_pred_var():
            predictions = self.likelihood(self.model(X_tensor))
            mean = predictions.mean.cpu().numpy()
            std = predictions.variance.sqrt().cpu().numpy()
            
        mean = self.scaler_y.inverse_transform(mean.reshape(-1, 1))
        std = std.reshape(-1, 1) * self.scaler_y.scale_
        
        return mean, std
    
    def plot_rho_evolution(self):
        """Plot the evolution of rho parameter over iterations with integer x-axis ticks."""
        if not self.multi_fidelity or self.rho_history is None or len(self.rho_history) == 0:
            return
        
        plt.figure(figsize=(7, 6))
        iterations = range(1, len(self.rho_history) + 1)
        plt.plot(iterations, self.rho_history, 'k-s', linewidth=2)
        
        # Set integer ticks on x-axis
        ax = plt.gca()
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        
        plt.xlabel('Iteration')
        plt.ylabel('Scaling factor')
        plt.title('Evolution of Co-Kriging Correlation Parameter (Rho)')
        plt.grid(True, alpha=0.3, linestyle='--')
        
        # # Add horizontal line at the final rho value
        # final_rho = self.rho_history[-1]
        # plt.axhline(y=final_rho, color='r', linestyle='--', 
        #         label=f'Final value: {final_rho:.4f}')
        
        #plt.legend()
        
        plt.tight_layout()
        
        # Save plot
        plot_path = os.path.join(self.save_dir, 'plots', 'rho_evolution.png')
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
            
    def _plot_1D_final(self, X_train, y_train, true_function=None, n_points=200, fidelities=None):
        """Create final 1D prediction plot with multi-fidelity support."""
        plt.figure(figsize=(12, 8))
        
        # Generate test points
        X_test = np.linspace(self.bounds[0, 0], self.bounds[0, 1], n_points).reshape(-1, 1)
        
        # Get high-fidelity predictions
        mean, std = self.predict(X_test, fidelity=1)
        
        plt.plot(X_test, mean, 'b-', label='High Fidelity Prediction', linewidth=2)
        plt.fill_between(X_test.flatten(), 
                        (mean - 2 * std).flatten(), 
                        (mean + 2 * std).flatten(), 
                        color='b', alpha=0.2, label='95% Confidence')
        
        # If multi-fidelity, also get low-fidelity predictions
        if self.multi_fidelity and fidelities is not None:
            low_mean, low_std = self.predict(X_test, fidelity=0)
            plt.plot(X_test, low_mean, 'g--', label='Low Fidelity Prediction', linewidth=1.5)
        
        # Plot data points with different markers/colors based on fidelity
        if self.multi_fidelity and fidelities is not None:
            # Split data by fidelity
            low_fid_mask = fidelities.flatten() < 0.5
            high_fid_mask = ~low_fid_mask
            
            # Plot low fidelity points
            if np.any(low_fid_mask):
                plt.scatter(X_train[low_fid_mask], y_train[low_fid_mask], 
                         c='green', marker='o', edgecolors='black',
                         label='Low Fidelity Data', s=60, zorder=4)
            
            # Plot high fidelity points
            if np.any(high_fid_mask):
                plt.scatter(X_train[high_fid_mask], y_train[high_fid_mask], 
                         c='red', marker='s',
                         label='High Fidelity Data', s=60, zorder=5)
        else:
            # Standard plot for single fidelity
            plt.scatter(X_train, y_train, c='r', marker='o', label='Training Points')
        
        if true_function is not None:
            y_true = true_function(X_test)
            plt.plot(X_test, y_true, 'k-.', label='True Function')
        
        plt.xlabel(self.variable_names[0])
        plt.ylabel('Response')
        plt.title('Final Model Prediction')
        plt.legend()
        plt.grid(True, alpha=0.3, linestyle='--')
        
        save_path = os.path.join(self.save_dir, 'plots', 'final_prediction_1d.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()

    def plot_final_prediction(self, X_train, y_train, true_function=None, fidelities=None):
        """Create final prediction plots."""
        if len(self.variable_names) == 1:
            self._plot_1D_final(X_train, y_train, true_function, fidelities=fidelities)
        elif len(self.variable_names) == 2:
            self._plot_2D_final(X_train, y_train, fidelities=fidelities)

    def _plot_2D_final(self, X_train, y_train, n_points=50, fidelities=None):
        """Create final 2D prediction plot with multi-fidelity support."""
        x1 = np.linspace(self.bounds[0, 0], self.bounds[0, 1], n_points)
        x2 = np.linspace(self.bounds[1, 0], self.bounds[1, 1], n_points)
        X1, X2 = np.meshgrid(x1, x2)
        X_test = np.vstack((X1.flatten(), X2.flatten())).T
        
        # Get high-fidelity predictions
        mean, std = self.predict(X_test, fidelity=1)
        Y_pred = mean.reshape(n_points, n_points)
        Y_std = std.reshape(n_points, n_points)
        
        fig = plt.figure(figsize=(20, 8))
        
        # Prediction surface
        ax1 = fig.add_subplot(121, projection='3d')
        surf1 = ax1.plot_surface(X1, X2, Y_pred, cmap='jet')
        
        # # Plot data points with different markers/colors based on fidelity
        # if self.multi_fidelity and fidelities is not None:
        #     # Split data by fidelity
        #     low_fid_mask = fidelities.flatten() < 0.5
        #     high_fid_mask = ~low_fid_mask
            
        #     # Plot low fidelity points if any
        #     if np.any(low_fid_mask):
        #         ax1.scatter(X_train[low_fid_mask, 0], X_train[low_fid_mask, 1], 
        #                  y_train[low_fid_mask], c='green', marker='o', s=50,
        #                  label='Low Fidelity Data')
            
        #     # Plot high fidelity points if any
        #     if np.any(high_fid_mask):
        #         ax1.scatter(X_train[high_fid_mask, 0], X_train[high_fid_mask, 1], 
        #                  y_train[high_fid_mask], c='red', marker='s', s=50,
        #                  label='High Fidelity Data')
        # else:
        #     # Standard plot for single fidelity
        #     ax1.scatter(X_train[:, 0], X_train[:, 1], y_train, c='r', marker='o')
        
        ax1.set_xlabel(self.variable_names[0])
        ax1.set_ylabel(self.variable_names[1])
        ax1.set_zlabel('Response')
        ax1.set_title('Final Prediction Surface')
        plt.colorbar(surf1, ax=ax1)
        
        # Uncertainty surface
        ax2 = fig.add_subplot(122, projection='3d')
        surf2 = ax2.plot_surface(X1, X2, Y_std, cmap='jet')
        
        # # Plot data points on the uncertainty surface
        # if self.multi_fidelity and fidelities is not None:
        #     # Plot with zero z-coordinate (on the surface)
        #     if np.any(low_fid_mask):
        #         ax2.scatter(X_train[low_fid_mask, 0], X_train[low_fid_mask, 1], 
        #                  np.zeros_like(y_train[low_fid_mask]), c='green', marker='o', s=50)
            
        #     if np.any(high_fid_mask):
        #         ax2.scatter(X_train[high_fid_mask, 0], X_train[high_fid_mask, 1], 
        #                  np.zeros_like(y_train[high_fid_mask]), c='red', marker='s', s=50)
        # else:
        #     ax2.scatter(X_train[:, 0], X_train[:, 1], np.zeros_like(y_train), c='r', marker='o')
        
        ax2.set_xlabel(self.variable_names[0])
        ax2.set_ylabel(self.variable_names[1])
        ax2.set_zlabel('Uncertainty (std)')
        ax2.set_title('Final Prediction Uncertainty')
        plt.colorbar(surf2, ax=ax2)
        
        plt.tight_layout()
        save_path = os.path.join(self.save_dir, 'plots', 'final_prediction_2d.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()


    def plot_convergence_metrics(self, history: dict):
        """Plot optimization metrics over iterations."""
        # Only show RMSE and rho plots
        if self.multi_fidelity and 'rho_values' in history and len(history['rho_values']) > 0:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        else:
            fig, ax1 = plt.subplots(1, 1, figsize=(8, 6))
        
        iterations = history['iterations']
        
        # Plot RMSE evolution
        ax1.plot(iterations, history['rmse_values'], 'k-s', linewidth=2)
        ax1.set_xlabel('Iteration')
        ax1.set_ylabel('RMSE')
        ax1.set_title('RMSE Evolution')
        ax1.grid(True, alpha=0.3, linestyle='--')

        # Set integer ticks on x-axis for RMSE plot
        ax1.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        
        # Plot rho evolution if multi-fidelity
        if self.multi_fidelity and 'rho_values' in history and len(history['rho_values']) > 0:
            ax2.plot(iterations, history['rho_values'], 'b-s', linewidth=2)
            ax2.set_xlabel('Iteration')
            ax2.set_ylabel('Scaling factor')
            ax2.set_title('Co-Kriging Correlation Evolution')
            ax2.grid(True, alpha=0.3, linestyle='--')
            ax2.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

        
        plt.tight_layout()
        save_path = os.path.join(self.save_dir, 'plots', 'convergence_metrics.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()


    def plot_error_analysis(self, X_train, y_train, fidelities=None):
        """Plot prediction errors and residuals with separate plots for high and low fidelity data."""
        # Get predictions for training points using high fidelity
        y_pred, y_std = self.predict(X_train, fidelity=1)
        
        # Determine layout based on multi-fidelity
        if self.multi_fidelity and fidelities is not None:
            # Create layout with separate plots for high and low fidelity
            fig, ((ax_high_actual, ax_low_actual), (ax_high_resid, ax_low_resid)) = plt.subplots(2, 2, figsize=(12, 12))
            
            # Split data by fidelity
            low_fid_mask = fidelities.flatten() < 0.5
            high_fid_mask = ~low_fid_mask
            
            # Check if we have both fidelity types
            have_low = np.any(low_fid_mask)
            have_high = np.any(high_fid_mask)
            
            # Prepare data - high fidelity
            if have_high:
                high_x_train = X_train[high_fid_mask]
                high_y_train = y_train[high_fid_mask]
                high_y_pred = y_pred[high_fid_mask]
                high_residuals = high_y_train - high_y_pred
            
            # Prepare data - low fidelity
            if have_low:
                low_x_train = X_train[low_fid_mask]
                low_y_train = y_train[low_fid_mask]
                low_y_pred = y_pred[low_fid_mask]
                low_residuals = low_y_train - low_y_pred
            
            # High fidelity - Actual vs Predicted
            if have_high:
                ax_high_actual.scatter(high_y_train, high_y_pred, c='blue', edgecolors='black', s=70, alpha=0.7)
                min_val = min(high_y_train.min(), high_y_pred.min())
                max_val = max(high_y_train.max(), high_y_pred.max())
                ax_high_actual.plot([min_val, max_val], [min_val, max_val], 'k--')
                ax_high_actual.set_xlabel('Actual Values')
                ax_high_actual.set_ylabel('Predicted Values')
                ax_high_actual.set_title('High Fidelity: Actual vs Predicted')
                
                # Add R² score
                r2_high = r2_score(high_y_train, high_y_pred)
                ax_high_actual.text(0.05, 0.95, f'R² = {r2_high:.4f}', 
                                transform=ax_high_actual.transAxes, fontsize=14,
                                bbox=dict(facecolor='white', alpha=0.7))
            else:
                ax_high_actual.text(0.5, 0.5, 'No high fidelity data',
                                horizontalalignment='center', verticalalignment='center',
                                transform=ax_high_actual.transAxes)
            ax_high_actual.grid(True, alpha=0.3, linestyle='--' )
            
            # Low fidelity - Actual vs Predicted
            if have_low:
                ax_low_actual.scatter(low_y_train, low_y_pred, c='green', edgecolors='black', s=70, alpha=0.7)
                min_val = min(low_y_train.min(), low_y_pred.min())
                max_val = max(low_y_train.max(), low_y_pred.max())
                ax_low_actual.plot([min_val, max_val], [min_val, max_val], 'k--')
                ax_low_actual.set_xlabel('Actual Values')
                ax_low_actual.set_ylabel('Predicted Values')
                ax_low_actual.set_title('Low Fidelity: Actual vs Predicted')
                
                # Add R² score
                r2_low = r2_score(low_y_train, low_y_pred)
                ax_low_actual.text(0.05, 0.95, f'R² = {r2_low:.4f}', 
                                transform=ax_low_actual.transAxes, fontsize=14,
                                bbox=dict(facecolor='white', alpha=0.7))
            else:
                ax_low_actual.text(0.5, 0.5, 'No low fidelity data',
                                horizontalalignment='center', verticalalignment='center',
                                transform=ax_low_actual.transAxes)
            ax_low_actual.grid(True, alpha=0.3, linestyle='--')
            
            # High fidelity - Residuals
            if have_high:
                ax_high_resid.scatter(high_y_pred, high_residuals, edgecolor='black', c='blue', s=70, alpha=0.7)
                ax_high_resid.axhline(y=0, color='r', linestyle='--')
                ax_high_resid.set_xlabel('Predicted Values')
                ax_high_resid.set_ylabel('Residuals')
                ax_high_resid.set_title('High Fidelity: Residuals')
                
                # Add RMSE
                rmse_high = np.sqrt(np.mean(high_residuals**2))
                ax_high_resid.text(0.05, 0.95, f'RMSE = {rmse_high:.4f}', 
                                transform=ax_high_resid.transAxes, fontsize=12,
                                bbox=dict(facecolor='white', alpha=0.7))
            else:
                ax_high_resid.text(0.5, 0.5, 'No high fidelity data',
                                horizontalalignment='center', verticalalignment='center',
                                transform=ax_high_resid.transAxes)
            ax_high_resid.grid(True, alpha=0.3, linestyle='--')
            
            # Low fidelity - Residuals
            if have_low:
                ax_low_resid.scatter(low_y_pred, low_residuals, edgecolor='black', c='green', s=70, alpha=0.7)
                ax_low_resid.axhline(y=0, color='r', linestyle='--')
                ax_low_resid.set_xlabel('Predicted Values')
                ax_low_resid.set_ylabel('Residuals')
                ax_low_resid.set_title('Low Fidelity: Residuals')
                
                # Add RMSE
                rmse_low = np.sqrt(np.mean(low_residuals**2))
                ax_low_resid.text(0.05, 0.95, f'RMSE = {rmse_low:.4f}', 
                                transform=ax_low_resid.transAxes, fontsize=12,
                                bbox=dict(facecolor='white', alpha=0.7))
            else:
                ax_low_resid.text(0.5, 0.5, 'No low fidelity data',
                                horizontalalignment='center', verticalalignment='center',
                                transform=ax_low_resid.transAxes)
            ax_low_resid.grid(True, alpha=0.3, linestyle='--')
            
        else:
            # Standard 1×2 layout for single fidelity
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
            
            # Actual vs Predicted
            ax1.scatter(y_train, y_pred, edgecolor='black', c='b', alpha=0.7, s=70)
            ax1.plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], 'r--')
            ax1.set_xlabel('Actual Values')
            ax1.set_ylabel('Predicted Values')
            ax1.set_title('Actual vs Predicted')
            
            # Add R² score
            r2 = r2_score(y_train, y_pred)
            ax1.text(0.05, 0.95, f'R² = {r2:.4f}', 
                transform=ax1.transAxes, fontsize=12,
                bbox=dict(facecolor='white', alpha=0.7))
            ax1.grid(True, alpha=0.3, linestyle='--')
            
            # Residuals vs Predicted
            residuals = y_train - y_pred
            ax2.scatter(y_pred, residuals, edgecolor='black', c='b', alpha=0.7, s=70)
            ax2.axhline(y=0, color='r', linestyle='--')
            ax2.set_xlabel('Predicted Values')
            ax2.set_ylabel('Residuals')
            ax2.set_title('Residuals vs Predicted')
            
            # Add RMSE
            rmse = np.sqrt(np.mean(residuals**2))
            ax2.text(0.05, 0.95, f'RMSE = {rmse:.4f}', 
                transform=ax2.transAxes, fontsize=12,
                bbox=dict(facecolor='white', alpha=0.7))
            ax2.grid(True, alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        save_path = os.path.join(self.save_dir, 'plots', 'error_analysis.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()