"""
scripts/generate_epub.py
Generates a valid, complete EPUB 3.0 file of Sahih Muslim from data/hadiths/ and data/books.json.
Output: documents/sahih-muslim.epub
"""

import html
import json
import os
import time
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DOCS_DIR = BASE_DIR / "documents"

def generate_epub():
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    epub_path = DOCS_DIR / "sahih-muslim.epub"

    print("=== Generating Sahih Muslim EPUB 3.0 ===")

    books_file = DATA_DIR / "books.json"
    with open(books_file, "r", encoding="utf-8") as bf:
        books = json.load(bf)

    hadiths_dir = DATA_DIR / "hadiths"

    with zipfile.ZipFile(epub_path, "w") as zf:
        # 1. mimetype (must be first, uncompressed)
        zf.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)

        # 2. META-INF/container.xml
        container_xml = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""
        zf.writestr("META-INF/container.xml", container_xml, compress_type=zipfile.ZIP_DEFLATED)

        # 3. OEBPS/style.css
        css = """@charset "UTF-8";
body {
  font-family: -apple-system, system-ui, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  margin: 1.5rem;
  color: #1e293b;
}
.title-page {
  text-align: center;
  padding: 4rem 1rem;
}
.main-title {
  font-size: 2rem;
  color: #0284c7;
  margin-bottom: 0.5rem;
}
.main-title-ar {
  font-family: 'Amiri', 'Traditional Arabic', serif;
  font-size: 2.2rem;
  direction: rtl;
  color: #d97706;
  margin-bottom: 1.5rem;
}
.book-heading {
  border-bottom: 2px solid #0284c7;
  padding-bottom: 0.5rem;
  margin-bottom: 1.5rem;
  color: #0284c7;
}
.book-heading-ar {
  font-family: 'Amiri', 'Traditional Arabic', serif;
  direction: rtl;
  color: #d97706;
  font-size: 1.6rem;
  margin-top: -0.5rem;
}
.hadith-entry {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}
.hadith-header {
  font-weight: bold;
  color: #0284c7;
  margin-bottom: 0.75rem;
  font-size: 1rem;
}
.arabic-text {
  font-family: 'Amiri', 'Traditional Arabic', serif;
  font-size: 1.4rem;
  line-height: 2.2;
  direction: rtl;
  text-align: right;
  color: #0f172a;
  margin-bottom: 1rem;
  background-color: #f0f9ff;
  padding: 1rem;
  border-radius: 8px;
  border-right: 4px solid #0284c7;
}
.translation-ms, .translation-en {
  margin-top: 0.75rem;
  font-size: 1rem;
}
.trans-label {
  font-weight: 600;
  color: #475569;
}
"""
        zf.writestr("OEBPS/style.css", css, compress_type=zipfile.ZIP_DEFLATED)

        # 4. OEBPS/titlepage.xhtml
        titlepage = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="ms" dir="ltr">
<head>
  <title>Sahih Muslim</title>
  <link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body>
  <div class="title-page">
    <h1 class="main-title">Sahih Muslim</h1>
    <h2 class="main-title-ar">صحيح مسلم</h2>
    <p><strong>Al-Musnad al-Sahih al-Mukhtasar min al-Sunan</strong></p>
    <p>Disusun oleh: <strong>Imam Abu al-Husayn Muslim ibn al-Hajjaj an-Naysaburi (204–261 H)</strong></p>
    <p>Diterbitkan oleh: <strong>Maktabah Maftoohah (المكتبة المفتوحة)</strong></p>
    <p style="margin-top:2rem; font-size:0.9rem; color:#64748b;">Naskhah lengkap 57 Kitab &bull; 7,563 Hadis &bull; Matan Arab, Terjemahan Melayu &amp; Inggeris</p>
  </div>
</body>
</html>"""
        zf.writestr("OEBPS/titlepage.xhtml", titlepage, compress_type=zipfile.ZIP_DEFLATED)

        # 5. Build chapters / book XHTML files
        manifest_items = [
            '<item id="style" href="style.css" media-type="text/css"/>',
            '<item id="titlepage" href="titlepage.xhtml" media-type="application/xhtml+xml"/>',
            '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>'
        ]
        spine_items = ['<itemref idref="titlepage"/>']
        nav_points = []
        nav_links = []

        print(f"  Packaging 57 books into EPUB...")
        for play_order, book in enumerate(books, 1):
            b_num = book["book_number"]
            shard_file = hadiths_dir / f"{b_num:02d}.json"
            if not shard_file.exists():
                continue

            with open(shard_file, "r", encoding="utf-8") as sf:
                hadiths = json.load(sf)

            item_id = f"book_{b_num:02d}"
            filename = f"book_{b_num:02d}.xhtml"

            manifest_items.append(f'<item id="{item_id}" href="{filename}" media-type="application/xhtml+xml"/>')
            spine_items.append(f'<itemref idref="{item_id}"/>')

            b_title = html.escape(book.get("title_ms") or book.get("title") or book.get("title_en") or f"Kitab {b_num}")
            b_title_ar = html.escape(book.get("title_ar", ""))

            nav_links.append(f'<li><a href="{filename}">{b_num}. {b_title} ({b_title_ar})</a></li>')
            nav_points.append(f"""  <navPoint id="np_{b_num}" playOrder="{play_order}">
    <navLabel><text>{b_num}. {b_title}</text></navLabel>
    <content src="{filename}"/>
  </navPoint>""")

            # Build XHTML for this book
            content_html = [
                '<?xml version="1.0" encoding="utf-8"?>',
                '<!DOCTYPE html>',
                '<html xmlns="http://www.w3.org/1999/xhtml" lang="ms" dir="ltr">',
                '<head>',
                f'  <title>{b_title}</title>',
                '  <link rel="stylesheet" type="text/css" href="style.css"/>',
                '</head>',
                '<body>',
                f'  <h1 class="book-heading">{"Muqaddimah" if b_num == 0 else f"Kitab {b_num}"}: {b_title}</h1>',
                f'  <h2 class="book-heading-ar">{b_title_ar}</h2>'
            ]

            for h in hadiths:
                h_num = h["hadith_number"]
                in_book = h.get("in_book_number") or ""
                ar = html.escape(h.get("arabic", ""))
                ms = html.escape(h.get("translations", {}).get("ms", ""))
                en = html.escape(h.get("translations", {}).get("en", ""))

                content_html.append(f'  <article class="hadith-entry" id="h{h_num}">')
                content_html.append(f'    <div class="hadith-header">Hadis #{h_num} {f"(Kitab: {in_book})" if in_book else ""}</div>')
                if ar:
                    content_html.append(f'    <p class="arabic-text">{ar}</p>')
                else:
                    content_html.append('    <p class="arabic-text" style="color: #64748b; font-style: italic;">[إسناد ومتابعة تابعة للحديث السابق بدون تكرار المتن]</p>')
                if ms:
                    content_html.append(f'    <div class="translation-ms"><span class="trans-label">Terjemahan Melayu:</span> {ms}</div>')
                if en and en != ms:
                    content_html.append(f'    <div class="translation-en"><span class="trans-label">English Translation:</span> {en}</div>')
                content_html.append('  </article>')

            content_html.append('</body>')
            content_html.append('</html>')

            zf.writestr(f"OEBPS/{filename}", "\n".join(content_html), compress_type=zipfile.ZIP_DEFLATED)

        # 6. OEBPS/nav.xhtml (EPUB 3 Navigation Document)
        nav_xhtml = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="ms">
<head>
  <title>Daftar Kandungan - Sahih Muslim</title>
  <link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body>
  <nav epub:type="toc" id="toc">
    <h1>Daftar Kitab (57 Bab Termasuk Muqaddimah)</h1>
    <ol>
      {"".join(nav_links)}
    </ol>
  </nav>
</body>
</html>"""
        zf.writestr("OEBPS/nav.xhtml", nav_xhtml, compress_type=zipfile.ZIP_DEFLATED)

        # 7. OEBPS/toc.ncx (EPUB 2 compatibility)
        toc_ncx = f"""<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="urn:isbn:maktabah-maftoohah-muslim"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle><text>Sahih Muslim</text></docTitle>
  <navMap>
    {"".join(nav_points)}
  </navMap>
</ncx>"""
        zf.writestr("OEBPS/toc.ncx", toc_ncx, compress_type=zipfile.ZIP_DEFLATED)

        # 8. OEBPS/content.opf
        content_opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId" version="3.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="BookId">urn:isbn:maktabah-maftoohah-muslim</dc:identifier>
    <dc:title>Sahih Muslim (صحيح مسلم)</dc:title>
    <dc:creator>Imam Muslim ibn al-Hajjaj</dc:creator>
    <dc:publisher>Maktabah Maftoohah</dc:publisher>
    <dc:language>ms</dc:language>
    <dc:language>ar</dc:language>
    <dc:language>en</dc:language>
    <meta property="dcterms:modified">{time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}</meta>
  </metadata>
  <manifest>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    {"".join(manifest_items)}
  </manifest>
  <spine toc="ncx">
    {"".join(spine_items)}
  </spine>
</package>"""
        zf.writestr("OEBPS/content.opf", content_opf, compress_type=zipfile.ZIP_DEFLATED)

    size_mb = epub_path.stat().st_size / (1024 * 1024)
    print(f"  Successfully created EPUB: {epub_path.name} ({size_mb:.2f} MB)")
    return 0

if __name__ == "__main__":
    generate_epub()
