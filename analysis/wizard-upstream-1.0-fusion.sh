#!/usr/bin/env bash
#
# Wizard: 上游 1.0 底座 · 融合决策
# 逐个决定「以上游 1.0 为底座做薄扩展」这件事里的每一个岔路口。
# 每个决定写进 analysis/fusion-decisions.env，中断后重跑会保留已答内容。
#
# 跑法:
#   bash analysis/wizard-upstream-1.0-fusion.sh

set -euo pipefail

# ──────────────────────────────────────────────────────────────────────────
# Wizard library: delightful, consistent UX, identical across every wizard.
# ──────────────────────────────────────────────────────────────────────────

if [[ -t 1 ]] && command -v tput >/dev/null 2>&1 && [[ "$(tput colors 2>/dev/null || echo 0)" -ge 8 ]]; then
  BOLD=$(tput bold); DIM=$(tput dim); RESET=$(tput sgr0)
  BLUE=$(tput setaf 4); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); RED=$(tput setaf 1)
else
  BOLD=""; DIM=""; RESET=""; BLUE=""; GREEN=""; YELLOW=""; RED=""
fi

# Author sets this at the top of the stages section.
TOTAL_STAGES=0

_STAGE_INDEX=0
ENV_FILE="${ENV_FILE:-.env}"
WRITTEN_ENV=()    # KEYs written to ENV_FILE this run
WRITTEN_SECRET=() # secret NAMEs set this run
SKIPPED=()        # things we couldn't do (e.g. gh missing)

# _clear wipes the terminal so only the current step is on screen. No-op when
# output isn't a terminal, so piped logs stay readable.
_clear() {
  [[ -t 1 ]] || return 0
  if command -v tput >/dev/null 2>&1; then tput clear; else printf '\033[2J\033[3J\033[H'; fi
}

# banner "Title" shows the opening frame: what this wizard does.
banner() {
  _clear
  printf '\n%s%s  %s%s\n' "$BOLD" "$BLUE" "$1" "$RESET"
  printf '%s  %s stages%s\n\n' "$DIM" "$TOTAL_STAGES" "$RESET"
  printf '%s  You drive the browser; this wizard tells you exactly what to do and\n' "$DIM"
  printf '  captures the values you copy back. Stop any time with Ctrl-C and re-run\n' "$DIM"
  printf '  later, since it remembers values already saved.%s\n' "$RESET"
  pause "Ready to start?"
}

# stage "Name" clears the screen, then announces a stage and shows progress.
# Clearing keeps only the current step on screen.
stage() {
  _clear
  _STAGE_INDEX=$((_STAGE_INDEX + 1))
  printf '\n%s%s▸ Stage %s/%s · %s%s\n' \
    "$BOLD" "$BLUE" "$_STAGE_INDEX" "$TOTAL_STAGES" "$1" "$RESET"
}

# say "..." prints a plain instruction line.
say()  { printf '  %s\n' "$1"; }
# step "..." is a numbered-feeling action the human takes in the browser.
step() { printf '  %s•%s %s\n' "$BLUE" "$RESET" "$1"; }
note() { printf '  %s%s%s\n' "$DIM" "$1" "$RESET"; }
warn() { printf '  %s⚠ %s%s\n' "$YELLOW" "$1" "$RESET"; }

# open_url URL opens it in the human's browser, cross-platform incl. WSL.
open_url() {
  local url="$1"
  printf '  %s↗ opening%s %s\n' "$GREEN" "$RESET" "$url"
  { if   command -v wslview     >/dev/null 2>&1; then wslview "$url"
    elif command -v explorer.exe >/dev/null 2>&1; then explorer.exe "$url"
    elif command -v xdg-open    >/dev/null 2>&1; then xdg-open "$url"
    elif command -v open        >/dev/null 2>&1; then open "$url"
    else warn "couldn't open a browser; visit it manually: $url"; fi
  } >/dev/null 2>&1 || warn "couldn't open a browser, so visit it manually: $url"
}

# pause "msg" waits for the human to confirm they've done the manual part.
pause() {
  printf '  %s%s%s ' "$DIM" "${1:-Press Enter to continue}" "$RESET"
  read -r _ || true
}

# confirm "question" is a y/N gate; returns success on yes.
confirm() {
  local reply=""
  printf '  %s? %s [y/N] ' "$YELLOW" "$1"
  read -r reply || true
  [[ "$reply" =~ ^[Yy] ]]
}

# _existing KEY: current value of KEY in ENV_FILE, if any.
_existing() {
  [[ -f "$ENV_FILE" ]] || return 1
  local line; line=$(grep -E "^${1}=" "$ENV_FILE" | tail -n1) || return 1
  printf '%s' "${line#*=}"
}

# ask KEY "Prompt" reads a value into $KEY. Offers the existing .env value as
# a default on re-runs (Enter keeps it). Visible input (non-secret).
ask() {
  local key="$1" prompt="$2" current input
  current=$(_existing "$key" || true)
  if [[ -n "$current" ]]; then
    printf '  %s%s%s %s[Enter keeps current]%s ' "$BOLD" "$prompt" "$RESET" "$DIM" "$RESET"
  else
    printf '  %s%s%s ' "$BOLD" "$prompt" "$RESET"
  fi
  read -r input || true
  [[ -z "$input" && -n "$current" ]] && input="$current"
  printf -v "$key" '%s' "$input"
}

# ask_secret KEY "Prompt" is like ask, but input is hidden.
ask_secret() {
  local key="$1" prompt="$2" current input
  current=$(_existing "$key" || true)
  if [[ -n "$current" ]]; then
    printf '  %s%s%s %s[Enter keeps current]%s ' "$BOLD" "$prompt" "$RESET" "$DIM" "$RESET"
  else
    printf '  %s%s%s ' "$BOLD" "$prompt" "$RESET"
  fi
  read -rs input || true
  printf '\n'
  [[ -z "$input" && -n "$current" ]] && input="$current"
  printf -v "$key" '%s' "$input"
}

# write_env KEY VALUE upserts KEY=VALUE into ENV_FILE (creates it; replaces
# any existing line). Idempotent.
write_env() {
  local key="$1" value="$2" tmp
  touch "$ENV_FILE"
  tmp=$(mktemp)
  grep -vE "^${key}=" "$ENV_FILE" > "$tmp" || true
  printf '%s=%s\n' "$key" "$value" >> "$tmp"
  mv "$tmp" "$ENV_FILE"
  WRITTEN_ENV+=("$key")
  printf '  %s✓ wrote%s %s → %s\n' "$GREEN" "$RESET" "$key" "$ENV_FILE"
}

# set_secret NAME VALUE sets a GitHub Actions repo secret via gh. Falls back
# to a warning (and records it) if gh is unavailable or unauthenticated.
set_secret() {
  local name="$1" value="$2"
  if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
    if printf '%s' "$value" | gh secret set "$name" >/dev/null 2>&1; then
      WRITTEN_SECRET+=("$name")
      printf '  %s✓ set%s GitHub secret %s\n' "$GREEN" "$RESET" "$name"
      return
    fi
  fi
  SKIPPED+=("GitHub secret $name (set it manually: gh secret set $name)")
  warn "skipped GitHub secret $name: gh not ready; set it later"
}

# set_var NAME VALUE sets a GitHub Actions repo variable (non-secret).
set_var() {
  local name="$1" value="$2"
  if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
    if gh variable set "$name" --body "$value" >/dev/null 2>&1; then
      printf '  %s✓ set%s GitHub variable %s\n' "$GREEN" "$RESET" "$name"
      return
    fi
  fi
  SKIPPED+=("GitHub variable $name")
  warn "skipped GitHub variable $name, gh not ready; set it later"
}

# finish clears, then shows a closing summary of everything configured.
finish() {
  _clear
  printf '\n%s%s  ✓ Setup complete%s\n' "$BOLD" "$GREEN" "$RESET"
  (( ${#WRITTEN_ENV[@]}    ))    && note "wrote ${#WRITTEN_ENV[@]} value(s) to $ENV_FILE: ${WRITTEN_ENV[*]}"
  (( ${#WRITTEN_SECRET[@]} )) && note "set ${#WRITTEN_SECRET[@]} GitHub secret(s): ${WRITTEN_SECRET[*]}"
  if (( ${#SKIPPED[@]} )); then
    printf '\n'; warn "still to do by hand:"
    for s in "${SKIPPED[@]}"; do note "  - $s"; done
  fi
  printf '\n'
}

# ──────────────────────────────────────────────────────────────────────────
# STAGES: author this section. One stage() per step the human takes.
# Replace the example below. Set TOTAL_STAGES to match the stages you write.
# ──────────────────────────────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${ENV_FILE:-$SCRIPT_DIR/fusion-decisions.env}"
DECISIONS_MD="$SCRIPT_DIR/fusion-decisions.md"

TOTAL_STAGES=16

# _seed KEY VALUE stores a value without recording it as "written this run".
_seed() {
  local k="$1" v="$2" tmp
  touch "$ENV_FILE"
  tmp=$(mktemp)
  grep -vE "^${k}=" "$ENV_FILE" >"$tmp" || true
  printf '%s=%s\n' "$k" "$v" >>"$tmp"
  mv "$tmp" "$ENV_FILE"
}

# choose KEY "Prompt" "Recommended" "legend" — a decision with a recommended default.
# Enter accepts the recommendation (or the answer already on file).
choose() {
  local key="$1" prompt="$2" recommended="$3" legend="${4:-}"
  local current input
  current=$(_existing "$key" 2>/dev/null || true)
  [[ -z "$current" ]] && current="$recommended"
  _seed "$key" "$current"
  if [[ -n "$legend" ]]; then
    while IFS= read -r l; do printf '      %s%s%s\n' "$DIM" "$l" "$RESET"; done <<< "$legend"
  fi
  printf '  %s%s%s ' "$BOLD" "$prompt" "$RESET"
  read -r input || true
  [[ -z "$input" ]] && input="$current"
  write_env "$key" "$input" >/dev/null 2>&1
  printf '  %s✓ %s = %s%s\n' "$GREEN" "$key" "$input" "$RESET"
}

# choose_num KEY "Prompt" "Recommended" LO HI "legend" — same, but the answer must be an integer in range.
choose_num() {
  local key="$1" prompt="$2" recommended="$3" lo="$4" hi="$5" legend="${6:-}"
  local v
  while true; do
    choose "$key" "$prompt" "$recommended" "$legend"
    v=$(_existing "$key" 2>/dev/null || echo "$recommended")
    if [[ "$v" =~ ^[0-9]+$ ]] && (( v >= lo && v <= hi )); then break; fi
    printf '  %s⚠ 请输入 %s 到 %s 之间的整数%s\n' "$YELLOW" "$lo" "$hi" "$RESET"
  done
}

banner "上游 1.0 底座 · 融合决策"

say "这一步要定的是：把上游 1.0 当底座，你自己的 8 个工具重写一遍。"
say "共 16 个决定，按依赖顺序排好了。每个都会给你一个推荐答案，回车即采纳。"
say "所有回答写进 analysis/fusion-decisions.env。中途 Ctrl-C 退出，重跑会接着上次。"

# ── 1 ───────────────────────────────────────────────────────────────────────
stage "重写的含义"
say "这个词决定这件事是三周还是三个月。"
say ""
say "ModelRebuild.cs 1003 行里有一半是踩出来的坑：MEP 系统成员不能当普通元素、"
say "副本要 rehost 并恢复 join、Revit 会弹 duplicate-name 对话框。"
say ""
choose REWRITE_SCOPE "你的选择（Enter = 推荐）:" "contract-remap" \
"a) contract-remap  契约重映射：保留逻辑，按上游重塑 DTO 与签名  ← 推荐
b) rewrite-from-scratch  从零重写：按上游形状重新设计每个工具
c) lift-as-is  现状照搬：整体拷过去，只改编译错误"

# ── 2 ───────────────────────────────────────────────────────────────────────
stage "底座钉在哪"
say "上游 1.0.0 是 27c1c45（2026-10-16）。它之后还有 11 个提交，当前 main 是 760bb7c。"
say "那 11 个里有三条在你每天都在用的错误路径上：传输丢失报可重试错误、"
say "目标文档没打开时说清楚、切换文档后能恢复。"
say ""
choose BASE_PIN "你的选择（Enter = 推荐）:" "760bb7c" \
"a) 760bb7c  当前 upstream/main，含 11 个 post-1.0 修复  ← 推荐
b) v1.0.0    官方发布点，少 11 个修复"

# ── 3 ───────────────────────────────────────────────────────────────────────
stage "薄的上限：改动行数"
say "「薄」现在是个感觉词。给它一个能检查的数，否则半年后没人知道有没有守住。"
say "实测：11 个钩子合计 35 行。给你留一倍余量。"
say ""
choose_num THIN_LINES "允许改动上游文件的总行数上限:" 80 20 300 \
"（Enter = 80 行）"

# ── 4 ───────────────────────────────────────────────────────────────────────
stage "薄的上限：改动位置"
say "只在上游指定的兜底分支里挂钩。出现在别处即视为破坏薄扩展。"
say ""
choose_num THIN_HOOKS "允许出现改动的上游位置数量:" 7 3 20 \
"（Enter = 7 处）"

# ── 5 ───────────────────────────────────────────────────────────────────────
stage "写权限默认"
say "上游 1.0 默认可写。你现在是 REVIT_MCP_ALLOW_WRITE 不开就整个不注册动作工具。"
say "两套并存会出现 revit_create_wall 能写、revit_create_floor 被拒，用户没法理解。"
say ""
choose WRITE_DEFAULT "你的选择（Enter = 推荐）:" "readonly-default-upstream-shape" \
"a) readonly-default-upstream-shape  默认只读，工具始终列出、调用时按上游形状拒绝  ← 推荐
b) upstream-writable  照上游：默认可写，只读靠策略文件
c) dual-gate  两套门禁并存（你的注册期 + 上游策略层）"

# ── 6 ───────────────────────────────────────────────────────────────────────
stage "revit_batch 怎么处置"
say "事实已查清：上游 revit_run_actions 的签名是 steps 1..50、dry_run、document，"
say "docstring 写着「Execute up to 50 actions with one undo step; the whole batch rolls back"
say "on its first failure」，内部发的命令就是 batch。和你 revit_batch 一字不差。"
say ""
choose BATCH_TOOL "你的选择（Enter = 推荐）:" "drop-use-upstream" \
"a) drop-use-upstream  删掉你的 revit_batch，用上游 revit_run_actions  ← 推荐
b) keep-both  两个都留"

# ── 7 ───────────────────────────────────────────────────────────────────────
stage "主力 Revit 年份"
say "这个问题决定 R2020 值不值得留。"
say "每多一个年份，就多一条构建矩阵加一整套兼容层要维护。"
say ""
choose PRIMARY_YEAR "你的工作站主力跑哪个 Revit 年份:" "2026" \
"例如 2026 / 2024 / 2020（Enter = 2026）"

# ── 8 ───────────────────────────────────────────────────────────────────────
stage "R2020 处置"
say "上游只覆盖 R22–R27，按年固定到当年最低 build。你的 R2020 是靠浮动版本区间"
say "绕进去的，另带 305 行兼容层——而那层存在的原因是工作站缺约 90 个新成员。"
say ""
choose R2020 "你的选择（Enter = 推荐）:" "defer" \
"a) defer  延后：八个工具移植完再单独一轮  ← 推荐
b) drop   放弃：只在主力年份上支持
c) now    本轮就重做 R2020，塞进上游的 pin 机制"

# ── 9 ───────────────────────────────────────────────────────────────────────
stage "双语站点"
say "tools/site/generate_features.py 632 行从活的 MCP 注册表导出工具清单，生成中英双语页。"
say "这是资产：工具面怎么变它跟着走。18 对 .en.md 是负债：上游重写了 13 个 docs 文件。"
say ""
choose SITE "你的选择（Enter = 推荐）:" "keep-generator" \
"a) keep-generator  保留生成器机制，丢弃文档内容和 18 对翻译  ← 推荐
b) drop-all        整个丢掉，之后重建
c) keep-all        全保，跟着上游新文档重做 18 对翻译"

# ── 10 ──────────────────────────────────────────────────────────────────────
stage "工作区里那 35 个未提交改动"
say "身份隔离那部分在新底座上必须重做（上游 Installer.cs 多了 Installer.Policy.cs）。"
say "manifest 修复和台账脚本基本能直接搬。"
say "成果只活在未提交的工作区里，一次误操作就没了。"
say ""
choose WIP "你的选择（Enter = 推荐）:" "commit-then-branch-from-5afcb55" \
"a) commit-then-branch-from-5afcb55  先提交到 main，再从 5afcb55 开底座分支  ← 推荐
b) discard-and-redo                不提交，直接在新底座上重做
c) commit-and-carry-onto-new-base  先提交，并把这批改动整体搬到新底座上"

# ── 11 ──────────────────────────────────────────────────────────────────────
stage "Fork 代码归属目录"
say "已核实：上游 1.0 的 ActionJobContract / ActionResultData / ActionFacts 都是 public，"
say "在 RevitModelMcp.Core 里，Addin 引用 Core。所以纯逻辑可以放 Core，碰 Revit API 的放 Addin。"
say ""
choose FORK_DIR "你的选择（Enter = 推荐）:" "core-and-addin" \
"a) core-and-addin  src/RevitModelMcp.Core/Fork/ + src/RevitModelMcp.Addin/Fork/  ← 推荐
b) addin-only       全放 src/RevitModelMcp.Addin/Fork/
c) single-file      全塞进一个 Fork/ForkActions.cs"

# ── 12 ──────────────────────────────────────────────────────────────────────
stage "缝的形状"
say "「薄」的成败全在这一步。上游的派发是散在 7 个文件里的 if/switch 链。"
say "如果照上游形状逐处插入，8 个工具就是 80–90 个编辑点，每次上游发版都要重做一遍。"
say ""
choose SEAM_SHAPE "你的选择（Enter = 推荐）:" "registry-plus-hooks" \
"a) registry-plus-hooks  外挂注册表 + 兜底钩子（只在「不认识这个命令」的分支挂钩）  ← 推荐
b) upstream-shape       照上游形状逐处插入
c) source-generator     源生成器产出派发代码"

# ── 13 ──────────────────────────────────────────────────────────────────────
stage "第一个走通的工具"
say "选一个工具把全部接触点走一遍，剩下的就是复制这个形状。"
say "选它的理由要能覆盖：入参校验、事务执行、前后事实、摘要标题、命令注册。"
say ""
choose TRACER_TOOL "你的选择（Enter = 推荐）:" "set-view-lighting" \
"a) set-view-lighting  碰全部面，逻辑最独立  ← 推荐
b) create_level        最接近上游 create_wall
c) element-id-register 只读导出，风险最低"

# ── 14 ──────────────────────────────────────────────────────────────────────
stage "第一个工具的验收标准"
say "Windows CI 是本地验不了 C# 的唯一裁判。定清楚「做完」是什么意思。"
say ""
choose TRACER_ACCEPT "你的选择（Enter = 推荐）:" "compile-plus-tests-plus-contract" \
"a) compile-plus-tests-plus-contract  编译绿 + Core 解析测试绿 + Python 测试绿 + 契约落盘  ← 推荐
b) plus-real-revit                   上面全部 + 真机 Revit 跑一次
c) compile-only                      只要编译绿"

# ── 15 ──────────────────────────────────────────────────────────────────────
stage "本地必过的检查"
say "每次提交前，本机必须全绿的项目。"
say ""
choose LOCAL_GATES "你的选择（Enter = 推荐）:" "standard" \
"a) standard   identity 守卫 + intake 闸门 + 生成物一致 + 站点测试 + ruff + pytest  ← 推荐
b) strict-plus 上面全部 + mkdocs --strict + site 引用检查 + mcpb validate"

# ── 16 ──────────────────────────────────────────────────────────────────────
stage "上游同步节奏"
say "永久分叉的代价：安全修复不会自己来。读上游的频率必须定死。"
say ""
choose UPSTREAM_RHYTHM "你的选择（Enter = 推荐）:" "per-minor-release" \
"a) per-minor-release  每个上游 minor 版本读一次，跑 intake 闸门  ← 推荐
b) per-patch           每个 patch 也读
c) manual              想起来才读"

# ── 收尾 ────────────────────────────────────────────────────────────────────
_clear
printf '\n%s%s  ▸ 收尾%s\n' "$BOLD" "$BLUE" "$RESET"
say "16 个决定全部记下了。"
say ""
say "接下来我按这份文件做三件事："
say "  1) 建 GLOSSARY.md（batch 这一个词现在有三个含义，必须钉死）"
say "  2) 建 adr/ 里的 ADR（每个「难回退 + 反直觉 + 有取舍」的决定一条）"
say "  3) 改写 issue #27 的正文，让它和这些决定一致"
say ""
note "决策文件：$DECISIONS_MD"
note "原始回答：$ENV_FILE"

if confirm "现在就按这些决定开始产出 GLOSSARY.md 和 ADR 吗？"; then
  say "好。我读 $ENV_FILE 之后开工。"
else
  say "好。文件已保存，随时可以让我继续。"
fi

finish
