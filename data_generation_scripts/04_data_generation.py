import json
from utils.seperation_bars import *
from utils.dictionary_manipulation import *

# ===========================
# CONFIGURATION SECTION
# ===========================

data_generation_config_path = 'config/data_generation_config.json'
expected_data_structure_path = 'config/expected_data_structure.json'

# ===========================
# CONSTANTS SECTION
# ===========================



# ===========================
# MAIN SCRIPT SECTION
# ===========================



seperation_bar()
print("Script 04: Data Generation\n")



# Retrieve JSON Data
small_seperation_bar("RETRIEVE expected_data_structure.json")

# Retrieve Expected Data Structure JSON as Dict
expected_data_structure_dict = retrieve_json(expected_data_structure_path)
print("\nExpected Data Structure JSON:")
print(json.dumps(expected_data_structure_dict, indent=4))

# Retrieve Data Generation Config Default Values JSON as Dict
data_generation_config_dict = retrieve_json(data_generation_config_path)
print("\nData Generation Config JSON:")
print(json.dumps(data_generation_config_dict, indent=4))

# Data Generation Config Creation
expected_data_structure_variables = flatten_vars_in_dict(expected_data_structure_dict['variables'])
print(json.dumps(expected_data_structure_variables, indent=4))


# END OF SCRIPT

seperation_bar()