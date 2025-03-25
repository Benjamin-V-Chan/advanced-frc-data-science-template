from utils.seperation_bars import *
from utils.dictionary_manipulation import *
from utils.logging import *

# ===========================
# CONFIGURATION
# ===========================

FULL_CLEANED_MATCHAPP_DATA_PATH = "data/cleaned/full_cleaned_matchapp_data.json"
FULL_CLEANED_SUPERAPP_DATA_PATH = "data/cleaned/full_cleaned_superapp_data.json"
FORMATTED_MATCHAPP_DATA_PATH = "data/processed/formatted_matchapp_data.json"
FORMATTED_SUPERAPP_DATA_PATH = "data/processed/formatted_superapp_data.json"

# ===========================
# HELPER FUNCTIONS
# ===========================

def reformat_dict_list_for_variable_keys(dict_list):
    """"Inputs a list of dictionaries. Outputs list of dictionaries with each dictionary contaning grouped variables under a single variable key in dict"""
    output_dict_list = []
    
    for dict in dict_list:
        output_dict_list.append(create_variables_key(dict))
        
    return output_dict_list

def create_variables_key(dict):
    """Inputs a dictionary. Output the dictionary with non-metadata variables grouped into a single key within the dict"""
    output_dict = {
        "metadata": {dict['metadata']},
        "variables": {}
        }
    
    for key, val in dict.items():
        if key != "metdata":
            output_dict[key] = val
    
    return output_dict

# ===========================
# MAIN SCRIPT
# ===========================


def main():
    
    # SCRIPT START
    script_start("[Data Analysis Preperation] 05 - Variables Key Creation")
    
    

    # Load DATA
    log_header("Load Data")
    
    log_info(f"Loading 'Matchapp Data' from '{FULL_CLEANED_MATCHAPP_DATA_PATH}'")
    matchapp_data = retrieve_json(FULL_CLEANED_MATCHAPP_DATA_PATH)

    log_info(f"Loading 'Superapp Data' from '{FULL_CLEANED_SUPERAPP_DATA_PATH}'")
    superapp_data = retrieve_json(FULL_CLEANED_SUPERAPP_DATA_PATH)
    
    
    
    # Create Variables Key
    
    matchapp_output = reformat_dict_list_for_variable_keys(matchapp_data)
    superapp_output = reformat_dict_list_for_variable_keys(superapp_data)
    
    
    
    
    # SAVE DATA
    log_header("Save Data")
    
    log_info(f"Saving 'Formatted Matchapp Data' to '{FORMATTED_MATCHAPP_DATA_PATH}'")
    save_json(FORMATTED_MATCHAPP_DATA_PATH, matchapp_output)
    
    log_info(f"Saving 'Formatted Superapp Data' to '{FORMATTED_SUPERAPP_DATA_PATH}'")
    save_json(FORMATTED_SUPERAPP_DATA_PATH, superapp_output)
    
    
    
    # SCRIPT END
    script_end("[Data Analysis Preperation] 05 - Variables Key Creation")

if __name__ == "__main__":
    main()