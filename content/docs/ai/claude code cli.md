---
title: "claude code cli"
data: 2026-05-07
draft: false
weight: 1
---

# 一、安装
```BASH
# powershell安装
irm https://claude.ai/install.ps1 | iex
```

安装后提示如下，需要添加环境变量`C:\Users\10714\.local\bin`到Path
```BASH
⚠ Setup notes:
  ● Native installation exists but C:\Users\10714\.local\bin is not in your PATH. Add it by
    opening: System Properties → Environment Variables → Edit User PATH → New → Add the path
     above. Then restart your terminal.
```

```bash
版本检查
claude --version
```
# 二、首次使用(deepseek接入)
临时使用deepseek api
```POWERSHELL
$env:ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
$env:ANTHROPIC_AUTH_TOKEN="输入deepseek的key"
$env:ANTHROPIC_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-v4-flash"
$env:CLAUDE_CODE_SUBAGENT_MODEL="deepseek-v4-flash"
$env:CLAUDE_CODE_EFFORT_LEVEL="max"
```

一直使用deepseek api
```powershell
if (!(Test-Path -Path $PROFILE)) { New-Item -ItemType File -Path $PROFILE -Force }
notepad $PROFILE

# 粘贴以下内容到$PROFILE
$env:ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
$env:ANTHROPIC_AUTH_TOKEN="输入deepseek的key"
$env:ANTHROPIC_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-v4-flash"
$env:CLAUDE_CODE_SUBAGENT_MODEL="deepseek-v4-flash"
$env:CLAUDE_CODE_EFFORT_LEVEL="max"
```


# 三、特定版本安装
```BASH
npm install -g @anthropic-ai/claude-code@2.1.152
```

```BASH
# 环境配置
notepad $PROFILE

# 应用环境
.$PROFILE
```