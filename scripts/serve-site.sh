#!/usr/bin/env bash
# Serve the built documentation on the LAN.
#
# The port is checked before starting and the served page after starting, because a neighbouring service on
# the same port answers 200 as well: without those two checks a stale server looks like a working site.
set -euo pipefail

PORT="${1:-8099}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SITE="${SITE_DIR:-$ROOT/site}"
TITLE="Revit Model MCP"
HOST="$(hostname -I 2>/dev/null | awk '{print $1}')"

[ -d "$SITE" ] || { echo "no built site at $SITE - run scripts/update-site.sh first" >&2; exit 1; }
[ -f "$SITE/index.html" ] || { echo "$SITE holds no index.html - run scripts/update-site.sh first" >&2; exit 1; }

if command -v ss >/dev/null 2>&1 && ss -ltn | awk '{print $4}' | grep -q ":$PORT\$"; then
  owner="$(ss -ltnp 2>/dev/null | grep ":$PORT" | sed -n 's/.*users:(("\([^"]*\)",pid=\([0-9]*\).*/\1 (pid \2)/p' | head -1)"
  echo "port $PORT is already in use${owner:+ by $owner}; start on another port: $0 <port>" >&2
  exit 1
fi

cd "$SITE"
python3 -m http.server "$PORT" --bind 0.0.0.0 &
server=$!
sleep 2
if ! curl -fsS "http://127.0.0.1:$PORT/" | grep -q "$TITLE"; then
  echo "port $PORT answers, but not with this documentation; stopping" >&2
  kill "$server" 2>/dev/null || true
  exit 1
fi
echo "serving $SITE on http://${HOST:-127.0.0.1}:$PORT/"
wait "$server"
