import os
import json
import traceback
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates

# ===========================
# CONFIGURATION SECTION
# ===========================

TEAM_PERFORMANCE_DATA_PATH_JSON = "outputs/team_data/team_performance_data.json"
VISUALIZATIONS_DIR = "outputs/visualizations"

# Define the configuration for bar chart visualizations
BAR_CHART_CONFIG = {
    "distribution a": {"variable_metrics": ["var1_mean"], "visualizations": ["grouped_bar_chart"]},
    "distribution b": {
        "variable_metrics": ["var4.var2_percent_value2", "var4.var2_percent_value4", "var4.var2_percent_value3", "var4.var2_percent_value1"],
        "visualizations": ["stacked_bar_chart", "grouped_bar_chart", "parallel_coordinates_plot"]
    }
}

# ===========================
# HELPER FUNCTIONS
# ===========================

def load_team_performance_data():
    """Loads the team performance JSON data."""
    if not os.path.exists(TEAM_PERFORMANCE_DATA_PATH_JSON):
        print(f"[ERROR] Team performance data file not found: {TEAM_PERFORMANCE_DATA_PATH_JSON}")
        return None

    with open(TEAM_PERFORMANCE_DATA_PATH_JSON, "r") as infile:
        return json.load(infile)

def ensure_directory_exists(directory):
    """Ensures that a directory exists."""
    os.makedirs(directory, exist_ok=True)

def extract_metric_data(team_data, metric_list):
    """
    Extracts relevant metrics from the team data.

    :param team_data: The dictionary containing team statistics.
    :param metric_list: List of metric names to extract.
    :return: A DataFrame containing the extracted metrics.
    """
    extracted_data = []

    for team, stats in team_data.items():
        row = {"team": team}
        for metric in metric_list:
            row[metric] = stats.get(metric, 0)  # Default to 0 if metric is missing
        extracted_data.append(row)

    return pd.DataFrame(extracted_data)

# ===========================
# VISUALIZATION FUNCTIONS
# ===========================

# ===========================
# MAIN SCRIPT
# ===========================

print("Script 06: Bar Chart & Comparative Visualizations\n")

try:
    # Load data
    team_performance_data = load_team_performance_data()
    if team_performance_data is None:
        raise ValueError("No team performance data available.")

    ensure_directory_exists(VISUALIZATIONS_DIR)

    # Loop through configurations
    for title, config in BAR_CHART_CONFIG.items():
        variable_metrics = config["variable_metrics"]
        visualizations = config["visualizations"]

        print(f"[INFO] Processing {title}: {variable_metrics}")

        # Extract data
        df = extract_metric_data(team_performance_data, variable_metrics)

        if df.empty:
            print(f"[WARNING] No data found for {title}. Skipping...")
            continue

        # Generate visualizations based on the configuration
        for vis in visualizations:
            save_path = os.path.join(VISUALIZATIONS_DIR, f"{title}_{vis}.png")
        
    print("\n[INFO] Script 06: Completed.")

except Exception as e:
    print(f"\n[ERROR] {e}")
    print(traceback.format_exc())
