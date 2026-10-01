#!/usr/bin/env bash
# Pull and publish reviewed documentation only; never publish a dirty checkout or kill a port owner.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PORT="${SITE_PORT:-8099}"
LOG_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/revit-model-mcp"
LOG="$LOG_DIR/site-update.log"
mkdir -p "$LOG_DIR"

{
  echo "=== $(date -Is) update on port $PORT"
  cd "$ROOT"
  if [ -n "$(git status --porcelain)" ]; then
    echo "working tree is dirty; skipping pull AND publish (including untracked files)"
    exit 0
  fi
  git pull --ff-only || echo "pull failed; checking the current clean revision"
  failed=0
  SITE_SKIP_PULL=1 "$ROOT/scripts/update-site.sh" || { echo "update failed; keeping the published build"; failed=1; }

  page="$(curl -fsS "http://127.0.0.1:$PORT/" 2>/dev/null || true)"
  if [[ "$page" == *"Revit Model MCP"* && "$page" == *"data-md-component"* ]]; then
    echo "already serving on $PORT"
  elif command -v ss >/dev/null 2>&1 && ss -ltn | awk '{print $4}' | grep -q ":$PORT\$"; then
    echo "port $PORT is occupied by another service; leaving it untouched"
    exit 1
  else
    echo "starting documentation server on free port $PORT"
    setsid nohup python3 -m http.server "$PORT" --bind 0.0.0.0 --directory "$ROOT/site" >>"$LOG" 2>&1 &
    sleep 1
    page="$(curl -fsS "http://127.0.0.1:$PORT/" 2>/dev/null || true)"
    [[ "$page" == *"Revit Model MCP"* && "$page" == *"data-md-component"* ]] || { echo "documentation server verification failed"; exit 1; }
  fi
  exit "$failed"
} >>"$LOG" 2>&1
