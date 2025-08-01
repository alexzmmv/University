from flask import Flask, render_template, request, jsonify, send_file
import os
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Do not show plots on the screen
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
from scipy import stats

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.functions import FUNCTIONS, get_function
from src.genetic_algorithm import create_ga_config
from src.experiments import ExperimentRunner
from src.visualization import plot_function_2d, plot_function_3d, plot_convergence
from src.statistical_analysis import StatisticalAnalyzer

app = Flask(__name__)

current_results = None
experiment_runner = None


@app.route('/')
def index():
    """Main page with function visualization and experiment configuration."""
    return render_template('index.html', functions=list(FUNCTIONS.keys()))


@app.route('/visualize_function')
def visualize_function():
    function_name = request.args.get('function', 'drop_wave')
    plot_type = request.args.get('type', '2d')
    
    try:
        function = get_function(function_name)
        
        if plot_type == '2d':
            fig = plot_function_2d(function, resolution=100, show_global_min=True)
        else:
            fig = plot_function_3d(function, resolution=50, show_global_min=True)
        
        # Convert plot to base64 string
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        img_string = base64.b64encode(img_buffer.read()).decode()
        plt.close(fig)
        
        return jsonify({
            'success': True,
            'image': img_string,
            'function_info': {
                'name': function.name,
                'domain': function.domain,
                'global_minimum': function.global_minimum,
                'global_min_value': function.global_min_value
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/run_experiment', methods=['POST'])
def run_experiment():
    """Run a single GA experiment with specified parameters."""
    try:
        data = request.json
        
        # Extract parameters
        function_name = data.get('function', 'drop_wave')
        representation = data.get('representation', 'binary')
        crossover = data.get('crossover', '1point')
        
        # GA parameters
        params = {
            'population_size': int(data.get('population_size', 100)),
            'generations': int(data.get('generations', 100)),
            'mutation_rate': float(data.get('mutation_rate', 0.01)),
            'crossover_rate': float(data.get('crossover_rate', 0.8)),
            'elitism': int(data.get('elitism', 2)),
            'alpha': float(data.get('alpha', 0.5)),
            'bits_per_variable': int(data.get('bits_per_variable', 16))
        }
        
        # Run experiment
        function = get_function(function_name)
        ga = create_ga_config(representation, crossover, **params)
        results = ga.run(function, params['generations'])
        
        # Generate convergence plot
        fig = plot_convergence(results, title=f"GA Convergence: {representation}_{crossover}")
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        convergence_plot = base64.b64encode(img_buffer.read()).decode()
        plt.close(fig)
        
        # Format results for JSON response
        response_data = {
            'success': True,
            'results': {
                'best_fitness': float(results['best_fitness']),
                'best_solution': results['best_solution'].tolist(),
                'function_evaluations': int(results['function_evaluations']),
                'generations': int(results['generations']),
                'convergence_plot': convergence_plot,
                'configuration': f"{representation}_{crossover}",
                'final_best_fitness': float(results['best_fitness_history'][-1]),
                'final_mean_fitness': float(results['mean_fitness_history'][-1])
            },
            'function_info': {
                'global_minimum': function.global_minimum,
                'global_min_value': function.global_min_value
            }
        }
        
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/run_full_experiments', methods=['POST'])
def run_full_experiments():
    """Run comprehensive experiments with statistical analysis."""
    global current_results, experiment_runner
    
    try:
        data = request.json
        num_runs = int(data.get('num_runs', 10))  # Reduced for web interface
        
        # Initialize experiment runner
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"web_results_{timestamp}"
        experiment_runner = ExperimentRunner(output_dir)
        
        # Override parameters for faster web execution
        experiment_runner.default_params.update({
            'population_size': int(data.get('population_size', 50)),
            'generations': int(data.get('generations', 50)),
            'mutation_rate': float(data.get('mutation_rate', 0.01)),
            'crossover_rate': float(data.get('crossover_rate', 0.8))
        })
        
        # Run experiments
        results_df, summary_df = experiment_runner.run_full_experiment_suite(num_runs=num_runs)
        current_results = (results_df, summary_df)
        
        # Generate statistical analysis
        analyzer = StatisticalAnalyzer(results_df)
        stats_results = analyzer.generate_complete_analysis(
            os.path.join(output_dir, "statistical_analysis")
        )
        
        # Prepare summary data for response
        summary_data = {}
        for function_name in results_df['function_name'].unique():
            function_summary = summary_df[summary_df['function_name'] == function_name]
            best_idx = function_summary['best_fitness_min'].idxmin()
            best_config = function_summary.loc[best_idx]
            
            summary_data[function_name] = {
                'best_config': best_config['config_name'],
                'best_fitness': float(best_config['best_fitness_min']),
                'mean_fitness': float(best_config['best_fitness_mean']),
                'std_fitness': float(best_config['best_fitness_std']),
                'all_configs': []
            }
            
            for _, row in function_summary.iterrows():
                summary_data[function_name]['all_configs'].append({
                    'config': row['config_name'],
                    'mean': float(row['best_fitness_mean']),
                    'std': float(row['best_fitness_std']),
                    'min': float(row['best_fitness_min']),
                    'max': float(row['best_fitness_max'])
                })
        
        return jsonify({
            'success': True,
            'summary': summary_data,
            'total_experiments': len(results_df),
            'output_directory': output_dir
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/get_experiment_status')
def get_experiment_status():
    """Get status of current experiments."""
    global current_results
    
    if current_results is None:
        return jsonify({'status': 'no_experiments', 'message': 'No experiments have been run yet.'})
    
    results_df, summary_df = current_results
    
    return jsonify({
        'status': 'completed',
        'total_runs': len(results_df),
        'functions': list(results_df['function_name'].unique()),
        'configurations': list(results_df['config_name'].unique()),
        'summary_available': True
    })


@app.route('/download_results')
def download_results():
    """Download experiment results as CSV."""
    global current_results
    
    if current_results is None:
        return jsonify({'error': 'No results available'})
    
    results_df, _ = current_results
    
    # Create temporary CSV file
    temp_file = f"temp_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    results_df.to_csv(temp_file, index=False)
    
    return send_file(temp_file, as_attachment=True, download_name='ga_experiment_results.csv')


@app.route('/api/function_info/<function_name>')
def get_function_info(function_name):
    """Get detailed information about a function."""
    try:
        function = get_function(function_name)
        return jsonify({
            'success': True,
            'name': function.name,
            'domain': function.domain,
            'global_minimum': function.global_minimum,
            'global_min_value': function.global_min_value,
            'description': function.__doc__ or "No description available"
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/compare_configurations')
def compare_configurations():
    """Page for comparing different GA configurations."""
    return render_template('compare.html', functions=list(FUNCTIONS.keys()))


@app.route('/api/run_comparison', methods=['POST'])
def run_comparison():
    """Run comparison experiments for selected configurations."""
    try:
        data = request.json
        
        # Extract parameters
        function_name = data.get('function', 'drop_wave')
        configurations = data.get('configurations', [])
        num_runs = int(data.get('num_runs', 5))  # Fewer runs for web interface
        
        if not configurations:
            return jsonify({'success': False, 'error': 'No configurations selected'})
        
        # Initialize experiment runner
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"web_comparison_{timestamp}"
        runner = ExperimentRunner(output_dir)
        
        # Override parameters for faster web execution
        runner.default_params.update({
            'population_size': int(data.get('population_size', 50)),
            'generations': int(data.get('generations', 50)),
            'mutation_rate': float(data.get('mutation_rate', 0.01)),
            'crossover_rate': float(data.get('crossover_rate', 0.8))
        })
        
        # Set configurations for comparison
        selected_configs = []
        for config in configurations:
            representation = config['representation']
            crossover = config['crossover']
            selected_configs.append((representation, crossover))
        
        runner.configurations = selected_configs
        
        # Run experiments for selected function only
        results_df = runner.run_experiments(
            num_runs=num_runs, 
            functions=[function_name], 
            parallel=False
        )
        
        # Store results for plotting
        global comparison_results_cache
        if 'comparison_results_cache' not in globals():
            comparison_results_cache = {}
        comparison_results_cache[function_name] = results_df
        
        # Generate statistical analysis
        analyzer = StatisticalAnalyzer(results_df)
        stats_results = analyzer.generate_complete_analysis(
            os.path.join(output_dir, "statistical_analysis")
        )
        
        # Prepare comparison data
        comparison_data = prepare_comparison_data(results_df, function_name)
        
        return jsonify({
            'success': True,
            'comparison_data': comparison_data,
            'total_experiments': len(results_df),
            'output_directory': output_dir,
            'function_name': function_name
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/get_comparison_plot')
def get_comparison_plot():
    try:
        function_name = request.args.get('function', 'drop_wave')
        config_names = request.args.getlist('configs')
        
        # If no configs provided, try to get from single config parameter
        if not config_names:
            single_config = request.args.get('config')
            if single_config:
                config_names = [single_config]
        
        print(f"Generating plot for function: {function_name}, configs: {config_names}")
        
        global comparison_results_cache
        if 'comparison_results_cache' not in globals():
            comparison_results_cache = {}
            
        if comparison_results_cache and function_name in comparison_results_cache:
            results_df = comparison_results_cache[function_name]
            print(f"Found cached data with {len(results_df)} rows")
            print(f"Available configs in data: {results_df['config_name'].unique()}")
            
            # Filter data for selected configurations
            filtered_df = results_df[results_df['config_name'].isin(config_names)]
            
            if not filtered_df.empty:
                print(f"Creating boxplot with {len(filtered_df)} rows")
                fig = create_comparison_boxplot(filtered_df)
            else:
                print("No data found for selected configs, creating simple plot")
                fig = create_simple_comparison_plot(function_name, config_names)
        else:
            print("No cached data found, creating simple plot")
            fig = create_simple_comparison_plot(function_name, config_names)
        
        # Convert plot to base64 string
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        img_string = base64.b64encode(img_buffer.read()).decode()
        plt.close(fig)
        
        return jsonify({
            'success': True,
            'plot': img_string
        })
    
    except Exception as e:
        print(f"Error generating comparison plot: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)})


def create_simple_comparison_plot(function_name, config_names):
    """Create a simple comparison plot when detailed data is not available."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if not config_names:
        config_names = ['No configurations selected']
    
    # Create a placeholder plot with some visual elements
    ax.text(0.5, 0.6, f'Comparison Plot for {function_name.replace("_", " ").title()}', 
            horizontalalignment='center', verticalalignment='center', 
            transform=ax.transAxes, fontsize=16, fontweight='bold')
    
    ax.text(0.5, 0.4, f'Selected Configurations:\n{", ".join(config_names)}', 
            horizontalalignment='center', verticalalignment='center', 
            transform=ax.transAxes, fontsize=12)
    
    ax.text(0.5, 0.2, 'Run experiments to generate comparison data', 
            horizontalalignment='center', verticalalignment='center', 
            transform=ax.transAxes, fontsize=10, style='italic')
    
    ax.set_title('Configuration Comparison Plot', fontsize=14, fontweight='bold')
    ax.set_xlabel('Configuration')
    ax.set_ylabel('Performance Metric')
    ax.grid(True, alpha=0.3)
    
    # Remove ticks since this is a placeholder
    ax.set_xticks([])
    ax.set_yticks([])
    
    return fig


def _interpret_eta_squared(eta_squared: float) -> str:
    """Interpret eta-squared effect size."""
    if eta_squared < 0.01:
        return "negligible"
    elif eta_squared < 0.06:
        return "small"
    elif eta_squared < 0.14:
        return "medium"
    else:
        return "large"


def prepare_comparison_data(results_df, function_name):
    """Prepare comparison data for frontend display."""
    function_data = results_df[results_df['function_name'] == function_name]
    
    comparison_data = {
        'configurations': [],
        'statistical_tests': {},
        'summary_stats': {}
    }
    
    # Calculate summary statistics for each configuration
    for config in function_data['config_name'].unique():
        config_data = function_data[function_data['config_name'] == config]
        best_fitness = config_data['best_fitness']
        
        config_stats = {
            'name': config,
            'mean': float(np.mean(best_fitness)),
            'std': float(np.std(best_fitness, ddof=1)),
            'median': float(np.median(best_fitness)),
            'min': float(np.min(best_fitness)),
            'max': float(np.max(best_fitness)),
            'q25': float(np.percentile(best_fitness, 25)),
            'q75': float(np.percentile(best_fitness, 75)),
            'runs': int(len(best_fitness)),
            'convergence_mean': float(np.mean(config_data['convergence_generation'])),
            'runtime_mean': float(np.mean(config_data['runtime']))
        }
        
        comparison_data['configurations'].append(config_stats)
        comparison_data['summary_stats'][config] = config_stats
    
    # Perform pairwise statistical tests if we have data
    if len(comparison_data['configurations']) > 1:
        try:
            # Try to import scipy for statistical tests
            import scipy.stats as stats
            configs = list(comparison_data['summary_stats'].keys())
            
            for i, config1 in enumerate(configs):
                for j, config2 in enumerate(configs):
                    if i >= j:
                        continue
                    
                    data1 = function_data[function_data['config_name'] == config1]['best_fitness']
                    data2 = function_data[function_data['config_name'] == config2]['best_fitness']
                    
                    # Perform t-test
                    t_stat, t_p_value = stats.ttest_ind(data1, data2)
                    
                    # Perform Wilcoxon signed-rank test or Mann-Whitney U test
                    if len(data1) == len(data2):
                        try:
                            # Use Wilcoxon signed-rank test for paired data
                            w_stat, w_p_value = stats.wilcoxon(data1, data2, alternative='two-sided')
                            wilcoxon_test = "Wilcoxon signed-rank"
                        except ValueError:
                            # Fall back to Mann-Whitney U if Wilcoxon fails
                            w_stat, w_p_value = stats.mannwhitneyu(data1, data2, alternative='two-sided')
                            wilcoxon_test = "Mann-Whitney U"
                    else:
                        # Use Mann-Whitney U test for independent samples of different sizes
                        w_stat, w_p_value = stats.mannwhitneyu(data1, data2, alternative='two-sided')
                        wilcoxon_test = "Mann-Whitney U"
                    
                    test_key = f"{config1}_vs_{config2}"
                    comparison_data['statistical_tests'][test_key] = {
                        'config1': config1,
                        'config2': config2,
                        't_test': {
                            'statistic': float(t_stat),
                            'p_value': float(t_p_value),
                            'significant': bool(t_p_value < 0.05)
                        },
                        'wilcoxon': {
                            'statistic': float(w_stat),
                            'p_value': float(w_p_value),
                            'significant': bool(w_p_value < 0.05),
                            'test_type': wilcoxon_test
                        }
                    }
            
            # Perform ANOVA test
            all_data = []
            all_labels = []
            for config in configs:
                config_data = function_data[function_data['config_name'] == config]['best_fitness']
                all_data.extend(config_data.values)
                all_labels.extend([config] * len(config_data))
            
            # One-way ANOVA
            groups = [function_data[function_data['config_name'] == config]['best_fitness'].values 
                     for config in configs]
            f_stat, anova_p_value = stats.f_oneway(*groups)
            
            # Kruskal-Wallis (non-parametric alternative to ANOVA)
            kw_stat, kw_p_value = stats.kruskal(*groups)
            
            # Effect size (eta-squared)
            grand_mean = np.mean(np.concatenate(groups))
            ssb = sum(len(group) * (np.mean(group) - grand_mean)**2 for group in groups)
            sst = sum(sum((x - grand_mean)**2 for x in group) for group in groups)
            eta_squared = ssb / sst if sst != 0 else 0
            
            comparison_data['anova_results'] = {
                'f_statistic': float(f_stat),
                'f_p_value': float(anova_p_value),
                'f_significant': bool(anova_p_value < 0.05),
                'kw_statistic': float(kw_stat),
                'kw_p_value': float(kw_p_value),
                'kw_significant': bool(kw_p_value < 0.05),
                'eta_squared': float(eta_squared),
                'effect_size_interpretation': _interpret_eta_squared(eta_squared)
            }
        except (ImportError, Exception) as e:
            configs = list(comparison_data['summary_stats'].keys())
            for i, config1 in enumerate(configs):
                for j, config2 in enumerate(configs):
                    if i >= j:
                        continue
                    
                    test_key = f"{config1}_vs_{config2}"
                    comparison_data['statistical_tests'][test_key] = {
                        'config1': config1,
                        'config2': config2,
                        't_test': {
                            'statistic': 0.0,
                            'p_value': 1.0,
                            'significant': False
                        },
                        'wilcoxon': {
                            'statistic': 0.0,
                            'p_value': 1.0,
                            'significant': False,
                            'test_type': 'Mann-Whitney U'
                        }
                    }
            
            # Placeholder ANOVA results
            comparison_data['anova_results'] = {
                'f_statistic': 0.0,
                'f_p_value': 1.0,
                'f_significant': False,
                'kw_statistic': 0.0,
                'kw_p_value': 1.0,
                'kw_significant': False,
                'eta_squared': 0.0,
                'effect_size_interpretation': 'negligible'
            }
    
    return comparison_data


def create_comparison_boxplot(results_df):
    """Create box plot for configuration comparison."""
    try:
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Prepare data for box plot
        configs = results_df['config_name'].unique()
        print(f"Creating boxplot for configs: {configs}")
        
        data_to_plot = []
        labels = []
        
        for config in configs:
            config_data = results_df[results_df['config_name'] == config]['best_fitness']
            if len(config_data) > 0:
                data_to_plot.append(config_data.values)
                labels.append(config.replace('_', '\n'))
                print(f"Config {config}: {len(config_data)} data points")
        
        if not data_to_plot:
            # No data available, create empty plot
            ax.text(0.5, 0.5, 'No data available for selected configurations', 
                   horizontalalignment='center', verticalalignment='center', 
                   transform=ax.transAxes, fontsize=12)
            ax.set_title('Configuration Comparison - No Data', fontsize=14, fontweight='bold')
            return fig
        
        # Create box plot
        box_plot = ax.boxplot(data_to_plot, labels=labels, patch_artist=True)
        
        # Color the boxes
        colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow', 'lightpink', 'lightgray']
        for i, patch in enumerate(box_plot['boxes']):
            patch.set_facecolor(colors[i % len(colors)])
        
        ax.set_title('Configuration Comparison - Best Fitness Distribution', fontsize=14, fontweight='bold')
        ax.set_ylabel('Best Fitness', fontsize=12)
        ax.set_xlabel('Configuration', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Add mean markers
        for i, config in enumerate(configs):
            config_data = results_df[results_df['config_name'] == config]['best_fitness']
            if len(config_data) > 0:
                mean_val = np.mean(config_data)
                ax.plot(i + 1, mean_val, 'ro', markersize=8, label='Mean' if i == 0 else "")
        
        if len(configs) > 0:
            ax.legend()
        
        plt.tight_layout()
        return fig
    
    except Exception as e:
        print(f"Error creating boxplot: {str(e)}")
        # Create fallback plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, f'Error creating plot: {str(e)}', 
               horizontalalignment='center', verticalalignment='center', 
               transform=ax.transAxes, fontsize=12)
        ax.set_title('Configuration Comparison - Error', fontsize=14, fontweight='bold')
        return fig


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
