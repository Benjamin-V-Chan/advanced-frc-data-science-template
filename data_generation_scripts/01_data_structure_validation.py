import json
from utility_functions.print_formats import seperation_bar, small_seperation_bar

# ===========================
# CONFIGURATION SECTION
# ===========================

data_generation_config_path = 'data_generation_config.json'
expected_data_structure_path = 'expected_data_structure.json'

# ===========================
# CONSTANTS SECTION
# ===========================

statistical_data_type_options = ['quantitative', 'categorical', 'binary']

# ===========================
# HELPER FUNCTIONS SECTION
# ===========================

def single_dict(dictionary):
    if not isinstance(dictionary, dict):
        return False
    for key in dictionary:
        if isinstance(dictionary[key], dict):
            return False
    return True

def flatten_vars_in_dict(dictionary, return_dict=None, prefix=""):
    if return_dict is None:
        return_dict = {}
    
    for key in dictionary:
        full_key = f"{prefix}.{key}" if prefix else key
        if single_dict(dictionary[key]):
            # print(f"single_key added: {full_key}: {dictionary[key]}")
            return_dict[full_key] = dictionary[key]
        else:
            flatten_vars_in_dict(dictionary[key], return_dict, full_key)
    
    return return_dict

def retrieve_json(json_path):
    with open(json_path) as json_file:
        return json.load(json_file)

# ===========================
# MAIN SCRIPT SECTION
# ===========================
seperation_bar()
print("Script 01: Data Structure Validation\n")

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

# TODO: Restructure and better organize below error logging code for expected data structure variable property checking D:

small_seperation_bar("EXPECTED DATA STRUCTURE JSON VALIDATION")

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

# DATA GENERATION CONFIGURATION SETTINGS CHECKS

# TODO: Data Generation Config checks (BELOW)

if data_generation_config['running_data_generation']:
    # Ensure each section of of five sections of JSON is there
    # Create a list similar to the list of the expected data structure variables but in this case for variables in the data generation config
    # Use the set method to check for any repeats or incorrect NUMBER of variables between the expected data structure variables list AND the data generation config list
    # Ensure data quantitiy section format is correct
        # Properties exist and are of correct data type
    # Iterate through each type of statistical data type and check for:
        # All variables have a SINGLE match to the expected data structure AND they are both the same statistical data type
            # Iterate through each key name in the gen config list
                # Use the 'in' keyword to search for if the gen config key name is in the expected_data_structure list
                # If not, log an error
                # Error format will be refrencing the data_gen_config variable and saying how it is missing from the expected data structure congfig
                # If yes, then further nest and compare the statistical data type (may need to restructure gen_config JSON to make the variable format the same as the expected_data_structure format to help with easier and more efficient searching)
                # For categorical statistical data type:
                    # Same number and names of all the values between both lists
    # Broader stuff to look for:
        # Variable properties exist and are of correct data type
        # Ensure all unfair distributions add up to 1.0
        # Ensure all chance properties (ie; outliers, missing values, etc.) are between 0 and 1
        # Ensure no repeats between missing values filler and categorical values options
        # Ensure positive outliers std dev amount is positive (since positive outliers mean it will be ~N std devs (relative to the mean and the previously stated std devs amount for that specific variable) above the initially natural random value)

    # NOTE: Probably some more edge cases yet to be discovered, but these are core ones for now
    pass

# END OF SCRIPT

print()
print(expected_data_structure_vars)

seperation_bar()