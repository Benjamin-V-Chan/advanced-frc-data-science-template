import json
from utils.logging import *
from utils.dictionary_manipulation import *

# ===========================
# CONFIGURATION
# ===========================

DATA_GENERATION_CONFIG_PATH = 'config/data_generation_config.json'
EXPECTED_DATA_STRUCTURE_PATH = 'config/expected_data_structure.json'

# ===========================
# CONSTANTS
# ===========================

STATISTICAL_DATA_TYPE_OPTIONS = ['quantitative', 'categorical', 'binary']
VALID_ROBOT_POSITIONS = ['red_1', 'red_2', 'red_3', 'blue_1', 'blue_2', 'blue_3']

# ===========================
# HELPER FUNCTIONS
# ===========================

# ===========================
# VALIDATION FUNCTIONS
# ===========================


# ===========================
# MAIN SCRIPT
# ===========================



def main():
    script_start("[Data Generation] Script 03: Data Generation Config Validation")



    # LOAD CONFIG
    log_header("Load Config")
    
    log_info(f"Loading 'Expected Data Structure JSON Config' from '{EXPECTED_DATA_STRUCTURE_PATH}'")
    expected_data_structure = retrieve_json(EXPECTED_DATA_STRUCTURE_PATH)

    log_info(f"Expected Data Structure JSON Config: \n{json.dumps(expected_data_structure, indent=4)}\n")
    
    
    
    # LOAD DATA
    log_header("Load Data")

    log_info(f"Loading 'Expected  Data' from '{RAW_DATA_PATH}'")
    expected_data_structure = retrieve_json(EXPECTED_DATA_STRUCTURE_PATH)

    data_generation_config = retrieve_json(DATA_GENERATION_CONFIG_PATH)

    # OFFICIAL START FOR DATA CHECKS
    log_header("DATA GENERATION CONFIG CHECKS")
    if data_generation_config.get('running_data_generation'):
        log_info("Running Data Generation Set ON")

        # DATA QUANTITY CHECKS
        log_header("DATA GENERATION CONFIG: DATA QUANTITY CHECKS")
        if 'data_quantity' in data_generation_config:
            data_quantity = data_generation_config['data_quantity']

            if 'teams_per_match' in data_quantity:
                if not isinstance(data_quantity['teams_per_match'], int):
                    log_warning(f"Invalid data type for 'teams_per_match' key; received {type(data_quantity['teams_per_match'])} in 'data_quantity'. Expected int.")
            else:
                log_warning("Missing 'teams_per_match' key in 'data_quantity'.")

            if 'number_of_teams' in data_quantity:
                if isinstance(data_quantity['number_of_teams'], int):
                    if data_quantity['number_of_teams'] <= data_quantity.get('teams_per_match', 0):
                        log_warning(f"Invalid value {data_quantity['number_of_teams']} for 'number_of_teams': must be >= teams_per_match ({data_quantity.get('teams_per_match', 'undefined')}).")
                else:
                    log_warning(f"Invalid data type for 'number_of_teams' key; received {type(data_quantity['number_of_teams'])} in 'data_quantity'. Expected int.")
            else:
                log_warning("Missing 'number_of_teams' key in 'data_quantity'.")

            if 'number_of_matches_per_team' in data_quantity:
                if isinstance(data_quantity['number_of_matches_per_team'], int):
                    if data_quantity['number_of_matches_per_team'] <= 0:
                        log_warning(f"Invalid value {data_quantity['number_of_matches_per_team']} for 'number_of_matches_per_team': must be > 0.")
                else:
                    log_warning(f"Invalid data type for 'number_of_matches_per_team' key; received {type(data_quantity['number_of_matches_per_team'])} in 'data_quantity'. Expected int.")
            else:
                log_warning("Missing 'number_of_matches_per_team' key in 'data_quantity'.")
        else:
            log_warning("Missing 'data_quantity' key in configuration.")

        # SCOUTER NAMES CHECK
        if 'scouter_names' in data_generation_config:
            if isinstance(data_generation_config['scouter_names'], list):
                if len(data_generation_config['scouter_names']) <= data_quantity.get('teams_per_match', 0):
                    log_warning(f"Invalid length of 'scouter_names' list ({len(data_generation_config['scouter_names'])}): must be >= teams_per_match ({data_quantity.get('teams_per_match', 'undefined')}). Received list: {data_generation_config['scouter_names']}")
            else:
                log_warning(f"Invalid data type for 'scouter_names' key; received {type(data_generation_config['scouter_names'])} in configuration. Expected list.")
        else:
            log_warning("Missing 'scouter_names' key in configuration.")

        # VARIABLE KEY CHECKS
        log_header("DATA GENERATION CONFIG: VARIABLE KEY CHECKS")
        log_info(f"Data Generation Config Variables:\n{data_generation_config.get('variables')}")
        data_generation_config_vars = flatten_vars_in_dict(data_generation_config.get('variables', {}), return_dict={})
        list_of_var_keys = list(data_generation_config_vars.keys())

        for key in list_of_var_keys:
            if not isinstance(key, str):
                log_warning(f"Variable key {key} is not of type str.")

        if len(list_of_var_keys) != len(set(list_of_var_keys)):
            log_warning(f"Duplicate variable keys found: {list_of_var_keys}")

        expected_data_structure_vars = flatten_vars_in_dict(expected_data_structure.get("variables", {}), return_dict={})

        for var_key, var_value in data_generation_config_vars.items():
            if var_key in expected_data_structure_vars:
                var_stat_type = expected_data_structure_vars[var_key].get('statistical_data_type')

                # MISSING VALUES CHANCE CHECKS
                log_header("DATA GENERATION CONFIG: MISSING VALUES CHANCE CHECKS")
                if 'missing_values_chance' in var_value:
                    if isinstance(var_value['missing_values_chance'], (int, float)):
                        if not (0 < var_value['missing_values_chance'] < 1):
                            log_warning(f"Invalid value {var_value['missing_values_chance']} for 'missing_values_chance' in {var_key}: must be between 0 and 1.")
                    else:
                        log_warning(f"Invalid data type for 'missing_values_chance' in {var_key}; received {type(var_value['missing_values_chance'])}. Expected int or float.")
                else:
                    log_warning(f"Missing 'missing_values_chance' key in {var_key}.")

                # STATISTICAL DATA TYPE SPECIFIC CHECKS
                log_header("DATA GENERATION CONFIG: STATISTICAL DATA TYPE SPECIFIC CHECKS")
                if var_stat_type == 'quantitative':
                    if 'data_deviation' in var_value:
                        data_deviation = var_value['data_deviation'][0]
                        if 'mean' in data_deviation:
                            if not isinstance(data_deviation['mean'], (int, float)):
                                log_warning(f"Invalid data type for 'mean' in {var_key}; received {type(data_deviation['mean'])}. Expected int or float.")
                        else:
                            log_warning(f"Missing 'mean' key in data deviation for {var_key}.")

                        if 'standard_deviation' in data_deviation:
                            if not isinstance(data_deviation['standard_deviation'], (int, float)):
                                log_warning(f"Invalid data type for 'standard_deviation' in {var_key}; received {type(data_deviation['standard_deviation'])}. Expected int or float.")
                        else:
                            log_warning(f"Missing 'standard_deviation' key in data deviation for {var_key}.")
                    else:
                        log_warning(f"Missing 'data_deviation' key in {var_key}.")

                    if 'missing_values_filler' in var_value:
                        if not isinstance(var_value['missing_values_filler'], (int, float)):
                            log_warning(f"Invalid data type for 'missing_values_filler' in {var_key}; received {type(var_value['missing_values_filler'])}. Expected int or float.")
                    else:
                        log_warning(f"Missing 'missing_values_filler' key in {var_key}.")

                    if 'positive_outliers_chance' in var_value:
                        if isinstance(var_value['positive_outliers_chance'], (int, float)):
                            if not (0 < var_value['positive_outliers_chance'] < 1):
                                log_warning(f"Invalid value {var_value['positive_outliers_chance']} for 'positive_outliers_chance' in {var_key}: must be between 0 and 1.")
                        else:
                            log_warning(f"Invalid data type for 'positive_outliers_chance' in {var_key}; received {type(var_value['positive_outliers_chance'])}. Expected int or float.")
                    else:
                        log_warning(f"Missing 'positive_outliers_chance' key in {var_key}.")

                    if 'positive_outliers_amount_of_std_devs' in var_value:
                        if isinstance(var_value['positive_outliers_amount_of_std_devs'], (int, float)):
                            if var_value['positive_outliers_amount_of_std_devs'] <= 0:
                                log_warning(f"Invalid value for 'positive_outliers_amount_of_std_devs' in {var_key}: {var_value['positive_outliers_amount_of_std_devs']}. Must be greater than 0.")
                        else:
                            log_warning(f"Invalid data type for 'positive_outliers_amount_of_std_devs' in {var_key}; received {type(var_value['positive_outliers_amount_of_std_devs'])}. Expected int or float.")
                    else:
                        log_warning(f"Missing 'positive_outliers_amount_of_std_devs' key in {var_key}.")

                elif var_stat_type in ['categorical', 'binary']:
                    if 'fair_distribution' in var_value:
                        if isinstance(var_value['fair_distribution'], bool):
                            if not var_value['fair_distribution']:
                                log_info("Fair Distribution Set OFF")
                                if 'unfair_distribution' in var_value:
                                    unfair_distribution = var_value['unfair_distribution'][0]
                                    if var_stat_type == 'categorical':
                                        if len(set(unfair_distribution.keys())) == len(unfair_distribution):
                                            expected_values = expected_data_structure_vars[var_key].get('values', [])
                                            if len(unfair_distribution.keys()) == len(expected_values):
                                                val_sum = 0
                                                for key, val in unfair_distribution.items():
                                                    if key not in expected_values:
                                                        log_warning(f"Key '{key}' in unfair_distribution for {var_key} not found in expected values {expected_values}.")
                                                    if isinstance(val, (int, float)):
                                                        if not (0 <= val <= 1):
                                                            log_warning(f"Invalid value {val} for key '{key}' in {var_key}: must be between 0 and 1.")
                                                        val_sum += val
                                                    else:
                                                        log_warning(f"Invalid data type for '{key}' in unfair_distribution for {var_key}; received {type(val)}. Expected int or float.")
                                                if val_sum != 1:
                                                    log_warning(f"Sum of values in unfair_distribution for {var_key} is {val_sum}, must equal 1.")
                                            else:
                                                log_warning(f"Invalid count for unfair_distribution in {var_key}: expected {len(expected_values)} keys, got {len(unfair_distribution)}.")
                                        else:
                                            log_warning(f"Duplicate keys detected in unfair_distribution for {var_key}.")
                                    elif var_stat_type == 'binary':
                                        if len(unfair_distribution.keys()) == 2:
                                            if "true" not in unfair_distribution.keys():
                                                log_warning(f"Missing 'true' key in unfair_distribution for {var_key}.")
                                            if "false" not in unfair_distribution.keys():
                                                log_warning(f"Missing 'false' key in unfair_distribution for {var_key}.")
                                            val_sum = 0
                                            for key, val in unfair_distribution.items():
                                                if isinstance(val, (int, float)):
                                                    if not (0 <= val <= 1):
                                                        log_warning(f"Invalid value {val} for key '{key}' in {var_key}: must be between 0 and 1.")
                                                    val_sum += val
                                                else:
                                                    log_warning(f"Invalid data type for '{key}' in unfair_distribution for {var_key}; received {type(val)}. Expected int or float.")
                                            if val_sum != 1:
                                                log_warning(f"Sum of values in unfair_distribution for {var_key} is {val_sum}, must equal 1.")
                                        else:
                                            log_warning(f"Invalid count for unfair_distribution in {var_key}: must contain two keys (true/false).")
                                else:
                                    log_warning(f"Missing 'unfair_distribution' key in {var_key}.")
                            else:
                                log_info("Fair Distribution Set ON")
                        else:
                            log_warning(f"Invalid data type for 'fair_distribution' in {var_key}; received {type(var_value['fair_distribution'])}. Expected bool.")
                    else:
                        log_warning(f"Missing 'fair_distribution' key in {var_key}.")

                    if 'missing_values_filler' in var_value:
                        if var_stat_type == 'binary':
                            if not isinstance(var_value['missing_values_filler'], bool):
                                log_warning(f"Invalid data type for 'missing_values_filler' in {var_key}; received {type(var_value['missing_values_filler'])}. Expected bool.")
                        else:
                            if not isinstance(var_value['missing_values_filler'], str):
                                log_warning(f"Invalid data type for 'missing_values_filler' in {var_key}; received {type(var_value['missing_values_filler'])}. Expected str.")
                    else:
                        log_warning(f"Missing 'missing_values_filler' key in {var_key}.")
                else:
                    log_warning(f"[MAJOR ERROR] {var_key} has invalid statistical data type {var_stat_type}.")
            else:
                log_warning(f"Invalid variable {var_key}: not found in expected data structure.")
    else:
        log_info("Running Data Generation Set OFF")

    script_end()

if __name__ == "__main__":
    main()
