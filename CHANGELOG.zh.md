# 变更日志

从 0.4.0 开始，条目由 release-please 根据提交信息生成。

本页记录本项目所有值得关注的变更。
格式遵循 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)。
版本遵循[语义化版本规范](https://semver.org/spec/v2.0.0.html)。

!!! note "完整中文翻译与权威来源"
    本页逐条翻译英文 [CHANGELOG.md](CHANGELOG.md)，保留版本、日期、分类、Issue 和提交链接，不以摘要替代历史明细。release-please 维护的英文日志是发布记录的权威来源；不得手工修改英文日志或版本字段。中文页仅翻译已记录的变更，不增加发布声明或真机验证结论。

<a id="090-2026-09-30"></a>
## [0.9.0](https://github.com/vibe-bimer/revit-model-mcp/compare/v0.8.1...v0.9.0)（2026-09-30）

<a id="features"></a>
### 新功能

* **rebuild：** 从一个模型写出多份副本（[ca6b77b](https://github.com/vibe-bimer/revit-model-mcp/commit/ca6b77bde214f6282113e3368c3f88f1f5110f91)）。

<a id="bug-fixes"></a>
### 错误修复

* **farm：** 为每个实例提供独立的模型副本（[2357a7d](https://github.com/vibe-bimer/revit-model-mcp/commit/2357a7ddced77c1325230076bcc87e8417bbfcbd)）。
* **rebuild：** 在同一模型的各份副本之间清理已粘贴类型（[b9867de](https://github.com/vibe-bimer/revit-model-mcp/commit/b9867de130ff6b7f142bb9d171c52432cf19f621)）。
* **rebuild：** 确保每一批副本都完整生成（[20354ec](https://github.com/vibe-bimer/revit-model-mcp/commit/20354ecc6d009a96d8d4edfdfcefdca3555d885b)）。
* **rebuild：** 仅在映射确实失败时重复复制（[437b78b](https://github.com/vibe-bimer/revit-model-mcp/commit/437b78b027725e4139a52131e22ce793a60c7fbf)）。

<a id="performance"></a>
### 性能

* **rebuild：** 回答 Revit 的重名询问，而不是重命名模板（[5aaea7c](https://github.com/vibe-bimer/revit-model-mcp/commit/5aaea7c8b64bed81846b3b5d937b9960e2efa235)）。
* **rebuild：** 在逐元素处理前，先重试被拒绝的复制（[2bc8cc8](https://github.com/vibe-bimer/revit-model-mcp/commit/2bc8cc88ae762b523bf0796103e37aa6569984ee)）。
* **rebuild：** 复用已粘贴类型，并保留一份备份（[a15fdb8](https://github.com/vibe-bimer/revit-model-mcp/commit/a15fdb821e38c40a48140f806304d5b4de72bdf7)）。

<a id="081-2026-09-29"></a>
## [0.8.1](https://github.com/vibe-bimer/revit-model-mcp/compare/v0.8.0...v0.8.1)（2026-09-29）

<a id="bug-fixes_1"></a>
### 错误修复

* **actions：** 防止重建操作等待重名询问对话框（[13194e4](https://github.com/vibe-bimer/revit-model-mcp/commit/13194e4cd91938135311e36f3182fc40a188d3fc)）。

<a id="documentation"></a>
### 文档

* 记录导出、重置和重建工具的 Revit 2020 验证证据（[f1ea0f9](https://github.com/vibe-bimer/revit-model-mcp/commit/f1ea0f92ae04b5fbf647184566a8e8563aff7086)）。

<a id="080-2026-09-28"></a>
## [0.8.0](https://github.com/vibe-bimer/revit-model-mcp/compare/v0.7.0...v0.8.0)（2026-09-28）

<a id="features_1"></a>
### 新功能

* **actions：** 新增可试运行的元素 ID 重置功能（[0c8d92a](https://github.com/vibe-bimer/revit-model-mcp/commit/0c8d92aaf8a8147b061a1768fab5795997e9921d)）。
* **actions：** 重建模型，让 Revit 为每个元素分配新的 ID（[b1c0b5d](https://github.com/vibe-bimer/revit-model-mcp/commit/b1c0b5d408e1746c4e9a00777147a4c58dece0f3)）。
* **actions：** 为副本重新关联宿主、恢复连接，并报告重置成本（[a405693](https://github.com/vibe-bimer/revit-model-mcp/commit/a405693fe07a29af90964714c2d7b8ed87876566)）。
* **read：** 将元素标识符清单导出到工作簿（[6fb4560](https://github.com/vibe-bimer/revit-model-mcp/commit/6fb456010c128b23fc83aedc2921303a7e783466)）。

<a id="bug-fixes_2"></a>
### 错误修复

* **actions：** 将系统成员集合按元素读取，并检查连接器（[dc9d34c](https://github.com/vibe-bimer/revit-model-mcp/commit/dc9d34c405eedef34e573e3414d9dcc45d4558d6)）。
* **actions：** 拒绝所有 MEP 系统成员，而不仅是 MEP 曲线（[c81fa91](https://github.com/vibe-bimer/revit-model-mcp/commit/c81fa91dac1f50eb2ee38eba1546b0270b6bf782)）。
* **actions：** 在各自的子事务中替换每个元素（[c0ac48a](https://github.com/vibe-bimer/revit-model-mcp/commit/c0ac48a207e3d86b4ec8a3c0b8678a6ab1ea4545)）。
* **bundle：** 在 bundle 清单中列出新的导出工具（[aa7f8ce](https://github.com/vibe-bimer/revit-model-mcp/commit/aa7f8ce5b6698eb33a90938e844707885eb251f0)）。
* **read：** 将草图线和辅助线排除在构件清单之外（[a141ea1](https://github.com/vibe-bimer/revit-model-mcp/commit/a141ea1fc2cd9f4430da5ec07e3ec30fd099030b)）。

<a id="070-2026-09-28"></a>
## [0.7.0](https://github.com/vibe-bimer/revit-model-mcp/compare/v0.6.0...v0.7.0)（2026-09-28）

<a id="features_2"></a>
### 新功能

* **channel：** 报告插件构建版本（[155a7e9](https://github.com/vibe-bimer/revit-model-mcp/commit/155a7e9ef514afd10cb9d2b6481091565cd13e84)）。

<a id="bug-fixes_3"></a>
### 错误修复

* **server：** 显示插件构建信息，并停止阻塞心跳写入（[5c9f4c1](https://github.com/vibe-bimer/revit-model-mcp/commit/5c9f4c13fee05fa77ccc678eb06f96f863e37aea)）。

<a id="060-2026-09-28"></a>
## [0.6.0](https://github.com/vibe-bimer/revit-model-mcp/compare/v0.5.0...v0.6.0)（2026-09-28）

<a id="features_3"></a>
### 新功能

* **actions：** 新增 `revit_create_floor` 动作工具（[a63c580](https://github.com/vibe-bimer/revit-model-mcp/commit/a63c580cab5829ca424c48276cc192ca3f10b0e8)）。
* **actions：** 新增 `set_phase` 和 `merge_phases` 工具（[afd83c0](https://github.com/vibe-bimer/revit-model-mcp/commit/afd83c0526072f6314a1b18a9efd6a636286d915)）。
* **addin：** 新增 Revit 2020 支持（[14ed865](https://github.com/vibe-bimer/revit-model-mcp/commit/14ed8657aec52e589cdc60c9ef137f408101738e)）。
* **channel：** 根据任务 ID 关联响应，并以原子方式发布（[#61](https://github.com/vibe-bimer/revit-model-mcp/issues/61)，[5a65afc](https://github.com/vibe-bimer/revit-model-mcp/commit/5a65afc47789f07c2df495e2779e69dafd2e58b0)）。
* **read：** 在文档信息中公开文档的 `isModified`（[04550e4](https://github.com/vibe-bimer/revit-model-mcp/commit/04550e43edc1a6e8ebd496da22de4d67633683a9)）。

<a id="bug-fixes_4"></a>
### 错误修复

* **addin：** 将写入动作指向寻址的文档，而不是当前活动文档（[#60](https://github.com/vibe-bimer/revit-model-mcp/issues/60)，[d558ee9](https://github.com/vibe-bimer/revit-model-mcp/commit/d558ee955e29f60a194d7280df88791c2fc9c1d9)）。
* **ci：** 断言已安装年份数与 CI 实际构建数量一致（[ca65487](https://github.com/vibe-bimer/revit-model-mcp/commit/ca6548752f73dc725aefff7a996cabfd18dfce04)）。
* 解决人工测试中的读取及 HTTP 安装失败（[#45](https://github.com/vibe-bimer/revit-model-mcp/issues/45)，[61bd2ba](https://github.com/vibe-bimer/revit-model-mcp/commit/61bd2ba13c1c668b0a3d5e53f06ee6a8011f4292)）。

<a id="documentation_1"></a>
### 文档

* 添加 Revit API 语料库工作流程和项目分析（[e0b821a](https://github.com/vibe-bimer/revit-model-mcp/commit/e0b821a535d301be30430c57ad6aeaf1caf77dd0)）。
* 修正 Linux 构建标志，并记录部署经验（[e0848f8](https://github.com/vibe-bimer/revit-model-mcp/commit/e0848f88e7344c8fd669d0c171650d50a8feb4b9)）。
* 记录 Linux 下 `dotnet format` 的替代方案（[679b4fc](https://github.com/vibe-bimer/revit-model-mcp/commit/679b4fcff154b3b6af02bf63f7e55a80c9b1f0c6)）。
* 记录 Revit 2020 支持（[5ac9a55](https://github.com/vibe-bimer/revit-model-mcp/commit/5ac9a55ce5804cda986ddb31f6c4986ca40121ac)）。
* 枚举动作工具，并链接工具新增指南（[f437d63](https://github.com/vibe-bimer/revit-model-mcp/commit/f437d639963c4fb8cd2b25519ad794a8ac11136d)）。
* 记录插件签名和自动重启流程（[e4139f3](https://github.com/vibe-bimer/revit-model-mcp/commit/e4139f30a51248b9d524bd220f8b9395dd71a754)）。
* 记录已经确定的 Revit 阶段 API 限制（[b820aaf](https://github.com/vibe-bimer/revit-model-mcp/commit/b820aaf2366413732668e25eb052a8540f514b8d)）。
* 要求远程重启 Revit 前检查 `isModified`（[70b6582](https://github.com/vibe-bimer/revit-model-mcp/commit/70b6582002e5f3df5e8eeb22e798671df47dbc7a)）。

<a id="050-2026-09-14"></a>
## [0.5.0](https://github.com/sharafutdinovdi/revit-model-mcp/compare/v0.4.0...v0.5.0)（2026-09-14）

<a id="features_4"></a>
### 新功能

* 为目录审核准备桌面 bundle（[#40](https://github.com/sharafutdinovdi/revit-model-mcp/issues/40)，[fcd5db9](https://github.com/sharafutdinovdi/revit-model-mcp/commit/fcd5db91a52c904193d86f1ba804e25161ec6a32)）。

<a id="bug-fixes_5"></a>
### 错误修复

* 使用每个年份可用的最低 Revit API 构建版本作为目标（[#42](https://github.com/sharafutdinovdi/revit-model-mcp/issues/42)，[e17d8a7](https://github.com/sharafutdinovdi/revit-model-mcp/commit/e17d8a75be7ea9db058a5478537c2c3449ebfa67)）。

<a id="040-2026-09-14"></a>
## [0.4.0](https://github.com/sharafutdinovdi/revit-model-mcp/compare/v0.3.0...v0.4.0)（2026-09-14）

<a id="features_5"></a>
### 新功能

* 添加 Claude Desktop bundle、发布来源证明和 Scorecard（[#34](https://github.com/sharafutdinovdi/revit-model-mcp/issues/34)，[15f1ff4](https://github.com/sharafutdinovdi/revit-model-mcp/commit/15f1ff4710b971d2f29f5b8558050207c2f9f05b)）。

<a id="documentation_2"></a>
### 文档

* 添加品牌标志、分组文档导航，并移除过时安装说明（[#21](https://github.com/sharafutdinovdi/revit-model-mcp/issues/21)，[5f5e67b](https://github.com/sharafutdinovdi/revit-model-mcp/commit/5f5e67b69638b8279e44ad1161e2a9aa38453816)）。
* **brand：** 将标志改为叠放的楼板（[#22](https://github.com/sharafutdinovdi/revit-model-mcp/issues/22)，[5003907](https://github.com/sharafutdinovdi/revit-model-mcp/commit/5003907a165cb3cf7d72b77e590f899d099323ad)）。

<a id="030-2026-09-13"></a>
## [0.3.0] - 2026-09-13

<a id="added"></a>
### 新增

- 使用 MkDocs Material 的 GitHub Pages 文档，包括服务器参考、搜索，以及 llms.txt 和 llms-full.txt 导出。
- Contributor Covenant 2.1，以及面向编码 Agent 的仓库说明。
- 从带标签的变更日志小节提取发布亮点，并提供直接安装链接。
- 单用户和多用户 MSI 发布资产，以及 CI 中的解包、安装和卸载冒烟测试。
- 按年份 ZIP、MSI、Python wheel 和源码发行包的 SHA256 校验和。
- 稳定发布通过 GitHub OIDC 进行 PyPI 可信发布，以及尽力而为的 MCP Registry 发布。
- MCP Registry 清单，以及适用于 Claude Code 和 Claude Desktop 的 uvx 配置。
- WinGet 清单模板、生成、校验，以及通过 `WINGET_TOKEN` 可选提交。

<a id="changed"></a>
### 变更

- README 展示安装与分组工具；详细动作、安全和验证参考放在 `docs/` 中。
- 贡献指南加入测试覆盖和发布流程。

<a id="fixed"></a>
### 修复

- Python 发行包包含 MIT 许可证文件，并声明已经测试的 Python 3.13 支持。

<a id="020-2026-09-12"></a>
## [0.2.0] - 2026-09-12

<a id="added_1"></a>
### 新增

- Revit 2027 构建配置及 CI／发布打包。
- `install.ps1`，支持构建／发布来源、可选程序集签名和 Claude Code 注册。
- 默认只读协调工具：`revit_model_health`、`revit_links_status`、`revit_shared_coordinates` 和 `revit_parameter_fill_check`。
- `revit_move`、`revit_place_family`、`revit_create_wall`、`revit_set_parameter` 和 `revit_delete` 的 `dry_run`：成功的预览在事务内执行，随后回滚，并返回同样的校验块。
- `verification`：变更前采集 `before`，提交后重新读取 `after`（试运行则在回滚前读取）。
- 提交后重新读取失败时返回 `verification.error`。
- `revit_batch`：在单个 `TransactionGroup` 中最多执行 50 个动作，合并为一次撤销，在第一个步骤失败时回滚。

<a id="changed_1"></a>
### 变更

- README 快速入门使用安装脚本。
- MCP 握手版本来自包元数据。
- `install.ps1` 在缺少某个 Revit 年份的发布资产时给出清楚提示。

<a id="010-2026-09-11"></a>
## [0.1.0] - 2026-09-11

<a id="added_2"></a>
### 新增

- Windows Revit 插件，包含 Revit 2022–2026 构建配置。
- Python MCP 服务器，提供 14 个默认读取工具，覆盖目录、查询、聚合、参数、警告、关系、视图和实例发现。
- PNG 视图导出，以及以模型毫米为单位的可选元素几何信息。
- 八个主动启用的动作工具，由服务器标志和工作站门禁文件保护。
- 面向远程工作站的本地 PowerShell、SSH 文件通道及带认证 HTTP 传输。
- 每用户 HTTP 令牌、回环监听器、路径脱敏和可配置通道目录。
- Core 测试、服务器测试，以及 Revit 2022 和 2026 的 CI 产物。
- 标签触发的五个 Revit 版本发布打包，以及一个 Python wheel。
- 安装、传输、协议、安全及贡献文档。
