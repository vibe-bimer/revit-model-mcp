# Issue 跟踪：GitHub

本仓库的 Issue 和规格说明以 GitHub Issue 的形式保存。所有操作使用 `gh` CLI。

<a id="conventions"></a>
## 约定

- **创建 Issue**：`gh issue create --title "..." --body "..."`。多行正文使用 heredoc。
- **读取 Issue**：`gh issue view <number> --comments`，用 `jq` 筛选评论，并同时获取标签。
- **列出 Issue**：`gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'`，配合适当的 `--label` 和 `--state` 过滤条件。
- **评论 Issue**：`gh issue comment <number> --body "..."`
- **添加／移除标签**：`gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **关闭 Issue**：`gh issue close <number> --comment "..."`

从 `git remote -v` 推断仓库——在克隆目录内运行时，`gh` 会自动完成这一点。

在本工作区中，`origin` 是 fork `vibe-bimer/revit-model-mcp`，`upstream` 是 `sharafutdinovdi/revit-model-mcp`。Issue 和工单在 fork 中跟踪。

<a id="pull-requests-as-a-triage-surface"></a>
## PR 是否作为分诊入口

**PRs as a request surface: no.** _（如果本仓库将外部 PR 视为功能请求，才改为 `yes`；`/triage` 会读取此标记。）_

设置为 `yes` 时，PR 使用与 Issue 相同的标签和状态，并使用对应的 `gh pr` 命令：

- **读取 PR**：`gh pr view <number> --comments`，并用 `gh pr diff <number>` 查看差异。
- **列出待分诊的外部 PR**：`gh pr list --state open --json number,title,body,labels,author,authorAssociation,comments`，只保留 `authorAssociation` 为 `CONTRIBUTOR`、`FIRST_TIME_CONTRIBUTOR` 或 `NONE` 的记录（排除 `OWNER` / `MEMBER` / `COLLABORATOR`）。
- **评论／打标签／关闭**：`gh pr comment`、`gh pr edit --add-label` / `--remove-label`、`gh pr close`。

GitHub 的 Issue 和 PR 共用编号空间，因此单独的 `#42` 可能指向任何一种——先用 `gh pr view 42` 解析，失败时再用 `gh issue view 42`。

<a id="when-a-skill-says-publish-to-the-issue-tracker"></a>
## 当技能要求“发布到 Issue 跟踪器”

创建一个 GitHub Issue。

<a id="when-a-skill-says-fetch-the-relevant-ticket"></a>
## 当技能要求“获取相关工单”

运行 `gh issue view <number> --comments`。

<a id="wayfinding-operations"></a>
## Wayfinding 操作

供 `/wayfinder` 使用。**地图（map）**是一张 Issue，**子 Issue（child）**作为工单。

- **地图**：一张带 `wayfinder:map` 标签的 Issue，正文包含 Notes / Decisions-so-far / Fog（笔记／当前决策／迷雾）区块。使用 `gh issue create --label wayfinder:map` 创建。
- **子工单**：通过 GitHub 子 Issue 关系挂到地图下（使用 `gh api` 调用子 Issue 端点）。如果未启用子 Issue，就将子工单加入地图正文的任务列表，并在子工单正文顶部写 `Part of #<map>`。标签为 `wayfinder:<type>`（`research` / `prototype` / `grilling` / `task`）。认领后，将工单分配给负责推进的开发者。
- **阻塞关系**：使用 GitHub **原生 Issue 依赖**，这是规范且在 UI 中可见的表示方式。用 `gh api --method POST repos/<owner>/<repo>/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>` 添加依赖边，其中 `<blocker-db-id>` 是阻塞工单的数字**数据库 ID**（通过 `gh api repos/<owner>/<repo>/issues/<n> --jq .id` 获取，_不是_ `#number` 或 `node_id`）。GitHub 会报告 `issue_dependencies_summary.blocked_by`（只统计未关闭的阻塞工单，是实时门禁）。若依赖功能不可用，则在子工单正文顶部用 `Blocked by: #<n>, #<n>` 行作为替代。只有所有阻塞工单都关闭后，当前工单才解除阻塞。
- **前沿查询**：列出地图下未关闭的子工单（`gh issue list --state open`，范围限定为地图的子 Issue／任务列表），排除仍有未关闭阻塞工单的记录（`issue_dependencies_summary.blocked_by > 0`，或 `Blocked by` 行中仍有未关闭 Issue），也排除已有人认领的记录；按地图顺序选择第一项。
- **认领**：`gh issue edit <n> --add-assignee @me`——这是本会话的第一次写操作。
- **解决**：先运行 `gh issue comment <n> --body "<answer>"`，再运行 `gh issue close <n>`，最后将上下文指针（gist + 链接）追加到地图的 Decisions-so-far 区块。
