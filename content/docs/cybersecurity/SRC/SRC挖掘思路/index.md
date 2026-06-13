---
title: "SRC挖掘思路"
data: 2026-06-13
draft: false
weight: 1
---

# 一、总体思路
前端刺探 -> 发现端点 -> 后端变现

# 二、前端刺探
全自动收集 + 关键点人工确认

## 2.1 自动化收集
- **爬取：**使用`Crawlergo`或`Rad`（联动Burp Suite）。利用headless浏览器模拟真人点击、滚动，将前端动态加载的Webpack`chunk.js`全部触发抓取。
- **接口、指纹提取：**使用`LinkFinder`或burp插件`Hae`、`FindSomething`。配置好正则表达式，自动从抓到的JS流量中提取：
  - 全量URL/域名/子域名
  - API路由（如`/api/v2/update`）
  - 疑似天生敏感的字符串（带有`pwd`、`secret`、`token`、`key`的变量）

## 2.2 白盒化
发现某JS文件存在对应的`.map`文件（如访问`main.js.map`返回巨大的JSON），使用工具恢复：
```BASH
# 使用 reverse-sourcemap 恢复源码
reverse-sourcemap -i main.js -o src_code
```

恢复后，获得开发者的原始代码。重点看：
- `src/api/`或`src/net/`：通常定义了完整的后端接口列表
- `src/store/`（如Vuex/Pinia）：定义了全局变量、用户信息、权限逻辑
- 代码中的`// TODO:`或`// FIXME:`注释，开发者常在这里写下未完成的越狱接口和测试账密

# 二、发现端点
刺探会找到上千个字符串和接口，乱测会触发WAF（防火墙）封IP。

## 2.1 划分端点优先级
提取出的 API 按照高价值、低价值排序：
- 第一梯队（核心业务与管理）：包含`/admin/`、`/manage/、/system/`、`/user/delete`、`/audit/`、`/config/` 的接口
- 第二梯队（数据交互）： 包含 `/query`、`/export`、`/download`、`/getDetail` 的数据查询类接口。
- 第三梯队（常规功能）： 包含 `/log`、`/static`、`/version`、`/feedback` 等高概率无用接口。

## 2.2 补全API上下文
前端提取出的接口通常不完整（如只有`/api/v1/user/update`），需要观察正常流量，补全HTTP请求：
- 请求方式（Method）： 根据 JS 中的 Axios 定义，确认是 `GET`、`POST`、`PUT` 还是 `DELETE`。
- Content-Type： 确认是 `application/json` 还是 `application/x-www-form-urlencoded`。
- 鉴权头部： 观察正常请求中，鉴权用的是 `Cookie`、`Authorization: Bearer <token>` 还是自定义的 `X-Token`。

# 三、后端变现
将端点放进`Burp Suite Repaeater`或`Postman`中，向后端服务器发起请求。
## 3.1 未授权访问（BOLA/Missing Auth）
- 复制高价值接口（如`/api/admin/viewLogs`），删除请求头中所有的`Cookie`、`Authorization`、`Token` 以及自定义签名，直接发送请求。
- 变现标准：后端返回`200 OK`且溴代敏感数据，高危/严重漏洞
- 如果返回`401 Unauthorized`或`403 Forbidden`，说明有全局鉴权，换下一个

## 3.2 水平/垂直越权（IDOR / Privilege Escalation）
- 水平越权：注册两个普通账户A、B。用 A 的 Token 请求接口，但把参数中的`userId`、`orderId`或`accountId`改成B的。
- 垂直越权：很多前端通过配置`role: 'user'`或`role: 'admin'`来控制菜单显示。在Burp中截获请求，尝试在请求体或Query参数中加入`&role=admin`或`{"isAdmin": true}`，看后端是否直接信任并赋予管理权限。

## 3.3 云资产/第三方凭据接管（Credential Leak）
如果前端刺探到了硬编码的Key
- OSS/S3 密钥：使用 `S3Scanner` 或云服务管理工具，尝试列出存储桶（`Bucket`）。只要能列出文件名，即证明存在信息泄露（不要批量下载）
- 企业微信/钉钉 Webhook：构造一个标准的 JSON 文本发送给该 Webhook 地址。如果你的测试群收到了消息，中/高危漏洞变现成功。

## 3.4 接口输入点引申（SQLi / SSRF / Log4j）
- 针对未公开接口的参数（如`/api/query?name=test`），进行常规的 web 漏洞测试：
  - 在参数后加单引号`'`测试SQL注入
  - 如果参数是URL（如`/api/fetch?url=http://...`），测试 SSRF（服务端请求伪造）