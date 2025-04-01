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
    small_seperation_bar("DATA GENERATION CONFIG CHECKS")

    if data_generation_config['running_data_generation']:

        print("[INFO] Running Data Generation Set ON")
        
        


        # DATA QUANTITY CHECKS
        small_seperation_bar("DATA GENERATION CONFIG: DATA QUANTITY CHECKS")

        if 'data_quantity' in data_generation_config:

            data_generation_config_data_quantity = data_generation_config['data_quantity']

            if 'teams_per_match' in data_generation_config_data_quantity:
                if not isinstance(data_generation_config_data_quantity['teams_per_match'], int):
                    print(f"[ERROR invalid data type for 'teams_per_match' key; '{type(data_generation_config_data_quantity['teams_per_match'])}' in 'data_quantity': must be 'int' data type")
            else:
                log_warning(" missing 'teams_per_match' key in 'data_quantity' key: must contain 'teams_per_match' key")
                
            if 'number_of_teams' in data_generation_config_data_quantity:
                if isinstance(data_generation_config_data_quantity['number_of_teams'], int):
                    if (data_generation_config_data_quantity['number_of_teams'] <= data_generation_config_data_quantity['teams_per_match']):
                        log_warning(" invalid value {data_generation_config_data_quantity['number_of_teams']} for 'number_of_teams' key in 'data_quantity' key: must be >= teams_per_match ({data_generation_config_data_quantity['teams_per_match']})")
                else:
                    print(f"[ERROR invalid data type for 'number_of_teams' key; '{type(data_generation_config_data_quantity['number_of_teams'])}' in 'data_quantity': must be 'int' data type")
            else:
                log_warning(" missing 'number_of_teams' key in 'data_quantity' key: must contain 'number_of_teams' key")

            if 'number_of_matches_per_team' in data_generation_config_data_quantity:
                if isinstance(data_generation_config_data_quantity['number_of_matches_per_team'], int):
                    if not (data_generation_config_data_quantity['number_of_matches_per_team'] > 0):
                        log_warning(" invalid value {data_generation_config_data_quantity['number_of_matches_per_team']} for 'numbers_of_matches_per_team' key in 'data_quantity' key: must be > 0")
                else:
                    print(f"[ERROR invalid data type for 'number_of_matches_per_team' key; '{type(data_generation_config_data_quantity['number_of_matches_per_team'])}' in 'data_quantity': must be 'int' data type")
            else:
                log_warning(" missing 'number_of_matches_per_team' key in 'data_quantity' key: must contain 'number_of_matches_per_team' key")

        else:
            log_warning(" missing 'data_quantity' key: must contain 'data_quantity' key")

        # SCOUTER NAMES CHECK
        if 'scouter_names' in data_generation_config:
            if isinstance(data_generation_config['scouter_names'], list):
                if (len(data_generation_config['scouter_names']) <= data_generation_config_data_quantity['teams_per_match']):
                    log_warning(" invalid length for of {len(data_generation_config['scouter_names'])} for 'scouter_names' key in 'data_generation_config' key: length must be >= teams_per_match ({data_generation_config_data_quantity['teams_per_match']}). recieved scouter_names list: {data_generation_config['scouter_names']}")
            else:
                print(f"[ERROR invalid data type for 'scouter_names' key; '{type(data_generation_config['scouter_names'])}' in 'data_generation_config': must be 'list' data type")
        else:
            log_warning(" missing 'scouter_names' key in 'data_generation_config' key: must contain 'scouter_names' key")




        # VARIABLE KEY CHECKS
        small_seperation_bar("DATA GENERATION CONFIG: VARIABLE KEY CHECKS")

        # Retrieve Data Generation Config Variables
        print(data_generation_config)
        print(data_generation_config['variables'])
        data_generation_config_vars = flatten_vars_in_dict(data_generation_config['variables'], return_dict={})
        
        # Keys checks for data generation config var keys
        list_of_data_generation_config_var_keys = []
        list_of_data_generation_config_var_keys = data_generation_config_vars.keys()

        for key in list_of_data_generation_config_var_keys:
            if type(key) != str:
                log_warning(" {key} invalid var key data type: must be 'str'")

        if set(list_of_data_generation_config_var_keys) != list_of_data_generation_config_var_keys:
            log_warning(" invalid variable keys '{list_of_data_generation_config_var_keys}': must contain no repeat variable keys")

        # Retrieve Expected Data Structure Variables (for comparison checks)
        expected_data_structure_vars = flatten_vars_in_dict(expected_data_structure["variables"], return_dict={})
        list_of_expected_data_structure_var_keys = expected_data_structure_vars.keys()




        for var_key, var_value in data_generation_config_vars.items():
            # print(f"{var_key}: {var_value}")

            if var_key in expected_data_structure_vars:
                var_key_statistical_data_type = expected_data_structure_vars[var_key]['statistical_data_type']

                


                # MISSING VALUES CHANCE CHECK (ALL STATISTICAL DATA TYPES REQUIRE IT)
                small_seperation_bar("DATA GENERATION CONFIG: MISSING VALUES CHANCE CHECKS")

                if 'missing_values_chance' in var_value:
                    if isinstance(var_value['missing_values_chance'], (int, float)):
                        if not (0 < var_value['missing_values_chance'] < 1):
                            log_warning(" invalid value {var_value['missing_values_chance']} in {var_key} for missing_values_chance: must be between 0 and 1")
                    else:
                        print(f"[ERROR invalid data type for 'missing_values_chance' key; '{type(var_value['missing_values_chance'])}' in {var_key}: must be 'int' or 'float' data type")
                else:
                    log_warning(" missing 'missing_values_chance' key in {var_key}: must contain 'missing_values_chance' key")





                # QUANTITATIVE CHECKS
                small_seperation_bar("DATA GENERATION CONFIG: STATISTICAL DATA TYPE SPECIFIC CHECKS")

                if var_key_statistical_data_type == 'quantitative':



                    # DATA DEVIATION CHECKS
                    if 'data_deviation' in var_value:

                        data_deviation_values = var_value['data_deviation'][0] # so we can access easier. we index [0] because we are initializing structure as a list in the JSONs in order to avoid single dict check

                        # MEAN CHECK
                        if 'mean' in data_deviation_values:
                            if not isinstance(data_deviation_values['mean'], (int, float)):
                                log_warning(" invalid data type for 'mean' key; '{type(data_deviation_values['mean'])}' in {var_key}: must be 'int' or 'float' data type")
                        else:
                            log_warning(" missing 'mean' key in {var_key} data deviation section")


                        # STANDARD DEV CHECK
                        if 'standard_deviation' in data_deviation_values:
                            if not isinstance(data_deviation_values['standard_deviation'], (int, float)):
                                log_warning(" invalid data type for 'standard_deviation' key; '{type(data_deviation_values['mean'])}' in {var_key}: must be 'int' or 'float' data type")
                        else:
                            log_warning(" missing 'standard_deviation' key in {var_key} data deviation section")

                    else:
                        log_warning(" missing 'data_deviation' key in {var_key}: most contain 'data_deviation'")



                    # MISSING VALUES FILLER CHECK (SPECIFIC TO QUANTITATIVE SINCE REQUIRES INT DATA TYPE)
                    if 'missing_values_filler' in var_value:
                        if not isinstance(var_value['missing_values_filler'], (int, float)):
                            log_warning(" invalid data type for 'missing_values_filler' key; '{type(var_value['missing_values_filler'])}' in {var_key}: must be 'int' or 'float' data type")
                    else:
                        log_warning(" missing 'missing_values_filler' key in {var_key}: must contain 'missing_values_filler' key")



                    # POSITIVE OUTLIERS CHANCE CHECK
                    if 'positive_outliers_chance' in var_value:
                        if isinstance(var_value['positive_outliers_chance'], (int, float)):
                            if not (0 < var_value['positive_outliers_chance'] < 1):
                                log_warning(" invalid value {var_value['positive_outliers_chance']} in {var_key} for positive_outliers_chance: must be between 0 and 1")
                        else:
                            log_warning(" invalid data type for 'positive_outliers_chance' key; '{type(var_value['positive_outliers_chance'])}' in {var_key}: must be 'int' or 'float' data type")
                    else:
                        log_warning(" missing 'positive_outliers_chance' key in {var_key}: must contain 'positive_outliers_chance' key")



                    # POSITIVE OUTLIERS AMOUNT OF STD DEVS CHECK
                    if 'positive_outliers_amount_of_std_devs' in var_value:
                        if isinstance(var_value['positive_outliers_amount_of_std_devs'], (int, float)):
                            if var_value['positive_outliers_amount_of_std_devs'] <= 0:
                                print (f"[ERROR] invalid value for 'positive_outliers_amount_of_std_devs' key in '{var_key}'; {var_value['positive_outliers_amount_of_std_devs']}: must be greater then '0'")
                        else:
                            log_warning(" invalid data type for 'positive_outliers_amount_of_std_devs' key; '{type(var_value['positive_outliers_amount_of_std_devs'])}' in {var_key}: must be 'int' or 'float' data type")
                    else:
                        log_warning(" missing 'positive_outliers_amount_of_std_devs' key in {var_key}: must contain 'positive_outliers_amount_of_std_devs' key")




                # CATEGORICAL/BINARY CHECKS
                elif var_key_statistical_data_type == 'categorical' or var_key_statistical_data_type == 'binary':

                    # FAIR DISTRIBUTION CHECKS
                    if 'fair_distribution' in var_value:
                        if isinstance(var_value['fair_distribution'], bool):
                            if not var_value['fair_distribution']: # CHECK IF FAIR DISTRIBUTION IS FALSE (IF FALSE, MUST BE TRUE SINCE ALREADY CHECKED THAT DATA TYPE IS BOOL)

                                print("[INFO] Fair Distribution Set OFF")



                                # UNFAIR DISTRIBUTION CHECKS (ONLY IF FAIR DISTRIBUTION CHECKS ARE SET TRUE)
                                if 'unfair_distribution' in var_value:
                                    unfair_distribution_dict = var_value['unfair_distribution'][0] # MAKE IT A VAR SO VARS ARE EASIER TO ACCESS FOR CHECKS


                                    # CATEGORICAL SPECIFIC CHECKS
                                    if var_key_statistical_data_type == 'categorical':


                                        # KEY CHECKS
                                        if len(set(unfair_distribution_dict.keys())) == len(unfair_distribution_dict): # CHECK FOR DUPLICATES
                                            if len(set(unfair_distribution_dict.keys())) == len(expected_data_structure_vars[var_key]['values']): # CHECK FOR SAME NUMBER OF VALUES AS EXPECTED_DATA_STRUCTURE VARS
                                                
                                                # VALUE CHANCE CHECKS
                                                val_chance_sum = 0
                                                for key, val in unfair_distribution_dict.items():
                                                    if key not in expected_data_structure_vars[var_key]['values']:
                                                        log_warning(" missing '{key}' in 'unfair_distribution' key in '{var_key}': must be one of the following expected_data_structure keys; {expected_data_structure_vars[var_key]['values']}")
                                                    if isinstance(val, (int, float)):
                                                        if not (0 <= val <= 1):
                                                            log_warning(" invalid value '{val}' for key '{key}' in {var_key}: must be between 0 and 1")
                                                        val_chance_sum += val
                                                    else:
                                                        log_warning(" invalid data type for '{key}' key in 'unfair_distribution' key in '{var_key}'; '{type(val)}' in {var_key}: must be 'int' or 'float' data type")
                                                if val_chance_sum != 1:
                                                    log_warning(" invalid sum of '{val_chance_sum}' for '{unfair_distribution_dict.keys()}' in '{var_key}': must sum to 1")

                                            else:
                                                log_warning(" invalid count for 'unfair_distribution' key in {var_key}; {len(unfair_distribution_dict)}: must be same count 'expected_data_structure' values; {len(expected_data_structure_vars[var_key]['values'])}")
                                        else:
                                            log_warning(" duplicate values detected '{unfair_distribution_dict.keys}' for '{var_key}' 'values' key")



                                    # BINARY SPECIFIC CHECKS
                                    elif var_key_statistical_data_type == 'binary':
                                        if len(unfair_distribution_dict.keys()) == 2:

                                            # KEY CHECKS
                                            if "true" not in unfair_distribution_dict.keys():
                                                log_warning(" missing 'true' key in 'unfair_distribution' key in '{var_key}': binary statistical_data_type variables must contain a single 'true' key within 'unfair_distribution' key")
                                            if "false" not in unfair_distribution_dict.keys():
                                                log_warning(" missing 'false' key in 'unfair_distribution' key in '{var_key}': binary statistical_data_type variables must contain a single 'false' key within 'unfair_distribution' key")
                                            
                                            # VALUE CHANCE CHECKS
                                            val_chance_sum = 0
                                            for key, val in unfair_distribution_dict.items():
                                                if isinstance(val, (int, float)):
                                                    if not (0 <= val <= 1):
                                                        log_warning(" invalid value '{val}' for key '{key}' in {var_key}: must be between 0 and 1")
                                                    val_chance_sum += val
                                                else:
                                                    log_warning(" invalid data type for '{key}' key in 'unfair_distribution' key in '{var_key}'; '{type(val)}' in {var_key}: must be 'int' or 'float' data type")
                                            if val_chance_sum != 1:
                                                log_warning(" invalid sum of '{val_chance_sum}' for '{unfair_distribution_dict.keys()}' in '{var_key}': must sum to 1")
                                        else:
                                            log_warning(" invalid count for 'unfair_distribution' key in '{var_key}': must be two keys (true/false)")


                                else:
                                    log_warning(" missing 'unfair_distribution' key in {var_key}: must contain 'unfair_distribution' key")
                            else:
                                print("[INFO] Fair Distribution Set ON")
                        else:
                            log_warning(" invalid data type for 'fair_distribution' key; '{type(var_value['positive_outliers_amount_of_std_devs'])}' in {var_key}: must be 'bool' data type (true/false)")
                    else:
                        log_warning(" missing 'fair_distribution' key in {var_key}: must contain 'fair_distribution' key")





                    # MISSING VALUES FILLER CHECK
                    if 'missing_values_filler' in var_value:

                        # BINARY SPECIFIC CHECK
                        if var_key_statistical_data_type == 'binary':
                            if not isinstance(var_value['missing_values_filler'], bool):
                                log_warning(" invalid data type for 'missing_values_filler' key; '{type(var_value['missing_values_filler'])}' in {var_key}: must be 'bool' data type (true/false)")

                        # CATEGORICAL SPECIFIC CHECK
                        else:
                            if not isinstance(var_value['missing_values_filler'], str):
                                print("FDEDDD")
                                log_warning(" invalid data type for 'missing_values_filler' key; '{type(var_value['missing_values_filler'])}' in {var_key}: must be 'str' data type")
                    else:
                        log_warning(" missing 'missing_values_filler' key in {var_key}: must contain 'missing_values_filler' key")





                else:
                    print(f'[MAJOR ERROR] {var_key} invalid statistical data type {var_key_statistical_data_type}')
            else:
                log_warning(" invalid var {var_key}: must be one of the following {expected_data_structure_vars}")
    else:
        print("[INFO] Running Data Generation Set OFF")

    script_end()



if __name__ == "__main__":
    main()
