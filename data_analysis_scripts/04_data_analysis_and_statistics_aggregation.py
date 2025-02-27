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

# Flatten expected variable structure while keeping properties intact
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

# ===========================
# HELPER FUNCTIONS
# ===========================

def convert_to_serializable(obj):
    """Converts NumPy and Pandas types to standard Python types for JSON serialization."""
    if isinstance(obj, (np.integer, int)):
        return int(obj)
    if isinstance(obj, (np.floating, float)):
        return float(obj) if not np.isnan(obj) else None
    if isinstance(obj, (bool, np.bool_)):
        return int(obj)  # Convert bool to 0/1 for CSV readability
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
    Computes performance metrics and consistency scores for each team.

    :param team_data: Dictionary containing match data for each team.
    :return: A dictionary with aggregated team statistics.
    """
    all_team_performance_data = {}

    for team, data in team_data.items():
        matches = data.get("matches", [])
        if not matches:
            all_team_performance_data[team] = {"team_name": team, "number_of_matches": 0, "consistency_score": 0}
            continue

        # Flatten only the variables inside each match
        flat_data = [{k: v for k, v in flatten_expected_vars(match["variables"]).items()} for match in matches]
        df = pd.DataFrame(flat_data)

        # Drop empty columns
        df.dropna(axis=1, how="all", inplace=True)

        team_performance = {"team_name": team, "number_of_matches": len(df)}
        consistency_scores = []

        print(f"\n[DEBUG] Processing Team {team}: Found {df.shape[1]} variables")  # Debugging

        # Store raw match values for each metric
        for column in df.columns:
            team_performance[f"{column}_values"] = convert_to_serializable(df[column].tolist())

        # Compute statistics based on expected data types
        for column in df.columns:
            stat_type = determine_statistical_type(column)

            print(f"[DEBUG] Processing variable '{column}' as '{stat_type}'")  # Debugging

            if stat_type == "quantitative":
                df[column] = pd.to_numeric(df[column], errors='coerce')  # Ensure numeric conversion
                std_dev = df[column].std()
                mean_val = df[column].mean()
                cv = std_dev / mean_val if mean_val != 0 else 1  # Avoid division by zero

                team_performance[f"{column}_mean"] = convert_to_serializable(mean_val)
                team_performance[f"{column}_std_dev"] = convert_to_serializable(std_dev)
                team_performance[f"{column}_range"] = convert_to_serializable(df[column].max() - df[column].min())

                consistency_scores.append(1 - min(cv, 1))  # Lower CV = higher consistency

            elif stat_type == "categorical":
                value_counts = df[column].value_counts()
                most_common_count = value_counts.max() if not value_counts.empty else 0
                consistency = most_common_count / len(df) if len(df) > 0 else 1

                team_performance[f"{column}_mode"] = value_counts.idxmax() if not value_counts.empty else None
                team_performance[f"{column}_mode_frequency"] = most_common_count

                consistency_scores.append(consistency)

            elif stat_type == "binary":
                df[column] = df[column].astype(str).str.lower().replace({"true": True, "false": False})
                df[column] = df[column].astype(bool)
                major_value_count = max(df[column].sum(), len(df) - df[column].sum())
                consistency_scores.append(major_value_count / len(df))

            else:
                print(f"[ERROR] Unrecognized statistical type for {column}: {stat_type}")

        # Compute overall consistency score
        team_performance["consistency_score"] = round(np.mean(consistency_scores), 3) if consistency_scores else 0

        all_team_performance_data[str(team)] = team_performance  # Ensure team key is a string

    return all_team_performance_data

# ===========================
# MAIN SCRIPT
# ===========================

seperation_bar()
print("Script 04: Data Analysis & Statistics Aggregation\n")

try:
    print("[INFO] Loading team-based match data.")
    with open(TEAM_BASED_MATCH_DATA_PATH, 'r') as infile:
        team_data = json.load(infile)

    team_performance_data = calculate_team_performance_data(team_data)

    # Save JSON
    print(f"[INFO] Saving JSON team performance data to: {TEAM_PERFORMANCE_DATA_PATH_JSON}")
    os.makedirs(os.path.dirname(TEAM_PERFORMANCE_DATA_PATH_JSON), exist_ok=True)
    with open(TEAM_PERFORMANCE_DATA_PATH_JSON, 'w') as json_file:
        json.dump(convert_to_serializable(team_performance_data), json_file, indent=4)

    # Save CSV
    print(f"[INFO] Saving CSV team performance data to: {TEAM_PERFORMANCE_DATA_PATH_CSV}")
    os.makedirs(os.path.dirname(TEAM_PERFORMANCE_DATA_PATH_CSV), exist_ok=True)

    with open(TEAM_PERFORMANCE_DATA_PATH_CSV, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        if team_performance_data:
            sample_team = list(team_performance_data.values())[0]
            headers = ["team"] + list(sample_team.keys())

            csv_writer.writerow(headers)

            for team, metrics in team_performance_data.items():
                row = [team] + [
                    str(metrics[k]) if isinstance(metrics[k], list) else metrics[k]
                    for k in sample_team.keys()
                ]
                csv_writer.writerow(row)

    print("\n[INFO] Script 04: Completed.")

except Exception as e:
    print(f"\n[ERROR] {e}")
    print(traceback.format_exc())

seperation_bar()
