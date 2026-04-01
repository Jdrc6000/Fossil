from pathlib import Path
import json

path = Path(__file__).parent / "dinos.json"

def read():
    print("reading...")
    with open(path, "r") as f:
        data = json.load(f)
    return data

def save(data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    print("saved")

# "rdict-1" means "random dict 1"
def remove_rdict_1(data):
    print("  removing (creatures_elsewhere)...")
    for dino in data["dinos"].values():
        if isinstance(dino, dict):
            if "creature_elsewhere" in dino:
                dino.pop("creature_elsewhere")
    return data

# common datapoints
def remove_datapoints(data):
    print("  removing common datapoints...")
    for dino in data["dinos"].values():
        if isinstance(dino, dict):
            drop = {"ambermine", "prestige_cost_ratio", "prestige_area_ratio", "species_id", "fossil_icon", "fossil_biosyn_icon", "uuid"}
            for key in drop:dino.pop(key, None)
    return data

if __name__ == "__main__":
    data = read()
    data = remove_rdict_1(data)
    data = remove_datapoints(data)
    save(data)