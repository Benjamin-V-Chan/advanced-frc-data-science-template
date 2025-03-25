from utils.seperation_bars import *
from utils.dictionary_manipulation import *
from utils.logging import *

# ===========================
# CONFIGURATION
# ===========================

FORMATTED_MATCHAPP_DATA_PATH = "data/processed/formatted_matchapp_data.json"
FORMATTED_SUPERAPP_DATA_PATH = "data/processed/formatted_superapp_data.json"
CONDENSED_DATA_PATH = "data/processed/formatted_data.json"
EXPECTED_DATA_STRUCTURE = "config/expected_data_structure.json"
BAD_ENTRIES = "outputs/errors/condense_datasets_errors.txt"

# ===========================
# HELPER FUNCTIONS
# ===========================


# ===========================
# MAIN SCRIPT
# ===========================


def main():
    
    # SCRIPT START
    script_start("[Data Analysis Preperation] 06 - Condense Datasets")
    
    
    # LOAD DATA
    log_header("Load Data")
    
    log_info(f"Extracting 'Matchapp Data' from '{FORMATTED_MATCHAPP_DATA_PATH}'")
    matchapp_data = retrieve_json(FORMATTED_MATCHAPP_DATA_PATH)

    log_info(f"Extracting 'Superapp Data' from '{FORMATTED_SUPERAPP_DATA_PATH}'")
    superapp_data = retrieve_json(FORMATTED_SUPERAPP_DATA_PATH)
    
    
    # Cross-check Data
    output_data = []
    
    for matchapp in matchapp_data:
        # match to superapp data
        # when found... add to output data
        # if none found, log entry
        pass
    
    
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