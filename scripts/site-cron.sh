#!/usr/bin/env bash
# Runs from cron: publish the current documentation and make sure it is being served.
#
# The pull is skipped while the working tree is dirty, so an unfinished edit on the server never gets mixed
# into a published build. Everything is logged to a file, because cron output goes nowhere by default.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PORT="${SITE_PORT:-8099}"
LOG_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/revit-model-mcp"
LOG="$LOG_DIR/site-update.log"
mkdir -p "$LOG_DIR"

{
  echo "=== $(date -Is) update on port $PORT"
  cd "$ROOT"
  if git diff --quiet && git diff --cached --quiet; then
    git pull --ff-only || echo "pull failed; publishing what is here"
  else
    echo "working tree is dirty; skipping the pull"
  fi
  "$ROOT/scripts/update-site.sh" || echo "update failed; keeping the published build"

  if curl -fsS "http://127.0.0.1:$PORT/" 2>/dev/null | grep -q "Revit Model MCP"; then
    echo "already serving on $PORT"
  else
    echo "nothing answers with this documentation on $PORT; starting a server"
    old="$(ss -ltnp 2>/dev/null | grep ":$PORT" | sed -n 's/.*pid=\([0-9]*\).*/\1/p' | head -1)"
    [ -n "$old" ] && kill "$old" 2>/dev/null || true
    sleep 1
    setsid nohup python3 -m http.server "$PORT" --bind 0.0.0.0 --directory "$ROOT/site" >>"$LOG" 2>&1 &
  fi
} >>"$LOG" 2>&1
