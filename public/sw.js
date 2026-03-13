const cacheName = self.location.pathname
const pages = [

  "/docs/cybersecurity/vulnhub/easy/vulnhub-beelzebub_1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub-empire_breakout/",
  "/docs/cybersecurity/vulnhub/medium/vulnhub-empire_lupinone/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub-ica_1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub-jangow_1.0.1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub-napping-1.0.1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub-noob_1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub-the-planets_earth/",
  "/docs/navigator/n_cyber-range/",
  "/docs/skills/anaconda%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97/",
  "/docs/cybersecurity/ctf/easy/",
  "/docs/cybersecurity/vulnhub/easy/",
  "/docs/skills/kali-linux/",
  "/docs/skills/switchyomega-mv3%E6%93%8D%E4%BD%9C%E8%AE%B0%E5%BD%95/",
  "/docs/cybersecurity/vulnhub/",
  "/docs/cybersecurity/ctf/easy/ctf-web-low/",
  "/docs/skills/win-+-r%E5%B8%B8%E7%94%A8%E6%8C%87%E4%BB%A4/",
  "/docs/cybersecurity/",
  "/docs/skills/%E7%BD%91%E7%AB%99%E6%9E%84%E5%BB%BA/",
  "/docs/",
  "/docs/navigator/n_papers/",
  "/docs/papers/",
  "/docs/cybersecurity/ctf/",
  "/docs/cybersecurity/ctf/medium/",
  "/docs/cybersecurity/vulnhub/medium/",
  "/docs/navigator/n_work/",
  "/docs/work/",
  "/docs/cybersecurity/ctf/hard/",
  "/docs/cybersecurity/vulnhub/hard/",
  "/docs/navigator/n_ai/",
  "/docs/ai/",
  "/docs/navigator/n_life/",
  "/docs/skills/",
  "/docs/life/",
  "/docs/navigator/n_forum/",
  "/docs/navigator/n_airport/",
  "/docs/navigator/",
  "/posts/k/",
  "/posts/",
  "/categories/",
  "/showcases/",
  "/tags/",
  "/",
  "/book.min.74a1ce47a9056b5f53aded13e2efe34b70e12db4c43106cbf6cf7d179f0f1cf8.css",
  "/zh.search-data.min.807ea96b99ce85b87a3a1c8402aa8efb3f8b69faf88ed294c9f53b21344661b4.json",
  "/zh.search.min.83f7e09a214b708d744db335492722c5756f5261c9c05a8e276581ba464413db.js",
  
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
