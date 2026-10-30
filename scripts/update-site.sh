#!/usr/bin/env bash
# Publish the documentation site from a clean export of a fixed commit.
#
# The work lives in scripts/publish_site.py: it exports the target commit with git archive, runs the
# repository gates on that export, builds into an immutable release directory and flips a current
# symlink. A dirty development tree neither blocks publishing nor leaks into the release.
#
# Exit codes: 0 published or already current, 1 build or publish failure, 2 sync failure,
# 3 another publish holds the lock, 4 the health probe failed and current was rolled back.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# SITE_REPO overrides the published checkout, which drills use to publish a throwaway repository.
ROOT="${SITE_REPO:-$(cd "$HERE/.." && pwd)}"
PYTHON="${PYTHON:-python3}"

exec "$PYTHON" "$HERE/publish_site.py" --repo "$ROOT" "$@"
