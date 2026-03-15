const cacheName = self.location.pathname
const pages = [

  "/posts/2026_03_14/",
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
  "/docs/navigator/n_function/",
  "/docs/skills/",
  "/docs/life/",
  "/docs/navigator/n_forum/",
  "/docs/navigator/n_airport/",
  "/docs/navigator/",
  "/docs/cybersecurity/ctf/competition/suctf-2026/",
  "/categories/",
  "/showcases/",
  "/tags/",
  "/",
  "/posts/",
  "/book.min.97949cc0e0264c59f6b67d681168cc646828d25eac76d9276840a134e1f94ec5.css",
  "/zh.search-data.min.3240259a46c5d7a6b84964a4872ea5b2783636c7ff705cb50241b6c706ab9bfd.json",
  "/zh.search.min.85989551872957b91e52153b10a200c6cc86782ef3a4939cd9109c8d525f6096.js",
  
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
