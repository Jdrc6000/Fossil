from pathlib import Path
import json

base_path = Path(r"/Users/joshuacarter/Desktop/Coding/Code Vault/projects/fossil")
dino_path = base_path / "dinos.json"
guides_path = base_path / "guides"

with open(dino_path, "r") as f:
    data = json.load(f)
all_dinos = data["all_dinos"]

# dinos
def list_all_dinos() -> dict:
    return all_dinos

def is_dino_real(dino_name: str) -> bool:
    dino_name = dino_name.lower().strip().replace(" ", "")
    return dino_name in all_dinos

def query_dino(dino_name: str) -> None | dict:
    dino_name = dino_name.lower().strip().replace(" ", "")
    if not is_dino_real(dino_name): return None
    return data[dino_name]

# guides
def list_all_guides() -> list[str]:
    if not guides_path.exists(): return []
    return [f.stem for f in guides_path.glob("*.md")]

def read_guide(guide_name: str) -> str | None:
    guide_path = guides_path / f"{guide_name}.md"
    
    if not guide_path.exists(): return None
    return guide_path.read_text(encoding="utf-8")