import os
import json
import traceback
from utils.seperation_bars import seperation_bar

# ===========================
# CONFIGURATION
# ===========================

# File paths (Modify these as needed)
CLEANED_MATCH_DATA_PATH = "data/processed/cleaned_match_data.json"  # Input: Cleaned match-level data
TEAM_BASED_MATCH_DATA_PATH = "data/processed/team_based_match_data.json"  # Output: Team-based data


# ===========================
# HELPER FUNCTIONS
# ===========================

def restructure_to_team_based(cleaned_file_path, team_file_path):
    """
    Restructures cleaned match data into a team-based format with advanced statistics.

    :param cleaned_file_path: Path to the cleaned JSON file.
    :param team_file_path: Path to save the team-based JSON file.
    """
    try:
        # Load cleaned data
        print(f"[INFO] Loading cleaned data from: {cleaned_file_path}")
        with open(cleaned_file_path, 'r') as infile:
            cleaned_data = json.load(infile)

        if not isinstance(cleaned_data, list):
            raise ValueError("[ERROR] Cleaned data must be a list of matches.")

        # Group matches by team
        team_data = {}
        for match in cleaned_data:
            team = match["metadata"]["robotTeam"]
            if team not in team_data:
                team_data[team] = {"matches": []}
            team_data[team]["matches"].append(match)

        # Placeholder for advanced statistics calculations
        for team, data in team_data.items():
            for match in data["matches"]:
                # Example: Add any advanced calculations here
                pass  # Placeholder for custom metrics

        # Save team-based data
        print(f"[INFO] Saving team-based match data to: {team_file_path}")
        with open(team_file_path, 'w') as outfile:
            json.dump(team_data, outfile, indent=4)

    except FileNotFoundError as e:
        print(f"[ERROR] Cleaned data file not found: {e}")
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to decode JSON: {e}")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred during restructuring: {e}")
        print(traceback.format_exc())


# ===========================
# MAIN SCRIPT
# ===========================

def main():
    """Main function to execute the team-based match data restructuring."""
    seperation_bar()
    print("Script 02: Team-based Match Data Restructuring\n")

    try:
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(TEAM_BASED_MATCH_DATA_PATH), exist_ok=True)

        # Restructure data to team-based format
        restructure_to_team_based(CLEANED_MATCH_DATA_PATH, TEAM_BASED_MATCH_DATA_PATH)

        print("\n[INFO] Script 02: Completed.")

    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")
        print(traceback.format_exc())
        print("\nScript 02: Failed.")

    seperation_bar()


if __name__ == "__main__":
    main()