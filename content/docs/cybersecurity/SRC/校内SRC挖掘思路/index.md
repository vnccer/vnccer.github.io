---
title: "校内SRC挖掘思路"
date: 2026-06-27
draft: true
weight: 1
---

# 一、思路
Masscan/Naabu（快速发现开放端口）
        ↓
Nmap（服务识别）
        ↓
httpx（Web资产探测）
        ↓
Nuclei（漏洞验证）


# 二、重要端口
- 远程控制、终端接入：22(SSH)、3389(RDP windows远控)、5900(VNC 图形远控)
- 内网基础设施、统一身份：445(SMB 文件共享)、389(LDAP 目录服务)、161(SNMP 网络管理)
- 核心数据库服务：6379(Redis)、27017(MongoDB)、9200(Elasticsearch)、3306(MySQL)、1433(SQL Server)、1521(Oracle)、5432(PostgreSQL)
- 企业中间件与Web容器：7001(WebLogic)、8080(Tomcat/JBoss)、80/443(HTTP/HTTPS)
- 云原生、现代运维开发：2375(Docker API)、5005(Java JDWP调试)、9000(Portainer/宝塔)、8888(宝塔面板/高位Web)

# 三、扫描
## 3.1 masscan
```bash
masscan -p22,80,443,445,1433,2375,3306,3389,5005,5900,6379,7001,8000,8080,27017 某个IP/24 --rate=2000 -oX 某个IP网段_masscan.xml
```

## 3.2 nmap
```bash
nmap -p22,80,443,445,1433,2375,3306,3389,5005,5900,6379,7001,8000,8080,27017 -sS -sV -sC -n -iL ips.txt -oA subnet_scan_report
```