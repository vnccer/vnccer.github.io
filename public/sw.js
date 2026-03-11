const cacheName = self.location.pathname
const pages = [

  "/docs/cybersecurity/vulnhub/easy/vulnhub-Beelzebub_1/",
  "/docs/cybersecurity/vulnhub/easy/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub-Empire_Breakout/",
  "/docs/cybersecurity/vulnhub/medium/vulnhub-Empire_lupinone/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub-ICA_1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub-jangow_1.0.1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub-Napping-1.0.1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub-Noob_1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub-The-planets_earth/",
  "/docs/cybersecurity/vulnhub/",
  "/docs/skills/anaconda%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97/",
  "/docs/cybersecurity/CTF/web/easy/",
  "/docs/skills/SwitchyOmega-mv3%E6%93%8D%E4%BD%9C%E8%AE%B0%E5%BD%95/",
  "/docs/skills/win-+-r%E5%B8%B8%E7%94%A8%E6%8C%87%E4%BB%A4/",
  "/docs/cybersecurity/",
  "/docs/skills/%E7%BD%91%E7%AB%99%E6%9E%84%E5%BB%BA/",
  "/docs/",
  "/docs/cybersecurity/vulnhub/medium/",
  "/docs/papers/",
  "/docs/cybersecurity/CTF/",
  "/docs/cybersecurity/CTF/web/medium/",
  "/docs/work/",
  "/docs/cybersecurity/CTF/web/hard/",
  "/docs/cybersecurity/vulnhub/hard/",
  "/docs/ai/",
  "/docs/skills/",
  "/docs/life/",
  "/posts/K/",
  "/posts/",
  "/categories/",
  "/showcases/",
  "/tags/",
  "/",
  "/book.min.4c5f6b0a2c9458d9b295650ba6c81a5261a6e5925a9e3f4141ed0a7db0ed85ac.css",
  "/zh.search-data.min.0368d7ae10ab1091748671670c0c6cfc54063a7d95d5785231c6f32dfe57437c.json",
  "/zh.search.min.397ea39ee9b7278158b3763fe9378bf4978298d0dc1d6c1dd3e5cf2b70c93ec0.js",
  
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
