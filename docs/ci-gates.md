# CI 门禁与盲区

每次 push 和 PR 都会跑一组门禁，但它们各自只证明一件事。
这一页列出每道门禁证明什么、**不能**证明什么，以及 2026-10-31 那次事故暴露的盲区是如何补上的。

## 门禁链

| 门禁 | 位置 | 证明什么 |
| --- | --- | --- |
| 文档线存在性 | `tools/site/check_docs_line.py` | 发布所需的 15 个文件都在，且 `docs/features`、`docs/platform` 的工具页数量达标 |
| 双配置构建 | `tools/site/verify_dual_build.py` | `mkdocs.yml` 与 `mkdocs-lan.yml` 都能 `--strict` 构建，`check_site.py` 全绿，两次构建归一化后一致 |
| 生成器一致性 | `tools/site/generate_features.py --check` | 已提交的生成页与注册表、契约、目录清单一致 |
| 工具清单 | `ci.yml` 的 bundle job | `bundle/manifest.json` 的工具集合与 `docs/features/index.md` 列出的工具集合相同 |
| Python 测试 | `server/` 与 `tools/site/` | 服务器与站点工具的行为符合测试 |
| 预算 | `build/check_fork_budget.py` | 每个改动文件都归属于一个声明过的路径 |

## 每道门禁不能证明什么

- **双配置构建**只在配置仍指向存在的文件时才失败。
  删掉 `docs/platform/` 整棵子树，`mkdocs-lan.yml` 的 nav 指向一个不存在的文件 → 构建失败，这是它抓得到的。
  但如果删掉的是构建不依赖的文件（`scripts/serve-site.py`、`tools/site/check_site.py`、定时器脚本），构建照旧通过，CI 全绿。
- **生成器一致性**只比对已提交的生成页与当前注册表，它不检查生成器本身是否还在。
- **工具清单**只比对文档与 bundle 的集合是否相同；两边同时被删时它保持一致，因此不会报警。
- **预算**检查归属，不检查功能：一个文件被正确声明为 fork 路径，即使它已经没用了也不会失败。

## 2026-10-31 的事故

一次 rebase 线的合并把整条文档线从 `main` 上带走了：327 个文件消失，包括 `scripts/`、`tools/site/`、`docs/platform/` 与 `mkdocs-lan.yml`。
那一刻 CI 全绿——因为剩下的树仍然自洽：没有 nav 指向缺失文件，没有生成页与注册表冲突。
定时发布器在 13:46 完成了最后一次成功发布，14:01 起 `scripts/site-cron.sh` 已不存在，失败只写在本机日志里，直到第二天才被发现。

## 盲区是如何补上的

**存在性断言。** `tools/site/check_docs_line.py` 断言发布线所需的文件与最小页数，`ci.yml` 的 `docs-line` job 与 `docs.yml` 的第一步都会跑它。
它不关心构建是否成功，只关心这些文件还在。

**发布健康可见。** 发布器把每次尝试写进状态目录的 `manifest.json`，定时器把每次运行写进 `cron-status.json`，部署把它自己暴露成两个只读端点：

- `/status.json` — 同一份摘要的机器可读版本
- `/status.html` — 双语页面，异常时顶部横幅给出原因

摘要包含：最后一次尝试的结果与阶段、最后一次成功的 release、最后一次失败的原因、定时器最后一次运行、以及是否 stale（成功发布超过 26 小时、或定时器静默超过 2 小时）。
阈值可用 `SITE_STATUS_STALE_HOURS`、`SITE_STATUS_TIMER_SILENT_HOURS` 调整。

**巡检退出码。** `scripts/check-site-status.py` 读同一份摘要并给出退出码：`0` 健康、`1` 最后一次发布失败、`2` 已 stale。
`scripts/install-site-timer.sh` 会在 cron 分支里安装每小时一次的巡检，输出追加到 `site-update.log`；设置 `SITE_ALERT_WEBHOOK` 后，非健康状态会 POST 一份 JSON 到该 webhook。
巡检每次运行也写入 `watchdog-status.json`，因此状态页能显示巡检本身是否在跑。

## 判断一个门禁是否够用

问两个问题：

1. 这个门禁失败时，会有人在一小时内看到吗？
2. 这个门禁通过时，它排除了哪些"看起来正常"的坏状态？

第二问的答案就是盲区清单。门禁的价值不在它抓到了什么，而在它抓不到什么被写下来、并由另一道门禁覆盖。
