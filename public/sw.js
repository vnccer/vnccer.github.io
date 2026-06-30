const cacheName = self.location.pathname
const pages = [

  "/docs/cybersecurity/SRC/szuSRC/172.31.1.0/172.31.1.205/",
  "/docs/cybersecurity/SRC/szuSRC/172.31.1.0/",
  "/docs/cybersecurity/SRC/szuSRC/",
  "/docs/skills/%E5%AE%89%E8%A3%85%E7%89%B9%E5%AE%9A%E7%89%88%E6%9C%ACchromium/",
  "/docs/skills/git%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97/",
  "/docs/papers/%E5%9F%BA%E4%BA%8EBERT-CNN%E7%9A%84Webshell%E6%B5%81%E9%87%8F%E6%A3%80%E6%B5%8B%E7%B3%BB%E7%BB%9F%E8%AE%BE%E8%AE%A1%E4%B8%8E%E5%AE%9E%E7%8E%B0/",
  "/docs/cybersecurity/SRC/%E6%BC%8F%E6%B4%9E%E7%9B%92%E5%AD%90%E8%81%94%E6%83%B3%E9%9B%86%E5%9B%A2%E5%AE%89%E5%85%A8%E5%BA%94%E6%80%A5%E5%93%8D%E5%BA%94%E4%B8%AD%E5%BF%83%E5%A4%B1%E8%B4%A5/",
  "/docs/papers/%E5%9F%BA%E4%BA%8E%E5%8F%AF%E5%8F%98%E9%95%BF%E5%BA%8F%E5%88%97%E7%9A%84%E6%81%B6%E6%84%8F%E5%8A%A0%E5%AF%86%E6%B5%81%E9%87%8F%E6%A3%80%E6%B5%8B%E6%96%B9%E6%B3%95/",
  "/docs/cybersecurity/vulnhub/hard/vulnhub_Matrix-Breakout_-2_Morpheus/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub_drippingblues/",
  "/docs/cybersecurity/vulnhub/medium/vulnhub_Corrosion2/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub_doubletrouble_1/",
  "/docs/cybersecurity/xnwlaqbc%E9%9D%B6%E6%9C%BA%E8%AE%B0%E5%BD%95/",
  "/docs/cybersecurity/xnwlaqbc%E9%9D%B6%E6%9C%BA%E8%AE%B0%E5%BD%95/xnwlaqbc%E9%9D%B6%E6%9C%BA%E9%83%A8%E7%BD%B2%E4%B8%8E%E6%94%BB%E5%87%BB/",
  "/docs/cybersecurity/xnwlaqbc%E9%9D%B6%E6%9C%BA%E8%AE%B0%E5%BD%95/DDos%E6%94%BB%E5%87%BB%E6%B5%8B%E8%AF%95/",
  "/docs/cybersecurity/vulnhub/medium/vulnhub_Thales/",
  "/docs/skills/Hugo%E6%9E%B6%E6%9E%84%E7%BD%91%E7%AB%99%E6%90%AD%E5%BB%BA%E6%8C%87%E5%8D%97/",
  "/docs/cybersecurity/vulnerabilities/Apache-Log4j2CVE-2021-44228%E5%A4%B1%E8%B4%A5%E5%B0%9D%E8%AF%95/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub_Beelzebub_1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub_Empire_Breakout/",
  "/docs/cybersecurity/vulnhub/medium/vulnhub_Empire_lupinone/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub_ICA_1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub_jangow_1.0.1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub_Napping-1.0.1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub_Noob_1/",
  "/docs/cybersecurity/vulnhub/easy/vulnhub_The-planets_earth/",
  "/docs/skills/anaconda%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97/",
  "/docs/AI/claude-code-cli/",
  "/docs/cybersecurity/SRC/crawlergo%E4%BD%BF%E7%94%A8/",
  "/docs/cybersecurity/CTF/WEB/easy/CTFSHOW-Base64%E7%BC%96%E7%A0%81%E9%9A%90%E8%97%8F/",
  "/docs/cybersecurity/DVWA/",
  "/docs/cybersecurity/DVWA/dvwa%E5%88%9D%E5%A7%8B%E5%8C%96%E4%BF%AE%E5%A4%8D/",
  "/docs/cybersecurity/CTF/WEB/easy/",
  "/docs/cybersecurity/vulnhub/easy/",
  "/docs/cybersecurity/SRC/eduSRC/",
  "/docs/papers/ET-BERT/",
  "/docs/papers/ET-BERT%E5%A4%8D%E7%8E%B0/",
  "/docs/cybersecurity/SRC/FOFA%E4%BD%BF%E7%94%A8/",
  "/docs/cybersecurity/kali_linux%E5%9F%BA%E6%93%8D/",
  "/docs/skills/linux_clash%E9%83%A8%E7%BD%B2/",
  "/docs/cybersecurity/vulnhub/medium/",
  "/docs/project/",
  "/docs/skills/pyenv%E7%AE%A1%E7%90%86python%E7%89%88%E6%9C%AC/",
  "/docs/cybersecurity/SRC/",
  "/docs/cybersecurity/SRC/SRC%E6%8C%96%E6%8E%98%E6%80%9D%E8%B7%AF/",
  "/docs/skills/SwitchyOmega_mv3%E6%93%8D%E4%BD%9C%E8%AE%B0%E5%BD%95/",
  "/docs/project/vigil/",
  "/docs/project/vigil_t/",
  "/docs/cybersecurity/vulnerabilities/",
  "/docs/cybersecurity/vulnhub/",
  "/docs/cybersecurity/CTF/WEB/",
  "/docs/skills/win+r%E5%B8%B8%E7%94%A8%E6%8C%87%E4%BB%A4/",
  "/docs/skills/windows%E7%BB%88%E7%AB%AF%E8%B5%B0%E4%BB%A3%E7%90%86/",
  "/docs/AI/%E4%B8%BB%E6%B5%81AI%E5%AE%9A%E4%BB%B7/",
  "/docs/",
  "/docs/papers/%E5%8A%A0%E5%AF%86%E6%B5%81%E9%87%8F%E5%9F%BA%E7%A1%80/",
  "/docs/skills/%E5%9F%BA%E4%BA%8Evmware%E7%9A%84kali_linux%E4%B8%8B%E7%9A%84docker%E9%83%A8%E7%BD%B2%E5%9D%91%E5%A4%9A/",
  "/docs/papers/%E6%95%B0%E6%8D%AE%E9%9B%86%E5%88%86%E6%9E%90/",
  "/docs/cybersecurity/SRC/eduSRC/%E6%B1%9F%E8%8B%8F%E8%81%94%E5%90%88%E8%81%8C%E4%B8%9A%E6%8A%80%E6%9C%AF%E5%AD%A6%E9%99%A2/",
  "/docs/cybersecurity/SRC/eduSRC/%E6%B2%9B%E5%8E%BF%E8%80%81%E5%B9%B4%E5%A4%A7%E5%AD%A6/",
  "/docs/work/%E7%AE%80%E5%8E%86%E6%B7%B1%E6%8C%96/",
  "/docs/navigation/%E7%BD%91%E5%AE%89/",
  "/docs/cybersecurity/SRC/eduSRC/%E9%BB%91%E9%BE%99%E6%B1%9F%E5%86%9C%E4%B8%9A%E5%B7%A5%E7%A8%8B%E8%81%8C%E4%B8%9A%E6%8A%80%E6%9C%AF%E5%A4%A7%E5%AD%A6%E8%8D%AF%E5%BE%B7%E4%BA%91%E7%AB%AF%E5%AD%A6%E9%99%A2/",
  "/docs/cybersecurity/DVWA/Authorisation-Bypass/",
  "/docs/cybersecurity/CTF/",
  "/docs/cybersecurity/CTF/WEB/easy/CTFSHOW-HTTP%E5%A4%B4%E6%B3%A8%E5%85%A5/",
  "/docs/cybersecurity/CTF/WEB/medium/",
  "/docs/cybersecurity/",
  "/docs/navigation/%E8%AE%BA%E6%96%87/",
  "/docs/cybersecurity/DVWA/CSRF/",
  "/docs/cybersecurity/CTF/WEB/hard/",
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
  "/docs/navigation/%E8%AE%BA%E5%9D%9B/",
  "/docs/cybersecurity/DVWA/Command-Injection/",
  "/docs/navigation/%E6%9C%BA%E5%9C%BA/",
  "/docs/cybersecurity/DVWA/File-Inclusion/",
  "/docs/cybersecurity/DVWA/SQL-Injection/",
  "/categories/",
  "/tags/",
  "/categories/%E6%80%9D%E8%80%83/",
  "/tags/%E7%A0%94%E7%A9%B6%E7%94%9F%E8%A7%84%E5%88%92/",
  "/posts/20260929%E9%9D%A2%E5%90%91%E5%B0%B1%E4%B8%9A%E7%9A%84%E8%9B%8B%E7%96%BC/",
  "/posts/20260531%E7%A0%94%E7%A9%B6%E7%94%9F%E4%B8%89%E5%B9%B4%E8%A7%84%E5%88%92/",
  "/posts/20260526%E8%87%AA%E5%B7%B1%E7%BC%B4%E7%BA%B3%E7%A4%BE%E4%BF%9D/",
  "/categories/%E5%AE%9E%E7%94%A8%E6%8A%80%E8%83%BD/",
  "/tags/%E7%A4%BE%E4%BF%9D/",
  "/posts/20260515%E8%BF%9B%E5%85%A5%E5%9C%B0%E7%8B%B1/",
  "/tags/%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8/",
  "/posts/",
  "/",
  "/showcases/",
  "/book.min.736951ca3ba5472b01b559ccf11c0bd72daa52528001c9a2789c1ea4a2c2c765.css",
  "/en.search-data.min.cc1e9e7920c91cd1efe6e40bb3809705d36faec02d4c1ee2d6a679df7601484b.json",
  "/en.search-data.min.e85c4e15db8af74a440ca7f47ea4b451ad098c9133f3dea875b894735acc41d4.json",
  "/en.search.min.b07a5689a3e36089a8aa84ba332fbc1b88f5ebac77fb0acf7ab5c191acfea822.js",
  "/en.search.min.ed60ffbde602cce2a8971657928efaf7c4ddc8e462b4ce6a9d7440958ee7cb3a.js",
  
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
