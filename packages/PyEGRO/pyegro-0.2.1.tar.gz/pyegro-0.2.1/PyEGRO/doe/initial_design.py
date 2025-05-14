# initial_design.py

from typing import List, Dict, Union, Optional, Callable
import os
import numpy as np
import pandas as pd
import json
from dataclasses import dataclass, asdict
from datetime import datetime

from rich.progress import Progress, TextColumn, BarColumn
from rich.progress import TaskProgressColumn, TimeRemainingColumn
from rich.progress import TimeElapsedColumn, SpinnerColumn
from rich.console import Console
from rich.table import Table

from .sampling import AdaptiveDistributionSampler, Variable

class InitialDesign:
    def __init__(
        self,
        output_dir: str = 'DATA_PREPARATION',
        show_progress: bool = True,
        show_result: bool = True,
        sampling_method: str = 'lhs',
        sampling_criterion: Optional[str] = 'maximin',
        results_filename: str = 'training_data'
    ):
        if sampling_method not in AdaptiveDistributionSampler.SAMPLING_METHODS:
            raise ValueError(f"Unsupported sampling method: {sampling_method}. "
                        f"Available methods: {AdaptiveDistributionSampler.SAMPLING_METHODS}")
            
        self.output_dir = output_dir
        self.show_progress = show_progress
        self.show_result = show_result
        self.sampling_method = sampling_method
        self.sampling_criterion = sampling_criterion
        self.results_filename = results_filename
        
        self.variables = []
        self.design_info = {}
        os.makedirs(output_dir, exist_ok=True)
        
    def add_design_variable(
        self,
        name: str,
        range_bounds: List[float],
        cov: Optional[float] = None,
        std: Optional[float] = None,
        delta: Optional[float] = None,
        distribution: str = 'normal',
        description: str = ''
    ):
        """
        Add a design variable to the experiment.
        
        Args:
            name: Name of the variable
            range_bounds: [min, max] bounds for the variable
            cov: Coefficient of variation (std/mean) for uncertain variables
            std: Standard deviation for uncertain variables (alternative to cov)
            delta: Half-width for uniform distribution (for design variables with uncertainty)
            distribution: Distribution type ('normal', 'uniform', 'lognormal')
            description: Variable description
            
        Note:
            For uncertain variables, specify exactly one of: cov, std, or delta
        """
        # Validation to ensure only one uncertainty parameter is provided
        params_provided = sum(1 for p in [cov, std, delta] if p is not None)
        if params_provided > 1:
            raise ValueError("Specify only one of: cov, std, or delta")
        
        variable = Variable(
            name=name,
            vars_type='design_vars',
            range_bounds=range_bounds,
            cov=cov,
            std=std,
            delta=delta,
            distribution=distribution,
            description=description
        )
        self.variables.append(variable)
        
    def add_env_variable(
        self,
        name: str,
        distribution: str,
        description: str = '',
        mean: Optional[float] = None,
        cov: Optional[float] = None,
        std: Optional[float] = None,
        low: Optional[float] = None,
        high: Optional[float] = None,
        min: Optional[float] = None,
        max: Optional[float] = None
    ):
        """
        Add an environmental variable to the experiment.
        
        Args:
            name: Name of the variable
            distribution: Distribution type ('normal', 'uniform', 'lognormal')
            description: Variable description
            mean: Mean value for normal/lognormal distributions
            cov: Coefficient of variation for normal/lognormal distributions
            std: Standard deviation for normal/lognormal distributions (alternative to cov)
            low: Lower bound for uniform distribution
            high: Upper bound for uniform distribution
            min: Lower bound for uniform distribution (alternative to low)
            max: Upper bound for uniform distribution (alternative to high)
            
        Note:
            For normal/lognormal distributions, provide mean and either cov or std
            For uniform distributions, provide either low/high or min/max
        """
        # Validation for parameters
        if distribution in ['normal', 'lognormal']:
            if mean is None:
                raise ValueError(f"{distribution} distribution requires mean value")
            
            # Check that exactly one of cov or std is provided
            if (cov is None and std is None) or (cov is not None and std is not None):
                raise ValueError(f"{distribution} distribution requires exactly one of: cov or std")
                
        elif distribution == 'uniform':
            # Support both low/high and min/max
            if low is None:
                low = min
            if high is None:
                high = max
                
            if low is None or high is None:
                raise ValueError("Uniform distribution requires low/high bounds")
        
        # For backward compatibility, use both min/max and low/high
        if min is None and low is not None:
            min = low
        if max is None and high is not None:
            max = high
            
        variable = Variable(
            name=name,
            vars_type='env_vars',
            distribution=distribution,
            description=description,
            mean=mean,
            cov=cov,
            std=std,
            low=low,
            high=high,
            min=min,
            max=max
        )
        self.variables.append(variable)
        
    def save(self, filename: str = "data_info"):
        """
        Save design configuration to JSON file.
        
        Args:
            filename: Base name for the JSON file (without extension)
            
        The saved JSON will contain:
            - variables: List of all variable configurations
            - variable_names: List of variable names
            - input_bound: Calculated bounds for each variable
            - sampling_config: Sampling method and criterion
            - metadata: Creation time and variable counts
        """
        # Calculate input bounds for all variables
        input_bound = []
        for var in self.variables:
            if var.vars_type == 'design_vars':
                input_bound.append(var.range_bounds)
            elif var.distribution == 'uniform':
                # Use min/max if available, otherwise low/high
                min_val = var.min if var.min is not None else var.low
                max_val = var.max if var.max is not None else var.high
                input_bound.append([min_val, max_val])
            elif var.distribution in ['normal', 'lognormal']:
                # Calculate bounds based on mean and uncertainty
                if var.std is not None:
                    std = var.std
                elif var.cov is not None:
                    std = var.mean * var.cov
                else:
                    std = 0.1 * var.mean  # Fallback
                    
                lower = var.mean - 3*std  # 3 sigma rule
                upper = var.mean + 3*std
                input_bound.append([lower, upper])

        # Prepare the complete configuration
        self.design_info = {
            'variables': [self._variable_to_dict(var) for var in self.variables],
            'variable_names': [var.name for var in self.variables],
            'input_bound': input_bound,
            'sampling_config': {
                'method': self.sampling_method,
                'criterion': self.sampling_criterion,
            },
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'total_variables': len(self.variables)
            }
        }
        
        filepath = os.path.join(self.output_dir, f"{filename}.json")
        with open(filepath, 'w') as f:
            json.dump(self.design_info, f, indent=4)
            
        if self.show_result:
            print(f"\nDesign configuration saved to: {filepath}")
    
    def _variable_to_dict(self, var: Variable) -> Dict:
        """Convert Variable object to dictionary, removing None values."""
        var_dict = {}
        for k, v in asdict(var).items():
            if v is not None:
                var_dict[k] = v
        return var_dict

    def load(self, filename: str):
        """
        Load design configuration from a JSON file.
        
        Args:
            filename: Base name of the JSON file (without extension)
        """
        filepath = os.path.join(self.output_dir, f"{filename}.json")
        with open(filepath, 'r') as f:
            config = json.load(f)
            
        self.variables = []
        
        for var_dict in config['variables']:
            if var_dict['vars_type'] == 'design_vars':
                self.add_design_variable(
                    name=var_dict['name'],
                    range_bounds=var_dict['range_bounds'],
                    cov=var_dict.get('cov'),
                    std=var_dict.get('std'),
                    delta=var_dict.get('delta'),
                    distribution=var_dict.get('distribution', 'normal'),
                    description=var_dict.get('description', '')
                )
            else:
                self.add_env_variable(
                    name=var_dict['name'],
                    distribution=var_dict['distribution'],
                    description=var_dict.get('description', ''),
                    mean=var_dict.get('mean'),
                    cov=var_dict.get('cov'),
                    std=var_dict.get('std'),
                    low=var_dict.get('low'),
                    high=var_dict.get('high'),
                    min=var_dict.get('min'),
                    max=var_dict.get('max')
                )
                
        sampling_config = config['sampling_config']
        self.sampling_method = sampling_config['method']
        self.sampling_criterion = sampling_config['criterion']
    
    def run(
        self,
        objective_function: Callable,
        num_samples: int,
        save_results: bool = True
    ):
        """
        Run the sampling process and evaluate objective function.
        
        Args:
            objective_function: Function to evaluate samples
            num_samples: Number of samples to generate
            save_results: Whether to save results to file
                
        Returns:
            DataFrame containing samples and objective values
        """
        sampler = AdaptiveDistributionSampler()
        console = Console()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            TextColumn("[cyan]{task.fields[info]}"),
            disable=not self.show_progress
        ) as progress:
            
            task1 = progress.add_task(
                "[white]Generating design points : ",
                total=1,
                info="Sampling..."
            )
            
            all_samples = sampler.generate_all_samples(
                self.variables,
                num_samples,
                method=self.sampling_method,
                criterion=self.sampling_criterion
            )
            
            df = pd.DataFrame(
                all_samples,
                columns=[var.name for var in self.variables]
            )
            
            progress.update(task1, advance=1, info="Complete")
            
            task2 = progress.add_task(
                "[white]Evaluating objective function : ",
                total=len(df),
                info="Processing..."
            )
            
            results = []
            for i, row in enumerate(df.values):
                y = objective_function(row.reshape(1, -1))
                if isinstance(y, (np.ndarray, list)):
                    y = y.item() if hasattr(y, 'item') else y[0]
                results.append(y)
                
                progress.update(
                    task2,
                    advance=1,
                    info=f"Sample {i+1}/{len(df)}"
                )
            
            df['y'] = results
            

        if save_results:
            # Make sure we have design info content from save() method
            if not self.design_info:
                # If design_info wasn't created yet, create it now
                self.save('data_info')
                
            # Update design info with the actual number of samples
            self.design_info['num_samples'] = num_samples
            
            # Save training data with filename from class attribute
            results_file = os.path.join(self.output_dir, f'{self.results_filename}.csv')
            df.to_csv(results_file, index=False)
            
            # Re-save data_info.json with updated sample count
            info_file = os.path.join(self.output_dir, 'data_info.json')
            with open(info_file, 'w') as f:
                json.dump(self.design_info, f, indent=4)
            
            if self.show_result:
                console.print(f"\nResults saved to: {results_file}")
                self.print_summary(df)
                
        return df
        
    
    def print_summary(self, df: pd.DataFrame):
        """
        Print summary statistics of the generated samples and results.
        
        Args:
            df: DataFrame containing samples and objective values
        """
        if not self.show_result:
            return
            
        console = Console()
        table = Table(title="Summary Statistics", show_header=True, header_style="bold")
        
        table.add_column("Statistic")
        for col in df.columns:
            table.add_column(col)
            
        stats = df.describe()
        for stat in stats.index:
            row = [stat]
            for col in stats.columns:
                val = stats.loc[stat, col]
                row.append(f"{val:.6f}" if isinstance(val, float) else str(val))
            table.add_row(*row)
            
        console.print("\n")
        console.print(table)
        console.print("\n")


if __name__ == "__main__":
    import numpy as np

    # Define the true function as a 2D function
    def true_function(x):
        X1, X2 = x[:, 0], x[:, 1]
        a1, x1, y1, sigma_x1, sigma_y1 = 100, 3, 2.1, 3, 3  # Lower and more sensitive
        a2, x2, y2, sigma_x2, sigma_y2 = 150, -1.5, -1.2, 1, 1  # Higher and more robust
        f = -(
            a1 * np.exp(-((X1 - x1) ** 2 / (2 * sigma_x1 ** 2) + (X2 - y1) ** 2 / (2 * sigma_y1 ** 2))) +
            a2 * np.exp(-((X1 - x2) ** 2 / (2 * sigma_x2 ** 2) + (X2 - y2) ** 2 / (2 * sigma_y2 ** 2))) - 200
        )
        return f
    
    # =================================================
    # Example 1: Basic LHS Design
    # =================================================
    print("\nExample 1: Basic LHS Design")
    print("-" * 50)
    
    # Create design with LHS sampling
    design_lhs = InitialDesign(
        output_dir='DATA_PREPARATION_LHS',
        sampling_method='lhs',
        sampling_criterion='maximin',
        show_progress=True
    )
    
    # Add design variables
    design_lhs.add_design_variable(
        name='x1',
        range_bounds=[-5, 5],
        cov=0.1,
        description='first design variable'
    )
    
    design_lhs.add_design_variable(
        name='x2',
        range_bounds=[-6, 6],
        cov=0.1,
        description='second design variable'
    )
    
    # Save configuration
    design_lhs.save("design_config_lhs")
    
    # Run sampling
    results_lhs = design_lhs.run(
        objective_function=true_function,
        num_samples=50
    )

    # =================================================
    # Example 2: Using standard deviation instead of CoV
    # =================================================
    print("\nExample 2: Using standard deviation")
    print("-" * 50)
    
    design_std = InitialDesign(
        output_dir='DATA_PREPARATION_STD',
        sampling_method='lhs',
        show_progress=True
    )
    
    # Add variables with std instead of cov
    design_std.add_design_variable(
        name='x1',
        range_bounds=[-5, 5],
        std=0.5,  # Using std directly
        description='first design variable'
    )
    
    design_std.add_design_variable(
        name='x2',
        range_bounds=[-6, 6],
        std=0.6,  # Using std directly
        description='second design variable'
    )
    
    # Save configuration
    design_std.save("design_config_std")
    
    # Run sampling
    results_std = design_std.run(
        objective_function=true_function,
        num_samples=50
    )

    # =================================================
    # Example 3: Using delta for uniform uncertainty
    # =================================================
    print("\nExample 3: Using delta for uniform uncertainty")
    print("-" * 50)
    
    design_delta = InitialDesign(
        output_dir='DATA_PREPARATION_DELTA',
        sampling_method='lhs',
        show_progress=True
    )
    
    # Add variables with delta and uniform distribution
    design_delta.add_design_variable(
        name='x1',
        range_bounds=[-5, 5],
        delta=0.2,  # Half-width for uniform
        distribution='uniform',  # Using uniform distribution
        description='first design variable with uniform uncertainty'
    )
    
    design_delta.add_design_variable(
        name='x2',
        range_bounds=[-6, 6],
        delta=0.3,  # Half-width for uniform
        distribution='uniform',
        description='second design variable with uniform uncertainty'
    )
    
    # Save configuration
    design_delta.save("design_config_delta")
    
    # Run sampling
    results_delta = design_delta.run(
        objective_function=true_function,
        num_samples=50
    )

    # =================================================
    # Example 4: Normal env_vars with std
    # =================================================
    print("\nExample 4: Normal env_vars with std")
    print("-" * 50)
    
    design_env = InitialDesign(
        output_dir='DATA_PREPARATION_ENV_STD',
        sampling_method='lhs',
        show_progress=True
    )
    
    # Add design variable
    design_env.add_design_variable(
        name='x1',
        range_bounds=[-5, 5],
        cov=0.1,
        description='design variable'
    )
    
    # Add environmental variable with std
    design_env.add_env_variable(
        name='noise',
        distribution='normal',
        mean=0,
        std=0.5,  # Using std directly instead of cov
        description='measurement noise'
    )
    
    # Save configuration
    design_env.save("design_config_env_std")
    
    # Run sampling
    results_env = design_env.run(
        objective_function=true_function,
        num_samples=50
    )