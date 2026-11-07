import json
from pathlib import Path

def test_data():
    root = Path(__file__).resolve().parent.parent
    data_dir = root / "data"
    if data_dir.exists():
        for f in data_dir.glob("**/*.json"):
            with open(f, "r", encoding="utf-8") as jf:
                json.load(jf)
    print("Data integrity verification PASSED.")

if __name__ == "__main__":
    test_data()
