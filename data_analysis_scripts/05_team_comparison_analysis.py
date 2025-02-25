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

# Define metrics with their sorting order and type
METRICS_TO_ANALYZE = {
    # Quantitative Metrics
    "var1_mean": {"ascending": False, "type": "quantitative"},
    "var1_max": {"ascending": False, "type": "quantitative"},
    "var1_min": {"ascending": True, "type": "quantitative"},
    "var1_std_dev": {"ascending": True, "type": "quantitative"},
    "var1_range": {"ascending": False, "type": "quantitative"},
    "var2_mean": {"ascending": False, "type": "quantitative"},
    "var2_max": {"ascending": False, "type": "quantitative"},
    "var2_min": {"ascending": True, "type": "quantitative"},
    "var2_std_dev": {"ascending": True, "type": "quantitative"},
    "var2_range": {"ascending": False, "type": "quantitative"},
    "var3_percent_true": {"ascending": False, "type": "quantitative"},
    "var3_percent_false": {"ascending": True, "type": "quantitative"},

    # Categorical Metrics (Value Counts)
    "var4.var1_value_counts": {"type": "categorical"},
    "var4.var2_value_counts": {"type": "categorical"}
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


def save_visualization(df, metric_name, metric_type, ascending):
    """
    Generates:
    - Standard bar chart for quantitative data.
    - Both split and stacked bar charts for categorical data.

    :param df: DataFrame containing the team performance data.
    :param metric_name: The metric to visualize.
    :param metric_type: The type of metric (quantitative or categorical).
    :param ascending: Whether to sort in ascending order.
    """
    if metric_name not in df.columns:
        print(f"[WARNING] Metric '{metric_name}' not found in data. Skipping visualization...")
        return

    os.makedirs(VISUALIZATIONS_DIR, exist_ok=True)

    if metric_type == "quantitative":
        # Standard Bar Chart for Quantitative Data
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

    elif metric_type == "categorical":
        # Convert category value counts into a DataFrame (expanding key-value pairs)
        category_data = df[metric_name].dropna().apply(lambda x: pd.Series(x)).fillna(0)
        category_data.index = df.index  # Ensure team index is kept

        # Split Bar Chart (Each category as separate bars)
        category_data.plot(
            kind="bar",
            figsize=(12, 6),
            title=f"Category Split Distribution - {metric_name}",
            width=0.8
        )
        plt.ylabel("Count")
        plt.xlabel("Teams")
        plt.xticks(rotation=45, ha="right")
        plt.legend(title="Category Values", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.tight_layout()
        plt.savefig(os.path.join(VISUALIZATIONS_DIR, f"{metric_name}_split.png"))
        plt.close()

        # Stacked Bar Chart (All values stacked in a single bar per team)
        category_data.plot(
            kind="bar",
            stacked=True,
            figsize=(12, 6),
            title=f"Category Stacked Distribution - {metric_name}",
            width=0.8
        )
        plt.ylabel("Count")
        plt.xlabel("Teams")
        plt.xticks(rotation=45, ha="right")
        plt.legend(title="Category Values", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.tight_layout()
        plt.savefig(os.path.join(VISUALIZATIONS_DIR, f"{metric_name}_stacked.png"))
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
        metric_type = metric_config.get("type", "quantitative")
        ascending = metric_config.get("ascending", False) if metric_type == "quantitative" else None

        print(f"[INFO] Processing metric: {metric_name} ({metric_type})")
        if metric_type == "quantitative":
            save_rankings(team_performance_data, metric_name, ascending)
        
        save_visualization(team_performance_data, metric_name, metric_type, ascending)

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
