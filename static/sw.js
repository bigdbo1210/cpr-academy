/* DBO CPR service worker — installability + fast static assets.
   Pages and student data are always network-first: course content,
   enrollments and account pages must never be served stale. */
const CACHE = "dbo-cpr-v4";
const STATIC_PATHS = ["/static/icons/", "/static/img/"];

self.addEventListener("install", (event) => {
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  if (event.request.method !== "GET" || url.origin !== self.location.origin) return;

  if (STATIC_PATHS.some((p) => url.pathname.startsWith(p))) {
    // Cache-first for brand/static assets.
    event.respondWith(
      caches.open(CACHE).then((cache) =>
        cache.match(event.request).then((hit) => {
          const fetchPromise = fetch(event.request).then((res) => {
            if (res.ok) cache.put(event.request, res.clone());
            return res;
          });
          return hit || fetchPromise;
        })
      )
    );
    return;
  }

  // Network-first for everything else; fall back to cache, then a simple
  // offline notice for page navigations.
  event.respondWith(
    fetch(event.request)
      .then((res) => {
        if (res.ok && url.pathname === "/") {
          const copy = res.clone();
          caches.open(CACHE).then((cache) => cache.put(event.request, copy));
        }
        return res;
      })
      .catch(() =>
        caches.match(event.request).then((hit) => {
          if (hit) return hit;
          if (event.request.mode === "navigate") {
            return new Response(
              "<h1>You're offline</h1><p>Don't Be Ordinary CPR needs a connection for classes and sign-ups. Reconnect and refresh.</p>",
              { headers: { "Content-Type": "text/html" } }
            );
          }
          throw new Error("offline");
        })
      )
  );
});
