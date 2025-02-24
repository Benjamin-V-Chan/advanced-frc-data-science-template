import json
import os
import traceback
from collections import defaultdict
from utils.seperation_bars import *
from utils.dictionary_manipulation import *

# ===========================
# CONFIGURATION SECTION
# ===========================

# File Paths
EXPECTED_DATA_STRUCTURE_PATH = 'config/expected_data_structure.json'
RAW_MATCH_DATA_PATH = "data/raw/generated_raw_match_data.json"
CLEANED_MATCH_DATA_PATH = "data/processed/cleaned_match_data.json"
SCOUTER_LEADERBOARD_PATH = "outputs/statistics/scouter_leaderboard.txt"

# Load Expected Data Structure
EXPECTED_DATA_STRUCTURE_DICT = retrieve_json(EXPECTED_DATA_STRUCTURE_PATH)

# Constants
VALID_ROBOT_POSITIONS = {"red_1", "red_2", "red_3", "blue_1", "blue_2", "blue_3"}
STATISTICAL_DATA_TYPE_OPTIONS = ["quantitative", "categorical", "binary"]

# Flatten the expected variable structure for easy validation
FLATTENED_EXPECTED_VARIABLES = flatten_vars_in_dict(EXPECTED_DATA_STRUCTURE_DICT["variables"])
print(FLATTENED_EXPECTED_VARIABLES)
SHOW_WARNINGS = True

# ===========================
# HELPER FUNCTIONS SECTION
# ===========================

warnings = []
scouter_warnings = defaultdict(int)
scouter_participation = defaultdict(int)
team_match_counts = defaultdict(int)
match_robot_positions = defaultdict(set)

def log_warning(message, scouter=None):
    """Logs a warning and associates it with the scouter."""
    global warnings, scouter_warnings
    warnings.append(message)
    if scouter:
        scouter_warnings[scouter] += 1

def get_expected_type(data_type):
    """Returns the corresponding Python type for a given statistical data type."""
    type_mapping = {
        "quantitative": (int, float),
        "categorical": str,
        "binary": bool
    }
    return type_mapping.get(data_type, str)  # Default to str if unknown

def validate_value(key, value, expected_info, scouter, path=""):
    """
    Validates a single value based on its expected type or predefined values.
    """
    expected_type = expected_info.get("statistical_data_type")
    expected_python_type = get_expected_type(expected_type)

    full_key_path = f"{path}.{key}" if path else key

    # Convert string binary values to boolean
    if expected_type == "binary":
        if isinstance(value, str):
            if value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            else:
                log_warning(f"[WARNING] Invalid binary value '{value}' for '{full_key_path}'. Expected 'true' or 'false'.", scouter)
                return None
        elif not isinstance(value, bool):
            log_warning(f"[WARNING] Incorrect type for '{full_key_path}'. Expected binary (True/False), got {type(value).__name__}.", scouter)
            return None

    # Validate predefined categorical values
    if expected_type == "categorical" and "values" in expected_info:
        if value not in expected_info["values"]:
            log_warning(f"[WARNING] Invalid value '{value}' for '{full_key_path}'. Expected one of {expected_info['values']}.", scouter)
            return None

    # Type validation
    if not isinstance(value, expected_python_type):
        log_warning(f"[WARNING] Incorrect type for '{full_key_path}'. Expected {expected_python_type}, got {type(value).__name__}.", scouter)
        return None

    return value

def validate_structure(data, expected_structure, scouter, path=""):
    """
    Validates and cleans a structure dynamically based on the expected structure.

    :param data: The input data to validate.
    :param expected_structure: The expected structure from the config.
    :param scouter: The scouter responsible for the data.
    :param path: The path to the current key for logging purposes.
    :return: A validated and cleaned version of the data.
    """
    validated = {}

    for key, expected_info in expected_structure.items():
        full_key_path = f"{path}.{key}" if path else key

        if key not in data:
            log_warning(f"[WARNING] Missing key '{full_key_path}'.", scouter)
            continue

        value = data[key]

        # Handle nested dictionaries (recursive validation)
        if isinstance(expected_info, dict) and "statistical_data_type" not in expected_info:
            validated[key] = validate_structure(value, expected_info, scouter, full_key_path)
        else:
            validated_value = validate_value(key, value, expected_info, scouter, path)
            if validated_value is not None:
                validated[key] = validated_value

    return validated

def validate_and_clean_entry(entry):
    """
    Validates and cleans a single entry, ensuring it adheres to the correct structure and rules.

    - Flattens variable dictionary if nested.
    - Ensures all expected fields are present.
    """
    scouter = entry.get("metadata", {}).get("scouterName", "Unknown")
    scouter_participation[scouter] += 1

    validated_entry = {}

    # Validate Metadata
    if "metadata" in entry:
        validated_entry["metadata"] = validate_structure(entry["metadata"], EXPECTED_DATA_STRUCTURE_DICT.get("metadata", {}), scouter)

    # Flatten Variables and Validate
    if "variables" in entry:
        flat_variables = flatten_vars_in_dict(entry["variables"])

        if not flat_variables:  # Ensure variables are not empty
            log_warning(f"[WARNING] No valid variables found for scouter {scouter}. Entry may be missing values.")

        validated_entry["variables"] = validate_structure(flat_variables, FLATTENED_EXPECTED_VARIABLES, scouter)

        if not validated_entry["variables"]:  # If no variables remain, log and keep raw variables
            log_warning(f"[WARNING] All variables removed after validation for scouter {scouter}. Keeping original variables.")
            validated_entry["variables"] = flat_variables

    return validated_entry

def analyze_data_consistency():
    """
    Analyzes data consistency for matches and robot teams.
    """
    global warnings

    # Check team match counts
    match_count_groups = defaultdict(list)
    for team, count in team_match_counts.items():
        match_count_groups[count].append(team)

    if len(match_count_groups) > 1:
        log_warning(
            "[WARNING] Inconsistent match counts detected:\n"
            + "\n".join(
                f"  Teams with {count} matches: {teams}"
                for count, teams in match_count_groups.items()
            )
        )

    # Check match completeness
    for match, positions in match_robot_positions.items():
        if len(positions) != 6:
            missing_positions = VALID_ROBOT_POSITIONS - positions
            log_warning(f"[WARNING] Match {match} is missing positions: {missing_positions}.")

# ===========================
# MAIN SCRIPT SECTION
# ===========================

seperation_bar()
print("Script 02: Data Cleaning and Preprocessing\n")

try:
    small_seperation_bar("LOAD RAW DATA")
    print(f"[INFO] Loading raw data from: {RAW_MATCH_DATA_PATH}")
    with open(RAW_MATCH_DATA_PATH, "r") as infile:
        raw_data = json.load(infile)

    if not isinstance(raw_data, list):
        raise ValueError("Raw data must be a list of matches.")

    cleaned_data = []
    for entry in raw_data:
        cleaned_entry = validate_and_clean_entry(entry)
        cleaned_data.append(cleaned_entry)

    small_seperation_bar("ANALYZE DATA CONSISTENCY")
    analyze_data_consistency()

    print(f"[INFO] Saving cleaned data to: {CLEANED_MATCH_DATA_PATH}")
    os.makedirs(os.path.dirname(CLEANED_MATCH_DATA_PATH), exist_ok=True)
    with open(CLEANED_MATCH_DATA_PATH, "w") as outfile:
        json.dump(cleaned_data, outfile, indent=4)

    if SHOW_WARNINGS:
        print("\n".join(warnings))
    print(f"[INFO] Total warnings/errors: {len(warnings)}")
    print("Script 02: Completed.")

except Exception as e:
    print(f"[ERROR] An unexpected error occurred: {e}")
    print(traceback.format_exc())
    print("Script 02: Failed.")

print(seperation_bar)