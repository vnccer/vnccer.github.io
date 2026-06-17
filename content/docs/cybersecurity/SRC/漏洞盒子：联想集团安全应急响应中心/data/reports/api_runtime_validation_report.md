# 排除伪 200 后的接口名单

> 在线校验已自动剔除命中 SPA 兜底特征的接口，下面保留的是后续仍值得继续手测或人工复核的目标。

**生成时间:** 2026-06-17 16:04:24

**基准域名:** https://baiying.com.cn

**主页样本标题:** 联想百应智能体-企业AI落地 一步到位

## 结果概览

| 项目 | 数量 |
|---|---|
| 总接口数 | 44 |
| 已排除伪 200 | 16 |
| 保留接口数 | 20 |
| 可优先继续测试 | 0 |
| 需人工复核 | 20 |

## 可优先继续测试

当前没有自动判定为可直接继续测试的接口。

## 需人工复核

| 方法 | 接口 | 鉴权 | HTTP 状态 | 结论 | 备注 |
|---|---|---|---|---|---|
| ? | `/bs/#/merchant/ES/settle` | 无 | — | 需人工复核 | 非 GET，未自动请求 |
| ? | `/bs/#/merchant/SP/settle` | 无 | — | 需人工复核 | 非 GET，未自动请求 |
| POST | `/merchant/shop/selectPcShopShopListV2` | 无 | — | 需人工复核 | 非 GET，未自动请求 |
| POST | `/qrcode-server/account/omoc/miniProgramLink` | 无 | — | 需人工复核 | 非 GET，未自动请求 |
| POST | `/api/cms/website/front/news/listPageForWeb` | 无 | — | 需人工复核 | 非 GET，未自动请求 |
| POST | `/api/cms/website/front/reservation/addOrUpdate` | 无 | — | 需人工复核 | 非 GET，未自动请求 |
| POST | `/api/customer/hardware/save` | Token | — | 需人工复核 | 非 GET，未自动请求 |
| POST | `/api/marketing/platform/official/sendSmsCode` | 无 | — | 需人工复核 | 非 GET，未自动请求 |
| ? | `/api/user/userinfo` | 无 | — | 需人工复核 | 非 GET，未自动请求 |
| POST | `/login-server/login` | 无 | — | 需人工复核 | 非 GET，未自动请求 |
| POST | `/login-server/logout` | Token | — | 需人工复核 | 非 GET，未自动请求 |
| POST | `/login-server/v3/doLogin` | 无 | — | 需人工复核 | 非 GET，未自动请求 |
| POST | `/login-server/v3/doRegistAndLogin` | 无 | — | 需人工复核 | 非 GET，未自动请求 |
| POST | `/login-server/v3/fastLogin` | 无 | — | 需人工复核 | 非 GET，未自动请求 |
| POST | `/login-server/v3/sendSmsVCodeForLogin` | 无 | — | 需人工复核 | 非 GET，未自动请求 |
| POST | `/login-server/v3/sendSmsVCodeForPwd` | 无 | — | 需人工复核 | 非 GET，未自动请求 |
| POST | `/login-server/v3/sendSmsVCodeForRegister` | 无 | — | 需人工复核 | 非 GET，未自动请求 |
| POST | `/login-server/v3/updatePwd` | 无 | — | 需人工复核 | 非 GET，未自动请求 |
| POST | `/api/cms/website/front/job/position` | Token | — | 需人工复核 | 非 GET，未自动请求 |
| POST | `/log-server/access` | 无 | — | 需人工复核 | 非 GET，未自动请求 |

## 说明

- 已自动排除的伪 200 接口数量: 16
- 当前版本仍只自动请求 GET；POST/PUT/PATCH/DELETE 默认保留到“需人工复核”。
- 页面路由类噪声已在精简输出中尽量压缩，只保留更像接口的目标。