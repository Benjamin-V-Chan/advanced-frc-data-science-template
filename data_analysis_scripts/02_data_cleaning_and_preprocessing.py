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
RAW_MATCH_DATA_PATH = "data/raw/formatted_match_data.json"
CLEANED_MATCH_DATA_PATH = "data/processed/cleaned_match_data.json"
SCOUTER_LEADERBOARD_PATH = "outputs/statistics/scouter_leaderboard.txt"

# Load Expected Data Structure
EXPECTED_DATA_STRUCTURE_DICT = retrieve_json(EXPECTED_DATA_STRUCTURE_PATH)

# Constants
VALID_ROBOT_POSITIONS = {"red_1", "red_2", "red_3", "blue_1", "blue_2", "blue_3"}
STATISTICAL_DATA_TYPE_OPTIONS = ["quantitative", "categorical", "binary"]

# Flatten expected variable structure for easy validation
FLATTENED_EXPECTED_VARIABLES = flatten_vars_in_dict(EXPECTED_DATA_STRUCTURE_DICT["variables"])

# Configurable options
SHOW_WARNINGS = True
VOID_MISSING_ENTRIES = True


# ===========================
# HELPER FUNCTIONS
# ===========================

def log_warning(warnings, scouter_warnings, message, scouter=None):
    """Logs a warning and associates it with the scouter."""
    warnings.append(message)
    if scouter:
        scouter_warnings[scouter] += 1

def log_voided_entry(voided_entries, entry):
    """Logs voided entries when missing keys are found."""
    voided_entries.append(entry)

def get_expected_type(data_type):
    """Returns the corresponding Python type for a given statistical data type."""
    type_mapping = {
        "quantitative": (int, float),
        "categorical": str,
        "binary": bool
    }
    return type_mapping.get(data_type, str)  # Default to str if unknown

def validate_value(warnings, key, value, expected_info, scouter, path=""):
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
                log_warning(warnings, scouter, f"[WARNING] Invalid binary value '{value}' for '{full_key_path}'. Expected 'true' or 'false'.")
                return None
        elif not isinstance(value, bool):
            log_warning(warnings, scouter, f"[WARNING] Incorrect type for '{full_key_path}'. Expected binary (True/False), got {type(value).__name__}.")
            return None

    # Validate predefined categorical values
    if expected_type == "categorical" and "values" in expected_info:
        if value not in expected_info["values"]:
            log_warning(warnings, scouter, f"[WARNING] Invalid value '{value}' for '{full_key_path}'. Expected one of {expected_info['values']}.")
            return None

    # Type validation
    if not isinstance(value, expected_python_type):
        log_warning(warnings, scouter, f"[WARNING] Incorrect type for '{full_key_path}'. Expected {expected_python_type}, got {type(value).__name__}.")
        return None

    return value

def validate_structure(warnings, data, expected_structure, scouter, path=""):
    """
    Validates and cleans a structure dynamically based on the expected structure.

    :return: A validated and cleaned version of the data, or None if the entry should be voided.
    """
    validated = {}
    missing_keys = False

    for key, expected_info in expected_structure.items():
        full_key_path = f"{path}.{key}" if path else key

        if key not in data:
            log_warning(warnings, scouter, f"[WARNING] Missing key '{full_key_path}'.")
            missing_keys = True
            continue

        value = data[key]

        # Handle nested dictionaries (recursive validation)
        if isinstance(expected_info, dict) and "statistical_data_type" not in expected_info:
            validated[key] = validate_structure(warnings, value, expected_info, scouter, full_key_path)
        else:
            validated_value = validate_value(warnings, key, value, expected_info, scouter, path)
            if validated_value is not None:
                validated[key] = validated_value

    if VOID_MISSING_ENTRIES and missing_keys:
        return None  # Mark the entry for deletion

    return validated

def validate_and_clean_entry(warnings, voided_entries, entry):
    """
    Validates and cleans a single entry. Removes entry if VOID_MISSING_ENTRIES is enabled and keys are missing.
    """
    scouter = entry.get("metadata", {}).get("scouterName", "Unknown")

    validated_entry = {}

    # Validate Metadata
    if "metadata" in entry:
        validated_metadata = validate_structure(warnings, entry["metadata"], EXPECTED_DATA_STRUCTURE_DICT.get("metadata", {}), scouter)
        if validated_metadata is None:
            log_voided_entry(voided_entries, entry)
            return None  # Mark entry for deletion
        validated_entry["metadata"] = validated_metadata

    # Flatten Variables and Validate
    if "variables" in entry:
        flat_variables = flatten_vars_in_dict(entry["variables"])
        validated_variables = validate_structure(warnings, flat_variables, FLATTENED_EXPECTED_VARIABLES, scouter)

        if validated_variables is None:
            log_voided_entry(voided_entries, entry)
            return None  # Mark entry for deletion

        validated_entry["variables"] = validated_variables

    return validated_entry


# ===========================
# MAIN SCRIPT
# ===========================

def main():
    warnings = []
    voided_entries = []
    scouter_warnings = defaultdict(int)

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
            cleaned_entry = validate_and_clean_entry(warnings, voided_entries, entry)
            if cleaned_entry is not None:
                cleaned_data.append(cleaned_entry)

        print(f"[INFO] Saving cleaned data to: {CLEANED_MATCH_DATA_PATH}")
        os.makedirs(os.path.dirname(CLEANED_MATCH_DATA_PATH), exist_ok=True)
        with open(CLEANED_MATCH_DATA_PATH, "w") as outfile:
            json.dump(cleaned_data, outfile, indent=4)

        if SHOW_WARNINGS:
            print("\n".join(warnings))

        print(f"[INFO] Total warnings/errors: {len(warnings)}")
        print(f"[INFO] Voided Entries: {len(voided_entries)}")
        print("Script 02: Completed.")

    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")
        print(traceback.format_exc())
        print("Script 02: Failed.")

    print(seperation_bar())

if __name__ == "__main__":
    main()
