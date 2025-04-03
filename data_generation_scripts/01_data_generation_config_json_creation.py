from utils.dictionary_manipulation import *
from utils.logging import *

# ===========================
# CONFIGURATION
# ===========================

EXPECTED_DATA_STRUCTURE_CONFIG_PATH = "config/expected_data_structure.json"
DATA_GENERATION_CONFIG_DEFAULT_VALUES_CONFIG_PATH = "config/data_generation_config_default_values_config.json"

DATA_GENERATION_CONFIG_PATH = "config/data_generation_config.json"

# ===========================
# CONSTANTS
# ===========================

STATISTICAL_DATA_TYPE_OPTIONS = ['quantitative', 'categorical', 'binary', 'string']
VALID_ROBOT_POSITIONS = ['red_1', 'red_2', 'red_3', 'blue_1', 'blue_2', 'blue_3']

# ===========================
# HELPER FUNCTIONS
# ===========================



seperation_bar()
print("Script 02: Data Generation Config JSON Creation\n")



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
print(json.dumps(expected_data_structure_variables, indent=4))



# Initialization of data_generation_config dict
small_seperation_bar("Data Generation Config NON-variables")

data_generation_config_dict = {}

# Adding the NON-variable dicts to the data_generation_config_dict

print(json.dumps(data_generation_config_default_values_dict, indent=4))

for key, val in data_generation_config_default_values_dict.items():
    if key != 'variables':
        data_generation_config_dict[key] = val

data_generation_config_dict['variables'] = {} # Adding later for visual clarity within JSON

print(json.dumps(data_generation_config_dict, indent=4))



small_seperation_bar("Data Generation Config Variables")

# Data generation config default variable values initialization
quantitative_var_default = data_generation_config_default_values_dict['variables']['quantitative']
categorical_var_default = data_generation_config_default_values_dict['variables']['categorical']
binary_var_default = data_generation_config_default_values_dict['variables']['binary']

for key, var in expected_data_structure_variables.items():
    
    var_statistical_data_type = var['statistical_data_type']
    
    # Quantitative Var
    if var_statistical_data_type == 'quantitative':
        data_generation_config_dict['variables'][key] = quantitative_var_default
        
    # Categorical Var
    elif var_statistical_data_type == 'categorical':
        data_generation_config_dict['variables'][key] = categorical_var_default
    
    # Binary Var
    elif var_statistical_data_type == 'binary':
        data_generation_config_dict['variables'][key] = binary_var_default
    
    else:
        print(f"[MAJOR ERROR] INVALID STATISTICAL DATA TYPE")

print(json.dumps(data_generation_config_dict, indent=4))

with open("config/data_generation_config.json", "w") as file:
    json.dump(data_generation_config_dict, file, indent=4)

# END OF SCRIPT

seperation_bar()