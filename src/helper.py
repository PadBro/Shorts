import json

def read_json (file):
    with open(file, "r") as json_file:
        data = json.load(json_file)
    return data

def write_json(file, data):
    with open(file, "w") as json_file:
        json.dump(data, json_file, indent=4, sort_keys=True)
