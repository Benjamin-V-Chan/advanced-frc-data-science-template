from utils.dictionary_manipulation import (
    flatten_vars_in_dict, retrieve_json
)
from utils.logging import (
    script_start, script_end, log_header, log_info, log_warning,
    warn_missing_key, warn_invalid_type, warn_invalid_value,
    warn_duplicate_value
)
import json

# ===========================
# CONFIGURATION
# ===========================
EXPECTED_DATA_STRUCTURE_PATH = 'config/expected_data_structure.json'

# ===========================
# CONSTANTS
# ===========================
statistical_data_type_options = ['quantitative', 'categorical', 'binary', 'string']
valid_robot_positions = ['red_1', 'red_2', 'red_3', 'blue_1', 'blue_2', 'blue_3']

# ===========================
# VALIDATION FUNCTIONS
# ===========================

def validate_metadata(expected_data_structure):
    """
    Validates that 'metadata' is present and meets the expected structure.
    """
    function_name = "validate_metadata"

    if 'metadata' not in expected_data_structure:
        warn_missing_key(
            key_name="metadata",
            function_name=function_name,
            location="expected_data_structure",
            code="W101"
        )
        return
# ===========================
# HELPER FUNCTIONS SECTION
# ===========================

def validate_statistical_data_type(key, value, expected_type):
    """Validates that the value matches the expected statistical data type."""
    if expected_type == "quantitative" and not isinstance(value, (int, float)):
        return f"[ERROR] {key} has invalid data type '{type(value).__name__}': must be 'int' or 'float'."
    
    if expected_type == "binary" and not isinstance(value, bool):
        return f"[ERROR] {key} has invalid data type '{type(value).__name__}': must be 'bool'."
    
    if expected_type == "categorical" and not isinstance(value, str):
        return f"[ERROR] {key} has invalid data type '{type(value).__name__}': must be 'str'."
    
    return None

# ===========================
# MAIN SCRIPT SECTION
# ===========================

seperation_bar()
print("Script 01: Expected Data Structure Validation\n")

# RETRIEVE DATA
small_seperation_bar("EXPECTED DATA STRUCTURE: RETRIEVE DATA")

# Retrieve Expected Data Structure JSON as Dict
expected_data_structure = retrieve_json(expected_data_structure_path)
print("\nExpected Data Structure JSON:")
print(json.dumps(expected_data_structure, indent=4))

# OFFICIAL START FOR DATA CHECKS
small_seperation_bar("EXPECTED DATA STRUCTURE CHECKS")

# METADATA CHECKS
small_seperation_bar("EXPECTED DATA STRUCTURE: METADATA CHECKS")

if 'metadata' in expected_data_structure:
    expected_metadata = expected_data_structure['metadata']

    for key, properties in expected_metadata.items():
        if isinstance(properties, dict) and "statistical_data_type" in properties:
            expected_type = properties["statistical_data_type"]

            if expected_type not in statistical_data_type_options:
                print(f"[ERROR] Metadata field '{key}' has invalid statistical data type '{expected_type}': must be one of {statistical_data_type_options}.")
                continue
            
            if expected_type == "categorical" and "values" in properties:
                if not isinstance(properties["values"], list) or len(properties["values"]) < 1:
                    print(f"[ERROR] Metadata field '{key}' has an invalid 'values' property: must be a list with at least one element.")
                elif len(set(properties["values"])) != len(properties["values"]):
                    print(f"[ERROR] Metadata field '{key}' contains duplicate values in 'values' property.")

                # Special case for robotPosition validation
                if key == "robotPosition":
                    invalid_positions = [pos for pos in properties["values"] if pos not in valid_robot_positions]
                    if invalid_positions:
                        print(f"[ERROR] Metadata field 'robotPosition' contains invalid values: {invalid_positions}. Must be one of {valid_robot_positions}.")

        else:
            print(f"[ERROR] Metadata field '{key}' is missing 'statistical_data_type' property.")

else:
    print(f"[ERROR] 'metadata' key is missing from the expected data structure.")

# VARIABLE KEY CHECKS
small_seperation_bar("EXPECTED DATA STRUCTURE: VARIABLE KEY CHECKS")

if "variables" in expected_data_structure:
    expected_variables = flatten_vars_in_dict(expected_data_structure["variables"], return_dict={})

    for var_key, var_properties in expected_variables.items():
        if "statistical_data_type" not in var_properties:
            print(f"[ERROR] Variable '{var_key}' is missing 'statistical_data_type' property.")
            continue

        expected_type = var_properties["statistical_data_type"]

        if expected_type not in statistical_data_type_options:
            print(f"[ERROR] Variable '{var_key}' has invalid statistical data type '{expected_type}': must be one of {statistical_data_type_options}.")
            continue

        # Categorical Variables Checks
        if expected_type == "categorical":
            if "values" not in var_properties:
                print(f"[ERROR] Categorical variable '{var_key}' is missing 'values' property.")
                continue

            if not isinstance(var_properties["values"], list) or len(var_properties["values"]) < 1:
                print(f"[ERROR] Categorical variable '{var_key}' has invalid 'values' property: must be a list with at least one element.")
                continue

            if len(set(var_properties["values"])) != len(var_properties["values"]):
                print(f"[ERROR] Categorical variable '{var_key}' contains duplicate values in 'values' property.")

            if (True in var_properties["values"] or False in var_properties["values"]) and len(var_properties["values"]) == 2:
                print(f"[ERROR] Categorical variable '{var_key}' contains only 'True' and 'False' values: must be set as 'binary' instead.")

else:
    print(f"[ERROR] 'variables' key is missing from the expected data structure.")

# END OF SCRIPT
seperation_bar()

# ===========================
# MAIN SCRIPT
# ===========================
def main():
    script_start("[Data Generation] 02 - expected_data_structure Config Validation")

    # LOAD CONFIG
    log_header("Load Config")
    log_info(f"Loading 'Expected Data Structure JSON Config' from '{EXPECTED_DATA_STRUCTURE_PATH}'")
    
    expected_data_structure = retrieve_json(EXPECTED_DATA_STRUCTURE_PATH)

    log_info(f"Expected Data Structure JSON Config:\n{json.dumps(expected_data_structure, indent=4)}\n")

    # CONFIG VALIDATION
    log_header("Config Validation")
    validate_metadata(expected_data_structure)
    validate_matchapp_variables(expected_data_structure)
    validate_superapp_variables(expected_data_structure)

    script_end("[Data Generation] 02 - expected_data_structure Config Validation")


if __name__ == "__main__":
    main()