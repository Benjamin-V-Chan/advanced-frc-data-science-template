from utils.seperation_bars import *
import pandas as pd
import os
import json
import traceback
import matplotlib.pyplot as plt
from utils.dictionary_manipulation import flatten_vars_in_dict

# ===========================
# CONFIGURATION SECTION
# ===========================

# File paths
EXPECTED_DATA_STRUCTURE_PATH = "config/expected_data_structure.json"
TEAM_PERFORMANCE_DATA_PATH = "outputs/team_data/team_performance_data.json"
TEAM_COMPARISON_ANALYSIS_STATS_PATH = "outputs/statistics/team_comparison_analysis_stats.txt"
VISUALIZATIONS_DIR = "outputs/visualizations"

# ===========================
# LOAD EXPECTED DATA STRUCTURE
# ===========================

with open(EXPECTED_DATA_STRUCTURE_PATH, "r") as file:
    EXPECTED_DATA_STRUCTURE = json.load(file)

# Flatten expected variables structure
FLATTENED_EXPECTED_VARIABLES = flatten_vars_in_dict(EXPECTED_DATA_STRUCTURE.get("variables", {}))

# Automatically extract metrics and define ranking order
METRICS_TO_ANALYZE = {}

for var_name, var_info in FLATTENED_EXPECTED_VARIABLES.items():
    stat_type = var_info.get("statistical_data_type", "unknown")

    if stat_type == "quantitative":
        METRICS_TO_ANALYZE[f"{var_name}_mean"] = {"type": "quantitative", "ascending": False}  # Higher is better
        METRICS_TO_ANALYZE[f"{var_name}_min"] = {"type": "quantitative", "ascending": True}   # Lower is better
        METRICS_TO_ANALYZE[f"{var_name}_max"] = {"type": "quantitative", "ascending": False}  # Higher is better
        METRICS_TO_ANALYZE[f"{var_name}_std_dev"] = {"type": "quantitative", "ascending": True}  # Lower is better (more consistent)
        METRICS_TO_ANALYZE[f"{var_name}_range"] = {"type": "quantitative", "ascending": False}  # Higher is better

    elif stat_type == "categorical":
        METRICS_TO_ANALYZE[f"{var_name}_mode"] = {"type": "categorical", "ascending": False}
        METRICS_TO_ANALYZE[f"{var_name}_value_counts"] = {"type": "categorical", "ascending": False}

    elif stat_type == "binary":
        METRICS_TO_ANALYZE[f"{var_name}_percent_true"] = {"type": "binary", "ascending": False}  # More True is better
        METRICS_TO_ANALYZE[f"{var_name}_percent_false"] = {"type": "binary", "ascending": True}  # More False is worse
        METRICS_TO_ANALYZE[f"{var_name}_mode"] = {"type": "binary", "ascending": False}

# ===========================
# HELPER FUNCTIONS SECTION
# ===========================

def save_rankings_and_visualizations(df, metric_name, metric_info):
    """
    Ranks teams based on a given metric and generates a visualization.

    :param df: DataFrame containing the team performance data.
    :param metric_name: The metric to rank and visualize.
    :param metric_info: Dictionary containing metric type and sorting order.
    """
    if metric_name not in df:
        print(f"[WARNING] Metric '{metric_name}' not found in data. Skipping...")
        return

    ascending = metric_info["ascending"]  # Get sorting order (True = increasing, False = decreasing)

    # Rank teams
    df[f"{metric_name}_rank"] = df[metric_name].rank(ascending=ascending)

    # Save rankings
    with open(TEAM_COMPARISON_ANALYSIS_STATS_PATH, 'a') as stats_file:
        stats_file.write(f"Rankings by {metric_name}:\n")
        stats_file.write(df[[metric_name, f"{metric_name}_rank"]].sort_values(by=metric_name, ascending=ascending).to_string(index=True) + "\n\n")
    
    # Visualization
    os.makedirs(VISUALIZATIONS_DIR, exist_ok=True)
    top_n = min(10, len(df))  # Show top 10 teams or fewer if less data
    df_sorted = df.sort_values(by=metric_name, ascending=ascending).head(top_n)

    df_sorted.plot(
        y=metric_name,
        kind="bar",
        title=f"Top {top_n} Teams by {metric_name.replace('_', ' ').title()}",
        legend=False
    )

    plt.ylabel(metric_name.replace("_", " ").title())
    plt.xticks(ticks=range(top_n), labels=df_sorted.index, rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(VISUALIZATIONS_DIR, f"top_{top_n}_{metric_name}.png"))
    plt.close()


# ===========================
# MAIN SCRIPT SECTION
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

    small_seperation_bar("RANK TEAMS AND SAVE METRICS")

    # Process each metric in METRICS_TO_ANALYZE
    for metric_name, metric_info in METRICS_TO_ANALYZE.items():
        print(f"[INFO] Processing metric: {metric_name} ({metric_info['type']}, ascending={metric_info['ascending']})")
        save_rankings_and_visualizations(team_performance_data, metric_name, metric_info)

    print("\n[INFO] Script 05: Completed successfully.")

# ===========================
# ERROR HANDLING SECTION
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
