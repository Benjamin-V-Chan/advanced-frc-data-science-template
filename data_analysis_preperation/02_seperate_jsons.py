import os
import json
from utils.seperation_bars import seperation_bar, small_seperation_bar
from utils.dictionary_manipulation import retrieve_json
from utils.logging import log_message

# ===========================
# CONFIGURATION
# ===========================

RAW_DATA_PATH = "data/raw/raw_data.json"
MATCHAPPS_DATA_PATH = "data/raw/raw_matchapps_data.json"
SUPERAPPS_DATA_PATH = "data/raw/raw_superapps_data.json"


# ===========================
# HELPER FUNCTIONS
# ===========================


# ===========================
# MAIN SCRIPT
# ===========================

def main():    

    raw_data = retrieve_json(RAW_DATA_PATH)
    
    matchapps_data = raw_data["matchapps"]
    superapps_data = raw_data["superapps"]

if __name__ == "__main__":
    main()