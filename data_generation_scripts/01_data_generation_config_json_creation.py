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


# ===========================
# MAIN SCRIPT
# ===========================

def main():
    
    # SCRIPT START
    script_start("[Data Generation] 01 - Data Generation Config JSON Creation")

    
    
    # LOAD CONFIG
    log_header("Load Config")
    
    log_info(f"Loading 'Expected Data Structure Config' from '{EXPECTED_DATA_STRUCTURE_CONFIG_PATH}'")
    expected_data_structure = retrieve_json(EXPECTED_DATA_STRUCTURE_CONFIG_PATH)
    log_info(f"Expected Data Structure Config:\n{json.dumps(expected_data_structure, indent=4)}\n")

    log_info(f"Loading 'Data Geneation Config Default Values Config' from '{DATA_GENERATION_CONFIG_DEFAULT_VALUES_CONFIG_PATH}'")
    data_generation_default_values = retrieve_json(DATA_GENERATION_CONFIG_DEFAULT_VALUES_CONFIG_PATH)
    log_info(f"Data Geneation Config Default Values Config:\n{json.dumps(data_generation_default_values, indent=4)}\n")

    statistical_data_type_defaults = {
        "quantitative": data_generation_default_values['variables']['quantitative'],
        "categorical": data_generation_default_values['variables']['categorical'],
        "binary": data_generation_default_values['variables']['binary'],
        "string": data_generation_default_values['variables']['string']
        }
   
   
    # DATA GENERATION CONFIG CREATION
    log_header("Data Generation Config Creation")

    data_generation_config = {}
    
    
    # Retrieve Expected Data Structure Variables
    log_subheader("Retrieve Expected Data Structure Variables")
    
    expected_data_structure_matchapp_variables = flatten_vars_in_dict(expected_data_structure['matchapp_variables'])
    log_info(f"Expected Data Structure Variables:\n{json.dumps(expected_data_structure_matchapp_variables, indent=4)}")
    
    expected_data_structure_superapp_variables = flatten_vars_in_dict(expected_data_structure['superapp_variables'])
    log_info(f"Expected Data Structure Variables:\n{json.dumps(expected_data_structure_superapp_variables, indent=4)}")
    

    # NON-Variable Properties Creation
    log_subheader("NON-Variable Properties Creation")
    
    for key, val in data_generation_default_values.items():
        if key != "variables":
            data_generation_config[key] = val
    
    log_info(f"Data Generation Config:\n{json.dumps(data_generation_config, indent=4)}")


    # Matchapp Variable Properties Creation
    log_subheader("Matchapp Variable Properties Creation")
    
    fill_variable_data(data_generation_config, expected_data_structure_matchapp_variables, statistical_data_type_defaults, "matchapp_variables")
    

    # Superapp Variable Properties Creation
    log_subheader("Superapp Variable Properties Creation")
        
    fill_variable_data(data_generation_config, expected_data_structure_superapp_variables, statistical_data_type_defaults, "superapp_variables")
    
    
    # SAVE CONFIG
    log_header("Save Config")
    
    log_info(f"Saving 'Data Generation Config' to '{DATA_GENERATION_CONFIG_PATH}'")
    save_json(DATA_GENERATION_CONFIG_PATH, data_generation_config)
    
    
    # SCRIPT END
    script_end("[Data Generation] 01 - Data Generation Config JSON Creation")

if __name__ == "__main__":
    main()