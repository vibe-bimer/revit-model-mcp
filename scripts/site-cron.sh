#!/usr/bin/env bash
# Publish the documentation site on a timer; never kill a port owner.
#
# A dirty development tree is not a reason to skip: the publisher exports the target commit into a
# temporary tree, so uncommitted edits neither block nor leak into the release. Skips and failures are
# logged with different words and different exit codes so the timer unit shows a skip as success.
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# SITE_REPO overrides the published checkout, which drills use to publish a throwaway repository.
ROOT="${SITE_REPO:-$(cd "$HERE/.." && pwd)}"
PORT="${SITE_PORT:-8099}"
LOG_DIR="${SITE_STATE_DIR:-${XDG_STATE_HOME:-$HOME/.local/state}/revit-model-mcp}"
LOG="$LOG_DIR/site-update.log"
mkdir -p "$LOG_DIR"

{
  echo "=== $(date -Is) update on port $PORT"
  cd "$ROOT"
  if [ -n "$(git status --porcelain)" ]; then
    echo "working tree is dirty; publishing from a clean export of the target commit anyway"
  fi

  SITE_SKIP_PULL=1 "$HERE/update-site.sh"
  publish_rc=$?
  case "$publish_rc" in
    0)
      echo "publish ok"
      ;;
    3)
      # Another publish is already running and holds the lock; this round is a skip, not a failure.
      echo "publish skipped: another publish is in progress; the published site is unchanged"
      exit 0
      ;;
    2)
      echo "publish failed while syncing; the published site is unchanged"
      ;;
    *)
      echo "publish failed (exit $publish_rc); the published site is unchanged"
      ;;
  esac

  verify_failed=0
  page="$(curl -fsS "http://127.0.0.1:$PORT/" 2>/dev/null || true)"
  if [[ "$page" == *"Revit Model MCP"* && "$page" == *"data-md-component"* ]]; then
    echo "already serving on $PORT"
  elif command -v ss >/dev/null 2>&1 && ss -ltn | awk '{print $4}' | grep -q ":$PORT\$"; then
    echo "port $PORT is occupied by another service; leaving it untouched"
    verify_failed=1
  elif systemctl --user list-unit-files revit-model-mcp-serve.service >/dev/null 2>&1; then
    # The server is its own unit; a process spawned here would be killed with this unit's cgroup.
    echo "starting revit-model-mcp-serve.service"
    systemctl --user restart revit-model-mcp-serve.service
    sleep 2
    page="$(curl -fsS "http://127.0.0.1:$PORT/" 2>/dev/null || true)"
    if [[ "$page" != *"Revit Model MCP"* || "$page" != *"data-md-component"* ]]; then
      echo "documentation server verification failed"
      verify_failed=1
    fi
  else
    echo "nothing serves port $PORT; run scripts/install-site-timer.sh to install the serve unit, or scripts/serve-site.sh $PORT"
    verify_failed=1
  fi

  if [ "$publish_rc" -ne 0 ] || [ "$verify_failed" -ne 0 ]; then
    echo "run failed: publish exit $publish_rc, verification exit $verify_failed"
    exit 1
  fi
  exit 0
} >>"$LOG" 2>&1
