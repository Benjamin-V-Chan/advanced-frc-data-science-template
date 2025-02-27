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

# Define bar chart configuration (per metric category)
BAR_CHART_CONFIG = {
    "distribution a": {"variable_metrics": ["var1_mean"], "visualizations": ["bar_chart"]},
    "distribution b": {
        "variable_metrics": ["var2_mean", "var2_max", "var3_percent_true"],
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
# BOX PLOT VISUALIZATION
# ===========================

# ===========================
# BAR CHART VISUALIZATION
# ===========================

def generate_bar_chart(df, title, save_path):
    """Generates a simple bar chart for a single metric comparison."""
    metric = df.columns[1]  # Assuming "team" is the first column
    df.set_index("team")[metric].plot(kind="bar", figsize=(10, 5), color="skyblue", edgecolor="black")

    plt.title(title)
    plt.xlabel("Teams")
    plt.ylabel(metric)
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    print(f"[INFO] Bar Chart saved: {save_path}")

def generate_grouped_bar_chart(df, title, save_path):
    """Generates a grouped bar chart comparing teams for each variable metric."""
    df.set_index("team").plot(kind="bar", figsize=(12, 6), colormap="viridis")
    
    plt.title(title)
    plt.xlabel("Teams")
    plt.ylabel("Values")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Metrics")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    print(f"[INFO] Grouped Bar Chart saved: {save_path}")

def generate_stacked_bar_chart(df, title, save_path):
    """Generates a stacked bar chart comparing teams across multiple metrics."""
    df.set_index("team").plot(kind="bar", stacked=True, figsize=(12, 6), colormap="plasma")

    plt.title(title)
    plt.xlabel("Teams")
    plt.ylabel("Values")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Metrics")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    print(f"[INFO] Stacked Bar Chart saved: {save_path}")

def generate_parallel_coordinates_plot(df, title, save_path):
    """Generates a parallel coordinates plot to compare multiple metrics per team."""
    df_normalized = df.copy()
    df_normalized[df.columns[1:]] = df_normalized[df.columns[1:]].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
    
    plt.figure(figsize=(12, 6))
    parallel_coordinates(df_normalized, class_column="team", colormap=plt.get_cmap("tab10"), linewidth=2)
    
    plt.title(title)
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Metrics")
    plt.ylabel("Normalized Values (0-1)")
    plt.legend(title="Teams", bbox_to_anchor=(1.05, 1), loc="upper left")

    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    print(f"[INFO] Parallel Coordinates Plot saved: {save_path}")

# ===========================
# MAIN SCRIPT
# ===========================

print("Script 06: Visualizations (Boxplots & Bar Charts)\n")

try:
    # Load data
    team_performance_data = load_team_performance_data()
    if team_performance_data is None:
        raise ValueError("No team performance data available.")

    ensure_directory_exists(VISUALIZATIONS_DIR)

    # Generate boxplots
    for title, variables in BOXPLOT_CONFIG.items():
        for variable in variables:
            df = extract_metric_data(team_performance_data, ["team", f"{variable}_median"])
            save_path = os.path.join(VISUALIZATIONS_DIR, f"{title}_boxplot.png")
            generate_boxplot(df, f"{variable}_median", save_path)

    # Generate bar chart-based visualizations
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

            if vis == "bar_chart" and len(variable_metrics) == 1:
                generate_bar_chart(df, title, save_path)
                
            elif vis == "grouped_bar_chart":
                generate_grouped_bar_chart(df, title, save_path)
                
            elif vis == "stacked_bar_chart":
                generate_stacked_bar_chart(df, title, save_path)
                
            elif vis == "parallel_coordinates_plot":
                generate_parallel_coordinates_plot(df, title, save_path)

    print("\n[INFO] Script 06: Completed.")

except Exception as e:
    print(f"\n[ERROR] {e}")
    print(traceback.format_exc())
