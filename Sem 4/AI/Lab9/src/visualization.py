"""
Visualization module for benchmark functions and GA results.

This module provides functions to create:
- 2D contour plots of benchmark functions
- 3D surface plots of benchmark functions
- GA convergence plots
- Statistical comparison plots
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import pandas as pd
from typing import List, Dict, Any, Tuple, Optional
import os

from .functions import BenchmarkFunction


def setup_plotting_style():
    """Setup matplotlib and seaborn plotting style."""
    plt.style.use('default')
    sns.set_palette("husl")
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 11
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['legend.fontsize'] = 10


def plot_function_2d(function: BenchmarkFunction, resolution: int = 100, 
                     save_path: Optional[str] = None, show_global_min: bool = True) -> plt.Figure:
    """
    Create 2D contour plot of benchmark function.
    
    Args:
        function: Benchmark function to plot
        resolution: Grid resolution for plotting
        save_path: Path to save the plot (optional)
        show_global_min: Whether to mark global minimum
        
    Returns:
        matplotlib Figure object
    """
    setup_plotting_style()
    
    # Create coordinate grid
    x_min, x_max = function.domain[0]
    y_min, y_max = function.domain[1]
    
    x = np.linspace(x_min, x_max, resolution)
    y = np.linspace(y_min, y_max, resolution)
    X, Y = np.meshgrid(x, y)
    
    # Evaluate function
    Z = function(X, Y)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create contour plot
    contour = ax.contour(X, Y, Z, levels=20, colors='black', alpha=0.3, linewidths=0.5)
    contourf = ax.contourf(X, Y, Z, levels=50, cmap='viridis', alpha=0.8)
    
    # Add colorbar
    cbar = plt.colorbar(contourf, ax=ax)
    cbar.set_label('Function Value', rotation=270, labelpad=20)
    
    # Mark global minimum
    if show_global_min:
        gm_x, gm_y = function.global_minimum
        ax.plot(gm_x, gm_y, 'r*', markersize=15, label=f'Global Min: ({gm_x}, {gm_y})')
        ax.legend()
    
    # Labels and title
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'{function.name} - 2D Contour Plot')
    ax.grid(True, alpha=0.3)
    
    # Set aspect ratio
    ax.set_aspect('equal', adjustable='box')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


def plot_function_3d(function: BenchmarkFunction, resolution: int = 100,
                     save_path: Optional[str] = None, show_global_min: bool = True) -> plt.Figure:
    """
    Create 3D surface plot of benchmark function.
    
    Args:
        function: Benchmark function to plot
        resolution: Grid resolution for plotting
        save_path: Path to save the plot (optional)
        show_global_min: Whether to mark global minimum
        
    Returns:
        matplotlib Figure object
    """
    setup_plotting_style()
    
    # Create coordinate grid
    x_min, x_max = function.domain[0]
    y_min, y_max = function.domain[1]
    
    x = np.linspace(x_min, x_max, resolution)
    y = np.linspace(y_min, y_max, resolution)
    X, Y = np.meshgrid(x, y)
    
    # Evaluate function
    Z = function(X, Y)
    
    # Create 3D figure
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    
    # Create surface plot
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.9, 
                          linewidth=0, antialiased=True)
    
    # Add contour lines at bottom
    ax.contour(X, Y, Z, zdir='z', offset=np.min(Z), cmap='viridis', alpha=0.5)
    
    # Mark global minimum
    if show_global_min:
        gm_x, gm_y = function.global_minimum
        gm_z = function(gm_x, gm_y)
        ax.scatter([gm_x], [gm_y], [gm_z], color='red', s=100, 
                  label=f'Global Min: ({gm_x}, {gm_y}, {gm_z:.4f})')
        ax.legend()
    
    # Labels and title
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('f(x, y)')
    ax.set_title(f'{function.name} - 3D Surface Plot')
    
    # Add colorbar
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=20)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


def plot_convergence(results: Dict[str, Any], title: str = "GA Convergence",
                    save_path: Optional[str] = None) -> plt.Figure:
    """
    Plot GA convergence history.
    
    Args:
        results: GA results dictionary
        title: Plot title
        save_path: Path to save the plot (optional)
        
    Returns:
        matplotlib Figure object
    """
    setup_plotting_style()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    generations = range(1, len(results['best_fitness_history']) + 1)
    
    ax.plot(generations, results['best_fitness_history'], 'b-', linewidth=2, 
            label='Best Fitness', alpha=0.8)
    ax.plot(generations, results['mean_fitness_history'], 'r--', linewidth=2, 
            label='Mean Fitness', alpha=0.8)
    
    ax.set_xlabel('Generation')
    ax.set_ylabel('Fitness')
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Add final best fitness annotation
    final_best = results['best_fitness_history'][-1]
    ax.annotate(f'Final Best: {final_best:.6f}', 
                xy=(len(generations), final_best),
                xytext=(len(generations)*0.7, final_best*1.1),
                arrowprops=dict(arrowstyle='->', color='blue', alpha=0.7),
                fontsize=10, ha='center')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


def plot_multiple_convergence(results_dict: Dict[str, Dict[str, Any]], 
                             title: str = "GA Convergence Comparison",
                             save_path: Optional[str] = None) -> plt.Figure:
    """
    Plot convergence comparison for multiple GA configurations.
    
    Args:
        results_dict: Dictionary of {config_name: results}
        title: Plot title
        save_path: Path to save the plot (optional)
        
    Returns:
        matplotlib Figure object
    """
    setup_plotting_style()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(results_dict)))
    
    for i, (config_name, results) in enumerate(results_dict.items()):
        generations = range(1, len(results['best_fitness_history']) + 1)
        
        ax1.plot(generations, results['best_fitness_history'], 
                color=colors[i], linewidth=2, label=config_name, alpha=0.8)
        ax2.plot(generations, results['mean_fitness_history'], 
                color=colors[i], linewidth=2, label=config_name, alpha=0.8)
    
    ax1.set_xlabel('Generation')
    ax1.set_ylabel('Best Fitness')
    ax1.set_title('Best Fitness Convergence')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    ax2.set_xlabel('Generation')
    ax2.set_ylabel('Mean Fitness')
    ax2.set_title('Mean Fitness Convergence')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.suptitle(title, fontsize=16)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


def plot_statistical_comparison(stats_df: pd.DataFrame, metric: str = 'best_fitness',
                               save_path: Optional[str] = None) -> plt.Figure:
    """
    Create box plots for statistical comparison of GA configurations.
    
    Args:
        stats_df: DataFrame with columns ['config', 'run', metric]
        metric: Metric to plot ('best_fitness', 'mean_fitness', etc.)
        save_path: Path to save the plot (optional)
        
    Returns:
        matplotlib Figure object
    """
    setup_plotting_style()
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create box plot
    sns.boxplot(data=stats_df, x='config', y=metric, ax=ax)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    
    ax.set_title(f'Statistical Comparison: {metric.replace("_", " ").title()}')
    ax.set_ylabel(metric.replace("_", " ").title())
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


def plot_performance_matrix(results_matrix: np.ndarray, config_names: List[str],
                           metric_name: str = "Best Fitness", 
                           save_path: Optional[str] = None) -> plt.Figure:
    """
    Create heatmap of performance matrix.
    
    Args:
        results_matrix: 2D array of performance metrics
        config_names: List of configuration names
        metric_name: Name of the metric being displayed
        save_path: Path to save the plot (optional)
        
    Returns:
        matplotlib Figure object
    """
    setup_plotting_style()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create heatmap
    sns.heatmap(results_matrix, annot=True, fmt='.6f', cmap='viridis_r',
                xticklabels=config_names, yticklabels=config_names,
                ax=ax, cbar_kws={'label': metric_name})
    
    ax.set_title(f'Performance Matrix: {metric_name}')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


def create_function_plots(function: BenchmarkFunction, output_dir: str) -> None:
    """
    Create and save both 2D and 3D plots for a function.
    
    Args:
        function: Benchmark function to plot
        output_dir: Directory to save plots
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Create safe filename
    safe_name = function.name.lower().replace(' ', '_').replace('-', '_')
    
    # 2D plot
    fig_2d = plot_function_2d(function, resolution=200)
    plt.savefig(os.path.join(output_dir, f'{safe_name}_2d.png'), 
                dpi=300, bbox_inches='tight')
    plt.close(fig_2d)
    
    # 3D plot
    fig_3d = plot_function_3d(function, resolution=100)
    plt.savefig(os.path.join(output_dir, f'{safe_name}_3d.png'), 
                dpi=300, bbox_inches='tight')
    plt.close(fig_3d)
    
    print(f"Plots saved for {function.name} in {output_dir}")


if __name__ == "__main__":
    # Test visualization with both functions
    from .functions import drop_wave, levy
    
    # Create plots directory
    os.makedirs("../plots", exist_ok=True)
    
    # Create function plots
    create_function_plots(drop_wave, "../plots")
    create_function_plots(levy, "../plots")
    
    print("Test plots created successfully!")
