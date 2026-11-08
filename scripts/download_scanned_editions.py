"""
scripts/download_scanned_editions.py
CLI tool to download scanned primary PDF editions of Sahih Muslim.
"""

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "scanned_editions.json"
DOCS_DIR = BASE_DIR / "documents"

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def download_file(url: str, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        print(f"  [Already exists] {dest.name} ({dest.stat().st_size / (1024*1024):.1f} MB)")
        return

    print(f"  Downloading: {dest.name} from {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Maktabah Maftoohah Downloader)"})
    with urllib.request.urlopen(req) as resp, open(dest, "wb") as f:
        total = 0
        while True:
            chunk = resp.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)
            total += len(chunk)
            print(f"    Downloaded {total / (1024*1024):.1f} MB...", end="\r")
    print(f"\n  Done: {dest.name} ({total / (1024*1024):.2f} MB)")

def main():
    parser = argparse.ArgumentParser(description="Download scanned PDF editions of Sahih Muslim")
    parser.add_argument("--edition", choices=["dar-al-taseel", "abdul-baqi", "darussalam-bilingual"], default="dar-al-taseel", help="Edition ID")
    parser.add_argument("--volume", type=int, help="Specific volume number to download")
    parser.add_argument("--all", action="store_true", help="Download all volumes for this edition")
    parser.add_argument("--output-dir", type=str, help="Custom output directory")
    args = parser.parse_args()

    if not DATA_FILE.exists():
        print(f"Error: {DATA_FILE} not found.")
        return 1

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    selected_ed = next((e for e in data.get("editions", []) if e["id"] == args.edition), None)
    if not selected_ed:
        print(f"Edition '{args.edition}' not found.")
        return 1

    out_dir = Path(args.output_dir) if args.output_dir else DOCS_DIR
    print(f"Selected Edition: {selected_ed['name']} ({selected_ed['volumes_count']} volumes)")

    volumes = selected_ed.get("volumes", [])
    if args.volume:
        volumes = [v for v in volumes if v["volume"] == args.volume]
        if not volumes:
            print(f"Volume {args.volume} not found.")
            return 1
    elif not args.all:
        print("Note: Specify --volume [N] or --all to proceed with download.")
        print("Available volumes:")
        for v in volumes:
            print(f"  Vol {v['volume']}: {v['filename']} (~{v.get('size_mb', 0)} MB)")
        return 0

    for v in volumes:
        dest = out_dir / v["filename"]
        download_file(v["download_url"], dest)

    return 0

if __name__ == "__main__":
    sys.exit(main())
