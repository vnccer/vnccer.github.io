---
title: "crawlergo使用"
data: 2026-06-13
draft: false
weight: 1
---

# 基础使用：linux
chromium安装在`/tmp/chromium/`,开启最大10标签页，爬取AWVS靶场
```zsh
# quitck start
bin/crawlergo -c /tmp/chromium/chrome -t 10 http://testphp.vulnweb.com/

# proxyon
bin/crawlergo -c /tmp/chromium/chrome -t 10 --request-proxy socks5://127.0.0.1:7891 http://testphp.vulnweb.com/
```

# 基础使用：windows
windows
```bash
.\crawlergo_win_amd64.exe -c chrome.exe地址 -t 10 要爬取的网站
```

# 系统调用
```PYTHON
#!/usr/bin/python3
# coding: utf-8

import simplejson
import subprocess


def main():
    target = "http://testphp.vulnweb.com/"
    cmd = ["bin/crawlergo", "-c", "/tmp/chromium/chrome", "-o", "json", target]
    rsp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = rsp.communicate()
	#  "--[Mission Complete]--"  是任务结束的分隔字符串
    result = simplejson.loads(output.decode().split("--[Mission Complete]--")[1])
    req_list = result["req_list"]
    print(req_list[0])


if __name__ == '__main__':
    main()
```

# 适配最新chromium的codex更新提示词
**角色与背景：**
你现在是一个资深的 Go 语言开发工程师。我正在本地编译和修改一个著名的开源 Web 动态爬虫项目 crawlergo（基于 Go 语言）。

**遇到的问题：**
该项目底层依赖了 github.com/chromedp/chromedp 和 github.com/chromedp/cdproto 来与 Chrome 浏览器进行 CDP 通信。因为项目较老（约2022年），而我本地使用的是最新的 Chrome 浏览器（v151 内核），导致 CDP 协议不兼容。
在运行爬虫时，控制台出现了大量反序列化报错：
ERROR: could not unmarshal event: unknown IPAddressSpace value
ERROR: could not unmarshal event: unknown ClientNavigationReason value

**我的目标：**
我想升级该项目的依赖，使其兼容最新版的 Chrome DevTools Protocol，并重新编译。

请你帮我完成以下步骤，并给出具体的操作指令和代码修改指南：

1. 升级依赖： 我应该使用哪些 go get 命令来安全地将 chromedp 和 cdproto 升级到最新版本？

2. 解决破坏性更新 (Breaking Changes)： 升级这几个核心库通常会导致原有代码报错（例如 network.EventRequestWillBeSent 或其他 CDP 事件结构体字段发生变化）。请告诉我如何定位并修复由于 cdproto 升级带来的编译错误。

3. 处理未知的 Enum 值： 针对上述 unknown IPAddressSpace value 这种因为 Chrome 新增了枚举值而引发的 unmarshal 报错，如果在最新版本的 cdproto 中依然存在，我该如何在 Go 代码中优雅地忽略或兼容这些未知的 JSON 字段，以保证主线程不被报错刷屏？

4. 编译构建： 修复完代码后，在 Windows 环境下编译出 crawlergo_win_amd64.exe 的标准 go build 命令是什么？