import json

def readJson (file):
	with open(file, "r") as jsonFile:
		data = json.load(jsonFile)
	return data

def writeJson(file, data):
	with open(file, "w") as jsonFile:
		json.dump(data, jsonFile)