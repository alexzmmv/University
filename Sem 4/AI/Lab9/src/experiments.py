"""
Experiment runner for GA optimization of benchmark functions.

This module orchestrates experiments across all combinations of:
- Functions: Drop-Wave, Levy
- Representations: Binary, Real-valued
- Crossover methods: 1-point, 2-point (binary), Arithmetic, BLX-α (real)
- Multiple independent runs for statistical analysis
"""

import numpy as np
import pandas as pd
import time
import os
import json
from typing import Dict, List, Any, Tuple
from itertools import product
import multiprocessing as mp
from functools import partial

from .functions import FUNCTIONS, BenchmarkFunction
from .genetic_algorithm import create_ga_config, GeneticAlgorithm
from .visualization import plot_convergence, plot_multiple_convergence, create_function_plots


class ExperimentRunner:
    """Manages and executes GA experiments."""
    
    def __init__(self, output_dir: str = "results"):
        """
        Initialize experiment runner.
        
        Args:
            output_dir: Directory to save results
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "plots"), exist_ok=True)
        
        # Default GA parameters
        self.default_params = {
            'population_size': 100,
            'generations': 100,
            'mutation_rate': 0.01,
            'crossover_rate': 0.8,
            'elitism': 2,
            'alpha': 0.5,  # For arithmetic and BLX-α crossover
            'bits_per_variable': 16  # For binary representation
        }
        
        # Configuration combinations
        self.configurations = [
            ('binary', '1point'),
            ('binary', '2point'),
            ('real', 'arithmetic'),
            ('real', 'blx_alpha')
        ]
    
    def run_single_experiment(self, function_name: str, representation: str, 
                             crossover: str, run_id: int, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a single GA experiment.
        
        Args:
            function_name: Name of benchmark function
            representation: 'binary' or 'real'
            crossover: Crossover method name
            run_id: Independent run identifier
            params: GA parameters
            
        Returns:
            Dictionary with experiment results
        """
        function = FUNCTIONS[function_name]
        ga = create_ga_config(representation, crossover, **params)
        
        start_time = time.time()
        results = ga.run(function, params['generations'])
        end_time = time.time()
        
        # Add metadata
        results.update({
            'function_name': function_name,
            'representation': representation,
            'crossover': crossover,
            'run_id': run_id,
            'runtime': end_time - start_time,
            'config_name': f"{representation}_{crossover}",
            'parameters': params.copy()
        })
        
        return results
    
    def run_experiments(self, num_runs: int = 30, 
                       functions: List[str] = None,
                       parallel: bool = True) -> pd.DataFrame:
        """
        Run comprehensive experiments.
        
        Args:
            num_runs: Number of independent runs per configuration
            functions: List of function names to test (default: all)
            parallel: Whether to use parallel processing
            
        Returns:
            DataFrame with all experiment results
        """
        if functions is None:
            functions = list(FUNCTIONS.keys())
        
        print(f"Starting experiments with {num_runs} runs per configuration...")
        print(f"Functions: {functions}")
        print(f"Configurations: {self.configurations}")
        
        all_results = []
        total_experiments = len(functions) * len(self.configurations) * num_runs
        completed = 0
        
        for function_name in functions:
            print(f"\nRunning experiments for {function_name}...")
            
            for representation, crossover in self.configurations:
                config_name = f"{representation}_{crossover}"
                print(f"  Configuration: {config_name}")
                
                if parallel and num_runs > 1:
                    # Parallel execution
                    with mp.Pool() as pool:
                        run_func = partial(
                            self.run_single_experiment,
                            function_name, representation, crossover,
                            params=self.default_params
                        )
                        config_results = pool.map(run_func, range(num_runs))
                else:
                    # Sequential execution
                    config_results = []
                    for run_id in range(num_runs):
                        result = self.run_single_experiment(
                            function_name, representation, crossover, 
                            run_id, self.default_params
                        )
                        config_results.append(result)
                        completed += 1
                        print(f"    Run {run_id + 1}/{num_runs} completed "
                              f"({completed}/{total_experiments} total)")
                
                all_results.extend(config_results)
        
        # Convert to DataFrame
        df = self._results_to_dataframe(all_results)
        
        # Save results
        results_file = os.path.join(self.output_dir, "experiment_results.csv")
        df.to_csv(results_file, index=False)
        print(f"\nResults saved to {results_file}")
        
        return df
    
    def _results_to_dataframe(self, results: List[Dict[str, Any]]) -> pd.DataFrame:
        """Convert results list to DataFrame."""
        data = []
        for result in results:
            data.append({
                'function_name': result['function_name'],
                'representation': result['representation'],
                'crossover': result['crossover'],
                'config_name': result['config_name'],
                'run_id': result['run_id'],
                'best_fitness': result['best_fitness'],
                'final_mean_fitness': result['mean_fitness_history'][-1],
                'convergence_generation': self._find_convergence_generation(result),
                'runtime': result['runtime'],
                'function_evaluations': result['function_evaluations'],
                'best_x': result['best_solution'][0],
                'best_y': result['best_solution'][1]
            })
        return pd.DataFrame(data)
    
    def _find_convergence_generation(self, result: Dict[str, Any], 
                                   threshold: float = 1e-6) -> int:
        """Find generation where algorithm converged (fitness change < threshold)."""
        history = result['best_fitness_history']
        for i in range(1, len(history)):
            if abs(history[i] - history[i-1]) < threshold:
                return i
        return len(history)  # Didn't converge
    
    def create_summary_statistics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create summary statistics from experiment results."""
        summary = df.groupby(['function_name', 'config_name']).agg({
            'best_fitness': ['mean', 'std', 'min', 'max'],
            'final_mean_fitness': ['mean', 'std'],
            'convergence_generation': ['mean', 'std'],
            'runtime': ['mean', 'std'],
            'function_evaluations': 'mean'
        }).round(6)
        
        # Flatten column names
        summary.columns = ['_'.join(col).strip() for col in summary.columns]
        summary = summary.reset_index()
        
        # Save summary
        summary_file = os.path.join(self.output_dir, "summary_statistics.csv")
        summary.to_csv(summary_file, index=False)
        print(f"Summary statistics saved to {summary_file}")
        
        return summary
    
    def create_visualizations(self, df: pd.DataFrame) -> None:
        """Create all visualizations from experiment results."""
        print("\nCreating visualizations...")
        
        plots_dir = os.path.join(self.output_dir, "plots")
        
        # Function plots
        for function_name in df['function_name'].unique():
            function = FUNCTIONS[function_name]
            create_function_plots(function, plots_dir)
        
        # Convergence plots for each function and configuration
        for function_name in df['function_name'].unique():
            function_df = df[df['function_name'] == function_name]
            
            # Get best run for each configuration
            best_runs = function_df.loc[function_df.groupby('config_name')['best_fitness'].idxmin()]
            
            # Create convergence comparison (requires access to full history)
            # This would need to be implemented with stored history data
            
        print("Visualizations created successfully!")
    
    def run_full_experiment_suite(self, num_runs: int = 30) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Run complete experiment suite with analysis.
        
        Args:
            num_runs: Number of independent runs per configuration
            
        Returns:
            Tuple of (results_df, summary_df)
        """
        print("=" * 60)
        print("GENETIC ALGORITHM BENCHMARK OPTIMIZATION EXPERIMENTS")
        print("=" * 60)
        
        # Run experiments
        results_df = self.run_experiments(num_runs=num_runs)
        
        # Create summary statistics
        summary_df = self.create_summary_statistics(results_df)
        
        # Create visualizations
        self.create_visualizations(results_df)
        
        # Print summary
        print("\n" + "=" * 60)
        print("EXPERIMENT SUMMARY")
        print("=" * 60)
        
        for function_name in results_df['function_name'].unique():
            print(f"\n{function_name.upper()}:")
            function_summary = summary_df[summary_df['function_name'] == function_name]
            
            best_config = function_summary.loc[function_summary['best_fitness_min'].idxmin()]
            print(f"  Best configuration: {best_config['config_name']}")
            print(f"  Best fitness achieved: {best_config['best_fitness_min']:.6f}")
            print(f"  Mean best fitness: {best_config['best_fitness_mean']:.6f} ± {best_config['best_fitness_std']:.6f}")
        
        return results_df, summary_df


def run_quick_test():
    """Run a quick test with fewer runs for development/testing."""
    runner = ExperimentRunner("test_results")
    
    # Override default parameters for quick test
    runner.default_params.update({
        'population_size': 50,
        'generations': 50
    })
    
    results_df, summary_df = runner.run_full_experiment_suite(num_runs=3)
    return results_df, summary_df


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run GA optimization experiments")
    parser.add_argument("--runs", type=int, default=30, 
                       help="Number of independent runs per configuration")
    parser.add_argument("--quick", action="store_true", 
                       help="Run quick test with reduced parameters")
    parser.add_argument("--output", type=str, default="results",
                       help="Output directory for results")
    
    args = parser.parse_args()
    
    if args.quick:
        print("Running quick test...")
        run_quick_test()
    else:
        runner = ExperimentRunner(args.output)
        runner.run_full_experiment_suite(num_runs=args.runs)
