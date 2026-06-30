---
title: "FOFA使用"
data: 2026-06-18
draft: false
weight: 1
---

# 一、eduSRC
## 1.1 FOFA思路：edu.cn域名下的低防护
```
domain="edu.cn" && (title="招生" || title="就业" || title="迎新") && (title="财务" || title="教务" || title="科研" || title="统一身份认证" || title="信息门户" || title="OA" || title="智慧校园" || title="网上办事大厅" || title="资产管理" || title="实验室" || title="实训" || title="一卡通")

domain="edu.cn" && title="招生" && body="用户名" && (body="职业" || body="专科" || body="大专")

domain="edu.cn" && title="就业"
domain="edu.cn" && title="迎新"
domain="edu.cn" && title="实验室"
```

https://jwc.sdipct.edu.cn/
http://nyzsjy.hynu.edu.cn/
https://zhaosheng.huwai.edu.cn:9443
http://ckxx.hebeea.edu.cn:8080/Hebzz.jh/webmaster/admin/login.do
https://danzhao.sddfvc.edu.cn/page/login
## 1.2 图片查询
**favicon：**
某学校用了某OA，可以利用favicon hash反查所有学校

**icon_hash：**

## 1.3 挖掘流程
```
FOFA
    ↓
筛 edu.cn
    ↓
找后台系统
    ↓
识别 CMS / 厂商
    ↓
判断是否为外包产品
    ↓
收集 JS
    ↓
找 API
    ↓
未授权
    ↓
越权
    ↓
文件上传
    ↓
SQL注入
    ↓
SSRF
    ↓
XXE
```
