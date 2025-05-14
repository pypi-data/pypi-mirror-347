
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.ticker import FormatStrFormatter
from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.lhs import LHS
from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting
from pymoo.indicators.hv import HV
import torch
import torch.nn as nn
import gpytorch
import json
import joblib
import time
from typing import List, Dict, Tuple, Union, Optional
from ...doe.sampling import AdaptiveDistributionSampler

# Set plotting style
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = 'Times New Roman'
rcParams['font.size'] = 14
rcParams['axes.titlesize'] = 16
rcParams['axes.labelsize'] = 14
rcParams['xtick.labelsize'] = 14
rcParams['ytick.labelsize'] = 14


# Suppress warning GP
import warnings
from gpytorch.utils.warnings import GPInputWarning
warnings.filterwarnings("ignore", category=GPInputWarning)


class ANNModel(nn.Module):
    """Neural Network Model Class."""
    def __init__(self, input_size: int, hidden_layers: List[int], 
                 output_size: int, activation: nn.Module):
        super().__init__()
        layers = []
        for i, units in enumerate(hidden_layers):
            layers.append(nn.Linear(input_size if i == 0 else hidden_layers[i-1], units))
            layers.append(activation)
        layers.append(nn.Linear(hidden_layers[-1], output_size))
        self.model = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)

class DeviceAgnosticHandler:
    """Unified handler for metamodels with device management"""
    def __init__(self, model_type='gpr', model_path=None, prefer_gpu=False):
        self.model_type = model_type.lower()  # 'gpr', 'cokriging', etc.
        self.model_path = model_path or f'RESULT_MODEL_{self.model_type.upper()}'
        self.prefer_gpu = prefer_gpu
        self.device = self._get_device()
        
        # Model components
        self.model = None
        self.scaler_X = None
        self.scaler_y = None
        
        # ANN components
        self.ann_mean = None
        self.ann_std = None
        self.scaler_X_ann = None
        self.scaler_y_mean = None
        self.scaler_y_std = None
        
        # Problem information
        self.variable_names = None
        self.input_bound = None
        self.variables = None
        self.data_info = None
        
        self._print_device_info()
    
    def _get_device(self) -> torch.device:
        """Determine appropriate device"""
        if self.prefer_gpu and torch.cuda.is_available():
            return torch.device("cuda")
        return torch.device("cpu")
    
    def _print_device_info(self):
        if self.device.type == "cuda":
            device_name = torch.cuda.get_device_name(0)
            memory_gb = torch.cuda.get_device_properties(0).total_memory / 1024**3
            print(f"\nUsing GPU: {device_name}")
            print(f"GPU Memory: {memory_gb:.1f} GB")
            print(f"CUDA Version: {torch.version.cuda}")
        else:
            import psutil
            import cpuinfo  # Need to install: pip install py-cpuinfo
            
            # Get clean CPU name using cpuinfo
            cpu_info = cpuinfo.get_cpu_info()
            device_name = cpu_info.get('brand_raw', 'Unknown CPU')  # This will show like "Intel(R) Core(TM) i9-13900K"
            
            memory_gb = psutil.virtual_memory().total / 1024**3
            print(f"\nUsing CPU: {device_name}")
            print(f"System Memory: {memory_gb:.1f} GB")
        
        print(f"PyTorch Version: {torch.__version__}")
        print(f"GPyTorch Version: {gpytorch.__version__}\n")

    def _load_data_info(self):
        """Load problem information"""
        with open('DATA_PREPARATION/data_info.json', 'r') as f:
            self.data_info = json.load(f)
        
        # Get design variables information
        design_vars = [var for var in self.data_info['variables'] 
                      if var['vars_type'] == 'design_vars']
        
        self.variables = design_vars
        self.variable_names = [var['name'] for var in design_vars]
        self.input_bound = [var['range_bounds'] for var in design_vars]

    def _load_scalers(self):
        """Load all scalers"""
        # Metamodel scalers
        self.scaler_X = joblib.load(f'{self.model_path}/scaler_X.pkl')
        self.scaler_y = joblib.load(f'{self.model_path}/scaler_y.pkl')
        
        # ANN scalers
        self.scaler_X_ann = joblib.load('RESULT_MODEL_ANN/scaler_X_stage2.pkl')
        self.scaler_y_mean = joblib.load('RESULT_MODEL_ANN/scaler_y_mean_stage2.pkl')
        self.scaler_y_std = joblib.load('RESULT_MODEL_ANN/scaler_y_std_stage2.pkl')

    def load_models(self) -> bool:
        """Load both metamodel and ANN models"""
        try:
            # Load problem information first
            self._load_data_info()
            
            # Load scalers
            self._load_scalers()
            
            # Load models
            print("\n****** Handle Model Loading:")
            
            # Load the appropriate model based on model_type
            success_metamodel = False
            
            if self.model_type == 'gpr':
                from ...meta.gpr import gpr_utils
                self.model = gpr_utils.DeviceAgnosticGPR(prefer_gpu=self.prefer_gpu)
                success_metamodel = self.model.load_model(self.model_path)
            elif self.model_type == 'cokriging':
                from ...meta.cokriging import cokriging_utils
                self.model = cokriging_utils.DeviceAgnosticCoKriging(prefer_gpu=self.prefer_gpu)
                success_metamodel = self.model.load_model(self.model_path)
            else:
                raise ValueError(f"Unsupported model type: {self.model_type}")
            
            success_ann = self._load_ann_models()
            
            if not (success_metamodel and success_ann):
                raise RuntimeError("Failed to load one or more models")
            
            return True
            
        except Exception as e:
            print(f"Error loading models: {str(e)}")
            return False

    def _load_ann_models(self) -> bool:
        """Load ANN models with proper device handling"""
        # Same as original implementation
        try:
            # Load parameters
            with open('RESULT_MODEL_ANN/best_params_mean.json', 'r') as f:
                params_mean = json.load(f)
            with open('RESULT_MODEL_ANN/best_params_std.json', 'r') as f:
                params_std = json.load(f)
            
            # Build models
            self.ann_mean = self._build_ann_model(params_mean)
            self.ann_std = self._build_ann_model(params_std)
            
            # Load weights
            self.ann_mean.load_state_dict(torch.load(
                'RESULT_MODEL_ANN/mlp_model_mean.pth',
                map_location=self.device
            ))
            self.ann_std.load_state_dict(torch.load(
                'RESULT_MODEL_ANN/mlp_model_std.pth',
                map_location=self.device
            ))
            
            # Move to device and set eval mode
            self.ann_mean = self.ann_mean.to(self.device).eval()
            self.ann_std = self.ann_std.to(self.device).eval()
            
            print(f"ANN models loaded successfully on {self.device}")
            return True
            
        except Exception as e:
            print(f"Error loading ANN models: {str(e)}")
            return False

    def _build_ann_model(self, params: dict) -> ANNModel:
        """Build ANN model with given parameters"""
        # Same as original implementation
        hidden_layers = [params[f'n_units_l{i}'] for i in range(params['n_layers'])]
        activation = getattr(nn, params['activation'])()
        return ANNModel(
            input_size=len(self.variable_names),
            hidden_layers=hidden_layers,
            output_size=1,
            activation=activation
        )

    def predict_metamodel(self, X: np.ndarray, batch_size: int = 1000) -> np.ndarray:
        """Evaluate metamodel predictions in batches"""
        if self.model is None:
            raise ValueError("Metamodel not loaded. Call load_models first.")
        
        # Use the model's predict method which returns (mean, std) for both GPR and CoKriging
        mean_pred, _ = self.model.predict(X)
        
        return mean_pred

    def predict_ann(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Make predictions with ANN models"""
        # Same as original implementation
        if self.ann_mean is None or self.ann_std is None:
            raise ValueError("ANN models not loaded. Call load_models first.")
            
        X_scaled = self.scaler_X_ann.transform(X)
        X_tensor = torch.tensor(X_scaled, dtype=torch.float32).to(self.device)
        
        with torch.no_grad():
            mean_scaled = self.ann_mean(X_tensor).cpu().numpy()
            std_scaled = self.ann_std(X_tensor).cpu().numpy()
        
        mean = self.scaler_y_mean.inverse_transform(mean_scaled.reshape(-1, 1)).flatten()
        std = self.scaler_y_std.inverse_transform(std_scaled.reshape(-1, 1)).flatten()
        
        return mean, np.abs(std)


class OptimizationVisualizer:
    def __init__(self, save_dir: str = 'RESULT_PARETO_FRONT_TWOSTAGE'):
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)

    def plot_pareto_front(self, pareto_front: np.ndarray):
        fig, ax = plt.subplots(figsize=(6, 5), tight_layout=True)
        
        ax.scatter(pareto_front[:, 0], pareto_front[:, 1], 
                  color='b', edgecolors='k', s=30, marker='s')
        ax.set_xlabel('Mean Performance')
        ax.set_ylabel('Standard Deviation')
        ax.grid(True, linestyle='--')
        
        ax.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        
        plt.savefig(f'{self.save_dir}/pareto_front.png', dpi=300)
        plt.close()

    def plot_decision_variables(self, pareto_set: np.ndarray, 
                              variable_names: List[str]):
        n_vars = pareto_set.shape[1]
        fig, axs = plt.subplots(n_vars, 1, figsize=(10, 4*n_vars), 
                               tight_layout=True)
        
        if n_vars == 1:
            axs = [axs]
        
        for i, ax in enumerate(axs):
            ax.scatter(pareto_set[:, i], np.zeros_like(pareto_set[:, i]),
                      color='blue', edgecolors='k', s=30,
                      label=f'Decision Variable: {variable_names[i]}')
            ax.set_xlabel(f'Value of {variable_names[i]}')
            ax.set_yticks([0])
            ax.set_ylabel('Constant Value (0)')
            ax.legend()
            ax.grid(True, linestyle='--')
        
        plt.savefig(f'{self.save_dir}/pareto_set.png', dpi=300)
        plt.close()


class MultiFidelityOptimizationProblem(Problem):
    """Multi-fidelity optimization problem using Pareto-based approach"""
    def __init__(self, model_handler: DeviceAgnosticHandler, 
                 num_mcs_samples: int = 1000000,
                 pop_size: int = 50):  # Added pop_size parameter
        self.model_handler = model_handler
        self.num_mcs_samples = num_mcs_samples
        self.pop_size = pop_size  # Store pop_size
        self.dist_sampler = AdaptiveDistributionSampler()
        
        # Initialize counters
        self.ann_evaluations = 0
        self.mcs_evaluations = 0
        self.promising_points_current = 0  # at Current generation
        self.promising_points_total = 0    # at Running total
        
        # Initialize problem
        xl = np.array([b[0] for b in model_handler.input_bound])
        xu = np.array([b[1] for b in model_handler.input_bound])
        
        super().__init__(
            n_var=len(model_handler.variable_names),
            n_obj=2,
            n_constr=0,
            xl=xl,
            xu=xu
        )



    def evaluate_ann(self, X: np.ndarray) -> np.ndarray:
        """Evaluate points using ANN models"""
        mean, std = self.model_handler.predict_ann(X)
        self.ann_evaluations += len(X)
        return np.column_stack([mean, std])

    def evaluate_mcs(self, X: np.ndarray) -> np.ndarray:
        """Evaluate points using MCS with metamodel"""
        results = []
        for x in X:
            X_samples = self._generate_mc_samples(x)
            Y_samples = self.model_handler.predict_metamodel(X_samples)
            results.append([np.mean(Y_samples), np.std(Y_samples)])
        
        self.mcs_evaluations += len(X) * self.num_mcs_samples
        return np.array(results)


    def _generate_mc_samples(self, design_point: np.ndarray) -> np.ndarray:
        """Generate Monte Carlo samples for a design point"""
        X_samples = np.zeros((self.num_mcs_samples, 
                            len(self.model_handler.data_info['variables'])))
        design_var_idx = 0
        
        for i, var in enumerate(self.model_handler.data_info['variables']):
            if var['vars_type'] == 'design_vars':
                base_value = design_point[design_var_idx]
                    
                # Check for various uncertainty parameters
                has_uncertainty = False
                
                # Case 1: Using CoV
                if var.get('cov') is not None and var.get('cov') > 0:
                    lower, upper = var['range_bounds']
                    X_samples[:, i] = self.dist_sampler.generate_samples(
                        distribution=var.get('distribution', 'normal'),
                        mean=base_value,
                        cov=var['cov'],
                        lower=lower,
                        upper=upper,
                        size=self.num_mcs_samples
                    )
                    has_uncertainty = True
                
                # Case 2: Using std directly
                elif var.get('std') is not None and var.get('std') > 0:
                    lower, upper = var['range_bounds']
                    X_samples[:, i] = self.dist_sampler.generate_samples(
                        distribution=var.get('distribution', 'normal'),
                        mean=base_value,
                        std=var['std'],
                        lower=lower,
                        upper=upper,
                        size=self.num_mcs_samples
                    )
                    has_uncertainty = True
                
                # Case 3: Using delta (for uniform)
                elif var.get('delta') is not None and var.get('delta') > 0:
                    if var.get('distribution') == 'uniform':
                        X_samples[:, i] = self.dist_sampler.generate_samples(
                            distribution='uniform',
                            mean=base_value,
                            delta=var['delta'],
                            size=self.num_mcs_samples
                        )
                    else:
                        # Treat delta as std for non-uniform distributions
                        lower, upper = var['range_bounds']
                        X_samples[:, i] = self.dist_sampler.generate_samples(
                            distribution=var.get('distribution', 'normal'),
                            mean=base_value,
                            std=var['delta'],
                            lower=lower,
                            upper=upper,
                            size=self.num_mcs_samples
                        )
                    has_uncertainty = True
                        
                # Deterministic case
                if not has_uncertainty:
                    X_samples[:, i] = base_value
                    
                design_var_idx += 1
            else:  # Environmental variable
                X_samples[:, i] = self.dist_sampler.generate_env_samples(
                    var, self.num_mcs_samples
                )
        return X_samples


    def select_pareto_points(self, X: np.ndarray, F: np.ndarray) -> np.ndarray:
        """Select Pareto front points"""
        nds = NonDominatedSorting()
        fronts = nds.do(F)
        return fronts[0]  # Return all Pareto points

    def _evaluate(self, X: np.ndarray, out: Dict, *args, **kwargs):
        """Main evaluation function using ANN for screening and MCS for final results"""
        # Get ANN predictions for all points (fast screening)
        F_ann = self.evaluate_ann(X)
        
        # Select Pareto points for MCS evaluation
        pareto_indices = self.select_pareto_points(X, F_ann)
        
        # Update both current and total promising points
        self.promising_points_current = len(pareto_indices)
        self.promising_points_total += len(pareto_indices)
        
        # Evaluate selected points with MCS
        F_mcs = self.evaluate_mcs(X[pareto_indices])
        
        # Initialize output array with high values
        F = np.full_like(F_ann, np.max(F_mcs) + 1)
        
        # Update selected points with MCS results
        F[pareto_indices] = F_mcs
        
        out["F"] = F


class OptimizationRunner:
    """Handles the optimization process and results visualization"""
    def __init__(self, save_dir: str = 'RESULT_PARETO_FRONT_TWOSTAGE'):
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)
        
        # Set plotting style
        rcParams['font.family'] = 'serif'
        rcParams['font.serif'] = 'Times New Roman'
        rcParams['font.size'] = 14
        rcParams['axes.titlesize'] = 16
        rcParams['axes.labelsize'] = 14
        rcParams['xtick.labelsize'] = 14
        rcParams['ytick.labelsize'] = 14

    def setup_algorithm(self, pop_size: int) -> NSGA2:
        """Setup NSGA-II algorithm with standard parameters"""
        return NSGA2(
            pop_size=pop_size,
            sampling=LHS(),
            crossover=SBX(prob=0.9, eta=20),
            mutation=PM(eta=20),
            eliminate_duplicates=True
        )

    def create_visualizations(self, pareto_front: np.ndarray, 
                            pareto_set: np.ndarray,
                            variable_names: List[str]):
        """Create and save optimization visualizations"""
        # Plot Pareto front
        fig, ax = plt.subplots(figsize=(6, 5), tight_layout=True)
        ax.scatter(pareto_front[:, 0], pareto_front[:, 1], 
                  color='b', edgecolors='k', s=30, marker='s')
        ax.set_xlabel('Mean Performance')
        ax.set_ylabel('Standard Deviation')
        ax.grid(True, linestyle='--')
        # ax.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
        # ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        plt.savefig(os.path.join(self.save_dir, 'pareto_front.png'), dpi=300)
        plt.close()

        # Plot decision variables
        n_vars = pareto_set.shape[1]
        fig, axs = plt.subplots(n_vars, 1, figsize=(10, 4*n_vars), 
                               tight_layout=True)
        
        if n_vars == 1:
            axs = [axs]
        
        for i, ax in enumerate(axs):
            ax.scatter(pareto_set[:, i], np.zeros_like(pareto_set[:, i]),
                      color='blue', edgecolors='k', s=30,
                      label=f'Decision Variable: {variable_names[i]}')
            ax.set_xlabel(f'Value of {variable_names[i]}')
            ax.set_yticks([0])
            ax.set_ylabel('Constant Value (0)')
            ax.legend()
            ax.grid(True, linestyle='--')
            ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        
        plt.savefig(os.path.join(self.save_dir, 'pareto_set.png'), dpi=300)
        plt.close()


    def save_results(self, pareto_set: np.ndarray, pareto_front: np.ndarray,
                    variable_names: List[str], problem: MultiFidelityOptimizationProblem,
                    total_time: float, n_gen: int, pipeline_start_time: float, 
                    callback=None):  # Add callback parameter
        
        pipeline_total_time = time.time() - pipeline_start_time  # record start time

        """Save optimization results with detailed information"""
        # Save solutions to CSV
        results_df = pd.DataFrame(
            np.hstack([pareto_set, pareto_front]),
            columns=variable_names + ['Mean', 'StdDev']
        )
        results_df.sort_values('StdDev', ascending=True, inplace=True)
        results_df.to_csv(os.path.join(self.save_dir, 'pareto_solutions.csv'), 
                        index=False)
        
        # Calculate theoretical evaluations
        total_theoretical_evals = problem.pop_size * n_gen * problem.num_mcs_samples
        efficiency = ((total_theoretical_evals - problem.mcs_evaluations) / 
                    total_theoretical_evals * 100)
        
        # Save convergence data if available
        if callback and callback.metrics:
            convergence_df = pd.DataFrame({
                'Time_Elapsed': callback.elapsed_times,
                'ann_evaluations': callback.ann_evals,
                'promising_points_per_gen': callback.promising_points_per_gen,
                'promising_points_total': callback.promising_points_total,
                'mcs_evaluations': callback.mcs_evals,
                f'{callback.metric_type}_value': callback.metrics
            })
            convergence_df.to_csv(os.path.join(self.save_dir, 'convergence.csv'), 
                                index=False)
            
            # Create convergence history dict in the same format as other methods
            convergence_history = {
                'n_evals': callback.ann_evals,
                'metric_values': callback.metrics,
                'metric_type': callback.metric_type,
                'elapsed_times': callback.elapsed_times,
                'reference_point': callback.reference_point if hasattr(callback, 'reference_point') else None
            }
            
            # Use the same visualizer as other methods
            from ...robustopt.visualization import OptimizationVisualizer
            visualizer = OptimizationVisualizer(save_dir=self.save_dir)
            visualizer.create_all_visualizations(
                results_df=results_df,
                convergence_history=convergence_history
            )
                    
        # Save detailed summary
        with open(os.path.join(self.save_dir, 'optimization_summary.txt'), 'w') as f:
            f.write("Variable Information\n")
            f.write("===================\n\n")
            
            # Design Variables
            f.write("Design Variables:\n")
            f.write("-----------------\n\n")
            for var in problem.model_handler.variables:
                f.write(f"{var['name']}:\n")
                f.write(f"  Type: {var['vars_type']}\n")
                f.write(f"  Distribution: {var['distribution']}\n")
                f.write(f"  Range: [{var['range_bounds'][0]:.3f}, {var['range_bounds'][1]:.3f}]\n")
                f.write(f"  CoV: {var['cov']:.3f}\n\n")
            
            # Environmental Variables
            f.write("Environmental Variables:\n")
            f.write("----------------------\n\n")
            env_vars = [var for var in problem.model_handler.data_info['variables'] 
                        if var['vars_type'] == 'env_vars']
            if env_vars:
                for var in env_vars:
                    f.write(f"{var['name']}:\n")
                    f.write(f"  Distribution: {var['distribution']}\n")
                    if 'low' in var and 'high' in var:
                        f.write(f"  Range: [{var['low']}, {var['high']}]\n")
                    if 'params' in var:  # Check if the 'params' key exists
                        f.write(f"  Parameters: {var['params']}\n")
                    f.write("\n")
            else:
                f.write("No Environmental Variables\n\n\n")

            
            # Optimization Summary
            f.write("Optimization Summary\n")
            f.write("===================\n\n")
            f.write("Performance Statistics:\n")
            f.write(f"Total Runtime Optimization Loop: {total_time:.2f} seconds\n")
            f.write(f"Total Runtime Pipeline: {pipeline_total_time:.2f} seconds\n")
            f.write(f"ANN Evaluations: {problem.ann_evaluations:,}\n")
            f.write(f"MCS Evaluations: {problem.mcs_evaluations:,}\n")
            f.write(f"Theoretical Full MCS: {total_theoretical_evals:,}\n")
            f.write(f"Computational Efficiency Improved: {efficiency:.1f}%\n")
            
            if callback and callback.metrics:
                f.write(f"\nConvergence Information:\n")
                f.write(f"Initial {callback.metric_type.upper()} value: {callback.metrics[0]:.6f}\n")
                f.write(f"Final {callback.metric_type.upper()} value: {callback.metrics[-1]:.6f}\n")
                
                if hasattr(callback, 'reference_point') and callback.reference_point is not None:
                    f.write(f"Reference point: {callback.reference_point}\n")
                
                # Calculate improvement safely to avoid division by zero
                if callback.metrics[0] > 0:
                    improvement = ((callback.metrics[-1] / callback.metrics[0]) - 1) * 100
                    f.write(f"Improvement: {improvement:.1f}%\n")
                else:
                    # Handle the case where initial metric value is 0
                    if callback.metrics[-1] > 0:
                        f.write("Improvement: Infinite (started at zero)\n")
                    else:
                        f.write("Improvement: 0% (no change from zero)\n")


    

def run_optimization(num_mcs_samples: int = 1000000, 
                    pop_size: int = 50, 
                    n_gen: int = 100,
                    metric: str = 'hv',
                    reference_point: Optional[np.ndarray] = None,
                    model_type: str = 'gpr',
                    model_path: str = None,
                    prefer_gpu: bool = True,
                    verbose: bool = False,
                    save_dir: str = 'RESULT_PARETO_FRONT_TWOSTAGE'):  
    
    pipeline_start_time = time.time()

    class ProgressCallback:
        def __init__(self, n_gen, metric='hv', eval_interval=50):
            self.start_time = time.time()
            self.n_gen = n_gen
            self.metrics = []
            self.ann_evals = []
            self.mcs_evals = []
            self.promising_points_per_gen = []
            self.promising_points_total = []
            self.elapsed_times = []
            self.metric_type = metric
            self.indicator = None
            self.reference_point = reference_point  # Store reference point
            self.last_recorded_anns = 0
            self.eval_interval = eval_interval
                
        def __call__(self, algorithm):
            current_ann_evals = problem.ann_evaluations
            
            if current_ann_evals >= self.last_recorded_anns + self.eval_interval:
                elapsed = time.time() - self.start_time
                
                F = algorithm.opt.get("F")
                if F is None:
                    F = algorithm.pop.get("F")
                
                if self.indicator is None and F is not None:
                    if self.metric_type == 'hv':
                        if self.reference_point is None:
                            # Automatic reference point calculation if not provided
                            self.reference_point = np.max(F, axis=0) * 1.1
                        self.indicator = HV(ref_point=self.reference_point)
                
                if F is not None and self.indicator is not None:
                    metric_value = self.indicator(F)
                    self.metrics.append(metric_value)
                    self.ann_evals.append(problem.ann_evaluations)
                    self.mcs_evals.append(problem.mcs_evaluations)
                    self.promising_points_per_gen.append(problem.promising_points_current)
                    self.promising_points_total.append(problem.promising_points_total)
                    self.elapsed_times.append(elapsed)
                    
                    self.last_recorded_anns = current_ann_evals
                
                    # Print progress
                    print(f"\nTime Elapsed: {elapsed:.1f} seconds")
                    print(f"ANN Evaluations: {problem.ann_evaluations:,}")
                    print(f"Promising Points (Current/Total): {problem.promising_points_current:,}/{problem.promising_points_total:,}")
                    print(f"MCS Evaluations: {problem.mcs_evaluations:,}")
                    print(f"Generation: {algorithm.n_gen + 1}/{self.n_gen}")
                    if self.metric_type == 'hv':
                        print(f"Current HV: {metric_value:.6f}")
                    print(f"Non-dominated Solutions: {len(algorithm.opt)}")


    """Run two-stage optimization"""
    start_time = time.time()
    
    # Calculate theoretical evaluations
    total_theoretical_evals = pop_size * n_gen * num_mcs_samples
    
    # Print initial setup information
    print("\n" + "="*50)
    print("TWO-STAGE ROBUST OPTIMIZATION")
    print("="*50)
    
    # Initialize model handler with model_type
    model_handler = DeviceAgnosticHandler(
        model_type=model_type,
        model_path=model_path,
        prefer_gpu=prefer_gpu
    )
    
    # Load models
    if not model_handler.load_models():
        raise RuntimeError("Failed to load models")
    
    print("\n****** Optimization Parameters:")
    print(f"Population Size: {pop_size}")
    print(f"Number of Generations: {n_gen}")
    print(f"MCS Samples per Evaluation: {num_mcs_samples:,}")
    print(f"Performance Metric: {metric.upper()}")
    if reference_point is not None and metric == 'hv':
        print(f"Reference point: {reference_point}")
    print(f"Total theoretical MCS evaluations: {total_theoretical_evals:,}")
    
    # Initialize optimization components
    problem = MultiFidelityOptimizationProblem(
        model_handler=model_handler,
        num_mcs_samples=num_mcs_samples
    )
    
    runner = OptimizationRunner(save_dir=save_dir)
    algorithm = runner.setup_algorithm(pop_size)
    
    # Setup progress tracking with metric
    callback = ProgressCallback(n_gen, metric=metric, eval_interval=50)  
    
    # Run optimization
    res = minimize(
        problem,
        algorithm,
        ('n_gen', n_gen),
        callback=callback,
        seed=42,
        verbose=verbose
    )
    
    # Process results
    total_time = time.time() - start_time
    efficiency = ((total_theoretical_evals - problem.mcs_evaluations) / 
                total_theoretical_evals * 100)
    
    print("\n" + "="*50)
    print("OPTIMIZATION COMPLETE")
    print("="*50)
    
    print("\nPerformance Statistics:")
    print(f"Total Runtime: {total_time:.2f} seconds")
    print(f"ANN Evaluations: {problem.ann_evaluations:,}")
    print(f"MCS Evaluations: {problem.mcs_evaluations:,}")
    print(f"Theoretical Full MCS: {total_theoretical_evals:,}")
    print(f"Computational Efficiency Improved: {efficiency:.1f}%")
    if callback.metrics:
        print(f"Final {metric.upper()} Value: {callback.metrics[-1]:.6f}")
    
    
    # Create visualizations and save results
    runner.create_visualizations(
        res.F, res.X, model_handler.variable_names
    )
    
    runner.save_results(
        pareto_set=res.X,
        pareto_front=res.F,
        variable_names=model_handler.variable_names,
        problem=problem,
        total_time=total_time,
        n_gen=n_gen,
        pipeline_start_time=pipeline_start_time,
        callback=callback  
    )
        
    print(f"\nResults saved in: {runner.save_dir}")
    
    return res.X, res.F














