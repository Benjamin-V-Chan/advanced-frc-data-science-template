import json

# JSON Handling Functions
def dump_json_with_path(json_path, indent=4):
    with open(json_path) as json_file:
        print(json.dumps(json.load(json_file), indent))

def dump_json(json_input, indent=4):
    print(json.dumps(json_input, indent)) 

def retrieve_json(json_path, dump_json=False, indent=4):
    with open(json_path) as json_file:
        return_json = json.load(json_file)
        if dump_json:
            print(json.dumps(return_json, indent))
        return return_json

def save_json(json_path, data, indent=4):
    """Saves a JSON object to a file."""
    with open(json_path, "w") as json_file:
        json.dump(data, json_file, indent=indent)
        
# Dictionary Manipulation
def single_dict(dictionary):
    if not isinstance(dictionary, dict):
        return False
    for key in dictionary:
        if isinstance(dictionary[key], dict):
            return False
    return True

def flatten_vars_in_dict(dictionary, return_dict=None, prefix=""):
    """Flattens only variable names but keeps their properties (statistical_data_type, values) intact."""
    if return_dict is None:
        return_dict = {}

    for key, value in dictionary.items():
        full_key = f"{prefix}.{key}" if prefix else key

        if isinstance(value, dict) and "statistical_data_type" not in value:
            # If the dictionary does NOT contain a 'statistical_data_type' key, keep flattening
            flatten_vars_in_dict(value, return_dict, full_key)
        else:
            # If we hit the final structure (statistical data type exists), store as-is
            return_dict[full_key] = value

    return return_dict
