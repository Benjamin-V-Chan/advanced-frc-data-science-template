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


# END OF SCRIPT

seperation_bar()