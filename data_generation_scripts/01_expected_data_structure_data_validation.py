
import json
from utils.seperation_bars import *
from utils.dictionary_manipulation import *

# ===========================
# CONFIGURATION SECTION
# ===========================

expected_data_structure_path = 'config/expected_data_structure.json'

# ===========================
# CONSTANTS SECTION
# ===========================

statistical_data_type_options = ['quantitative', 'categorical', 'binary']
valid_robot_positions = ['red_1', 'red_2', 'red_3', 'blue_1', 'blue_2', 'blue_3']

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

    expected_data_structure_metadata = expected_data_structure['metadata']

    if 'scouterName' in expected_data_structure_metadata:
        if expected_data_structure_metadata['scouterName'] != 'str':
            print(f"[ERROR] invalid value '{expected_data_structure_metadata['scouterName']}' for set data type: must be 'str'")
    else:
        print(f"[ERROR] missing 'scouterName' key in 'metadata' key: must contain 'scouterName' key")

    if 'matchNumber' in expected_data_structure_metadata:
        if expected_data_structure_metadata['matchNumber'] != 'int':
            print(f"[ERROR] invalid value '{expected_data_structure_metadata['matchNumber']}' for set data type: must be 'int'")
    else:
        print(f"[ERROR] missing 'matchNumber' key in 'metadata' key: must contain 'matchNumber' key")

    if 'robotTeam' in expected_data_structure_metadata:
        if expected_data_structure_metadata['robotTeam'] != 'int':
            print(f"[ERROR] invalid value '{expected_data_structure_metadata['robotTeam']}' for set data type: must be 'int'")
    else:
        print(f"[ERROR] missing 'robotTeam' key in 'metadata' key: must contain 'robotTeam' key")

    if 'robotPosition' in expected_data_structure_metadata:
        if 'values' in expected_data_structure_metadata['robotPosition']:
            if len(expected_data_structure_metadata['robotPosition']['values']) == 6:
                for val in expected_data_structure_metadata['robotPosition']['values']:
                    if isinstance(val, str):
                        if val not in valid_robot_positions:
                            print(f"[ERROR] invalid value '{val}' in 'values' key in 'robotPosition' key in 'metadata': must be one of the following valid robot positions: {valid_robot_positions}")
                    else:
                        print(f"[ERROR] invalid data type '{type(val)}' for value in 'values' key in 'robotPosition' key in 'metadata': must be 'str'")
    else:
        print(f"[ERROR] missing 'robotPosition' key in 'metadata' key: must contain 'robotPosition' key")
        
else:
    print()



# VARIABLE KEY CHECKS
small_seperation_bar("EXPECTED DATA STRUCTURE: VARIABLE KEY CHECKS")

# Retrieve Expected Data Structure Variables
expected_data_structure_vars = flatten_vars_in_dict(expected_data_structure["variables"], return_dict={})

# Keys checks for expected data structure var keys
list_of_expected_data_structure_vars = []
list_of_expected_data_structure_vars = expected_data_structure_vars.keys()

for key in list_of_expected_data_structure_vars:
    if type(key) != str:
        print(f"[ERROR] {key} invalid var key data type: must be 'str'")

if set(list_of_expected_data_structure_vars) != list_of_expected_data_structure_vars:
    print(f"[ERROR] invalid variable keys '{list_of_expected_data_structure_vars}': must contain no repeat variable keys")




# SPECIFIC VARIABLE CHECKS (FOR CATEGORICAL STATISTICAL_DATA_TYPE)
small_seperation_bar("EXPECTED DATA STRUCTURE: SPECIFIC VARIABLE CHECKS")

for var_key, var_value in expected_data_structure_vars.items():

    if 'statistical_data_type' in var_value:

        if var_value['statistical_data_type'] in statistical_data_type_options:

            # Categorical Variable Property Checks (due to extra 'values' property)
            if var_value['statistical_data_type'] == 'categorical':
                if 'values' in var_value:
                    if type(var_value['values']) == list:
                        var_values_count = len(var_value['values'])
                        if var_values_count <= 1:
                            print(f"[ERROR] categorical variable {var_key} has invalid count '{len(var_value['values'])}' for 'values' property: must be >= 1")
                        if len(set(var_value['values'])) != var_values_count:
                            print(f"[ERROR] categorical variable {var_key} has invalid values '{var_value['values']}' for 'values' property: must contain no repeat values")
                        if (True in var_value['values'] or False in var_value['values']) and var_values_count == 2:
                            print(f"[ERROR] categorical variable {var_key} contains invalid data type 'binary' for 'values' property: must set statistical data type to 'binary' if true or false is being used")
                    else:
                        print(f"[ERROR] categorical variable {var_key} has invalid data type '{type(var_value['values'])}' for 'values' property: must be 'list' data type")
                else:
                    print(f"[ERROR] categorical variable {var_key} has no 'values' property: vars with categorical statistical data type must have 'values' property")
        else:
            print(f"[ERROR] {var_key} has invalid value '{var_value['statistical_data_type']}' for 'statistical_data_type' property: must be one of the following; {statistical_data_type_options}")

    else:
        print(f"[ERROR] {var_key} has no 'statistical_data_type' property")




# END OF SCRIPT

seperation_bar()