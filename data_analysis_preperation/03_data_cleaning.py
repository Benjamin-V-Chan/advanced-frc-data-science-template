# CLEAN MATCHAPP AND SUPERAPP RAW DATA SEPERATLEY.

from utils.dictionary_manipulation import *
from utils.logging import *

# ===========================
# CONFIGURATION
# ===========================

RAW_MATCHAPP_DATA_PATH = "data/raw/raw_matchapp_data.json"
RAW_SUPERAPP_DATA_PATH = "data/raw/raw_superapp_data.json"
CLEANED_MATCHAPP_DATA_PATH = "data/cleaned/initial_cleaned_matchapp_data.json"
CLEANED_SUPERAPP_DATA_PATH = "data/cleaned/initial_cleaned_superapp_data.json"
EXPECTED_DATA_STRUCTURE = "config/expected_data_structure.json"

# ===========================
# HELPER FUNCTIONS
# ===========================


# ===========================
# MAIN SCRIPT
# ===========================


def main():
    
    # SCRIPT START
    script_start("[Data Analysis Preperation] 03 - Data Cleaning")
    
    
    
    # LOAD DATA
    log_header("Load Data")
    
    log_info(f"Loading 'Raw Matchapp Data' from '{RAW_MATCHAPP_DATA_PATH}'")
    raw_matchapp_data = retrieve_json(RAW_MATCHAPP_DATA_PATH)
    
    log_info(f"Loading 'Raw Matchapp Data' from '{RAW_MATCHAPP_DATA_PATH}'")
    raw_superapp_data = retrieve_json(RAW_SUPERAPP_DATA_PATH)
    
    
    
    # DATA CLEANING
    log_header("Data Cleaning")
    
    
    
    # SAVE DATA
    log_header("Save Data")
    
    log_info(f"Saving 'Cleaned Matchapp Data' to '{CLEANED_MATCHAPP_DATA_PATH}'")
    save_json(CLEANED_MATCHAPP_DATA_PATH, cleaned_matchapp_data)
    
    log_info(f"Saving 'Cleaned Superapp Data' to '{CLEANED_SUPERAPP_DATA_PATH}'")
    save_json(CLEANED_SUPERAPP_DATA_PATH, cleaned_superapp_data)
    
    
    # SCRIPT END
    script_end("[Data Analysis Preperation] 03 - Data Cleaning")

if __name__ == "__main__":
    main()