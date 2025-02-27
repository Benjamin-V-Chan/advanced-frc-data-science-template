from utils.seperation_bars import *
import os
import csv
import json
import traceback
import pandas as pd
import numpy as np

# ===========================
# CONFIGURATION SECTION
# ===========================

# File paths
EXPECTED_DATA_STRUCTURE_PATH = "config/expected_data_structure.json"
TEAM_BASED_MATCH_DATA_PATH = "data/processed/team_based_match_data.json"
TEAM_PERFORMANCE_DATA_PATH_JSON = "outputs/team_data/team_performance_data.json"
TEAM_PERFORMANCE_DATA_PATH_CSV = "outputs/team_data/team_performance_data.csv"

# Load Expected Data Structure
with open(EXPECTED_DATA_STRUCTURE_PATH, "r") as f:
    EXPECTED_DATA_STRUCTURE_DICT = json.load(f)

# Flatten the expected variable structure while keeping properties intact
def flatten_expected_vars(dictionary, return_dict=None, prefix=""):
    """Flattens only variable names but keeps their properties (statistical_data_type, values) intact."""
    if return_dict is None:
        return_dict = {}

    for key, value in dictionary.items():
        full_key = f"{prefix}.{key}" if prefix else key

        if isinstance(value, dict) and "statistical_data_type" not in value:
            flatten_expected_vars(value, return_dict, full_key)
        else:
            return_dict[full_key] = value

    return return_dict

FLATTENED_EXPECTED_VARIABLES = flatten_expected_vars(EXPECTED_DATA_STRUCTURE_DICT.get("variables", {}))

print("\n[DEBUG] Expected Variables Structure (Flattened):")
print(json.dumps(FLATTENED_EXPECTED_VARIABLES, indent=4))  # Debugging

# ===========================
# HELPER FUNCTIONS SECTION
# ===========================

def convert_to_serializable(obj):
    """Converts NumPy and Pandas types to standard Python types for JSON serialization."""
    if isinstance(obj, (np.integer, int)):
        return int(obj)
    if isinstance(obj, (np.floating, float)):
        return float(obj) if not np.isnan(obj) else 0  # Replace NaN with 0
    if isinstance(obj, (bool, np.bool_)):  # Convert bool to int for JSON
        return int(obj)
    if isinstance(obj, (pd.Series, pd.DataFrame)):
        return obj.to_dict()
    if isinstance(obj, dict):
        return {str(k): convert_to_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    return obj

def determine_statistical_type(variable_name):
    """Returns the statistical data type (quantitative, categorical, binary) based on the expected structure."""
    if variable_name in FLATTENED_EXPECTED_VARIABLES:
        return FLATTENED_EXPECTED_VARIABLES[variable_name].get("statistical_data_type", "unknown")
    print(f"[WARNING] Variable '{variable_name}' not found in expected data structure.")
    return "unknown"

def calculate_team_performance_data(team_data):
    """
    Computes performance metrics for each team based on statistical data types.

    :param team_data: Dictionary containing match data for each team.
    :return: A dictionary with aggregated team statistics.
    """
    all_team_performance_data = {}

    for team, data in team_data.items():
        matches = data.get("matches", [])
        if not matches:
            all_team_performance_data[team] = {"number_of_matches": 0}
            continue

        # Flatten only the variables inside each match
        flat_data = [{k: v for k, v in flatten_expected_vars(match["variables"]).items()} for match in matches]
        df = pd.DataFrame(flat_data)

        # Drop empty columns
        df.dropna(axis=1, how="all", inplace=True)

        team_performance = {"number_of_matches": len(df)}

        print(f"\n[DEBUG] Processing Team {team}: Found {df.shape[1]} variables")  # Debugging

        # Compute statistics based on expected data types
        for column in df.columns:
            stat_type = determine_statistical_type(column)

            print(f"[DEBUG] Processing variable '{column}' as '{stat_type}'")  # Debugging

            if stat_type == "quantitative":
                df[column] = pd.to_numeric(df[column], errors='coerce')  # Ensure numeric conversion
                team_performance[f"{column}_mean"] = convert_to_serializable(df[column].mean())
                team_performance[f"{column}_median"] = convert_to_serializable(df[column].median())
                team_performance[f"{column}_min"] = convert_to_serializable(df[column].min())
                team_performance[f"{column}_max"] = convert_to_serializable(df[column].max())
                team_performance[f"{column}_std_dev"] = convert_to_serializable(df[column].std()) if len(df[column].dropna()) > 1 else 0
                team_performance[f"{column}_range"] = convert_to_serializable(df[column].max() - df[column].min())

            elif stat_type == "categorical":
                value_counts = df[column].value_counts().to_dict()
                mode_value = df[column].mode().iloc[0] if not df[column].mode().empty else None
                team_performance[f"{column}_value_counts"] = convert_to_serializable(value_counts)
                team_performance[f"{column}_mode"] = mode_value

            elif stat_type == "binary":
                df[column] = df[column].astype(str).str.lower().replace({"true": True, "false": False})
                df[column] = df[column].astype(bool)  # Ensure correct dtype
                if pd.api.types.is_bool_dtype(df[column]):
                    team_performance[f"{column}_percent_true"] = round(df[column].mean() * 100, 2)
                    team_performance[f"{column}_percent_false"] = round((1 - df[column].mean()) * 100, 2)
                    team_performance[f"{column}_mode"] = convert_to_serializable(df[column].mode().iloc[0] if not df[column].mode().empty else None)

            else:
                print(f"[ERROR] Unrecognized statistical type for {column}: {stat_type}")

        all_team_performance_data[str(team)] = team_performance  # Ensure team key is a string

    return all_team_performance_data

# ===========================
# MAIN SCRIPT SECTION
# ===========================

seperation_bar()
print("Script 04: Data Analysis & Statistics Aggregation\n")

try:
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

    # Save team performance data (JSON)
    print(f"[INFO] Saving JSON team performance data to: {TEAM_PERFORMANCE_DATA_PATH_JSON}")
    os.makedirs(os.path.dirname(TEAM_PERFORMANCE_DATA_PATH_JSON), exist_ok=True)
    with open(TEAM_PERFORMANCE_DATA_PATH_JSON, 'w') as json_file:
        json.dump(team_performance_data_serializable, json_file, indent=4)

    # Save team performance data (CSV)
    print(f"[INFO] Saving CSV team performance data to: {TEAM_PERFORMANCE_DATA_PATH_CSV}")
    os.makedirs(os.path.dirname(TEAM_PERFORMANCE_DATA_PATH_CSV), exist_ok=True)

    with open(TEAM_PERFORMANCE_DATA_PATH_CSV, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        if team_performance_data_serializable:
            header = list(team_performance_data_serializable.values())[0].keys()
            csv_writer.writerow(header)

            for item in team_performance_data_serializable.values():
                csv_writer.writerow(item.values())

    print("\n[INFO] Script 04: Completed.")

except Exception as e:
    print(f"\n[ERROR] An unexpected error occurred: {e}")
    print(traceback.format_exc())
    print("\nScript 04: Failed.")

seperation_bar()
