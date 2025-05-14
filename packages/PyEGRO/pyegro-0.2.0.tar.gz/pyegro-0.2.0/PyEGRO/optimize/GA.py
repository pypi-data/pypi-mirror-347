
"""
PyEGRO Deterministic Optimization Module - Genetic Algorithm (GA) Approach
-----------------------------------------------------------------------
This module implements deterministic optimization using Genetic Algorithm for
single-objective optimization problems with constraint handling.
"""

import os
import numpy as np
import pandas as pd
import time
from typing import List, Dict, Optional, Any, Union, Tuple, Callable

from pymoo.core.problem import Problem
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.optimize import minimize
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.operators.sampling.lhs import LHS
from pymoo.termination import get_termination


class DeterministicOptimizationProblemGA(Problem):
    """Single-objective optimization problem using Genetic Algorithm with constraint handling."""
    
    def __init__(self, 
                 variables: List[Dict], 
                 true_func: Optional[callable] = None,
                 model_handler: Optional[Any] = None,
                 constraint_funcs: Optional[List[Callable]] = None,
                 constraint_models: Optional[List[Any]] = None,
                 constraint_penalty: float = 1e6,
                 batch_size: int = 1000,
                 minimize_objective: bool = True):
        """
        Initialize the deterministic optimization problem.

        Args:
            variables: List of variable definitions
            true_func: True objective function (if using direct evaluation)
            model_handler: Handler for surrogate model evaluations
            constraint_funcs: List of constraint functions (g(x) <= 0 for feasibility)
            constraint_models: List of surrogate models for constraints
            constraint_penalty: Penalty factor for constraint violations
            batch_size: Batch size for model evaluations
            minimize_objective: Whether to minimize (True) or maximize (False) the objective
        """
        if true_func is None and model_handler is None:
            raise ValueError("Either true_func or model_handler must be provided")
            
        self.true_func = true_func
        self.model_handler = model_handler
        self.variables = variables
        self.batch_size = batch_size
        self.minimize_objective = minimize_objective
        self.constraint_funcs = constraint_funcs or []
        self.constraint_models = constraint_models or []
        self.constraint_penalty = constraint_penalty
        
        # Filter design variables
        self.design_vars = [var for var in variables if var['vars_type'] == 'design_vars']
        if not self.design_vars:
            raise ValueError("No design variables found in problem definition")
        
        # Set optimization bounds
        xl = np.array([var['range_bounds'][0] for var in self.design_vars])
        xu = np.array([var['range_bounds'][1] for var in self.design_vars])
        
        # Determine number of constraints
        n_constr = len(self.constraint_funcs) if self.constraint_funcs else 0
        
        # Initialize problem
        super().__init__(
            n_var=len(self.design_vars),
            n_obj=1,  # Single objective
            n_constr=n_constr,
            xl=xl,
            xu=xu
        )
            
    def _evaluate(self, X, out, *args, **kwargs):
        """Evaluate objective function and constraints."""
        X = np.atleast_2d(X)
        
        # For single-objective optimization
        if self.true_func is not None:
            # Direct evaluation with true function
            if self.minimize_objective:
                out["F"] = self.true_func(X)
            else:
                out["F"] = -self.true_func(X)  # Negate for maximization
                
            # Evaluate constraints if provided
            if self.constraint_funcs:
                G = np.zeros((X.shape[0], len(self.constraint_funcs)))
                for i, constraint_func in enumerate(self.constraint_funcs):
                    G[:, i] = constraint_func(X)
                out["G"] = G
        else:
            # Using surrogate model
            if hasattr(self.model_handler, 'predict_with_constraints'):
                # Model handler supports both objective and constraints
                F, G = self.model_handler.predict_with_constraints(X, batch_size=self.batch_size)
                
                if self.minimize_objective:
                    out["F"] = F
                else:
                    out["F"] = -F  # Negate for maximization
                    
                if G is not None:
                    out["G"] = G
            else:
                # Traditional predict method (objective only)
                predict_mean, _ = self.model_handler.predict(X, batch_size=self.batch_size)
                
                if self.minimize_objective:
                    out["F"] = predict_mean
                else:
                    out["F"] = -predict_mean  # Negate for maximization
                
                # Evaluate constraint models if provided
                if self.constraint_models:
                    G = np.zeros((X.shape[0], len(self.constraint_models)))
                    for i, model in enumerate(self.constraint_models):
                        pred, _ = model.predict(X, batch_size=self.batch_size)
                        G[:, i] = pred.flatten()
                    out["G"] = G


def setup_algorithm(pop_size: int, 
                   sampling_method: str = 'lhs',
                   crossover_prob: float = 0.9,
                   crossover_eta: float = 20,
                   mutation_eta: float = 20) -> GA:
    """
    Setup Genetic Algorithm with standard parameters.
    
    Args:
        pop_size: Population size
        sampling_method: Sampling method ('lhs' or 'random')
        crossover_prob: Crossover probability
        crossover_eta: Crossover distribution index
        mutation_eta: Mutation distribution index
        
    Returns:
        Configured GA algorithm
    """
    # Select sampling method
    if sampling_method.lower() == 'lhs':
        sampling = LHS()
    else:
        sampling = FloatRandomSampling()
    
    return GA(
        pop_size=pop_size,
        sampling=sampling,
        crossover=SBX(prob=crossover_prob, eta=crossover_eta),
        mutation=PM(eta=mutation_eta),
        eliminate_duplicates=True
    )


def run_deterministic_optimization(
    data_info: Dict,
    true_func: Optional[callable] = None,
    model_handler: Optional[Any] = None,
    constraint_funcs: Optional[List[Callable]] = None,
    constraint_models: Optional[List[Any]] = None,
    constraint_penalty: float = 1e6,
    pop_size: int = 100,
    n_gen: int = 100,
    termination: Union[str, Dict, Tuple] = 'n_gen',
    sampling_method: str = 'lhs',
    crossover_prob: float = 0.9,
    crossover_eta: float = 15,
    mutation_eta: float = 20,
    minimize_objective: bool = True,
    show_info: bool = True,
    verbose: bool = False) -> Dict:
    """
    Run deterministic optimization using GA.
    
    Args:
        data_info: Problem definition data
        true_func: True objective function (if using direct evaluation)
        model_handler: Handler for surrogate model evaluations
        constraint_funcs: List of constraint functions (g(x) <= 0 for feasibility)
        constraint_models: List of surrogate models for constraints
        constraint_penalty: Penalty factor for constraint violations
        pop_size: Population size for GA
        n_gen: Number of generations
        termination: Termination criteria:
                     - 'n_gen': Run for fixed number of generations
                     - ('n_gen', n): Run for n generations
                     - ('ftol', tol, n_skip): Terminate when change in fitness is below tol
                     - ('xtol', tol): Terminate when change in variables is below tol
        sampling_method: Method to generate initial population ('lhs' or 'random')
        crossover_prob: Probability of crossover
        crossover_eta: Crossover distribution index
        mutation_eta: Mutation distribution index
        minimize_objective: Whether to minimize (True) or maximize (False) the objective
        show_info: Whether to display problem information
        verbose: Whether to print detailed progress
        
    Returns:
        Dictionary containing optimization results
    """
    if show_info:
        print_variable_information(data_info['variables'])
        print("\nOptimization Configuration:")
        print("-" * 50)
        print(f"Evaluation type: {'Direct Function' if true_func else 'Surrogate Model'}")
        print(f"Optimization type: {'Minimization' if minimize_objective else 'Maximization'}")
        print(f"Constraint handling: {'Yes' if constraint_funcs or constraint_models else 'No'}")
        print(f"Population size: {pop_size}")
        if termination == 'n_gen' or (isinstance(termination, tuple) and termination[0] == 'n_gen'):
            print(f"Number of generations: {n_gen}")
        else:
            print(f"Termination criteria: {termination}")
        print(f"Sampling method: {sampling_method}")
        print("-" * 50 + "\n")
    
    start_time = time.time()
    
    # Setup problem
    problem = DeterministicOptimizationProblemGA(
        variables=data_info['variables'],
        true_func=true_func,
        model_handler=model_handler,
        constraint_funcs=constraint_funcs,
        constraint_models=constraint_models,
        constraint_penalty=constraint_penalty,
        minimize_objective=minimize_objective
    )
    
    # Setup optimization
    algorithm = setup_algorithm(
        pop_size=pop_size, 
        sampling_method=sampling_method,
        crossover_prob=crossover_prob,
        crossover_eta=crossover_eta,
        mutation_eta=mutation_eta
    )
    
    # Setup termination
    if termination == 'n_gen':
        term_criterion = get_termination("n_gen", n_gen)
    elif isinstance(termination, tuple) and termination[0] == 'n_gen':
        term_criterion = get_termination("n_gen", termination[1])
    elif isinstance(termination, tuple) and termination[0] == 'ftol':
        if len(termination) >= 3:
            term_criterion = get_termination("ftol", termination[1], n_skip=termination[2])
        else:
            term_criterion = get_termination("ftol", termination[1])
    elif isinstance(termination, tuple) and termination[0] == 'xtol':
        term_criterion = get_termination("xtol", termination[1])
    else:
        term_criterion = get_termination("n_gen", n_gen)
    
    # Setup metric tracking
    class OptimizationCallback:
        def __init__(self):
            self.start_time = time.time()
            self.best_f = []
            self.n_evals = []
            self.elapsed_times = []
            self.feasible_solutions = []
            self.last_gen = -1
            
        def __call__(self, algorithm):
            if algorithm.n_gen > self.last_gen and show_info:
                if isinstance(termination, tuple) and termination[0] == 'n_gen':
                    max_gen = termination[1]
                else:
                    max_gen = n_gen
                    
                # Fix progress calculation to max at 100%
                progress = min((algorithm.n_gen + 1) / max_gen * 100, 100)
                elapsed = time.time() - self.start_time
                
                # Check if we have constraint values
                has_constraints = hasattr(algorithm.pop, "G") and algorithm.pop.get("G") is not None
                n_feasible = 0
                
                if has_constraints:
                    # Count feasible solutions (all constraints <= 0)
                    g_vals = algorithm.pop.get("G")
                    feasible_mask = np.all(g_vals <= 0, axis=1)
                    n_feasible = np.sum(feasible_mask)
                    
                    if n_feasible > 0:
                        # Get best feasible solution
                        feasible_f = algorithm.pop.get("F")[feasible_mask]
                        best_f = np.min(feasible_f)
                    else:
                        # If no feasible solutions, report best overall
                        best_f = algorithm.pop.get("F").min()
                else:
                    best_f = algorithm.pop.get("F").min()
                
                if algorithm.n_gen < max_gen:  # Only show progress for generations within limit
                    if has_constraints:
                        print(f"Progress: {progress:6.1f}% | Gen: {algorithm.n_gen + 1:3d}/{max_gen:3d} | " 
                              f"Best: {best_f:.6f} | Feasible: {n_feasible}/{algorithm.pop.size} | Time: {elapsed:6.1f}s")
                    else:
                        print(f"Progress: {progress:6.1f}% | Generation: {algorithm.n_gen + 1:3d}/{max_gen:3d} | "
                              f"Best fitness: {best_f:.6f} | Time: {elapsed:6.1f}s")
                self.last_gen = algorithm.n_gen
            
            elapsed = time.time() - self.start_time
            
            # Record best feasible solution if constraints exist
            if hasattr(algorithm.pop, "G") and algorithm.pop.get("G") is not None:
                g_vals = algorithm.pop.get("G")
                feasible_mask = np.all(g_vals <= 0, axis=1)
                n_feasible = int(np.sum(feasible_mask))
                self.feasible_solutions.append(n_feasible)
            else:
                # If no constraint info, all solutions are "feasible"
                self.feasible_solutions.append(algorithm.pop.size)
                        
            self.best_f.append(algorithm.pop.get("F").min())
            self.n_evals.append(algorithm.evaluator.n_eval)
            self.elapsed_times.append(elapsed)
            
    callback = OptimizationCallback()
    
    # Run optimization
    res = minimize(
        problem,
        algorithm,
        term_criterion,
        callback=callback,
        seed=42,
        verbose=verbose
    )
    
    total_time = time.time() - start_time
    
    # Process results based on constraints
    if hasattr(res, "G") and res.G is not None and res.X is not None:
        # We have constraint values and solutions
        G = res.G
        F = res.F
        X = res.X
        
        # Make sure F is an array
        if np.isscalar(F):
            F = np.array([F])
        
        # Handle single result case
        if X.ndim == 1 or (isinstance(X, np.ndarray) and X.shape[0] == 1):
            # Only one solution - check if it's feasible
            if G.ndim == 0:  # Single constraint, single solution
                is_feasible = G <= 0
            elif G.ndim == 1 and len(G) == 1:  # Single solution with multiple constraints
                is_feasible = G[0] <= 0
            elif G.ndim == 1:  # Multiple constraints for single solution
                is_feasible = np.all(G <= 0)
            else:
                is_feasible = np.all(G[0] <= 0)  # First solution's constraints
            
            best_x = X if X.ndim == 1 else X[0]
            best_f = F[0]
        else:
            # Multiple solutions
            if G.ndim == 1:  # Only one constraint type
                feasible_mask = G <= 0
            else:  # Multiple constraints
                feasible_mask = np.all(G <= 0, axis=1)
            
            n_feasible = np.sum(feasible_mask)
            
            if n_feasible > 0:
                # Get best feasible solution
                feasible_idx = np.where(feasible_mask)[0]
                feasible_f = F[feasible_idx]
                best_idx = feasible_idx[np.argmin(feasible_f)]
                best_x = X[best_idx]
                best_f = F[best_idx]
                is_feasible = True
            else:
                # If no feasible solutions, get best overall
                if len(F) > 0:  # Make sure we have solutions
                    best_idx = np.argmin(F)
                    best_x = X[best_idx]
                    best_f = F[best_idx]
                else:
                    # No valid solutions found
                    best_x = None
                    best_f = None
                is_feasible = False
    elif hasattr(res, "F") and res.F is not None and res.X is not None:
        # No constraint info but we have solutions
        if len(res.F) > 0:
            best_idx = np.argmin(res.F)
            best_x = res.X[best_idx]
            best_f = res.F[best_idx]
        else:
            best_x = None
            best_f = None
        is_feasible = True  # Assume feasible if no constraints
    else:
        # No valid results returned
        print("Warning: Optimization did not return valid results.")
        best_x = None
        best_f = None
        is_feasible = False
    
    # Handle case where no valid solution was found
    if best_x is None:
        print("No valid solution found. Try adjusting constraints or increasing population size.")
        # Create a dummy solution at the middle of the bounds
        lower_bounds = np.array([var['range_bounds'][0] for var in data_info['variables'] 
                        if var['vars_type'] == 'design_vars'])
        upper_bounds = np.array([var['range_bounds'][1] for var in data_info['variables'] 
                        if var['vars_type'] == 'design_vars'])
        best_x = (lower_bounds + upper_bounds) / 2
        best_f = float('inf')  # Set to infinity for minimization
        is_feasible = False

    # Handle both 1D and 2D arrays
    if np.isscalar(best_x) or (isinstance(best_x, np.ndarray) and best_x.ndim == 0):
        best_x = np.array([best_x])
    
    # Convert result if maximization problem
    if not minimize_objective:
        best_f = -best_f
        callback.best_f = [-f for f in callback.best_f]
    
    # Prepare results
    results = {
        'best_solution': best_x,
        'best_fitness': float(best_f),  # Convert to Python float for JSON serialization
        'is_feasible': is_feasible,
        'convergence_history': {
            'n_evals': callback.n_evals,
            'best_f': callback.best_f,
            'elapsed_times': callback.elapsed_times,
            'feasible_solutions': callback.feasible_solutions
        },
        'runtime': total_time,
        'success': res.success
    }

    if show_info:
        print(f"\nOptimization completed in {total_time:.2f} seconds")
        print(f"Best fitness value: {results['best_fitness']:.6f}")
        print(f"Solution feasibility: {'Feasible' if is_feasible else 'Infeasible'}")
        
        # Get design variable names
        design_var_names = [var['name'] for var in data_info['variables'] 
                           if var['vars_type'] == 'design_vars']
        
        # Print best solution
        print("\nBest solution:")
        for i, name in enumerate(design_var_names):
            if i < len(best_x):
                print(f"  {name}: {best_x[i]:.6f}")
            else:
                print(f"  {name}: Value not available")
    
    return results


def save_optimization_results(results: Dict,
                            data_info: Dict,
                            save_dir: str = 'RESULT_GA',
                            minimize_objective: bool = True) -> None:
    """
    Save optimization results and create visualizations.
    
    Args:
        results: Optimization results dictionary
        data_info: Problem definition data
        save_dir: Directory to save results
        minimize_objective: Whether the objective was minimized or maximized
    """
    os.makedirs(save_dir, exist_ok=True)
    
    # Get design variable names
    design_var_names = [var['name'] for var in data_info['variables'] 
                      if var['vars_type'] == 'design_vars']
    
    # Get best solution vector
    best_solution = results['best_solution']
    
    # Create results DataFrame
    solution_data = {}
    for i, name in enumerate(design_var_names):
        if i < len(best_solution):
            solution_data[name] = [best_solution[i]]
        else:
            solution_data[name] = [np.nan]
    
    solution_data['Fitness'] = [results['best_fitness']]
    solution_data['Feasible'] = [results['is_feasible']]
    solution_df = pd.DataFrame(solution_data)
    
    # Save numerical results
    solution_df.to_csv(os.path.join(save_dir, 'best_solution.csv'), index=False)
    
    # Save convergence data if available
    if 'convergence_history' in results:
        history = results['convergence_history']
        
        # Prepare DataFrame for convergence history
        history_data = {
            'Time_Elapsed': history.get('elapsed_times', []),
            'Evaluations': history['n_evals'],
            'Best_Fitness': history['best_f']
        }
        
        # Add feasible solutions if available
        if 'feasible_solutions' in history:
            history_data['Feasible_Solutions'] = history['feasible_solutions']
            
        convergence_df = pd.DataFrame(history_data)
        convergence_df.to_csv(os.path.join(save_dir, 'convergence.csv'), index=False)
        
        # Create convergence plots
        try:
            import matplotlib.pyplot as plt
            
            plt.figure(figsize=(12, 8))
            
            # Subplot 1: Fitness vs Evaluations
            plt.subplot(2, 1, 1)
            plt.plot(history['n_evals'], history['best_f'])
            plt.xlabel('Number of Evaluations')
            plt.ylabel('Best Fitness Value')
            plt.title('Convergence History')
            plt.grid(True, linestyle='--', alpha=0.7)
            
            # Subplot 2: Feasible Solutions
            if 'feasible_solutions' in history:
                plt.subplot(2, 1, 2)
                plt.plot(history['n_evals'], history['feasible_solutions'])
                plt.xlabel('Number of Evaluations')
                plt.ylabel('Number of Feasible Solutions')
                plt.title('Feasibility History')
                plt.grid(True, linestyle='--', alpha=0.7)
            
            plt.tight_layout()
            plt.savefig(os.path.join(save_dir, 'convergence_plot.png'), dpi=300)
            plt.close()
            
            # Also plot vs time
            plt.figure(figsize=(10, 6))
            plt.plot(history['elapsed_times'], history['best_f'])
            plt.xlabel('Time (seconds)')
            plt.ylabel('Best Fitness Value')
            plt.title('Convergence vs Time')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig(os.path.join(save_dir, 'convergence_time_plot.png'), dpi=300)
            plt.close()
        except:
            print("Warning: Couldn't create convergence plots. Matplotlib may not be available.")
            
    # Save detailed optimization summary
    with open(os.path.join(save_dir, 'optimization_summary.txt'), 'w') as f:
        f.write("Optimization Results Summary\n")
        f.write("=" * 50 + "\n\n")
        
        # Problem Information
        f.write("Problem Information:\n")
        f.write("-" * 20 + "\n")
        f.write(f"Number of design variables: {len(design_var_names)}\n")
        f.write(f"Optimization type: {'Minimization' if minimize_objective else 'Maximization'}\n\n")
        
        # Optimization Settings
        f.write("Optimization Settings:\n")
        f.write("-" * 20 + "\n")
        if 'convergence_history' in results:
            f.write(f"Total evaluations: {results['convergence_history']['n_evals'][-1]:,}\n\n")
        
        # Results Summary
        f.write("Results Summary:\n")
        f.write("-" * 20 + "\n")
        f.write(f"Runtime: {results['runtime']:.2f} seconds\n")
        f.write(f"Best fitness value: {results['best_fitness']:.6f}\n")
        f.write(f"Solution feasibility: {'Feasible' if results['is_feasible'] else 'Infeasible'}\n\n")
        
        if 'convergence_history' in results and len(results['convergence_history']['best_f']) > 1:
            initial_f = results['convergence_history']['best_f'][0]
            final_f = results['convergence_history']['best_f'][-1]
            
            if minimize_objective:
                improvement = ((initial_f - final_f) / initial_f) * 100 if initial_f != 0 else float('inf')
                f.write(f"Initial fitness: {initial_f:.6f}\n")
                f.write(f"Final fitness: {final_f:.6f}\n")
                f.write(f"Improvement: {improvement:.2f}%\n\n")
            else:
                improvement = ((final_f - initial_f) / initial_f) * 100 if initial_f != 0 else float('inf')
                f.write(f"Initial fitness: {initial_f:.6f}\n")
                f.write(f"Final fitness: {final_f:.6f}\n")
                f.write(f"Improvement: {improvement:.2f}%\n\n")
        
        # Best Solution
        f.write("Best Solution:\n")
        f.write("-" * 20 + "\n")
        for i, name in enumerate(design_var_names):
            if i < len(best_solution):
                f.write(f"{name}: {best_solution[i]:.6f}\n")
            else:
                f.write(f"{name}: Value not available\n")


def print_variable_information(variables: List[Dict]) -> None:
    """Print information about the optimization variables."""
    design_vars = [var for var in variables if var['vars_type'] == 'design_vars']
    env_vars = [var for var in variables if var['vars_type'] != 'design_vars']
    
    print("Optimization Problem Variables:")
    print("-" * 50)
    
    # Print design variables
    if design_vars:
        print("Design Variables:")
        for i, var in enumerate(design_vars):
            bounds = var.get('range_bounds', [None, None])
            desc = var.get('description', '')
            print(f"  {i+1}. {var['name']} [{bounds[0]}, {bounds[1]}] - {desc}")
    
    # Print environmental variables
    if env_vars:
        print("\nEnvironmental Variables:")
        for i, var in enumerate(env_vars):
            dist = var.get('distribution', 'unknown')
            if dist == 'uniform':
                bounds = f"[{var.get('low', 'N/A')}, {var.get('high', 'N/A')}]"
            elif dist == 'normal':
                bounds = f"mean={var.get('mean', 'N/A')}, std={var.get('std', 'N/A')}"
            else:
                bounds = "distribution parameters not specified"
            desc = var.get('description', '')
            print(f"  {i+1}. {var['name']} ({dist}) {bounds} - {desc}")
    
    print("-" * 50)


if __name__ == "__main__":
    """
    PyEGRO Deterministic Optimization Module - Example Usage
    ================================================================
    
    Example of using the GA module to solve the Weld Beam Design problem with constraints.
    """
    
    import numpy as np
    
    # Weld Beam Design Problem 
    # Fixed problem constants
    P = 6000      # load in lb
    L = 14        # length in inches
    E = 30e6      # psi
    G = 12e6      # psi
    tau_max = 13600
    sigma_max = 30000
    delta_max = 0.25

    # Objective function
    def weld_beam_cost(X):
        """Calculate the cost of the weld beam design."""
        X = np.atleast_2d(X)
        costs = []
        
        for x in X:
            h, l, t, b = x
            cost = 1.10471 * h**2 * l + 0.04811 * t * b * (14 + l)
            costs.append(cost)
            
        return np.array(costs)
    
    # Constraint functions - must return g(x) <= 0 for feasibility
    def constraint_tau(X):
        """Shear stress constraint."""
        X = np.atleast_2d(X)
        results = []
        
        for x in X:
            h, l, t, b = x
            
            # Calculate shear stress
            R = np.sqrt(l**2 / 4 + ((h + t) / 2)**2)
            J = 2 * (np.sqrt(2) * h * l * ((l**2 / 12) + ((h + t) / 2)**2))
            tau_p = P / (np.sqrt(2) * h * l)
            tau_d = (P * (L + l / 2) * R) / J
            tau = np.sqrt(tau_p**2 + 2 * tau_p * tau_d * l / (2 * R) + tau_d**2)
            
            # Constraint g(x) <= 0
            results.append(tau - tau_max)
            
        return np.array(results)
    
    def constraint_sigma(X):
        """Normal stress constraint."""
        X = np.atleast_2d(X)
        results = []
        
        for x in X:
            h, l, t, b = x
            
            # Calculate normal stress
            sigma = 6 * P * L / (b * t**2)
            
            # Constraint g(x) <= 0
            results.append(sigma - sigma_max)
            
        return np.array(results)
    
    def constraint_geometry(X):
        """Geometric constraint: h <= b."""
        X = np.atleast_2d(X)
        results = []
        
        for x in X:
            h, l, t, b = x
            
            # Constraint g(x) <= 0
            results.append(h - b)
            
        return np.array(results)
    
    def constraint_buckling(X):
        """Buckling load constraint."""
        X = np.atleast_2d(X)
        results = []
        
        for x in X:
            h, l, t, b = x
            
            # Calculate buckling load
            Pc = (4.013 * E * np.sqrt(t**2 * b**6 / 36)) / (L**2) * (1 - t / (2 * L) * np.sqrt(E / (4 * G)))
            
            # Constraint g(x) <= 0
            results.append(P - Pc)
            
        return np.array(results)
    
    def constraint_deflection(X):
        """Deflection constraint."""
        X = np.atleast_2d(X)
        results = []
        
        for x in X:
            h, l, t, b = x
            
            # Calculate deflection
            delta = 4 * P * L**3 / (E * b * t**3)
            
            # Constraint g(x) <= 0
            results.append(delta - delta_max)
            
        return np.array(results)
    
    def constraint_thickness(X):
        """Minimum thickness constraint."""
        X = np.atleast_2d(X)
        results = []
        
        for x in X:
            h, l, t, b = x
            
            # Constraint g(x) <= 0 (h >= 0.125)
            results.append(0.125 - h)
            
        return np.array(results)

    # Define the problem information
    data_info = {
        'variables': [
            {
                'name': 'h',
                'vars_type': 'design_vars',
                'distribution': 'normal',
                'range_bounds': [0.125, 5],
                'description': 'Weld thickness'
            },
            {
                'name': 'l',
                'vars_type': 'design_vars',
                'distribution': 'normal',
                'range_bounds': [0.1, 10],
                'description': 'Length of welded joint'
            },
            {
                'name': 't',
                'vars_type': 'design_vars',
                'distribution': 'normal',
                'range_bounds': [0.1, 10],
                'description': 'Width of the beam'
            },
            {
                'name': 'b',
                'vars_type': 'design_vars',
                'distribution': 'normal',
                'range_bounds': [0.1, 5],
                'description': 'Thickness of the beam'
            }
        ]
    }

    # List of constraint functions
    constraint_functions = [
        constraint_tau,
        constraint_sigma,
        constraint_geometry,
        constraint_buckling,
        constraint_deflection,
        constraint_thickness
    ]

    # Run optimization with explicit constraints
    results = run_deterministic_optimization(
        data_info=data_info,
        true_func=weld_beam_cost,
        constraint_funcs=constraint_functions,
        pop_size=100,
        n_gen=200,
        sampling_method='lhs',
        crossover_prob=0.9,
        crossover_eta=15,
        mutation_eta=20
    )

    # Save results
    save_optimization_results(
        results=results,
        data_info=data_info,
        save_dir='WELD_BEAM_RESULT_CONSTRAINED'
    )