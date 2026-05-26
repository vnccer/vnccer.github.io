const cacheName = self.location.pathname
const pages = [

  "/docs/cybersecurity/vulnhub/medium/vulnhub_Corrosion2/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub_doubletrouble_1/",
  "/docs/cybersecurity/xnwlaqbc%E9%9D%B6%E6%9C%BA%E8%AE%B0%E5%BD%95/",
  "/docs/cybersecurity/xnwlaqbc%E9%9D%B6%E6%9C%BA%E8%AE%B0%E5%BD%95/xnwlaqbc%E9%9D%B6%E6%9C%BA%E9%83%A8%E7%BD%B2%E4%B8%8E%E6%94%BB%E5%87%BB/",
  "/docs/cybersecurity/xnwlaqbc%E9%9D%B6%E6%9C%BA%E8%AE%B0%E5%BD%95/DDos%E6%94%BB%E5%87%BB%E6%B5%8B%E8%AF%95/",
  "/docs/cybersecurity/vulnhub/medium/vulnhub_Thales/",
  "/docs/cybersecurity/vulnerabilities/Apache-Log4j2CVE-2021-44228%E5%A4%B1%E8%B4%A5%E5%B0%9D%E8%AF%95/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub_ICA_1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub_Beelzebub_1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub_Empire_Breakout/",
  "/docs/cybersecurity/vulnhub/medium/vulnhub_Empire_lupinone/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub_jangow_1.0.1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub_Napping-1.0.1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub_Noob_1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub_The-planets_earth/",
  "/docs/work/leetcode/1.%E5%93%88%E5%B8%8C/1.%E4%B8%A4%E6%95%B0%E4%B9%8B%E5%92%8C/",
  "/docs/work/AI%E5%AE%89%E5%85%A8%E6%80%9D%E8%80%83/",
  "/docs/skills/anaconda%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97/",
  "/docs/AI/claude-code-cli/",
  "/docs/cybersecurity/DVWA/",
  "/docs/cybersecurity/DVWA/dvwa%E5%88%9D%E5%A7%8B%E5%8C%96%E4%BF%AE%E5%A4%8D/",
  "/docs/cybersecurity/CTF/easy/",
  "/docs/cybersecurity/vulnhub/easy/",
  "/docs/papers/ET-BERT/",
  "/docs/papers/ET-BERT%E5%A4%8D%E7%8E%B0/",
  "/docs/cybersecurity/kali_linux%E5%9F%BA%E6%93%8D/",
  "/docs/work/leetcode/",
  "/docs/skills/linux-clash%E9%83%A8%E7%BD%B2/",
  "/docs/cybersecurity/vulnhub/medium/",
  "/docs/project/",
  "/docs/skills/pyenv%E7%AE%A1%E7%90%86python%E7%89%88%E6%9C%AC/",
  "/docs/skills/SwitchyOmega_mv3%E6%93%8D%E4%BD%9C%E8%AE%B0%E5%BD%95/",
  "/docs/project/vigil/",
  "/docs/project/vigil-abandoned-version/",
  "/docs/cybersecurity/vulnerabilities/",
  "/docs/cybersecurity/vulnhub/",
  "/docs/cybersecurity/CTF/easy/CTF-web-low/",
  "/docs/skills/win+r%E5%B8%B8%E7%94%A8%E6%8C%87%E4%BB%A4/",
  "/docs/skills/windows%E7%BB%88%E7%AB%AF%E8%B5%B0%E4%BB%A3%E7%90%86/",
  "/docs/AI/%E4%B8%BB%E6%B5%81AI%E5%AE%9A%E4%BB%B7/",
  "/docs/",
  "/docs/papers/%E5%8A%A0%E5%AF%86%E6%B5%81%E9%87%8F%E5%9F%BA%E7%A1%80/",
  "/docs/work/leetcode/1.%E5%93%88%E5%B8%8C/",
  "/docs/skills/%E5%9F%BA%E4%BA%8Evmware%E7%9A%84kali_linux%E4%B8%8B%E7%9A%84docker%E9%83%A8%E7%BD%B2%E5%9D%91%E5%A4%9A/",
  "/docs/work/%E5%AE%9E%E4%B9%A0%E7%AE%80%E5%8E%86/",
  "/docs/papers/%E6%95%B0%E6%8D%AE%E9%9B%86%E5%88%86%E6%9E%90/",
  "/docs/navigation/%E7%BD%91%E5%AE%89/",
  "/docs/skills/%E7%BD%91%E7%AB%99%E6%9E%84%E5%BB%BA/",
  "/docs/cybersecurity/DVWA/Authorisation-Bypass/",
  "/docs/cybersecurity/CTF/",
  "/docs/cybersecurity/CTF/medium/",
  "/docs/cybersecurity/",
  "/docs/navigation/%E8%AE%BA%E6%96%87/",
  "/docs/cybersecurity/DVWA/CSRF/",
  "/docs/cybersecurity/CTF/hard/",
  "/docs/cybersecurity/vulnhub/hard/",
  "/docs/navigation/%E5%B7%A5%E4%BD%9C/",
  "/docs/papers/",
  "/docs/navigation/Function/",
  "/docs/cybersecurity/DVWA/Open-HTTP-Redirect/",
  "/docs/work/",
  "/docs/navigation/AI/",
  "/docs/cybersecurity/DVWA/API/",
  "/docs/skills/",
  "/docs/AI/",
  "/docs/cybersecurity/DVWA/CSP-Bypass/",
  "/docs/navigation/Life/",
  "/docs/cybersecurity/DVWA/Cyptography/",
  "/docs/navigation/",
  "/docs/navigation/%E5%B9%B3%E5%8F%B0/",
  "/docs/cybersecurity/DVWA/Command-Injection/",
  "/docs/navigation/%E6%9C%BA%E5%9C%BA/",
  "/docs/cybersecurity/DVWA/File-Inclusion/",
  "/docs/cybersecurity/DVWA/SQL-Injection/",
  "/categories/",
  "/tags/",
  "/posts/20260526%E8%87%AA%E5%B7%B1%E7%BC%B4%E7%BA%B3%E7%A4%BE%E4%BF%9D/",
  "/categories/%E5%AE%9E%E7%94%A8%E6%8A%80%E8%83%BD/",
  "/tags/%E7%A4%BE%E4%BF%9D/",
  "/posts/20260515%E8%BF%9B%E5%85%A5%E5%9C%B0%E7%8B%B1/",
  "/categories/%E6%80%9D%E8%80%83/",
  "/tags/%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8/",
  "/posts/",
  "/",
  "/showcases/",
  "/book.min.736951ca3ba5472b01b559ccf11c0bd72daa52528001c9a2789c1ea4a2c2c765.css",
  "/en.search-data.min.e1c7ca9cd68908eae752227d25ef3e38281fc1d9ba9bfc08718f21982c0108d2.json",
  "/en.search.min.36173c825c36b40cdd8e4816b52adb05f1b8e4fa1d393c83b0ee2c884ec68a8f.js",
  
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
