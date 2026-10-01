#!/usr/bin/env bash
# Regenerate the feature pages from the tool registry and publish the site atomically.
#
# The previous build is kept until the new one passes its checks, so a failed generation cannot take the
# documentation offline.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
MKDOCS="${MKDOCS:-mkdocs}"
PYTHON="${PYTHON:-python3}"

echo "== pulling"
git pull --ff-only

echo "== checking that the tool registry and the pages agree"
"$PYTHON" tools/site/generate_features.py --check

echo "== building"
rm -rf site.new
"$MKDOCS" build --strict -d site.new

echo "== publishing"
rm -rf site.prev
[ -d site ] && mv site site.prev
mv site.new site
rm -rf site.prev
echo "published $ROOT/site ($(find site -name '*.html' | wc -l) pages)"
echo "serve it with scripts/serve-site.sh <port>"
