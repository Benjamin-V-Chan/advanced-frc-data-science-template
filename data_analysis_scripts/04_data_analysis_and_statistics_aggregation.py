from utils import seperation_bar, small_seperation_bar
import os
import json
import traceback
import pandas as pd
import numpy as np

# ===========================
# CONFIGURATION SECTION
# ===========================

# File paths (Modify these as needed)
TEAM_BASED_MATCH_DATA_PATH = "data/processed/team_based_match_data.json"  # Input: Team-based match data
TEAM_PERFORMANCE_DATA_PATH = "outputs/team_data/team_performance_data.json"  # Output: Team performance data

# ===========================
# HELPER FUNCTIONS SECTION
# ===========================

def convert_to_serializable(obj):
    """
    Converts all non-serializable types (like NumPy types) to Python native types.

    :param obj: Object to convert.
    :return: Serializable object.
    """
    if isinstance(obj, (pd.Series, pd.DataFrame)):
        return obj.to_dict()
    if isinstance(obj, (np.int64, np.float64)):
        return obj.item()
    if isinstance(obj, (pd.Timestamp, pd.Timedelta)):
        return str(obj)
    if isinstance(obj, (int, float, str, bool, list, dict)):
        return obj
    if hasattr(obj, "__iter__") and not isinstance(obj, (str, bytes)):
        return [convert_to_serializable(item) for item in obj]
    return obj


def calculate_team_performance_data(team_data):
    """
    Automatically calculates team performance data for each team based on detected data types.

    :param team_data: Dictionary containing match data for each team.
    :return: A dictionary with aggregated team statistics.
    """
    all_team_performance_data = {}

    for team, data in team_data.items():
        matches = data["matches"]
        df = pd.DataFrame(matches)

        # Initialize team_performance dictionary for this team
        team_performance = {}

        # Number of matches played
        team_performance["number_of_matches"] = len(df)

        # Process data based on detected types
        for column in df.columns:
            if pd.api.types.is_numeric_dtype(df[column]):
                team_performance[f"{column}_average"] = float(df[column].mean())
                team_performance[f"{column}_min"] = float(df[column].min())
                team_performance[f"{column}_max"] = float(df[column].max())
                team_performance[f"{column}_std_dev"] = float(df[column].std())
            elif pd.api.types.is_categorical_dtype(df[column]) or pd.api.types.is_object_dtype(df[column]):
                team_performance[f"{column}_value_counts"] = df[column].value_counts().to_dict()
            elif pd.api.types.is_bool_dtype(df[column]):
                team_performance[f"{column}_percent_true"] = float(df[column].mean() * 100)

        # Add processed statistics for the team
        all_team_performance_data[team] = team_performance

    return all_team_performance_data

# ===========================
# MAIN SCRIPT SECTION
# ===========================

seperation_bar()
print("Script 04: Data Analysis & Statistics Aggregation\n")

try:
    # Guidance for FRC teams:
    # - Ensure your team-based match data is in `data/processed/team_based_match_data.json`.
    # - Modify the file paths above if your structure is different.

    small_seperation_bar("LOAD TEAM-BASED MATCH DATA")
    print(f"[INFO] Loading team-based match data from: {TEAM_BASED_MATCH_DATA_PATH}")
    with open(TEAM_BASED_MATCH_DATA_PATH, 'r') as infile:
        team_data = json.load(infile)

    if not isinstance(team_data, dict):
        raise ValueError("[ERROR] Team-based match data must be a dictionary.")

    small_seperation_bar("CALCULATE AND SAVE TEAM PERFORMANCE DATA")
    print("[INFO] Calculating team performance data.")
    team_performance_data = calculate_team_performance_data(team_data)

    # Convert data to serializable format
    team_performance_data_serializable = convert_to_serializable(team_performance_data)

    # Save team performance data
    print(f"[INFO] Saving team performance data to: {TEAM_PERFORMANCE_DATA_PATH}")
    os.makedirs(os.path.dirname(TEAM_PERFORMANCE_DATA_PATH), exist_ok=True)
    with open(TEAM_PERFORMANCE_DATA_PATH, 'w') as outfile:
        json.dump(team_performance_data_serializable, outfile, indent=4)

    print("\n[INFO] Script 04: Completed.")

except Exception as e:
    print(f"\n[ERROR] An unexpected error occurred: {e}")
    print(traceback.format_exc())
    print("\nScript 04: Failed.")

seperation_bar()