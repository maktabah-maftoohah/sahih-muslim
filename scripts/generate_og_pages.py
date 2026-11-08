#!/usr/bin/env python3
"""
scripts/generate_og_pages.py
Generates lightweight static Open Graph preview & redirect stubs for all hadiths in Sahih Muslim.
Enables rich link unfurling on WhatsApp, Facebook, Telegram, Twitter/X, Discord, and LinkedIn
while instantly redirecting human visitors into the SPA reading view with smooth scroll & highlight.
"""

import html
import json
import os
import shutil
import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
HADITHS_DIR = ROOT_DIR / "data" / "hadiths"

def clean_og_pages():
    cleaned = 0
    for entry in ROOT_DIR.iterdir():
        if entry.is_dir() and entry.name.isdigit():
            shutil.rmtree(entry)
            cleaned += 1
    print(f"Cleaned {cleaned} generated hadith directory trees.")

def main():
    if "--clean" in sys.argv:
        clean_og_pages()
        return

    start_time = time.time()
    base_url = "https://maktabah-maftoohah.github.io/sahih-muslim"
    banner_url = f"{base_url}/assets/og-banner.jpg"

    total_hadiths = 0
    hadith_files = sorted(HADITHS_DIR.glob("*.json"))

    print(f"Scanning {len(hadith_files)} book shard files...")

    for hf in hadith_files:
        with open(hf, "r", encoding="utf-8") as f:
            hadiths = json.load(f)

        for h in hadiths:
            h_num = h.get("hadith_number")
            if h_num is None:
                continue

            # Handle integer or float hadith numbers
            h_str = str(int(h_num)) if isinstance(h_num, (int, float)) and float(h_num).is_integer() else str(h_num)
            
            # Directory e.g. /1/ or /42/
            target_dir = ROOT_DIR / h_str
            target_dir.mkdir(parents=True, exist_ok=True)
            out_file = target_dir / "index.html"

            book_title_ms = h.get("book_title", {}).get("ms") or f"Kitab {h.get('book_number')}"
            book_title_ar = h.get("book_title", {}).get("ar") or ""
            in_book = h.get("in_book_number")
            in_book_text = f" : Hadis {in_book}" if in_book else ""

            # Prepare snippet for description
            ar_text = h.get("arabic", "").strip()
            ar_snippet = (ar_text[:140] + "...") if len(ar_text) > 140 else ar_text
            
            trans_ms = h.get("translations", {}).get("ms") or h.get("translations", {}).get("en") or ""
            trans_snippet = (trans_ms[:180] + "...") if len(trans_ms) > 180 else trans_ms

            page_title = f"Sahih Muslim #{h_str} — Maktabah Maftoohah"
            og_title = f"Sahih Muslim #{h_str} ({book_title_ms})"
            og_desc = f"{ar_snippet} — {trans_snippet}"
            og_url = f"{base_url}/{h_str}"

            # Prepare direct Quran references if present
            quran_links = []
            for cr in h.get("cross_references", []):
                if cr.get("type") == "quran":
                    s_num = cr.get("surah")
                    a_num = cr.get("ayah")
                    s_name = cr.get("surah_name") or f"Surah {s_num}"
                    cr_url = cr.get("url") or f"https://maktabah-maftoohah.github.io/al-quran/{s_num}/{a_num}"
                    quran_links.append(f'<a href="{cr_url}" target="_blank" rel="noopener" style="display: inline-block; margin: 0.25rem 0.35rem; background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.5); color: #38bdf8; text-decoration: none; font-size: 0.85rem; font-weight: 600; padding: 0.4rem 0.85rem; border-radius: 6px;">📖 Rujuk {html.escape(s_name)} ({s_num}:{a_num}) dalam Al-Quran Digital ↗</a>')

            quran_html = f'<div style="margin: 1rem 0;">{"".join(quran_links)}</div>' if quran_links else ""

            # Calculate relative path back to root (1 directory deep)
            redirect_target = f"../#hadith/{h_str}"

            html_content = f"""<!DOCTYPE html>
<html lang="ms">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(page_title)}</title>

  <!-- Open Graph & Twitter Social Card Meta Tags -->
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Maktabah Maftoohah — Sahih Muslim">
  <meta property="og:title" content="{html.escape(og_title)}">
  <meta property="og:description" content="{html.escape(og_desc)}">
  <meta property="og:image" content="{banner_url}">
  <meta property="og:image:secure_url" content="{banner_url}">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{html.escape(og_title)}">
  <meta property="og:url" content="{og_url}">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(og_title)}">
  <meta name="twitter:description" content="{html.escape(og_desc)}">
  <meta name="twitter:image" content="{banner_url}">

  <!-- Immediate Redirect for Human Visitors -->
  <meta http-equiv="refresh" content="0; url={redirect_target}">
  <script>
    (function() {{
      var p = window.location.pathname;
      var base = p.indexOf('/sahih-muslim') === 0 ? '/sahih-muslim/' : '/';
      window.location.replace(base + '#hadith/{h_str}');
    }})();
  </script>
</head>
<body style="background: #0c2340; color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; padding: 1.5rem; box-sizing: border-box;">
  <div style="max-width: 650px; text-align: center; background: #081728; border: 1px solid rgba(56, 189, 248, 0.4); border-radius: 14px; padding: 2.25rem 2rem; box-shadow: 0 12px 30px rgba(0,0,0,0.6);">
    <div style="font-size: 0.85rem; color: #38bdf8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Maktabah Maftoohah — Sahih Muslim</div>
    <h1 style="font-size: 1.4rem; color: #f8fafc; margin: 0 0 0.5rem 0;">Sahih Muslim #{h_str}</h1>
    <div style="font-size: 0.95rem; color: #fbbf24; margin-bottom: 1.25rem;">{html.escape(book_title_ms)} ({html.escape(book_title_ar)}){in_book_text}</div>
    <div style="font-family: 'Amiri', 'Traditional Arabic', serif; font-size: 1.45rem; color: #fef3c7; direction: rtl; line-height: 1.8; margin-bottom: 1.25rem;">{html.escape(ar_snippet)}</div>
    <p style="font-size: 0.95rem; color: #cbd5e1; line-height: 1.6; margin-bottom: 1.75rem;">"{html.escape(trans_snippet)}"</p>
    {quran_html}
    <a href="{redirect_target}" style="display: inline-block; background: #0284c7; color: #ffffff; text-decoration: none; font-weight: 700; padding: 0.75rem 1.5rem; border-radius: 8px;">Buka Hadis Penuh / Open Full Hadith ↗</a>
  </div>
</body>
</html>
"""
            with open(out_file, "w", encoding="utf-8") as out_f:
                out_f.write(html_content)

            total_hadiths += 1

    elapsed = time.time() - start_time
    print(f"Generated {total_hadiths} static OG preview pages in {elapsed:.2f} seconds.")

if __name__ == "__main__":
    main()
