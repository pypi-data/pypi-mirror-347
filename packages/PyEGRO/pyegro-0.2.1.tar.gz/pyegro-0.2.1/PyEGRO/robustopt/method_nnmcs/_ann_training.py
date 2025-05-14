import os
import json
import warnings
import joblib
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt
from matplotlib import rcParams
from rich.progress import Progress
from gpytorch.utils.warnings import GPInputWarning

# Suppress warnings
warnings.filterwarnings("ignore", category=GPInputWarning)


# Set plotting style
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Times New Roman']
rcParams['font.size'] = 14
rcParams['axes.titlesize'] = 14
rcParams['axes.labelsize'] = 14

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

class DataPreparation:
    @staticmethod
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
        
        try:
            # Try to load existing scalers
            scaler_X = joblib.load('RESULT_MODEL_ANN/scaler_X_stage2.pkl')
            scaler_y_mean = joblib.load('RESULT_MODEL_ANN/scaler_y_mean_stage2.pkl')
            scaler_y_std = joblib.load('RESULT_MODEL_ANN/scaler_y_std_stage2.pkl')
        except:
            raise RuntimeError(
                "Scalers not found. Please run hyperparameter optimization first."
            )
        
        # Transform data using loaded scalers
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

class ModelTrainer:
    def __init__(self, X_train, y_train, X_test, y_test, scaler_y, device, model_type='mean'):
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.scaler_y = scaler_y
        self.device = device
        self.model_type = model_type
        
        # Load optimized parameters
        with open(f'RESULT_MODEL_ANN/best_params_{model_type}.json', 'r') as f:
            self.params = json.load(f)
        
        # Initialize model and training components
        self.model = self._build_model()
        self.optimizer = self._get_optimizer()
        self.criterion = nn.MSELoss()
        self.train_loader = self._create_dataloader()
        
        # Initialize lists to store loss values
        self.train_losses = []
        self.val_losses = []
        self.epochs_trained = []
    
    def _build_model(self):
        hidden_layers = [self.params[f'n_units_l{i}'] 
                        for i in range(self.params['n_layers'])]
        activation = getattr(nn, self.params['activation'])()
        
        model = ANNModel(
            input_size=self.X_train.shape[1],
            hidden_layers=hidden_layers,
            output_size=1,
            activation=activation
        ).to(self.device)
        
        return model
    
    def _get_optimizer(self):
        optimizer_class = getattr(optim, self.params['optimizer'])
        return optimizer_class(self.model.parameters(), 
                             lr=self.params['learning_rate'])
    
    def _create_dataloader(self):
        dataset = TensorDataset(self.X_train, self.y_train)
        return DataLoader(dataset, 
                         batch_size=self.params['batch_size'],
                         shuffle=True)
    

    def train(self):
        print(f"\nTraining {self.model_type} prediction model...")
        best_loss = float('inf')
        patience = 10
        epochs_without_improvement = 0

        # Initialize Progress Bar
        with Progress() as progress:
            task = progress.add_task(f"[cyan]Training {self.model_type} model...", total=self.params['max_epochs'])

            for epoch in range(self.params['max_epochs']):
                # Training
                self.model.train()
                train_loss = 0
                for X_batch, y_batch in self.train_loader:
                    self.optimizer.zero_grad()
                    output = self.model(X_batch)
                    loss = self.criterion(output, y_batch)
                    loss.backward()
                    self.optimizer.step()
                    train_loss += loss.item()

                # Calculate average training loss
                avg_train_loss = train_loss / len(self.train_loader)

                # Validation
                self.model.eval()
                with torch.no_grad():
                    val_output = self.model(self.X_test)
                    val_loss = self.criterion(val_output, self.y_test).item()

                # Store losses
                self.train_losses.append(avg_train_loss)
                self.val_losses.append(val_loss)
                self.epochs_trained.append(epoch + 1)

                # Log progress
                progress.update(task, advance=1, description=f"Epoch {epoch + 1} | Train Loss: {avg_train_loss:.6f} | Val Loss: {val_loss:.6f}")

                # Early stopping logic
                if val_loss < best_loss:
                    best_loss = val_loss
                    epochs_without_improvement = 0
                    # Save best model
                    if self.device.type == 'cuda':
                        model_cpu = self.model.cpu()
                        torch.save(model_cpu.state_dict(), 
                                f'RESULT_MODEL_ANN/mlp_model_{self.model_type}.pth')
                        self.model = self.model.to(self.device)
                    else:
                        torch.save(self.model.state_dict(), 
                                f'RESULT_MODEL_ANN/mlp_model_{self.model_type}.pth')
                else:
                    epochs_without_improvement += 1

                if epochs_without_improvement >= patience:
                    progress.update(task, description=f"[bold red]Early stopping at epoch {epoch + 1}")
                    break

            # Save loss metrics and plot training history after training completes or early stopping
            self._save_loss_metrics()
            self._plot_training_history()


    def _save_loss_metrics(self):
        """Save training and validation losses to CSV"""
        loss_df = pd.DataFrame({
            'epoch': self.epochs_trained,
            'train_loss': self.train_losses,
            'val_loss': self.val_losses
        })
        
        # Create directory if it doesn't exist
        os.makedirs('RESULT_MODEL_ANN/training_history', exist_ok=True)
        loss_df.to_csv(
            f'RESULT_MODEL_ANN/training_history/{self.model_type}_loss_history.csv',
            index=False
        )
    
    def _plot_training_history(self):
        """Plot training and validation loss history"""
        plt.figure(figsize=(6, 3))
        plt.plot(self.epochs_trained, self.train_losses, 
                label='Training Loss', color='blue', linewidth=1.5)
        plt.plot(self.epochs_trained, self.val_losses, 
                label='Validation Loss', color='red', linewidth=1.5)
        
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.title(f'{self.model_type.capitalize()} Model Training History')
        plt.legend()
        plt.grid(True, alpha=0.3, linestyle='--')
        
        # Save plot
        plt.savefig(
            f'RESULT_MODEL_ANN/training_history/{self.model_type}_loss_history.png',
            dpi=300, bbox_inches='tight'
        )
        plt.close()
    
    def evaluate(self):
        """Evaluate model performance"""
        self.model.eval()
        with torch.no_grad():
            # Get predictions
            train_pred = self.model(self.X_train).cpu().numpy()
            test_pred = self.model(self.X_test).cpu().numpy()
            
            # Transform back to original scale
            train_pred = self.scaler_y.inverse_transform(train_pred)
            test_pred = self.scaler_y.inverse_transform(test_pred)
            y_train = self.scaler_y.inverse_transform(self.y_train.cpu().numpy())
            y_test = self.scaler_y.inverse_transform(self.y_test.cpu().numpy())
            
            # Calculate metrics
            metrics = {
                'r2_train': r2_score(y_train, train_pred),
                'r2_test': r2_score(y_test, test_pred),
                'rmse_train': np.sqrt(mean_squared_error(y_train, train_pred)),
                'rmse_test': np.sqrt(mean_squared_error(y_test, test_pred))
            }
            
            return metrics, (y_train, train_pred, y_test, test_pred)

    def plot_results(self, results):
        """Plot and save performance figures"""
        y_train, train_pred, y_test, test_pred = results
        
        # Plot training results
        self._create_performance_plot(
            y_train, train_pred, 
            f'{self.model_type}_train_r2.png', 
            'Training Data'
        )
        
        # Plot testing results
        self._create_performance_plot(
            y_test, test_pred, 
            f'{self.model_type}_test_r2.png', 
            'Testing Data'
        )
        
    def _create_performance_plot(self, y_true, y_pred, filename, title_prefix):
        plt.figure(figsize=(6, 5))
        plt.scatter(y_true, y_pred, alpha=0.5, color='b')
        
        # Perfect prediction line
        lims = [
            min(min(y_true), min(y_pred)),
            max(max(y_true), max(y_pred))
        ]
        plt.plot(lims, lims, 'k--', alpha=0.75)
        
        plt.xlabel('True Values')
        plt.ylabel('Predicted Values')
        r2 = r2_score(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        plt.title(f'{title_prefix}\nR² = {r2:.4f}, RMSE = {rmse:.4f}')
        plt.grid(True, alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        # Change the save directory to RESULT_MODEL_ANN/performance_plots
        os.makedirs('RESULT_MODEL_ANN/performance_plots', exist_ok=True)
        plt.savefig(f'RESULT_MODEL_ANN/performance_plots/{filename}', 
                    dpi=300, bbox_inches='tight')
        plt.close()


def run_training_ann():
    """
    Run the training of ANN models.
    This function is designed to be imported and used by other modules.
    
    Returns:
        bool: True if training was successful, False otherwise
    """
    try:
        # Set up device
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Check if hyperparameter optimization has been performed
        if not os.path.exists('RESULT_MODEL_ANN/best_params_mean.json') or \
           not os.path.exists('RESULT_MODEL_ANN/best_params_std.json'):
            raise FileNotFoundError(
                "Hyperparameter optimization results not found. "
                "Please run hyperparameter optimization first."
            )
        
        # Prepare data using existing scalers
        # print("\nPreparing data for training...")
        (X_train_tensor, X_test_tensor,
         y_train_mean_tensor, y_test_mean_tensor,
         y_train_std_tensor, y_test_std_tensor,
         scaler_y_mean, scaler_y_std) = DataPreparation.prepare_data()
        
        # Move tensors to device
        X_train_tensor = X_train_tensor.to(device)
        X_test_tensor = X_test_tensor.to(device)
        y_train_mean_tensor = y_train_mean_tensor.to(device)
        y_test_mean_tensor = y_test_mean_tensor.to(device)
        y_train_std_tensor = y_train_std_tensor.to(device)
        y_test_std_tensor = y_test_std_tensor.to(device)
        
        # Train and evaluate mean prediction model
        mean_trainer = ModelTrainer(
            X_train_tensor, y_train_mean_tensor,
            X_test_tensor, y_test_mean_tensor,
            scaler_y_mean, device, 'mean'
        )
        mean_trainer.train()
        mean_metrics, mean_results = mean_trainer.evaluate()
        mean_trainer.plot_results(mean_results)
        
        # Train and evaluate standard deviation prediction model
        std_trainer = ModelTrainer(
            X_train_tensor, y_train_std_tensor,
            X_test_tensor, y_test_std_tensor,
            scaler_y_std, device, 'std'
        )
        std_trainer.train()
        std_metrics, std_results = std_trainer.evaluate()
        std_trainer.plot_results(std_results)
        
        # Print final metrics
        print("\nFinal Model Performance:")
        print("\nMean Prediction Model:")
        for metric, value in mean_metrics.items():
            print(f"{metric}: {value:.4f}")
        
        print("\nStandard Deviation Prediction Model:")
        for metric, value in std_metrics.items():
            print(f"{metric}: {value:.4f}")
        
        return True
        
    except Exception as e:
        print(f"\nError during model training: {str(e)}")
        return False

if __name__ == "__main__":
    run_training_ann()