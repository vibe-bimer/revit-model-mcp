#!/usr/bin/env bash
# Keeps the documentation fresh without cron: runs the update every SITE_INTERVAL seconds and makes sure the
# site is being served. Start it with scripts/install-site-timer.sh, which records the pid and the log path.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INTERVAL="${SITE_INTERVAL:-900}"
STATE="${XDG_STATE_HOME:-$HOME/.local/state}/revit-model-mcp"
mkdir -p "$STATE"
echo $$ > "$STATE/supervisor.pid"
echo "supervisor pid $$ every ${INTERVAL}s" >> "$STATE/site-update.log"

while true; do
  SITE_PORT="${SITE_PORT:-8099}" "$ROOT/scripts/site-cron.sh" || true
  sleep "$INTERVAL"
done
