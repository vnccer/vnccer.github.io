# Nuxt 通用版重构设计文档

## 1. 文档目标

本文档用于指导当前联想百应专用脚本，重构为一套可复用于类似 `Nuxt.js / Vue SPA` 架构站点的通用流水线。

目标不是重写一套完全不同的新工具，而是在保留当前使用习惯的前提下，把现有能力拆成可复用模块，使其面对类似站点时仍然能完成以下工作：

- 从 `crawlergo / Burp / HaE / 手工样本` 中接收输入
- 下载 `JS / JSON / Nuxt` 资源
- 提取页面路由和 API
- 补全接口上下文
- 识别 `SPA 伪 200 / 前端兜底 / 登录页 / 重定向`
- 输出“排除伪 200 后的保留接口名单”


## 2. 当前现状

当前脚本已经具备一条完整链路，主要能力集中在：

- [main.py](D:/4work/3project/rocky666/content/docs/cybersecurity/SRC/漏洞盒子：联想集团安全应急响应中心/data/function/main.py)
- [classify_apis.py](D:/4work/3project/rocky666/content/docs/cybersecurity/SRC/漏洞盒子：联想集团安全应急响应中心/data/function/classify_apis.py)
- [api_context.py](D:/4work/3project/rocky666/content/docs/cybersecurity/SRC/漏洞盒子：联想集团安全应急响应中心/data/function/api_context.py)
- [runtime_validate.py](D:/4work/3project/rocky666/content/docs/cybersecurity/SRC/漏洞盒子：联想集团安全应急响应中心/data/function/runtime_validate.py)
- [src_pipeline](D:/4work/3project/rocky666/content/docs/cybersecurity/SRC/漏洞盒子：联想集团安全应急响应中心/data/function/src_pipeline)

现有能力已经覆盖：

- 数据源目录选择
- API 分类
- Nuxt 资源下载
- JS bundle 上下文补全
- 在线识别伪 200
- 输出排除伪 200 后的保留名单

但当前仍然带有明显“单站专用”特征：

- `DEFAULT_BASE_URL` 写死为 `https://baiying.com.cn`
- 样本文件名写死
- 分类规则与域名规则偏联想资产
- Nuxt 识别和 API 提取逻辑都集中在单文件中
- 运行时校验依赖当前站点样本
- 输出格式已经实用，但结构上还没有“框架层 / 站点层 / 输入适配层”的边界


## 3. 重构目标

重构后的通用版应满足以下目标：

1. 不依赖某个具体站点常量。
2. 不依赖手工命名固定样本文件才能运行。
3. 可以通过配置切换目标站点。
4. 可以自动识别 Nuxt 类站点的 SPA fallback 特征。
5. 可以保留当前菜单式使用体验。
6. 可以持续扩展到 `Next.js / 普通 Vue SPA / SSR + API` 混合站点。


## 4. 设计原则

### 4.1 保留当前使用习惯

仍然保留：

- `python function\main.py`
- 编号式菜单
- `reports/` 放报告
- `downloads/` 放下载产物

### 4.2 从“单站逻辑”改为“站点配置”

任何目标站特有信息都不应该再直接写在 Python 逻辑中，而应移动到配置层。

### 4.3 从“大脚本”改为“模块组合”

下载、提取、分类、校验、报告分别独立，避免后续改一个功能时牵连其它流程。

### 4.4 优先做 Nuxt 通用化，再考虑框架扩展

第一阶段只把当前能力稳定抽象到 `Nuxt / Vue SPA`。
不要在第一阶段就同时支持过多前端框架，否则复杂度会明显上升。


## 5. 目标架构

建议重构为以下结构：

```text
data/
  downloads/
  reports/
  targets/
    default.yml
    baiying.yml
  samples/
    baiying/
  function/
    main.py
    classify_apis.py
    api_context.py
    runtime_validate.py
    pipeline_menu.py
    src_pipeline/
      __init__.py
      config.py
      menu.py
      source_utils.py
      core/
        downloader.py
        route_extractor.py
        api_extractor.py
        context_enricher.py
        runtime_classifier.py
        reporter.py
      adapters/
        hae_adapter.py
        burp_adapter.py
        crawlergo_adapter.py
        sample_adapter.py
      frameworks/
        nuxt.py
        vue_spa.py
      targets/
        loader.py
      workflows/
        classify_workflow.py
        context_workflow.py
        runtime_workflow.py
```


## 6. 模块职责划分

### 6.1 `adapters/`

作用：接入不同来源的数据。

建议模块：

- `hae_adapter.py`
  - 读取 `Linkfinder.txt / ALL URL.txt / Sensitive Field.txt`
- `burp_adapter.py`
  - 读取 Burp 导出的原始请求/响应
- `crawlergo_adapter.py`
  - 读取 crawlergo 结果
- `sample_adapter.py`
  - 读取手工保存的请求/响应样本

收益：

- 输入格式与核心分析逻辑解耦
- 后续新增新输入源时，不需要动主流程

### 6.2 `frameworks/`

作用：识别和封装前端框架特征。

建议第一阶段保留：

- `nuxt.py`
  - 识别 `/_nuxt/`
  - 识别 `_payload.json`
  - 识别 `builds/meta/*.json`
  - 定义 Nuxt 资产下载规则
  - 定义 Nuxt 页面 fallback 特征
- `vue_spa.py`
  - 兜底支持普通 Vue 单页应用

收益：

- 将“Nuxt 特征”从业务逻辑中拆出来
- 后续新增 `nextjs.py` 时不用重写其它模块

### 6.3 `core/downloader.py`

作用：通用资产下载器。

负责：

- 扫描文本、HTML、JS 中的 Nuxt 资源 URL
- 自动去重
- 下载 `js / json / payload / meta`
- 统一下载目录结构

建议补强点：

- 增加 `manifest.json` 式下载记录
- 对失败文件记录原因
- 支持断点续跑

### 6.4 `core/route_extractor.py`

作用：提取页面路由和前端页面路径。

负责：

- 识别 Nuxt 页面路由
- 识别动态路径占位符
- 从 payload 和 bundle 中恢复页面列表
- 标记“更像页面而不是接口”的路径

### 6.5 `core/api_extractor.py`

作用：从 bundle 中提取 API 路径。

建议采用“三层策略”：

1. 正则提取
   - 快速扫描 `"/api/..."`
   - 适合批量粗提取
2. 调用模式提取
   - 识别 `.get(` `.post(` `fetch(` `$fetch(` `useFetch(`
3. 轻量 AST 提取
   - 只对高价值命中文件做精细提取

收益：

- 对 Nuxt 2 / Nuxt 3 / 压缩代码都更稳
- 降低误提取页面路由的概率

### 6.6 `core/context_enricher.py`

作用：补全接口上下文。

负责：

- 方法推断
- 鉴权推断
- Content-Type 推断
- 查询参数推断
- 调用片段定位

建议未来支持：

- 区分 `公共客户端` 与 `认证客户端`
- 记录 header 构造逻辑
- 标记是否引用本地状态、token store、cookie

### 6.7 `core/runtime_classifier.py`

作用：运行时校验与响应分类。

建议输出统一分类：

- `spa_fallback_200`
- `json_api`
- `login_page_html`
- `html_page`
- `redirect`
- `forbidden_or_unauthorized`
- `not_found`
- `waf_block`
- `manual_check`
- `unknown`

当前已有的 `伪 200` 判定逻辑可以保留，但需要通用化为“站点无关”的规则引擎。

### 6.8 `core/reporter.py`

作用：统一管理报告输出。

负责：

- 完整分析报告
- 精简接口名单
- 排除伪 200 后名单
- JSON 格式结果
- 未来可增加 TXT / CSV

收益：

- 输出结构统一
- 以后修改报告格式不需要改核心逻辑


## 7. 配置体系设计

### 7.1 新增 `targets/default.yml`

默认配置用于兜底：

```yaml
name: default
base_url: ""
framework: nuxt
auth_headers:
  - Token
  - Authorization
api_prefix_hints:
  - /api/
  - /admin/
  - /merchant/
spa_markers:
  - /_nuxt/
  - _payload.json
  - data-capo
exclude_extensions:
  - .png
  - .jpg
  - .css
  - .js
```

### 7.2 新增 `targets/baiying.yml`

联想百应专用配置从当前代码中抽出，例如：

- `base_url`
- `target_domains`
- `标题特征`
- `站点关键词`
- `鉴权 header 偏好`

### 7.3 配置加载器

新增：

- `src_pipeline/targets/loader.py`

负责：

- 读取 YAML
- 合并 `default.yml + 指定站点.yml`
- 提供给各模块统一访问


## 8. 自动基线生成设计

这是通用版最关键的能力之一。

当前问题：

- 伪 200 判定依赖手工样本文件

目标：

- 不需要手工提供主页样本，也能自动识别 SPA fallback

建议方案：

1. 自动请求主页 `/`
2. 自动请求一个明显不存在的路径，例如：
   - `/__codex_spa_probe__`
3. 比较两者是否：
   - 状态码相同
   - `Content-Type` 相同
   - 标题相同
   - HTML 结构高度相似
   - 同时命中 `/_nuxt/` 等标记

若相似度高，则自动建立该站点的 SPA fallback 指纹。

这样后续校验任何接口时，就能自动判断：

- 是真实 JSON
- 是主页型 fallback
- 是登录页型 fallback

建议保留手工样本作为“覆盖项”，但不再作为必需项。


## 9. 菜单设计建议

重构后建议菜单升级为：

1. 选择目标配置
2. 选择数据源目录
3. 识别站点架构
4. 下载 Nuxt 资产
5. 分类 API
6. 补全 API 上下文
7. 在线校验并排除伪 200
8. 输出保留接口名单
9. 执行完整流水线
0. 退出

如果不想一次改太大，也可以先保持当前 1-6，只在内部改为新模块调用。


## 10. 输出物设计

建议最终固定以下报告：

- `api_priority_report.txt`
  - API 分类报告
- `api_context_report.md`
  - API 上下文补全报告
- `api_runtime_validation_report.md`
  - 在线校验结果
- `api_runtime_keep_list.md`
  - 排除伪 200 后的保留接口名单
- `api_runtime_keep_list.txt`
  - 纯文本名单，便于复制到 Burp / Excel
- `api_runtime_validation.json`
  - 结构化结果，便于后续二次处理


## 11. 第一阶段重构范围

第一阶段不建议大拆大改，只做“最有收益、风险最低”的部分。

### 第一阶段目标

把当前联想百应脚本改造成“可配置的 Nuxt 通用版”。

### 第一阶段包含

1. 抽离站点配置
2. 抽离框架特征
3. 抽离运行时分类器
4. 保留现有 CLI 和菜单
5. 保留现有报告名
6. 新增自动基线生成功能

### 第一阶段不包含

1. AST 深度解析
2. Next.js 支持
3. 全量 Burp 请求复放
4. WAF 分类精细化
5. 多线程在线批量优化


## 12. 推荐迁移顺序

### 阶段 A：配置外移

目标：

- 把 [config.py](D:/4work/3project/rocky666/content/docs/cybersecurity/SRC/漏洞盒子：联想集团安全应急响应中心/data/function/src_pipeline/config.py) 中写死的站点常量转为配置输入

任务：

- 新增 `targets/default.yml`
- 新增 `targets/baiying.yml`
- 增加配置加载器
- 修改 `classifier.py / context.py / runtime_validator.py` 读取配置

### 阶段 B：框架抽象

目标：

- 把 Nuxt 特征识别从逻辑代码中拆出来

任务：

- 新增 `frameworks/nuxt.py`
- 迁移以下规则：
  - `/_nuxt/`
  - `_payload.json`
  - `builds/meta/*.json`
  - Nuxt SPA marker

### 阶段 C：自动基线

目标：

- 移除“依赖手工样本才能判定伪 200”的硬依赖

任务：

- 自动请求主页
- 自动请求不存在页面
- 自动生成 SPA fallback 指纹
- 手工样本降级为可选增强项

### 阶段 D：输出拆分

目标：

- 分离“详细报告”和“保留名单”

任务：

- `api_runtime_validation_report.md` 保留完整报告
- 新增 `api_runtime_keep_list.md`
- 新增 `api_runtime_keep_list.txt`

### 阶段 E：输入适配扩展

目标：

- 支持更多来源

任务：

- 增加 `crawlergo_adapter.py`
- 增加 `burp_adapter.py`
- 增加通用请求/响应样本读取


## 13. 风险与注意点

### 13.1 误判风险

通用版最大风险不是跑不起来，而是：

- 把真实页面误判成接口
- 把真实接口误判成伪 200

因此运行时分类器一定要保留：

- 相似度
- 标题
- SPA marker
- 状态码
- Content-Type
- 人工复核分支

### 13.2 过度自动化风险

当前你已经明确要求只自动请求 `GET`，这一点建议继续保留。

对 `POST/PUT/PATCH/DELETE`：

- 默认仍走人工复核
- 除非后续引入“真实请求复放模式”

### 13.3 站点差异风险

即便都是 Nuxt，实际仍可能有差异：

- SSR 与 CSR 混用
- API 与页面域名分离
- 登录页与主页不是同一模板
- WAF 会把不存在路径统一返回 200 HTML

因此配置层必须允许站点覆盖默认规则。


## 14. 建议保留的现有能力

以下内容建议尽量保留，不要推翻：

- 当前菜单交互方式
- 当前 `reports/`、`downloads/`、`function/` 目录习惯
- 当前 `api_context_report.md` 的表格结构
- 当前“排除伪 200 后保留名单”的输出方向
- 当前“只自动请求 GET”的安全策略


## 15. 建议新增的核心文件

第一阶段建议新增这些文件：

- `data/targets/default.yml`
- `data/targets/baiying.yml`
- `function/src_pipeline/targets/loader.py`
- `function/src_pipeline/frameworks/nuxt.py`
- `function/src_pipeline/core/runtime_classifier.py`
- `function/src_pipeline/core/reporter.py`

第二阶段再新增：

- `function/src_pipeline/adapters/crawlergo_adapter.py`
- `function/src_pipeline/adapters/burp_adapter.py`
- `function/src_pipeline/core/api_extractor.py`


## 16. 第一阶段落地后的预期效果

完成第一阶段后，这套工具应当达到：

- 不改核心代码，只换配置，就可以切站
- 面对同类 Nuxt 站点仍能下载 JS/JSON
- 仍能提取 API 和页面路由
- 仍能识别伪 200
- 仍能输出排除伪 200 后的保留名单

这时它就已经从“联想百应脚本”升级成“Nuxt 前端分析通用流水线”。


## 17. 推荐下一步实施顺序

如果按实际开发顺序推进，我建议下一步就做：

1. 新建 `targets/default.yml` 和 `targets/baiying.yml`
2. 新建配置加载器
3. 先改 `runtime_validator.py` 读取配置
4. 再改 `classifier.py`
5. 最后改 `context.py`

这样能最快把“站点写死”问题先解决。


## 18. 结论

当前这套脚本已经具备一个很好的基础，不需要推倒重来。

最合理的重构路线是：

- 保留入口与使用习惯
- 拆出站点配置
- 拆出 Nuxt 框架特征
- 拆出运行时分类器
- 增加自动基线生成
- 逐步扩展输入适配和输出格式

按这个路线推进，最终可以沉淀出一套适用于 `Nuxt / Vue SPA` 站点的通用分析工具，而不仅仅服务于当前这个项目。
