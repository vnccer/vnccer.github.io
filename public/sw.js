const cacheName = self.location.pathname
const pages = [

  "/docs/cybersecurity/xnwlaqbc%E9%9D%B6%E6%9C%BA%E8%AE%B0%E5%BD%95/",
  "/docs/cybersecurity/xnwlaqbc%E9%9D%B6%E6%9C%BA%E8%AE%B0%E5%BD%95/xnwlaqbc%E9%9D%B6%E6%9C%BA%E9%83%A8%E7%BD%B2+%E6%94%BB%E5%87%BB%E5%85%A8%E6%B5%81%E7%A8%8B/",
  "/docs/cybersecurity/vulnhub/medium/vulnhub-Thales/",
  "/docs/cybersecurity/vulnerabilities/Apache-Log4j2CVE-2021-44228%E5%A4%B1%E8%B4%A5%E5%B0%9D%E8%AF%95/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub-ICA_1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub-Beelzebub_1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub-Empire_Breakout/",
  "/docs/cybersecurity/vulnhub/medium/vulnhub-Empire_lupinone/vulnhub-Empire_lupinone/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub-jangow_1.0.1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub-Napping-1.0.1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub-Noob_1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub-The-planets_earth/",
  "/docs/cybersecurity/DVWA/DVWA/",
  "/docs/skills/anaconda%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97/",
  "/docs/cybersecurity/DVWA/",
  "/docs/cybersecurity/CTF/easy/",
  "/docs/cybersecurity/vulnhub/easy/",
  "/docs/papers/ET-BERT/ET-BERT/",
  "/docs/skills/kali-linux/",
  "/docs/skills/SwitchyOmega-mv3%E6%93%8D%E4%BD%9C%E8%AE%B0%E5%BD%95/",
  "/docs/cybersecurity/vulnerabilities/",
  "/docs/cybersecurity/vulnhub/",
  "/docs/cybersecurity/CTF/easy/CTF-web-low/",
  "/docs/skills/win-+-r%E5%B8%B8%E7%94%A8%E6%8C%87%E4%BB%A4/",
  "/docs/",
  "/docs/skills/%E5%9F%BA%E4%BA%8Evmware%E7%9A%84kali-linux%E4%B8%8B%E7%9A%84docker%E9%83%A8%E7%BD%B2%E5%9D%91%E5%A4%9A/",
  "/docs/cybersecurity/",
  "/docs/skills/%E7%BD%91%E7%AB%99%E6%9E%84%E5%BB%BA/",
  "/docs/navigation/%E9%9D%B6%E5%9C%BA/",
  "/docs/cybersecurity/vulnerabilities/log4j2.8.1%E6%BC%8F%E6%B4%9E%E5%A4%8D%E7%8E%B0/",
  "/docs/cybersecurity/CTF/",
  "/docs/papers/ET-BERT/ET-BERT%E5%A4%8D%E7%8E%B0/",
  "/docs/cybersecurity/CTF/medium/",
  "/docs/cybersecurity/vulnhub/medium/",
  "/docs/papers/%E5%9F%BA%E4%BA%8E%E7%AA%81%E5%8F%91%E7%89%B9%E5%BE%81%E8%AF%8D%E5%85%83%E8%87%AA%E5%AD%A6%E4%B9%A0%E7%9A%84%E6%9C%AA%E7%9F%A5%E5%8A%A0%E5%AF%86%E6%81%B6%E6%84%8F%E6%B5%81%E9%87%8F%E6%A3%80%E6%B5%8B%E6%96%B9%E6%B3%95/",
  "/docs/navigation/%E8%AE%BA%E6%96%87/",
  "/docs/papers/",
  "/docs/cybersecurity/CTF/hard/",
  "/docs/cybersecurity/vulnhub/hard/",
  "/docs/navigation/%E5%B7%A5%E4%BD%9C/",
  "/docs/skills/",
  "/docs/navigation/Function/",
  "/docs/navigation/",
  "/docs/navigation/AI/",
  "/docs/navigation/Life/",
  "/docs/navigation/%E5%B9%B3%E5%8F%B0/",
  "/docs/navigation/%E6%9C%BA%E5%9C%BA/",
  "/docs/shortcodes/",
  "/tags/",
  "/tags/xxx/",
  "/tags/zzz/",
  "/tags/Base64%E8%A7%A3%E7%A0%81/",
  "/tags/FTP%E5%8C%BF%E5%90%8D%E7%99%BB%E5%BD%95/",
  "/tags/GTFOBins/",
  "/tags/Nano%E6%8F%90%E6%9D%83/",
  "/tags/ROT13%E8%A7%A3%E5%AF%86/",
  "/tags/SUID%E6%8F%90%E6%9D%83/",
  "/tags/XOR%E8%84%9A%E6%9C%AC/",
  "/tags/%E4%B8%80%E5%8F%A5%E8%AF%9D%E6%9C%A8%E9%A9%AC/",
  "/tags/%E5%91%BD%E4%BB%A4%E6%B3%A8%E5%85%A5/",
  "/tags/%E5%9E%82%E7%9B%B4%E6%8F%90%E6%9D%83/",
  "/tags/%E6%BC%8F%E6%B4%9E%E5%88%A9%E7%94%A8/",
  "/tags/%E7%BB%95%E8%BF%87/",
  "/tags/%E8%9A%81%E5%89%91/",
  "/tags/%E9%80%86%E5%90%91%E5%88%86%E6%9E%90/",
  "/tags/%E9%9A%90%E5%86%99%E6%9C%AF/",
  "/docs/shortcodes/asciinema/",
  "/docs/shortcodes/buttons/",
  "/docs/shortcodes/columns/",
  "/docs/shortcodes/details/",
  "/docs/shortcodes/experimental/",
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
  "/categories/",
  "/docs/shortcodes/katex/",
  "/",
  "/showcases/",
  "/book.min.736951ca3ba5472b01b559ccf11c0bd72daa52528001c9a2789c1ea4a2c2c765.css",
  "/en.search-data.min.5fa0d7baf574d9145c1aaaf1adff63a1225de45a9d011e9f585d42c7bc964524.json",
  "/en.search.min.559976af16ad20a509cb570a188159faf0af9c33bdc3538b6d2b68fb60cf3ed4.js",
  
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
