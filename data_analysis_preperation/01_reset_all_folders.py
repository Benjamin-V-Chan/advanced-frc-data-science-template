import os
import json
import shutil
from utils.dictionary_manipulation import *
from utils.logging import *

# ===========================
# CONFIGURATION
# ===========================

FOLDER_CONFIG = {
    "data": {
        "cleaned": {},
        "processed": {},  
        "raw": {
            "raw_data.json": None
        }
    },
    "outputs": {
        "statistics": {},
        "team_data": {},
        "visualizations": {},
        "scouter_leaderboard": {},
        "errors": {}
    },
    "config": {
        "data_generation_config_default_values_config.json": None,
        "expected_data_structure.json": None
    }
}
BASE_PATH = "."

# ===========================
# HELPER FUNCTIONS
# ===========================


def reset_folders(config, base_path="."):
    """
    Resets the directory structure based on the provided config dictionary.
    Deletes all files and subdirectories except for specified files and folders.

    Parameters:
        config (dict): Dictionary defining folder structure and files/folders to keep.
        base_path (str): Base directory for the operation.
    """
    for folder, content in config.items():
        folder_path = os.path.join(base_path, folder)

        if isinstance(content, dict):  # It's a folder
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)  # Create missing folders
            else:
                keep_files, keep_folders = extract_keep_items(content)

                log_info(f"Processing Folder: {folder_path}")
                log_info(f"Keeping Files: {keep_files}")
                log_info(f"Keeping Folders: {keep_folders}")

                # Process files FIRST before clearing folder
                clear_folder(folder_path, keep_files, keep_folders)

            # Recursively process subdirectories AFTER preserving files
            reset_folders(content, folder_path)
        elif content is None:  # It's a file
            os.makedirs(os.path.dirname(folder_path), exist_ok=True)


def extract_keep_items(content):
    """Extracts files and folders that should be preserved."""
    keep_files = set()
    keep_folders = set()

    for key, value in content.items():
        if value is None:  # If value is None, it means it's a file
            keep_files.add(key)
        else:  # Otherwise, it's a folder
            keep_folders.add(key)

    return keep_files, keep_folders


def clear_folder(folder_path, keep_files, keep_folders):
    """Clears all files and subdirectories in a folder except specified items."""
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        log_info(f"Checking: {item_path} (is file: {os.path.isfile(item_path)}, is dir: {os.path.isdir(item_path)})")

        if item in keep_files or item in keep_folders:
            log_info(f"Skipping: {item}")
            continue

        if os.path.isfile(item_path):
            log_info(f"Deleting file: {item_path}")
            os.remove(item_path)
        elif os.path.isdir(item_path):
            log_info(f"Deleting folder: {item_path}")
            shutil.rmtree(item_path)


# ===========================
# MAIN SCRIPT
# ===========================

def main():
    
    # SCRIPT START
    script_start("[Data Analysis Preperation] 01 - Reset all Folders")
    
    
    
    # CONFIG LOGGING VALIDATION
    log_header("Config Logging Validation")
    
    log_info(f"Config being used: \n{json.dumps(FOLDER_CONFIG, indent=4)}\n")
    
    
    
    # RESET FOLDERS
    log_header("Reset Folders")
    
    reset_folders(FOLDER_CONFIG)
    
    

    # SCRIPT END 
    script_end("[Data Analysis Preperation] 01 - Reset all Folders")

if __name__ == "__main__":
    main()