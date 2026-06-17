---
title: "crawlergo使用"
data: 2026-06-13
draft: false
weight: 1
---

> https://github.com/Qianlitp/crawlergo
> 
> [点击学习chromium特定版本安装](/docs/skills/安装特定版本chromium/#chromium)

# 基础使用：windows {#crawlergo}
windows
```bash
.\crawlergo_win_amd64.exe -c D:\3patience\chromium\chrome.exe -t 10 要爬取的网站

# 可加参数：
--output-json 爬取的网站.json
--request-proxy 127.0.0.1:8080
--push-proxy 127.0.0.1:8080
```