# Documentation hosting / 文档托管

The Linux host serves the reviewed bilingual build on port **8099**. The root is Chinese; `/en/` is English. The update timer runs every **900 seconds**.

Linux 主机在 **8099** 端口提供已审核的双语构建，根目录是中文，`/en/` 是英文；更新定时器每 **900 秒**执行一次。

## Release layout / 发布布局

A publish never edits the served directory. It exports a fixed commit into a temporary tree, builds into an immutable release directory, and flips a `current` symlink. The served root is a symlink to that pointer, so a switch is one atomic rename.

发布过程从不就地改写线上目录：它把固定 commit 导出到临时树，构建进不可变的发布目录，再翻转 `current` 符号链接；线上根目录是指向该指针的符号链接，因此切换只是一次原子 rename。

```
${SITE_STATE_DIR:-${XDG_STATE_HOME:-$HOME/.local/state}/revit-model-mcp}/
  releases/<utcstamp>-<shortsha>/   immutable build + manifest.json
  releases/<utcstamp>-adopted/      a legacy directory taken over by --adopt
  current -> releases/<id>          atomic pointer, flipped with rename
  manifest.json                     latest status: attempt, success, failure
  publish.lock                      flock held for the whole publish
  site-update.log                   timer log
<repo>/site -> state/current        served root (SITE_PUBLISH_ROOT)
```

`current` and the previous release are always kept; older releases are pruned to `SITE_KEEP_RELEASES` entries. Pruning never removes the release a request may still be reading from the previous switch.

`current` 与上一版始终保留，更旧的版本按 `SITE_KEEP_RELEASES` 清理；清理不会删掉刚被切换掉的上一版，避免打断在途请求。

## Scripts / 脚本

| Script / 脚本 | Behavior / 作用 |
| --- | --- |
| `update-site.sh` | Thin wrapper: runs `publish_site.py` for this checkout. / 薄壳：对本仓库运行 `publish_site.py`。 |
| `publish_site.py` | The publisher: resolve target commit, export, gate, build, probe, switch, prune. / 发布器：解析目标 commit、导出、校验、构建、探测、切换、清理。 |
| `serve-site.sh <port>` | Start a LAN server on a free port and verify its content. / 仅在空闲端口启动局域网服务，并核实页面内容。 |
| `site-cron.sh` | Timer entry: publish, then verify something answers on the port; restarts the serve unit only when nothing does, and never kills another port owner. / 定时入口：发布后核实端口有响应，仅在无人响应时重启 serve 单元，绝不终止占用端口的其他服务。 |
| `install-site-timer.sh [schedule]` | Prefer cron, then a systemd user timer, then a supervised loop; installs the refresh timer and the serve unit. / 优先 cron，其次 systemd 用户定时器，最后托管循环；同时安装刷新定时器与服务单元。 |

The documentation server runs as `revit-model-mcp-serve.service`, never as a child of the refresh job: a process started from the oneshot refresh unit is killed with its cgroup when that unit exits.

文档服务由 `revit-model-mcp-serve.service` 常驻提供，而不是刷新任务的子进程：从 oneshot 刷新单元启动的进程会随该单元的 cgroup 一起被回收。

## Exit codes / 退出码

| Code | Meaning / 含义 | Timer / 定时器 |
| --- | --- | --- |
| 0 | Published, or the target commit is already current (no-op, recorded). / 已发布，或目标 commit 已是当前版本（no-op，有记录）。 | success / 成功 |
| 1 | Build, gate, export or publish-root failure; the served release is unchanged. / 构建、校验、导出或发布根失败，线上版本不变。 | failure / 失败 |
| 2 | Sync failure: the fetch or the pinned commit could not be resolved. / 同步失败：拉取失败或固定 commit 无法解析。 | failure / 失败 |
| 3 | Another publish holds `publish.lock`. / 另一个发布进程持有 `publish.lock`。 | logged skip, exit 0 / 记为跳过，退出 0 |
| 4 | The post-switch health probe failed and `current` was rolled back. / 切换后健康探测失败，`current` 已回滚。 | failure / 失败 |

A skip and a failure are never the same event: the log says `publish skipped: another publish is in progress` and the unit stays green, while every other failure logs `publish failed` or `run failed` and exits nonzero.

跳过与失败绝不混同：锁被占用时日志写 `publish skipped: another publish is in progress` 且单元保持绿色；其余失败记录 `publish failed` / `run failed` 并以非零退出。

## Status file and manifests / 状态与清单

`<state>/manifest.json` records the latest state of the site, not a history:

`<state>/manifest.json` 记录站点最近状态（不是历史）：

| Field | Content / 内容 |
| --- | --- |
| `schema` | `revit-model-mcp.site-status/v1`. |
| `current_release` | Release id the pointer names. / 指针指向的发布 id。 |
| `current_manifest` | Copy of that release's manifest, plus `verification.health_probe`. / 该版清单副本，另加健康探测结论。 |
| `last_attempt` | `utc`, `target_commit`, `release_id`, `outcome` (`success`/`noop`/`adopt`/`failure`), `stage`. |
| `last_success` | `utc`, `release_id`, `source_commit`, `noop`. |
| `last_failure` | `utc`, `stage`, `reason`. Kept after a later success as the last known failure. / 之后成功也保留，表示最近一次失败。 |

Each release carries its own `manifest.json` (`revit-model-mcp.site-manifest/v1`): `release_id`, `source_commit`, `source_resolution` (`pin`/`head`/`upstream`/`adopt`), `tree_sha256` (paths and bytes of the built tree), `config` (config file name and hash), `tools` (python and builder versions), `built_utc`, and `verification` (per-gate `pass`/`absent`, plus `health_probe` in the status copy). No credentials, no absolute home paths.

每版自带 `manifest.json`（`revit-model-mcp.site-manifest/v1`）：发布 id、源码 commit、解析方式、构建树内容哈希、配置文件名与哈希、工具版本、UTC 时间、各校验项结论；不含凭据，也不含家目录绝对路径。

## Environment variables / 环境变量

| Variable | Default | Meaning / 含义 |
| --- | --- | --- |
| `SITE_STATE_DIR` | `${XDG_STATE_HOME:-$HOME/.local/state}/revit-model-mcp` | State root: releases, current, status, lock, log. / 状态根。 |
| `SITE_PUBLISH_ROOT` | `<repo>/site` | Served root; a symlink to `<state>/current` after migration. / 线上根目录。 |
| `SITE_REPO` | script parent | Checkout to publish; drills point it at a throwaway repository. / 要发布的仓库，演练时指向临时仓库。 |
| `SITE_COMMIT` | unset | Pin the published commit instead of the branch tip. / 固定发布某个 commit。 |
| `SITE_SKIP_PULL` | `0` | `1` publishes the local `HEAD` without fetching. / `1` 表示不拉取，直接发布本地 `HEAD`。 |
| `SITE_KEEP_RELEASES` | `3` | Releases to keep, never fewer than current plus previous. / 保留的版本数。 |
| `SITE_HEALTH_MARKER` | `Revit Model MCP` | Text the health probe requires in the home page. / 健康探测要求的首页文本。 |
| `MKDOCS` | auto-discovered | Builder command; a command line is split, not evaluated. / 构建命令，按词拆分，不做 eval。 |
| `MKDOCS_CONFIG` | `<export>/mkdocs-lan.yml` | Config file, relative to the exported tree. / 配置文件。 |
| `PYTHON` | `python3` | Interpreter for the publisher and the gates. / 解释器。 |
| `SITE_PUBLISH_RUNNING` | unset | Set for the nested test gate so the publisher's own tests skip themselves. / 发布器在导出树内跑测试时设置，避免递归。 |

A dirty development tree is not a reason to skip: the export comes from `git archive`, so uncommitted edits neither block publishing nor leak into the release.

开发树是否干净不再影响发布：产物来自 `git archive`，未提交的改动既不会阻塞发布，也不会混进发布内容。

## Migration / 迁移

The live root `/home/roky/revit-mcp/site` is still a plain directory. Rehearse in isolation first, then adopt:

线上根目录 `/home/roky/revit-mcp/site` 目前仍是普通目录。先在隔离环境验收，再执行接管：

```bash
# 1. Rehearse: throwaway state, publish root and port. / 隔离演练
STATE=$(mktemp -d); ROOT=$(mktemp -d)
SITE_STATE_DIR=$STATE SITE_PUBLISH_ROOT=$ROOT/site SITE_COMMIT=$(git rev-parse HEAD) \
  scripts/update-site.sh
SITE_PORT=<free port> python3 scripts/serve-site.py <free port> $ROOT/site &

# 2. Adopt the real directory into a release; the bytes are kept. / 接管线上目录，内容保留
SITE_PUBLISH_ROOT=/home/roky/revit-mcp/site scripts/update-site.sh --adopt

# 3. Publish a real release on top of the adopted one. / 在接管版本之上发布真实版本
SITE_COMMIT=$(git rev-parse HEAD) scripts/update-site.sh
```

`--adopt` renames the directory aside, points the served root at `current`, then moves the bytes into `releases/<utcstamp>-adopted/` with a manifest of its own. The served path is missing for two renames, not for a copy, and the adopted release stays on disk, so rollback is a symlink flip.

`--adopt` 先把目录改名挪开、把线上根指向 `current`，再把内容移进 `releases/<utcstamp>-adopted/` 并补一份清单。线上路径只在两次 rename 之间短暂缺失，不是整段拷贝时间；接管版本保留在磁盘上，回滚只需翻转符号链接。

Risks to accept before adopting: the timer and the serve unit must be idle during the two renames (a request in that window gets a 404); `revit-model-mcp-serve.service` keeps its `ExecStart` path, which now resolves through the symlink per request, so no restart is required but a restart is the safest check; and the adopted release has no `source_commit`, so the first real publish is what pins the site to a commit.

接管前需接受的代价：两次 rename 期间定时器与服务需空闲（该窗口内的请求会 404）；serve 单元仍用原 `ExecStart` 路径，经符号链接按请求解析，无需重启，但重启一次最稳；接管版本没有源码 commit，站点与某个 commit 的绑定从第一次真实发布开始。

## Rollback / 回滚

```bash
STATE=${SITE_STATE_DIR:-$HOME/.local/state/revit-model-mcp}
ls "$STATE/releases"                                  # what is available / 可用版本
ln -sfn "releases/<older-id>" "$STATE/.current-manual"
mv -T "$STATE/.current-manual" "$STATE/current"       # atomic pointer flip / 原子翻转
scripts/update-site.sh SITE_COMMIT=<commit>           # or republish a known commit / 或重发已知 commit
```

Rollback is the same operation as publishing: flip `current` and probe. A failed probe restores the previous pointer automatically, so the served site never ends up on a broken release.

回滚与发布是同一动作：翻转 `current` 并探测。探测失败会自动把指针换回上一版，线上不会停留在坏版本上。

## Checks / 校验

```bash
scripts/install-site-timer.sh                       # every 15 minutes / 每 15 分钟
scripts/serve-site.sh 8099                          # serve manually / 手动服务
SITE_SKIP_PULL=1 scripts/update-site.sh             # publish local HEAD / 发布本地 HEAD
SITE_COMMIT=$(git rev-parse origin/main) scripts/update-site.sh   # publish a pinned commit / 发布固定 commit
systemctl --user status revit-model-mcp-serve.service   # is the site up? / 站点是否在线
```

`serve-site.py` answers over HTTP/1.1: an existing directory reached without a trailing slash, and an explicit `index.html` URL, redirect (301) to the canonical directory URL while keeping the query string; gzip is negotiated from `Accept-Encoding` and a fully excluded set answers 406; responses carry per-encoding strong ETags, `Vary: Accept-Encoding` and a 304 that repeats both. Stored `*.xml.gz` archives download as `application/gzip` and are never recompressed. Only filenames carrying a content hash cache for a year; everything else revalidates. A miss for a page returns the site's own `404.html`, and a miss under `/en/` returns `en/404.html`, which puts the English entries first; a miss for an asset — an asset suffix or an asset directory — returns 14 bytes of `text/plain` with `no-store` instead of a 100 KB page. `robots.txt` never takes part in that decision: it is an indexing hint, not access control.

`serve-site.py` 以 HTTP/1.1 提供构建产物：已存在的目录在缺少尾斜杠或使用显式 `index.html` 地址时以 301 跳转到规范目录地址并保留查询串；按 `Accept-Encoding` 协商 gzip，全部表示被排除时返回 406；响应带按编码区分的强 ETag、`Vary: Accept-Encoding`，304 同样重复这两项；存储的 `*.xml.gz` 以 `application/gzip` 下载且不二次压缩；仅文件名含内容哈希的资源缓存一年，其余走重新验证。页面缺失返回站点自己的 `404.html`，`/en/` 下缺失返回 `en/404.html`（英文入口在前）；资源缺失（资源后缀或资源目录）只返回 14 字节 `text/plain` 并带 `no-store`，不再回一整页。`robots.txt` 不参与该判断：它是索引提示，不是访问控制。

### Merge gate / 合并门禁

Both deployment configs are gated, not just the Pages one. `tools/site/verify_dual_build.py` builds `mkdocs.yml` and `mkdocs-lan.yml` under `--strict`, runs `check_site.py` on each output with that config's own `--base-url`, then compares the two trees file for file after normalizing the deployment base (absolute `site_url`, root-relative prefixes, robots policy, gzip streams, and the volatile timestamp and release ids inside manifests). CI runs it in place of a single `mkdocs build --strict`; a local run is the same command.

两份部署配置都受门禁约束，不只是 Pages 那份。`tools/site/verify_dual_build.py` 以 `--strict` 分别构建 `mkdocs.yml` 与 `mkdocs-lan.yml`，对两份产物各带自己的 `--base-url` 跑 `check_site.py`，再把两棵树按部署基址归一化（绝对 `site_url`、根相对前缀、robots 策略、gzip 流、清单里的时间戳与发布 id）后逐文件比对。CI 用它取代单份 `mkdocs build --strict`；本地复核就是同一条命令。

```bash
python tools/site/verify_dual_build.py              # build both, check both, compare
python tools/site/verify_dual_build.py --skip-build # compare existing site/ and site-lan/
```

The comparison asserts no fixed page, asset or tool count: it asserts that the two outputs agree once the deployment difference is erased. `site-lan/` is build output and is ignored by Git.

比对不断言固定的页面、资源或工具数量，只断言「抹掉部署差异后两份产物一致」。`site-lan/` 是构建产物，已加入 `.gitignore`。

When tools change, run `python tools/site/generate_features.py --dump`, review both languages in `capabilities.yaml` and the complete Chinese contracts in `contracts.yaml`, then run `--write`. A stale registry, translation hash, generated page, language pair or link blocks publication and leaves the old site online. Those gates now run on the exported tree, and each one is recorded in the release manifest.

工具变化后运行 `python tools/site/generate_features.py --dump`，审核 `capabilities.yaml` 的双语内容与 `contracts.yaml` 的完整中文契约，再运行 `--write`。集成分支的 80 个工具页在 `docs/platform/`，由 `platform_catalog.py` 从 `platform-tools.json` 生成；刷新快照用 `python tools/site/generate_features.py --dump-platform /path/to/branch/worktree`，不要手改。注册表、译文哈希、生成页面、语言配对或链接未通过检查时，发布会被阻止，旧站点仍在线；这些校验现在跑在导出树上，结论逐项写进发布清单。

Dependencies / 依赖：`docs/requirements.txt`, the Python server package / Python 服务器包, `curl`, `flock`, `ss`, Git. Logs / 日志：`${SITE_STATE_DIR:-~/.local/state/revit-model-mcp}/site-update.log`.
