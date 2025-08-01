#!/usr/bin/env python3
"""
Main script for running GA optimization experiments.

This script provides command-line interface to run different types of experiments:
- Quick tests for development
- Full statistical analysis
- Function visualization
- Web application
"""

import argparse
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.functions import FUNCTIONS, drop_wave, levy
from src.experiments import ExperimentRunner, run_quick_test
from src.visualization import create_function_plots
from src.statistical_analysis import StatisticalAnalyzer


def test_functions():
    """Test benchmark functions implementation."""
    print("Testing benchmark functions...")
    
    # Test Drop-Wave function
    print(f"\nDrop-Wave Function:")
    print(f"  f(0, 0) = {drop_wave(0, 0):.6f} (expected: -1.0)")
    print(f"  Domain: {drop_wave.domain}")
    print(f"  Global minimum: {drop_wave.global_minimum} = {drop_wave.global_min_value}")
    
    # Test Levy function  
    print(f"\nLevy Function:")
    print(f"  f(1, 1) = {levy(1, 1):.6f} (expected: 0.0)")
    print(f"  Domain: {levy.domain}")
    print(f"  Global minimum: {levy.global_minimum} = {levy.global_min_value}")
    
    print("\nFunction tests completed successfully!")


def test_ga():
    """Test genetic algorithm implementation."""
    print("Testing genetic algorithm...")
    
    from src.genetic_algorithm import create_ga_config
    
    # Test binary representation
    print("\nTesting binary representation with 1-point crossover...")
    ga_binary = create_ga_config('binary', '1point', population_size=20, generations=10)
    result_binary = ga_binary.run(drop_wave, 10)
    print(f"  Best fitness: {result_binary['best_fitness']:.6f}")
    print(f"  Best solution: ({result_binary['best_solution'][0]:.4f}, {result_binary['best_solution'][1]:.4f})")
    
    # Test real-valued representation
    print("\nTesting real-valued representation with arithmetic crossover...")
    ga_real = create_ga_config('real', 'arithmetic', population_size=20, generations=10)
    result_real = ga_real.run(levy, 10)
    print(f"  Best fitness: {result_real['best_fitness']:.6f}")
    print(f"  Best solution: ({result_real['best_solution'][0]:.4f}, {result_real['best_solution'][1]:.4f})")
    
    print("\nGA tests completed successfully!")


def create_visualizations():
    """Create function visualizations."""
    print("Creating function visualizations...")
    
    plots_dir = "plots"
    os.makedirs(plots_dir, exist_ok=True)
    
    for function_name, function in FUNCTIONS.items():
        print(f"  Creating plots for {function.name}...")
        create_function_plots(function, plots_dir)
    
    print(f"Visualizations saved to {plots_dir}/ directory")


def run_experiments(num_runs=30, output_dir="results"):
    """Run full experiment suite."""
    print(f"Running full experiment suite with {num_runs} runs per configuration...")
    
    runner = ExperimentRunner(output_dir)
    results_df, summary_df = runner.run_full_experiment_suite(num_runs=num_runs)
    
    # Generate statistical analysis
    print("Performing statistical analysis...")
    analyzer = StatisticalAnalyzer(results_df)
    stats_results = analyzer.generate_complete_analysis(
        os.path.join(output_dir, "statistical_analysis")
    )
    
    print(f"\nExperiments completed! Results saved to {output_dir}/")
    return results_df, summary_df, stats_results


def start_web_app():
    """Start the Flask web application."""
    print("Starting web application...")
    from web_app.app import app
    app.run(debug=True, host='0.0.0.0', port=8555)


def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(
        description="GA Optimization of Benchmark Functions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --test                     # Run quick tests
  python main.py --test-functions           # Test function implementations
  python main.py --test-ga                  # Test GA implementation
  python main.py --visualize                # Create function plots
  python main.py --experiments --runs 30    # Run full experiments
  python main.py --quick                    # Run quick experiment (3 runs)
  python main.py --web                      # Start web application
        """
    )
    
    parser.add_argument('--test', action='store_true',
                       help='Run all tests')
    parser.add_argument('--test-functions', action='store_true',
                       help='Test benchmark functions')
    parser.add_argument('--test-ga', action='store_true',
                       help='Test genetic algorithm')
    parser.add_argument('--visualize', action='store_true',
                       help='Create function visualizations')
    parser.add_argument('--experiments', action='store_true',
                       help='Run full experiment suite')
    parser.add_argument('--quick', action='store_true',
                       help='Run quick test experiments')
    parser.add_argument('--web', action='store_true',
                       help='Start web application')
    parser.add_argument('--runs', type=int, default=30,
                       help='Number of runs per configuration (default: 30)')
    parser.add_argument('--output', type=str, default='results',
                       help='Output directory (default: results)')
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    try:
        if args.test or args.test_functions:
            test_functions()
        
        if args.test or args.test_ga:
            test_ga()
        
        if args.visualize:
            create_visualizations()
        
        if args.quick:
            print("Running quick test experiments...")
            run_quick_test()
        
        if args.experiments:
            run_experiments(num_runs=args.runs, output_dir=args.output)
        
        if args.web:
            start_web_app()
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
