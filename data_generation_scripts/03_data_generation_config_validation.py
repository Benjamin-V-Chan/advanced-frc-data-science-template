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
print("Script 03: Data Generation Config Validation\n")




# RETRIEVE DATA
small_seperation_bar("DATA GENERATION CONFIG: RETRIEVE DATA")

# Retrieve Expected Data Structure JSON as Dict
expected_data_structure = retrieve_json(expected_data_structure_path)
print("\nExpected Data Structure JSON:")
print(json.dumps(expected_data_structure, indent=4))

# Retrieve Data Generation Configuration JSON as Dict
data_generation_config = retrieve_json(data_generation_config_path)
print("\nData Generation Configuration JSON:")
print(json.dumps(data_generation_config, indent=4))





# OFFICIAL START FOR DATA CHECKS
small_seperation_bar("DATA GENERATION CONFIG CHECKS")



if data_generation_config['running_data_generation']:

    print("[INFO] Running Data Generation Set ON")




    # DATA QUANTITY CHECKS
    small_seperation_bar("DATA GENERATION CONFIG: DATA QUANTITY CHECKS")

    if 'data_quantity' in data_generation_config:

        data_generation_config_data_quantity = data_generation_config['data_quantity']

        if 'number_of_teams' in data_generation_config_data_quantity:
            if isinstance(data_generation_config_data_quantity['number_of_teams'], int):
                if not (data_generation_config_data_quantity['number_of_teams'] >= 6):
                    print(f"[ERROR] invalid value {data_generation_config_data_quantity['number_of_teams']} for 'number_of_teams' key in 'data_quantity' key: must be >= 6")
            else:
                print(f"[ERROR invalid data type for 'number_of_matches_per_team' key; '{type(data_generation_config_data_quantity['number_of_matches_per_team'])}' in 'data_quantity': must be 'int' data type")
        else:
            print(f"[ERROR] missing 'number_of_teams' key in 'data_quantity' key: must contain 'number_of_teams' key")

        if 'number_of_matches_per_team' in data_generation_config_data_quantity:
            if isinstance(data_generation_config_data_quantity['number_of_matches_per_team'], int):
                if not (data_generation_config_data_quantity['number_of_matches_per_team'] > 0):
                    print(f"[ERROR] invalid value {data_generation_config_data_quantity['number_of_matches_per_team']} for 'numbers_of_matches_per_team' key in 'data_quantity' key: must be > 0")
            else:
                print(f"[ERROR invalid data type for 'number_of_matches_per_team' key; '{type(data_generation_config_data_quantity['number_of_matches_per_team'])}' in 'data_quantity': must be 'int' data type")
        else:
            print(f"[ERROR] missing 'number_of_matches_per_team' key in 'data_quantity' key: must contain 'number_of_matches_per_team' key")
    
    else:
        print(f"[ERROR] missing 'data_quantity' key: must contain 'data_quantity' key")