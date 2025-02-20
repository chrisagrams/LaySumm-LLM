import json

file_path = "data/plos/val.json"

with open(file_path, "r") as file:
    data = json.load(file)

print(f"{file_path}\t{len(data)}")
