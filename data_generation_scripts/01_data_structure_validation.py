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
            # print(dictionary[key])
            return False
    return True

def flatten_vars_in_dict(dictionary, main_dict = {}):
    for key in dictionary:
        # print()
        # print(f"{key}: {dictionary[key]}")
        if single_dict(dictionary[key]):
            # print("single dict confirmed")
            main_dict[key] = dictionary[key]
        else:
            # print("nested dict confirmed")
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

# validate correctness of expected data structure vars
    # log detailed print log errors
    # include location of error, and neccessary change based off prewritten rule



# set base var properties constants for data_type and statistical_data_type consistency

list_of_expected_data_structure_var_keys = []
for key in expected_data_structure_vars:
    if type(key) != str:
        print(f"[ERROR] {key} invalid var key data type: must be 'str'")
    list_of_expected_data_structure_var_keys.append(key)

if set(list_of_expected_data_structure_var_keys) != list_of_expected_data_structure_var_keys:
    print(f"[ERROR] invalid variable keys '{list_of_expected_data_structure_var_keys}'. must contain no repeat variable keys")

# iterate through each key-val pair
    # check for consistent data_type and statistical_data_type properties based off known constants
        # ensure property exists
        # backcheck each property (data_type and statistical_data_type) with known constants using 'in' keyword
        # use iteration to avoid uneccessary statments for each of the 6 checks
        # NOTE: later will be changing to be more detailed for quantitative and binary statistical data type variables
        # NOTE: for now the base var properties system will allow for efficient filtering
        # NOTE: will restructure and recode the revamped system once initial system is complete

    # for categorical variable specifically, also check for consistent values property
     # ensure the chosen values within the value property are rigourously tested for edge cases
     # examples: 
        # ensure property exists
        # ensuring correct data type (no true/false since could just use binary statistical data type)
        # len >= 2
        # values property data type is list
        # no repeats



print()
print(expected_data_structure_vars)

print(seperation_bar)