---
title: "git使用指南"
date: 2026-06-03
draft: false
weight: 1
---


# 一、Git 上传基础操作

从零开始将本地项目推送到 GitHub 远程仓库。

```powershell
# 1. 在项目根目录初始化 Git 仓库
cd D:\4work\3project\vigil
git init

# 2. 关联远程仓库（首次）
git remote add origin https://github.com/vnccer/vigil.git

# 3. 查看当前状态（哪些文件被修改、未跟踪）
git status

# 4. 将文件加入暂存区
git add .                        # 暂存所有变更（需确认 .gitignore 生效）
git add <文件名>                  # 暂存指定文件

# 5. 提交到本地仓库
git commit -m "描述本次改动的提交信息"

# 6. 推送到远程仓库
git push origin master           # 首次推送
git push                         # 已关联上游分支后简写

# 7. 日常提交流程（一气呵成）
git add <文件1> <文件2>
git commit -m "feat: 新增 PCAP 文件夹批量分析功能"
git push
```

**常用提交信息前缀约定：**

| 前缀        | 含义     | 示例                                   |
| ----------- | -------- | -------------------------------------- |
| `feat:`     | 新功能   | `feat: 新增 PCAP 文件夹批量解析`       |
| `fix:`      | 修复 bug | `fix: 修复 Streamlit 文件上传路径错误` |
| `refactor:` | 重构     | `refactor: 统一 CLI 与 Web 解析入口`   |
| `docs:`     | 文档更新 | `docs: 更新 Manual.md 附录 C`          |
| `chore:`    | 杂项维护 | `chore: 更新 .gitignore`               |

---

# 二、Commit 存档与版本回退

**核心思想：每一个 commit 就是一个存档点。** 存盘、读盘、覆盖云端存档，像游戏一样操作。

```powershell
# ===== 存档（Commit = 创建存档点） =====

# 改完代码 → 暂存 → 提交（三步存盘）
git add <文件1> <文件2>
git commit -m "feat: 新功能描述"

# 一步到位：提交所有已跟踪的修改
git add -u && git commit -m "fix: 修复了某个 bug"

# 推送到 GitHub（云端存档备份）
git push


# ===== 查看存档列表 =====

# 简洁历史（每个 commit 一行）
git log --oneline
# 输出示例:
#   f42bf68 vigil v1.0
#   a1b2c3d feat: 新增 PCAP 文件夹批量分析
#   e4f5g6h refactor: 统一 CLI 与 Web 解析入口

# 详细历史（含作者、日期、完整 message）
git log

# 图形化分支历史
git log --oneline --graph --all


# ===== 读档（Reset = 回到某个存档点） =====

# 回到指定 commit，丢弃之后的所有修改
git reset --hard <commit-hash>

# 回到上一个存档（最新 commit），丢弃未提交的修改
git reset --hard HEAD

# 回到倒数第 3 个存档
git reset --hard HEAD~3

# ⚠️ reset --hard 会丢弃之后的所有改动，操作前确认:
#   1. git log --oneline 确认目标 commit
#   2. git status 确认没有想保留的未提交内容


# ===== 回退后强制同步云端 =====

# reset 后本地落后于远程，需要 force push 覆盖
git push --force-with-lease

# --force-with-lease vs --force:
#   --force-with-lease: 如果远程有别人推送的新 commit，会拒绝覆盖（更安全）
#   --force: 无条件覆盖（暴力，多人协作时危险）


# ===== 反悔读档（Reflog = 撤销回退） =====

# reset 之后后悔了？reflog 记录了你所有的 HEAD 移动
git reflog
# 输出示例:
#   f42bf68 HEAD@{0}: reset: moving to HEAD~3
#   a1b2c3d HEAD@{1}: commit: feat: 新增 PCAP 文件夹批量分析
#   e4f5g6h HEAD@{2}: commit: refactor: 统一 CLI 与 Web 解析入口

# 回到 reset 之前的状态（跳到 HEAD@{1} 那个时刻）
git reset --hard HEAD@{1}
```

**经典操作流程 —— 开发翻车了，回到昨天的版本：**

```powershell
# 1. 查看历史，找到昨天那个"好版本"
git log --oneline
# f42bf68 vigil v1.0                          ← 想回到这里
# a1b2c3d feat: 新增功能（有问题）
# e4f5g6h feat: 另一个功能（也有问题）

# 2. 硬回退
git reset --hard f42bf68

# 3. 覆盖 GitHub 上的存档
git push --force-with-lease

# 4. 验证
git log --oneline          # 确认最新 commit 是 f42bf68
pytest tests/ -v           # 确认代码正常

# 5. 如果后悔了，还能回去
git reflog                 # 找到 reset 前的 commit
git reset --hard a1b2c3d   # 回到刚才那个"翻车"版本
```

**回退的粒度选择：**

| 命令                      | 效果                          | 什么时候用                           |
| ------------------------- | ----------------------------- | ------------------------------------ |
| `git reset --hard HEAD`   | 丢弃所有未提交的修改          | AI 改了一堆不想留的，回到上次 commit |
| `git reset --hard HEAD~1` | 撤销最近 1 个 commit          | 刚刚的 commit 就是坏的               |
| `git reset --hard HEAD~N` | 撤销最近 N 个 commit          | 最近几轮对话都在错的方向上           |
| `git reset --hard <hash>` | 回到指定 commit               | 需要回到上周某个稳定版本             |
| `git revert <hash>`       | 新建一个反向 commit，不删历史 | 多人协作，不能 force push 时使用     |

**删除与合并存档：**

AI 编程时你可能会频繁 commit 产生很多零散存档（如 "feat: 改了一半"、"WIP"）。这些碎片存档可以合并或删除。

```powershell
# ===== 合并存档：把最近 N 个 commit 压成一个 =====

# 方法一：软回退 + 重新提交（最简单，推荐）
git reset --soft HEAD~5     # 撤销最近 5 个 commit，但保留所有修改在暂存区
git update-ref -d HEAD      # 清空log，git回到最初状态，但工作区保持现状
git commit -m "feat: PCAP 文件夹批量分析（含进度优化、文档更新）"
git push --force-with-lease # 因为重写了历史，需要 force push

# 方法二：交互式合并（精细控制，想合哪些、留哪些）
git rebase -i HEAD~5
# 打开编辑器后，会看到最近 5 个 commit:
#   pick a1b2c3d feat: 新增功能
#   pick b2c3d4e fix: 小修复
#   pick c3d4e5f chore: 改格式
#   pick d4e5f6g fix: 又一个小修复
#   pick e5f6g7h docs: 更新注释
#
# 把后面 4 个的 pick 改成 squash（或 s），保留第一个 pick：
#   pick a1b2c3d feat: 新增功能
#   squash b2c3d4e fix: 小修复
#   squash c3d4e5f chore: 改格式
#   squash d4e5f6g fix: 又一个小修复
#   squash e5f6g7h docs: 更新注释
#
# 保存退出后，Git 会把 5 个 commit 合并为 1 个，并让你编辑新的 commit message


# ===== 删除存档：干掉中间某个 commit =====

# 交互式 rebase，把要删的 commit 标记为 drop
git rebase -i HEAD~5
# 把要删除的那行 pick 改成 drop（或 d），保存退出
#   pick a1b2c3d feat: 有用的功能
#   drop b2c3d4e feat: 这个功能不要了  ← 会被删除
#   pick c3d4e5f feat: 另一个有用的

# 操作完同样需要 force push 同步
git push --force-with-lease


# ⚠️ rebase 操作后必须 force push（历史被重写了）
# 如果 rebase 过程中出现问题：
git rebase --abort           # 取消这次 rebase，回到原始状态
git rebase --continue        # 解决冲突后继续
```

**合并时机参考：**

| 场景                                   | 操作                                             |
| -------------------------------------- | ------------------------------------------------ |
| 对话中产生了 5 个零散 WIP commit       | 对话结束后 `reset --soft` 合并为 1 个正式 commit |
| 中间某个 commit 引入了不该提交的大文件 | `rebase -i` → `drop` 删掉那个 commit             |
| GitHub 上已经有了这些零散 commit       | 合并后需要 `push --force-with-lease`             |
| 已经 push 且别人可能基于你的分支开发   | 不要再 force push，用 `revert` 代替              |

---

# 三、Vibe Coding 中的 Git 工作流

你跟 AI 结对编程，AI 改代码很快但有时会翻车。以下工作流专为这个场景设计。

**核心原则：每完成一轮对话就 commit 存档。翻车了就 reset 回退。**

```
┌──────────────────────────────────────────────────────┐
│  Vibe Coding + Git 工作流（Commit = 存档点）           │
├──────────────────────────────────────────────────────┤
│                                                      │
│  对话开始前                                           │
│    ├─ git status        确认工作区干净               │
│    └─ git log --oneline 记住当前版本 hash             │
│                                                      │
│  AI 结对编程中                                        │
│    ├─ 每完成一个独立功能                               │
│    │   └─ git add + git commit -m "..."   ← 存档！   │
│    └─ 如果 AI 改歪了                                  │
│        └─ git reset --hard HEAD   ← 读档回退！       │
│                                                      │
│  对话结束前                                           │
│    ├─ git diff           浏览 AI 改了什么              │
│    ├─ pytest tests/ -v   确认没破坏                  │
│    ├─ git add + commit   最终存档                     │
│    └─ git push           上传云端                     │
│                                                      │
│  发现之前某个版本更好                                  │
│    ├─ git log --oneline  找到好版本 hash              │
│    ├─ git reset --hard <hash>   回退                 │
│    └─ git push --force-with-lease   覆盖云端         │
│                                                      │
└──────────────────────────────────────────────────────┘
```

**具体操作节奏：**

```powershell
# ===== 对话开始 —— 记住出发版本 =====
git status
git log --oneline -5
# 记下当前最新 commit hash，万一翻车知道回哪


# ===== 对话中 —— 每个独立功能完成后存档 =====

# 比如 AI 刚完成了 PCAP 文件夹批量分析
git add app/main.py cli.py src/vigil/parser/pcap_parser.py
git commit -m "feat: PCAP 文件夹批量分析功能（CLI + Web 统一入口）"

# 接着 AI 又优化了进度展示
git add cli.py src/vigil/parser/pcap_parser.py
git commit -m "fix: 抑制 scapy 噪音警告，优化中文进度条"


# ===== 对话中 —— AI 改歪了，立刻回退 =====

# 发现 AI 刚才的改动方向不对
git reset --hard HEAD         # 丢弃未提交的修改
git reset --hard HEAD~1       # 连最新那个 commit 也丢掉
# 然后告诉 AI："前面这个方向不对，换一种做法"


# ===== 对话结束 —— 检查 + 存档 + 推送 =====

git diff                       # 确认没有遗漏的改动
pytest tests/ -v               # 跑测试
git add -u                     # 暂存所有修改
git commit -m "feat: 统一 PCAP 批量分析，更新文档"
git push


# ===== 第二天发现昨天改的整个方向都不对 =====

# 回到对话开始前的版本
git reset --hard <昨天记下的hash>
git push --force-with-lease
# 重新开始，这次换个思路
```

**三种翻车场景速查：**

```powershell
# 场景 1: AI 刚改了几行代码，还没 commit → 直接丢弃
git checkout -- <文件名>       # 恢复某个文件
git reset --hard HEAD          # 恢复所有文件

# 场景 2: 已经 commit 了，但就最近 1-2 个 commit 有问题
git reset --hard HEAD~2        # 回退 2 个 commit

# 场景 3: 改了很久，想回到历史上某个特定版本
git log --oneline              # 找目标 commit hash
git reset --hard <hash>        # 跳过去
git push --force-with-lease    # 覆盖远程
```

---

# 四、Vigil 项目环境部署

拿到项目代码后的完整部署流程。

## 4.1 硬件要求

| 组件 | 最低要求 | 推荐配置 |
|------|---------|---------|
| CPU | 4 核 | 6 核以上 |
| 内存 | 16 GB | 32 GB |
| GPU | 无（仅 Layer 1/2 可 CPU） | NVIDIA 8GB+ VRAM（Layer 3 训练） |
| 磁盘 | 10 GB 空闲 | SSD 20GB+（数据集较大） |
| OS | Windows 10+ / Ubuntu 20.04+ | — |

## 4.2 环境部署步骤

```powershell
# ===== 1. 克隆项目 =====
git clone https://github.com/vnccer/vigil.git
cd vigil

# ===== 2. 创建虚拟环境（二选一） =====
# 方案 A: Python venv
python -m venv venv
.\venv\Scripts\Activate.ps1     # Windows PowerShell
# venv\Scripts\activate         # Windows CMD
# source venv/bin/activate      # Linux / macOS

# 方案 B: Conda（推荐，GPU 训练时 cudatoolkit 管理更方便）
conda create -n vigil python=3.12 -y
conda activate vigil

# ===== 3. 安装依赖 =====
pip install -r requirements.txt

# Windows 下的额外依赖（scapy 完整 TLS 解析）
pip install scapy[complete]

# ===== 4. 验证安装 =====
python -c "import pandas; import scapy; import streamlit; import torch; print('安装成功')"

# ===== 5. 运行单元测试确认环境正常 =====
pytest tests/ -v

# ===== 6. 准备数据 =====
# 将 PCAP / TSV 数据放入 data/ 目录
# 示例结构:
#   data/
#   ├── sample.tsv                          # 自带测试样本
#   ├── your-capture.pcap                   # 单个抓包文件
#   └── your-website.com/                   # 按网站组织的多段抓包
#       ├── 001.pcap
#       ├── 002.pcap
#       └── ...
```

## 4.3 各系统注意事项

**Windows 11 (本地开发)：**

```powershell
# 如遇到 powershell 执行策略限制
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 如 matplotlib 中文显示为方框，系统自带微软雅黑无需额外配置
# 若在其他 Windows 版本上，需检查 C:\Windows\Fonts\msyh.ttc 是否存在
```

**Linux / AutoDL 云端训练：**

```bash
# 中文字体安装
sudo apt-get install fonts-noto-cjk -y

# 无 GUI 环境运行 matplotlib
echo 'export MPLBACKEND=Agg' >> ~/.bashrc

# Jupyter 远程端口映射（本地浏览器访问云端 Notebook）
# 在 AutoDL 控制台获取 SSH 命令后，添加端口转发:
# ssh -L 8888:127.0.0.1:8888 -p <端口> root@<实例IP>
```

## 4.4 启动各组件

```powershell
# Streamlit 演示面板
streamlit run app/main.py
# 访问 http://localhost:8501

# CLI 命令行检测
python cli.py data/sample.tsv                    # TSV 样本
python cli.py data/nvidia.com/                   # PCAP 文件夹批量分析
python cli.py data/your-capture.pcap             # 单个 PCAP

# Jupyter EDA 分析
jupyter notebook notebooks/01_eda_and_plot.ipynb

# 运行全部测试
pytest tests/ -v
```

##4.5 常见部署问题

| 症状                                    | 原因                        | 解决                                                         |
| --------------------------------------- | --------------------------- | ------------------------------------------------------------ |
| `pip install` 超时                      | 国内网络                    | `pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple` |
| `torch` 安装后 GPU 不可用               | CPU-only 版本               | 从 pytorch.org 按 CUDA 版本重新安装                          |
| `scapy.layers.tls` 导入失败             | 缺少 `cryptography`         | `pip install cryptography`                                   |
| Streamlit 端口冲突                      | 8501 已被占用               | `streamlit run app/main.py --server.port 8502`               |
| 项目导入报错 `ModuleNotFoundError: src` | PYTHONPATH 未包含项目根目录 | CLI/Streamlit 自动处理；自定义脚本需在项目根目录运行或 `sys.path.insert(0, ...)` |
