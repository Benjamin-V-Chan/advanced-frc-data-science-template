import json
from utils.seperation_bars import *
from utils.dictionary_manipulation import *

# ===========================
# CONFIGURATION SECTION
# ===========================

data_generation_config_path = 'config/data_generation_config.json'
expected_data_structure_path = 'config/expected_data_structure.json'
output_generated_data_path = 'data/raw/raw_match_data.json'

# ===========================
# HELPER FUNCTIONS SECTION
# ===========================



# ===========================
# MAIN SCRIPT SECTION
# ===========================

seperation_bar()
print("Script 04: Data Generation\n")

# Retrieve JSON Data
small_seperation_bar("RETRIEVE expected_data_structure.json")

# Retrieve Expected Data Structure JSON as Dict
expected_data_structure_dict = retrieve_json(expected_data_structure_path)
print("\nExpected Data Structure JSON:")
print(json.dumps(expected_data_structure_dict, indent=4))

# Retrieve Data Generation Config Default Values JSON as Dict
data_generation_config_dict = retrieve_json(data_generation_config_path)
print("\nData Generation Config JSON:")
print(json.dumps(data_generation_config_dict, indent=4))

# Retrieve Data Generation settings
running_data_generation = data_generation_config_dict['running_data_generation']
num_teams = data_generation_config_dict['data_quantity']['number_of_teams']
num_matches_per_team = data_generation_config_dict['data_quantity']['number_of_matches_per_team']

# Matches per team dict tracker
matches_per_team = {team: 0 for team in range(1, num_teams + 1)}
print("Initialized Matches Per Team:\n", matches_per_team)

# Simulation Setup Vars
output_data_list = []  # Initializing output JSON as a list
min_matches_for_team = 0
match_number = 0

robot_positions = expected_data_structure_dict['metadata']['robotPosition']['values']
expected_data_structure_variables = flatten_vars_in_dict(expected_data_structure_dict["variables"], return_dict={})

scouter_names = data_generation_config_dict['scouter_names']
data_generation_config_variables = data_generation_config_dict['variables']

# Outer Loop
if running_data_generation:
    while min_matches_for_team < matches_per_team:
        # retrieve list of teams with lowest matches
        # simulate match
        # add data to output_data_dict
        # find min_matches_for_team
else:
    print("[INFO] Running Data Generation Set OFF")

# END OF SCRIPT

seperation_bar()