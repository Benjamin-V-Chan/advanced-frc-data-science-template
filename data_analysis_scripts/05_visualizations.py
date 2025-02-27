import os
import json
import traceback
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates

# ===========================
# CONFIGURATION SECTION
# ===========================

TEAM_PERFORMANCE_DATA_PATH_JSON = "outputs/team_data/team_performance_data.json"
VISUALIZATIONS_DIR = "outputs/visualizations"

# Bar Chart Configuration
BAR_CHART_CONFIG = {
    "distribution a": {"variable_metrics": ["var1_mean"], "visualizations": ["bar_chart"]},
    "distribution b": {
        "variable_metrics": ["var2_mean", "var2_max", "var3_percent_True"],
        "visualizations": ["stacked_bar_chart", "grouped_bar_chart", "parallel_coordinates_plot"]
    }
}

# Boxplot Configuration
BOXPLOT_CONFIG = {
    "Boxplot for Variable 1": ["var1"],
    "Boxplot for Variable 2 and 3": ["var2"]
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
# BAR CHART VISUALIZATION FUNCTIONS
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
# BOXPLOT VISUALIZATION FUNCTION
# ===========================

def extract_boxplot_data(team_data, variable):
    """
    Extracts Min, Q1, Median, Q3, and Max for each team for a given variable.

    :param team_data: Dictionary containing team performance data.
    :param variable: The base name of the variable to extract.
    :return: DataFrame structured for boxplot visualization.
    """
    boxplot_dict = {}

    for team, stats in team_data.items():
        min_val = stats.get(f"{variable}_min", None)
        q1 = stats.get(f"{variable}_first_quartile", None)
        median = stats.get(f"{variable}_median", None)
        q3 = stats.get(f"{variable}_third_quartile", None)
        max_val = stats.get(f"{variable}_max", None)

        if None not in [min_val, q1, median, q3, max_val]:  # Ensure all values exist
            boxplot_dict[team] = [min_val, q1, median, q3, max_val]

    return pd.DataFrame.from_dict(boxplot_dict, orient="index", columns=["Min", "Q1", "Median", "Q3", "Max"])

def generate_boxplot(team_data, variable, save_path):
    """
    Generates a boxplot for a single variable across teams.

    :param team_data: Dictionary containing team performance data.
    :param variable: Variable name for the boxplot.
    :param save_path: Path to save the plot.
    """
    boxplot_data = extract_boxplot_data(team_data, variable)

    if boxplot_data.empty:
        print(f"[WARNING] No valid data for {variable}, skipping boxplot.")
        return

    plt.figure(figsize=(10, 6))
    plt.boxplot(boxplot_data.values.T, labels=boxplot_data.index)

    plt.title(f"Boxplot for {variable} across Teams")
    plt.xlabel("Teams")
    plt.ylabel(variable.replace("_", " ").title())
    plt.xticks(rotation=45, ha="right")

    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    print(f"[INFO] Boxplot saved: {save_path}")

# ===========================
# MAIN SCRIPT
# ===========================

print("Script 05: Visualizations\n")

try:
    # Load data
    team_performance_data = load_team_performance_data()
    if team_performance_data is None:
        raise ValueError("No team performance data available.")

    ensure_directory_exists(VISUALIZATIONS_DIR)

    # Process bar charts
    for title, config in BAR_CHART_CONFIG.items():
        variable_metrics = config["variable_metrics"]
        visualizations = config["visualizations"]

        print(f"[INFO] Processing {title}: {variable_metrics}")

        df = extract_metric_data(team_performance_data, variable_metrics)
        if df.empty:
            print(f"[WARNING] No data found for {title}. Skipping...")
            continue

        for vis in visualizations:
            save_path = os.path.join(VISUALIZATIONS_DIR, f"{title}_{vis}.png")

            if vis == "bar_chart" and len(variable_metrics) == 1:
                generate_bar_chart(df, title, save_path)
            elif vis == "grouped_bar_chart" and len(variable_metrics) > 1:
                generate_grouped_bar_chart(df, title, save_path)
            elif vis == "stacked_bar_chart" and len(variable_metrics) > 1:
                generate_stacked_bar_chart(df, title, save_path)
            elif vis == "parallel_coordinates_plot" and len(variable_metrics) > 1:
                generate_parallel_coordinates_plot(df, title, save_path)

    # Process boxplots
    for title, variables in BOXPLOT_CONFIG.items():
        for variable in variables:
            print(f"[INFO] Generating boxplot for {variable}")

            save_path = os.path.join(VISUALIZATIONS_DIR, f"{variable}_boxplot.png")
            generate_boxplot(team_performance_data, variable, save_path)

    print("\n[INFO] Script 05: Completed.")

except Exception as e:
    print(f"\n[ERROR] {e}")
    print(traceback.format_exc())
