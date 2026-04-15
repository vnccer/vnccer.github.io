---
title: "DVWA"
weight: 1
bookCollapseSection: true  #控制折叠
---

|DVWA|OWASP Top10:2025|简述|
|-----|-------------------|-----|
|Authorisation Bypass|A01:2025 - Broken Access Control|权限校验失效，允许访问非授权资源或执行越权操作。|
|CSRF|A01:2025 - Broken Access Control|利用受害者的身份在不知情下向服务器发送越权请求。|
|Open HTTP Redirect|A01:2025 - Broken Access Control|访问控制失效，攻击者可重定向用户至恶意钓鱼站点。|
|API|A01:2025 - Broken Access Control|API接口缺乏有效的对象级别授权或访问控制。|
|CSP Bypass|A02:2025 - Security Misconfiguration|内容安全策略配置不当或存在逻辑漏洞导致防护失效。|
|Cryptography|A04:2025 - Cryptographic Failures|使用弱加密算法、泄露硬编码密钥或敏感数据明文传输。|
|Command Injection|A05:2025 - Injection|应用未过滤输入，直接执行了由攻击者构造的系统命令。|
|File Inclusion|A05:2025 - Injection|通过注入路径导致服务器加载本地或远程的非预期文件。|
|SQL Injection|A05:2025 - Injection|向数据库查询语句注入非法代码，从而窃取或篡改数据。|
|SQL Injection (Blind)|A05:2025 - Injection|在无直接报错回显的情况下，通过逻辑或时间差注入数据。|
|XSS (DOM)|A05:2025 - Injection|在客户端通过操纵 DOM 环境注入并执行恶意脚本。|
|XSS (Reflected)|A05:2025 - Injection|恶意脚本通过 URL 参数即时反射回页面并在浏览器执行。|
|XSS (Stored)|A05:2025 - Injection|恶意脚本持久化存储在数据库中，用户访问页面时自动触发。|
|JavaScript Attacks|A05:2025 - Injection|攻击者篡改客户端 JS 逻辑或利用 JS 注入实施攻击。|
|Brute Force|A07:2025 - Authentication Failures|身份验证机制薄弱，未能防止自动化爆破和撞库攻击。|
|Insecure CAPTCHA|A07:2025 - Authentication Failures|验证码逻辑设计缺陷，导致认证防护环节可被轻易绕过。|
|Weak Session IDs|A07:2025 - Authentication Failures|会话标识符过于简单或可预测，导致会话被劫持或固定。|
|File Upload|A08:2025 - Software or Data Integrity Failures|未能校验文件完整性或类型，允许上传并执行恶意脚本文件。|