# W9 回执 — 门禁、发布演练与验收记录

- 票：#37 `docs: W9 enforce gates and record release verification`（spec #28 收口票）
- 分支 / worktree：`w9/gates-receipts` @ `/home/roky/revit-wt/w9`
- 基线：`d188736 merge: W8 referenced assets and error surfaces into the integration branch`（已含 W1–W8）
- 日期：2026-10-30 / 2026-10-31
- 本轮只做本地提交：**未 push、未改 GitHub issue、未触碰线上服务**（未跑 `publish_site.py --adopt`，未 start/stop/restart 任何 systemd 单元，未写 `/home/roky/revit-mcp/site`，未动 `~/.local/state/revit-model-mcp`）。

---

## 1. 结论

1. **合并门禁补齐了双部署配置**。此前 CI 只构建 `mkdocs.yml` 一份配置并跑一次 `check_site`；现在 `python tools/site/verify_dual_build.py` 一次完成：两份配置各自 `--strict` 构建 → 各自带自己的 `--base-url` 跑 `check_site` → 两棵产物做归一化后逐文件比对。页面数、资源数、工具数**没有任何断言**，比对的是「两棵树在抹掉部署差异后是否一致」。
2. **确定性比较有归一化函数与单测**：绝对 `site_url`、根相对前缀、robots 策略、gzip 流、清单里的时间戳与产物 ID 全部归一化，20 条单测覆盖（含「必须不动的」GitHub 仓库链接与正文样例）。
3. **发布链路的故障与并发行为可复现**：22 条黑盒测试覆盖并发锁、探测回滚、失败保留上一版、连续请求零窗口、同 commit no-op、保留 current+上一版、cron 四种结论、`--adopt` 接管。
4. **浏览器矩阵 84/84 通过**（3 视口 × 2 主题 × 2 语言 × 7 类页面），搜索、键盘、焦点、跳转、打印逐项实测。
5. **线上切换后冒烟未执行**——按票面要求由 Lead 执行，本回执给出可直接照做的 runbook（第 6 节，含回退步骤与必记字段）。

---

## 2. 门禁清单与运行结果

### 2.1 合并检查里现在跑什么

`.github/workflows/pr-checks.yml`（`quality` job，windows-latest）与 `.github/workflows/docs.yml`（`build` job）的 “Build documentation” 步骤：

```bash
python tools/site/generate_features.py --verify-registry --check   # 生成物与注册表一致
python -m unittest discover -s tools/site -p 'test_*.py'           # 生成器 + 站点 + 发布器行为测试
python tools/site/verify_dual_build.py                             # 双配置严格构建 + 双份 check_site + 归一化比对
```

`verify_dual_build.py` 内部展开为：

```bash
mkdocs build --strict -f mkdocs.yml     -d site
mkdocs build --strict -f mkdocs-lan.yml -d site-lan
python tools/site/check_site.py --site-dir site     --base-url https://vibe-bimer.github.io/revit-model-mcp/
python tools/site/check_site.py --site-dir site-lan --base-url http://192.168.100.120:8099/
# 归一化后逐文件比对 site 与 site-lan
```

其他改动：

- `docs.yml` 的 `paths` 触发器补上 `mkdocs-lan.yml`——此前改 LAN 配置不会触发文档工作流。
- `pr-checks.yml` 的 explain-failure 提示同步改为 `python tools/site/verify_dual_build.py`（原为 `mkdocs build --strict`，失败时给的建议命令会漏掉双配置与 check_site）。
- `docs.yml` 的 `upload-pages-artifact` 仍取 `site`（Pages 构建），`site-lan/` 只用于比对，不进产物；`.gitignore` 增加 `/site-lan/`。

> 备注（W1 曾担心的点）：CI 的 “Install documentation dependencies” 步骤本来就执行 `pip install -r docs/requirements.txt -e ./server`，server 包在文档构建环境里已可用，`generate_features.py --verify-registry` 不需要额外安装步骤。**此问题在 W1 时已被实际解决**，不是本轮新增。

### 2.2 本次真实运行结果

| 门禁 | 命令 | 结果 |
| --- | --- | --- |
| 全量行为测试 | `python3 -m unittest discover -s tools/site -p 'test_*.py'` | 319 tests OK（39.4s） |
| 生成物一致 | `python3 tools/site/generate_features.py --verify-registry --check` | 248 files checked，0 changed |
| 双配置严格构建 + 双份 check_site + 归一化比对 | `python3 tools/site/verify_dual_build.py` | 两份配置均 `--strict` 通过、`check_site` 各 0 error、比对 pass |
| 发布器演练 | `python3 -m unittest tools.site.test_publish_site -v` | 22 tests OK（27.0s），明细见 §4 |
| 工作流静态检查 | `actionlint`（v1.7.12，与本仓库 CI 同版本） | 退出 0，无输出 |

完整输出见 §2.3。`check_site` 在两份配置上的观测值相同：288 页（zh 144 / en 144）、56152 条内部引用、356 个资源（引用 21 + 约定 335）、0 错误。这些是**本次运行的观测值，不是断言**——门禁不固定页面/资源/工具数量（规格里 35 已发布工具、80 分支工具、27 同名工具只作基线）。

### 2.3 本次真实运行输出

```text
$ python3 -m unittest discover -s tools/site -p 'test_*.py'
Ran 319 tests in 39.363s
OK

$ python3 tools/site/generate_features.py --verify-registry --check
checked 248 generated files; 0 changed

$ python3 tools/site/verify_dual_build.py
+ .../mkdocs build --strict -f mkdocs.yml -d site
+ .../mkdocs build --strict -f mkdocs-lan.yml -d site-lan
+ python3 tools/site/check_site.py --site-dir site --base-url https://vibe-bimer.github.io/revit-model-mcp/
Pages: 288 (zh 144 / en 144); checked internal references: 56152
Assets: 356 shipped; referenced 21, conventional 335
Site/source errors: 0
check_site (pages, base https://vibe-bimer.github.io/revit-model-mcp/): pass
+ python3 tools/site/check_site.py --site-dir site-lan --base-url http://192.168.100.120:8099/
Pages: 288 (zh 144 / en 144); checked internal references: 56152
Assets: 356 shipped; referenced 21, conventional 335
Site/source errors: 0
check_site (lan, base http://192.168.100.120:8099/): pass
dual-config deterministic comparison: pass

$ actionlint        # v1.7.12，与 CI 同版本
(无输出，退出 0)
```

319 = W1–W8 的 299 条 + W9 新增的 20 条（`test_verify_dual_build.py`）。

### 2.4 归一化规则（确定性比较）

`tools/site/verify_dual_build.py`：

| 差异来源 | 归一化做法 | 反例（必须不被误伤） |
| --- | --- | --- |
| 绝对 `site_url` | 整串替换为 `<site-base>/` | — |
| 根相对前缀（`/revit-model-mcp/...`） | 只在引号锚定的位置去掉前缀：`"/revit-model-mcp/` → `"/` | `https://github.com/vibe-bimer/revit-model-mcp/...`（编辑入口）、`https://github.com/sharafutdinovdi/...`（fork 身份）、正文里的 `http://127.0.0.1:8000/revit-model-mcp/` 样例 |
| robots 策略 | 不做文本等同，按目标断言：Pages 版必须 `Allow: /` 且 `Sitemap: <pages base>sitemap.xml`；LAN 版必须 `Disallow: /` | — |
| `sitemap.xml.gz` | gzip 魔数 `\x1f\x8b` 解压后再归一化比较（两版 gzip 流字节不同、内容相同） | 非 UTF-8 的二进制原样比较 |
| 清单时间戳与产物 ID | JSON 解析后把 `built_utc`、`release_id`、`source_commit`、`tree_sha`、`tree_sha256` 置为 `<volatile>`，`verification` 整节置为 `<volatile-section>`，再按 key 排序重排 | 非 JSON 文本原样返回 |

同配置重复构建是**逐字节一致**的（无时间戳参与），所以「同配置两次构建必须相同」不需要归一化；归一化只为跨配置比较服务。

单测：`tools/site/test_verify_dual_build.py`，20 条，覆盖上述每一行，包括「前缀剥离不得碰 GitHub 仓库链接」「单引号属性」「根路径配置下前缀剥离为 no-op」「gzip 解压后一致」「文件集合不等要报告」「robots 三向断言」。

---

## 3. W1–W8 逐项状态

票号对应：W1 #29、W2 #31、W3 #32、W4 #30、W5 #33、W6 #34、W7 #35、W8 #36（均已 CLOSED），W9 #37。

| 包 | 票 | 交付 | 证据命令与结果 | 遗留 |
| --- | --- | --- | --- | --- |
| W1 版本与语言覆盖 | #29 | `catalogs.yaml` 声明版本/状态/来源 SHA/语言覆盖/所有权；分支页未发布横幅；同名页双向互链；按 inputSchema 结构（参数、required、类型、默认值、约束）比对差异 | `test_catalogs`(12)、`test_contract_diff`(12)、`test_platform`(29)、`test_check_site`(31) 全过；`check_site` 的 `audit_twin_hints` 零错误 | 无 |
| W2 元数据与编辑来源 | #31 | 生成页同语言 frontmatter；locale、hreflang、编辑入口从配置派生（不再手写）；元数据审计进 `check_site` | `test_metadata`(17) 全过；双配置下编辑入口指向真实维护源（本轮双构建复核） | 无 |
| W3 搜索与导航 | #32 | 版本感知搜索（当前语言优先、精确工具名优先、结果带状态）、全语言入口、目录双向入口、移植表落点；搜索索引与迁移表审计进 `check_site` | `test_search`(25) 全过；浏览器实测见 §5.2 | 英文侧走 Material 原生 worker，结果元信息文案与中文侧的自定义增强不同（§5.2 记录） |
| W4 HTTP 与缓存 | #30 | `serve-site.py`：目录 301 规范化、gzip 质量值协商（全排除 406）、按编码的强 ETag 与 `Vary`、304 重复校验器、`.xml.gz` 以 `application/gzip` 下载、非法/越界 URL 受控错误、按语言返回 404、资源缺失返回 14 字节纯文本 | `test_serve_site`(58) 全过（真起服务、真发 HTTP） | 无 |
| W5 发布隔离与恢复 | #33 | `publish_site.py`：`git archive` 干净导出 → 门禁 → 构建进不可变 release → 健康探测 → 原子翻转 `current` → 清理（保 current+上一版）；锁互斥；同步失败与构建失败分开退出码；`--adopt` 接管旧目录 | `test_publish_site`(22) 全过，明细见 §4 | 无 |
| W6 内容与译文可信度 | #34 | 译文指纹门禁（原文变更触发过期）、术语审计、环境变量适用性/性能来源/默认值/年份/路线图逐项校准 | `test_generate_features`(7)、`test_check_site` 的 `audit_terminology` 全过；`generate_features --verify-registry --check` 0 changed | 无 |
| W7 移动端与键盘阅读 | #35 | 首页与 404 的 skip link、表格语义、可滚动区域、对比度提升到 AA | `test_a11y`(34) 全过；浏览器矩阵（§5.1）零横滚、首个 Tab 为 skip link | 主题深浅切换靠 `prefers-color-scheme`，`emulateMedia` 不改 `body[data-md-color-scheme]`（§5.3 记录测法限制） |
| W8 资源与错误页 | #36 | 未引用 GIF 不进产物（构建失败）、按部署配置写 robots/favicon、英文错误页、资源缺失轻量纯文本错误；`audit_assets`/`audit_deployment` 进 `check_site` | `test_hooks`(24)、`test_site`(28) 全过；双配置 `check_site` 的 Assets/deployment 审计 0 错误 | 404 页语言入口指向某个工具页而非首页（§5.4） |
| W9 门禁与回执 | #37 | 双配置严格构建 + 双份 `check_site` + 归一化比对进合并检查；`verify_dual_build.py` + 20 条单测；本回执 | 见 §2、§4、§5 | 线上冒烟待 Lead 执行（§6） |

基线测试总数 299 条（W1–W8 交付），W9 新增 20 条 → 319 条。

---

## 4. 故障与并发演练汇总

命令：`python3 -m unittest tools.site.test_publish_site -v`（22 条，全部黑盒：真 `git`、真 `mkdocs`、真 HTTP、真 flock）。

| 演练 | 测试 | 观测 |
| --- | --- | --- |
| 并发互斥 | `ConcurrencyTests.test_a_second_publisher_is_rejected_by_the_lock` | 第二个发布进程拿不到锁，退出码 3，线上版本不变 |
| 连续请求零窗口 | `ZeroWindowTests.test_requests_never_fail_while_a_new_release_switches_in` | 切换期间持续 GET `/`：三次实测分别为 **88 / 89 / 86 次请求，0 次非 200**，响应体里同时出现旧版与新版内容（说明切换真的发生在请求流中间）。次数随机器速度浮动（票面基线记录 261 次），断言的是「0 失败」而不是次数；测试现在把请求数打进日志（`zero-window drill: N requests during the switch`） |
| 构建失败保留 | `FailureSemanticsTests.test_build_failure_keeps_the_served_site_and_records_the_reason` | 退出码 1，`current` 未动，状态文件记 `last_failure.stage` |
| 同步失败可区分 | `FailureSemanticsTests.test_sync_failure_is_a_distinguishable_non_success` | 退出码 2，与构建失败（1）不同 |
| 未知固定 commit | `FailureSemanticsTests.test_unknown_pinned_commit_is_a_sync_failure` | 退出码 2，不发布 |
| 探测失败回滚 | `HealthProbeTests.test_failed_probe_rolls_current_back_to_the_previous_release` | 退出码 4，`current` 翻回上一版，线上仍可用 |
| 探测标记可配 | `HealthProbeTests.test_probe_marker_is_configurable` | `SITE_HEALTH_MARKER` 生效 |
| 同 commit no-op | `NoOpTests.test_republishing_the_same_commit_is_a_recorded_no_op` | 不重建、不切换，状态记 `noop` |
| 保留 current + 上一版 | `ReleaseLayoutTests.test_old_releases_are_pruned_but_current_and_previous_survive`、`..._switch_keeps_the_previous_release_on_disk` | 清理后 `current` 与刚被切掉的那一版都在磁盘上 |
| 清单公开字段 | `ReleaseLayoutTests.test_release_carries_a_public_manifest` | `release_id`/`source_commit`/`source_resolution`/`tree_sha256`/`config`/`tools`/`built_utc`/`verification`，无凭据、无家目录绝对路径 |
| 脏工作树 | `DirtySourcePublishTests.test_dirty_development_tree_publishes_pinned_head_content` | 脏树不阻塞，产物来自 `git archive`，未提交改动不泄漏 |
| 发布根符号链接 | `DirtySourcePublishTests.test_publish_root_becomes_a_symlink_to_current` | 线上根指向 `current`，切换是一次 rename |
| 接管旧目录 | `AdoptTests` ×2 | `--adopt` 把普通目录搬进 `releases/<utc>-adopted/` 并补清单；根已是符号链接时拒绝 |
| cron 四种结论 | `CronTests` ×4 | 干净轮发布并验证；脏树只告警不跳过；锁被占用记「跳过」且单元仍绿；构建失败记「失败」并非零退出 |
| 真构建冒烟 | `RealMkdocsSmokeTests.test_a_real_build_produces_a_release_with_real_tool_versions` | 真跑 mkdocs 产出 release，清单记录真实工具版本 |
| 环境链接 | `EnvironmentLinkTests` ×2 | 检出目录里的 venv 被链进导出树；缺失的 venv 保持缺失 |

结果：`Ran 22 tests ... OK`。

---

## 5. 浏览器矩阵

环境：本地 `python3 scripts/serve-site.py 8123 <worktree>/site-lan`（就是 LAN 配置的真实产物），Playwright + 本地 chromium 1243。

### 5.1 组合矩阵：84/84 通过

3 视口（desktop 1440×900 / tablet 768×1024 / mobile 390×844）× 2 主题（light / dark）× 2 语言（zh 根路径 / en `/en/`）× 7 类页面 = 84 个组合。

页面：首页 `/`、同名两版工具 `/features/revit_export_view/` 与 `/platform/revit_export_view/`、长参数页 `/platform/revit_align_link_datums/`、目录 `/features/` 与 `/platform/`、404 `/no-such-page-w9/`。

每个组合的断言与结果：

| 断言 | 结果 |
| --- | --- |
| HTTP 状态（正常页 200、404 页 404） | 84/84 |
| `<html lang>` 与语言一致 | 84/84（404 例外，见 §5.4） |
| 存在单一 `h1` | 84/84 |
| 页面级横向滚动为 0（`scrollWidth - clientWidth == 0`） | 84/84 |
| skip link 存在且指向页内锚点 | 84/84 |
| 语言入口存在 | 84/84 |

> 首轮我自己的断言写错过两处，导致 66 个「失败」：①要求 skip link 一律 `href="#rmc-main"`——实际首页/404 用 `#rmc-main`（`docs/overrides/main.html:99` 注入），工具页与目录页用主题默认的「第一个 TOC 锚点」（`#_1`、`#png` 等），两者都合法；②要求 404 页 `lang="zh"`——404 是刻意做成中英并列的单页（“404 页面不存在 · Page not found”），由 mkdocs-static-i18n 渲染为 `lang="en"`。修正断言后 84/84 通过，**站点本身无缺陷**。

### 5.2 搜索

| 场景 | 观测 |
| --- | --- |
| 中文页搜 `revit_export_view` | 元信息「14 条结果 · 仅简体中文」（默认只搜当前语言）；第 1 条 `./features/revit_export_view/`「导出视图图片 · 已发布 0.9.0」，第 2 条 `./platform/revit_export_view/`「导出视图为 PNG · 未发布 · 集成分支」→ **精确工具名命中，发布版在前** |
| 中文页搜「导出视图」 | 「9 条结果 · 仅简体中文」，同样 features 在前、platform 在后 |
| 点「所有语言」 | 元信息变为「9 条结果」（语言过滤标记消失）→ 全语言入口可用 |
| 英文页搜 `revit_export_view` | 「28 matching documents」；结果里 features 版排第 4、platform 版排第 5 → **发布版仍在前**；首页/总览页排在前面是因为正文多次出现该词（相关度排序），非缺陷 |
| 英文页过滤按钮 | 存在（`All languages`） |

### 5.3 键盘、焦点、跳转、打印、主题

| 项 | 观测 |
| --- | --- |
| 首个 Tab 停靠 | `/features/revit_export_view/`：`A.md-skip`（`focus-visible`）文本「跳转至」，`href="#_1"` |
| Enter 后跳转 | URL 变为 `.../features/revit_export_view/#_1`，焦点落在 `id="_1"` 的元素上（该元素有 `tabindex`）→ skip link 真的把焦点送进正文 |
| 打印媒体 | `emulateMedia({media:'print'})` 下：横向滚动 0、`.md-header` `display:none`、`.md-sidebar` `display:none` → 无裁切、导航不占版面 |
| 主题 | 用 `emulateMedia({colorScheme})` 切换：布局断言在浅/深两态均通过，但 `body[data-md-color-scheme]` 始终是 `default`、背景色始终 `rgb(255,255,255)`。原因：Material 的配色由 `prefers-color-scheme` 媒体查询在 CSS 层驱动，而 `data-md-color-scheme` 反映的是**手动切换控件**的状态，`emulateMedia` 不会改它。**测法限制，如实记录**：矩阵里的「浅/深」是媒体查询两态，不是点击调色板开关后的两态 |

### 5.4 浏览器侧发现的既有小问题（非本轮引入，列入遗留）

1. **404 页的语言入口指向某个工具页**（中文入口指向 `/platform/revit_walls_from_cad/`，英文入口指向 `/en/platform/revit_walls_from_cad/`），不是首页——mkdocs-static-i18n 对没有对应译文的页面用 alternate 回退时挑了一个页面。入口可用但落点不理想。
2. **404 页 `lang="en"`**：中英并列的单页设计所致（同一页同时给两种语言的提示），对读屏语言标注不精确。
3. **本地测试环境的控制台 CORS 报错**：`navigation.instant` 会按配置里声明的 `site_url`（`http://192.168.100.120:8099/`）去取 `sitemap.xml`，从 `127.0.0.1:8123` 打开就是跨源。这是**本地起服务的必然产物**，真实部署下同源、不会出现。主题降级正常（站点地图为空即隐藏）。Lead 冒烟时请确认线上控制台干净。
4. **英文侧搜索走 Material 原生 worker**，中文侧走自定义增强（带语言过滤元信息与发布状态），两侧结果元信息文案不一致但功能都在。

---

## 6. 上线冒烟 runbook（**由 Lead 执行，W9 未执行**）

前提：隔离环境验收已通过（本回执 §2、§4、§5）。执行前确认没有其他发布在跑。
（2026-10-31 更新：#38 补记三个运行默认项的决定与验证，见 §6.4；§6.1、§6.3 的演练记录项同步补充。）

### 6.1 步骤

```bash
# 0. 记录基线（下面每一项都要填进 §6.3 的表）
STATE=${SITE_STATE_DIR:-$HOME/.local/state/revit-model-mcp}
readlink -f "$STATE/current"                      # 当前 release id
python3 -c "import json,sys;d=json.load(open('$STATE/manifest.json'));print(d['current_release'],d['last_success'])"
curl -sI http://192.168.100.120:8099/ | head -3    # 切换前线上仍可用

# 1. 确认工作流与门禁在目标 commit 上绿（CI 结果页）
#    pr-checks: "Build documentation" 通过；docs.yml: build + deploy 通过

# 2. 在主机上跑一次隔离演练（不碰线上根）
STATE_TMP=$(mktemp -d); ROOT_TMP=$(mktemp -d)
SITE_STATE_DIR=$STATE_TMP SITE_PUBLISH_ROOT=$ROOT_TMP/site \
  SITE_COMMIT=$(git rev-parse HEAD) scripts/update-site.sh ; echo "exit=$?"
#    期望 exit=0，$STATE_TMP/manifest.json 里 last_attempt.outcome=success，
#    current_manifest.source_resolution=pin，
#    current_manifest.server_environment.mode 为 uv-sync 或 linked（§6.4）

# 3. 正常发布（第一次需要接管线上普通目录，只做一次）
SITE_PUBLISH_ROOT=/home/roky/revit-mcp/site scripts/update-site.sh --adopt
SITE_COMMIT=$(git rev-parse HEAD) scripts/update-site.sh ; echo "exit=$?"

# 4. 冒烟（逐项记录）
curl -s  http://192.168.100.120:8099/ | grep -o '<title>[^<]*</title>'
curl -sI http://192.168.100.120:8099/features/revit_export_view/ | head -3   # 200
curl -sI http://192.168.100.120:8099/en/ | head -3                            # 200
curl -s  http://192.168.100.120:8099/robots.txt                               # Disallow: /
curl -sI -H 'Accept-Encoding: gzip' http://192.168.100.120:8099/ | grep -i 'content-encoding\|etag\|vary'
curl -sI http://192.168.100.120:8099/nope-w9/ | head -1                        # 404
# 浏览器：首页、/features/revit_export_view/、/platform/revit_export_view/、
#         /platform/revit_align_link_datums/、/features/、/platform/、404
#   逐页确认：无页面级横滚、skip link 首个 Tab、搜索精确工具名且发布版在前、
#            打印无裁切、控制台无报错（尤其无 sitemap 的 CORS/404）
systemctl --user status revit-model-mcp-serve.service --no-pager | head -5
```

### 6.2 回退

```bash
STATE=${SITE_STATE_DIR:-$HOME/.local/state/revit-model-mcp}
ls "$STATE/releases"                                   # 选上一版
ln -sfn "releases/<previous-id>" "$STATE/.current-manual"
mv -T "$STATE/.current-manual" "$STATE/current"        # 原子翻转
curl -sI http://192.168.100.120:8099/ | head -1        # 确认 200
# 或者：重发已知好 commit
SITE_COMMIT=<known-good-sha> scripts/update-site.sh
```

回退与发布是同一个动作（翻 `current` + 探测）；探测失败会自动把指针换回上一版，线上不会停在坏版本上。

### 6.3 必须记录的字段

| 字段 | 值（Lead 填） |
| --- | --- |
| 发布 release id | `<utcstamp>-<shortsha>` |
| 前一版 release id | `<utcstamp>-<shortsha>` |
| 源码 commit（`source_commit`） | `<sha>` |
| 解析方式（`source_resolution`） | `<pin / head / upstream>` |
| 服务器环境（`server_environment.mode`） | `<uv-sync / linked / absent>`；`linked` 时附 `fallback` 原因 |
| 切换时间（UTC） | `<YYYY-MM-DDTHH:MM:SSZ>` |
| 发布退出码 / 结论 | `<0 success / 4 rollback / 1 构建失败 / 2 同步失败>` |
| 冒烟结果（逐项） | `<标题/200/404/robots/gzip/浏览器 7 页>` |
| 是否回退 | `<否 / 是，原因>` |
| 状态文件快照 | `$STATE/manifest.json` 的 `current_release`、`last_attempt`、`last_success` |

### 6.4 三个运行默认项的决定（#38，2026-10-31 补记）

| 默认项 | 决定 | 实现与验证 |
| --- | --- | --- |
| `SITE_COMMIT` | **端到端支持固定 commit**。接受仓库内 `git rev-parse` 能解析的任意 revision（完整 sha、短 sha、tag、分支名，须已存在于本地仓库）；设置时不执行 fetch，导出、门禁、构建与清单全部使用该 commit，清单记 `source_resolution: "pin"`；未设置时发布分支远端顶端，无远端则发布本地 `HEAD`。 | 新增 `tools/site/test_publish_defaults.py` 3 个黑盒测试（HEAD 更新后仍发布 pin 内容、短 sha 解析、重复固定发布为 no-op）；演练（§8 命令）发布 pin 的旧 commit 并核对页面与清单。 |
| 导出树服务器环境 | **能自建就自建**：`PATH` 上有 uv 且导出树带 `server/pyproject.toml` 时，在导出树内跑 `uv sync`，从导出源码安装本包；否则回退为符号链接开发目录的 `server/.venv`，并在发布日志写明回退原因。所选路径记入清单 `server_environment`（`mode: uv-sync / linked / absent`，`fallback` 记原因）。`.venv-docs` 仍照旧从开发目录链接。 | 6 个单元测试（自建、sync 失败回退、半成品清理、无 uv 回退、皆无记 absent、无服务器工程）+ 3 个流程测试（清单字段与日志行）；主机实跑演练确认 `uv-sync` 路径。 |
| `SITE_KEEP_RELEASES` | **默认保持 3**。实测一个版本约 36 MB（35,548,718 字节），默认稳态约 110 MB；需增减用该环境变量，最小值 2（当前版与上一版必须保留），非整数或低于 2 在构建开始前以退出码 1、阶段 `config` 失败。 | 3 个测试（`SITE_KEEP_RELEASES=2` 保留数、`banana` 与 `1` 的响亮失败）；保留数由既有发布测试回归覆盖。 |

依据与细节见 `scripts/README.md` 的「Export server environment」一节与变量表；实现见 `scripts/publish_site.py`（`prepare_server_environment`、`keep_releases`）。

---

## 7. 明确延期的非必做体验项

| 项 | 为什么延期 | 建议归属 |
| --- | --- | --- |
| 404 页语言入口改为指向首页 | 需要改 static-i18n 的 alternate 回退或给 404 单独配 alternates；属体验打磨，不影响可达 | 后续小票 |
| 404 页语言标注（中英并列单页） | 同上，与页面设计绑定 | 后续小票 |
| 英文侧搜索与中文侧增强统一（元信息文案、发布状态标签） | 两侧都能用，统一是重构 | 后续小票 |
| 主题切换的自动化断言（点击调色板开关而非媒体查询） | 需要 Playwright 点击 `input[name="__palette"]` 并断言 `data-md-color-scheme` 变化；本轮用媒体查询两态覆盖 | 后续小票 |
| 双配置产物在 CI 里的缓存（`site-lan` 不缓存，重复构建约几十秒） | 收益小，先保证正确性 | 不做 |
| `docs/agents/**` 里补一篇「站点门禁维护」说明 | `docs/` 下内容属已发布站点，本轮不动 | 后续小票（若确实需要对外） |

---

## 8. 复现命令

```bash
cd /home/roky/revit-wt/w9

python3 -m unittest discover -s tools/site -p 'test_*.py'          # 全量行为测试
python3 tools/site/generate_features.py --verify-registry --check   # 生成物一致
python3 tools/site/verify_dual_build.py                             # 双配置门禁（真构建）
python3 tools/site/verify_dual_build.py --skip-build                # 只比对已有产物
python3 -m unittest tools.site.test_publish_site -v                 # 发布演练
python3 -m unittest tools.site.test_publish_defaults -v             # 三个默认项行为测试（#38）
python3 -m unittest tools.site.test_verify_dual_build -v            # 归一化/比对单测
actionlint                                                          # 工作流静态检查

# 浏览器复核（不碰线上）
python3 scripts/serve-site.py 8123 site-lan
```
