const CACHE_NAME = 'serenity-v1';
const ASSETS_TO_CACHE = [
    '/',
    '/static/css/style.css',
    '/static/js/main.js',
    '/static/js/accessibility.js',
    '/support'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(ASSETS_TO_CACHE);
        })
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        }).catch(() => {
            if (event.request.mode === 'navigate') {
                return caches.match('/support');
            }
        })
    );
});
