import os
from pathlib import Path

def test_project():
    root = Path(__file__).resolve().parent.parent
    assert (root / "index.html").exists(), "index.html missing"
    assert (root / "AGENTS.md").exists(), "AGENTS.md missing"
    assert (root / ".nojekyll").exists(), ".nojekyll missing"
    print("Project structure verification PASSED for sahih-muslim.")

if __name__ == "__main__":
    test_project()
