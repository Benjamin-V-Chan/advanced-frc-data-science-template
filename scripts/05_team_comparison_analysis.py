from utility_functions.print_formats import seperation_bar
import pandas as pd
import os
import traceback
import matplotlib.pyplot as plt
from scipy.stats import zscore

# ===========================
# CONFIGURATION SECTION
# ===========================

# File paths (Modify these as needed)
TEAM_PERFORMANCE_DATA_PATH = "outputs/team_data/team_performance_data.json"  # Input: Team performance data
ADVANCED_TEAM_PERFORMANCE_DATA_PATH = "outputs/team_data/advanced_team_performance_data.json"  # Output: Advanced team performance data
TEAM_COMPARISON_ANALYSIS_STATS_PATH = "outputs/statistics/team_comparison_analysis_stats.txt"  # Output: Team comparison stats
VISUALIZATIONS_DIR = "outputs/visualizations"  # Output: Visualizations folder

# Custom Metrics Configuration
CUSTOM_METRICS = {
    "consistency": {
        "description": (
            "Calculates how consistent a team is across all quantitative metrics. "
            "This uses the average of the z-scores of standard deviations across all metrics. "
            "Lower values indicate better consistency."
        ),
        "calculation": lambda df: df[
            [col for col in df.columns if col.endswith("_std_dev")]
        ].apply(zscore).mean(axis=1),
        "ascending": True  # Lower values are better for consistency
    }
    # Add more custom metrics here..
}

# ===========================
# MAIN SCRIPT SECTION
# ===========================

print(seperation_bar)
print("Script 05: Team Comparison Analysis\n")

try:
    # Step 1: Verify input file exists
    if not os.path.exists(TEAM_PERFORMANCE_DATA_PATH):
        raise FileNotFoundError(f"Team performance data file not found: {TEAM_PERFORMANCE_DATA_PATH}")

    # Step 2: Load team performance data
    print(f"[INFO] Loading team performance data from: {TEAM_PERFORMANCE_DATA_PATH}")
    with open(TEAM_PERFORMANCE_DATA_PATH, "r") as infile:
        team_performance_data = pd.read_json(infile, orient="index")

    # Ensure the DataFrame is not empty
    if team_performance_data.empty:
        raise ValueError(f"Team performance data is empty. Check the file: {TEAM_PERFORMANCE_DATA_PATH}")

    # Step 3: Calculate custom metrics
    print("[INFO] Calculating custom metrics.")
    for metric_name, metric_details in CUSTOM_METRICS.items():
        print(f"[INFO] Adding custom metric: {metric_name} - {metric_details['description']}")
        try:
            # NOTE: Ensure your custom calculation:
            # - Takes the `team_performance_data` DataFrame as input.
            # - Outputs a Pandas Series with team indices and calculated metric values.
            team_performance_data[metric_name] = metric_details["calculation"](team_performance_data)
        except Exception as e:
            print(f"[ERROR] Failed to calculate metric '{metric_name}'. Reason: {e}")

    # Step 4: Save advanced team performance data
    print(f"[INFO] Saving advanced analysis to: {ADVANCED_TEAM_PERFORMANCE_DATA_PATH}")
    os.makedirs(os.path.dirname(ADVANCED_TEAM_PERFORMANCE_DATA_PATH), exist_ok=True)
    team_performance_data.to_json(ADVANCED_TEAM_PERFORMANCE_DATA_PATH, orient="index", indent=4)

    # Step 5: Rank teams for each metric
    print("[INFO] Ranking teams for metrics.")
    rankings = {}
    for metric_name, metric_details in CUSTOM_METRICS.items():
        ascending = metric_details.get("ascending", False)
        team_performance_data[f"{metric_name}_rank"] = team_performance_data[metric_name].rank(ascending=ascending)
        rankings[metric_name] = team_performance_data.sort_values(by=metric_name, ascending=ascending)

    # Step 6: Save rankings to text file
    print(f"[INFO] Saving rankings to: {TEAM_COMPARISON_ANALYSIS_STATS_PATH}")
    os.makedirs(os.path.dirname(TEAM_COMPARISON_ANALYSIS_STATS_PATH), exist_ok=True)
    with open(TEAM_COMPARISON_ANALYSIS_STATS_PATH, 'w') as stats_file:
        stats_file.write("Team Rankings by Custom Metrics\n")
        stats_file.write("=" * 80 + "\n\n")
        for metric_name, ranked_df in rankings.items():
            stats_file.write(f"Rankings by {metric_name}:\n")
            stats_file.write(
                ranked_df[[metric_name, f"{metric_name}_rank"]].to_string(index=True) + "\n\n"
            )

    # Step 7: Generate visualizations
    print(f"[INFO] Generating visualizations in: {VISUALIZATIONS_DIR}")
    os.makedirs(VISUALIZATIONS_DIR, exist_ok=True)
    for metric_name, ranked_df in rankings.items():
        top_n = 10  # Top 10 teams for visualization
        ranked_df.head(top_n).plot(
            y=metric_name,
            kind="bar",
            title=f"Top {top_n} Teams by {metric_name.replace('_', ' ').title()}",
            legend=False
        )
        plt.ylabel(metric_name.replace("_", " ").title())
        plt.xticks(ticks=range(top_n), labels=ranked_df.head(top_n).index, rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(os.path.join(VISUALIZATIONS_DIR, f"top_{top_n}_{metric_name}.png"))
        plt.close()

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

print(seperation_bar)