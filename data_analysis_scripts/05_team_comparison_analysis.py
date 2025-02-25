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

# Define the metrics to analyze with sorting preferences
METRICS_TO_ANALYZE = {
    "var1_mean": {"ascending": False},
    "var1_max": {"ascending": False},
    "var1_min": {"ascending": True},
    "var1_std_dev": {"ascending": True},
    "var1_range": {"ascending": False},
    "var2_mean": {"ascending": False},
    "var2_max": {"ascending": False},
    "var2_min": {"ascending": True},
    "var2_std_dev": {"ascending": True},
    "var2_range": {"ascending": False},
    "var3_percent_true": {"ascending": False},
    "var3_percent_false": {"ascending": True}
}

# ===========================
# HELPER FUNCTIONS
# ===========================

def save_rankings(df, metric_name, ascending):
    """
    Saves rankings of teams based on a specific metric.

    :param df: DataFrame containing the team performance data.
    :param metric_name: The metric to rank teams by.
    :param ascending: Whether to rank in ascending order (True) or descending order (False).
    """
    if metric_name not in df.columns:
        print(f"[WARNING] Metric '{metric_name}' not found in data. Skipping rankings...")
        return

    df_sorted = df.sort_values(by=metric_name, ascending=ascending)

    with open(TEAM_COMPARISON_ANALYSIS_STATS_PATH, 'a') as stats_file:
        stats_file.write(f"Rankings by {metric_name} (Ascending={ascending}):\n")
        stats_file.write("=" * 80 + "\n")
        stats_file.write(df_sorted[[metric_name]].to_string(index=True) + "\n\n")


def save_visualization(df, metric_name, ascending):
    """
    Generates a bar chart showing the distribution of a metric across teams.

    :param df: DataFrame containing the team performance data.
    :param metric_name: The metric to visualize.
    :param ascending: Whether to sort in ascending order.
    """
    if metric_name not in df.columns:
        print(f"[WARNING] Metric '{metric_name}' not found in data. Skipping visualization...")
        return

    os.makedirs(VISUALIZATIONS_DIR, exist_ok=True)

    df_sorted = df.sort_values(by=metric_name, ascending=ascending)
    df_sorted.plot(
        y=metric_name,
        kind="bar",
        title=f"Team Comparison - {metric_name} (Ascending={ascending})",
        legend=False
    )

    plt.ylabel(metric_name.replace("_", " ").title())
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
    for metric_name, metric_config in METRICS_TO_ANALYZE.items():
        ascending = metric_config.get("ascending", False)  # Default to descending if not specified
        print(f"[INFO] Processing metric: {metric_name} (Ascending={ascending})")
        save_rankings(team_performance_data, metric_name, ascending)
        save_visualization(team_performance_data, metric_name, ascending)

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
