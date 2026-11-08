const CACHE_NAME = 'muslim-reader-v1';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './404.html',
  './css/main.css',
  './js/app.js',
  './js/analytics.js',
  './data/books.json',
  './data/collection.json',
  './data/chapters/00.json',
  './data/chapters/01.json',
  './data/hadiths/00.json',
  './data/hadiths/01.json',
  './manifest.webmanifest',
  './icon.svg'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS_TO_CACHE))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) return cachedResponse;
      return fetch(event.request).then((networkResponse) => {
        if (event.request.method === 'GET' && networkResponse && networkResponse.status === 200) {
          const clone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
        }
        return networkResponse;
      });
    }).catch(() => caches.match('./index.html'))
  );
});
