---
title: "log4j2.8.1漏洞复现"
date: 2026-03-18
draft: false
weight: 2
---

# 一、环境
文件夹位置：`vulhub/base/log4j/2.8.1`

```BASH
# 小数点.，代表使用当前目录的Dockerfile，镜像起名为log4j-target
sudo docker build -t log4j-target .

# java web应用默认开放8080端口，把它映射到8080
sudo docker run -d --name my-log4j-app -p 8080:8080 log4j-target
```