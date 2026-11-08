#!/usr/bin/env python3
"""
scripts/generate_branding.py
Generates the complete official Maktabah Maftoohah visual identity for Sahih Muslim:
1. assets/logo-mark.svg & logo-mark.png (512x512 Standalone Emblem)
2. assets/github-avatar.svg, github-avatar.png, avatar.png (512x512 Circle-Safe GitHub Avatar)
3. assets/logo.svg & logo.png (800x200 Horizontal Brand Lockup)
4. assets/site-banner.svg & site-banner.png (1280x640 GitHub Repository Social Preview)
5. assets/og-banner.jpg (1280x640 High-Res Open Graph Banner)
6. assets/icon-192.png & icon-512.png (PWA Manifest Icons)
7. root icon.svg
"""

import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

CHROME_EXEC = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
PLAYWRIGHT_DIR = "D:/RepoTools/GitHub/maktabah-maftoohah/al-quran/node_modules"

# ==============================================================================
# 1. BUILD ASSETS/LOGO-MARK.SVG (512x512 Standalone Square Emblem)
# ==============================================================================
def build_logo_mark_svg() -> str:
    return '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <!-- Background Gradient (Royal Midnight Sapphire) -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0c2340" />
      <stop offset="50%" stop-color="#081728" />
      <stop offset="100%" stop-color="#030b14" />
    </linearGradient>

    <!-- Regal Gold Gradient -->
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fef3c7" />
      <stop offset="25%" stop-color="#fde68a" />
      <stop offset="50%" stop-color="#f59e0b" />
      <stop offset="75%" stop-color="#d97706" />
      <stop offset="100%" stop-color="#92400e" />
    </linearGradient>

    <!-- Sapphire Glow Radial -->
    <radialGradient id="sapphireAura" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#0284c7" stop-opacity="0.38" />
      <stop offset="60%" stop-color="#0369a1" stop-opacity="0.14" />
      <stop offset="100%" stop-color="#0b1e36" stop-opacity="0" />
    </radialGradient>

    <!-- Book Page Gradient -->
    <linearGradient id="pageGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#fef9c3" />
      <stop offset="48%" stop-color="#ffffff" />
      <stop offset="52%" stop-color="#e2e8f0" />
      <stop offset="100%" stop-color="#fef9c3" />
    </linearGradient>

    <style>
      @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@700&amp;family=Inter:wght@600;700;800&amp;display=swap');
      .ar-title { font-family: 'Amiri', 'Traditional Arabic', serif; font-weight: 700; }
      .latin-brand { font-family: 'Inter', -apple-system, sans-serif; }
    </style>
  </defs>

  <!-- Base Rounded Container (Squircle) -->
  <rect width="512" height="512" rx="108" fill="url(#bgGrad)" />
  <rect width="496" height="496" x="8" y="8" rx="100" fill="none" stroke="url(#goldGrad)" stroke-width="2.5" stroke-opacity="0.85" />
  <rect width="480" height="480" x="16" y="16" rx="92" fill="none" stroke="#38bdf8" stroke-width="1" stroke-opacity="0.4" />

  <!-- Ambient Sapphire Aura -->
  <circle cx="256" cy="240" r="190" fill="url(#sapphireAura)" />

  <!-- Outer Islamic 8-Point Geometric Star (Rub el Hizb) Background -->
  <g transform="translate(256, 240)" opacity="0.22" stroke="url(#goldGrad)" stroke-width="2" fill="none">
    <rect x="-140" y="-140" width="280" height="280" rx="20" />
    <rect x="-140" y="-140" width="280" height="280" rx="20" transform="rotate(45)" />
    <circle r="152" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="6 6" />
  </g>

  <!-- Central Open Hadith Tome / Manuscript -->
  <g id="HadithBook" transform="translate(256, 225)">
    <!-- Book Drop Shadow -->
    <ellipse cx="0" cy="98" rx="130" ry="16" fill="#000000" opacity="0.45" />

    <!-- Open Book Cover (Leather Moroccan Sapphire) -->
    <path d="M-132,78 Q-66,94 0,82 Q66,94 132,78 L138,-52 Q66,-36 0,-48 Q-66,-36 -138,-52 Z" 
          fill="#0c4a6e" stroke="url(#goldGrad)" stroke-width="3" />

    <!-- Book Inner Pages (Cream & White Parchment) -->
    <path d="M-124,70 Q-62,84 0,74 Q62,84 124,70 L130,-44 Q62,-30 0,-40 Q-62,-30 -130,-44 Z" 
          fill="url(#pageGrad)" stroke="#cbd5e1" stroke-width="1" />

    <!-- Book Spine Center Fold & Shading -->
    <path d="M-6,-40 Q0,-42 6,-40 L6,74 Q0,76 -6,74 Z" fill="#94a3b8" opacity="0.6" />
    <line x1="0" y1="-41" x2="0" y2="75" stroke="#0284c7" stroke-width="2" />

    <!-- Manuscript Text Ruling Lines (Gold Ink) -->
    <!-- Left Page Lines -->
    <line x1="-105" y1="-18" x2="-22" y2="-12" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" opacity="0.85" />
    <line x1="-110" y1="2" x2="-22" y2="8" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" opacity="0.85" />
    <line x1="-105" y1="22" x2="-22" y2="28" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" opacity="0.85" />
    <line x1="-95" y1="42" x2="-35" y2="48" stroke="#d97706" stroke-width="2" stroke-linecap="round" opacity="0.6" />

    <!-- Right Page Lines -->
    <line x1="22" y1="-12" x2="105" y2="-18" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" opacity="0.85" />
    <line x1="22" y1="8" x2="110" y2="2" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" opacity="0.85" />
    <line x1="22" y1="28" x2="105" y2="22" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" opacity="0.85" />
    <line x1="35" y1="48" x2="95" y2="42" stroke="#d97706" stroke-width="2" stroke-linecap="round" opacity="0.6" />

    <!-- Silk Bookmark Ribbon (Draping Down - Gold) -->
    <path d="M-5,-42 Q-3,10 8,88 L22,96 L16,84 Q4,10 5,-42 Z" fill="#d97706" stroke="#b45309" stroke-width="1" />
    <polygon points="8,88 22,96 17,90 22,84" fill="#fbbf24" />
  </g>

  <!-- Arabic Calligraphy Inscription: "صحيح مسلم" -->
  <text x="256" y="375" text-anchor="middle" class="ar-title" font-size="46" fill="url(#goldGrad)" letter-spacing="1">صَحِيحُ مُسْلِمٍ</text>

  <!-- Subtitle Ribbon Badge: "MAKTABAH MAFTOOHAH" -->
  <g transform="translate(256, 432)">
    <rect x="-145" y="-18" width="290" height="34" rx="10" fill="#082f49" stroke="url(#goldGrad)" stroke-width="1.5" />
    <circle cx="-120" cy="-1" r="3" fill="#fbbf24" />
    <circle cx="120" cy="-1" r="3" fill="#fbbf24" />
    <text x="0" y="5" text-anchor="middle" class="latin-brand" font-size="14.5" font-weight="700" fill="#38bdf8" letter-spacing="2.5">MAKTABAH MAFTOOHAH</text>
  </g>
</svg>'''


# ==============================================================================
# 2. BUILD ASSETS/GITHUB-AVATAR.SVG (512x512 Circle-Safe Avatar)
# ==============================================================================
def build_github_avatar_svg() -> str:
    return '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <!-- Master Circular Mask / Safe Boundary -->
    <clipPath id="circleClip">
      <circle cx="256" cy="256" r="256" />
    </clipPath>

    <linearGradient id="avBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0c2340" />
      <stop offset="50%" stop-color="#081728" />
      <stop offset="100%" stop-color="#020912" />
    </linearGradient>

    <linearGradient id="avGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fef08a" />
      <stop offset="35%" stop-color="#f59e0b" />
      <stop offset="70%" stop-color="#d97706" />
      <stop offset="100%" stop-color="#78350f" />
    </linearGradient>

    <radialGradient id="avGlow" cx="50%" cy="45%" r="48%">
      <stop offset="0%" stop-color="#0284c7" stop-opacity="0.4" />
      <stop offset="65%" stop-color="#0369a1" stop-opacity="0.12" />
      <stop offset="100%" stop-color="#0c2340" stop-opacity="0" />
    </radialGradient>

    <style>
      @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@700&amp;family=Inter:wght@600;700;800&amp;display=swap');
      .ar-avatar { font-family: 'Amiri', 'Traditional Arabic', serif; font-weight: 700; }
      .latin-avatar { font-family: 'Inter', -apple-system, sans-serif; font-weight: 800; }
    </style>
  </defs>

  <!-- Group clipped to Circle for GitHub display -->
  <g clip-path="url(#circleClip)">
    <!-- Base Background -->
    <rect width="512" height="512" fill="url(#avBg)" />

    <!-- Circular Rings -->
    <circle cx="256" cy="256" r="248" fill="none" stroke="url(#avGold)" stroke-width="4" stroke-opacity="0.9" />
    <circle cx="256" cy="256" r="236" fill="none" stroke="#38bdf8" stroke-width="1.5" stroke-opacity="0.4" stroke-dasharray="8 6" />

    <!-- Ambient Sapphire Glow -->
    <circle cx="256" cy="220" r="160" fill="url(#avGlow)" />

    <!-- Compact Open Book Motif -->
    <g transform="translate(256, 185) scale(0.88)">
      <!-- Book Drop Shadow -->
      <ellipse cx="0" cy="85" rx="110" ry="14" fill="#000000" opacity="0.45" />

      <!-- Leather Cover (Sapphire) -->
      <path d="M-115,68 Q-58,82 0,72 Q58,82 115,68 L120,-45 Q58,-32 0,-42 Q-58,-32 -120,-45 Z" 
            fill="#0369a1" stroke="url(#avGold)" stroke-width="3" />

      <!-- Pages Parchment -->
      <path d="M-108,60 Q-54,72 0,64 Q54,72 108,60 L113,-38 Q54,-26 0,-35 Q-54,-26 -113,-38 Z" 
            fill="#fefce8" stroke="#cbd5e1" stroke-width="1" />

      <!-- Center Fold -->
      <line x1="0" y1="-35" x2="0" y2="65" stroke="#0284c7" stroke-width="2" />

      <!-- Ruling Lines Left Page -->
      <line x1="-92" y1="-14" x2="-20" y2="-9" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" />
      <line x1="-96" y1="4" x2="-20" y2="9" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" />
      <line x1="-92" y1="22" x2="-20" y2="27" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" />

      <!-- Ruling Lines Right Page -->
      <line x1="20" y1="-9" x2="92" y2="-14" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" />
      <line x1="20" y1="9" x2="96" y2="4" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" />
      <line x1="20" y1="27" x2="92" y2="22" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" />

      <!-- Golden Bookmark Ribbon -->
      <path d="M-4,-36 Q-2,8 6,76 L18,84 L14,72 Q3,8 4,-36 Z" fill="#d97706" stroke="#b45309" stroke-width="1" />
    </g>

    <!-- Bold Arabic Headline: "صحيح مسلم" -->
    <text x="256" y="340" text-anchor="middle" class="ar-avatar" font-size="44" fill="url(#avGold)">صَحِيحُ مُسْلِمٍ</text>

    <!-- English/Malay Sub-title: "SAHIH MUSLIM" -->
    <text x="256" y="380" text-anchor="middle" class="latin-avatar" font-size="16.5" fill="#f8fafc" letter-spacing="3.5">SAHIH MUSLIM</text>

    <!-- Bottom Organization Arc Pill -->
    <g transform="translate(256, 422)">
      <rect x="-115" y="-14" width="230" height="28" rx="8" fill="#082f49" stroke="#38bdf8" stroke-width="1.2" />
      <circle cx="-95" cy="0" r="2.5" fill="#fbbf24" />
      <circle cx="95" cy="0" r="2.5" fill="#fbbf24" />
      <text x="0" y="5" text-anchor="middle" class="latin-avatar" font-size="11" fill="#38bdf8" letter-spacing="2">MAKTABAH MAFTOOHAH</text>
    </g>
  </g>
</svg>'''


# ==============================================================================
# 3. BUILD ASSETS/LOGO.SVG (800x200 Horizontal Lockup)
# ==============================================================================
def build_logo_horizontal_svg() -> str:
    logo_mark_inner = build_logo_mark_svg()
    idx = logo_mark_inner.find("<svg")
    inner_svg = logo_mark_inner[idx:]

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 200" width="800" height="200">
  <defs>
    <linearGradient id="logoCardBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0c2340" />
      <stop offset="50%" stop-color="#081728" />
      <stop offset="100%" stop-color="#020912" />
    </linearGradient>

    <linearGradient id="goldHdr" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fef3c7" />
      <stop offset="40%" stop-color="#f59e0b" />
      <stop offset="100%" stop-color="#d97706" />
    </linearGradient>

    <style>
      @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@700&amp;family=Inter:wght@400;600;700;800&amp;display=swap');
      .ar-hdr {{ font-family: 'Amiri', 'Traditional Arabic', serif; font-weight: 700; }}
      .latin-title {{ font-family: 'Inter', -apple-system, sans-serif; font-weight: 800; }}
      .latin-sub {{ font-family: 'Inter', -apple-system, sans-serif; font-weight: 600; }}
    </style>
  </defs>

  <!-- Container Box -->
  <rect width="800" height="200" rx="28" fill="url(#logoCardBg)" />
  <rect width="794" height="194" x="3" y="3" rx="25" fill="none" stroke="url(#goldHdr)" stroke-width="1.5" stroke-opacity="0.4" />

  <!-- Left: Emblem Mark (160x160 at x=20, y=20) -->
  <g transform="translate(20, 20)">
    <svg width="160" height="160" viewBox="0 0 512 512">
      {inner_svg}
    </svg>
  </g>

  <!-- Vertical Divider Line -->
  <line x1="205" y1="35" x2="205" y2="165" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1.5" />
  <circle cx="205" cy="100" r="3.5" fill="#f59e0b" />

  <!-- Right: Typography Lockup -->
  <!-- Arabic Calligraphy Headline: "صحيح مسلم" -->
  <text x="235" y="72" class="ar-hdr" font-size="40" fill="url(#goldHdr)" letter-spacing="1">صَحِيحُ مُسْلِمٍ</text>

  <!-- Latin Main Title: "Sahih Muslim" -->
  <text x="235" y="124" class="latin-title" font-size="44" fill="#ffffff">Sahih Muslim</text>

  <!-- Bottom Brand Row / Pill -->
  <g transform="translate(235, 144)">
    <rect x="0" y="0" width="195" height="26" rx="6" fill="rgba(2, 132, 199, 0.18)" stroke="rgba(56, 189, 248, 0.4)" stroke-width="1" />
    <text x="10" y="18" class="latin-sub" font-size="12.5" fill="#38bdf8" letter-spacing="1.5">MAKTABAH MAFTOOHAH</text>
    <text x="210" y="18" class="latin-sub" font-size="13" fill="#94a3b8">• Koleksi Hadis Autentik Digital (57 Kitab, 7,563 Hadis)</text>
  </g>
</svg>'''


# ==============================================================================
# 4. BUILD ASSETS/SITE-BANNER.SVG (1280x640 GitHub Social Preview & OG Banner)
# ==============================================================================
def build_site_banner_svg() -> str:
    logo_mark_inner = build_logo_mark_svg()
    idx = logo_mark_inner.find("<svg")
    inner_svg = logo_mark_inner[idx:]

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 640" width="1280" height="640">
  <defs>
    <!-- Master Background Radial -->
    <radialGradient id="bannerBg" cx="30%" cy="40%" r="85%">
      <stop offset="0%" stop-color="#0c2340" />
      <stop offset="45%" stop-color="#081728" />
      <stop offset="100%" stop-color="#020912" />
    </radialGradient>

    <!-- Gold Foil Gradient -->
    <linearGradient id="goldText" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fef9c3" />
      <stop offset="25%" stop-color="#fef08a" />
      <stop offset="50%" stop-color="#f59e0b" />
      <stop offset="75%" stop-color="#d97706" />
      <stop offset="100%" stop-color="#92400e" />
    </linearGradient>

    <!-- Ambient Sapphire Glow -->
    <radialGradient id="sapphireSpot" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#0284c7" stop-opacity="0.32" />
      <stop offset="70%" stop-color="#0369a1" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#0c2340" stop-opacity="0" />
    </radialGradient>

    <style>
      @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@700&amp;family=Inter:wght@400;500;600;700;800;900&amp;display=swap');
      .ar-banner {{ font-family: 'Amiri', 'Traditional Arabic', serif; font-weight: 700; }}
      .latin-bold {{ font-family: 'Inter', -apple-system, sans-serif; font-weight: 800; }}
      .latin-semi {{ font-family: 'Inter', -apple-system, sans-serif; font-weight: 600; }}
      .latin-reg {{ font-family: 'Inter', -apple-system, sans-serif; font-weight: 400; }}
    </style>
  </defs>

  <!-- Background Base -->
  <rect width="1280" height="640" fill="url(#bannerBg)" />

  <!-- Double Golden Precision Border -->
  <rect width="1248" height="608" x="16" y="16" rx="28" fill="none" stroke="url(#goldText)" stroke-width="2.5" stroke-opacity="0.65" />
  <rect width="1228" height="588" x="26" y="26" rx="20" fill="none" stroke="#38bdf8" stroke-width="1" stroke-opacity="0.35" stroke-dasharray="10 6" />

  <!-- Background Islamic Arabesque Geometry Accent -->
  <g transform="translate(1080, 320)" opacity="0.1" stroke="url(#goldText)" stroke-width="2" fill="none">
    <rect x="-240" y="-240" width="480" height="480" rx="40" />
    <rect x="-240" y="-240" width="480" height="480" rx="40" transform="rotate(45)" />
    <circle r="260" stroke="#38bdf8" stroke-width="2" />
    <circle r="180" stroke="url(#goldText)" stroke-width="1.5" stroke-dasharray="8 8" />
  </g>

  <!-- Left: Emblem Container -->
  <circle cx="280" cy="320" r="210" fill="url(#sapphireSpot)" />
  <g transform="translate(100, 140)">
    <svg width="360" height="360" viewBox="0 0 512 512">
      {inner_svg}
    </svg>
  </g>

  <!-- Center-Right: Typography & Presentation -->
  <g transform="translate(510, 150)">
    <!-- Organization Top Badge -->
    <g transform="translate(0, 0)">
      <rect width="265" height="32" rx="8" fill="#082f49" stroke="#38bdf8" stroke-width="1.2" />
      <circle cx="16" cy="16" r="3.5" fill="#fbbf24" />
      <text x="32" y="21" class="latin-semi" font-size="13" fill="#38bdf8" letter-spacing="2">MAKTABAH MAFTOOHAH</text>
    </g>

    <!-- Arabic Inscription: "صحيح مسلم" -->
    <text x="0" y="105" class="ar-banner" font-size="64" fill="url(#goldText)" letter-spacing="1">صَحِيحُ مُسْلِمٍ</text>

    <!-- English/Latin Main Headline -->
    <text x="0" y="175" class="latin-bold" font-size="54" fill="#ffffff" letter-spacing="-0.5">Sahih Muslim</text>

    <!-- Subtitle / Full Book Title -->
    <text x="0" y="218" class="latin-semi" font-size="19" fill="#93c5fd">
      Al-Musnad al-Sahih al-Mukhtasar min al-Sunan
    </text>

    <!-- Feature Description -->
    <text x="0" y="260" class="latin-reg" font-size="16" fill="#cbd5e1" line-height="1.6">
      Koleksi Lengkap 57 Kitab &amp; 7,563 Hadis • Teks Arab Berbaris Penuh (Tashkeel)
    </text>
    <text x="0" y="288" class="latin-reg" font-size="16" fill="#94a3b8">
      Terjemahan Melayu &amp; Inggeris • Sanad &amp; Matn • Carian Pantas Luar Talian (PWA)
    </text>

    <!-- Badges Row -->
    <g transform="translate(0, 325)">
      <!-- Badge 1: 57 Kitab -->
      <rect x="0" y="0" width="110" height="34" rx="8" fill="rgba(56, 189, 248, 0.15)" stroke="rgba(56, 189, 248, 0.4)" stroke-width="1" />
      <text x="55" y="22" text-anchor="middle" class="latin-semi" font-size="13.5" fill="#38bdf8">57 Kitab</text>

      <!-- Badge 2: 7,563 Hadis -->
      <rect x="120" y="0" width="130" height="34" rx="8" fill="rgba(245, 158, 11, 0.15)" stroke="rgba(245, 158, 11, 0.4)" stroke-width="1" />
      <text x="185" y="22" text-anchor="middle" class="latin-semi" font-size="13.5" fill="#fbbf24">7,563 Hadis</text>

      <!-- Badge 3: 100% Sahih -->
      <rect x="260" y="0" width="125" height="34" rx="8" fill="rgba(16, 185, 129, 0.15)" stroke="rgba(16, 185, 129, 0.4)" stroke-width="1" />
      <text x="322" y="22" text-anchor="middle" class="latin-semi" font-size="13.5" fill="#34d399">100% Sahih</text>

      <!-- Badge 4: Zero-Build PWA -->
      <rect x="395" y="0" width="150" height="34" rx="8" fill="rgba(255, 255, 255, 0.08)" stroke="rgba(255, 255, 255, 0.2)" stroke-width="1" />
      <text x="470" y="22" text-anchor="middle" class="latin-semi" font-size="13.5" fill="#e2e8f0">Zero-Build PWA</text>
    </g>
  </g>
</svg>'''


# ==============================================================================
# 5. RENDER RASTER ASSETS VIA PLAYWRIGHT
# ==============================================================================
def render_with_playwright(tasks: list[dict]):
    print(f"=== Step 2: Rendering {len(tasks)} Raster Assets via Headless Chrome ===")
    
    tasks_json = json.dumps(tasks)
    chrome_path = CHROME_EXEC.replace("\\", "/")
    playwright_dir = PLAYWRIGHT_DIR.replace("\\", "/")

    script_content = f"""
const {{ chromium }} = require('{playwright_dir}/playwright');
const tasks = {tasks_json};

(async () => {{
  const browser = await chromium.launch({{
    executablePath: '{chrome_path}'
  }});

  for (const t of tasks) {{
    console.log(`Rendering ${{t.output}} (${{t.width}}x${{t.height}})...`);
    const page = await browser.newPage({{
      viewport: {{ width: t.width, height: t.height }},
      deviceScaleFactor: t.scale || 1
    }});
    
    await page.goto('file:///' + t.input);
    await page.waitForTimeout(400); // Allow web fonts to render
    
    const opts = {{ path: t.output }};
    if (t.type === 'jpeg') {{
      opts.type = 'jpeg';
      opts.quality = t.quality || 95;
    }}
    await page.screenshot(opts);
    await page.close();
  }}

  await browser.close();
  console.log('All Playwright rendering finished successfully!');
}})();
"""
    tmp_js = ROOT / "scripts" / ".render_tmp.cjs"
    tmp_js.write_text(script_content, encoding="utf-8")
    
    try:
        res = subprocess.run(["node", str(tmp_js)], capture_output=True, text=True, check=True)
        print(res.stdout)
    except subprocess.CalledProcessError as e:
        print("Node STDERR:", e.stderr)
        print("Node STDOUT:", e.stdout)
        raise
    finally:
        if tmp_js.exists():
            tmp_js.unlink()


def main():
    print("=== Step 1: Generating High-Precision Vector SVG Assets ===")

    # 1. assets/logo-mark.svg
    logo_mark_svg = build_logo_mark_svg()
    (ASSETS / "logo-mark.svg").write_text(logo_mark_svg, encoding="utf-8")
    print("  • Generated assets/logo-mark.svg (512x512)")

    # 2. assets/github-avatar.svg
    github_avatar_svg = build_github_avatar_svg()
    (ASSETS / "github-avatar.svg").write_text(github_avatar_svg, encoding="utf-8")
    print("  • Generated assets/github-avatar.svg (512x512 Circle-Safe)")

    # 3. assets/logo.svg
    logo_svg = build_logo_horizontal_svg()
    (ASSETS / "logo.svg").write_text(logo_svg, encoding="utf-8")
    print("  • Generated assets/logo.svg (800x200)")

    # 4. assets/site-banner.svg
    site_banner_svg = build_site_banner_svg()
    (ASSETS / "site-banner.svg").write_text(site_banner_svg, encoding="utf-8")
    print("  • Generated assets/site-banner.svg (1280x640)")

    # Step 2: Render raster PNGs and JPGs
    render_tasks = [
        # Logo mark PNG
        {
            "input": str(ASSETS / "logo-mark.svg"),
            "output": str(ASSETS / "logo-mark.png"),
            "width": 512,
            "height": 512,
            "scale": 1
        },
        # GitHub Avatar PNG (512x512)
        {
            "input": str(ASSETS / "github-avatar.svg"),
            "output": str(ASSETS / "github-avatar.png"),
            "width": 512,
            "height": 512,
            "scale": 1
        },
        # Avatar PNG alias
        {
            "input": str(ASSETS / "github-avatar.svg"),
            "output": str(ASSETS / "avatar.png"),
            "width": 512,
            "height": 512,
            "scale": 1
        },
        # PWA Icons
        {
            "input": str(ASSETS / "logo-mark.svg"),
            "output": str(ASSETS / "icon-192.png"),
            "width": 192,
            "height": 192,
            "scale": 1
        },
        {
            "input": str(ASSETS / "logo-mark.svg"),
            "output": str(ASSETS / "icon-512.png"),
            "width": 512,
            "height": 512,
            "scale": 1
        },
        # Horizontal Logo (1600x400 Retina)
        {
            "input": str(ASSETS / "logo.svg"),
            "output": str(ASSETS / "logo.png"),
            "width": 800,
            "height": 200,
            "scale": 2
        },
        # GitHub Site Banner (2560x1280 Retina)
        {
            "input": str(ASSETS / "site-banner.svg"),
            "output": str(ASSETS / "site-banner.png"),
            "width": 1280,
            "height": 640,
            "scale": 2
        },
        # Open Graph Banner (1280x640 JPEG)
        {
            "input": str(ASSETS / "site-banner.svg"),
            "output": str(ASSETS / "og-banner.jpg"),
            "width": 1280,
            "height": 640,
            "scale": 1,
            "type": "jpeg",
            "quality": 95
        }
    ]

    render_with_playwright(render_tasks)

    # Also update root icon.svg to match logo-mark.svg
    (ROOT / "icon.svg").write_text(logo_mark_svg, encoding="utf-8")
    print("  • Synchronized root icon.svg with latest emblem")

    print("\n>>> ALL BRANDING ASSETS SUCCESSFULLY GENERATED FOR SAHIH MUSLIM! <<<")

if __name__ == "__main__":
    main()
