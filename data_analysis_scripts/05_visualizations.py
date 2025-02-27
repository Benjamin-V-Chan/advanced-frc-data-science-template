import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import traceback

# ===========================
# CONFIGURATION SECTION
# ===========================

TEAM_PERFORMANCE_DATA_PATH = "outputs/team_data/team_performance_data.json"
VISUALIZATIONS_DIR = "outputs/visualizations/boxplots"

# Add the variables you want to generate boxplots for
BOXPLOT_CONFIG = [
    "var1",  # Example
    "var2",  # Add more as needed
]

# ===========================
# HELPER FUNCTIONS
# ===========================

def load_team_performance_data():
    """Loads team performance data from JSON."""
    if not os.path.exists(TEAM_PERFORMANCE_DATA_PATH):
        raise FileNotFoundError(f"[ERROR] Team performance data not found: {TEAM_PERFORMANCE_DATA_PATH}")

    with open(TEAM_PERFORMANCE_DATA_PATH, "r") as json_file:
        return json.load(json_file)

def extract_boxplot_data(team_data, variable):
    """
    Extracts min, Q1, median, Q3, and max for each team for a given variable.

    :param team_data: Dictionary containing team performance data.
    :param variable: The base name of the variable to extract.
    :return: DataFrame structured for boxplot visualization.
    """
    boxplot_dict = {}

    for team, stats in team_data.items():
        min_val = stats.get(f"{variable}_range", None)  # Min (Using range here)
        q1 = stats.get(f"{variable}_first_quartile", None)
        median = stats.get(f"{variable}_median", None)
        q3 = stats.get(f"{variable}_third_quartile", None)
        max_val = stats.get(f"{variable}_range", None)  # Max (Using range here)

        if None not in [min_val, q1, median, q3, max_val]:  # Ensure all values exist
            boxplot_dict[team] = [min_val, q1, median, q3, max_val]

    return pd.DataFrame.from_dict(boxplot_dict, orient="index", columns=["Min", "Q1", "Median", "Q3", "Max"])

def generate_boxplots(team_data):
    """
    Generates boxplots for each variable in BOXPLOT_CONFIG.
    """
    os.makedirs(VISUALIZATIONS_DIR, exist_ok=True)

    for variable in BOXPLOT_CONFIG:
        print(f"[INFO] Generating boxplot for {variable}")

        boxplot_data = extract_boxplot_data(team_data, variable)
        
        if boxplot_data.empty:
            print(f"[WARNING] No valid data for {variable}, skipping boxplot.")
            continue

        # Ensure the team names are used as labels
        boxplot_data.index = boxplot_data.index.astype(str)  # Convert index to string

        # Plot boxplot
        plt.figure(figsize=(10, 6))
        plt.boxplot(boxplot_data.values.T, labels=boxplot_data.index)

        plt.title(f"Boxplot for {variable} across Teams")
        plt.xlabel("Teams")
        plt.ylabel(variable.replace("_", " ").title())
        plt.xticks(rotation=45, ha="right")

        # Save plot
        file_path = os.path.join(VISUALIZATIONS_DIR, f"{variable}_boxplot.png")
        plt.savefig(file_path, bbox_inches="tight")
        plt.close()

        print(f"[INFO] Boxplot saved: {file_path}")

# ===========================
# MAIN SCRIPT
# ===========================

if __name__ == "__main__":
    print("\nScript 06: Generating Boxplot Visualizations\n")

    try:
        team_performance_data = load_team_performance_data()
        generate_boxplots(team_performance_data)
        print("\n[INFO] Script 06 Completed Successfully.")

    except Exception as e:
        print(f"\n[ERROR] {e}")
        print(traceback.format_exc())