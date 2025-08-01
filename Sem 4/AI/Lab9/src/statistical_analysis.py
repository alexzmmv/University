"""
Statistical analysis module for GA experiment results.

This module provides statistical tests and analysis methods to compare
the performance of different GA configurations, including:
- Descriptive statistics
- Hypothesis testing (t-tests, Wilcoxon, ANOVA)
- Effect size calculations
- Multiple comparison corrections
"""

import numpy as np
import pandas as pd
import scipy.stats as stats
from scipy.stats import ttest_ind, wilcoxon, kruskal, f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.power import ttest_power
import warnings
from typing import Dict, List, Tuple, Any, Optional
import os


class StatisticalAnalyzer:
    """Performs statistical analysis on GA experiment results."""
    
    def __init__(self, results_df: pd.DataFrame, alpha: float = 0.05):
        """
        Initialize statistical analyzer.
        
        Args:
            results_df: DataFrame with experiment results
            alpha: Significance level for hypothesis tests
        """
        self.results_df = results_df
        self.alpha = alpha
        self.analysis_results = {}
    
    def compute_descriptive_statistics(self) -> pd.DataFrame:
        """
        Compute descriptive statistics for each configuration.
        
        Returns:
            DataFrame with descriptive statistics
        """
        stats_list = []
        
        for function_name in self.results_df['function_name'].unique():
            function_data = self.results_df[self.results_df['function_name'] == function_name]
            
            for config in function_data['config_name'].unique():
                config_data = function_data[function_data['config_name'] == config]['best_fitness']
                
                stats_dict = {
                    'function_name': function_name,
                    'config_name': config,
                    'n_runs': len(config_data),
                    'mean': np.mean(config_data),
                    'std': np.std(config_data, ddof=1),
                    'median': np.median(config_data),
                    'min': np.min(config_data),
                    'max': np.max(config_data),
                    'q25': np.percentile(config_data, 25),
                    'q75': np.percentile(config_data, 75),
                    'iqr': np.percentile(config_data, 75) - np.percentile(config_data, 25),
                    'skewness': stats.skew(config_data),
                    'kurtosis': stats.kurtosis(config_data),
                    'cv': np.std(config_data, ddof=1) / np.mean(config_data) if np.mean(config_data) != 0 else 0
                }
                stats_list.append(stats_dict)
        
        return pd.DataFrame(stats_list)
    
    def test_normality(self) -> pd.DataFrame:
        """
        Test normality of data using Shapiro-Wilk test.
        
        Returns:
            DataFrame with normality test results
        """
        normality_results = []
        
        for function_name in self.results_df['function_name'].unique():
            function_data = self.results_df[self.results_df['function_name'] == function_name]
            
            for config in function_data['config_name'].unique():
                config_data = function_data[function_data['config_name'] == config]['best_fitness']
                
                # Shapiro-Wilk test
                statistic, p_value = stats.shapiro(config_data)
                
                normality_results.append({
                    'function_name': function_name,
                    'config_name': config,
                    'test': 'Shapiro-Wilk',
                    'statistic': statistic,
                    'p_value': p_value,
                    'is_normal': p_value > self.alpha
                })
        
        return pd.DataFrame(normality_results)
    
    def pairwise_comparisons(self, function_name: str, test_type: str = 'auto') -> pd.DataFrame:
        """
        Perform pairwise comparisons between configurations for a specific function.
        
        Args:
            function_name: Name of the function to analyze
            test_type: 'ttest', 'wilcoxon', or 'auto' (chooses based on normality)
            
        Returns:
            DataFrame with pairwise comparison results
        """
        function_data = self.results_df[self.results_df['function_name'] == function_name]
        configs = function_data['config_name'].unique()
        
        comparison_results = []
        
        for i, config1 in enumerate(configs):
            for j, config2 in enumerate(configs):
                if i >= j:  # Only compare each pair once
                    continue
                
                data1 = function_data[function_data['config_name'] == config1]['best_fitness']
                data2 = function_data[function_data['config_name'] == config2]['best_fitness']
                
                # Choose test method
                if test_type == 'auto':
                    # Use Shapiro-Wilk to test normality
                    _, p1 = stats.shapiro(data1)
                    _, p2 = stats.shapiro(data2)
                    use_parametric = (p1 > self.alpha) and (p2 > self.alpha)
                elif test_type == 'ttest':
                    use_parametric = True
                else:
                    use_parametric = False
                
                if use_parametric:
                    # Levene's test for equal variances
                    _, levene_p = stats.levene(data1, data2)
                    equal_var = levene_p > self.alpha
                    
                    # Independent t-test
                    statistic, p_value = ttest_ind(data1, data2, equal_var=equal_var)
                    test_used = f"t-test (equal_var={equal_var})"
                    
                    # Effect size (Cohen's d)
                    pooled_std = np.sqrt(((len(data1) - 1) * np.var(data1, ddof=1) + 
                                         (len(data2) - 1) * np.var(data2, ddof=1)) / 
                                        (len(data1) + len(data2) - 2))
                    effect_size = (np.mean(data1) - np.mean(data2)) / pooled_std
                else:
                    # Wilcoxon signed-rank test (for paired samples) or Mann-Whitney U (for independent samples)
                    if len(data1) == len(data2):
                        # Use Wilcoxon signed-rank test for paired data
                        try:
                            statistic, p_value = stats.wilcoxon(data1, data2, alternative='two-sided')
                            test_used = "Wilcoxon signed-rank"
                            # Effect size for Wilcoxon (r = Z / sqrt(N))
                            n = len(data1)
                            z_score = stats.norm.ppf(1 - p_value/2)  # Approximate Z-score from p-value
                            effect_size = z_score / np.sqrt(n)
                        except ValueError:
                            # Fall back to Mann-Whitney U if Wilcoxon fails
                            statistic, p_value = stats.mannwhitneyu(data1, data2, alternative='two-sided')
                            test_used = "Mann-Whitney U"
                            effect_size = 1 - (2 * statistic) / (len(data1) * len(data2))
                    else:
                        # Use Mann-Whitney U test for independent samples of different sizes
                        statistic, p_value = stats.mannwhitneyu(data1, data2, alternative='two-sided')
                        test_used = "Mann-Whitney U"
                        # Effect size (rank biserial correlation)
                        effect_size = 1 - (2 * statistic) / (len(data1) * len(data2))
                
                comparison_results.append({
                    'function_name': function_name,
                    'config1': config1,
                    'config2': config2,
                    'mean1': np.mean(data1),
                    'mean2': np.mean(data2),
                    'test_used': test_used,
                    'statistic': statistic,
                    'p_value': p_value,
                    'significant': p_value < self.alpha,
                    'effect_size': effect_size,
                    'better_config': config1 if np.mean(data1) < np.mean(data2) else config2  # For minimization
                })
        
        return pd.DataFrame(comparison_results)
    
    def multiple_comparison_correction(self, comparisons_df: pd.DataFrame, 
                                     method: str = 'bonferroni') -> pd.DataFrame:
        
        corrected_df = comparisons_df.copy()
        
        for function_name in corrected_df['function_name'].unique():
            function_mask = corrected_df['function_name'] == function_name
            p_values = corrected_df.loc[function_mask, 'p_value'].values
            
            if method == 'bonferroni':
                corrected_p = p_values * len(p_values)
                corrected_p = np.minimum(corrected_p, 1.0)  # Cap at 1.0
            elif method == 'holm':
                sorted_indices = np.argsort(p_values)
                corrected_p = np.zeros_like(p_values)
                for i, idx in enumerate(sorted_indices):
                    corrected_p[idx] = min(1.0, p_values[idx] * (len(p_values) - i))
                    if i > 0:
                        corrected_p[idx] = max(corrected_p[idx], corrected_p[sorted_indices[i-1]])
            elif method == 'fdr_bh':
                from statsmodels.stats.multitest import multipletests
                _, corrected_p, _, _ = multipletests(p_values, method='fdr_bh', alpha=self.alpha)
            else:
                raise ValueError(f"Unknown correction method: {method}")
            
            corrected_df.loc[function_mask, f'p_value_{method}'] = corrected_p
            corrected_df.loc[function_mask, f'significant_{method}'] = corrected_p < self.alpha
        
        return corrected_df
    
    def anova_test(self, function_name: str) -> Dict[str, Any]:
        """
        Perform one-way ANOVA to test if there are significant differences between configurations.
        
        Args:
            function_name: Name of the function to analyze
            
        Returns:
            Dictionary with ANOVA results
        """
        function_data = self.results_df[self.results_df['function_name'] == function_name]
        configs = function_data['config_name'].unique()
        
        # Prepare data for ANOVA
        groups = []
        for config in configs:
            config_data = function_data[function_data['config_name'] == config]['best_fitness']
            groups.append(config_data.values)
        
        # One-way ANOVA
        f_statistic, p_value = f_oneway(*groups)
        
        # Kruskal-Wallis (non-parametric alternative)
        kw_statistic, kw_p_value = kruskal(*groups)
        
        # Effect size (eta-squared)
        # SSB (sum of squares between groups)
        grand_mean = np.mean(np.concatenate(groups))
        ssb = sum(len(group) * (np.mean(group) - grand_mean)**2 for group in groups)
        
        # SST (total sum of squares)
        sst = sum(sum((x - grand_mean)**2 for x in group) for group in groups)
        
        eta_squared = ssb / sst if sst != 0 else 0
        
        results = {
            'function_name': function_name,
            'n_groups': len(configs),
            'total_n': len(function_data),
            'f_statistic': f_statistic,
            'f_p_value': p_value,
            'f_significant': p_value < self.alpha,
            'kw_statistic': kw_statistic,
            'kw_p_value': kw_p_value,
            'kw_significant': kw_p_value < self.alpha,
            'eta_squared': eta_squared,
            'effect_size_interpretation': self._interpret_eta_squared(eta_squared)
        }
        
        # Post-hoc analysis if significant
        if p_value < self.alpha:
            try:
                # Tukey HSD for parametric post-hoc
                all_data = []
                all_labels = []
                for config in configs:
                    config_data = function_data[function_data['config_name'] == config]['best_fitness']
                    all_data.extend(config_data.values)
                    all_labels.extend([config] * len(config_data))
                
                tukey_results = pairwise_tukeyhsd(all_data, all_labels, alpha=self.alpha)
                results['tukey_hsd'] = str(tukey_results)
            except Exception as e:
                results['tukey_hsd'] = f"Error in Tukey HSD: {str(e)}"
        
        return results
    
    def _interpret_eta_squared(self, eta_squared: float) -> str:
        """Interpret eta-squared effect size."""
        if eta_squared < 0.01:
            return "negligible"
        elif eta_squared < 0.06:
            return "small"
        elif eta_squared < 0.14:
            return "medium"
        else:
            return "large"
    
    def power_analysis(self, function_name: str) -> pd.DataFrame:
        """
        Perform power analysis for pairwise comparisons.
        
        Args:
            function_name: Name of the function to analyze
            
        Returns:
            DataFrame with power analysis results
        """
        function_data = self.results_df[self.results_df['function_name'] == function_name]
        configs = function_data['config_name'].unique()
        
        power_results = []
        
        for i, config1 in enumerate(configs):
            for j, config2 in enumerate(configs):
                if i >= j:
                    continue
                
                data1 = function_data[function_data['config_name'] == config1]['best_fitness']
                data2 = function_data[function_data['config_name'] == config2]['best_fitness']
                
                # Calculate effect size (Cohen's d)
                pooled_std = np.sqrt(((len(data1) - 1) * np.var(data1, ddof=1) + 
                                     (len(data2) - 1) * np.var(data2, ddof=1)) / 
                                    (len(data1) + len(data2) - 2))
                effect_size = abs(np.mean(data1) - np.mean(data2)) / pooled_std
                
                # Calculate power
                power = ttest_power(effect_size, nobs=len(data1), alpha=self.alpha)
                
                power_results.append({
                    'function_name': function_name,
                    'config1': config1,
                    'config2': config2,
                    'effect_size': effect_size,
                    'sample_size': len(data1),
                    'power': power,
                    'adequate_power': power >= 0.8
                })
        
        return pd.DataFrame(power_results)
    
    def generate_complete_analysis(self, output_dir: str) -> Dict[str, Any]:
        """
        Generate complete statistical analysis and save results.
        
        Args:
            output_dir: Directory to save analysis results
            
        Returns:
            Dictionary with all analysis results
        """
        os.makedirs(output_dir, exist_ok=True)
        
        print("Generating complete statistical analysis...")
        
        # Descriptive statistics
        print("  Computing descriptive statistics...")
        descriptive_stats = self.compute_descriptive_statistics()
        descriptive_stats.to_csv(os.path.join(output_dir, "descriptive_statistics.csv"), index=False)
        
        # Normality tests
        print("  Testing normality assumptions...")
        normality_results = self.test_normality()
        normality_results.to_csv(os.path.join(output_dir, "normality_tests.csv"), index=False)
        
        # Pairwise comparisons for each function
        print("  Performing pairwise comparisons...")
        all_comparisons = []
        anova_results = []
        power_analyses = []
        
        for function_name in self.results_df['function_name'].unique():
            # Pairwise comparisons
            comparisons = self.pairwise_comparisons(function_name)
            corrected_comparisons = self.multiple_comparison_correction(comparisons)
            all_comparisons.append(corrected_comparisons)
            
            # ANOVA
            anova_result = self.anova_test(function_name)
            anova_results.append(anova_result)
            
            # Power analysis
            power_analysis = self.power_analysis(function_name)
            power_analyses.append(power_analysis)
        
        # Combine and save results
        if all_comparisons:
            combined_comparisons = pd.concat(all_comparisons, ignore_index=True)
            combined_comparisons.to_csv(os.path.join(output_dir, "pairwise_comparisons.csv"), index=False)
        
        if anova_results:
            anova_df = pd.DataFrame(anova_results)
            anova_df.to_csv(os.path.join(output_dir, "anova_results.csv"), index=False)
        
        if power_analyses:
            combined_power = pd.concat(power_analyses, ignore_index=True)
            combined_power.to_csv(os.path.join(output_dir, "power_analysis.csv"), index=False)
        
        # Summary report
        self._generate_summary_report(output_dir, descriptive_stats, normality_results, 
                                    combined_comparisons if all_comparisons else None,
                                    anova_df if anova_results else None)
        
        analysis_results = {
            'descriptive_statistics': descriptive_stats,
            'normality_tests': normality_results,
            'pairwise_comparisons': combined_comparisons if all_comparisons else None,
            'anova_results': anova_df if anova_results else None,
            'power_analysis': combined_power if power_analyses else None
        }
        
        self.analysis_results = analysis_results
        print("Statistical analysis complete!")
        
        return analysis_results
    
    def _generate_summary_report(self, output_dir: str, descriptive_stats: pd.DataFrame,
                               normality_results: pd.DataFrame, comparisons: Optional[pd.DataFrame],
                               anova_results: Optional[pd.DataFrame]) -> None:
        """Generate a summary report in text format."""
        report_path = os.path.join(output_dir, "statistical_analysis_report.txt")
        
        with open(report_path, 'w') as f:
            f.write("STATISTICAL ANALYSIS REPORT\n")
            f.write("=" * 50 + "\n\n")
            
            # Overview
            f.write("OVERVIEW\n")
            f.write("-" * 20 + "\n")
            f.write(f"Analysis performed on {len(self.results_df)} total runs\n")
            f.write(f"Functions analyzed: {', '.join(self.results_df['function_name'].unique())}\n")
            f.write(f"Configurations: {', '.join(self.results_df['config_name'].unique())}\n")
            f.write(f"Significance level: {self.alpha}\n\n")
            
            # Descriptive statistics summary
            f.write("DESCRIPTIVE STATISTICS SUMMARY\n")
            f.write("-" * 35 + "\n")
            for function_name in descriptive_stats['function_name'].unique():
                f.write(f"\n{function_name}:\n")
                func_stats = descriptive_stats[descriptive_stats['function_name'] == function_name]
                best_config = func_stats.loc[func_stats['mean'].idxmin(), 'config_name']
                best_mean = func_stats.loc[func_stats['mean'].idxmin(), 'mean']
                f.write(f"  Best performing configuration: {best_config} (mean: {best_mean:.6f})\n")
                
                for _, row in func_stats.iterrows():
                    f.write(f"  {row['config_name']}: {row['mean']:.6f} ± {row['std']:.6f}\n")
            
            # Normality test summary
            f.write("\n\nNORMALITY TEST SUMMARY\n")
            f.write("-" * 25 + "\n")
            normal_count = normality_results['is_normal'].sum()
            total_count = len(normality_results)
            f.write(f"Normally distributed: {normal_count}/{total_count} configurations\n")
            
            # ANOVA results
            if anova_results is not None:
                f.write("\n\nANOVA RESULTS\n")
                f.write("-" * 15 + "\n")
                for _, row in anova_results.iterrows():
                    f.write(f"{row['function_name']}:\n")
                    f.write(f"  F-statistic: {row['f_statistic']:.4f}, p-value: {row['f_p_value']:.6f}\n")
                    f.write(f"  Significant differences: {'Yes' if row['f_significant'] else 'No'}\n")
                    f.write(f"  Effect size (η²): {row['eta_squared']:.4f} ({row['effect_size_interpretation']})\n\n")
            
            # Pairwise comparison summary
            if comparisons is not None:
                f.write("PAIRWISE COMPARISON SUMMARY\n")
                f.write("-" * 30 + "\n")
                for function_name in comparisons['function_name'].unique():
                    func_comparisons = comparisons[comparisons['function_name'] == function_name]
                    significant_comparisons = func_comparisons[func_comparisons['significant_bonferroni']]
                    f.write(f"{function_name}:\n")
                    f.write(f"  Significant differences (Bonferroni corrected): {len(significant_comparisons)}/{len(func_comparisons)}\n")
                    
                    if len(significant_comparisons) > 0:
                        f.write("  Significant pairs:\n")
                        for _, row in significant_comparisons.iterrows():
                            f.write(f"    {row['config1']} vs {row['config2']}: p = {row['p_value_bonferroni']:.6f}\n")
                    f.write("\n")


if __name__ == "__main__":
    # Example usage
    print("Statistical analysis module loaded successfully!")
    print("Use this module with experiment results to perform comprehensive statistical analysis.")
