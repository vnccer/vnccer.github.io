const cacheName = self.location.pathname
const pages = [

  "/docs/example/",
  "/docs/example/table-of-contents/with-toc/",
  "/docs/example/table-of-contents/without-toc/",
  "/posts/creating-a-new-theme/",
  "/posts/migrate-from-jekyll/",
  "/docs/example/table-of-contents/",
  "/docs/example/collapsed/",
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
  "/docs/example/collapsed/3rd-level/4th-level/",
  "/docs/example/collapsed/3rd-level/",
  "/docs/example/hidden/",
  "/docs/shortcodes/",
  "/docs/shortcodes/buttons/",
  "/docs/shortcodes/columns/",
  "/docs/shortcodes/details/",
  "/docs/shortcodes/experimental/",
  "/docs/shortcodes/experimental/asciinema/",
  "/docs/shortcodes/experimental/badges/",
  "/docs/shortcodes/experimental/cards/",
  "/docs/shortcodes/experimental/images/",
  "/docs/shortcodes/hints/",
  "/docs/shortcodes/mermaid/",
  "/docs/shortcodes/section/",
  "/docs/shortcodes/section/first-page/",
  "/docs/shortcodes/section/second-page/",
  "/docs/shortcodes/steps/",
  "/docs/shortcodes/tabs/",
  "/posts/",
  "/docs/",
  "/docs/shortcodes/katex/",
  "/showcases/",
  "/",
  "/book.min.6daafd9a7cc5c1b1fced275c563f8aade2721b175e2be95ddb14d0b615a0d4a9.css",
  "/zh.search-data.min.f20a280e0057a031029eb37dbcedbd176d485099ca86a06987667c6e87a8922f.json",
  "/zh.search.min.75f131ff071a1581dfe22aa708b284d4b80a1fb6bb4fd417a211e3937c04be95.js",
  
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
