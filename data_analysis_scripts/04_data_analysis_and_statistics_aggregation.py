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
# CUSTOM METRICS CLASS
# ===========================

class CustomMetrics:
    """
    Define your custom metrics here. Each function should:
    - Take a pandas DataFrame (df) as input (data for one team)
    - Return a single calculated value.
    - Be decorated with @staticmethod.
    """

    @staticmethod
    def consistency_score(df):
        """Computes how consistent a team is across all matches."""
        consistency_scores = []
        for column in df.columns:
            if df[column].dtype in [np.float64, np.int64]:  # Quantitative
                std_dev = df[column].std()
                mean_val = df[column].mean()
                cv = std_dev / mean_val if mean_val != 0 else 1
                consistency_scores.append(1 - min(cv, 1))
            elif df[column].dtype == "O":  # Categorical
                most_common = df[column].value_counts().max()
                consistency_scores.append(most_common / len(df))
            elif df[column].dtype == bool:  # Binary
                major_value_count = max(df[column].sum(), len(df) - df[column].sum())
                consistency_scores.append(major_value_count / len(df))
        return round(np.mean(consistency_scores), 3) if consistency_scores else 0

    # ✅ Add new custom metrics here
    # @staticmethod
    # def your_new_metric(df):
    #     return your_calculation_here


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
        return '"' + ", ".join(map(str, obj)) + '"'  # Ensure CSV stores as a single cell
    return obj

def determine_statistical_type(variable_name):
    """Returns the statistical data type (quantitative, categorical, binary) based on the expected structure."""
    if variable_name in FLATTENED_EXPECTED_VARIABLES:
        return FLATTENED_EXPECTED_VARIABLES[variable_name].get("statistical_data_type", "unknown")
    print(f"[WARNING] Variable '{variable_name}' not found in expected data structure.")
    return "unknown"

def calculate_team_performance_data(team_data):
    """
    Computes performance metrics and applies custom metrics per team.

    :param team_data: Dictionary containing match data for each team.
    :return: A dictionary with aggregated team statistics.
    """
    all_team_performance_data = {}

    for team, data in team_data.items():
        matches = data.get("matches", [])
        if not matches:
            all_team_performance_data[team] = {"team_name": team, "number_of_matches": 0}
            continue

        # Flatten only the variables inside each match
        flat_data = [{k: v for k, v in flatten_expected_vars(match["variables"]).items()} for match in matches]
        df = pd.DataFrame(flat_data)

        # Drop empty columns
        df.dropna(axis=1, how="all", inplace=True)

        team_performance = {"team_name": team, "number_of_matches": len(df)}

        # Store raw match values for each metric as a **string** for CSV compatibility
        for column in df.columns:
            team_performance[f"{column}_values"] = convert_to_serializable(df[column].tolist())

        # Apply all custom metrics automatically
        for metric_name in dir(CustomMetrics):
            if not metric_name.startswith("__") and callable(getattr(CustomMetrics, metric_name)):
                metric_func = getattr(CustomMetrics, metric_name)
                team_performance[metric_name] = metric_func(df)

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
        sample_team = list(team_performance_data.values())[0]
        headers = ["team"] + list(sample_team.keys())

        csv_writer.writerow(headers)
        for team, metrics in team_performance_data.items():
            row = [team] + [convert_to_serializable(metrics[k]) for k in sample_team.keys()]
            csv_writer.writerow(row)

    print("\n[INFO] Script 04: Completed.")

except Exception as e:
    print(f"\n[ERROR] {e}")
    print(traceback.format_exc())

seperation_bar()
