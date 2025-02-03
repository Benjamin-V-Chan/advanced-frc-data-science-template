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
print("Script 02: Data Structure Validation\n")

# Retrieve JSON Data
small_seperation_bar("RETRIEVE JSON DATA")

# Retrieve Expected Data Structure JSON as Dict
expected_data_structure = retrieve_json(expected_data_structure_path)
print("\nExpected Data Structure JSON:")
print(json.dumps(expected_data_structure, indent=4))

# Retrieve Data Generation Configuration JSON as Dict
data_generation_config = retrieve_json(data_generation_config_path)
print("\nData Generation Configuration JSON:")
print(json.dumps(data_generation_config, indent=4))


# EXPECTED DATA STRUCTURE
small_seperation_bar("EXPECTED DATA STRUCTURE JSON VALIDATION")

# EXPECTED DATA STRUCTURE METADATA CHECKS
if 'metadata' in expected_data_structure:

    expected_data_structure_metadata = expected_data_structure['metadata']

    if 'scouterName' in expected_data_structure_metadata:
        if expected_data_structure_metadata['scouterName'] != 'str':
            print(f"[ERROR] invalid value '{expected_data_structure_metadata['scouterName']}' for set data type: must be 'str'")
    else:
        print(f"[ERROR] missing 'scouterName' key in 'metadata' key: must contain 'scouterName' key")

    if 'matchNumber' in expected_data_structure_metadata:
        if expected_data_structure_metadata['matchNumber'] != 'int':
            print(f"[ERROR] invalid value '{expected_data_structure_metadata['matchNumber']}' for set data type: must be 'int'")
    else:
        print(f"[ERROR] missing 'matchNumber' key in 'metadata' key: must contain 'matchNumber' key")

    if 'robotTeam' in expected_data_structure_metadata:
        if expected_data_structure_metadata['robotTeam'] != 'int':
            print(f"[ERROR] invalid value '{expected_data_structure_metadata['robotTeam']}' for set data type: must be 'int'")
    else:
        print(f"[ERROR] missing 'robotTeam' key in 'metadata' key: must contain 'robotTeam' key")

    if 'robotPosition' in expected_data_structure_metadata:
        if 'values' in expected_data_structure_metadata['robotPosition']:
            if len(expected_data_structure_metadata['robotPosition']['values']) == 6:
                for val in expected_data_structure_metadata['robotPosition']['values']:
                    if isinstance(val, str):
                        if val not in valid_robot_positions:
                            print(f"[ERROR] invalid value '{val}' in 'values' key in 'robotPosition' key in 'metadata': must be one of the following valid robot positions: {valid_robot_positions}")
                    else:
                        print(f"[ERROR] invalid data type '{type(val)}' for value in 'values' key in 'robotPosition' key in 'metadata': must be 'str'")
    else:
        print(f"[ERROR] missing 'robotPosition' key in 'metadata' key: must contain 'robotPosition' key")
        
else:
    print()

# Retrieve Expected Data Structure Variables
expected_data_structure_vars = flatten_vars_in_dict(expected_data_structure["variables"], return_dict={})

# Keys checks for expected data structure var keys
list_of_expected_data_structure_var_keys = []

for key in expected_data_structure_vars:
    if type(key) != str:
        print(f"[ERROR] {key} invalid var key data type: must be 'str'")
    list_of_expected_data_structure_var_keys.append(key)

if set(list_of_expected_data_structure_var_keys) != list_of_expected_data_structure_var_keys:
    print(f"[ERROR] invalid variable keys '{list_of_expected_data_structure_var_keys}': must contain no repeat variable keys")

# Specific expected data structure var keys checks
for var_key, var_value in expected_data_structure_vars.items():

    if 'statistical_data_type' in var_value:

        if var_value['statistical_data_type'] in statistical_data_type_options:

            # Categorical Variable Property Checks (due to extra 'values' property)
            if var_value['statistical_data_type'] == 'categorical':
                if 'values' in var_value:
                    if type(var_value['values']) == list:
                        var_values_count = len(var_value['values'])
                        if var_values_count <= 1:
                            print(f"[ERROR] categorical variable {var_key} has invalid count '{len(var_value['values'])}' for 'values' property: must be >= 1")
                        if set(var_value['values']) != var_values_count:
                            print(f"[ERROR] categorical variable {var_key} has invalid values '{var_value['values']}' for 'values' property: must contain no repeat values")
                        if (True in var_value['values'] or False in var_value['values']) and var_values_count == 2:
                            print(f"[ERROR] categorical variable {var_key} contains invalid data type 'binary' for 'values' property: must set statistical data type to 'binary' if true or false is being used")
                    else:
                        print(f"[ERROR] categorical variable {var_key} has invalid data type '{type(var_value['values'])}' for 'values' property: must be 'list' data type")
                else:
                    print(f"[ERROR] categorical variable {var_key} has no 'values' property: vars with categorical statistical data type must have 'values' property")
        else:
            print(f"[ERROR] {var_key} has invalid value '{var_value['statistical_data_type']}' for 'statistical_data_type' property: must be one of the following; {statistical_data_type_options}")

    else:
        print(f"[ERROR] {var_key} has no 'statistical_data_type' property")


# DATA GENERARTION CONFIG CHECKS

small_seperation_bar("DATA GENERATION CONFIG JSON VALIDATION")

if data_generation_config['running_data_generation']:

    print(f"[INFO] Running Data Generation Set ON")

    if 'data_quantity' in data_generation_config: # DATA QUANTITY CHECKS

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

    # VARIABLE CHECKS

    # Retrieve Data Generation Config Variables
    data_generation_config_vars = flatten_vars_in_dict(data_generation_config['variables'], return_dict={})
    
    # Keys checks for data generation config var keys

    list_of_data_generation_config_var_keys = []

    list_of_data_generation_config_var_keys = data_generation_config_vars.keys()

    for key in list_of_data_generation_config_var_keys:
        if type(key) != str:
            print(f"[ERROR] {key} invalid var key data type: must be 'str'")
        
    if set(list_of_data_generation_config_var_keys) != list_of_data_generation_config_var_keys:
        print(f"[ERROR] invalid variable keys '{list_of_data_generation_config_var_keys}': must contain no repeat variable keys")

    for var_key, var_value in list_of_data_generation_config_var_keys:
        print(f"{var_key}: {var_value}")

        if var_key in expected_data_structure_vars:
            var_key_statistical_data_type = expected_data_structure_vars[var_key]['statistical_data_type']

            
            if 'missing_values_chance' in var_value: # MISSING VALUES CHANCE CHECK (ALL STATISTICAL DATA TYPES REQUIRE IT)
                if isinstance(var_value['missing_values_chance'], int):
                    if not (0 < var_value['missing_values_chance'] < 1):
                        print(f"[ERROR] invalid value {var_value['missing_values_chance']} in {var_key} for missing_values_chance: must be between 0 and 1")
                else:
                    print(f"[ERROR invalid data type for 'missing_values_chance' key; '{type(var_value['missing_values_chance'])}' in {var_key}: must be 'int' data type")
            else:
                print(f"[ERROR] missing 'missing_values_chance' key in {var_key}: must contain 'missing_values_chance' key")


            if var_key_statistical_data_type == 'quantitative': # QUANTITATIVE CHECKS

                if 'data_deviation' in var_value: # DATA DEVIATION CHECKS

                    if 'mean' in var_value['data_deviation']: # MEAN CHECK
                        if not isinstance(var_value['data_deviation'][0]['mean'], int): # [0] because we are initializing structure as a list to avoide single dict check
                            print(f"[ERROR] invalid data type for 'mean' key; '{type(var_value['data_deviation']['mean'])}' in {var_key}: must be 'int' data type")
                    else:
                        print(f"[ERROR] missing 'mean' key in {var_key} data deviation section")

                    if 'standard_deviation' in var_value['data_deviation']: # STANDARD DEV CHECK
                        if not isinstance(var_value['data_deviation'][0]['standard_deviation'], int): # [0] because we are initializing structure as a list to avoide single dict check
                            print(f"[ERROR] invalid data type for 'standard_deviation' key; '{type(var_value['standard_deviation']['mean'])}' in {var_key}: must be 'int' data type")
                    else:
                        print(f"[ERROR] missing 'standard_deviation' key in {var_key} data deviation section")
            
                else:
                    print(f"[ERROR] missing 'data_deviation' key in {var_key}: most contain 'data_deviation'")

                if 'missing_values_filler' in var_value: # MISSING VALUES FILLER CHECK (SPECIFIC TO QUANTITATIVE SINCE REQUIRES INT DATA TYPE)
                    if not isinstance(var_value['missing_values_filler'], int):
                        print(f"[ERROR] invalid data type for 'missing_values_filler' key; '{type(var_value['missing_values_filler'])}' in {var_key}: must be 'int' data type")
                else:
                    print(f"[ERROR] missing 'missing_values_filler' key in {var_key}: must contain 'missing_values_filler' key")

                if 'positive_outliers_chance' in var_value: # POSITIVE OUTLIERS CHANCE CHECK
                    if isinstance(var_value['positive_outliers_chance'], int):
                        if not (0 < var_value['positive_outliers_chance'] < 1):
                            print(f"[ERROR] invalid value {var_value['positive_outliers_chance']} in {var_key} for positive_outliers_chance: must be between 0 and 1")
                    else:
                        print(f"[ERROR] invalid data type for 'positive_outliers_chance' key; '{type(var_value['positive_outliers_chance'])}' in {var_key}: must be 'int' data type")
                else:
                    print(f"[ERROR] missing 'positive_outliers_chance' key in {var_key}: must contain 'positive_outliers_chance' key")

                if 'positive_outliers_amount_of_std_devs' in var_value: # POSITIVE OUTLIERS AMOUNT OF STD DEVS CHECK
                    if isinstance(var_value['positive_outliers_amount_of_std_devs'], int):
                        if var_value['positive_outliers_amount_of_std_devs'] <= 0:
                            print (f"[ERROR] invalid value for 'positive_outliers_amount_of_std_devs' key in '{var_key}'; {var_value['positive_outliers_amount_of_std_devs']}: must be greater then '0'")
                    else:
                        print(f"[ERROR] invalid data type for 'positive_outliers_amount_of_std_devs' key; '{type(var_value['positive_outliers_amount_of_std_devs'])}' in {var_key}: must be 'int' data type")
                else:
                    print(f"[ERROR] missing 'positive_outliers_amount_of_std_devs' key in {var_key}: must contain 'positive_outliers_amount_of_std_devs' key")


            elif var_key_statistical_data_type == 'categorical' or var_key_statistical_data_type == 'binary': # CATEGORICAL CHECKS

                if 'fair_distribution' in var_value: # FAIR DISTRIBUTION CHECKS
                    if isinstance(var_value['fair_distribution'], bool):
                        if var_value['fair_distribution']: # CHECK IF TRUE (IF INCORRECT, MUST BE FALSE SINCE ALREADY CHECKED THAT DATA TYPE IS BOOL)
                            print(f"[INFO] Fair Distribution Set ON")
                            if 'unfair_distribution' in var_value: # UNFAIR DISTRIBUTION CHECKS (ONLY IF FAIR DISTRIBUTION CHECKS ARE SET TRUE)
                                unfair_distribution_dict = var_value['unfair_distribution'][0] # MAKE IT A VAR SO VARS ARE EASIER TO ACCESS FOR CHECKS
                                if len(set(unfair_distribution_dict.keys())) == len(unfair_distribution_dict): # CHECK FOR DUPLICATES
                                    if len(set(unfair_distribution_dict.keys())) == len(expected_data_structure_vars[var_key]['values']): # CHECK FOR SAME NUMBER OF VALUES AS EXPECTED_DATA_STRUCTURE VARS
                                        temp_sum = 0
                                        for key, val in unfair_distribution_dict.items():
                                            if key not in expected_data_structure_vars[var_key]['values']:
                                                print(f"[ERROR] missing '{key}' in 'unfair_distribution' key in '{var_key}': must be one of the following expected_data_structure keys; {list_of_expected_data_structure_var_keys}")
                                            if isinstance(val, int):
                                                if not (0 <= val <= 1):
                                                    print(f"[ERROR] invalid value '{val}' for key '{key}' in {var_key}: must be between 0 and 1")
                                                temp_sum += val
                                            else:
                                                print(f"[ERROR] invalid data type for '{key}' key in 'unfair_distribution' key in '{var_key}'; '{type(val)}' in {var_key}: must be 'int' data type")
                                        if temp_sum != 1:
                                            print(f"[ERROR] invalid sum for {unfair_distribution_dict.keys()} in {var_key}: must sum to 1")
                                    else:
                                        print(f"[ERROR] invalid count for 'unfair_distribution' key in {var_key}; {len(unfair_distribution_dict)}: must be same count 'expected_data_structure' values; {len(expected_data_structure_vars[var_key]['values'])}")
                                else:
                                    print(f"[ERROR] duplicate values detected '{unfair_distribution_dict.keys}' for '{var_key}' 'values' key")
                            else:
                                print(f"[ERROR] missing 'unfair_distribution' key in {var_key}: must contain 'unfair_distribution' key")
                    else:
                        print(f"[ERROR] invalid data type for 'fair_distribution' key; '{type(var_value['positive_outliers_amount_of_std_devs'])}' in {var_key}: must be 'bool' data type (true/false)")
                else:
                    print(f"[ERROR] missing 'fair_distribution' key in {var_key}: must contain 'fair_distribution' key")

                if 'missing_values_filler' in var_value: # MISSING VALUES FILLER CHECK (SPECIFIC TO QUANTITATIVE SINCE REQUIRES INT DATA TYPE)
                    if not isinstance(var_value['missing_values_filler'], bool):
                        print(f"[ERROR] invalid data type for 'missing_values_filler' key; '{type(var_value['missing_values_filler'])}' in {var_key}: must be 'bool' data type (true/false)")
                else:
                    print(f"[ERROR] missing 'missing_values_filler' key in {var_key}: must contain 'missing_values_filler' key")

            else:
                print(f'[MAJOR ERROR] {var_key} invalid statistical data type {var_key_statistical_data_type}')


        else:
            print(f"[ERROR] invalid var {var_key}: must be one of the following {expected_data_structure_vars}")

else:
    print(f"[INFO] not running data generation")



# END OF SCRIPT

seperation_bar()