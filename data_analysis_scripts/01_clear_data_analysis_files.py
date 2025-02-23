from utils.seperation_bars import *
import os
import shutil

# ===========================
# CONFIGURATION SECTION
# ===========================

# Root directories (Modify these as needed)
OUTPUTS_DIR = "outputs"  # Directory for results, visualizations, and statistics
DATA_DIR = "data"        # Directory for raw and processed scouting data

# Folder handling options (Modify based on your team's needs)
# Specify folders to leave untouched or to preserve their structure while clearing contents.
OUTPUTS_UNTOUCHED_FOLDERS = []  # Leave these folders untouched
OUTPUTS_PRESERVED_FOLDERS = ["visualizations", "statistics", "team_data"]  # Clear contents but preserve these folders
DATA_UNTOUCHED_FOLDERS = ["raw"]  # Keep raw data untouched
DATA_PRESERVED_FOLDERS = ["processed"]  # Clear contents but preserve processed data folder structure

# ===========================
# HELPER FUNCTIONS SECTION
# ===========================

def ensure_folder_exists(folder_path):
    """
    Ensures that a folder exists. If it doesn't, it is created.

    :param folder_path: Path to the folder to ensure existence.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
        print(f"[INFO] Created missing folder: {folder_path}")
    else:
        print(f"[INFO] Folder exists: {folder_path}")


def clear_folder_with_exceptions(folder_path, untouched_folders=None, preserved_folders=None):
    """
    Clears all contents of a folder while keeping specific subfolders untouched or preserved.

    :param folder_path: The root folder to clear.
    :param untouched_folders: Subfolders to leave completely untouched (including their contents).
    :param preserved_folders: Subfolders to preserve but clear their contents.
    """
    # Ensure the root folder exists
    ensure_folder_exists(folder_path)

    # Default to empty lists if None
    if untouched_folders is None:
        untouched_folders = []
    if preserved_folders is None:
        preserved_folders = []

    # Ensure all folders in untouched_folders and preserved_folders exist
    for subfolder in untouched_folders + preserved_folders:
        subfolder_path = os.path.join(folder_path, subfolder)
        ensure_folder_exists(subfolder_path)

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        if item in untouched_folders:
            # Skip untouched folders entirely
            print(f"[INFO] Untouched folder: {item_path}")
            continue

        if item in preserved_folders:
            # Clear contents of preserved folders
            print(f"[INFO] Clearing preserved folder: {item_path}")
            for sub_item in os.listdir(item_path):
                sub_item_path = os.path.join(item_path, sub_item)
                try:
                    if os.path.isfile(sub_item_path) or os.path.islink(sub_item_path):
                        os.unlink(sub_item_path)
                        print(f"[INFO] Deleted file: {sub_item_path}")
                    elif os.path.isdir(sub_item_path):
                        shutil.rmtree(sub_item_path)
                        print(f"[INFO] Deleted folder: {sub_item_path}")
                except Exception as e:
                    print(f"[ERROR] Failed to clear {sub_item_path}. Reason: {e}")
            continue

        # Delete everything else
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
                print(f"[INFO] Deleted file: {item_path}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"[INFO] Deleted folder: {item_path}")
        except Exception as e:
            print(f"[ERROR] Failed to delete {item_path}. Reason: {e}")


# ===========================
# MAIN SCRIPT SECTION
# ===========================

seperation_bar()
print("Script 01: Clear Data Analysis Files\n")

try:
    # Guidance for FRC teams:
    # - `OUTPUTS_DIR` stores analysis results. Modify untouched/preserved folders above to suit your needs.
    # - `DATA_DIR` stores your team's scouting data. Ensure raw data is in `data/raw`.

    # Ensure root folders exist
    ensure_folder_exists(OUTPUTS_DIR)
    ensure_folder_exists(DATA_DIR)

    # Clear outputs folder
    clear_folder_with_exceptions(
        OUTPUTS_DIR,
        untouched_folders=OUTPUTS_UNTOUCHED_FOLDERS,
        preserved_folders=OUTPUTS_PRESERVED_FOLDERS
    )

    # Clear data folder
    clear_folder_with_exceptions(
        DATA_DIR,
        untouched_folders=DATA_UNTOUCHED_FOLDERS,
        preserved_folders=DATA_PRESERVED_FOLDERS
    )

    print("\n[INFO] Script 01: Completed.")

except Exception as e:
    print(f"\n[ERROR] An error occurred: {e}")
    print("\nScript 01: Failed.")

seperation_bar()