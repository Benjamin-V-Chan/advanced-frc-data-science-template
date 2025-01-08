import json
from utility_functions.print_formats import seperation_bar

# ===========================
# CONFIGURATION SECTION
# ===========================

data_generation_config_path = 'data_generation_config.json'
expected_data_structure_path = 'expected_data_structure.json'

# ===========================
# HELPER FUNCTIONS SECTION
# ===========================

def single_dict(dictionary):
    if not isinstance(dictionary, dict):
        return False
    for key in dictionary:
        if isinstance(dictionary[key], dict):
            return False
    return True

def flatten_vars_in_dict(dictionary, main_dict = {}):
    for key in dictionary:
        if single_dict(dictionary[key]):
            main_dict[key] = dictionary[key]
        else:
            flatten_vars_in_dict(dictionary[key])
    return main_dict

# ===========================
# MAIN SCRIPT SECTION
# ===========================

print(seperation_bar)
print("Script 01: Data Structure Validation\n")


# Retrieve Data Generation Configuration JSON as Dict
with open(data_generation_config_path) as json_file:
    data_generation_config = json.load(json_file)
print("\nData Generation Configuration:")
print(json.dumps(data_generation_config, indent=4) + "\n")

# Retrieve Expected Data Structure JSON as Dict
with open(expected_data_structure_path) as json_file:
    expected_data_structure = json.load(json_file)
print("\nExpected Data Structure:")
print(json.dumps(expected_data_structure, indent=4) + "\n")


# Retrieve Expected Data Structure Variables
expected_data_structure_vars = flatten_vars_in_dict(expected_data_structure["variables"])


list_of_expected_data_structure_var_keys = []

for key in expected_data_structure_vars:
    if type(key) != str:
        print(f"[ERROR] {key} invalid var key data type: must be 'str'")
    list_of_expected_data_structure_var_keys.append(key)

if set(list_of_expected_data_structure_var_keys) != list_of_expected_data_structure_var_keys:
    print(f"[ERROR] invalid variable keys '{list_of_expected_data_structure_var_keys}': must contain no repeat variable keys")


statistical_data_type_options = ['quantitative', 'categorical', 'binary']

for var_key, var_value in expected_data_structure_vars.items():

    if 'statistical_data_type' in var_value:

        if var_value['statistical_data_type'] in statistical_data_type_options:

            if var_value['statistical_data_type'] == 'categorical':
                if 'values' in var_value:
                    if type(var_value['values']) == list:
                        var_values_count = len(var_value['values'])
                        if var_values_count <= 1:
                            print(f"[ERROR] categorical variable {var_key} has invalid count '{len(var_value['values'])}' for 'values' property: must be >= 1")
                        if set(var_value['values']) != var_values_count:
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

print(seperation_bar)