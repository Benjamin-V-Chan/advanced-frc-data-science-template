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
    pass

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

print()
print(expected_data_structure_vars)

print(seperation_bar)