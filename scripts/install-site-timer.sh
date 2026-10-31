#!/usr/bin/env bash
# Schedule the recurring site update, preferring cron, then a systemd user timer, then a supervised loop.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PORT="${SITE_PORT:-8099}"
INTERVAL_SECONDS="${SITE_INTERVAL:-900}"
CRON_SCHEDULE="${1:-*/15 * * * *}"
STATE="${XDG_STATE_HOME:-$HOME/.local/state}/revit-model-mcp"
mkdir -p "$STATE"

if command -v crontab >/dev/null 2>&1; then
  entry="$CRON_SCHEDULE SITE_PORT=$PORT $ROOT/scripts/site-cron.sh"
  current="$(crontab -l 2>/dev/null || true)"
  { printf '%s\n' "$current" | grep -vF "site-cron.sh" || true; printf '%s\n' "$entry"; } | sed '/^$/d' | crontab -
  echo "scheduled with cron: $entry"
elif command -v systemctl >/dev/null 2>&1 && systemctl --user show-environment >/dev/null 2>&1; then
  unit_dir="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
  mkdir -p "$unit_dir"
  sed "s|@ROOT@|$ROOT|g; s|@PORT@|$PORT|g" "$ROOT/scripts/systemd/revit-model-mcp-site.service" > "$unit_dir/revit-model-mcp-site.service"
  sed "s|@INTERVAL@|$INTERVAL_SECONDS|g" "$ROOT/scripts/systemd/revit-model-mcp-site.timer" > "$unit_dir/revit-model-mcp-site.timer"
  # The server runs as its own unit: a process started from the oneshot refresh unit dies with its cgroup.
  sed "s|@ROOT@|$ROOT|g; s|@PORT@|$PORT|g" "$ROOT/scripts/systemd/revit-model-mcp-serve.service" > "$unit_dir/revit-model-mcp-serve.service"
  systemctl --user daemon-reload
  systemctl --user enable --now revit-model-mcp-site.timer
  systemctl --user enable --now revit-model-mcp-serve.service
  echo "scheduled with a systemd user timer every ${INTERVAL_SECONDS}s; serving on port $PORT"
  echo "check it with: systemctl --user status revit-model-mcp-serve.service"
else
  if [ -f "$STATE/supervisor.pid" ] && kill -0 "$(cat "$STATE/supervisor.pid")" 2>/dev/null; then
    echo "the supervisor is already running (pid $(cat "$STATE/supervisor.pid"))"
  else
    SITE_PORT="$PORT" SITE_INTERVAL="$INTERVAL_SECONDS" setsid nohup "$ROOT/scripts/site-supervisor.sh" >>"$STATE/site-update.log" 2>&1 &
    sleep 1
    echo "started the supervisor (pid $(cat "$STATE/supervisor.pid" 2>/dev/null)) every ${INTERVAL_SECONDS}s on port $PORT"
  fi
fi
echo "log: $STATE/site-update.log"
