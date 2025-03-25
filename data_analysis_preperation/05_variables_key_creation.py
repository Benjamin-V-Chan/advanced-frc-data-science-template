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
EXPECTED_DATA_STRUCTURE = "config/expected_data_structure.json"

# ===========================
# HELPER FUNCTIONS
# ===========================


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
    
    
    
    # Add Variables Section
    
    matchapp_output = []
    superapp_output = []
    
    for matchapp in matchapp_data: # Assumes data has been ROBUSTLY cleaned
        
        output_dict = {
            "metadata": {matchapp_data['metadata']},
            "variables": {}
            }
        
        for key, val in matchapp_data.items():
            if key != "metdata":
                output_dict[key] = val
        
        matchapp_output.append(output_dict)
    
    
    # SAVE DATA
    log_header("Save Data")
    
    log_info(f"Saving 'Matchapp Data' to '{MATCHAPP_DATA_PATH}'")
    save_json(MATCHAPP_DATA_PATH, matchapp_data)
    
    log_info(f"Saving 'Superapp Data' to '{SUPERAPP_DATA_PATH}'")
    save_json(SUPERAPP_DATA_PATH, superapp_data)
    
    
    
    # SCRIPT END
    script_end("[Data Analysis Preperation] 02 - Separate JSONs")

if __name__ == "__main__":
    main()