---
title: "windows终端/git 走代理"
data: 2026-05-07
draft: false
weight: 1
---

# 一、终端走代理
终端中`notepad $PROFILE`输入代理设置，`proxyon`开启代理，`proxyoff`关闭代理，`$env:HTTP_PROXY`检查代理情况
```TXT
# 1. 基础代理环境变量
$env:HTTP_PROXY = "http://127.0.0.1:7890"
$env:HTTPS_PROXY = "http://127.0.0.1:7890"

# 2. 只有在需要时才开启代理的开关 (可选，比一直开启更灵活)
function proxyon {
    $env:HTTP_PROXY = "http://127.0.0.1:7890"
    $env:HTTPS_PROXY = "http://127.0.0.1:7890"
    Write-Host "已开启终端代理 (Port: 7890)" -ForegroundColor Green
}

function proxyoff {
    $env:HTTP_PROXY = $null
    $env:HTTPS_PROXY = $null
    Write-Host "已关闭终端代理" -ForegroundColor Yellow
}
```

`. $PROFILE`立即加载

# 二、git走代理
```BASH
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890
```
取消`git config --global --unset http.proxy`

# 三、验证
HTTP代理`curl.exe -I https://www.google.com`