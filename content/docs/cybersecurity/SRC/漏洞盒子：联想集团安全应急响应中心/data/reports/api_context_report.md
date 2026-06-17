# API 上下文分析报告

> 自动从 JS bundle 中提取 API 的请求方式、鉴权、参数

**数据来源:** D:\4work\3project\rocky666\content\docs\cybersecurity\SRC\漏洞盒子：联想集团安全应急响应中心\data\downloads\lenovo_js_download 下 82 个文件 (JS + JSON)

**匹配率:** 40/44 个 API 在 JS bundle 中找到上下文

---

## 高危 — 核心业务与管理

### `/api/cms/website/front/job/config`

| 项目 | 值 |
|---|---|
| 方法 | **GET** |
| 鉴权 | Token |
| Content-Type | — |
| 参数 | `H` |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
ion/getByParentId/"+H)}function p(H){return e.post("/api/cms/website/front/news/listPageForWeb",H)}function h(H){return e.get(`/api/cms/website/front/news/getById?id=${H}`)}function g(){return e.get("/api/cms/website/front/job/config")}function v(H){return e.post("/api/cms/website/front/job/position",H)}function b(H){const D={};return H&&(D.Token=H),t.post("/login-server/logout",{},{headers:D})}function w(H,D,V){return t.get(`/lo
```

### `/api/order/region/getByParentId/`

| 项目 | 值 |
|---|---|
| 方法 | **GET** |
| 鉴权 | 无 |
| Content-Type | multipart/form-data |
| 参数 | `H` |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
Login",H)}function u(H){return t.post("/login-server/v3/updatePwd",H)}function f(H){return t.post("/login-server/login",H,{headers:{"Content-Type":"multipart/form-data"}})}function d(H){return e.get("/api/order/region/getByParentId/"+H)}function p(H){return e.post("/api/cms/website/front/news/listPageForWeb",H)}function h(H){return e.get(`/api/cms/website/front/news/getById?id=${H}`)}function g(){return e.get("/api/cms/website/
```

*（另有 3 处额外引用，见源文件）*

### `/app-version-manage-server/admin/driver/lenovoDriverList`

| 项目 | 值 |
|---|---|
| 方法 | **GET** |
| 鉴权 | 无 |
| Content-Type | — |
| 参数 | `H` |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
ount/omoc/miniProgramLink",H)}function ae(H){return t.post("/log-server/access",H)}function Te(H){return e.get("/api/customer/address/getByParentId?parentId="+H.parentId)}function Le(H){return e.get("/app-version-manage-server/admin/driver/lenovoDriverList",H)}function ye(){const{env:H}=ap();let D=H.value;return H.value==="production"?D="prod":H.value==="development"&&(D="dev"),t.get(`/app-version-manage-server/version/queryNewVersion?environment=${D}`
```

### `/bs/#/merchant/ES/settle`

| 项目 | 值 |
|---|---|
| 方法 | **?** |
| 鉴权 | 无 |
| Content-Type | ? |
| 来源文件 | `DBtvcc5o.js` |

**调用代码片段:**
```javascript
为供应商按钮"}),c.value=!0},H=()=>{t({type:"event",eventName:"supplierRecruit_settle",pageName:"supplierRecruit",moduleName:"成为供应商_成为供应商_立即入驻"}),window.open(u.value+"/bs/#/merchant/ES/settle","_blank")},L=()=>{t({type:"event",eventName:"supplierRecruit_application_submit",pageName:"supplierRecruit",moduleName:"成为供应商_成为供应商_留资提交按钮"})},O=()=>{t({type:"event",
```

### `/bs/#/merchant/SP/settle`

| 项目 | 值 |
|---|---|
| 方法 | **?** |
| 鉴权 | 无 |
| Content-Type | ? |
| 来源文件 | `_Nrr2E3B.js` |

**调用代码片段:**
```javascript
�服务商_申请加入合作流程"}),e.value=!0},S=()=>{A({type:"event",eventName:"serviceRecruit_settle",pageName:"supplierRecruit",moduleName:"成为服务商_立即入驻"}),window.open(d.value+"/bs/#/merchant/SP/settle","_blank")},N=()=>{A({type:"event",eventName:"serviceRecruit_application_submit",pageName:"serviceRecruit",moduleName:"成为服务商_申请加入_留资提交按钮"})},M=()=>{A({type:"event",event
```

### `/merchant/shop/selectPcShopShopListV2`

| 项目 | 值 |
|---|---|
| 方法 | **POST** |
| 鉴权 | 无 |
| Content-Type | application/json |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
search?brand="+H.brand+"&keyWord="+H.keyWord)}function j(){return e.get("/api/device/mechine-type/brand")}function B(H){return e.get("/api/order/region/getByParentId/"+H)}function G(H){return e.post("/merchant/shop/selectPcShopShopListV2",H)}function U(H){return e.post("/qrcode-server/account/omoc/miniProgramLink",H)}function ae(H){return t.post("/log-server/access",H)}function Te(H){return e.get("/api/customer/address/getByParentId?
```

### `/qrcode-server/account/omoc/miniProgramLink`

| 项目 | 值 |
|---|---|
| 方法 | **POST** |
| 鉴权 | 无 |
| Content-Type | application/json |
| 参数 | `H` |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
("/api/device/mechine-type/brand")}function B(H){return e.get("/api/order/region/getByParentId/"+H)}function G(H){return e.post("/merchant/shop/selectPcShopShopListV2",H)}function U(H){return e.post("/qrcode-server/account/omoc/miniProgramLink",H)}function ae(H){return t.post("/log-server/access",H)}function Te(H){return e.get("/api/customer/address/getByParentId?parentId="+H.parentId)}function Le(H){return e.get("/app-version-manage-serve
```

## 中危 — 数据交互

### `/api/cms/website/front/news/listPageForWeb`

| 项目 | 值 |
|---|---|
| 方法 | **POST** |
| 鉴权 | 无 |
| Content-Type | multipart/form-data |
| 参数 | `H` |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
,H)}function f(H){return t.post("/login-server/login",H,{headers:{"Content-Type":"multipart/form-data"}})}function d(H){return e.get("/api/order/region/getByParentId/"+H)}function p(H){return e.post("/api/cms/website/front/news/listPageForWeb",H)}function h(H){return e.get(`/api/cms/website/front/news/getById?id=${H}`)}function g(){return e.get("/api/cms/website/front/job/config")}function v(H){return e.post("/api/cms/website/front/job/po
```

### `/api/cms/website/front/reservation/addOrUpdate`

| 项目 | 值 |
|---|---|
| 方法 | **POST** |
| 鉴权 | 无 |
| Content-Type | application/json |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
er/humanVerify/sendAuthCode",H)}function S(){return e.get("/api/marketing/platform/captcha")}function y(H){return e.post("/api/marketing/platform/official/sendSmsCode",H)}function E(H){return e.post("/api/cms/website/front/reservation/addOrUpdate",H)}function C(H){return e.post("/api/customer/hardware/save",H)}function x(H,D){const V={};return D&&(V.Token=D),t.get("/login-server/getAuthorCodeVal",{headers:V,params:H})}function R(H){return t.g
```

### `/api/customer/address/getByParentId`

| 项目 | 值 |
|---|---|
| 方法 | **GET** |
| 鉴权 | 无 |
| Content-Type | — |
| 参数 | `H` |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
merchant/shop/selectPcShopShopListV2",H)}function U(H){return e.post("/qrcode-server/account/omoc/miniProgramLink",H)}function ae(H){return t.post("/log-server/access",H)}function Te(H){return e.get("/api/customer/address/getByParentId?parentId="+H.parentId)}function Le(H){return e.get("/app-version-manage-server/admin/driver/lenovoDriverList",H)}function ye(){const{env:H}=ap();let D=H.value;return H.value==="production"?D="prod":H
```

### `/api/customer/hardware/save`

| 项目 | 值 |
|---|---|
| 方法 | **POST** |
| 鉴权 | Token |
| Content-Type | application/json |
| 参数 | `H` |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
rm/captcha")}function y(H){return e.post("/api/marketing/platform/official/sendSmsCode",H)}function E(H){return e.post("/api/cms/website/front/reservation/addOrUpdate",H)}function C(H){return e.post("/api/customer/hardware/save",H)}function x(H,D){const V={};return D&&(V.Token=D),t.get("/login-server/getAuthorCodeVal",{headers:V,params:H})}function R(H){return t.get("/login-server/getUserTokenByAuthorCode",{params:H})}funct
```

*（另有 1 处额外引用，见源文件）*

### `/api/device/mechine-type/info/search`

| 项目 | 值 |
|---|---|
| 方法 | **GET** |
| 鉴权 | 无 |
| Content-Type | — |
| 参数 | `H` |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
(`/api/app/goods/getGoodsWarrantyInfoBySn?snCode=${H}`)}function L(H){return e.get("/api/device/mechine-type/machineTypeAutocomplete?brand="+H.brand+"&keyword="+H.keyword)}function $(H){return e.get("/api/device/mechine-type/info/search?brand="+H.brand+"&keyWord="+H.keyWord)}function j(){return e.get("/api/device/mechine-type/brand")}function B(H){return e.get("/api/order/region/getByParentId/"+H)}function G(H){return e.post("/merch
```

### `/api/marketing/platform/official/sendSmsCode`

| 项目 | 值 |
|---|---|
| 方法 | **POST** |
| 鉴权 | 无 |
| Content-Type | application/json |
| 参数 | `H` |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
erver/humanVerify/graphValidateCode")}function _(H){return t.get("/qrcode-server/humanVerify/sendAuthCode",H)}function S(){return e.get("/api/marketing/platform/captcha")}function y(H){return e.post("/api/marketing/platform/official/sendSmsCode",H)}function E(H){return e.post("/api/cms/website/front/reservation/addOrUpdate",H)}function C(H){return e.post("/api/customer/hardware/save",H)}function x(H,D){const V={};return D&&(V.Token=D),t.get
```

### `/api/user/userinfo`

| 项目 | 值 |
|---|---|
| 方法 | **?** |
| 鉴权 | 无 |
| Content-Type | ? |
| 来源文件 | `Cknfudua.js` |

**调用代码片段:**
```javascript
 URL("demo.COMo4Vwv.webp",import.meta.url).href,Ae={class:"project-list"},qe=oe({__name:"demo",async setup(r){let s,a;const t=ce();Ve();const e=P(1),n=P([]),i=P({}),{data:{value:d}}=([s,a]=le(()=>Ue("/api/user/userinfo","$KtCIpzVqJ1")),s=await s,a(),s);return i.value=d==null?void 0:d.data,t.isCsr.value,(u,o)=>{const p=J,c=W;return R(),ue(c,{class:he(u.$style["pc-demo"])},{default:U(()=>{var l;return[S("section",nul
```

### `/app-version-manage-server/version/queryNewVersion`

| 项目 | 值 |
|---|---|
| 方法 | **GET** |
| 鉴权 | 无 |
| Content-Type | — |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
turn e.get("/app-version-manage-server/admin/driver/lenovoDriverList",H)}function ye(){const{env:H}=ap();let D=H.value;return H.value==="production"?D="prod":H.value==="development"&&(D="dev"),t.get(`/app-version-manage-server/version/queryNewVersion?environment=${D}`)}function We(){return e.post("/api/customer/hardware/save")}function xe(){return t.get("/third-party-server/by_colleage/m_colleage_url")}function Ke(){return t.get("/enterprise-serv
```

### `/download`

| 项目 | 值 |
|---|---|
| 方法 | **?** |
| 鉴权 | 无 |
| Content-Type | ? |
| 来源文件 | `B4emEWQN.js` |

**调用代码片段:**
```javascript
�费标准",link:"/feeStandard"},{menuId:"6-5",menuName:"· 百应学院",link:"/college"},{menuId:"6-6",menuName:"· 服务政策",link:"/service-policy"}]},{menuId:"7",menuName:"下载中心",link:"/download"},{menuId:"8",menuName:"关于我们",link:"",width:150,isColumn:!0,subItems:[{menuId:"8-1",menuName:"· 关于联想百应",link:"/aboutBaiying"},{menuId:"8-2",menuName:"· 人才招聘",link:"/join
```

*（另有 10 处额外引用，见源文件）*

### `/download/_payload.json`

| 项目 | 值 |
|---|---|
| 状态 | :x: 未在 JS bundle 中找到 |

### `/login-server/getAuthorCodeVal`

| 项目 | 值 |
|---|---|
| 方法 | **GET** |
| 鉴权 | Token |
| Content-Type | — |
| 参数 | `H` |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
H)}function E(H){return e.post("/api/cms/website/front/reservation/addOrUpdate",H)}function C(H){return e.post("/api/customer/hardware/save",H)}function x(H,D){const V={};return D&&(V.Token=D),t.get("/login-server/getAuthorCodeVal",{headers:V,params:H})}function R(H){return t.get("/login-server/getUserTokenByAuthorCode",{params:H})}function O(H){const D={};return H&&(D.Token=H),t.get("/login-server/getLoginInfo",{headers:D})}f
```

### `/login-server/getLoginInfo`

| 项目 | 值 |
|---|---|
| 方法 | **GET** |
| 鉴权 | Token |
| Content-Type | — |
| 参数 | `H` |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
n=D),t.get("/login-server/getAuthorCodeVal",{headers:V,params:H})}function R(H){return t.get("/login-server/getUserTokenByAuthorCode",{params:H})}function O(H){const D={};return H&&(D.Token=H),t.get("/login-server/getLoginInfo",{headers:D})}function P(H){return e.get(`/api/app/goods/getGoodsWarrantyInfoBySn?snCode=${H}`)}function L(H){return e.get("/api/device/mechine-type/machineTypeAutocomplete?brand="+H.brand+"&keyword=
```

### `/login-server/getUserTokenByAuthorCode`

| 项目 | 值 |
|---|---|
| 方法 | **GET** |
| 鉴权 | Token |
| Content-Type | — |
| 参数 | `H` |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
}function C(H){return e.post("/api/customer/hardware/save",H)}function x(H,D){const V={};return D&&(V.Token=D),t.get("/login-server/getAuthorCodeVal",{headers:V,params:H})}function R(H){return t.get("/login-server/getUserTokenByAuthorCode",{params:H})}function O(H){const D={};return H&&(D.Token=H),t.get("/login-server/getLoginInfo",{headers:D})}function P(H){return e.get(`/api/app/goods/getGoodsWarrantyInfoBySn?snCode=${H}`)}function 
```

### `/login-server/login`

| 项目 | 值 |
|---|---|
| 方法 | **POST** |
| 鉴权 | 无 |
| Content-Type | multipart/form-data |
| 参数 | `H` |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
st("/login-server/v3/sendSmsVCodeForPwd",H)}function l(H){return t.post("/login-server/v3/doRegistAndLogin",H)}function u(H){return t.post("/login-server/v3/updatePwd",H)}function f(H){return t.post("/login-server/login",H,{headers:{"Content-Type":"multipart/form-data"}})}function d(H){return e.get("/api/order/region/getByParentId/"+H)}function p(H){return e.post("/api/cms/website/front/news/listPageForWeb",H)}funct
```

### `/login-server/logout`

| 项目 | 值 |
|---|---|
| 方法 | **POST** |
| 鉴权 | Token |
| Content-Type | application/json |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
Id?id=${H}`)}function g(){return e.get("/api/cms/website/front/job/config")}function v(H){return e.post("/api/cms/website/front/job/position",H)}function b(H){const D={};return H&&(D.Token=H),t.post("/login-server/logout",{},{headers:D})}function w(H,D,V){return t.get(`/login-server/v2/findPassword?deviceId=${H}&account=${D}&rid=${V}`)}function m(){return t.get("/qrcode-server/humanVerify/graphValidateCode")}function
```

### `/login-server/v2/checkRisk`

| 项目 | 值 |
|---|---|
| 方法 | **GET** |
| 鉴权 | 无 |
| Content-Type | — |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
s.Token||(o.headers.Token=(a=n==null?void 0:n.value)==null?void 0:a.token),o},o=>Promise.reject(o)),{request1:r,request2:s}}function HH(){const{request1:e,request2:t}=FH();function n(H){return t.get("/login-server/v2/checkRisk",{params:H})}function r(H){return t.post("/login-server/v3/sendSmsVCodeForRegister",H)}function s(H){return t.get("/login-server/v3/getGVCode",{params:H})}function o(H){return t.post("/login-server/v
```

### `/login-server/v2/findPassword`

| 项目 | 值 |
|---|---|
| 方法 | **GET** |
| 鉴权 | Token |
| Content-Type | — |
| 参数 | `H` |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
fig")}function v(H){return e.post("/api/cms/website/front/job/position",H)}function b(H){const D={};return H&&(D.Token=H),t.post("/login-server/logout",{},{headers:D})}function w(H,D,V){return t.get(`/login-server/v2/findPassword?deviceId=${H}&account=${D}&rid=${V}`)}function m(){return t.get("/qrcode-server/humanVerify/graphValidateCode")}function _(H){return t.get("/qrcode-server/humanVerify/sendAuthCode",H)}function S(){re
```

### `/login-server/v3/doLogin`

| 项目 | 值 |
|---|---|
| 方法 | **POST** |
| 鉴权 | 无 |
| Content-Type | application/json |
| 参数 | `H` |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
/login-server/v3/getGVCode",{params:H})}function o(H){return t.post("/login-server/v3/sendSmsVCodeForLogin",H)}function i(H){return t.post("/login-server/v3/fastLogin",H)}function a(H){return t.post("/login-server/v3/doLogin",H)}function c(H){return t.post("/login-server/v3/sendSmsVCodeForPwd",H)}function l(H){return t.post("/login-server/v3/doRegistAndLogin",H)}function u(H){return t.post("/login-server/v3/updatePwd",H)
```

### `/login-server/v3/doRegistAndLogin`

| 项目 | 值 |
|---|---|
| 方法 | **POST** |
| 鉴权 | 无 |
| Content-Type | multipart/form-data |
| 参数 | `H` |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
turn t.post("/login-server/v3/fastLogin",H)}function a(H){return t.post("/login-server/v3/doLogin",H)}function c(H){return t.post("/login-server/v3/sendSmsVCodeForPwd",H)}function l(H){return t.post("/login-server/v3/doRegistAndLogin",H)}function u(H){return t.post("/login-server/v3/updatePwd",H)}function f(H){return t.post("/login-server/login",H,{headers:{"Content-Type":"multipart/form-data"}})}function d(H){return e.get("/api/
```

### `/login-server/v3/fastLogin`

| 项目 | 值 |
|---|---|
| 方法 | **POST** |
| 鉴权 | 无 |
| Content-Type | application/json |
| 参数 | `H` |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
/v3/sendSmsVCodeForRegister",H)}function s(H){return t.get("/login-server/v3/getGVCode",{params:H})}function o(H){return t.post("/login-server/v3/sendSmsVCodeForLogin",H)}function i(H){return t.post("/login-server/v3/fastLogin",H)}function a(H){return t.post("/login-server/v3/doLogin",H)}function c(H){return t.post("/login-server/v3/sendSmsVCodeForPwd",H)}function l(H){return t.post("/login-server/v3/doRegistAndLogin",H)}f
```

### `/login-server/v3/getGVCode`

| 项目 | 值 |
|---|---|
| 方法 | **GET** |
| 鉴权 | 无 |
| Content-Type | — |
| 参数 | `H` |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
t{request1:e,request2:t}=FH();function n(H){return t.get("/login-server/v2/checkRisk",{params:H})}function r(H){return t.post("/login-server/v3/sendSmsVCodeForRegister",H)}function s(H){return t.get("/login-server/v3/getGVCode",{params:H})}function o(H){return t.post("/login-server/v3/sendSmsVCodeForLogin",H)}function i(H){return t.post("/login-server/v3/fastLogin",H)}function a(H){return t.post("/login-server/v3/doLogin",
```

### `/login-server/v3/sendSmsVCodeForLogin`

| 项目 | 值 |
|---|---|
| 方法 | **POST** |
| 鉴权 | 无 |
| Content-Type | application/json |
| 参数 | `H` |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
er/v2/checkRisk",{params:H})}function r(H){return t.post("/login-server/v3/sendSmsVCodeForRegister",H)}function s(H){return t.get("/login-server/v3/getGVCode",{params:H})}function o(H){return t.post("/login-server/v3/sendSmsVCodeForLogin",H)}function i(H){return t.post("/login-server/v3/fastLogin",H)}function a(H){return t.post("/login-server/v3/doLogin",H)}function c(H){return t.post("/login-server/v3/sendSmsVCodeForPwd",H)}function
```

### `/login-server/v3/sendSmsVCodeForPwd`

| 项目 | 值 |
|---|---|
| 方法 | **POST** |
| 鉴权 | 无 |
| Content-Type | application/json |
| 参数 | `H` |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
rn t.post("/login-server/v3/sendSmsVCodeForLogin",H)}function i(H){return t.post("/login-server/v3/fastLogin",H)}function a(H){return t.post("/login-server/v3/doLogin",H)}function c(H){return t.post("/login-server/v3/sendSmsVCodeForPwd",H)}function l(H){return t.post("/login-server/v3/doRegistAndLogin",H)}function u(H){return t.post("/login-server/v3/updatePwd",H)}function f(H){return t.post("/login-server/login",H,{headers:{"Conte
```

### `/login-server/v3/sendSmsVCodeForRegister`

| 项目 | 值 |
|---|---|
| 方法 | **POST** |
| 鉴权 | 无 |
| Content-Type | application/json |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
oken),o},o=>Promise.reject(o)),{request1:r,request2:s}}function HH(){const{request1:e,request2:t}=FH();function n(H){return t.get("/login-server/v2/checkRisk",{params:H})}function r(H){return t.post("/login-server/v3/sendSmsVCodeForRegister",H)}function s(H){return t.get("/login-server/v3/getGVCode",{params:H})}function o(H){return t.post("/login-server/v3/sendSmsVCodeForLogin",H)}function i(H){return t.post("/login-server/v3/fastLogin"
```

### `/login-server/v3/updatePwd`

| 项目 | 值 |
|---|---|
| 方法 | **POST** |
| 鉴权 | 无 |
| Content-Type | multipart/form-data |
| 参数 | `H` |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
post("/login-server/v3/doLogin",H)}function c(H){return t.post("/login-server/v3/sendSmsVCodeForPwd",H)}function l(H){return t.post("/login-server/v3/doRegistAndLogin",H)}function u(H){return t.post("/login-server/v3/updatePwd",H)}function f(H){return t.post("/login-server/login",H,{headers:{"Content-Type":"multipart/form-data"}})}function d(H){return e.get("/api/order/region/getByParentId/"+H)}function p(H){return e.post(
```

### `/news/list`

| 项目 | 值 |
|---|---|
| 方法 | **?** |
| 鉴权 | 无 |
| Content-Type | ? |
| 来源文件 | `B4emEWQN.js` |

**调用代码片段:**
```javascript
nsole.log(a.value),console.log(t.value),C){case"/aboutBaiying":console.log("href",C),a.value="footer_bar_introduction_about",t.value="底部导航栏_了解联想百应_关于联想百应";break;case"/news/list":a.value="footer_bar_introduction_news_list",t.value="底部导航栏_了解联想百应_最新动态";break;case"/join-us":a.value="footer_bar_introduction_recruitment",t.value="底部导航栏_了�
```

*（另有 6 处额外引用，见源文件）*

### `/news/list/_payload.json`

| 项目 | 值 |
|---|---|
| 状态 | :x: 未在 JS bundle 中找到 |

### `/qrcode-server/humanVerify/sendAuthCode`

| 项目 | 值 |
|---|---|
| 方法 | **GET** |
| 鉴权 | 无 |
| Content-Type | — |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
nction w(H,D,V){return t.get(`/login-server/v2/findPassword?deviceId=${H}&account=${D}&rid=${V}`)}function m(){return t.get("/qrcode-server/humanVerify/graphValidateCode")}function _(H){return t.get("/qrcode-server/humanVerify/sendAuthCode",H)}function S(){return e.get("/api/marketing/platform/captcha")}function y(H){return e.post("/api/marketing/platform/official/sendSmsCode",H)}function E(H){return e.post("/api/cms/website/front/rese
```

## 低危 — 常规功能

### `/api/cms/website/front/job/position`

| 项目 | 值 |
|---|---|
| 方法 | **POST** |
| 鉴权 | Token |
| Content-Type | application/json |
| 参数 | `H` |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
ite/front/news/listPageForWeb",H)}function h(H){return e.get(`/api/cms/website/front/news/getById?id=${H}`)}function g(){return e.get("/api/cms/website/front/job/config")}function v(H){return e.post("/api/cms/website/front/job/position",H)}function b(H){const D={};return H&&(D.Token=H),t.post("/login-server/logout",{},{headers:D})}function w(H,D,V){return t.get(`/login-server/v2/findPassword?deviceId=${H}&account=${D}&rid=${V}`)}fu
```

### `/api/cms/website/front/news/getById`

| 项目 | 值 |
|---|---|
| 方法 | **GET** |
| 鉴权 | 无 |
| Content-Type | multipart/form-data |
| 参数 | `H` |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
Type":"multipart/form-data"}})}function d(H){return e.get("/api/order/region/getByParentId/"+H)}function p(H){return e.post("/api/cms/website/front/news/listPageForWeb",H)}function h(H){return e.get(`/api/cms/website/front/news/getById?id=${H}`)}function g(){return e.get("/api/cms/website/front/job/config")}function v(H){return e.post("/api/cms/website/front/job/position",H)}function b(H){const D={};return H&&(D.Token=H),t.post("/l
```

### `/api/device/mechine-type/brand`

| 项目 | 值 |
|---|---|
| 方法 | **GET** |
| 鉴权 | 无 |
| Content-Type | — |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
-type/machineTypeAutocomplete?brand="+H.brand+"&keyword="+H.keyword)}function $(H){return e.get("/api/device/mechine-type/info/search?brand="+H.brand+"&keyWord="+H.keyWord)}function j(){return e.get("/api/device/mechine-type/brand")}function B(H){return e.get("/api/order/region/getByParentId/"+H)}function G(H){return e.post("/merchant/shop/selectPcShopShopListV2",H)}function U(H){return e.post("/qrcode-server/account/omoc/mini
```

### `/api/marketing/platform/captcha`

| 项目 | 值 |
|---|---|
| 方法 | **GET** |
| 鉴权 | 无 |
| Content-Type | — |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
H}&account=${D}&rid=${V}`)}function m(){return t.get("/qrcode-server/humanVerify/graphValidateCode")}function _(H){return t.get("/qrcode-server/humanVerify/sendAuthCode",H)}function S(){return e.get("/api/marketing/platform/captcha")}function y(H){return e.post("/api/marketing/platform/official/sendSmsCode",H)}function E(H){return e.post("/api/cms/website/front/reservation/addOrUpdate",H)}function C(H){return e.post("/api/custo
```

### `/log-server/access`

| 项目 | 值 |
|---|---|
| 方法 | **POST** |
| 鉴权 | 无 |
| Content-Type | application/json |
| 参数 | `H` |
| 来源文件 | `sTj8Gxax.js` |

**调用代码片段:**
```javascript
on/getByParentId/"+H)}function G(H){return e.post("/merchant/shop/selectPcShopShopListV2",H)}function U(H){return e.post("/qrcode-server/account/omoc/miniProgramLink",H)}function ae(H){return t.post("/log-server/access",H)}function Te(H){return e.get("/api/customer/address/getByParentId?parentId="+H.parentId)}function Le(H){return e.get("/app-version-manage-server/admin/driver/lenovoDriverList",H)}function ye(){con
```

### `/news/detail`

| 项目 | 值 |
|---|---|
| 方法 | **?** |
| 鉴权 | 无 |
| Content-Type | ? |
| 来源文件 | `B2x6TZ4H.js` |

**调用代码片段:**
```javascript
=Me(),s=ye(),f=ze();let o=N(""),v=N(0),u=N([]),h=N(1),w=N(0),c=N(0);const C=t=>{l({type:"event",eventName:"news_list_content_1-N",pageName:"news_list",moduleName:"最新动态_新闻内容"}),s.push(`/news/detail?id=${t}`)},g=async()=>{var p;const t=await f.getNewsList({current:h.value,size:15,terminalType:1});t.data.code==200&&((p=t.data.data)!=null&&p.records)&&(u.value=t.data.data.records,w.value=+t.data.d
```

*（另有 4 处额外引用，见源文件）*

### `/news/detail/_payload.json`

| 项目 | 值 |
|---|---|
| 状态 | :x: 未在 JS bundle 中找到 |

### `/warranty-enquiry`

| 项目 | 值 |
|---|---|
| 方法 | **?** |
| 鉴权 | 无 |
| Content-Type | ? |
| 来源文件 | `B4emEWQN.js` |

**调用代码片段:**
```javascript
Services"}]},{menuId:"6",menuName:"服务中心",width:180,isColumn:!0,subItems:[{menuId:"6-1",menuName:"· 服务网点查询",link:"/service-station"},{menuId:"6-2",menuName:"· 保修查询",link:"/warranty-enquiry"},{menuId:"6-3",menuName:"· 硬件加装升级查询",link:"/hardware-addition"},{menuId:"6-4",menuName:"· 服务收费标准",link:"/feeStandard"},{menuId:"6-5",menuName:"· 百应学院",link:"/c
```

*（另有 6 处额外引用，见源文件）*

### `/warranty-enquiry/_payload.json`

| 项目 | 值 |
|---|---|
| 状态 | :x: 未在 JS bundle 中找到 |
