const cacheName = self.location.pathname
const pages = [

  "/hugo-book/docs/example/",
  "/hugo-book/docs/example/table-of-contents/with-toc/",
  "/hugo-book/docs/example/table-of-contents/without-toc/",
  "/hugo-book/posts/creating-a-new-theme/",
  "/hugo-book/posts/migrate-from-jekyll/",
  "/hugo-book/docs/example/table-of-contents/",
  "/hugo-book/docs/example/collapsed/",
  "/hugo-book/",
  "/hugo-book/posts/",
  "/hugo-book/posts/goisforlovers/",
  "/hugo-book/categories/",
  "/hugo-book/categories/Development/",
  "/hugo-book/tags/development/",
  "/hugo-book/posts/hugoisforlovers/",
  "/hugo-book/tags/go/",
  "/hugo-book/categories/golang/",
  "/hugo-book/tags/golang/",
  "/hugo-book/tags/hugo/",
  "/hugo-book/tags/",
  "/hugo-book/tags/templates/",
  "/hugo-book/tags/themes/",
  "/hugo-book/docs/example/collapsed/3rd-level/4th-level/",
  "/hugo-book/docs/example/collapsed/3rd-level/",
  "/hugo-book/docs/example/hidden/",
  "/hugo-book/docs/shortcodes/",
  "/hugo-book/docs/shortcodes/buttons/",
  "/hugo-book/docs/shortcodes/columns/",
  "/hugo-book/docs/shortcodes/details/",
  "/hugo-book/docs/shortcodes/experimental/",
  "/hugo-book/docs/shortcodes/experimental/asciinema/",
  "/hugo-book/docs/shortcodes/experimental/badges/",
  "/hugo-book/docs/shortcodes/experimental/cards/",
  "/hugo-book/docs/shortcodes/experimental/images/",
  "/hugo-book/docs/shortcodes/hints/",
  "/hugo-book/docs/shortcodes/mermaid/",
  "/hugo-book/docs/shortcodes/section/",
  "/hugo-book/docs/shortcodes/section/first-page/",
  "/hugo-book/docs/shortcodes/section/second-page/",
  "/hugo-book/docs/shortcodes/steps/",
  "/hugo-book/docs/shortcodes/tabs/",
  "/hugo-book/docs/",
  "/hugo-book/docs/shortcodes/katex/",
  "/hugo-book/showcases/",
  "/hugo-book/book.min.6970156cec683193d93c9c4edaf0d56574e4361df2e0c1be4f697ae81c3ba55f.css",
  "/hugo-book/zh.search-data.min.53f72d1d5b4ab94d1f42cd484a7b62e835db207679cbc14214e311ddc40b8dc1.json",
  "/hugo-book/zh.search.min.1737c80f8992b7c5ecb235e0de29428ce6d9d4861ef69dc19f646c3d8d20e1a1.js",
  
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
