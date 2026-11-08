"""
scripts/extract_muslim_all.py
ETL pipeline for Sahih Muslim:
1. Downloads and archives full-text editions (Arabic vocalized, Arabic plain, English, Nusantara/Indonesian) into data/editions/.
2. Harmonizes and compiles all 57 books (0 to 56) into canonical data/hadiths/{book_id:02d}.json.
3. Updates data/books.json and data/chapters/{book_id:02d}.json with accurate ranges.
4. Updates data/collection.json with canonical collection metadata.
"""

import json
import os
import sys
import time
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
EDITIONS_DIR = DATA_DIR / "editions"
HADITHS_DIR = DATA_DIR / "hadiths"
CHAPTERS_DIR = DATA_DIR / "chapters"

BASE_URL = "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions"

EDITIONS = {
    "ara-muslim": {
        "file": "ara-muslim.min.json",
        "name": "Arabic (Vocalized with Tashkeel)",
        "language": "ar",
        "description": "Standard vocalized Arabic text of Sahih Muslim with full tashkeel."
    },
    "ara-muslim1": {
        "file": "ara-muslim1.min.json",
        "name": "Arabic (Unvocalized Plain)",
        "language": "ar-plain",
        "description": "Normalized Arabic text without diacritics for fast fulltext search."
    },
    "eng-muslim": {
        "file": "eng-muslim.min.json",
        "name": "English (Abdul Hamid Siddiqui)",
        "language": "en",
        "description": "Complete translation of Sahih Muslim by Abdul Hamid Siddiqui."
    },
    "ind-muslim": {
        "file": "ind-muslim.min.json",
        "name": "Nusantara / Indonesian (Terjemahan Lengkap)",
        "language": "ms-id",
        "description": "Complete Nusantara translation of Sahih Muslim hadiths."
    }
}

BOOK_TITLE_FALLBACKS = {
    0: {
        "title_ar": "مقدمة صحيح مسلم",
        "title_ms": "Muqaddimah Sahih Muslim (Pengenalan Hadis)",
        "title_en": "Introduction to Sahih Muslim"
    },
    55: {
        "title_ar": "كتاب الزهد والرقائق",
        "title_ms": "Kitab Zuhud dan Kelembutan Hati",
        "title_en": "Book of Zuhd and Softening of Hearts"
    },
    56: {
        "title_ar": "كتاب التفسير",
        "title_ms": "Kitab Tafsir Al-Quran",
        "title_en": "Book of Quranic Exegesis (Tafsir)"
    }
}

def fetch_json(url: str, retries: int = 3, delay: float = 2.0) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "MaktabahMaftoohah-MuslimBot/1.0"})
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            if attempt == retries:
                raise
            print(f"  [Retry {attempt}/{retries}] Failed fetching {url}: {e}. Retrying...")
            time.sleep(delay * attempt)
    raise RuntimeError(f"Could not fetch {url}")

def run_etl():
    EDITIONS_DIR.mkdir(parents=True, exist_ok=True)
    HADITHS_DIR.mkdir(parents=True, exist_ok=True)
    CHAPTERS_DIR.mkdir(parents=True, exist_ok=True)

    loaded_editions = {}

    print("=== Step 1: Downloading & Archiving Fulltext Editions ===")
    for key, info in EDITIONS.items():
        out_path = EDITIONS_DIR / f"{key}.json"
        if out_path.exists():
            print(f"  Found cached edition: {out_path.name}")
            with open(out_path, "r", encoding="utf-8") as f:
                loaded_editions[key] = json.load(f)
        else:
            url = f"{BASE_URL}/{info['file']}"
            print(f"  Downloading {info['name']} from {url}...")
            data = fetch_json(url)
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
            loaded_editions[key] = data
            print(f"  Saved {len(data.get('hadiths', []))} hadiths to {out_path.name}")

    # Write editions manifest
    manifest = {
        "collection": "sahih-muslim",
        "title": "Sahih Muslim (صحيح مسلم)",
        "total_hadiths": len(loaded_editions["ara-muslim"].get("hadiths", [])),
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "editions": [
            {
                "id": k,
                "name": v["name"],
                "language": v["language"],
                "description": v["description"],
                "filename": f"{k}.json",
                "hadith_count": len(loaded_editions.get(k, {}).get("hadiths", []))
            }
            for k, v in EDITIONS.items()
        ]
    }
    with open(EDITIONS_DIR / "manifest.json", "w", encoding="utf-8") as mf:
        json.dump(manifest, mf, ensure_ascii=False, indent=2)
    print("  Created data/editions/manifest.json")

    print("\n=== Step 2: Indexing and Mapping Hadiths by Book Number ===")
    ara_hadiths = loaded_editions["ara-muslim"].get("hadiths", [])
    eng_hadiths = loaded_editions.get("eng-muslim", {}).get("hadiths", [])
    ind_hadiths = loaded_editions.get("ind-muslim", {}).get("hadiths", [])

    eng_map = {h["hadithnumber"]: h.get("text", "") for h in eng_hadiths}
    ind_map = {h["hadithnumber"]: h.get("text", "") for h in ind_hadiths}

    # Load existing books.json for canonical titles
    books_file = DATA_DIR / "books.json"
    existing_books = []
    if books_file.exists():
        with open(books_file, "r", encoding="utf-8") as bf:
            existing_books = json.load(bf)
    books_dict = {b["book_number"]: b for b in existing_books}

    # Ensure fallback books (0, 55, 56) are present in books_dict
    for b_num, b_meta in BOOK_TITLE_FALLBACKS.items():
        if b_num not in books_dict:
            books_dict[b_num] = {
                "book_number": b_num,
                "title_ar": b_meta["title_ar"],
                "title_ms": b_meta["title_ms"],
                "title_en": b_meta["title_en"]
            }

    # Group hadiths sequentially
    books_hadiths = {}
    current_book = 0

    for h in ara_hadiths:
        h_num = h["hadithnumber"]
        ref_book = h.get("reference", {}).get("book")
        if ref_book and int(ref_book) > 0:
            current_book = int(ref_book)
        elif h_num <= 92:
            current_book = 0
        # Otherwise stays as current_book

        if current_book not in books_hadiths:
            books_hadiths[current_book] = []
        books_hadiths[current_book].append(h)

    print(f"  Indexed {sum(len(v) for v in books_hadiths.values())} hadiths across {len(books_hadiths)} books.")

    print("\n=== Step 3: Generating Canonical Hadith Shards (00.json - 56.json) ===")
    updated_books = []

    for book_num in sorted(books_hadiths.keys()):
        h_list = books_hadiths[book_num]
        book_info = books_dict.get(book_num, {
            "book_number": book_num,
            "title_ms": f"Kitab {book_num}",
            "title_ar": f"كتاب {book_num}",
            "title_en": f"Book {book_num}"
        })

        shard_hadiths = []
        first_h_num = h_list[0]["hadithnumber"]
        last_h_num = h_list[-1]["hadithnumber"]

        for idx, h in enumerate(h_list, start=1):
            h_num = h["hadithnumber"]
            in_book = h.get("reference", {}).get("hadith")
            ar_text = h.get("text", "").strip()

            en_trans = eng_map.get(h_num, "").strip()
            ms_trans = ind_map.get(h_num, "").strip()

            # Normalize integer or float hadith number
            normalized_h_num = int(h_num) if float(h_num).is_integer() else float(h_num)
            in_book_val = int(in_book) if in_book is not None and int(in_book) > 0 else idx

            canonical_h = {
                "collection_id": "sahih-muslim",
                "hadith_number": normalized_h_num,
                "in_book_number": in_book_val,
                "book_number": int(book_num),
                "book_title": {
                    "ar": book_info.get("title_ar", ""),
                    "ms": book_info.get("title_ms") or book_info.get("title", ""),
                    "en": book_info.get("title_en", "")
                },
                "arabic": ar_text,
                "gradings": [
                    {
                        "scholar": "Imam Muslim",
                        "grade": "Sahih",
                        "grade_ar": "صحيح",
                        "notes": "Al-Musnad al-Sahih al-Mukhtasar bi Naql al-'Adl 'an al-'Adl ila Rasulillah SAW"
                    }
                ],
                "translations": {
                    "ms": ms_trans if ms_trans else en_trans,
                    "en": en_trans,
                    "id": ms_trans
                }
            }
            shard_hadiths.append(canonical_h)

        # Write shard file e.g. 00.json, 01.json, ..., 56.json
        shard_filename = f"{book_num:02d}.json"
        shard_path = HADITHS_DIR / shard_filename
        with open(shard_path, "w", encoding="utf-8") as sf:
            json.dump(shard_hadiths, sf, ensure_ascii=False, indent=2)

        # Build chapters for this book
        chapters_data = [
            {
                "chapter_number": 1,
                "title": book_info.get("title_ms") or book_info.get("title", ""),
                "title_ar": book_info.get("title_ar", ""),
                "hadith_range": f"{first_h_num}-{last_h_num}",
                "hadiths_count": len(shard_hadiths)
            }
        ]
        with open(CHAPTERS_DIR / shard_filename, "w", encoding="utf-8") as cf:
            json.dump(chapters_data, cf, ensure_ascii=False, indent=2)

        # Update book record
        book_info["hadith_range"] = f"{first_h_num}-{last_h_num}"
        book_info["hadiths_count"] = len(shard_hadiths)
        book_info["hadith_start"] = int(first_h_num)
        book_info["hadith_end"] = int(last_h_num)
        book_info["hadith_count"] = len(shard_hadiths)
        updated_books.append(book_info)

    # Save updated books.json
    with open(DATA_DIR / "books.json", "w", encoding="utf-8") as bf:
        json.dump(updated_books, bf, ensure_ascii=False, indent=2)

    # Update collection.json
    collection_path = DATA_DIR / "collection.json"
    collection_meta = {
        "collection": "sahih-muslim",
        "title": "Maktabah Maftoohah — Sahih Muslim",
        "title_ar": "صحيح مسلم",
        "total_books": len(updated_books),
        "total_hadiths": len(ara_hadiths),
        "seeded_books": [b["book_number"] for b in updated_books],
        "active_hadiths": len(ara_hadiths)
    }
    with open(collection_path, "w", encoding="utf-8") as colf:
        json.dump(collection_meta, colf, ensure_ascii=False, indent=2)

    print(f"  Successfully compiled {len(updated_books)} books into data/hadiths/ and data/chapters/!")
    print(f"  Total hadiths in collection: {len(ara_hadiths)}")
    return 0

if __name__ == "__main__":
    run_etl()
