"""Best-effort server update checks outside the MCP startup path."""

from __future__ import annotations

import json
import logging
import os
import re
import sys
import threading
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

LOGGER = logging.getLogger(__name__)
PACKAGE = "revit-model-mcp"
# This fork publishes its server on GitHub Releases and not to PyPI. Upstream owns the
# revit-model-mcp project on PyPI and both projects share version numbers, so a PyPI lookup
# here would report upstream's release and a uvx refresh would install upstream's server.
REPOSITORY = "vibe-bimer/revit-model-mcp"
RELEASES_URL = f"https://api.github.com/repos/{REPOSITORY}/releases/latest"
CHECK_INTERVAL = timedelta(hours=24)
STABLE_VERSION = re.compile(
    r"v?(?:(\d+)!)?(\d+(?:\.\d+)*)(?:(?:[._-]?post|-)\s*(\d+))?"
    r"(?:\+[a-z0-9]+(?:[._-][a-z0-9]+)*)?",
    re.IGNORECASE,
)


def stable_version_key(value: str) -> tuple[int, tuple[int, ...], int] | None:
    """Return an ordered key for stable PEP 440 public releases and post releases."""
    match = STABLE_VERSION.fullmatch(value)
    if match is None:
        return None
    release = tuple(int(part) for part in match.group(2).split("."))
    return int(match.group(1) or 0), release, int(match.group(3) or -1)


def newer_stable(candidate: str, current: str) -> bool:
    candidate_key = stable_version_key(candidate)
    current_key = stable_version_key(current)
    if candidate_key is None:
        return False
    if current_key is None:
        return True
    epoch, release, post = candidate_key
    current_epoch, current_release, current_post = current_key
    width = max(len(release), len(current_release))
    return (epoch, release + (0,) * (width - len(release)), post) > (
        current_epoch,
        current_release + (0,) * (width - len(current_release)),
        current_post,
    )


def state_path() -> Path:
    if sys.platform == "win32":
        root = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    elif sys.platform == "darwin":
        root = Path.home() / "Library" / "Caches"
    else:
        root = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    return root / PACKAGE / "update.json"


def read_state(path: Path | None = None) -> dict[str, str]:
    try:
        value = json.loads((path or state_path()).read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError):
        return {}


def _write_state(path: Path, state: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(state), encoding="utf-8")
    temporary.replace(path)


def update_check_disabled() -> bool:
    """The opt-out variable, or the bundled executable, which is updated only by its installer."""
    return os.environ.get("REVIT_MCP_NO_UPDATE_CHECK") == "1" or bool(getattr(sys, "frozen", False))


def update_status(current: str | None = None) -> dict[str, str | None]:
    state = read_state()
    latest = state.get("latestKnown")
    if (
        current is not None
        and "+" not in current
        and stable_version_key(current) is not None
        and (not latest or newer_stable(current, latest))
    ):
        latest = current
    return {
        "latestKnownVersion": latest,
        "updateCheck": "disabled" if update_check_disabled() else state.get("lastChecked"),
    }


def _fetch_latest(path: Path) -> None:
    """Record this fork's newest stable release tag, read from its own GitHub releases."""
    try:
        with urllib.request.urlopen(RELEASES_URL, timeout=5) as response:
            release = json.load(response)
        if not isinstance(release, dict) or release.get("draft") or release.get("prerelease"):
            return
        tag = release.get("tag_name")
        if not isinstance(tag, str):
            return
        version = tag.removeprefix("v")
        if stable_version_key(version) is None:
            return
        state = read_state(path)
        if not state.get("latestKnown") or newer_stable(version, state["latestKnown"]):
            state["latestKnown"] = version
            _write_state(path, state)
    except Exception:
        LOGGER.debug("Update version lookup failed.", exc_info=True)


def check_for_updates(path: Path | None = None, now: datetime | None = None) -> None:
    if update_check_disabled():
        return
    path = path or state_path()
    now = now or datetime.now(timezone.utc)
    try:
        state = read_state(path)
        last = state.get("lastChecked")
        if last and now - datetime.fromisoformat(last) < CHECK_INTERVAL:
            return
        state["lastChecked"] = now.isoformat()
        _write_state(path, state)
        # No package warm-up here: this fork publishes no PyPI package, and a uvx refresh of the
        # bare name would install upstream's server. The lookup only reads a release tag.
        threading.Thread(target=_fetch_latest, args=(path,), daemon=True).start()
    except Exception:
        LOGGER.debug("Update check could not start.", exc_info=True)
