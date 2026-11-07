# Project Invariants: Maktabah Maftoohah — Sahih Muslim

> Governed by central standards defined in `maktabah-orchestrator`.

## Core Architectural Invariants
1. **GitHub Pages Subpath Compatibility**:
   - All network requests for assets and data MUST use relative paths (e.g., `./data/...`, `./css/...`, `./js/...`).
   - Absolute root paths (e.g. `/data/...`) break under subpath hosting (`https://maktabah-maftoohah.github.io/sahih-muslim/`).

2. **Encoding & File Standards**:
   - All text files (JSON, JS, CSS, HTML, MD, PY) MUST strictly use UTF-8 encoding without BOM.
   - Python output operations MUST specify `encoding="utf-8"` and `ensure_ascii=False`.

3. **Zero-Build Vanilla ES6 Architecture**:
   - Modern browser vanilla ES6 modules (`import` / `export`) only.
   - Zero compilation, bundling, or external npm runtime dependencies.
   - Entry point loaded via `<script type="module" src="./js/app.js"></script>`.

4. **Sacred Text Authenticity**:
   - NEVER generate or hallucinate Arabic texts or chains of transmission.
   - All texts must be sourced from authentic peer-reviewed editions and verified against canonical indices.

5. **Verification & Testing Commands**:
   - Project & Data Integrity: `python scripts/verify_project.py` && `python scripts/verify_data_integrity.py`.
   - Dev Server: `python scripts/serve.py --port 8000` (or `npm run serve`).
