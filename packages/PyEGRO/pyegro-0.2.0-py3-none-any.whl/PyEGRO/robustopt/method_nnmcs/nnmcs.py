import os
import time
import numpy as np
import torch
from typing import Tuple, Optional
from dataclasses import dataclass, field
from typing import Dict

from ...uncertainty.UQmcs.uqmcs import UncertaintyPropagation
from ._ann_hyperopt import run_hyperopt_ann
from ._ann_training import run_training_ann
from ._multi_obj_two_stage import run_optimization

@dataclass
class ANNConfig:
    n_trials: int = 50
    n_jobs: int = -1
    hyperparameter_ranges: Dict = field(default_factory=lambda: {
        'n_layers': (1, 6),
        'n_units': (32, 512),
        'learning_rate': (1e-4, 1e-1),
        'batch_size': (16, 128),
        'max_epochs': (50, 500),
        'activations': ['ReLU', 'LeakyReLU', 'Tanh'],
        'optimizers': ['Adam', 'AdamW'],
        'loss_functions': ['MSELoss', 'HuberLoss']
    })

@dataclass
class SamplingConfig:
    # LHS sampling configuration
    n_lhs_samples: int = 2000
    # Low fidelity MCS (for training ANN)
    n_mcs_samples_low: int = 10000
    # High fidelity MCS (for final verification)
    n_mcs_samples_high: int = 1000000
    random_seed: int = 42

@dataclass
class OptimizationConfig:
    pop_size: int = 50
    n_gen: int = 100
    prefer_gpu: bool = True
    verbose: bool = False
    random_seed: int = 42
    metric: str = 'hv'  # Add metric parameter
    reference_point: Optional[np.ndarray] = None,  # Added parameter

@dataclass
class PathConfig:
    model_type: str = 'gpr'  # Added field for model type
    model_dir: str = None    # Generic model directory
    gpr_model_dir: str = 'RESULT_MODEL_GPR'  # For backward compatibility
    ann_model_dir: str = 'RESULT_MODEL_ANN'
    data_info_path: str = 'DATA_PREPARATION/data_info.json'
    results_dir: str = 'RESULT_PARETO_FRONT_TWOSTAGE'
    qoi_dir: str = 'RESULT_QOI'
    
    def __post_init__(self):
        # Set model_dir based on model_type if not explicitly provided
        if self.model_dir is None:
            self.model_dir = f'RESULT_MODEL_{self.model_type.upper()}'


class RobustOptimization:
    def __init__(self, 
                 ann_config: Optional[ANNConfig] = None,
                 sampling_config: Optional[SamplingConfig] = None,
                 optimization_config: Optional[OptimizationConfig] = None,
                 path_config: Optional[PathConfig] = None):

        self.ann_config = ann_config or ANNConfig()
        self.sampling_config = sampling_config or SamplingConfig()
        self.opt_config = optimization_config or OptimizationConfig()
        self.path_config = path_config or PathConfig()

        self._create_directories()
        self._set_random_seeds()

    def _create_directories(self):
        # Create model directory based on model type
        os.makedirs(self.path_config.model_dir, exist_ok=True)
        os.makedirs(self.path_config.ann_model_dir, exist_ok=True)
        os.makedirs(self.path_config.results_dir, exist_ok=True)
        os.makedirs(self.path_config.qoi_dir, exist_ok=True)

    def _set_random_seeds(self):
        np.random.seed(self.opt_config.random_seed)
        torch.manual_seed(self.opt_config.random_seed)

    def _check_ann_params_exist(self) -> bool:
        mean_params = os.path.join(self.path_config.ann_model_dir, 'best_params_mean.json')
        std_params = os.path.join(self.path_config.ann_model_dir, 'best_params_std.json')
        return os.path.isfile(mean_params) and os.path.isfile(std_params)

    def _validate_file(self, file_path: str, description: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{description} file not found: {file_path}")

    def _run_uncertainty_propagation(self):
        self._validate_file(self.path_config.data_info_path, "Data info")

        # Load appropriate model handler based on model_type
        if self.path_config.model_type == 'gpr':
            from ...meta.gpr import gpr_utils
            model_handler = gpr_utils.DeviceAgnosticGPR(prefer_gpu=True)
        elif self.path_config.model_type == 'cokriging':
            from ...meta.cokriging import cokriging_utils
            model_handler = cokriging_utils.DeviceAgnosticCoKriging(prefer_gpu=True)
        else:
            raise ValueError(f"Unsupported model type: {self.path_config.model_type}")
        
        # Load the model
        model_handler.load_model(self.path_config.model_dir)
        
        # Use low fidelity MCS for uncertainty propagation
        propagation = UncertaintyPropagation(
            data_info_path=self.path_config.data_info_path,
            model_handler=model_handler,
            output_dir=self.path_config.qoi_dir,
            show_variables_info=True,
            use_gpu=True
        )
        
        results = propagation.run_analysis(
            num_design_samples=self.sampling_config.n_lhs_samples,
            num_mcs_samples=self.sampling_config.n_mcs_samples_low,
            show_progress=True
        )

    def _optimize_ann_hyperparams(self):
        if not os.path.exists(os.path.join(self.path_config.qoi_dir, 'uncertainty_propagation_results.csv')):
            self._run_uncertainty_propagation()
        
        # Pass the configuration parameters to run_hyperopt_ann
        run_hyperopt_ann(
            hyperparameter_ranges=self.ann_config.hyperparameter_ranges,
            n_trials=self.ann_config.n_trials,
            n_jobs=self.ann_config.n_jobs
        )

    def _train_ann_models(self):
        print("\n------> Training ANN models...")
        run_training_ann()

    def _run_optimization(self) -> Tuple[np.ndarray, np.ndarray]:
        # Use high fidelity MCS for final optimization verification
        pareto_set, pareto_front = run_optimization(
            num_mcs_samples=self.sampling_config.n_mcs_samples_high,
            pop_size=self.opt_config.pop_size,
            n_gen=self.opt_config.n_gen,
            metric=self.opt_config.metric,
            reference_point=self.opt_config.reference_point,
            model_type=self.path_config.model_type,
            model_path=self.path_config.model_dir,
            prefer_gpu=self.opt_config.prefer_gpu,
            verbose=self.opt_config.verbose,
            save_dir=self.path_config.results_dir  # Pass the custom results directory
        )
        return pareto_set, pareto_front

    def run(self):
        start_time = time.time()

        print("\n========== STEP 1: Uncertainty Propagation")
        qoi_file = os.path.join(self.path_config.qoi_dir, 'uncertainty_propagation_results.csv')
        if not os.path.exists(qoi_file):
            print("\nRunning uncertainty propagation...")
            self._run_uncertainty_propagation()
        else:
            print("\nUncertainty propagation results found.")

        print("\n========== STEP 2: Hyperparameter Optimization")
        if not self._check_ann_params_exist():
            self._optimize_ann_hyperparams()
        else:
            print("\nHyperparameter results found.")

        print("\n========== STEP 3: Training ANN Models")
        self._train_ann_models()

        print("\n========== STEP 4: Two-Stage Robust Optimization")
        pareto_set, pareto_front = self._run_optimization()

        total_time = time.time() - start_time
        print(f"\n========== Pipeline Completed in {total_time:.2f} seconds")

        return pareto_set, pareto_front

if __name__ == "__main__":
    # Initialize configurations with separated MCS sample sizes
    sampling_config = SamplingConfig(
        n_lhs_samples=2000,
        n_mcs_samples_low=10000,    # Lower number for training
        n_mcs_samples_high=1000000  # Higher number for verification
    )
    
    ann_config = ANNConfig(
        n_trials=50,
        n_jobs=-1,
        hyperparameter_ranges={
            'n_layers': (2, 4),
            'n_units': (64, 256),
            'learning_rate': (1e-4, 1e-2),
            'batch_size': (32, 64),
            'max_epochs': (100, 300),
            'activations': ['ReLU', 'LeakyReLU'],
            'optimizers': ['Adam'],
            'loss_functions': ['MSELoss']
        }
    )
    
    opt_config = OptimizationConfig(
        pop_size=50,
        n_gen=200,
        prefer_gpu=True,
        verbose=True,
        metric='hv',
        reference_point=[5,5]
    )
    
    path_config = PathConfig(
        model_type='gpr',  # Change this to 'gpr', 'cokriging', etc.
        model_dir='RESULT_MODEL_GPR',  # Customize if needed
        ann_model_dir='RESULT_MODEL_ANN',
        results_dir='RESULT_PARETO_FRONT_TWOSTAGE',
        qoi_dir='RESULT_QOI'
    )

    optimizer = RobustOptimization(
        ann_config=ann_config,
        sampling_config=sampling_config,
        optimization_config=opt_config,
        path_config=path_config
    )

    optimizer.run()