#!/usr/bin/env bash
# Regenerate the feature pages from the tool registry and publish the site atomically.
#
# The previous build is kept until the new one passes its checks, so a failed generation cannot take the
# documentation offline.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
exec 9>"$ROOT/.site-build.lock"
flock -n 9 || { echo "Another site build is running; leaving the published site unchanged" >&2; exit 1; }
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

if [ "${SITE_SKIP_PULL:-0}" != "1" ]; then
  echo "== pulling"
  git pull --ff-only
fi

# Guard every destructive target against an unexpected symlink or repository root.
[ "$(git rev-parse --show-toplevel)" = "$ROOT" ] || { echo "Unexpected repository root" >&2; exit 1; }
safe_remove_build() {
  local name="$1" target
  case "$name" in site.new|site.prev) ;; *) echo "Unsafe build target: $name" >&2; return 1 ;; esac
  target="$(realpath -m "$ROOT/$name")"
  [ "$target" = "$ROOT/$name" ] || { echo "Unexpected build target: $target" >&2; return 1; }
  rm -rf -- "$target"
}
for name in site site.new site.prev; do
  [ "$(realpath -m "$ROOT/$name")" = "$ROOT/$name" ] || { echo "Unexpected site target: $name" >&2; exit 1; }
done

echo "== checking that the live tool registry and translated pages agree"
"$PYTHON" tools/site/generate_features.py --verify-registry --check
"$PYTHON" -m unittest discover -s tools/site -p 'test_*.py'

echo "== building"
safe_remove_build site.new
eval "$MKDOCS build --strict -f \"$MKDOCS_CONFIG\" -d site.new"

echo "== checking both languages in the NEW build"
"$PYTHON" tools/site/check_site.py --site-dir site.new

echo "== publishing"
safe_remove_build site.prev
if [ -d site ]; then mv -- site site.prev; fi
if ! mv -- site.new site; then
  if [ -d site.prev ]; then mv -- site.prev site; fi
  exit 1
fi
safe_remove_build site.prev
echo "published $ROOT/site"
echo "serve it with scripts/serve-site.sh <port>"
