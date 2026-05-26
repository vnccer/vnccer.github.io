---
title: "vigil"
data: 2026-05-17
draft: false
weight: 1
---

# 一、项目介绍
吸取vigil (abandoned version)项目教训，vigil专注于恶意加密流量在学术方面的研究，从第一层编码规则，到第二层机器学习，到第三层深度学习或模型，逐步提升检测能力和可解释性。

研发思路：先从编码规则入手（同时保留第二层和第三层的接口），做出一个完整的端到端可落地系统，再迭代优化规则，接着开始第二层，第三层的研发。

项目使用全说明，详见`Manual.md`:https://github.com/vnccer/vigil/blob/master/Manual.md
# 二、开发问题
1. 对于 CSTNET TLS 1.3 加密数据的tsv数据，无法分析

**原因：**
|特性|预期格式|CSTNET 实际格式|
|----|------|-------------|
|列结构|`src_ip`、`sni`、`packet_count`...|`label` + `text_a`|
|`text_a`|无|滑动窗口 hex 编码（2 字节 token，stride=1）|
|标签|"`benign`" / "`malicious`"|整数 0-119（120 类多分类）|

**解决：**
  - `src/vigil/parser/cstnet_loader.py`：新加载器：hex 解码 → 以太网帧解析 → TLS 特征提取 → TrafficFlow
  - `cli.py`：自动检测 `text_a` 列识别 CSTNET 格式

---

2. 对于 CSTNET TLS 1.3 ，检测全是良性流，没有恶意流

**原因：**
TLS 1.3 加密了更多的握手信息，大幅削减了密码套件，只保留了5个极安全的套件