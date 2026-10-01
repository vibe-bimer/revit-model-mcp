# Documentation hosting / 文档托管

The Linux host serves the reviewed bilingual build on port **8099**. The root is Chinese; `/en/` is English. The update timer runs every **900 seconds**.

Linux 主机在 **8099** 端口提供已审核的双语构建，根目录是中文，`/en/` 是英文；更新定时器每 **900 秒**执行一次。

| Script / 脚本 | Behavior / 作用 |
| --- | --- |
| `update-site.sh` | Verify the current MCP registry, generated translations and tests; build into `site.new`; check its links, anchors and language pairs; publish only if every check passes. / 校验当前工具注册表、译文及测试，构建 `site.new` 后检查链接、锚点与语言配对，全部通过才发布。 |
| `serve-site.sh <port>` | Start a LAN server on a free port and verify its content. / 仅在空闲端口启动局域网服务，并核实页面内容。 |
| `site-cron.sh` | Pull and publish only a clean checkout, including absence of untracked files; restart the serve unit when nothing answers and never kill another port owner. / 仅拉取、发布干净的工作区（也检查未跟踪文件）；无响应时重启 serve 单元，绝不终止占用端口的其他服务。 |
| `install-site-timer.sh [schedule]` | Prefer cron, then a systemd user timer, then a supervised loop; installs the refresh timer and the serve unit. / 优先 cron，其次 systemd 用户定时器，最后托管循环；同时安装刷新定时器与服务单元。 |

The documentation server runs as `revit-model-mcp-serve.service`, never as a child of the refresh job: a process started from the oneshot refresh unit is killed with its cgroup when that unit exits.

文档服务由 `revit-model-mcp-serve.service` 常驻提供，而不是刷新任务的子进程：从 oneshot 刷新单元启动的进程会随该单元的 cgroup 一起被回收。

```bash
scripts/install-site-timer.sh                       # every 15 minutes / 每 15 分钟
scripts/serve-site.sh 8099                          # serve manually / 手动服务
SITE_SKIP_PULL=1 scripts/update-site.sh             # publish checked local content / 校验并发布本地内容
systemctl --user status revit-model-mcp-serve.service   # is the site up? / 站点是否在线
```

When tools change, run `python tools/site/generate_features.py --dump`, review both languages in `capabilities.yaml` and the complete Chinese contracts in `contracts.yaml`, then run `--write`. A stale registry, translation hash, generated page, language pair or link blocks publication and leaves the old site online. The script also prevents concurrent publishers with `flock`.

工具变化后运行 `python tools/site/generate_features.py --dump`，审核 `capabilities.yaml` 的双语内容与 `contracts.yaml` 的完整中文契约，再运行 `--write`。注册表、译文哈希、生成页面、语言配对或链接未通过检查时，发布会被阻止，旧站点仍在线。脚本还通过 `flock` 防止并发发布。

Dependencies / 依赖：`docs/requirements.txt`, the Python server package / Python 服务器包, `curl`, `flock`, `ss`, Git. Logs / 日志：`~/.local/state/revit-model-mcp/site-update.log`.
