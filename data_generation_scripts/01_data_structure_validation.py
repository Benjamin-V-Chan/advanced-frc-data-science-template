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

def flatten_vars_in_dict(dictionary):
    pass

# ===========================
# MAIN SCRIPT SECTION
# ===========================

print(seperation_bar)
print("Script 01: Data Structure Validation\n")

# Get Data Generation Configuration JSON as Dict
with open(data_generation_config_path) as json_file:
    data_generation_config = json.load(json_file)
print("\nData Generation Configuration:")
print(json.dumps(data_generation_config, indent=4) + "\n")

# Get Expected Data Structure JSON as Dict
with open(expected_data_structure_path) as json_file:
    expected_data_structure = json.load(json_file)
print("\nExpected Data Structure:")
print(json.dumps(expected_data_structure, indent=4) + "\n")

# Get Expected Data Structure Variables
expected_data_structure_vars = flatten_vars_in_dict(expected_data_structure["variables"])

print()
print(expected_data_structure_vars)

print(seperation_bar)