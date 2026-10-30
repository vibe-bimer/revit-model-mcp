# Revit Model MCP 文档站完整 review

目标：http://192.168.100.120:8099（MkDocs 1.6.1 + Material 9.7.7 + mkdocs-static-i18n 1.3.1，288 页 = 144 对 zh/en）
日期：2026-10-30　范围：构建产物 + 源文件 + 生成器 + 服务端 + 发布链路
方法：四轴并行独立审计（HTTP/托管、双语、事实准确性、IA/UX/可达性）+ Lead 跨轴复核，每条结论均有 `file:line` 或实测数值。

---

## 结论

站点的**工艺水平高，工程闭环破了一个口**。

- 288 页全部渲染正确、可达性基本达标（对比度 AA、单一 h1、键盘可操作、打印干净）、`mkdocs build --strict` 零警告、发布产物与工作树构建**逐字节一致**、`check_site.py` 的 54,704 条内部引用**零错误**。
- 但这套门禁只验证"链接能否解析"，不验证"内容是否互相矛盾、是否真的被发布、元数据是否真的渲染、HTTP 语义是否成立"。四轴找到的 40 条问题**全部在门禁盲区**。
- 唯一一条会让读者照文档操作直接失败的 P0，是**同一个工具被两个面各写一遍、参数不同、而两个面都说"当前版本已有"**。
- 一条 P0 级的流程问题：**受门禁的自动发布通道已死 27 天，线上正在服务未提交的工作树内容**，而 systemd 报"成功"。

分级口径：P0 = 照文档做会失败或被误导；P1 = 明确的正确性/可信度缺陷，有现成修法；P2 = 影响体验或运维，不阻断；P3 = 打磨项。

| 轴 | P0 | P1 | P2 | P3 |
|---|---|---|---|---|
| 双面 IA（Lead + ux-ia） | 1 | 2 | 3 | 2 |
| 元数据与发布（i18n + http-hosting） | – | 3 | 4 | 1 |
| 双语（i18n-audit） | – | 1 | 4 | 2 |
| 事实准确性（accuracy） | – | 1 | 1 | 4 |
| 可达性与交互（ux-ia） | – | 1 | 4 | 4 |
| 合计（去重后） | **1** | **7** | **14** | **11** |

---

## P0 — 同一工具，两份互相矛盾的契约，都说"当前版本已有"

`docs/features/`（35 个已发布工具）与 `docs/platform/`（80 个集成分支工具）是两个独立生成的目录树，**共 27 个工具名同时出现**。比对 `tools/site/content/tools.json` 与 `tools/site/content/platform-tools.json` 的 `inputSchema.properties`：

- **仅 8 个参数集相同，19 个不同。**
- **这 19 个不同的页面，事实条全部写着"当前版本是否已有：有"（19/19）。**

最直接的例证 `revit_export_view`：

```text
docs/platform/revit_export_view.md:5   <b>当前版本是否已有</b> 有
docs/platform/revit_export_view.md:13  | `output_path` | 否 | None | any | New PNG path, …   ← 分支版
docs/platform/revit_export_view.md:22  | `process_id`  | 否 | None | any | 目标 Revit 进程号。   ← 分支版

docs/features/revit_export_view.md:21  | `save_to` | 否 | `null` | `string / null` | …          ← 0.9.0 版
```

在 0.9.0 上照 `platform/revit_export_view` 传 `output_path` 会被 schema 拒绝；该传 `save_to`。页面却声明"当前版本已有"——这句话字面为真（工具在），实践为假（签名不在）。

同类差异（分支新增/改名的参数）：**16 个工具**把 `pickup_timeout_seconds` 换成 `process_id`（17 个分支页有 `process_id`，其中 16 个对应替换）；另有 `confirm_token`（`revit_delete`）、`limit`/`name_contains`（`revit_list_catalog`）、`parameter_id`（`revit_set_parameter`）、`output_path`（`revit_export_view`、`revit_model_health`）。

**为什么难发现**：两个面之间**零交叉链接**——`grep "platform/" docs/features/revit_*.md` = 0，`grep "../features/" docs/platform/*.md` = 0。读者从任一面都到不了另一面。唯一的免责声明在汇总页 `docs/platform/index.md:9`（"两者的工具数量与清单都不同，不能混用"）和 `:193`（"当成契约与进度，而不是「已可用」"），**单页上没有**。

叠加三个放大器：

1. **导航顺序误导**：`mkdocs.yml:233` 把 `功能`（已发布 35 个）排在 `新版基座`（未发布 80 个）之前，后者读起来是"更新的一代"，而实际是未发布分支。
2. **标题各说各话**：27 个共有工具里 **20 个两页显示标题不同**（`revit_export_view` = 「导出视图图片」vs「导出视图为 PNG」），7 个完全相同并在 `<title>` 里撞车（实测 10 组重复标题）。
3. **搜索不区分**：`revit_export_view` 同时命中两页，标题都是人话、都不含工具标识符，结果里没有任何面别标记。

**修法**（按成本从低到高）：
- 生成器里给 80 个分支页在 `h1` 之上加常驻横幅"未发布分支 · 契约可能变更"，并删除/改写"当前版本是否已有 有"这一行——它本身就不该由名字相等推断（`tools/site/platform_catalog.py:692-696`）。
- 每个重复页加一行生成式互链："发布版：`docs/features/<name>.md`"。键用注册表名，不要用标题。
- 导航标签加状态：`功能 · 0.9.0 已发布` / `新版基座 · 未发布`。
- 统一 `<title>` 生成规则，让两个面同名工具不再共用标题。

---

## P1 — 七个必须修的

### P1-1 元数据整段是死代码，上一轮"已修"从未生效
`mkdocs.yml` 从未定义 `site_description`，也没有任何页面设置 `meta.description`。因此 `docs/overrides/main.html:13-14` 的 `{% set page_description = … else config.site_description %}` 永远为空，`:16-17`、`:25-26`、`:37-38` 三处 emit 全是死代码：**288 个真实页面 0 处 `<meta name="description">`、0 处 `og:description`、0 处 `twitter:description`**（唯一 grep 命中是未渲染的模板副本 `site/overrides/main.html`）。2026-10-03 那轮 REVIEW 声称加过 description，实际只落了 OG/Twitter 的 title/image。
同一模板 `:33` 把 `og:locale` 硬编码成 `zh_CN`，**144 个英文页全部自称中文**（实测 `site/en/actions/index.html`）。
修：`mkdocs.yml` 加 `site_description`，每页 front matter 加 `description`；`og:locale` 按 `page.is_homepage`/i18n locale 取值。

### P1-2 唯一能让读者卡死的缺失环境变量
`src/RevitModelMcp.Addin/Control/DialogOverride.cs:16` 定义 `REVIT_MCP_ANSWER_DIALOGS`，`:22-24` 说明它用于自动应答 Revit 模态框。文档在 `docs/rebuild-performance.md:29-31` 与 `docs/actions.md:105` 教用户跑无人值守多实例复制农场，而该变量**在任何环境变量表里都不存在**（`docs/` 与 `server/` grep 零命中）。照文档搭的农场会卡在 Revit 的"文件已打开"模态框。
修：加入环境变量表，并在性能/动作页的农场步骤里显式设置。

### P1-3 发布通道死亡，线上服务的是未提交内容
`~/.local/state/revit-model-mcp/site-update.log`：2,716 次定时运行，**2,591 次 `skipping pull AND publish`**，最后一次成功自动发布是 **2026-10-03（124 页）**，此后 27 天全被工作树脏状态挡住。`site/` 当前内容来自手工构建（22:00 时间戳），因此线上 `/en/features/` 存在 `class="state part"` ×8，而 `git show HEAD:docs/features/index.en.md` 里没有。**跳过仍然 `exit 0`，systemd 报 "Finished" 成功**。
修：脏树时退出非零并让 systemd 标 failure；或改用"构建到临时目录 + 原子切换"的发布方式，从工作树发布但要显式记录来源 commit。当前是两次 rename，中间有被服务的空窗，且无回滚。

### P1-4 尾斜杠没有规范化，三个 URL 一份内容
`/features`、`/features/`、`/features/index.html` 三者均 `200`、同为 `107,595 B`、同一 `ETag "18e3536be9572d40-1a44b"`、无 `Location`。无斜杠形式下相对导航引用解析错位（可达 40–81 条断链的形态），且 canonical 只能指一个。
修：`serve-site.py` 对目录补 `/` 做 301。

### P1-5 hreflang 用相对 URL，备用语言集失效
`/features/` 输出 `<link rel="alternate" href="./" hreflang="zh">` 与 `href="../en/features/" hreflang="en"`；`/en/features/` 输出 `../../features/` 与 `./`。而 canonical 是正确的绝对 URL。hreflang 规范要求绝对 URL（含 host），相对值会被搜索引擎忽略。
修：与 canonical 同源生成绝对地址。

### P1-6 搜索不分语言
中文查询与英文查询返回**完全相同的 28 条结果、完全相同的顺序**，两个首页排 1–2，已发布页面排 4、分支页面排 5，每条都混着两种文字（`mkdocs.yml:94` 无 locale 配置）。同时工具页搜索标题是 H1 人话，不含 `revit_export_view`，按标识符检索的读者拿不到精确命中。
修：按 `/en/` 前缀分索引，或在索引条目加 `lang` 字段并按当前 locale 过滤。

### P1-7 双语互指，两边都没内容
`docs/rebuild-performance.en.md:3-4` 让读者去看中文页拿完整会话记录，`docs/rebuild-performance.md:5-6` 让读者去看英文页；两页都说自己是摘要、对方是全文，实际两边都没有那份记录。这是"我修好了/是他没修"式文档漂移的典型样本。
修：把记录放进其中一页，另一页只留链接。

---

## P2 — 十四项（按主线归并）

**HTTP / 托管**
- `HEAD` 与 `GET` 不一致：`HEAD /` 返回 `Content-Length: 114395` 且无 `Content-Encoding`；`GET` 加 gzip 返回 `15066` + `Content-Encoding: gzip` + `Vary: Accept-Encoding`。`HEAD` 404 返回 `Content-Length: 0`，`GET` 404 返回 `95,039 B`。
- 所有未命中（含 `/favicon.ico`、`/robots.txt`、manifest、`/.well-known/security.txt`）都返回 95 KB 的 HTML 404；这几个文件一个都没发布。
- `/sitemap.xml.gz` 以 `application/xml` 且无 `Content-Encoding` 发出。
- `Vary` 只出现在压缩的 200 上；304 缺 `Last-Modified`；未加哈希的 `.png`/`.woff2` 拿到 7 天 `max-age`（内容一变就长期脏缓存）。
- `GET /%00` 直接空响应并抛 `ValueError` 回溯（未捕获异常路径）。
- 发布是两次 rename，中间存在被服务的空窗；无回滚机制。
- 死资源：`site/screenshots/revit-model-mcp_claude-desktop.gif` **3.27 MB**，在 `site/` 全目录（html/css/js）零引用、`docs/` 源码零引用，仍随每次构建发布。占站点 39 MB 的 8.4%。

**双语**
- 生成器把中文 Revit UI 标签漏进英文页：`docs/features/revit_export_element_ids.en.md:41-44` 含 `构件ID`/`工作集`；`revit_set_phase.en.md:43` 含 `demolished_phase="现有"`。
- 译文校验只验"字段存在"不验"新鲜"：`tools/site/generate_features.py:143-153` 对 `contracts.yaml` 做了哈希绑定，对 `capabilities.yaml` 只断言字段在，陈旧译文可以过门禁。
- 术语冲突：`element` 译作「构件」374 次/「元素」52 次；`gate` 译作「门禁」56 次/「开关」2 次。
- 404 页 6 个内容链接全指向中文树（`docs/overrides/404.html:25-31`；`docs/overrides/partials/copyright.html:17,19` 是死条件分支），英文读者被送进中文页。

**事实准确性**
- 性能数字无 in-repo 证据：`docs/rebuild-performance.md:7` 自承未保留原始日志，165 s / 10 copies、286→185 s 这些数只能去外部 `validation-assets` 分支找；`analysis/`、`bench/` 里没有任何测量产物。

**IA / 交互**
- 移动端表格只能横着读：390px 下 253/288 页溢出内层滚动容器，最该读的「说明」列被挤到 462px 表宽里的 90px（`docs/stylesheets/extra.css:580-586`）。文档宽度本身正确，所以**看起来不像坏了**。
- `docs/platform/index.md` 是死胡同：它说两个面不能混用，却不链接任何一个已发布工具页；全站唯一的桥只朝一个方向。
- 跳转链接（skip link）在 `/`、`/en/`、`/404.html` 缺席（286/288 有），因为生成式落地页的 `h1` 没有 `id`（`docs/index.md:14`）。
- 首页"编辑此页"指向 `README.md`，改了也不生效：`docs/hooks.py:13` 与 `:50-53` 的 `SOURCES` 映射遮蔽了 `:54-66` 的落地页生成分支；`CONTRIBUTING.md:108` 还重复着这个错误指引。落地页真实来源是 `tools/site/landing.py:479-509`。
- `docs/platform/fork-tools.md:7-14` 8 行里 7 行没有页面可点（`:48` 只回 platform 索引）。

---

## P3 — 十一项

导航 `视图、图纸与明细表` 平铺 22 个工具、`查询与统计` 12 个、层级深达 4（`mkdocs.yml` nav 175 节点）；面包屑只写分组名不链接，无法横跳到兄弟工具（`tools/site/generate_features.py:322`、`platform_catalog.py:733`）；搜索无 suggest，索引 1,252,304 B raw / 237,178 B gzip 每次访问全量下载；`platform_catalog.py:662+671` 把 schema 的 `default ""` 渲染成「—」（影响 4 行 prefix/suffix）；`docs/validation.md:7` 漏列 R20 而 `ci.yml:76-83` 实际构建 R20/R22/R26/R27；`server/server.json` 把 `REVIT_MCP_HOST` 标 `isRequired:true` 但代码默认 `local`；`docs/roadmap.md:25` 的 registry 状态不可证；两套事实条 schema（`generate_features.py:250-259` vs `platform_catalog.py:692-696`），可用性靠名字相等推断。

---

## 已验证良好 — 不要把下面这些改回去

- **构建可复现**：`mkdocs build --strict -f mkdocs-lan.yml` 零警告、退出 0，`diff -rq site /tmp/site-repro` **零差异**。
- **一致性**：35/35 已发布页五段式完全统一；80/80 分支页两段式完全统一；缺通用参数段的 5 页（batch_* 与 build_report）确实没有通用字段，是正确变化。`generate_features.py --check` = 247 文件 0 变更，**没有手改过的生成页**。
- **事实准确**：35 个工具参数零不符（`tools.json` 与线上 `tools/list` 逐字节一致）；80 个分支页 schema 零不符（对照 `55d6ea5` 实测）；落地页 19/16/35、34/46/79+1、80 全部对；年份 2020·2022–2027 与 `csproj:15-16`、`release.yml` 一致；8 个 env 默认值全对。
- **双语**：nav 译文 52/52、无缺失无冗余、英文 nav 零 CJK 残留；4,535 个锚点零断链；结构对等 143/144；上一轮的 `接单`→`拾取` 修复仍成立（拾取 64、接单 0）。
- **可达性**：288/288 单一 `h1` 无层级跳跃；两主题对比度 AA（最低 4.57:1，正文 18.31/16.82）；420 个复制按钮全部有可访问名；表格键盘可滚；`prefers-reduced-motion` 生效；打印干净（A4 下表格 794/792）；抽屉惰性化、搜索对话框命名、`toc.follow` 均正常。
- **HTTP 基本盘**：288/288 sitemap URL 全 200；334 个引用资源全部解析；ETag/If-Modified-Since 真实 304；gzip 114,395 → 15,066 B，TTFB 2.1 ms；每目录 sitemap 修复仍成立；四种编码的路径穿越均被挡；零符号链接；404 是真 404 且深层可用。
- **性能**：首页 15 KB gz、工具页 12 KB gz、测试计划页 24 KB gz；图片已带 `width`/`height`/`loading="lazy"`/`decoding="async"`。

---

## 修复顺序

**第一批（半天，止血）**
1. `docs/platform/` 全 80 页加"未发布分支"横幅，删掉"当前版本是否已有"这一行 —— 消掉唯一 P0。
2. `serve-site.py` 目录补斜杠 301 —— 消掉重复 URL 与错位导航。
3. `mkdocs.yml` 加 `site_description` + 每页 `description`；`og:locale` 按 locale 取值 —— 让上一轮的元数据修复真正落地。
4. 删 `claude-desktop.gif`（-3.27 MB）与 `robots.txt`/`favicon.ico` 404 噪声。
5. `update-site.sh` 脏树时 `exit 1`。

**第二批（1–2 天，可信度）**
6. 环境变量表补 `REVIT_MCP_ANSWER_DIALOGS` 并写进农场步骤。
7. 重复工具页加生成式互链 + 统一 `<title>`（顺带消掉 10 组重复标题）。
8. 搜索按 locale 分索引；索引条目补工具标识符。
9. hreflang 改绝对 URL。
10. `rebuild-performance` 双语二选一，把记录放进去。
11. `hooks.py:13`/`:50-53` 的 `SOURCES` 移除 `README.md` 条目，修 `CONTRIBUTING.md:108`。

**第三批（下次迭代）**
12. 移动端表格 <600px 折叠默认值/类型列，说明列占满宽度。
13. `platform/index` 改成双向决策页。
14. 落地页 `h1` 加 `id` 修 skip link。
15. 统一两套事实条 schema，可用性从发布清单推导而非名字比对。
16. `capabilities.yaml` 也加哈希门禁。
17. 补 in-repo 测量产物，或从性能页撤掉未备份的数字。
18. nav 拆分 22 项平铺；面包屑链接分组锚点；搜索 suggest。

---

## 门禁该补什么

`check_site.py` 现在查的是"链接与锚点能否解析"（54,704 条，零错误），这解释了为什么上面 40 条问题一条都没被拦住。建议加四条断言：

1. **跨面一致性**：同名工具的参数集合必须相同，或页面上必须存在"本页为未发布分支"标记。
2. **元数据渲染**：每个构建页面必须有非空 `description`，`og:locale` 必须与页面语言一致。
3. **发布真实性**：线上 `site/` 的构建来源 commit 必须等于 `HEAD`，否则失败。
4. **标题唯一性**：`<title>` 不得重复。

这四条都是几十行的检查，能一次性把本轮 P0 与两个 P1 变成回归测试。

---

## 附：四轴报告

| 文件 | 轴 | 词数 | 分级 |
|---|---|---|---|
| [`http-hosting.md`](http-hosting.md) | HTTP/托管/服务端/发布链路 | 899 | 0/4/6/1 |
| [`i18n.md`](i18n.md) | 双语一致性与译文质量 | 1046 | 0/3/5/3 |
| [`accuracy.md`](accuracy.md) | 文档 vs 代码事实准确性 | 1014 | 0/1/1/4 |
| [`ux-ia.md`](ux-ia.md) | IA/UX/可达性/响应式/搜索 | 1080 | 0/3/5/4 |

上一轮（2026-10-03）的 [`REPORT.md`](../REPORT.md) 与 [`AUDIT.md`](../AUDIT.md) 已修项目本次全部复核通过，未重复计入；其 description 修复实际未生效，已归入 P1-1。
