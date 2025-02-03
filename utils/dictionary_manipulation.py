import json

def retrieve_json(json_path):
    with open(json_path) as json_file:
        return json.load(json_file)
    
def single_dict(dictionary):
    if not isinstance(dictionary, dict):
        return False
    for key in dictionary:
        if isinstance(dictionary[key], dict):
            return False
    return True

def flatten_vars_in_dict(dictionary, return_dict=None, prefix=""):
    if return_dict is None:
        return_dict = {}
    
    for key in dictionary:
        full_key = f"{prefix}.{key}" if prefix else key
        if single_dict(dictionary[key]):
            return_dict[full_key] = dictionary[key]
        else:
            flatten_vars_in_dict(dictionary[key], return_dict, full_key)
    
    return return_dict