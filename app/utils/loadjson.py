import json
from pathlib import Path

DATA_DIR = Path("data")

def load_json(filename):
    file_path = DATA_DIR / filename
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)