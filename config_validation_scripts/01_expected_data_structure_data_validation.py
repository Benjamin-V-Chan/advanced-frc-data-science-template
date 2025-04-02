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

    # Check top-level key
    if 'metadata' not in expected_data_structure:
        warn_missing_key(
            key_name="metadata",
            function_name=function_name,
            location="expected_data_structure",
            code="W101"
        )
        return

    expected_metadata = expected_data_structure['metadata']

    # Iterate over each metadata item
    for key, properties in expected_metadata.items():
        if not isinstance(properties, dict):
            warn_invalid_type(
                key_or_field=key,
                expected_type="dict",
                actual_value=properties,
                function_name=function_name,
                location=f"metadata.{key}",
                code="W102"
            )
            continue

        if "statistical_data_type" not in properties:
            warn_missing_key(
                key_name="statistical_data_type",
                function_name=function_name,
                location=f"metadata.{key}",
                code="W103"
            )
            continue

        expected_type = properties["statistical_data_type"]

        if expected_type not in statistical_data_type_options:
            warn_invalid_value(
                key_or_field=f"metadata.{key}.statistical_data_type",
                expected_condition=f"one of {statistical_data_type_options}",
                actual_value=expected_type,
                function_name=function_name,
                location=f"metadata.{key}",
                code="W104"
            )
            continue

        # If 'categorical', check 'values'
        if expected_type == "categorical":
            if "values" not in properties:
                warn_missing_key(
                    key_name="values",
                    function_name=function_name,
                    location=f"metadata.{key}",
                    code="W105"
                )
                continue

            if not isinstance(properties["values"], list) or len(properties["values"]) < 1:
                warn_invalid_value(
                    key_or_field=f"metadata.{key}.values",
                    expected_condition="non-empty list",
                    actual_value=properties["values"],
                    function_name=function_name,
                    location=f"metadata.{key}",
                    code="W106"
                )
                continue

            if len(set(properties["values"])) != len(properties["values"]):
                warn_duplicate_value(
                    key_or_field=f"metadata.{key}.values",
                    actual_values=properties["values"],
                    function_name=function_name,
                    location=f"metadata.{key}",
                    code="W107"
                )

            if key == "robotPosition":
                invalid_positions = [
                    pos for pos in properties["values"] 
                    if pos not in valid_robot_positions
                ]
                if invalid_positions:
                    log_warning(
                        f"Invalid robot positions: {invalid_positions}. "
                        f"Must be one of {valid_robot_positions}.",
                        function_name=function_name,
                        issue_type="invalid_value",
                        location=f"metadata.{key}",
                        code="W108"
                    )


def validate_app_variables(expected_data_structure, top_level_key, code_base=200):
    """
    Generic validator for any top-level key containing variables 
    (e.g. 'matchapp_variables', 'superapp_variables') that need:
    
      1) a 'statistical_data_type'
      2) a known data type from statistical_data_type_options
      3) additional checks if 'categorical'
    
    :param expected_data_structure: full dictionary of the config
    :param top_level_key: something like 'matchapp_variables' or 'superapp_variables'
    :param code_base: an integer offset for generating distinct warning codes 
                     (e.g., 200 for matchapp, 300 for superapp).
    """
    function_name = f"validate_{top_level_key}"

    # Check presence
    if top_level_key not in expected_data_structure:
        warn_missing_key(
            key_name=top_level_key,
            function_name=function_name,
            location="expected_data_structure",
            code=f"W{code_base+1}"
        )
        return

    # Flatten the sub-structure for easy iteration
    flattened_vars = flatten_vars_in_dict(
        expected_data_structure[top_level_key],
        return_dict={}
    )

    # Iterate over each variable
    for var_key, var_properties in flattened_vars.items():
        # Must have 'statistical_data_type'
        if "statistical_data_type" not in var_properties:
            warn_missing_key(
                key_name="statistical_data_type",
                function_name=function_name,
                location=f"{top_level_key}.{var_key}",
                code=f"W{code_base+2}"
            )
            continue

        expected_type = var_properties["statistical_data_type"]

        # Must be valid data type
        if expected_type not in statistical_data_type_options:
            warn_invalid_value(
                key_or_field=f"{top_level_key}.{var_key}.statistical_data_type",
                expected_condition=f"one of {statistical_data_type_options}",
                actual_value=expected_type,
                function_name=function_name,
                location=f"{top_level_key}.{var_key}",
                code=f"W{code_base+3}"
            )
            continue

        # If 'categorical', check 'values'
        if expected_type == "categorical":
            if "values" not in var_properties:
                warn_missing_key(
                    key_name="values",
                    function_name=function_name,
                    location=f"{top_level_key}.{var_key}",
                    code=f"W{code_base+4}"
                )
                continue

            if (not isinstance(var_properties["values"], list) 
                or len(var_properties["values"]) < 1):
                warn_invalid_value(
                    key_or_field=f"{top_level_key}.{var_key}.values",
                    expected_condition="non-empty list",
                    actual_value=var_properties["values"],
                    function_name=function_name,
                    location=f"{top_level_key}.{var_key}",
                    code=f"W{code_base+5}"
                )
                continue

            if len(set(var_properties["values"])) != len(var_properties["values"]):
                warn_duplicate_value(
                    key_or_field=f"{top_level_key}.{var_key}.values",
                    actual_values=var_properties["values"],
                    function_name=function_name,
                    location=f"{top_level_key}.{var_key}",
                    code=f"W{code_base+6}"
                )

            # Suggest 'binary' if it's just True/False
            if (True in var_properties["values"] or False in var_properties["values"]) \
               and len(var_properties["values"]) == 2:
                log_warning(
                    "Contains only True/False values; consider setting as 'binary'.",
                    function_name=function_name,
                    issue_type="invalid_value",
                    location=f"{top_level_key}.{var_key}",
                    code=f"W{code_base+7}"
                )


# ===========================
# MAIN SCRIPT
# ===========================
def main():
    
    # SCRIPT START
    script_start("[Data Generation] 02 - expected_data_structure Config Validation")



    # LOAD CONFIG
    log_header("Load Config")
    
    log_info(f"Loading 'Expected Data Structure JSON Config' from '{EXPECTED_DATA_STRUCTURE_PATH}'")
    expected_data_structure = retrieve_json(EXPECTED_DATA_STRUCTURE_PATH)

    log_info(f"Expected Data Structure JSON Config:\n{json.dumps(expected_data_structure, indent=4)}\n")



    # CONFIG VALIDATION
    log_header("Config Validation")
    
    validate_metadata(expected_data_structure)
    validate_app_variables(expected_data_structure, "matchapp_variables", code_base=200)
    validate_app_variables(expected_data_structure, "superapp_variables", code_base=300)



    # SCRIPT END
    script_end("[Data Generation] 02 - expected_data_structure Config Validation")


if __name__ == "__main__":
    main()
