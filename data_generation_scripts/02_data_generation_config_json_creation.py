# based off of info in expected_data_structure.json, will generate a new json that is a default template for data_generation_condig.json
# should use info about var names and statistical data types to make sure template is good
# users can further personalize the config later if needed

import json
from utils.seperation_bars import *
from utils.dictionary_manipulation import *

# ===========================
# CONFIGURATION SECTION
# ===========================

data_generation_config_path = 'data_generation_config.json'
expected_data_structure_path = 'expected_data_structure.json'
data_generation_config_default_values_path = 'data_generation_config_default_values_config.json'

# ===========================
# CONSTANTS SECTION
# ===========================

statistical_data_type_options = ['quantitative', 'categorical', 'binary']
valid_robot_positions = ['red_1', 'red_2', 'red_3', 'blue_1', 'blue_2', 'blue_3']

# ===========================
# MAIN SCRIPT SECTION
# ===========================

seperation_bar()
print("Script 01: Data Generation Config JSON Creation\n")



# Retrieve JSON Data
small_seperation_bar("RETRIEVE expected_data_structure.json")

# Retrieve Expected Data Structure JSON as Dict
expected_data_structure_dict = retrieve_json(expected_data_structure_path)
print("\nExpected Data Structure JSON:")
print(json.dumps(expected_data_structure_dict, indent=4))

# Retrieve Data Generation Config Default Values JSON as Dict
data_generation_config_default_values_dict = retrieve_json(data_generation_config_default_values_path)
print("\nData Generation Config Default Values JSON:")
print(json.dumps(data_generation_config_default_values_dict, indent=4))



# Data Generation Config Creation
expected_data_structure_variables = flatten_vars_in_dict(expected_data_structure_dict['variables'])
print(expected_data_structure_variables)

# Initialization of data_generation_config dict
data_generation_config_dict = {}

# Adding the NON-variable dicts to the data_generation_config_dict
print(data_generation_config_default_values_dict)
for key, val in data_generation_config_default_values_dict.items():
    if key != 'variables':
        data_generation_config_dict[key] = val

print(data_generation_config_dict)