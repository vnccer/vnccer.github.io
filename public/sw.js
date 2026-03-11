const cacheName = self.location.pathname
const pages = [

  "/docs/",
  "/posts/creating-a-new-theme/",
  "/posts/migrate-from-jekyll/",
  "/docs/cybersecurity/",
  "/posts/goisforlovers/",
  "/categories/",
  "/categories/Development/",
  "/tags/development/",
  "/posts/hugoisforlovers/",
  "/tags/go/",
  "/categories/golang/",
  "/tags/golang/",
  "/tags/hugo/",
  "/tags/",
  "/tags/templates/",
  "/tags/themes/",
  "/docs/ai/",
  "/docs/life/",
  "/docs/papers/",
  "/docs/skills/",
  "/docs/work/",
  "/posts/",
  "/showcases/",
  "/",
  "/book.min.cc3274658ef63c668ab9aef1ce1b3b54f9843bd31db13dd4ae7b1c30105950a0.css",
  "/zh.search-data.min.7a454bc21ade30b668743c99d6a957f49619f72fdd46ebfb969b5b299737af0c.json",
  "/zh.search.min.7e0e41d7f96fb3fa551ff612eb981f7c2ba38cafda5307d0c2d8a3e4c3ceabe8.js",
  
];

self.addEventListener("install", function (event) {
  self.skipWaiting();

  caches.open(cacheName).then((cache) => {
    return cache.addAll(pages);
  });
});

self.addEventListener("fetch", (event) => {
  const request = event.request;
  if (request.method !== "GET") {
    return;
  }

  /**
   * @param {Response} response
   * @returns {Promise<Response>}
   */
  function saveToCache(response) {
    if (cacheable(response)) {
      return caches
        .open(cacheName)
        .then((cache) => cache.put(request, response.clone()))
        .then(() => response);
    } else {
      return response;
    }
  }

  /**
   * @param {Error} error
   */
  function serveFromCache(error) {
    return caches.open(cacheName).then((cache) => cache.match(request.url));
  }

  /**
   * @param {Response} response
   * @returns {Boolean}
   */
  function cacheable(response) {
    return response.type === "basic" && response.ok && !response.headers.has("Content-Disposition")
  }

  event.respondWith(fetch(request).then(saveToCache).catch(serveFromCache));
});
