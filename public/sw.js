const cacheName = self.location.pathname
const pages = [

  "/docs/cybersecurity/xnwlaqbc%E9%9D%B6%E6%9C%BA%E8%AE%B0%E5%BD%95/",
  "/docs/cybersecurity/xnwlaqbc%E9%9D%B6%E6%9C%BA%E8%AE%B0%E5%BD%95/xnwlaqbc%E9%9D%B6%E6%9C%BA%E9%83%A8%E7%BD%B2%E4%B8%8E%E6%94%BB%E5%87%BB/",
  "/docs/cybersecurity/xnwlaqbc%E9%9D%B6%E6%9C%BA%E8%AE%B0%E5%BD%95/DDos%E6%94%BB%E5%87%BB%E6%B5%8B%E8%AF%95/",
  "/docs/cybersecurity/vulnhub/medium/vulnhub-Thales/",
  "/docs/cybersecurity/vulnerabilities/Apache-Log4j2CVE-2021-44228%E5%A4%B1%E8%B4%A5%E5%B0%9D%E8%AF%95/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub-ICA_1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub-Beelzebub_1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub-Empire_Breakout/",
  "/docs/cybersecurity/vulnhub/medium/vulnhub-Empire_lupinone/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub-jangow_1.0.1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub-Napping-1.0.1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub-Noob_1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub-The-planets_earth/",
  "/docs/work/leetcode/1.%E5%93%88%E5%B8%8C/1.%E4%B8%A4%E6%95%B0%E4%B9%8B%E5%92%8C/",
  "/docs/skills/anaconda%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97/",
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
  "/docs/skills/SwitchyOmega_mv3%E6%93%8D%E4%BD%9C%E8%AE%B0%E5%BD%95/",
  "/docs/cybersecurity/vulnerabilities/",
  "/docs/cybersecurity/vulnhub/",
  "/docs/cybersecurity/CTF/easy/CTF-web-low/",
  "/docs/skills/win+r%E5%B8%B8%E7%94%A8%E6%8C%87%E4%BB%A4/",
  "/docs/",
  "/docs/work/leetcode/1.%E5%93%88%E5%B8%8C/",
  "/docs/skills/%E5%9F%BA%E4%BA%8Evmware%E7%9A%84kali_linux%E4%B8%8B%E7%9A%84docker%E9%83%A8%E7%BD%B2%E5%9D%91%E5%A4%9A/",
  "/docs/work/%E5%AE%9E%E4%B9%A0%E7%AE%80%E5%8E%86/",
  "/docs/cybersecurity/",
  "/docs/navigation/%E7%BD%91%E5%AE%89/",
  "/docs/skills/%E7%BD%91%E7%AB%99%E6%9E%84%E5%BB%BA/",
  "/docs/cybersecurity/DVWA/Authorisation-Bypass/",
  "/docs/cybersecurity/CTF/",
  "/docs/cybersecurity/CTF/medium/",
  "/docs/navigation/%E8%AE%BA%E6%96%87/",
  "/docs/papers/",
  "/docs/cybersecurity/DVWA/CSRF/",
  "/docs/cybersecurity/CTF/hard/",
  "/docs/cybersecurity/vulnhub/hard/",
  "/docs/navigation/%E5%B7%A5%E4%BD%9C/",
  "/docs/work/",
  "/docs/navigation/Function/",
  "/docs/cybersecurity/DVWA/Open-HTTP-Redirect/",
  "/docs/skills/",
  "/docs/navigation/AI/",
  "/docs/cybersecurity/DVWA/API/",
  "/docs/navigation/",
  "/docs/cybersecurity/DVWA/CSP-Bypass/",
  "/docs/navigation/Life/",
  "/docs/cybersecurity/DVWA/Cyptography/",
  "/docs/navigation/%E5%B9%B3%E5%8F%B0/",
  "/docs/cybersecurity/DVWA/Command-Injection/",
  "/docs/navigation/%E6%9C%BA%E5%9C%BA/",
  "/docs/cybersecurity/DVWA/File-Inclusion/",
  "/docs/cybersecurity/DVWA/SQL-Injection/",
  "/tags/",
  "/tags/%E6%8E%88%E6%9D%83%E7%BB%95%E8%BF%87/",
  "/tags/%E8%AE%BF%E9%97%AE%E6%8E%A7%E5%88%B6%E5%A4%B1%E6%95%88/",
  "/tags/%E5%8F%8D%E5%BC%B9shell/",
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
  "/tags/API/",
  "/posts/",
  "/categories/",
  "/tags/CSP%E7%BB%95%E8%BF%87/",
  "/tags/CSRF/",
  "/tags/dvwa/",
  "/",
  "/showcases/",
  "/tags/SQL%E6%B3%A8%E5%85%A5/",
  "/tags/%E5%8A%A0%E5%AF%86%E6%9C%BA%E5%88%B6%E5%A4%B1%E6%95%88/",
  "/tags/%E5%AE%89%E5%85%A8%E9%85%8D%E7%BD%AE%E9%94%99%E8%AF%AF/",
  "/tags/%E6%96%87%E4%BB%B6%E5%8C%85%E5%90%AB/",
  "/tags/%E6%B3%A8%E5%85%A5/",
  "/tags/%E9%87%8D%E5%AE%9A%E5%90%91%E6%BC%8F%E6%B4%9E/",
  "/book.min.736951ca3ba5472b01b559ccf11c0bd72daa52528001c9a2789c1ea4a2c2c765.css",
  "/en.search-data.min.2e859b0fc70779cf3aa00b685d3b99785acb57ced63bd250425a5113850c7a87.json",
  "/en.search.min.795dfb1f2d832c7b91321e2217a250444744cb065734b2c9ff4b8d11be19f512.js",
  
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
