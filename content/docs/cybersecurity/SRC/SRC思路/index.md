---
title: "SRC思路"
date: 2026-07-02
draft: false
weight: 1
---

# 信息收集：
软件
ENScan_GO：https://github.com/wgpsec/ENScan_GO
subfinder(或者oneforall)：https://github.com/projectdiscovery/subfinder
xray：https://github.com/chaitin/xray
TscanPlus：https://github.com/TideSec/TscanPlus

第一步：
enscan-v1.2.1.exe -n 百度 -invest 100（注意要先把cookie准备好）

第二步：
将enscan扫描的IPC备案的urls结果复制到urls.txt文件（记得去掉域名俩字）

第三步：
subfinder.exe -dL urls.txt -o results.txt

第四步：
无影WscanPlus进行URL探测是否存活（勾选主动指纹，全量指纹，配置好代理）
去轻武器库，进行jsfinder，目录扫描（带`http://`）
跑端口扫描，常见RCE

第五步：
信息搜集完全了，再接着进行xray扫漏洞，（一定要有授权）