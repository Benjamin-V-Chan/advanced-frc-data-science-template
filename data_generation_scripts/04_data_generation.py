import json
import copy
import random
import numpy as np
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

def find_lowest_teams_list(matches_per_team, teams_per_match=6):
    """
    Returns a list of teams_per_match count of the lowest number of matches played.

    Args:
        matches_per_team (dict): Dictionary where keys are team numbers and values are match counts.
        teams_per_match (int): Number of teams to return.

    Returns:
        list: A list of team numbers with the lowest match count, limited to teams_per_match.
    """
    if teams_per_match > len(matches_per_team):
        print(f"[MAJOR ERROR] teams_per_match ({teams_per_match}) cannot be greater than total teams ({len(matches_per_team)}).")
        return []

    if not matches_per_team:
        return []

    # Find the minimum number of matches played
    min_matches = min(matches_per_team.values())

    # Get all teams with the minimum matches
    lowest_teams = [team for team, count in matches_per_team.items() if count == min_matches]

    # Return exactly `teams_per_match` teams, choosing randomly if needed
    return random.sample(lowest_teams, min(len(lowest_teams), teams_per_match))

def generate_quantitative_variable(var_config):
    """
    Generates a single random quantitative variable value based on the given variable configuration.
    
    Args:
        var_config (dict): The variable configuration dictionary.

    Returns:
        float or int: The generated value.
    """
    # Extract parameters
    mean = var_config["data_deviation"][0]["mean"]
    std_dev = var_config["data_deviation"][0]["standard_deviation"]
    missing_chance = var_config["missing_values_chance"]
    missing_filler = var_config["missing_values_filler"]
    outlier_chance = var_config["positive_outliers_chance"]
    outlier_std_dev_multiplier = var_config["positive_outliers_amount_of_std_devs"]

    # Generate base value from normal distribution
    value = np.random.normal(loc=mean, scale=std_dev)

    # Introduce missing values
    if random.random() < missing_chance:
        return missing_filler  # Return missing value filler

    # Introduce positive outliers
    if random.random() < outlier_chance:
        value += outlier_std_dev_multiplier * std_dev  # Add outlier deviation

    return value


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
    while min_matches_for_team < num_matches_per_team:
        
        match_number += 1
        
        lowest_teams = find_lowest_teams_list(matches_per_team)
        
        print(lowest_teams)
        
        for index, team in enumerate(lowest_teams):
            
            team_robot_position = robot_positions[index]
            
            # Create a deep copy of the expected structure for each team
            team_performance = copy.deepcopy(expected_data_structure_dict)
            
            # Assign the team number to the structure
            team_performance_metadata = {
                "scouterName": random.choice(scouter_names),
                "matchNumber": match_number,
                "robotTeam": team,
                "robotPosition": team_robot_position
                }

            team_performance_variables = {}

            for var_key, var_config in data_generation_config_variables.items():
                # print(expected_data_structure_variables)
                var_statistical_data_type = expected_data_structure_variables[var_key]['statistical_data_type']
                
                if var_statistical_data_type == 'quantitative':
                    team_performance_variables[var_key] = generate_quantitative_variable(var_config)
                
                elif var_statistical_data_type == 'categorical':
                    team_performance_variables[var_key] = generate_categorical_variable(var_config)
                
                elif var_statistical_data_type == 'binary':
                    team_performance_variables[var_key] = generate_binary_variable(var_config)
                
                else:
                    print(f"[MAJOR ERROR] INVALID STATISTICAL DATA TYPE")
            
            team_performance = {
                'metadata': team_performance_metadata,
                'variables': team_performance_variables
                }
            
            # Append to output list
            output_data_list.append(team_performance)
            
            # Update the matches played count
            matches_per_team[team] += 1

        min_matches_for_team = min(matches_per_team.values())  # Update minimum match count

else:
    print("[INFO] Running Data Generation Set OFF")

# Print the final generated data
# print("\nGenerated Output Data List:")
# print(json.dumps(output_data_list, indent=4))

with open(output_generated_data_path, "w") as outfile:
    json.dump(output_data_list, outfile, indent=4)

seperation_bar()