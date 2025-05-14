
import os
import time
from datetime import datetime
import json
import warnings
import joblib
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from rich.progress import Progress, BarColumn, TimeElapsedColumn, TimeRemainingColumn
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
import optuna
from gpytorch.utils.warnings import GPInputWarning

# Suppress warnings
warnings.filterwarnings("ignore", category=GPInputWarning)
optuna.logging.set_verbosity(optuna.logging.WARNING)


class ANNModel(nn.Module):
    def __init__(self, input_size, hidden_layers, output_size, activation):
        super(ANNModel, self).__init__()
        layers = []
        for i, units in enumerate(hidden_layers):
            layers.append(nn.Linear(input_size if i == 0 else hidden_layers[i-1], units))
            layers.append(activation)
        layers.append(nn.Linear(hidden_layers[-1], output_size))
        self.model = nn.Sequential(*layers)

    def forward(self, x):
        return self.model(x)


class ANNHyperparameterOptimizer:
    def __init__(self, X_train, y_train, X_test, y_test, device, param_space):
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.device = device
        self.param_space = param_space  # Accept param_space as input
        
        # Convergence tracking
        self.best_scores = []
        self.convergence_threshold = 1e-4
        self.convergence_count = 10
    
    def create_model(self, params):
        activation = getattr(nn, params['activation'])()
        model = ANNModel(
            input_size=self.X_train.shape[1],
            hidden_layers=params['hidden_layers'],
            output_size=1,
            activation=activation
        ).to(self.device)
        
        optimizer = getattr(optim, params['optimizer'])(
            model.parameters(), 
            lr=params['learning_rate']
        )
        criterion = getattr(nn, params['loss_function'])()
        
        return model, optimizer, criterion
    
    def create_dataloader(self, batch_size):
        dataset = TensorDataset(self.X_train, self.y_train)
        return DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    def suggest_parameters(self, trial):
        params = {
            'n_layers': trial.suggest_int('n_layers', *self.param_space['n_layers']),
            'learning_rate': trial.suggest_float('learning_rate', 
                                               *self.param_space['learning_rate'], 
                                               log=True),
            'batch_size': trial.suggest_int('batch_size', 
                                          *self.param_space['batch_size']),
            'max_epochs': trial.suggest_int('max_epochs', 
                                          *self.param_space['max_epochs']),
            'activation': trial.suggest_categorical('activation', 
                                                  self.param_space['activations']),
            'optimizer': trial.suggest_categorical('optimizer', 
                                                 self.param_space['optimizers']),
            'loss_function': trial.suggest_categorical('loss_function', 
                                                     self.param_space['loss_functions'])
        }
        
        hidden_layers = []
        for i in range(params['n_layers']):
            n_units = trial.suggest_int(f'n_units_l{i}', 
                                      *self.param_space['n_units'])
            hidden_layers.append(n_units)
        params['hidden_layers'] = hidden_layers
        
        return params
    
    def train_epoch(self, model, optimizer, criterion, train_loader):
        model.train()
        total_loss = 0
        for X_batch, y_batch in train_loader:
            optimizer.zero_grad()
            output = model(X_batch)
            loss = criterion(output, y_batch)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        return total_loss / len(train_loader)
    
    def check_convergence(self, score):
        """Check if the optimization has converged based on recent scores."""
        self.best_scores.append(score)
        
        if len(self.best_scores) >= self.convergence_count:
            recent_scores = self.best_scores[-self.convergence_count:]
            max_diff = max(abs(recent_scores[i] - recent_scores[i-1]) 
                         for i in range(1, len(recent_scores)))
            return max_diff < self.convergence_threshold
        return False
    
    def objective(self, trial):
        params = self.suggest_parameters(trial)
        model, optimizer, criterion = self.create_model(params)
        train_loader = self.create_dataloader(params['batch_size'])
        
        best_loss = float('inf')
        patience = 10
        epochs_without_improvement = 0
        
        for epoch in range(params['max_epochs']):
            loss = self.train_epoch(model, optimizer, criterion, train_loader)
            
            # Validation
            model.eval()
            with torch.no_grad():
                val_output = model(self.X_test)
                val_loss = criterion(val_output, self.y_test).item()
            
            if val_loss < best_loss:
                best_loss = val_loss
                epochs_without_improvement = 0
                # Store best model parameters in CPU format
                if self.device.type == 'cuda':
                    model_cpu = model.cpu()
                    best_state_dict = model_cpu.state_dict()
                    model = model.to(self.device)  # Move back to GPU
                else:
                    best_state_dict = model.state_dict()
            else:
                epochs_without_improvement += 1
            
            if epochs_without_improvement >= patience:
                break
            
            if np.isnan(loss) or np.isnan(val_loss):
                raise optuna.exceptions.TrialPruned()
        
        # Final evaluation using R2 score
        model.eval()
        with torch.no_grad():
            y_pred = model(self.X_test).cpu().numpy()
            score = -r2_score(self.y_test.cpu().numpy(), y_pred)
        
        return score

    def optimize(self, n_trials=50):
        study = optuna.create_study(direction='minimize')
        study.optimize(self.objective, n_trials=n_trials, n_jobs=-1,
                      show_progress_bar=True)
        
        return study.best_params, study.best_value


class ANNHyperOptLogger:
    def __init__(self, output_dir: str = 'RESULT_MODEL_ANN'):
        """
        Initialize logger for ANN hyperparameter optimization
        
        Args:
            output_dir (str): Base directory for outputs
        """
        # Create main output directory and subdirectories
        self.output_dir = Path(output_dir)
        self.results_dir = self.output_dir / 'optimization_results'

        # Create all directories
        self.output_dir.mkdir(exist_ok=True)
        self.results_dir.mkdir(exist_ok=True)


        # Initialize timing information
        self.timing_info = {
            'start_time': time.time(),
            'data_preparation': {'start': None, 'end': None},
            'mean_model': {
                'optimization_start': None,
                'optimization_end': None,
                'trials': []  # Will store time for each trial
            },
            'std_model': {
                'optimization_start': None,
                'optimization_end': None,
                'trials': []  # Will store time for each trial
            }
        }

        # Initialize system information
        self.system_info = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'device': None,
            'pytorch_version': torch.__version__,
            'cuda_version': torch.version.cuda if torch.cuda.is_available() else None
        }

        # Initialize results storage
        self.results = {
            'data_info': {
                'train_size': None,
                'test_size': None,
                'input_features': None,
                'scaling_info': None
            },
            'mean_model': {
                'best_params': None,
                'best_score': None,
                'trial_history': [],
                'convergence_data': []
            },
            'std_model': {
                'best_params': None,
                'best_score': None,
                'trial_history': [],
                'convergence_data': []
            },
            'hyperparameter_ranges': None
        }

    def record_device_info(self, device: torch.device):
        """Record device and hardware information"""
        self.system_info['device'] = str(device)
        
        if device.type == "cuda":
            self.system_info.update({
                'gpu_name': torch.cuda.get_device_name(),
                'gpu_memory': f"{torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB",
                'gpu_capability': f"CUDA Capability {torch.cuda.get_device_capability()}",
                'gpu_count': torch.cuda.device_count()
            })
        else:
            import platform
            import psutil
            self.system_info.update({
                'cpu_name': platform.processor() or "Unknown CPU",
                'cpu_count': psutil.cpu_count(),
                'physical_cores': psutil.cpu_count(logical=False),
                'system_memory': f"{psutil.virtual_memory().total / 1024**3:.1f} GB"
            })

    def record_data_info(self, X_train, X_test, scaler_info=None):
        """Record dataset information and scaling parameters"""
        self.results['data_info'].update({
            'train_size': len(X_train),
            'test_size': len(X_test),
            'input_features': X_train.shape[1],
            'scaling_info': scaler_info
        })

    def record_hyperparameter_ranges(self, param_ranges: dict):
        """Record hyperparameter search ranges"""
        self.results['hyperparameter_ranges'] = param_ranges

    def start_data_preparation(self):
        """Mark start of data preparation phase"""
        self.timing_info['data_preparation']['start'] = time.time()

    def end_data_preparation(self):
        """Mark end of data preparation phase"""
        self.timing_info['data_preparation']['end'] = time.time()

    def start_optimization(self, model_type: str):
        """Start timing for model optimization"""
        self.timing_info[f'{model_type}_model']['optimization_start'] = time.time()

    def end_optimization(self, model_type: str, best_params: dict, best_score: float, 
                        trial_history: list):
        """Record optimization results and timing"""
        end_time = time.time()
        self.timing_info[f'{model_type}_model']['optimization_end'] = end_time
        
        self.results[f'{model_type}_model'].update({
            'best_params': best_params,
            'best_score': best_score,
            'trial_history': trial_history
        })

    def record_trial(self, model_type: str, trial_num: int, params: dict, 
                    score: float, trial_time: float):
        """Record individual trial results"""
        self.results[f'{model_type}_model']['trial_history'].append({
            'trial_num': trial_num,
            'params': params,
            'score': score,
            'time': trial_time
        })


    def compute_timing_stats(self):
        """Compute comprehensive timing statistics"""
        total_time = time.time() - self.timing_info['start_time']
        data_prep_time = (self.timing_info['data_preparation']['end'] - 
                         self.timing_info['data_preparation']['start'])
        
        mean_opt_time = (self.timing_info['mean_model']['optimization_end'] - 
                        self.timing_info['mean_model']['optimization_start'])
        std_opt_time = (self.timing_info['std_model']['optimization_end'] - 
                       self.timing_info['std_model']['optimization_start'])

        return {
            'total_time': total_time,
            'data_preparation_time': data_prep_time,
            'mean_optimization_time': mean_opt_time,
            'std_optimization_time': std_opt_time,
            'optimization_time': mean_opt_time + std_opt_time
        }

    def save_all(self):
        """Save all information to files"""
        timing_stats = self.compute_timing_stats()
        
        # Prepare complete info dictionary
        complete_info = {
            'system_info': self.system_info,
            'timing_stats': timing_stats,
            'results': self.results
        }

        # Save main results
        with open(self.results_dir / 'optimization_results.json', 'w') as f:
            json.dump(complete_info, f, indent=4)


    def print_summary(self):
        """Print comprehensive summary of the optimization process"""
        timing_stats = self.compute_timing_stats()

        print("\nANN Hyperparameter Optimization Summary")
        print("=" * 50)

        print("\nSystem Information:")
        print("-" * 30)
        for key, value in self.system_info.items():
            if value is not None:
                print(f"{key.replace('_', ' ').title()}: {value}")

        print("\nDataset Information:")
        print("-" * 30)
        data_info = self.results['data_info']
        print(f"Training Samples: {data_info['train_size']:,}")
        print(f"Testing Samples: {data_info['test_size']:,}")
        print(f"Input Features: {data_info['input_features']}")

        print("\nOptimization Results:")
        print("-" * 30)
        for model_type in ['mean', 'std']:
            print(f"\n{model_type.upper()} Model:")
            print(f"Best R² Score: {-self.results[f'{model_type}_model']['best_score']:.4f}")
            print(f"Number of Trials: {len(self.results[f'{model_type}_model']['trial_history'])}")

        print("\nComputational Time:")
        print("-" * 30)
        print(f"Data Preparation: {timing_stats['data_preparation_time']:.2f} seconds")
        print(f"Mean Model Optimization: {timing_stats['mean_optimization_time']:.2f} seconds")
        print(f"Std Model Optimization: {timing_stats['std_optimization_time']:.2f} seconds")
        print(f"Total Optimization Time: {timing_stats['optimization_time']:.2f} seconds")
        print(f"Total Process Time: {timing_stats['total_time']:.2f} seconds")

        print("\nResults saved in:", self.output_dir.absolute())



def prepare_data():
    """Load and prepare data for training"""
    # Load data info and results
    with open('DATA_PREPARATION/data_info.json', 'r') as f:
        data_info = json.load(f)
    
    design_variable_names = [var['name'] for var in data_info['variables'] 
                           if var['vars_type'] == 'design_vars']
    data = pd.read_csv('RESULT_QOI/uncertainty_propagation_results.csv')
    
    # Extract features and targets
    X = data[design_variable_names].values
    y_mean = data['Mean'].values.reshape(-1, 1)
    y_std = data['StdDev'].values.reshape(-1, 1)
    
    # Split data
    X_train, X_test, y_train_mean, y_test_mean, y_train_std, y_test_std = train_test_split(
        X, y_mean, y_std, test_size=0.2, random_state=42)
    
    # Create and fit scalers if they don't exist
    try:
        scaler_X = joblib.load('RESULT_MODEL_ANN/scaler_X_stage2.pkl')
        scaler_y_mean = joblib.load('RESULT_MODEL_ANN/scaler_y_mean_stage2.pkl')
        scaler_y_std = joblib.load('RESULT_MODEL_ANN/scaler_y_std_stage2.pkl')
    except (FileNotFoundError, EOFError):
        # print("Creating new scalers...")
        # Create directory if it doesn't exist
        os.makedirs('RESULT_MODEL_ANN', exist_ok=True)
        
        # Initialize and fit scalers
        scaler_X = StandardScaler()
        scaler_y_mean = StandardScaler()
        scaler_y_std = StandardScaler()
        
        # Fit scalers
        scaler_X.fit(X_train)
        scaler_y_mean.fit(y_train_mean)
        scaler_y_std.fit(y_train_std)
        
        # Save scalers
        joblib.dump(scaler_X, 'RESULT_MODEL_ANN/scaler_X_stage2.pkl')
        joblib.dump(scaler_y_mean, 'RESULT_MODEL_ANN/scaler_y_mean_stage2.pkl')
        joblib.dump(scaler_y_std, 'RESULT_MODEL_ANN/scaler_y_std_stage2.pkl')
    
    # Transform data
    X_train_scaled = scaler_X.transform(X_train)
    X_test_scaled = scaler_X.transform(X_test)
    y_train_mean_scaled = scaler_y_mean.transform(y_train_mean)
    y_test_mean_scaled = scaler_y_mean.transform(y_test_mean)
    y_train_std_scaled = scaler_y_std.transform(y_train_std)
    y_test_std_scaled = scaler_y_std.transform(y_test_std)
    
    # Convert to tensors
    return (torch.tensor(X_train_scaled, dtype=torch.float32),
            torch.tensor(X_test_scaled, dtype=torch.float32),
            torch.tensor(y_train_mean_scaled, dtype=torch.float32),
            torch.tensor(y_test_mean_scaled, dtype=torch.float32),
            torch.tensor(y_train_std_scaled, dtype=torch.float32),
            torch.tensor(y_test_std_scaled, dtype=torch.float32),
            scaler_y_mean, scaler_y_std)



def run_hyperopt_ann(hyperparameter_ranges=None, n_trials=50, n_jobs=-1, output_dir='RESULT_MODEL_ANN'):
    """
    Run hyperparameter optimization for ANN models.

    Args:
        hyperparameter_ranges (dict): Hyperparameter ranges for optimization.
        n_trials (int): Number of optimization trials.
        n_jobs (int): Number of parallel jobs (-1 for all cores).
        output_dir (str): Directory to save results.
    """
    # Create necessary directories
    os.makedirs(output_dir, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Initialize logger
    logger = ANNHyperOptLogger(output_dir)
    logger.record_device_info(torch.device("cuda" if torch.cuda.is_available() else "cpu"))

    # Use default hyperparameter ranges if none provided
    if hyperparameter_ranges is None:
        hyperparameter_ranges = {
            'n_layers': (1, 6),
            'n_units': (32, 512),
            'learning_rate': (1e-4, 1e-1),
            'batch_size': (16, 128),
            'max_epochs': (50, 500),
            'activations': ['ReLU', 'LeakyReLU', 'Tanh'],
            'optimizers': ['Adam', 'AdamW'],
            'loss_functions': ['MSELoss', 'HuberLoss']
        }
    logger.record_hyperparameter_ranges(hyperparameter_ranges)

    try:
        print("\nPreparing data for hyperparameter optimization...")
        logger.start_data_preparation()

        # Prepare data
        (X_train_tensor, X_test_tensor,
         y_train_mean_tensor, y_test_mean_tensor,
         y_train_std_tensor, y_test_std_tensor,
         scaler_y_mean, scaler_y_std) = prepare_data()

        # Move tensors to device
        X_train_tensor = X_train_tensor.to(device)
        X_test_tensor = X_test_tensor.to(device)
        y_train_mean_tensor = y_train_mean_tensor.to(device)
        y_test_mean_tensor = y_test_mean_tensor.to(device)
        y_train_std_tensor = y_train_std_tensor.to(device)
        y_test_std_tensor = y_test_std_tensor.to(device)

        logger.record_data_info(X_train_tensor, X_test_tensor)
        logger.end_data_preparation()

        def optimize_model_with_rich_progress(model_type, y_train, y_test):
            """
            Optimize a model using the Rich progress bar for visualization.

            Args:
                model_type (str): Type of model ('mean' or 'std').
                y_train (torch.Tensor): Training targets.
                y_test (torch.Tensor): Testing targets.

            Returns:
                dict: Best parameters of the optimized model.
                float: Best score of the optimized model.
            """
            print(f"\nOptimizing {model_type} prediction model with {n_trials} trials...")

            logger.start_optimization(model_type)

            optimizer = ANNHyperparameterOptimizer(
                X_train_tensor, y_train, X_test_tensor, y_test, device, hyperparameter_ranges
            )

            with Progress(
                "[progress.description]{task.description}",
                BarColumn(),
                "[progress.percentage]{task.percentage:>3.0f}%",
                TimeElapsedColumn(),
                TimeRemainingColumn(),
            ) as progress:
                task = progress.add_task(f"[cyan]Optimizing {model_type} model...", total=n_trials)

                def rich_progress_callback(study, trial):
                    progress.advance(task)

                study = optuna.create_study(direction="minimize")
                study.optimize(
                    optimizer.objective,
                    n_trials=n_trials,
                    n_jobs=n_jobs,
                    callbacks=[rich_progress_callback]
                )

            best_params = study.best_params
            best_score = study.best_value

            logger.end_optimization(model_type, best_params, best_score, [])
            with open(os.path.join(output_dir, f'best_params_{model_type}.json'), 'w') as f:
                json.dump(best_params, f, indent=4)

            print(f"Best {model_type} model R² score: {-best_score:.4f}")
            return best_params, best_score

        # Optimize mean prediction model
        best_params_mean, best_score_mean = optimize_model_with_rich_progress('mean', y_train_mean_tensor, y_test_mean_tensor)

        # Optimize standard deviation prediction model
        best_params_std, best_score_std = optimize_model_with_rich_progress('std', y_train_std_tensor, y_test_std_tensor)

        # Save summary
        summary = {
            'mean_model': {
                'best_score': float(-best_score_mean),  # Convert to R²
                'best_params': best_params_mean,
                'n_trials': n_trials
            },
            'std_model': {
                'best_score': float(-best_score_std),  # Convert to R²
                'best_params': best_params_std,
                'n_trials': n_trials
            }
        }
        with open(os.path.join(output_dir, 'optimization_summary.json'), 'w') as f:
            json.dump(summary, f, indent=4)

        logger.save_all()
        logger.print_summary()

        print("\nHyperparameter optimization completed successfully!")
        print("Results saved in:", output_dir)
        return True

    except Exception as e:
        print(f"\nError during hyperparameter optimization: {e}")
        return False


if __name__ == "__main__":

    hyperparameter_ranges = {
            'n_layers': (1, 6),
            'n_units': (32, 512),
            'learning_rate': (1e-4, 1e-1),
            'batch_size': (16, 128),
            'max_epochs': (50, 500),
            'activations': ['ReLU', 'LeakyReLU', 'Tanh'],
            'optimizers': ['Adam', 'AdamW'],
            'loss_functions': ['MSELoss', 'HuberLoss']
        }

    run_hyperopt_ann(hyperparameter_ranges)
