from pathlib import Path
import requests, json, re

urls = {
    "jwe2": "https://www.paleo.gg/games/jurassic-world-evolution-2/dino-db",
    "jwe3": "https://www.paleo.gg/games/jurassic-world-evolution-3/dino-db"
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def get_next_data(url):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    match = re.search(
        r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
        response.text,
        re.DOTALL,
    )
    if not match:
        return None
    return json.loads(match.group(1))

def get_all_pages(game: str, out_path: Path):
    if game not in urls: print(f"[get_all_pages] 'game' must be in urls ({urls.keys()})");return
    
    index_data = get_next_data(urls[game])
    items = index_data["props"]["pageProps"]["dex"]["items"]
    print(f"[{game}] found {len(items)} dinos in index")

    all_dinos = []
    for item in items:
        slug = item["uuid"]

        try:
            data = get_next_data(f"{urls[game]}/{slug}")
            dino = data["props"]["pageProps"]["detail"]
            all_dinos.append(dino)
            print(f" + {dino.get('name', slug)} ({len(all_dinos)}/{len(items)})")
        except Exception as e:
            print(f" - {slug}: {e}")

    output = {
        "name_map": {d["uuid"]: d["name"] for d in all_dinos if d.get("uuid") and d.get("name")},
        "dinos": {d["uuid"]: d for d in all_dinos},
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"saved {len(all_dinos)} dinos -> {out_path}")

if __name__ == "__main__":
    get_all_pages("jwe2", Path(__file__).parent / "jwe2_dinos.json")
    get_all_pages("jwe3", Path(__file__).parent / "jwe3_dinos.json")