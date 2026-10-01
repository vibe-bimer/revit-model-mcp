#!/usr/bin/env bash
# Regenerate the feature pages from the tool registry and publish the site atomically.
#
# The previous build is kept until the new one passes its checks, so a failed generation cannot take the
# documentation offline.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
if [ -z "${MKDOCS:-}" ]; then
  for candidate in "$ROOT/.venv-docs/bin/mkdocs" "$HOME/.venv-docs/bin/mkdocs" "$(command -v mkdocs || true)"; do
    if [ -n "$candidate" ] && [ -x "$candidate" ]; then MKDOCS="$candidate"; break; fi
  done
fi
if [ -z "${MKDOCS:-}" ] && command -v uv >/dev/null 2>&1; then
  MKDOCS="uv run --with-requirements $ROOT/docs/requirements.txt mkdocs"
fi
[ -n "${MKDOCS:-}" ] || { echo "mkdocs was not found; install docs/requirements.txt or set MKDOCS" >&2; exit 1; }
PYTHON="${PYTHON:-python3}"
# The LAN build points site_url at the host that serves the site, so the language switch and the absolute
# links land on this server instead of the upstream Pages path.
MKDOCS_CONFIG="${MKDOCS_CONFIG:-$ROOT/mkdocs-lan.yml}"

echo "== pulling"
git pull --ff-only

echo "== checking that the tool registry and the pages agree"
"$PYTHON" tools/site/generate_features.py --check

echo "== building"
rm -rf site.new
eval "$MKDOCS build --strict -f \"$MKDOCS_CONFIG\" -d site.new"

echo "== checking both languages"
"$PYTHON" tools/site/check_site.py

echo "== publishing"
rm -rf site.prev
[ -d site ] && mv site site.prev
mv site.new site
rm -rf site.prev
echo "published $ROOT/site ($(find site -name '*.html' | wc -l) pages)"
echo "serve it with scripts/serve-site.sh <port>"
