"""Module providing helpfull functions."""

import json

def read_json (file):
    """Function read given file and return json."""
    with open(file, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data

def write_json(file, data):
    """Function writes json to give file."""
    with open(file, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, sort_keys=True)
