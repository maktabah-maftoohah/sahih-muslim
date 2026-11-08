/**
 * Maktabah Maftoohah Sahih Muslim - Analytics Module (analytics.js)
 * Google Tag Manager (GTM) and Google Analytics 4 (GA4) integration
 * with SPA virtual pageview tracking and specialized Hadith metrics.
 * 
 * Invariants:
 * - Zero external build dependencies (Vanilla ES6).
 * - Offline-first resilient: fails silently when offline without throwing errors.
 * - Respects Do Not Track (DNT) header.
 * - Dual GTM dataLayer & gtag compatibility.
 */

const DEFAULT_CONTAINER_ID = 'GTM-XXXXXXXX';

class AnalyticsService {
  constructor() {
    this.initialized = false;
    this.containerId = null;
    this.lastTrackedPath = null;
  }

  getContainerId() {
    try {
      const stored = localStorage.getItem('maktabah_ga_id');
      if (stored && stored.trim()) return stored.trim();
    } catch {
      // ignore localStorage
    }
    return DEFAULT_CONTAINER_ID;
  }

  init(customId = null) {
    if (this.initialized) return;

    this.containerId = customId || this.getContainerId();

    if (!this.containerId || this.containerId === 'GTM-XXXXXXXX' || this.containerId === 'G-XXXXXXXXXX') {
      return;
    }

    if (typeof navigator !== 'undefined') {
      const dnt = navigator.doNotTrack || window.doNotTrack || navigator.msDoNotTrack;
      if (dnt === '1' || dnt === 'yes') {
        return;
      }
    }

    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function() {
      window.dataLayer.push(arguments);
    };

    const existingScript = document.querySelector('script[src*="googletagmanager.com/gtm.js"], script[src*="googletagmanager.com/gtag/js"]');

    if (!existingScript) {
      if (typeof navigator !== 'undefined' && !navigator.onLine) {
        if (typeof window !== 'undefined') {
          window.addEventListener('online', () => this.init(this.containerId), { once: true });
        }
        return;
      }

      try {
        const isGtm = this.containerId.startsWith('GTM-');
        const scriptUrl = isGtm
          ? `https://www.googletagmanager.com/gtm.js?id=${this.containerId}`
          : `https://www.googletagmanager.com/gtag/js?id=${this.containerId}`;

        if (!isGtm) {
          window.gtag('js', new Date());
          window.gtag('config', this.containerId, {
            send_page_view: false,
            anonymize_ip: true,
            cookie_flags: 'SameSite=None;Secure'
          });
        }

        const script = document.createElement('script');
        script.async = true;
        script.src = scriptUrl;
        script.onerror = () => {};
        document.head.appendChild(script);
      } catch {
        // Safe fail
      }
    }

    this.initialized = true;

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.trackCurrentRoute());
    } else {
      this.trackCurrentRoute();
    }
  }

  trackEvent(eventName, params = {}) {
    const payload = {
      ...params,
      app_name: 'Maktabah Maftoohah Sahih Muslim'
    };

    try {
      if (typeof window !== 'undefined' && Array.isArray(window.dataLayer)) {
        window.dataLayer.push({
          event: eventName,
          ...payload
        });
      }
    } catch {
      // Safe fail
    }

    if (typeof window !== 'undefined' && typeof window.gtag === 'function') {
      try {
        window.gtag('event', eventName, payload);
      } catch {
        // Safe fail
      }
    }
  }

  trackPageView(pagePath, pageTitle) {
    const path = pagePath || (window.location.pathname + (window.location.hash || ''));
    if (path === this.lastTrackedPath) return;
    this.lastTrackedPath = path;

    const title = pageTitle || document.title || 'Maktabah Maftoohah Sahih Muslim';
    const payload = {
      page_path: path,
      page_title: title,
      page_location: window.location.href,
      app_name: 'Maktabah Maftoohah Sahih Muslim'
    };

    try {
      if (typeof window !== 'undefined' && Array.isArray(window.dataLayer)) {
        window.dataLayer.push({
          event: 'page_view',
          ...payload
        });
      }
    } catch {
      // Safe fail
    }

    if (typeof window !== 'undefined' && typeof window.gtag === 'function') {
      try {
        window.gtag('event', 'page_view', payload);
      } catch {
        // Safe fail
      }
    }
  }

  trackCurrentRoute() {
    this.trackPageView(window.location.pathname + (window.location.hash || ''));
  }

  // Specialized Hadith Event Helpers
  trackHadithView(hadithNumber, bookNumber) {
    this.trackEvent('view_hadith', {
      hadith_number: Number(hadithNumber),
      book_number: Number(bookNumber)
    });
  }

  trackBookView(bookNumber, bookName) {
    this.trackEvent('view_book', {
      book_number: Number(bookNumber),
      book_name: bookName
    });
  }

  trackGradeFilter(grade, scholar) {
    this.trackEvent('filter_grade', {
      grade,
      scholar
    });
  }

  trackIsnadInspect(hadithNumber) {
    this.trackEvent('inspect_isnad', {
      hadith_number: Number(hadithNumber)
    });
  }
}

export const analytics = new AnalyticsService();
