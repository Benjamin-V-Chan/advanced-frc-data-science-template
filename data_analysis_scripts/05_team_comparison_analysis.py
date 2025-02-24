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

# Automatically extract metrics and their statistical data types
METRICS_TO_ANALYZE = {}

for var_name, var_info in FLATTENED_EXPECTED_VARIABLES.items():
    stat_type = var_info.get("statistical_data_type", "unknown")
    
    if stat_type == "quantitative":
        METRICS_TO_ANALYZE[f"{var_name}_mean"] = "quantitative"
        METRICS_TO_ANALYZE[f"{var_name}_min"] = "quantitative"
        METRICS_TO_ANALYZE[f"{var_name}_max"] = "quantitative"
        METRICS_TO_ANALYZE[f"{var_name}_std_dev"] = "quantitative"
        METRICS_TO_ANALYZE[f"{var_name}_range"] = "quantitative"
    
    elif stat_type == "categorical":
        METRICS_TO_ANALYZE[f"{var_name}_mode"] = "categorical"
        METRICS_TO_ANALYZE[f"{var_name}_value_counts"] = "categorical"
    
    elif stat_type == "binary":
        METRICS_TO_ANALYZE[f"{var_name}_percent_true"] = "binary"
        METRICS_TO_ANALYZE[f"{var_name}_percent_false"] = "binary"
        METRICS_TO_ANALYZE[f"{var_name}_mode"] = "binary"

# ===========================
# HELPER FUNCTIONS SECTION
# ===========================


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
    for metric_name, metric_type in METRICS_TO_ANALYZE.items():
        print(f"[INFO] Processing metric: {metric_name} ({metric_type})")
        save_rankings_and_visualizations(team_performance_data, metric_name, metric_type)

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
