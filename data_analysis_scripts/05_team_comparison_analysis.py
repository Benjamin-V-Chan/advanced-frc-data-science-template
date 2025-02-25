import os
import json
import traceback
import pandas as pd
import matplotlib.pyplot as plt
from utils.seperation_bars import *

# ===========================
# CONFIGURATION SECTION
# ===========================

# File paths
TEAM_PERFORMANCE_DATA_PATH = "outputs/team_data/team_performance_data.json"
TEAM_COMPARISON_ANALYSIS_STATS_PATH = "outputs/statistics/team_ranking_analysis.txt"
VISUALIZATIONS_DIR = "outputs/visualizations"

# Define the metrics to analyze (only for quantitative values)
METRICS_TO_ANALYZE = {
    "var1_mean": "Variable 1 Mean",
    "var1_max": "Variable 1 Max",
    "var1_min": "Variable 1 Min",
    "var1_std_dev": "Variable 1 Standard Deviation",
    "var1_range": "Variable 1 Range",
    "var2_mean": "Variable 2 Mean",
    "var2_max": "Variable 2 Max",
    "var2_min": "Variable 2 Min",
    "var2_std_dev": "Variable 2 Standard Deviation",
    "var2_range": "Variable 2 Range",
    "var3_percent_true": "Variable 3 Percent True",
    "var3_percent_false": "Variable 3 Percent False"
}

# ===========================
# HELPER FUNCTIONS
# ===========================

def save_rankings(df, metric_name, metric_label):
    """
    Saves rankings of teams based on a specific metric.

    :param df: DataFrame containing the team performance data.
    :param metric_name: The metric to rank teams by.
    :param metric_label: Human-readable label for the metric.
    """
    if metric_name not in df.columns:
        print(f"[WARNING] Metric '{metric_name}' not found in data. Skipping rankings...")
        return

    df_sorted = df.sort_values(by=metric_name, ascending=False)
    
    with open(TEAM_COMPARISON_ANALYSIS_STATS_PATH, 'a') as stats_file:
        stats_file.write(f"Rankings by {metric_label}:\n")
        stats_file.write("=" * 80 + "\n")
        stats_file.write(df_sorted[[metric_name]].to_string(index=True) + "\n\n")


def save_visualization(df, metric_name, metric_label):
    """
    Generates a bar chart showing the distribution of a metric across teams.

    :param df: DataFrame containing the team performance data.
    :param metric_name: The metric to visualize.
    :param metric_label: Human-readable label for the metric.
    """
    if metric_name not in df.columns:
        print(f"[WARNING] Metric '{metric_name}' not found in data. Skipping visualization...")
        return

    os.makedirs(VISUALIZATIONS_DIR, exist_ok=True)

    df_sorted = df.sort_values(by=metric_name, ascending=False)
    df_sorted.plot(
        y=metric_name,
        kind="bar",
        title=f"Team Comparison - {metric_label}",
        legend=False
    )

    plt.ylabel(metric_label)
    plt.xticks(ticks=range(len(df_sorted)), labels=df_sorted.index, rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(VISUALIZATIONS_DIR, f"{metric_name}.png"))
    plt.close()


# ===========================
# MAIN SCRIPT
# ===========================

seperation_bar()
print("Script 05: Team Comparison Analysis\n")

try:
    small_seperation_bar("LOAD TEAM PERFORMANCE DATA")

    # Verify input file exists
    if not os.path.exists(TEAM_PERFORMANCE_DATA_PATH):
        raise FileNotFoundError(f"Team performance data file not found: {TEAM_PERFORMANCE_DATA_PATH}")

    # Load team performance data
    print(f"[INFO] Loading team performance data from: {TEAM_PERFORMANCE_DATA_PATH}")
    with open(TEAM_PERFORMANCE_DATA_PATH, "r") as infile:
        team_performance_data = pd.read_json(infile, orient="index")

    # Ensure the DataFrame is not empty
    if team_performance_data.empty:
        raise ValueError(f"Team performance data is empty. Check the file: {TEAM_PERFORMANCE_DATA_PATH}")

    # Clear previous rankings
    with open(TEAM_COMPARISON_ANALYSIS_STATS_PATH, 'w') as stats_file:
        stats_file.write("Team Rankings by Metrics\n")
        stats_file.write("=" * 80 + "\n\n")

    small_seperation_bar("PROCESS METRICS")

    # Process each metric in METRICS_TO_ANALYZE
    for metric_name, metric_label in METRICS_TO_ANALYZE.items():
        print(f"[INFO] Processing metric: {metric_name} ({metric_label})")
        save_rankings(team_performance_data, metric_name, metric_label)
        save_visualization(team_performance_data, metric_name, metric_label)

    print("\n[INFO] Script 05: Completed successfully.")

# ===========================
# ERROR HANDLING
# ===========================

except FileNotFoundError as fnf_error:
    print(f"[ERROR] File not found: {fnf_error}")
except ValueError as value_error:
    print(f"[ERROR] Data validation error: {value_error}")
except PermissionError as perm_error:
    print(f"[ERROR] Permission denied while accessing a file: {perm_error}")
except Exception as e:
    print(f"[ERROR] An unexpected error occurred: {e}")
    print(traceback.format_exc())
    print("\nScript 05: Failed.")

seperation_bar()
