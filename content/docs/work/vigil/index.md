---
title: "vigil"
data: 2026-05-09
draft: false
weight: 1
---

# 一、Vigil 启动指南
## 1.0 环境配置
前终端 python 默认指向 WindowsApps 的 3.14（无依赖包），依赖安装在 Anaconda 里。建议先设置别名：

方案 A：临时设置（每次启动终端执行一次）
```BASH
$env:PY = "D:\3patience\anaconda3\python.exe"
```
方案 B：永久调整 PATH 顺序，把 Anaconda 放最前面
System Properties → Environment Variables → Path → 将 D:\3patience\anaconda3 上移至顶部

## 1.1 快速冒烟测试（验证所有组件能否正常导入）
全链路数据流水线验证（不需要外部服务，用合成数据自测）
```
cd D:\4work\3project\vigil
.\test_pipeline.ps1
```

包含一次真实 MalwareBazaar 下载（需要网络）
```
# 1. 访问 https://bazaar.abuse.ch/api/ 申请 API Key
# 2. 设置环境变量后运行
$env:MALWAREBAZAAR_API_KEY = "这里写key"
.\test_pipeline.ps1 -DownloadTest
  
cd D:\4work\3project\vigil
.\test_pipeline.ps1 -DownloadTest
```

## 1.2 按模块启动
### 1.2.1 数据采集 - MalwareBazaar 下载样本
```bash
cd D:\4work\3project\vigil
D:\3patience\anaconda3\python.exe vigil-agents\agents\hunter.py TrickBot
```

### 1.2.2 数据采集 - Docker 沙箱抓包

```BASH
# 1. 启动docker desktop

# 2. 安装依赖（已安装）
D:\3patience\anaconda3\python.exe -m pip install docker

# 3. 从项目根目录运行沙箱（vigil-agents/malware_vault/）
cd D:\4work\3project\vigil
D:\3patience\anaconda3\python.exe vigil-agents\agents\sandbox.py 'vigil-agents\malware_vault\1a71a8bc099c9ab4d4c65431aa2190690ee0be76536c430e1acaf79254b4a455'

# 也可以一次跑多个样本
D:\3patience\anaconda3\python.exe vigil-agents\agents\sandbox.py 'vigil-agents\malware_vault\1a71a8bc099c9ab4d4c65431aa2190690ee0be76536c430e1acaf79254b4a455' 'vigil-agents\malware_vault\1d4ee7e7b4f27568f3d46a62070715e4c0b3d1c2b69ac7cf0db690fc3a1725b8'

# 4. 跑完后 .pcap 文件出现在 D:\4work\3project\vigil\sandbox_output\ 目录下
```

### 1.2.3 数据解析 — 加载 PCAP 或 CIC-IDS2017 CSV
```BASH
D:\3patience\anaconda3\python.exe vigil-data\dataset_parser.py <file_or_dir>

# 这里的<file_or_dir>为 .\sandbox_output\1a71a8bc099c9ab4d4c65431aa2190690ee0be76536c430e1acaf79254b4a455_20260511_030100.pcap
```

### 1.2.4 特征提取 — JA4 + SPL + IAT 验证
```BASH
cd D:\4work\3project\vigil
D:\3patience\anaconda3\python.exe vigil-engine\feature_extractor.py
# 输出: 30 维特征名称、合成样本提取结果、GNN stub 抛出证明
```

### 1.2.5 XAI 可解释性 — SHAP 解释器验证
```BASH
D:\3patience\anaconda3\python.exe vigil-engine\explainability.py
# 输出: 学术叙述 + 商业告警 + 全局特征重要性
```
### 1.2.6 评估指标 — TPR / FPR / F1 / ROC-AUC
```BASH
D:\3patience\anaconda3\python.exe vigil-eval\metrics.py
```

## 1.3 启动网关 + Benchmark（核心端到端演示）
终端 1 — 启动 API 网关：
```BASH
cd D:\4work\3project\vigil\vigil-gateway
D:\3patience\anaconda3\python.exe main.py
# 监听 http://127.0.0.1:8000
# 自动合成 XGBoost 模型 + SHAP 解释器
```

终端 2 — 运行性能 Benchmark：
```BASH
cd D:\4work\3project\vigil
D:\3patience\anaconda3\python.exe vigil-eval\api_benchmark.py

# 自定义参数
D:\3patience\anaconda3\python.exe vigil-eval\api_benchmark.py --total 5000 --concurrency 200
```

终端 3 — 手动 curl 测试：
```BASH
# 健康检查
curl http://127.0.0.1:8000/health

# 分析一个 30 维随机特征向量
$body = '{"features": [0.0,2.0,15.0,8.0,0.0,0.123,120.0,120.0,120.0,120.0,120.0,120.0,120.0,120.0,120.0,120.0,120.0,120.0,120.0,120.0,120.0,120.0,120.0,120.0,120.0,120.0,0.05,0.0,0.05,0.05]}'
curl -X POST http://127.0.0.1:8000/v1/analyze -H "Content-Type: application/json" -d $body
```

## 1.4 探针（仅 WSL2 / Linux）
```BASH
# 冒烟测试（Windows 也能跑，只验证 CPU 测量框架）
D:\3patience\anaconda3\python.exe vigil-probes\evaluate_overhead.py

# 1.1 检查安装的wsl版本
wsl -l -v

# 2. 安装+启动ubuntu
wsl --install -d Ubuntu
wsl -d Ubuntu

# 3. 安装python3
sudo apt update && sudo apt install python3

# 4. 安装 iperf3（自动运行建议No）
sudo apt update && sudo apt install iperf3 -y

# 5. 安装 BCC（探针依赖）
sudo apt install bpfcc-tools linux-headers-generic -y
sudo apt install python3-bpfcc -y

# 6. 启动 iperf3 服务器（另开一个 WSL2 终端）
iperf3 -s -p 5201

# 7. 进入项目
cd /mnt/d/4work/3project/vigil

# 8. 运行评估
sudo python3 vigil-probes/evaluate_overhead.py --full
```

## 1.5 一键实验脚本（未完成）
```BASH
cd D:\4work\3project\vigil
.\run_experiments.ps1 -Mode quick           # 快速验证
.\run_experiments.ps1 -Mode full -SkipShap  # 完整实验，跳过 SHAP
```

## 1.6 推荐启动顺序（从零验证全链路）
1. test_pipeline.ps1          → 验证所有模块导入和数据解析
2. vigil-engine/feature_extractor.py  → 确认特征提取正常
3. vigil-engine/explainability.py     → 确认 SHAP 可解释性
4. vigil-gateway/main.py (Terminal 1) → 启动 API
5. vigil-eval/api_benchmark.py (Terminal 2)  → 压测 + 出报告

# 二、git 上传
```BASH
echo "# Vigil" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/vnccer/Vigil.git
git push -u origin main
```