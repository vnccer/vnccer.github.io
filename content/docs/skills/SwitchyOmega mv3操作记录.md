---
title: "SwitchyOmega mv3操作记录"
data: 2026-03-07
draft: false
weight: 1
---

# 一、proxy模式设置
代理服务器选择`HTTP`，`127.0.0.1`，`7897`（梯子ip和端口）

# 二、auto switch
规则列表格式：AutoProxy
规则列表地址：`https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt`，立即更新情景模式

# 三、burp suite和switchyomega插件配合
## 3.1 简单切换
新建情景模式`burpsuite`，代理服务器，`HTTP`，`127.0.0.1`，`8080`

## 3.2 链式代理
`浏览器` -> `burp suite8080` -> `梯子软件7897` -> `互联网`
切换到`burpsuite`情景模式

burp suite软件开启 -> Network -> Connections
Upstream Proxy Servers部分，点击Add
Destination host填`*`（代表所有网站）
Proxy host填`127.0.0.1`
Proxy port填`7897`
认证类型：若无密码，留空

## 3.3 备注
在浏览器导入burp suite的CA证书，不然HTTPS网站会报安全错误

### 3.3.1 导出证书
开启burp suite代理监听器，浏览器访问`http://burp`，下载右上角的CA Certificate，得到`cacert.der`
浏览器隐私、安全性、管理证书，导入受信任的证书，重启
