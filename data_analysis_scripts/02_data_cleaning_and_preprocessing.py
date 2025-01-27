from utils import seperation_bar, small_seperation_bar
import os
import json
import traceback
from collections import defaultdict

# ===========================
# CONFIGURATION SECTION
# ===========================

# File Paths (Update These)
RAW_MATCH_DATA_PATH = "data/raw/raw_match_data.json"  # Input raw match data
CLEANED_MATCH_DATA_PATH = "data/processed/cleaned_match_data.json"  # Output cleaned match data
SCOUTER_LEADERBOARD_PATH = "outputs/statistics/scouter_leaderboard.txt"  # Output scouter leaderboard

# Expected JSON Structure
# IMPORTANT: Update this dictionary to reflect the expected structure of your raw JSON data.
EXPECTED_STRUCTURE = {
    "metadata": {
        "scouterName": str,  # Name of the scouter
        "matchNumber": int,  # Match number
        "robotTeam": int,    # Team number
        "robotPosition": str  # Robot position (e.g., red_1, blue_2)
    },
    "var1": int,  # Replace with your team's custom variable
    "var2": str,  # Replace with your team's custom variable
    "var3": bool  # Replace with your team's custom variable
}

# Valid Robot Positions (Update if different)
VALID_ROBOT_POSITIONS = {"red_1", "red_2", "red_3", "blue_1", "blue_2", "blue_3"}

# ===========================
# HELPER FUNCTIONS SECTION
# ===========================

warnings = []
scouter_warnings = defaultdict(int)
scouter_participation = defaultdict(int)
team_match_counts = defaultdict(int)
match_robot_positions = defaultdict(set)


def log_warning(message, scouter=None):
    """
    Logs a warning and associates it with the scouter.

    :param message: The warning message to log.
    :param scouter: The scouter responsible for the data.
    """
    global warnings, scouter_warnings
    warnings.append(message)
    if scouter:
        scouter_warnings[scouter] += 1


def validate_structure(data, expected_structure, scouter, path=""):
    """
    Validates and fixes a nested structure.

    :param data: The input data to validate.
    :param expected_structure: The expected structure.
    :param scouter: The scouter responsible for the data.
    :param path: The path to the current key for logging purposes.
    :return: A validated and cleaned version of the data.
    """
    validated = {}
    for key, expected_type in expected_structure.items():
        full_key_path = f"{path}.{key}" if path else key

        if key not in data:
            log_warning(f"[WARNING] Missing key '{full_key_path}'.", scouter)
            continue

        if isinstance(expected_type, dict):
            validated[key] = validate_structure(data[key], expected_type, scouter, full_key_path)
        else:
            value = data[key]
            if not isinstance(value, expected_type):
                log_warning(
                    f"[WARNING] Incorrect type for '{full_key_path}'. Expected {expected_type}, got {type(value)}.",
                    scouter,
                )
            else:
                # Handle specific cases (robotPosition, negative integers)
                if key == "robotPosition" and value not in VALID_ROBOT_POSITIONS:
                    log_warning(
                        f"[WARNING] Invalid robot position '{value}' at '{full_key_path}'. Defaulting to 'unknown'.",
                        scouter,
                    )
                    value = "unknown"

                if isinstance(value, int) and value < 0:
                    log_warning(
                        f"[WARNING] Negative value '{value}' at '{full_key_path}'. Defaulting to 0.",
                        scouter,
                    )
                    value = 0

                validated[key] = value

    # Remove extra keys
    extra_keys = set(data.keys()) - set(expected_structure.keys())
    for extra_key in extra_keys:
        log_warning(f"[WARNING] Extra key '{path}.{extra_key}' found and removed.", scouter)

    return validated


def validate_and_clean_entry(entry):
    """
    Validates and cleans a single entry, ensuring it adheres to the correct structure and rules.

    :param entry: The raw data entry.
    :return: A cleaned entry.
    """
    scouter = entry.get("metadata", {}).get("scouterName", "Unknown")
    scouter_participation[scouter] += 1
    return validate_structure(entry, EXPECTED_STRUCTURE, scouter)


def analyze_data_consistency():
    """
    Analyzes data consistency for matches and robot teams.
    """
    global warnings

    # Check team match counts
    match_count_groups = defaultdict(list)
    for team, count in team_match_counts.items():
        match_count_groups[count].append(team)

    if len(match_count_groups) > 1:
        log_warning(
            "[WARNING] Inconsistent match counts detected:\n"
            + "\n".join(
                f"  Teams with {count} matches: {teams}"
                for count, teams in match_count_groups.items()
            )
        )

    # Check match completeness
    for match, positions in match_robot_positions.items():
        if len(positions) != 6:
            missing_positions = VALID_ROBOT_POSITIONS - positions
            log_warning(
                f"[WARNING] Match {match} is missing positions: {missing_positions}."
            )


# ===========================
# MAIN SCRIPT SECTION
# ===========================

seperation_bar()
print("Script 02: Data Cleaning and Preprocessing\n")

try:
    small_seperation_bar("LOAD RAW DATA")
    print(f"[INFO] Loading raw data from: {RAW_MATCH_DATA_PATH}")
    with open(RAW_MATCH_DATA_PATH, "r") as infile:
        raw_data = json.load(infile)

    if not isinstance(raw_data, list):
        raise ValueError("Raw data must be a list of matches.")

    cleaned_data = []
    for entry in raw_data:
        cleaned_entry = validate_and_clean_entry(entry)
        cleaned_data.append(cleaned_entry)

    small_seperation_bar("ANALYZE DATA CONSISTENCY")
    analyze_data_consistency()

    print(f"[INFO] Saving cleaned data to: {CLEANED_MATCH_DATA_PATH}")
    os.makedirs(os.path.dirname(CLEANED_MATCH_DATA_PATH), exist_ok=True)
    with open(CLEANED_MATCH_DATA_PATH, "w") as outfile:
        json.dump(cleaned_data, outfile, indent=4)

    small_seperation_bar("SAVE SCOUTER LEADERBOARD")
    
    # Save scouter leaderboard
    os.makedirs(os.path.dirname(SCOUTER_LEADERBOARD_PATH), exist_ok=True)
    with open(SCOUTER_LEADERBOARD_PATH, "w") as leaderboard_file:
        leaderboard_file.write("Scouter Error Leaderboard:\n")
        for scouter, count in sorted(scouter_warnings.items(), key=lambda x: -x[1]):
            leaderboard_file.write(f"{scouter}: {count} errors/warnings\n")
        leaderboard_file.write("\nScouter Leaderboard:\n")
        for scouter, count in sorted(scouter_participation.items(), key=lambda x: -x[1]):
            leaderboard_file.write(f"{scouter}: {count} matches\n")

    print("\n".join(warnings))
    print(f"[INFO] Total warnings/errors: {len(warnings)}")
    print("Script 02: Completed.")

except Exception as e:
    print(f"[ERROR] An unexpected error occurred: {e}")
    print(traceback.format_exc())
    print("Script 02: Failed.")

print(seperation_bar)