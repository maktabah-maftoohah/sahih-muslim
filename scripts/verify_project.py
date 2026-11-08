import json
from pathlib import Path

def test_project():
    root = Path(__file__).resolve().parent.parent
    assert (root / "index.html").exists(), "index.html missing"
    assert (root / "404.html").exists(), "404.html missing"
    assert (root / "AGENTS.md").exists(), "AGENTS.md missing"
    assert (root / ".nojekyll").exists(), ".nojekyll missing"
    assert (root / "manifest.webmanifest").exists(), "manifest.webmanifest missing"
    assert (root / "sw.js").exists(), "sw.js missing"
    assert (root / "icon.svg").exists(), "icon.svg missing"

    # Assets & Branding
    assert (root / "assets" / "og-banner.jpg").exists(), "og-banner.jpg missing"
    assert (root / "assets" / "logo.svg").exists(), "logo.svg missing"
    assert (root / "assets" / "logo.png").exists(), "logo.png missing"
    assert (root / "assets" / "logo-mark.svg").exists(), "logo-mark.svg missing"
    assert (root / "assets" / "logo-mark.png").exists(), "logo-mark.png missing"
    assert (root / "assets" / "github-avatar.png").exists(), "github-avatar.png missing"
    assert (root / "assets" / "site-banner.png").exists(), "site-banner.png missing"
    assert (root / "assets" / "icon-192.png").exists(), "icon-192.png missing"
    assert (root / "assets" / "icon-512.png").exists(), "icon-512.png missing"

    # Static OG stubs
    assert (root / "1" / "index.html").exists(), "Hadith 1 OG page stub missing"
    assert (root / "7563" / "index.html").exists(), "Hadith 7563 OG page stub missing"

    # Data files
    assert (root / "data" / "books.json").exists(), "books.json missing"
    assert (root / "data" / "collection.json").exists(), "collection.json missing"
    assert (root / "data" / "editions" / "manifest.json").exists(), "editions/manifest.json missing"
    assert (root / "data" / "scanned_editions.json").exists(), "scanned_editions.json missing"

    # Documentation & Primary Scans Registry
    assert (root / "docs" / "SCANNED_EDITIONS.md").exists(), "SCANNED_EDITIONS.md missing"
    assert (root / "docs" / "index.html").exists(), "docs/index.html missing"
    assert (root / "documents" / "sahih-muslim.epub").exists(), "sahih-muslim.epub missing"
    assert (root / "documents" / "muslim_taseel_01.pdf").exists(), "muslim_taseel_01.pdf missing"

    with open(root / "data" / "books.json", "r", encoding="utf-8") as f:
        books = json.load(f)
        assert len(books) == 57, f"Expected 57 books, found {len(books)}"

    with open(root / "data" / "collection.json", "r", encoding="utf-8") as f:
        col = json.load(f)
        assert col.get("total_hadiths") == 7563, f"Expected 7563 hadiths, found {col.get('total_hadiths')}"

    print("Project structure & document verification PASSED for sahih-muslim.")

if __name__ == "__main__":
    test_project()
