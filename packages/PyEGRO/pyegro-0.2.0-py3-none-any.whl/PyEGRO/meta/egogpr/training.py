
"""
Main EGO training implementation with simplified structure.
"""

import os
import torch
import gpytorch
import numpy as np
import pandas as pd
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn
from rich.progress import TimeRemainingColumn, TimeElapsedColumn, SpinnerColumn
from rich.console import Console
from sklearn.preprocessing import StandardScaler

from .config import TrainingConfig
from .model import GPRegressionModel
from .utils import (
    setup_directories,
    evaluate_model_performance,
    get_device_info,
    calculate_regression_diagnostics,
    save_model_data,
    train_gp_model,
    save_metrics,
    save_infill_sample
)
# Import visualization classes directly
from .visualization import EGOAnimator, ModelVisualizer
from .acquisition import propose_location

class EfficientGlobalOptimization:
    """Main class for Efficient Global Optimization."""
    
    def __init__(self, 
                 objective_func,
                 bounds: np.ndarray,
                 variable_names: list,
                 config: TrainingConfig = None,
                 initial_data: pd.DataFrame = None):
        """Initialize EGO optimizer."""
        self.objective_func = objective_func
        self.bounds = bounds
        self.variable_names = variable_names
        self.config = config or TrainingConfig()
        self.device = torch.device(self.config.device)
        
        # Initialize directories and data
        setup_directories(self.config.save_dir, len(variable_names) <= 2)
        self.evaluation_metrics = pd.DataFrame()
        
        # Initialize animator if visualization is needed
        if len(variable_names) <= 2:
            self.animator = EGOAnimator(
                save_dir=os.path.join(self.config.save_dir, 'animation')
            )
        
        if initial_data is not None:
            self._initialize_data(initial_data)

    def _initialize_data(self, initial_data: pd.DataFrame):
        """Initialize training data and scalers."""
        self.n_initial_samples = len(initial_data)
        
        # Extract and scale training data
        self.X_train = initial_data[self.variable_names].values
        self.y_train = initial_data['y'].values.reshape(-1, 1)
        
        self.scaler_x = StandardScaler().fit(self.X_train)
        self.scaler_y = StandardScaler().fit(self.y_train)
        
        self.X_train_scaled = self.scaler_x.transform(self.X_train)
        self.y_train_scaled = self.scaler_y.transform(self.y_train)
        
        # Convert to tensors
        self.X_train_tensor = torch.tensor(self.X_train_scaled, dtype=torch.float32).to(self.device)
        self.y_train_tensor = torch.tensor(self.y_train_scaled.flatten(), dtype=torch.float32).to(self.device)

    def _print_summary(self, console: Console):
        """Print optimization configuration summary."""
        device_info = get_device_info()
        
        console.print("\n[red]========== Configuration Summary ==========[/red]")
        console.print("\n[green]Hardware Configuration[/green]")
        console.print(f"[white]• Device:[/white] {device_info['device_type']} - {device_info['device_name']}")
        console.print(f"[white]• CUDA Version:[/white] {device_info['cuda_version']}")
        
        console.print("\n[green]Problem Setup[/green]")
        console.print(f"[white]• Input Variables:[/white] {', '.join(self.variable_names)}")
        console.print(f"[white]• Initial Samples:[/white] {self.n_initial_samples}")
        
        console.print("\n[green]Optimization Settings[/green]")
        console.print(f"[white]• Acquisition:[/white] {self.config.acquisition_name.upper()}")
        console.print(f"[white]• Max Iterations:[/white] {self.config.max_iterations}")
        console.print(f"[white]• RMSE Threshold:[/white] {self.config.rmse_threshold}")
        console.print(f"[white]• Relative Improvement Threshold (%):[/white] {self.config.relative_improvement}")
        console.print(f"[white]• RMSE patience Threshold:[/white] {self.config.rmse_patience}")
        
        console.print("\n[green]Model Settings[/green]")
        # Map kernel names to readable descriptions
        kernel_descriptions = {
            'matern25': 'Matérn 2.5 with ARD',
            'matern15': 'Matérn 1.5 with ARD',
            'matern05': 'Matérn 0.5 with ARD',
            'rbf': 'Radial Basis Function (RBF) with ARD',
            'linear': 'Linear'
        }
        kernel_desc = kernel_descriptions.get(self.config.kernel, self.config.kernel)
        console.print(f"[white]• Kernel:[/white] {kernel_desc}")
        console.print(f"[white]• Learning Rate:[/white] {self.config.learning_rate}")
        console.print(f"[white]• Early Stopping Patience:[/white] {self.config.early_stopping_patience}")
        console.print(f"[white]• Training Iterations:[/white] {self.config.training_iter}")

        console.print("\n[red]==========================================[/red]\n")

    def _update_visualization(self, iteration: int):
        """Update visualization for current optimization state."""
        if len(self.variable_names) <= 2:
            try:
                # Move data to CPU for visualization
                X_train_cpu = self.X_train.copy()  # Already numpy array
                y_train_cpu = self.y_train.copy()  # Already numpy array
                
                # Create CPU versions of model and likelihood for visualization
                cpu_model = self.model.__class__(
                    torch.tensor(self.scaler_x.transform(X_train_cpu), dtype=torch.float32),
                    torch.tensor(self.scaler_y.transform(y_train_cpu).flatten(), dtype=torch.float32),
                    self.likelihood.__class__()
                ).cpu()
                
                cpu_model.load_state_dict({k: v.cpu() for k, v in self.model.state_dict().items()})
                cpu_likelihood = cpu_model.likelihood
                cpu_likelihood.load_state_dict({k: v.cpu() for k, v in self.likelihood.state_dict().items()})
                
                if len(self.variable_names) == 1:
                    self.animator.save_1D_frame(
                        cpu_model,
                        cpu_likelihood,
                        X_train_cpu,
                        y_train_cpu,
                        self.scaler_x,
                        self.scaler_y,
                        self.bounds,
                        iteration,
                        self.variable_names,
                        device=torch.device('cpu'),
                        true_function=self.objective_func
                    )
                else:  # 2D case
                    self.animator.save_2D_frame(
                        cpu_model,
                        cpu_likelihood,
                        X_train_cpu,
                        y_train_cpu,
                        self.scaler_x,
                        self.scaler_y,
                        self.bounds,
                        iteration,
                        self.variable_names,
                        self.n_initial_samples,
                        device=torch.device('cpu')
                    )
                
                # Create GIF if it's the final iteration
                if hasattr(self.model, 'final_iteration') and iteration >= self.model.final_iteration:
                    self.animator.create_gif(duration=1000)  # 1 second per frame for final animation
                    
            except Exception as e:
                print(f"Warning: Visualization update failed: {str(e)}")
                
            # Clear GPU memory if needed
            if self.device.type == 'cuda':
                torch.cuda.empty_cache()


    def _create_final_visualizations(self, history: dict, console: Console):
        """Create final visualizations and plots."""
        if len(self.variable_names) <= 2:
            try:
                # Create visualization instance with model and device
                visualizer = ModelVisualizer(
                    self.model,
                    self.likelihood,
                    self.scaler_x,
                    self.scaler_y,
                    self.bounds,
                    self.variable_names,
                    history,
                    self.device,
                    save_dir=self.config.save_dir
                )
                
                # Create error analysis plots
                # console.print("[cyan]Generating error analysis plots...[/cyan]")
                visualizer.plot_error_analysis(self.X_train, self.y_train)
                
                # Create convergence metrics plots
                # console.print("[cyan]Generating convergence metrics plots...[/cyan]")
                visualizer.plot_convergence_metrics(history)
                
                # Create final prediction plots based on dimension
                # console.print("[cyan]Generating final prediction plots...[/cyan]")
                visualizer.plot_final_prediction(
                    self.X_train,
                    self.y_train,
                    true_function=self.objective_func if len(self.variable_names) == 1 else None
                )
                
                # Create animation if animator exists
                if hasattr(self, 'animator'):
                    # console.print("[cyan]Creating optimization animation...[/cyan]")
                    self.animator.create_gif(duration=1000)
                
                console.print("[green]✓ Final visualizations created successfully[/green]")
                
            except Exception as e:
                console.print(f"[yellow]Warning: Final visualization creation failed: {str(e)}[/yellow]")
                import traceback
                console.print(traceback.format_exc())


    def _run_optimization(self) -> dict:
        """Run the optimization process."""
        if not hasattr(self, 'X_train'):
            raise ValueError("Data not initialized. Call initialize_data() first.")
            
        # Initialize model
        self.likelihood = gpytorch.likelihoods.GaussianLikelihood().to(self.device)
        self.model = GPRegressionModel(
            self.X_train_tensor,
            self.y_train_tensor,
            self.likelihood,
            kernel=self.config.kernel
        ).to(self.device)
        
        # Initial training
        train_gp_model(
            self.model, 
            self.likelihood, 
            self.X_train_tensor, 
            self.y_train_tensor,
            self.config
        )
        
        # Initialize tracking
        console = Console()
        if self.config.show_summary:
            self._print_summary(console)
            
        history = {
            'iterations': [],
            'X': [],
            'y': [],
            'best_y': [],
            'r2_scores': [],
            'rmse_values': [],
            'mean_uncertainty': []
        }
        
        # Initialize variables for tracking optimization progress
        best_rmse = float('inf')
        rmse_not_improved = 0
        previous_rmse = float('inf')
        current_rmse = float('inf')
        current_r2 = 0.0
        iteration = 0

        # Create final console for output after progress bar
        final_console = Console()
        
        # Main optimization loop with progress bar
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            TextColumn("[cyan]{task.fields[best_val]}"),
            TextColumn("[magenta]{task.fields[r2]}"),
            TextColumn("[yellow]{task.fields[rmse]}"),
            console=console
        ) as progress:
            task = progress.add_task(
                "[cyan]EGO Optimization",
                total=self.config.max_iterations,
                best_val="Best: N/A",
                r2="R²: N/A",
                rmse="RMSE: N/A"
            )
            
            # Main optimization loop
            for iteration in range(self.config.max_iterations):
                try:
                    # Get next point and evaluate
                    X_next = propose_location(
                        acquisition_name=self.config.acquisition_name,
                        model=self.model,
                        likelihood=self.likelihood,
                        y_train=self.y_train,
                        bounds=self.bounds,
                        scaler_x=self.scaler_x,
                        scaler_y=self.scaler_y,
                        **self.config.acquisition_params
                    )
                    y_next = self.objective_func(X_next).reshape(-1, 1)
                    
                    # Save infill point
                    save_infill_sample(X_next, y_next, self.variable_names, self.config.save_dir)
                    
                    # Update training data
                    self.X_train = np.vstack((self.X_train, X_next))
                    self.y_train = np.vstack((self.y_train, y_next))
                    
                    self.X_train_scaled = self.scaler_x.transform(self.X_train)
                    self.y_train_scaled = self.scaler_y.transform(self.y_train)
                    
                    self.X_train_tensor = torch.tensor(
                        self.X_train_scaled, 
                        dtype=torch.float32
                    ).to(self.device)
                    self.y_train_tensor = torch.tensor(
                        self.y_train_scaled.flatten(), 
                        dtype=torch.float32
                    ).to(self.device)
                    
                    # Retrain model
                    self.model.set_train_data(self.X_train_tensor, self.y_train_tensor, strict=False)
                    train_gp_model(
                        self.model, 
                        self.likelihood, 
                        self.X_train_tensor, 
                        self.y_train_tensor,
                        self.config
                    )
                    
                    # Get predictions and calculate metrics
                    self.model.eval()
                    with torch.no_grad(), gpytorch.settings.fast_pred_var():
                        predictions = self.likelihood(self.model(self.X_train_tensor))
                        y_pred = self.scaler_y.inverse_transform(
                            predictions.mean.cpu().numpy().reshape(-1, 1)
                        )
                        y_std = (predictions.variance.sqrt().cpu().numpy().reshape(-1, 1) * 
                                self.scaler_y.scale_)
                    
                    # Calculate metrics
                    metrics = evaluate_model_performance(
                        self.model, 
                        self.likelihood,
                        self.X_train_tensor,
                        self.y_train_tensor
                    )
                    current_rmse = metrics['rmse']
                    current_r2 = metrics['r2']
                    
                    # Save metrics including actual and predicted values
                    save_metrics(
                        self.evaluation_metrics,
                        iteration + 1,
                        self.config.acquisition_name,
                        current_rmse,
                        current_r2,
                        np.min(self.y_train),
                        float(np.mean(y_std)),
                        self.y_train,
                        y_pred,
                        self.config.save_dir
                    )
                    
                    # Update history
                    history['iterations'].append(iteration + 1)
                    history['X'].append(X_next)
                    history['y'].append(y_next)
                    history['best_y'].append(np.min(self.y_train))
                    history['r2_scores'].append(current_r2)
                    history['rmse_values'].append(current_rmse)
                    history['mean_uncertainty'].append(float(np.mean(y_std)))
                    
                    # Update visualization for 1D/2D cases
                    if len(self.variable_names) <= 2:
                        self._update_visualization(iteration + 1)
                    
                    # Update progress
                    progress.update(
                        task,
                        advance=1,
                        best_val=f"Best: {np.min(self.y_train):.6f}",
                        r2=f"R²: {current_r2:.4f}",
                        rmse=f"RMSE: {current_rmse:.4f}"
                    )
                    
                    # Check improvement and stopping criteria
                    relative_change = ((previous_rmse - current_rmse) / previous_rmse 
                                    if previous_rmse != float('inf') else float('inf'))
                    
                    if relative_change > (self.config.relative_improvement):
                        best_rmse = current_rmse
                        rmse_not_improved = 0
                    else:
                        rmse_not_improved += 1
                    previous_rmse = current_rmse
                    
                    # Check stopping criteria
                    if current_rmse <= self.config.rmse_threshold:
                        final_console.print("\n[red]===========> Optimization Stopped[/red]")
                        final_console.print(f"[white]✓ RMSE threshold met: {current_rmse:.4f} ≤ "
                                    f"{self.config.rmse_threshold}[/white]")
                        break
                        
                    if rmse_not_improved >= self.config.rmse_patience:
                        final_console.print("\n[red]===========> Optimization Stopped[/red]")
                        final_console.print(f"[white]• No improvement for {self.config.rmse_patience} "
                                    f"iterations[/white]")
                        final_console.print(f"[white]• Final RMSE: {current_rmse:.4f}[/white]")
                        break
                        
                except Exception as e:
                    final_console.print(f"\n[red]Error in iteration {iteration}: {str(e)}[/red]")
                    break

        # Now create visualizations after progress bar is closed
        try:
            # final_console.print("\n[cyan]Creating final visualizations...[/cyan]")
            
            # Create visualization instance
            visualizer = ModelVisualizer(
                self.model,
                self.likelihood,
                self.scaler_x,
                self.scaler_y,
                self.bounds,
                self.variable_names,
                history,
                self.device,
                save_dir=self.config.save_dir
            )
            
            # Create dimension-independent plots
            # final_console.print("[cyan]Generating error analysis plots...[/cyan]")
            visualizer.plot_error_analysis(self.X_train, self.y_train)
            
            # final_console.print("[cyan]Generating convergence metrics plots...[/cyan]")
            visualizer.plot_convergence_metrics(history)
            
            # Create dimension-dependent visualizations only for 1D/2D cases
            if len(self.variable_names) <= 2:
                # final_console.print("[cyan]Generating final prediction plots...[/cyan]")
                self._create_final_visualizations(history, final_console)
                
                if hasattr(self, 'animator'):
                    # final_console.print("[cyan]Creating optimization animation...[/cyan]")
                    self.animator.create_gif(duration=1000)
            
            final_console.print("[green]✓ Visualizations saved successfully[/green]")
            
            # Save model and associated data
            save_model_data(
                self.model,
                self.likelihood,
                {'X': self.scaler_x, 'y': self.scaler_y},
                {
                    'variable_names': self.variable_names,
                    'bounds': self.bounds.tolist(),
                    'acquisition_name': self.config.acquisition_name,
                    'n_initial_samples': self.n_initial_samples
                },
                self.config.save_dir
            )
            
            # Print final results summary
            final_console.print("\n[red]=========== Final Results ===========[/red]")
            final_console.print(f"[white]• Best value found: {np.min(self.y_train):.6f}[/white]")
            final_console.print(f"[white]• Final RMSE: {current_rmse:.4f}[/white]")
            final_console.print(f"[white]• Final R² Score: {current_r2:.4f}[/white]")
            final_console.print(f"[white]• Total iterations: {iteration + 1}[/white]")
            final_console.print("[red]=====================================[/red]\n")
            
        except Exception as e:
            final_console.print(f"[red]Error in finalization: {str(e)}[/red]")
            final_console.print(f"[yellow]Traceback:[/yellow]")
            import traceback
            final_console.print(traceback.format_exc())

        return history



    def run(self) -> dict:
        """Alias for run_optimization."""
        return self._run_optimization()





