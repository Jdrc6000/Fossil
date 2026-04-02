from pathlib import Path
import json

base_path = Path(__file__).parent
dino_path = {
    "jwe2": base_path / "jwe2_dinos.json",
    "jwe3": base_path / "jwe3_dinos.json",
}
guides_path = base_path / "guides"

data = {
    "jwe2": json.load(open(dino_path["jwe2"])),
    "jwe3": json.load(open(dino_path["jwe3"])),
}

# dinos
def list_all_dinos(game: str) -> dict:
    return data[game]["name_map"]

def is_dino_real(dino_name: str, game: str) -> bool:
    dino_name = dino_name.lower().strip().replace(" ", "")
    return dino_name in data[game]["dinos"]

def query_dino(dino_name: str, game: str) -> None | dict:
    dino_name = dino_name.lower().strip().replace(" ", "")
    if not is_dino_real(dino_name, game): return None
    return data[game]["dinos"][dino_name]

# guides
def list_all_guides(game: str) -> list[str]:
    if not guides_path.exists(): return []
    return [f.stem for f in (guides_path / game).glob("*.md")]

def read_guide(guide_name: str, game: str) -> str | None:
    guide_path = guides_path / game / f"{guide_name}.md"
    
    if not guide_path.exists(): return None
    return guide_path.read_text(encoding="utf-8")

if __name__ == "__main__":
    print(list_all_dinos("jwe3"))
    print(is_dino_real("tylosaurus", "jwe2"))
    print(True if query_dino("tapejara", "jwe2") else False)
    
    print(list_all_guides("jwe3"))
    print(True if read_guide("dominance", "jwe3") else False)