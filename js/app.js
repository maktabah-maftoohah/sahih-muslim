/**
 * Maktabah Maftoohah Sahih Muslim - Reader Application
 * Zero-Build Vanilla ES6 Architecture & Offline PWA
 */

import { analytics } from './analytics.js';

class MuslimReader {
  constructor() {
    this.currentLang = 'ms'; // Default Nusantara Malay
    this.currentBook = 1;
    this.books = [];
    this.hadiths = [];
    this.searchQuery = '';

    this.contentView = document.getElementById('contentView');
    this.langToggle = document.getElementById('langToggle');
    this.themeToggle = document.getElementById('themeToggle');
  }

  async init() {
    analytics.init();
    this.registerServiceWorker();

    // Parse language from URL params or search links (?lang=en or ?lang=ms)
    if (window.location.search) {
      const sp = new URLSearchParams(window.location.search);
      const urlLang = sp.get('lang');
      if (urlLang === 'en' || urlLang === 'ms') {
        this.currentLang = urlLang;
      }
    }
    if (this.langToggle) {
      this.langToggle.textContent = this.currentLang === 'ms' ? 'MY' : 'EN';
    }

    this.setupEventListeners();
    await this.loadBooks();
    await this.handleRouting();
    window.addEventListener('hashchange', () => this.handleRouting());
    window.addEventListener('popstate', () => this.handleRouting());
  }

  parseRoute() {
    // 1. Check path e.g. /sahih-muslim/42 or /42
    const pathname = window.location.pathname;
    let sub = pathname;
    if (sub.startsWith('/sahih-muslim')) {
      sub = sub.slice('/sahih-muslim'.length);
    }
    sub = sub.replace(/^\/+|\/+$/g, '');
    if (sub && sub !== 'index.html' && sub !== '404.html') {
      const pathMatch = sub.match(/^(?:hadith\/|h\/)?(\d+(?:\.\d+)?)$/i);
      if (pathMatch) {
        return { type: 'hadith', number: parseFloat(pathMatch[1]) };
      }
    }

    // 2. Check hash e.g. #hadith/42, #42, #muslim:42, #book/2
    const hash = window.location.hash.slice(1);
    if (hash) {
      const hadithHash = hash.match(/^(?:hadith\/|h\/|muslim:)?(\d+(?:\.\d+)?)$/i);
      if (hadithHash) {
        return { type: 'hadith', number: parseFloat(hadithHash[1]) };
      }
      const bookHash = hash.match(/^book\/(\d+)(?:\/(\d+))?$/i);
      if (bookHash) {
        return { type: 'book', book: parseInt(bookHash[1], 10), inBook: bookHash[2] ? parseInt(bookHash[2], 10) : null };
      }
    }

    // 3. Check query param e.g. ?hadith=42, ?h=42
    if (window.location.search) {
      const sp = new URLSearchParams(window.location.search);
      const h = sp.get('hadith') || sp.get('h');
      if (h) {
        return { type: 'hadith', number: parseFloat(h) };
      }
      const b = sp.get('book') || sp.get('b');
      if (b) {
        return { type: 'book', book: parseInt(b, 10) };
      }
    }

    return null;
  }

  async handleRouting() {
    const route = this.parseRoute();
    if (route && route.type === 'hadith') {
      const targetHadith = route.number;
      const targetBook = this.books.find(b => targetHadith >= b.hadith_start && targetHadith <= b.hadith_end) || this.books[0];
      const bookNum = targetBook ? targetBook.book_number : 1;
      this.currentBook = bookNum;
      await this.loadHadiths(bookNum);
      this.scrollToHadith(targetHadith);
    } else if (route && route.type === 'book') {
      this.currentBook = route.book;
      await this.loadHadiths(route.book);
    } else {
      await this.loadHadiths(this.currentBook);
    }
  }

  scrollToHadith(hadithNum) {
    const normalized = Number.isInteger(hadithNum) ? hadithNum : hadithNum;
    setTimeout(() => {
      const el = document.getElementById(`hadith-${normalized}`);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        el.classList.add('highlight-target');
        setTimeout(() => el.classList.remove('highlight-target'), 2600);
      }
    }, 200);

    // Update document title dynamically
    const bookObj = this.books.find(b => b.book_number === this.currentBook);
    const bookTitle = bookObj ? (this.currentLang === 'ms' ? bookObj.title_ms : bookObj.title_en) : '';
    document.title = `Sahih Muslim #${hadithNum} (${bookTitle}) — Maktabah Maftoohah`;

    // Reflect clean deep link in URL
    const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
    const basePath = window.location.pathname.startsWith('/sahih-muslim') ? '/sahih-muslim/' : './';
    if (!isLocal) {
      window.history.replaceState(null, '', `${basePath}${normalized}`);
    } else {
      window.history.replaceState(null, '', `#hadith/${normalized}`);
    }
  }

  registerServiceWorker() {
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('./sw.js').then(
          (reg) => console.log('Muslim PWA ServiceWorker registered:', reg.scope),
          (err) => console.warn('Muslim PWA ServiceWorker registration failed:', err)
        );
      });
    }
  }

  setupEventListeners() {
    if (this.themeToggle) {
      this.themeToggle.addEventListener('click', () => {
        const isDark = document.body.getAttribute('data-theme') === 'dark';
        document.body.setAttribute('data-theme', isDark ? 'light' : 'dark');
        this.themeToggle.textContent = isDark ? '🌙' : '☀️';
      });
    }

    if (this.langToggle) {
      this.langToggle.addEventListener('click', () => {
        this.currentLang = this.currentLang === 'ms' ? 'en' : 'ms';
        this.langToggle.textContent = this.currentLang === 'ms' ? 'MY' : 'EN';
        this.render();
      });
    }

    const docsToggle = document.getElementById('docsToggle');
    const docsModal = document.getElementById('docsModal');
    const closeDocsModal = document.getElementById('closeDocsModal');

    if (docsToggle && docsModal) {
      docsToggle.addEventListener('click', () => docsModal.showModal());
    }
    if (closeDocsModal && docsModal) {
      closeDocsModal.addEventListener('click', () => docsModal.close());
      docsModal.addEventListener('click', (e) => {
        if (e.target === docsModal) docsModal.close();
      });
    }

    // Direct Link Copy Event Listener
    document.addEventListener('click', async (e) => {
      const btn = e.target.closest('.btn-copy-link');
      if (btn) {
        const num = btn.getAttribute('data-hadith-num');
        const permalink = `https://maktabah-maftoohah.github.io/sahih-muslim/${num}`;
        try {
          await navigator.clipboard.writeText(permalink);
          const span = btn.querySelector('.copy-text');
          const original = span ? span.textContent : '';
          btn.classList.add('copied');
          if (span) span.textContent = this.currentLang === 'ms' ? 'Disalin!' : 'Copied!';
          setTimeout(() => {
            btn.classList.remove('copied');
            if (span) span.textContent = original;
          }, 2000);
        } catch (err) {
          console.warn('Clipboard write failed:', err);
          prompt(this.currentLang === 'ms' ? 'Salin pautan hadis ini:' : 'Copy this hadith link:', permalink);
        }
      }
    });
  }

  async loadBooks() {
    try {
      const res = await fetch('./data/books.json');
      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
      this.books = await res.json();
    } catch (e) {
      console.error('Failed to load books catalogue:', e);
      this.books = [];
    }
  }

  async loadHadiths(bookNumber) {
    this.contentView.innerHTML = '<p class="loading-state">Memuatkan hadis...</p>';
    const padded = String(bookNumber).padStart(2, '0');
    try {
      const res = await fetch(`./data/hadiths/${padded}.json`);
      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
      this.hadiths = await res.json();
      this.searchQuery = '';
      this.render();
    } catch (e) {
      console.warn(`Book ${bookNumber} not yet seeded:`, e);
      this.hadiths = [];
      this.renderUnseeded(bookNumber);
    }
  }

  renderUnseeded(bookNumber) {
    const book = this.books.find(b => b.book_number === bookNumber) || {};
    const title = this.currentLang === 'ms' ? (book.title_ms || book.title_ar) : (book.title_en || book.title_ar);
    this.contentView.innerHTML = `
      <div class="hadith-card" style="text-align: center; padding: 3rem 1rem;">
        <h3 style="margin-bottom: 0.5rem;">${title} (${book.title_ar || ''})</h3>
        <p style="color: var(--text-muted); margin-bottom: 1.5rem;">
          ${this.currentLang === 'ms' 
            ? 'Kitab ini dalam perancangan penyusunan dan pengesahan teks autentik.' 
            : 'This book is scheduled for text verification and ingestion.'}
        </p>
        <button class="btn-pill" id="backToBook1">
          ${this.currentLang === 'ms' ? 'Kembali ke Kitab 1 (Iman)' : 'Return to Book 1 (Faith)'}
        </button>
      </div>
    `;
    const btn = document.getElementById('backToBook1');
    if (btn) {
      btn.addEventListener('click', () => {
        this.currentBook = 1;
        const selector = document.getElementById('bookSelector');
        if (selector) selector.value = '1';
        this.loadHadiths(1);
      });
    }
  }

  getFilteredHadiths() {
    if (!this.searchQuery.trim()) {
      return this.hadiths;
    }
    const q = this.searchQuery.toLowerCase().trim();
    return this.hadiths.filter(h => {
      const numMatch = String(h.hadith_number).includes(q) || String(h.in_book_number).includes(q);
      const arMatch = (h.arabic || '').includes(q);
      const msMatch = (h.translations?.ms || '').toLowerCase().includes(q);
      const enMatch = (h.translations?.en || '').toLowerCase().includes(q);
      const tagMatch = (h.tags || []).some(t => t.toLowerCase().includes(q));
      return numMatch || arMatch || msMatch || enMatch || tagMatch;
    });
  }

  render() {
    const currentBookObj = this.books.find(b => b.book_number === this.currentBook) || {};
    const bookTitle = this.currentLang === 'ms' 
      ? (currentBookObj.title_ms || currentBookObj.title_ar) 
      : (currentBookObj.title_en || currentBookObj.title_ar);

    const filtered = this.getFilteredHadiths();

    // Book Selector & Search Control
    const controlsHtml = `
      <div class="hero-section">
        <div class="book-control-row">
          <label for="bookSelector" style="font-weight: 600;">
            ${this.currentLang === 'ms' ? 'Pilih Kitab:' : 'Select Book:'}
          </label>
          <select id="bookSelector" class="book-select">
            ${this.books.map(b => {
              const bName = this.currentLang === 'ms' ? b.title_ms : b.title_en;
              return `<option value="${b.book_number}" ${b.book_number === this.currentBook ? 'selected' : ''}>
                ${b.book_number}. ${bName} (${b.title_ar})
              </option>`;
            }).join('')}
          </select>
          <div class="book-meta">
            <span class="badge">${filtered.length} / ${this.hadiths.length} ${this.currentLang === 'ms' ? 'Hadis' : 'Hadiths'}</span>
            <span class="badge badge-sahih">Sahih Muslim</span>
          </div>
        </div>

        <div class="search-control-row">
          <input 
            type="search" 
            id="hadithSearch" 
            class="search-input" 
            placeholder="${this.currentLang === 'ms' ? 'Cari hadis mengikut nombor, kata kunci, atau tema...' : 'Search hadith by number, keyword, or topic...'}"
            value="${this.searchQuery}"
          />
        </div>
      </div>
    `;

    // Hadith Cards List
    const hadithListHtml = filtered.length > 0 ? `
      <div class="hadith-list">
        ${filtered.map(h => this.renderHadithCard(h)).join('')}
      </div>
    ` : `
      <div class="hadith-card" style="text-align: center; padding: 2rem;">
        <p style="color: var(--text-muted);">
          ${this.currentLang === 'ms' ? 'Tiada hadis sepadan dengan carian.' : 'No hadiths found matching your search.'}
        </p>
      </div>
    `;

    this.contentView.innerHTML = controlsHtml + hadithListHtml;

    // Attach event listeners
    const selector = document.getElementById('bookSelector');
    if (selector) {
      selector.addEventListener('change', (e) => {
        this.currentBook = parseInt(e.target.value, 10);
        this.loadHadiths(this.currentBook);
      });
    }

    const searchInput = document.getElementById('hadithSearch');
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        this.searchQuery = e.target.value;
        const listContainer = document.querySelector('.hadith-list') || this.contentView;
        const updated = this.getFilteredHadiths();
        if (document.querySelector('.hadith-list')) {
          document.querySelector('.hadith-list').innerHTML = updated.length > 0 
            ? updated.map(h => this.renderHadithCard(h)).join('')
            : `<div class="hadith-card" style="text-align: center; padding: 2rem;"><p style="color: var(--text-muted);">${this.currentLang === 'ms' ? 'Tiada hadis sepadan.' : 'No matching hadiths.'}</p></div>`;
        }
      });
    }
  }

  formatTranslation(trans, crossRefs = []) {
    if (!trans) return '';
    let formatted = trans;

    const quranRefs = crossRefs.filter(cr => cr.type === 'quran');
    if (quranRefs.length > 0) {
      quranRefs.forEach(cr => {
        const url = cr.url || `https://maktabah-maftoohah.github.io/al-quran/${cr.surah}/${cr.ayah}`;
        const label = cr.surah_name ? `Surah ${cr.surah_name} (${cr.surah}:${cr.ayah})` : `Surah ${cr.surah}:${cr.ayah}`;

        // 1. English patterns: (V. s:a), (s:a), (s.a)
        const enPattern = new RegExp(`\\((?:V\\.?\\s*)?${cr.surah}[:.]${cr.ayah}\\)`, 'gi');
        formatted = formatted.replace(enPattern, (match) => {
          return `<a href="${url}" class="quran-inline-link" target="_blank" rel="noopener" title="${this.currentLang === 'ms' ? `Buka ${label} dalam Al-Quran Digital` : `Open ${label} in Digital Quran`}">${match} ↗</a>`;
        });

        // 2. Malay/Indonesian patterns: (QS. Name: Ayah) or (As. Name: Ayah)
        if (cr.surah_name) {
          const escapedName = cr.surah_name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&').replace(/[-']/g, '[\\s\\-\']?');
          const msPattern = new RegExp(`\\((?:QS\\.?|Qs\\.?|Surat|Surah|As\\.)\\s*${escapedName}\\s*(?:[:.,]|ayat)?\\s*${cr.ayah}\\)`, 'gi');
          formatted = formatted.replace(msPattern, (match) => {
            return `<a href="${url}" class="quran-inline-link" target="_blank" rel="noopener" title="${this.currentLang === 'ms' ? `Buka ${label} dalam Al-Quran Digital` : `Open ${label} in Digital Quran`}">${match} ↗</a>`;
          });
        }
      });
    }

    return formatted;
  }

  renderHadithCard(hadith) {
    const rawTrans = hadith.translations?.[this.currentLang] || hadith.translations?.ms || '';
    const formattedTrans = this.formatTranslation(rawTrans, hadith.cross_references || []);
    const grade = hadith.gradings?.[0]?.grade || 'Sahih';
    const gradeAr = hadith.gradings?.[0]?.grade_ar || 'صحيح';

    const crossRefsHtml = (hadith.cross_references || []).map(cr => {
      if (cr.type === 'quran') {
        const quranUrl = cr.url || `https://maktabah-maftoohah.github.io/al-quran/${cr.surah}/${cr.ayah}`;
        const label = cr.surah_name ? `Surah ${cr.surah_name} (${cr.surah}:${cr.ayah})` : `Surah ${cr.surah}:${cr.ayah}`;
        return `<a href="${quranUrl}" class="badge badge-crossref" target="_blank" rel="noopener" title="${this.currentLang === 'ms' ? `Buka ${label} dalam Al-Quran Digital` : `Open ${label} in Digital Quran`}">📖 ${label} ↗</a>`;
      }
      return '';
    }).join('');

    const isnadHtml = hadith.sanad && hadith.sanad.length > 0 ? `
      <div class="hadith-isnad-bar">
        <span class="isnad-label">${this.currentLang === 'ms' ? 'Rangkaian Sanad Perawi (Jarh wa Ta\'dil):' : 'Chain of Narrators (Jarh wa Ta\'dil):'}</span>
        <div class="isnad-tokens">
          ${hadith.sanad.map((r, idx) => `
            <a href="${r.profile_url || `https://maktabah-maftoohah.github.io/rijal-al-hadith/rawi/${r.narrator_id}/`}?lang=${this.currentLang}&ref=sahih-muslim:${hadith.hadith_number}"
               class="rawi-token tier-${r.reliability_level !== undefined ? r.reliability_level : 1}"
               target="_blank" rel="noopener"
               title="${r.narrator_name_ms || r.narrator_name_ar} (Klik untuk profil lengkap)">
              <span class="rawi-dot tier-${r.reliability_level !== undefined ? r.reliability_level : 1}"></span>
              <span>${this.currentLang === 'ar' ? r.narrator_name_ar : (r.narrator_name_ms || r.narrator_name_ar)}</span>
            </a>
            ${idx < hadith.sanad.length - 1 ? '<span class="sanad-arrow">←</span>' : ''}
          `).join('')}
        </div>
      </div>
    ` : '';

    return `
      <article class="hadith-card" id="hadith-${hadith.hadith_number}">
        <div class="hadith-meta-bar">
          <div class="hadith-num-group">
            <span class="badge" style="background: var(--primary); color: #fff;">
              # ${hadith.hadith_number}
            </span>
            <span class="badge">
              ${this.currentLang === 'ms' ? 'Kitab' : 'Book'} ${hadith.book_number} : ${hadith.in_book_number || '-'}
            </span>
            <button class="btn-copy-link" data-hadith-num="${hadith.hadith_number}" title="${this.currentLang === 'ms' ? 'Salin pautan terus hadis ini' : 'Copy direct link to this hadith'}">
              🔗 <span class="copy-text">${this.currentLang === 'ms' ? 'Salin Pautan' : 'Copy Link'}</span>
            </button>
          </div>
          <div>
            <span class="badge badge-sahih">${gradeAr} / ${grade}</span>
          </div>
        </div>

        <div class="hadith-arabic">
          ${hadith.sanad_text ? `<span class="arabic-sanad">${hadith.sanad_text} </span>` : ''}
          <span class="arabic-matn">${hadith.matn_text || hadith.arabic}</span>
        </div>

        ${isnadHtml}

        <div class="hadith-translation">
          ${formattedTrans}
        </div>

        <div class="hadith-footer">
          <div class="cross-ref-list">
            ${crossRefsHtml}
          </div>
          <div>
            ${hadith.tags ? hadith.tags.map(t => `<span style="margin-left: 0.25rem;">#${t}</span>`).join(' ') : ''}
          </div>
        </div>
      </article>
    `;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const reader = new MuslimReader();
  reader.init();
});
