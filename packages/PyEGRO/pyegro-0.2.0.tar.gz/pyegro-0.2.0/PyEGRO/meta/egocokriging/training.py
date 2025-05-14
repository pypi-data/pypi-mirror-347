"""
Main EGO training implementation with Co-Kriging support for multi-fidelity optimization.
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
from .model import CoKrigingModel
from .utils import (
    setup_directories,
    evaluate_model_performance,
    get_device_info,
    calculate_regression_diagnostics,
    save_model_data,
    train_ck_model,
    save_metrics,
    save_infill_sample,
    check_rho_convergence,
    prepare_data_with_fidelity
)
# Import visualization classes directly
from .visualization import EGOAnimator, ModelVisualizer
from .acquisition import propose_location

class EfficientGlobalOptimization:
    """Main class for Efficient Global Optimization with multi-fidelity support."""
    
    def __init__(self, 
                 objective_func,
                 bounds: np.ndarray,
                 variable_names: list,
                 config: TrainingConfig = None,
                 initial_data: pd.DataFrame = None,
                 low_fidelity_func = None):
        """Initialize EGO optimizer.
        
        Args:
            objective_func: High-fidelity objective function
            bounds: Bounds for each variable [min, max]
            variable_names: Names of input variables
            config: Training configuration
            initial_data: Initial data points (with optional 'fidelity' column)
            low_fidelity_func: Low-fidelity objective function (optional)
        """
        self.objective_func = objective_func
        self.low_fidelity_func = low_fidelity_func
        self.bounds = bounds
        self.variable_names = variable_names
        self.config = config or TrainingConfig()
        self.device = torch.device(self.config.device)
        
        # Keep track of rho values for convergence checking
        self.rho_history = []
        
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
        """Initialize training data and scalers.
        
        Args:
            initial_data: DataFrame with input variables, target ('y'), and optionally 'fidelity'
        """
        self.n_initial_samples = len(initial_data)
        
        # Check if fidelity column exists, otherwise assume all high fidelity
        if 'fidelity' not in initial_data.columns:
            initial_data['fidelity'] = 1  # Default to high fidelity
            
        # Extract training data
        self.X_train = initial_data[self.variable_names].values
        self.y_train = initial_data['y'].values.reshape(-1, 1)
        self.fidelities = initial_data['fidelity'].values.reshape(-1, 1)
        
        # Setup scalers for input and output
        self.scaler_x = StandardScaler().fit(self.X_train)
        self.scaler_y = StandardScaler().fit(self.y_train)
        
        # Scale the data
        self.X_train_scaled = self.scaler_x.transform(self.X_train)
        self.y_train_scaled = self.scaler_y.transform(self.y_train)
        
        # For Co-Kriging, we need to include fidelity indicator in input
        if self.config.multi_fidelity:
            self.X_train_with_fidelity = np.hstack((self.X_train_scaled, self.fidelities))
            self.X_train_tensor = torch.tensor(self.X_train_with_fidelity, dtype=torch.float32).to(self.device)
        else:
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
        
        # Map kernel names to readable descriptions
        kernel_descriptions = {
            'matern25': 'Matérn 2.5 with ARD',
            'matern15': 'Matérn 1.5 with ARD',
            'matern05': 'Matérn 0.5 with ARD',
            'rbf': 'Radial Basis Function (RBF) with ARD'
        }
        kernel_desc = kernel_descriptions.get(self.config.kernel, self.config.kernel)
        
        console.print("\n[green]Model Settings[/green]")
        console.print(f"[white]• Kernel:[/white] {kernel_desc}")
        console.print(f"[white]• Learning Rate:[/white] {self.config.learning_rate}")
        console.print(f"[white]• Early Stopping Patience:[/white] {self.config.early_stopping_patience}")
        console.print(f"[white]• Training Iterations:[/white] {self.config.training_iter}")
        
        if self.config.multi_fidelity:
            console.print("\n[green]Multi-Fidelity Settings[/green]")
            console.print(f"[white]• Multi-fidelity Enabled:[/white] Yes")
            console.print(f"[white]• Rho Threshold:[/white] {self.config.rho_threshold}")
            console.print(f"[white]• Rho Patience:[/white] {self.config.rho_patience}")

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
                    torch.tensor(self.X_train_tensor.cpu().numpy(), dtype=torch.float32),
                    torch.tensor(self.y_train_scaled.flatten(), dtype=torch.float32),
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
                        true_function=self.objective_func,
                        fidelities=self.fidelities if self.config.multi_fidelity else None
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
                        device=torch.device('cpu'),
                        fidelities=self.fidelities if self.config.multi_fidelity else None
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
                    save_dir=self.config.save_dir,
                    multi_fidelity=self.config.multi_fidelity,
                    rho_history=self.rho_history if self.config.multi_fidelity else None
                )
                
                # Create error analysis plots
                visualizer.plot_error_analysis(self.X_train, self.y_train, self.fidelities if self.config.multi_fidelity else None)
                
                # Create convergence metrics plots
                visualizer.plot_convergence_metrics(history)
                
                # Create final prediction plots based on dimension
                visualizer.plot_final_prediction(
                    self.X_train,
                    self.y_train,
                    true_function=self.objective_func if len(self.variable_names) == 1 else None,
                    fidelities=self.fidelities if self.config.multi_fidelity else None
                )
                
                # Create animation if animator exists
                if hasattr(self, 'animator'):
                    self.animator.create_gif(duration=1000)
                
                console.print("[green]✓ Final visualizations created successfully[/green]")
                
            except Exception as e:
                console.print(f"[yellow]Warning: Final visualization creation failed: {str(e)}[/yellow]")
                import traceback
                console.print(traceback.format_exc())

    def _decide_fidelity(self) -> int:
        """Decide which fidelity to use for the next evaluation.
        
        In this implementation, we always use high fidelity (1) because 
        we're tracking rho convergence separately.
        
        Returns:
            Fidelity level (0 for low, 1 for high)
        """
        return 1  # Always use high fidelity

    def _run_optimization(self) -> dict:
        """Run the optimization process with multi-fidelity support.
        
        Returns:
            Dictionary containing optimization history
        """
        if not hasattr(self, 'X_train'):
            raise ValueError("Data not initialized. Call initialize_data() first.")
            
        # Initialize model
        self.likelihood = gpytorch.likelihoods.GaussianLikelihood().to(self.device)
        
        # Use CoKrigingModel
        self.model = CoKrigingModel(
            self.X_train_tensor,
            self.y_train_tensor,
            self.likelihood,
            kernel=self.config.kernel
        ).to(self.device)
        
        # Initial training using appropriate training function
        if self.config.multi_fidelity:
            current_rho = train_ck_model(
                self.model,
                self.likelihood,
                self.X_train_tensor,
                self.y_train_tensor,
                self.config
            )
            self.rho_history.append(current_rho)
        else:
            train_ck_model(
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
        
        if self.config.multi_fidelity:
            history['rho_values'] = []
        
        # Initialize variables for tracking optimization progress
        best_rmse = float('inf')
        rmse_not_improved = 0
        previous_rmse = float('inf')
        current_rmse = float('inf')
        current_r2 = 0.0
        iteration = 0
        rho_converged = False

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
            *(
                [TextColumn("[green]{task.fields[rho]}")] 
                if self.config.multi_fidelity else []
            ),
            console=console
        ) as progress:
            task = progress.add_task(
                "[cyan]EGO Optimization",
                total=self.config.max_iterations,
                best_val="Best: N/A",
                r2="R²: N/A",
                rmse="RMSE: N/A",
                **({"rho": "Rho: N/A"} if self.config.multi_fidelity else {})
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
                    
                    # Decide which fidelity to use
                    fidelity = self._decide_fidelity()
                    
                    # Evaluate function
                    if fidelity == 1 or self.low_fidelity_func is None:
                        y_next = self.objective_func(X_next).reshape(-1, 1)
                    else:
                        y_next = self.low_fidelity_func(X_next).reshape(-1, 1)
                    
                    # Save infill point
                    save_infill_sample(X_next, y_next, self.variable_names, self.config.save_dir, fidelity)
                    
                    # Update training data
                    self.X_train = np.vstack((self.X_train, X_next))
                    self.y_train = np.vstack((self.y_train, y_next))
                    self.fidelities = np.vstack((self.fidelities, np.array([[fidelity]])))
                    
                    self.X_train_scaled = self.scaler_x.transform(self.X_train)
                    self.y_train_scaled = self.scaler_y.transform(self.y_train)
                    
                    if self.config.multi_fidelity:
                        self.X_train_with_fidelity = np.hstack((self.X_train_scaled, self.fidelities))
                        self.X_train_tensor = torch.tensor(
                            self.X_train_with_fidelity, 
                            dtype=torch.float32
                        ).to(self.device)
                    else:
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
                    
                    # Use appropriate training function
                    current_rho = None
                    if self.config.multi_fidelity:
                        current_rho = train_ck_model(
                            self.model,
                            self.likelihood,
                            self.X_train_tensor,
                            self.y_train_tensor,
                            self.config
                        )
                        self.rho_history.append(current_rho)
                        
                        # Check for rho convergence
                        rho_converged = check_rho_convergence(self.rho_history, self.config)
                    else:
                        train_ck_model(
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
                        self.config.save_dir,
                        rho=current_rho if self.config.multi_fidelity else None
                    )
                    
                    # Update history
                    history['iterations'].append(iteration + 1)
                    history['X'].append(X_next)
                    history['y'].append(y_next)
                    history['best_y'].append(np.min(self.y_train))
                    history['r2_scores'].append(current_r2)
                    history['rmse_values'].append(current_rmse)
                    history['mean_uncertainty'].append(float(np.mean(y_std)))
                    
                    if self.config.multi_fidelity and current_rho is not None:
                        history['rho_values'].append(current_rho)
                    
                    # Update visualization for 1D/2D cases
                    if len(self.variable_names) <= 2:
                        self._update_visualization(iteration + 1)
                    
                    # Update progress
                    progress_update = {
                        'advance': 1,
                        'best_val': f"Best: {np.min(self.y_train):.6f}",
                        'r2': f"R²: {current_r2:.4f}",
                        'rmse': f"RMSE: {current_rmse:.4f}"
                    }
                    
                    if self.config.multi_fidelity and current_rho is not None:
                        progress_update['rho'] = f"Rho: {current_rho:.4f}"
                        
                    progress.update(task, **progress_update)
                    
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
                        
                    if self.config.multi_fidelity and rho_converged:
                        final_console.print("\n[red]===========> Optimization Partially Converged[/red]")
                        final_console.print(f"[white]• Rho parameter converged: {current_rho:.4f}[/white]")
                        final_console.print(f"[white]• Continuing with fixed correlation model[/white]")
                                    
                except Exception as e:
                    final_console.print(f"\n[red]Error in iteration {iteration}: {str(e)}[/red]")
                    break

        # Create visualizations after progress bar is closed
        try:
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
                save_dir=self.config.save_dir,
                multi_fidelity=self.config.multi_fidelity,
                rho_history=self.rho_history if self.config.multi_fidelity else None
            )
            
            # Create dimension-independent plots
            visualizer.plot_error_analysis(
                self.X_train, 
                self.y_train, 
                self.fidelities if self.config.multi_fidelity else None
            )
            
            visualizer.plot_convergence_metrics(history)

            visualizer.plot_rho_evolution()
            
            # Create dimension-dependent visualizations only for 1D/2D cases
            if len(self.variable_names) <= 2:
                self._create_final_visualizations(history, final_console)
                
                if hasattr(self, 'animator'):
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
                    'n_initial_samples': self.n_initial_samples,
                    'multi_fidelity': self.config.multi_fidelity,
                    'rho_history': self.rho_history if self.config.multi_fidelity else None
                },
                self.config.save_dir
            )
            
            # Print final results summary
            final_console.print("\n[red]=========== Final Results ===========[/red]")
            final_console.print(f"[white]• Best value found: {np.min(self.y_train):.6f}[/white]")
            final_console.print(f"[white]• Final RMSE: {current_rmse:.4f}[/white]")
            final_console.print(f"[white]• Final R² Score: {current_r2:.4f}[/white]")
            
            if self.config.multi_fidelity and current_rho is not None:
                final_console.print(f"[white]• Final Rho value: {current_rho:.4f}[/white]")
                
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