import json

path = r"/Users/joshuacarter/Desktop/Coding/Code Vault/projects/fossil/dinos.json"

print("reading...")

with open(path, "r") as f:
    data = json.load(f)

print("  removing (creatures_elsewhere)...")
for key, value in data.items():
    if isinstance(value, dict):  # skip the "all_dinos" list
        value.pop("creature_elsewhere", None)

with open(path, "w") as f:
    json.dump(data, f, indent=4)

print("done")