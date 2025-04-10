import json
import copy
import random
import numpy as np
from utils.logging import *
from utils.dictionary_manipulation import *

# ===========================
# CONFIGURATION SECTION
# ===========================

DATA_GENERATION_CONFIG_PATH = 'config/data_generation_config.json'
EXPECTED_DATA_STRUCTURE_CONFIG_PATH = 'config/expected_data_structure.json'

GENERATED_RAW_DATA_PATH = 'data/raw/generated_raw_data.json'

# ===========================
# HELPER FUNCTIONS SECTION
# ===========================

def find_lowest_teams_list(matches_per_team, teams_per_match):
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


def generate_categorical_variable(var_config):
    """
    Generates a single random categorical variable value based on the given variable configuration.
    
    Args:
        var_config (dict): The configuration dictionary.

    Returns:
        bool: The generated value.
    """
    distribution = var_config["unfair_distribution"][0]
    choices, probabilities = zip(*distribution.items())  # Extract values and probabilities

    # Handle missing values
    missing_chance = var_config["missing_values_chance"]
    missing_filler = var_config["missing_values_filler"]
    if random.random() < missing_chance:
        return missing_filler

    return random.choices(choices, probabilities)[0]  # Select based on unfair distribution


def generate_binary_variable(var_config):
    """
    Generates a single random binary variable value based on the given variable configuration.
    
    Args:
        var_config (dict): The configuration dictionary.

    Returns:
        str: The generated value.
    """
    distribution = var_config["unfair_distribution"][0]
    choices, probabilities = zip(*distribution.items())  # Extract values and probabilities

    # Handle missing values
    missing_chance = var_config["missing_values_chance"]
    missing_filler = var_config["missing_values_filler"]
    if random.random() < missing_chance:
        return missing_filler

    return random.choices(choices, probabilities)[0]  # Select based on unfair distribution


# ===========================
# MAIN SCRIPT SECTION
# ===========================

def main():
    
    # SCRIPT START
    script_start("[Data Generation] 04 - Data Generation")
    
    

    # LOAD CONFIG
    log_header("Load Config")

    log_info(f"Loading 'Expected Data Structure Config' from '{EXPECTED_DATA_STRUCTURE_CONFIG_PATH}'")
    expected_data_structure = retrieve_json(EXPECTED_DATA_STRUCTURE_CONFIG_PATH)
    log_info(f"Expected Data Structure Config:\n{json.dumps(expected_data_structure, indent=4)}\n")

    log_info(f"Loading 'Data Generation Config' from '{DATA_GENERATION_CONFIG_PATH}'")
    data_generation = retrieve_json(DATA_GENERATION_CONFIG_PATH)
    log_info(f"Data Generation Config:\n{json.dumps(data_generation, indent=4)}\n")
    
    
    
    # DATA GENERATION SETUP
    log_header("Data Generation Setup")
    
    # Retrieve Expected Data Structure Variables
    log_subheader("Retrieve Expected Data Structure Variables")
    
    expected_data_structure_matchapp_variables = flatten_vars_in_dict(expected_data_structure['matchapp_variables'])
    log_info(f"Expected Data Structure Matchapp Variables:\n{json.dumps(expected_data_structure_matchapp_variables, indent=4)}")
    
    expected_data_structure_superapp_variables = flatten_vars_in_dict(expected_data_structure['superapp_variables'])
    log_info(f"Expected Data Structure Superapp Variables:\n{json.dumps(expected_data_structure_superapp_variables, indent=4)}")
    
    
    # Retrieve Data Generation settings
    log_subheader("Retrieve Data Generation Settings")
    
    data_generation_settings = {
        "running_data_generation": data_generation['running_data_generation'],
        "num_teams": data_generation['data_quantity']['number_of_teams'],
        "num_matches_per_team": data_generation['data_quantity']['number_of_matches_per_team'],
        "teams_per_match": data_generation['data_quantity']['teams_per_match'],
        "scouters": data_generation['scouter_names'],
        "data_generation_superapp_variables": data_generation['matchapp_variables'],
        "data_generation_matchapp_variables": data_generation['superapp_variables']
    }


    # Simulation Setup Vars
    log_subheader("Simulation Setup Variables")
    output_data_list = []  # Initializing output JSON as a list
    min_matches_for_team = 0
    match_number = 0
    matches_per_team = {team: 0 for team in range(1, num_teams + 1)}


    
    # DATA GENERATION
    log_header("Data Generation")
    
    if data_generation_settings["running_data_generation"]:
        
        # MATCH LOOP
        log_subheader("Data Generation (Match-level)")
        while min_matches_for_team < data_generation_settings:
            
            match_number += 1
            
            match_scouters = random.sample(scouters, teams_per_match)
            
            lowest_teams = find_lowest_teams_list(matches_per_team, teams_per_match)
            
            print(lowest_teams)
            
            # TEAM PERFORMANCE LOOP
            for current_robot_index, team in enumerate(lowest_teams):
                
                team_robot_position = robot_positions[current_robot_index]
                
                # Create a deep copy of the expected structure for each team
                team_performance = copy.deepcopy(expected_data_structure_dict)
                
                # Assign the team number to the structure
                team_performance_metadata = {
                    "scouterName": match_scouters[current_robot_index],
                    "matchNumber": match_number,
                    "robotTeam": team,
                    "robotPosition": team_robot_position
                    }

                team_performance_variables = {}

                # TEAM PERFORMANCE VARIABLES LOOP
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

    # SAVE DATA
    save_json(GENERATED_RAW_DATA_PATH, output_data_list)

    # SCRIPT END
    script_end("[Data Generation] 04 - Data Generation")

if __name__ == "__main__":
    main()