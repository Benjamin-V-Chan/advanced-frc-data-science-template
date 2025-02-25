import os
import traceback
import numpy as np
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

# Define metrics with sorting order, type, and optional top N filtering
METRICS_TO_ANALYZE = {
    # Quantitative Metrics
    "var1_mean": {"ascending": False, "type": "quantitative", "top_n_teams": 5},
    "var1_max": {"ascending": False, "type": "quantitative"},
    "var1_min": {"ascending": True, "type": "quantitative"},
    "var1_std_dev": {"ascending": True, "type": "quantitative", "top_n_teams": 5},
    "var1_range": {"ascending": False, "type": "quantitative"},
    "var2_mean": {"ascending": False, "type": "quantitative", "top_n_teams": 5},
    "var2_max": {"ascending": False, "type": "quantitative", "top_n_teams": 5},
    "var2_min": {"ascending": True, "type": "quantitative"},
    "var2_std_dev": {"ascending": True, "type": "quantitative", "top_n_teams": 5},
    "var2_range": {"ascending": False, "type": "quantitative"},
    "var3_percent_true": {"ascending": False, "type": "quantitative"},
    "var3_percent_false": {"ascending": True, "type": "quantitative"},

    # Categorical Metrics (Value Counts)
    "var4.var1_value_counts": {"type": "categorical"},
    "var4.var2_value_counts": {"type": "categorical"}
}

# Define variables for boxplot analysis
BOXPLOT_METRICS = {
    "var1": {"title": "Var1 Distribution"},
    "var2": {"title": "Var2 Distribution"}
}

RADAR_CHART_METRICS = {
    "teams": [1, 2],
    "variables": {
        "var1_mean": {"type": "quantitative"}, 
        "var2_max": {"type": "quantitative"}, 
        "var3_percent_true": {"type": "quantitative"},
        "var4.var2_value_counts": {"type": "categorical", "values_to_show": ["value1", "value2"]}
        }
}

# ===========================
# HELPER FUNCTIONS
# ===========================

def save_rankings(df, metric_name, ascending, top_n_teams):
    """
    Saves rankings of teams based on a specific metric.

    :param df: DataFrame containing the team performance data.
    :param metric_name: The metric to rank teams by.
    :param ascending: Whether to rank in ascending order (True) or descending order (False).
    :param top_n_teams: Number of top teams to include (None means all teams).
    """
    if metric_name not in df.columns:
        print(f"[WARNING] Metric '{metric_name}' not found in data. Skipping rankings...")
        return

    df_sorted = df.sort_values(by=metric_name, ascending=ascending)

    if top_n_teams:
        df_sorted = df_sorted.head(top_n_teams)

    with open(TEAM_COMPARISON_ANALYSIS_STATS_PATH, 'a') as stats_file:
        stats_file.write(f"Rankings by {metric_name} (Ascending={ascending}, Top {top_n_teams if top_n_teams else 'All'} teams):\n")
        stats_file.write("=" * 80 + "\n")
        stats_file.write(df_sorted[[metric_name]].to_string(index=True) + "\n\n")

def save_visualization(df, metric_name, metric_type, ascending, top_n_teams=None):
    """
    Generates visualizations for both quantitative and categorical data.

    - Quantitative metrics: Creates a bar chart of ranked teams, optionally limiting to top_n_teams.
    - Categorical metrics: Creates both split and stacked bar charts, including all teams.
    """

    # Ensure directory exists
    os.makedirs(VISUALIZATIONS_DIR, exist_ok=True)

    if metric_type == "quantitative":
        # Sort and apply top_n_teams filtering if specified
        df_sorted = df.sort_values(by=metric_name, ascending=ascending)
        if top_n_teams:
            df_sorted = df_sorted.head(top_n_teams)

        # Generate Bar Chart
        df_sorted[metric_name].plot(
            kind="bar",
            figsize=(12, 6),
            title=f"Top {top_n_teams if top_n_teams else 'All'} Teams - {metric_name}",
            legend=False
        )
        plt.ylabel(metric_name.replace("_", " ").title())
        plt.xlabel("Teams")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(os.path.join(VISUALIZATIONS_DIR, f"{metric_name}.png"))
        plt.close()

    elif metric_type == "categorical":
        # Convert category value counts into a DataFrame (expanding key-value pairs)
        category_data = df[metric_name].dropna().apply(lambda x: pd.Series(x)).fillna(0)
        category_data.index = df.index  # Ensure team index is kept

        # Generate Split Bar Chart
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

        # Generate Stacked Bar Chart
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

def save_boxplot_visualizations(df):
    """
    Generates boxplots for each team, visualizing the spread of their performance metrics.

    - Extracts relevant statistics dynamically (min, max, median, std_dev, etc.).
    - Each team's metrics are displayed in a separate boxplot.
    """

    os.makedirs(VISUALIZATIONS_DIR, exist_ok=True)

    for variable, details in BOXPLOT_METRICS.items():
        # Extract only relevant statistics for this variable (ignore categorical)
        stat_columns = [col for col in df.columns if col.startswith(variable) and "_mode" not in col]
        if not stat_columns:
            print(f"[WARNING] No relevant statistics found for '{variable}'. Skipping boxplot.")
            continue

        # Prepare data for boxplot, organized by team
        boxplot_data = df[stat_columns].dropna()

        # Transpose to make teams on x-axis
        boxplot_data_transposed = boxplot_data.T

        # Generate Boxplot (Team-Based)
        plt.figure(figsize=(12, 6))
        boxplot_data_transposed.boxplot()
        plt.title(f"{details['title']} (Team-Based Distribution)")
        plt.xlabel("Teams")
        plt.ylabel(variable.replace("_", " ").title())
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(os.path.join(VISUALIZATIONS_DIR, f"{variable}_team_boxplot.png"))
        plt.close()
        print(f"[INFO] Team-based boxplot saved for {variable}")

def save_radar_chart_visualization(df):
    """
    Generates a dynamically scaled radar chart comparing selected teams across specified variables.

    - Quantitative variables are normalized using min-max scaling.
    - Categorical variables are plotted using selected value counts.
    """

    teams_to_compare = RADAR_CHART_METRICS["teams"]
    selected_variables = RADAR_CHART_METRICS["variables"]

    # Ensure selected teams exist in data
    df_filtered = df[df.index.astype(str).isin(map(str, teams_to_compare))]
    if df_filtered.empty:
        print(f"[WARNING] No matching teams found in data. Skipping radar chart.")
        return

    # Extract and normalize values
    radar_data = []
    labels = []

    for var, config in selected_variables.items():
        if config["type"] == "quantitative":
            if var in df_filtered.columns:
                # Extract values
                values = df_filtered[var].astype(float).values
                
                # Apply min-max scaling for dynamic representation
                min_val, max_val = values.min(), values.max()
                if max_val != min_val:
                    values = (values - min_val) / (max_val - min_val)  # Normalize to [0,1]
                else:
                    values = np.ones_like(values)  # If all values are same, set them to 1
                
                radar_data.append(values)
                labels.append(var.replace("_", " ").title())
            else:
                print(f"[WARNING] Quantitative variable '{var}' not found. Skipping...")

        elif config["type"] == "categorical":
            extracted_counts = []
            for team in df_filtered.index:
                team_counts = df_filtered.at[team, var] if var in df_filtered.columns else {}
                values_to_show = config.get("values_to_show", team_counts.keys())  # Default: all
                extracted_counts.append([team_counts.get(val, 0) for val in values_to_show])
            
            extracted_counts = np.array(extracted_counts).T  # Convert into radar chart format
            
            # Normalize categorical value counts
            for i in range(extracted_counts.shape[0]):
                min_val, max_val = extracted_counts[i].min(), extracted_counts[i].max()
                if max_val != min_val:
                    extracted_counts[i] = (extracted_counts[i] - min_val) / (max_val - min_val)
                else:
                    extracted_counts[i] = np.ones_like(extracted_counts[i])  # If same, set to 1
            
            radar_data.extend(extracted_counts)  # Extend data for multiple categories
            labels.extend([f"{var.replace('_', ' ').title()} ({val})" for val in values_to_show])

    # Convert data to numpy array for plotting
    radar_data = np.array(radar_data)
    num_vars = radar_data.shape[0]

    # Create angles for radar chart
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Close the circle

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    for i, team in enumerate(df_filtered.index):
        values = radar_data[:, i].tolist()
        values += values[:1]  # Close the circle
        ax.plot(angles, values, label=f"Team {team}", linewidth=2)
        ax.fill(angles, values, alpha=0.1)

    # Format chart
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10)
    plt.title("Team Comparison Radar Chart (Scaled)", fontsize=14)
    plt.legend(loc="upper right", bbox_to_anchor=(1.2, 1.1))

    # Save radar chart
    plt.tight_layout()
    os.makedirs(VISUALIZATIONS_DIR, exist_ok=True)
    plt.savefig(os.path.join(VISUALIZATIONS_DIR, "team_radar_chart_scaled.png"))
    plt.close()
    print(f"[INFO] Radar chart saved as 'team_radar_chart_scaled.png'.")

# ===========================
# MAIN SCRIPT
# ===========================

seperation_bar()
print("Script 05: Team Comparison Analysis\n")

try:
    small_seperation_bar("LOAD TEAM PERFORMANCE DATA")

    if not os.path.exists(TEAM_PERFORMANCE_DATA_PATH):
        raise FileNotFoundError(f"Team performance data file not found: {TEAM_PERFORMANCE_DATA_PATH}")

    print(f"[INFO] Loading team performance data from: {TEAM_PERFORMANCE_DATA_PATH}")
    with open(TEAM_PERFORMANCE_DATA_PATH, "r") as infile:
        team_performance_data = pd.read_json(infile, orient="index")

    if team_performance_data.empty:
        raise ValueError(f"Team performance data is empty. Check the file: {TEAM_PERFORMANCE_DATA_PATH}")

    with open(TEAM_COMPARISON_ANALYSIS_STATS_PATH, 'w') as stats_file:
        stats_file.write("Team Rankings by Metrics\n")
        stats_file.write("=" * 80 + "\n\n")

    small_seperation_bar("PROCESS METRICS")

    for metric_name, metric_config in METRICS_TO_ANALYZE.items():
        metric_type = metric_config.get("type", "quantitative")
        ascending = metric_config.get("ascending", False) if metric_type == "quantitative" else False
        top_n_teams = metric_config.get("top_n_teams")

        print(f"[INFO] Processing metric: {metric_name} ({metric_type})")
        if metric_type == "quantitative":
            save_rankings(team_performance_data, metric_name, ascending, top_n_teams)
        
        save_visualization(team_performance_data, metric_name, metric_type, ascending, top_n_teams)
    
    small_seperation_bar("GENERATING BOXPLOT CHART")
    save_boxplot_visualizations(team_performance_data)

    small_seperation_bar("GENERATING TEAM RADAR CHART")
    save_radar_chart_visualization(team_performance_data)

    print("\n[INFO] Script 05: Completed successfully.")

except Exception as e:
    print(f"[ERROR] {e}")
    print(traceback.format_exc())

seperation_bar()
