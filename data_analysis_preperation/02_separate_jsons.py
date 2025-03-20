import os
import json
from utils.seperation_bars import *
from utils.dictionary_manipulation import *
from utils.logging import *

# ===========================
# CONFIGURATION
# ===========================

RAW_DATA_PATH = "data/raw/raw_data.json"
MATCHAPP_DATA_PATH = "data/raw/raw_matchapp_data.json"
SUPERAPP_DATA_PATH = "data/raw/raw_superapp_data.json"

# ===========================
# HELPER FUNCTIONS
# ===========================


# ===========================
# MAIN SCRIPT
# ===========================


def main():
    
    # SCRIPT START
    script_start("[Data Analysis Preperation] 02 - Separate JSONs")
    
    

    # LOAD DATA
    log_header("Load Data")

    log_info(f"Loading 'Raw Data' from '{RAW_DATA_PATH}'")
    raw_data = retrieve_json(RAW_DATA_PATH)
    
    
    # EXTRACT DATA
    log_header("Extract Data")
    
    log_info(f"Extracting 'Matchapp Data' from 'Raw Data'")
    matchapp_data = raw_data["matchApp"]

    log_info(f"Extracting 'Superapp Data' from 'Raw Data'")
    superapp_data = raw_data["superApp"]
    
    
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