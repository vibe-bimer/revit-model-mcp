import io
import json
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest

from revit_model_mcp import package_version, updates
from revit_model_mcp.revit_channel import (
    RevitChannelError,
    check_addin_compatibility,
)


@pytest.mark.parametrize(
    ("candidate", "current", "expected"),
    [
        ("0.7.0", "0.6.0", True),
        ("0.6.0", "0.6", False),
        ("1!0.1", "0.99", True),
        ("0.6.0.post1", "0.6.0", True),
        ("0.7.0rc1", "0.6.0", False),
        ("0.7.0.dev1", "0.6.0", False),
    ],
)
def test_stable_version_comparison(candidate, current, expected):
    assert updates.newer_stable(candidate, current) is expected


def test_update_check_writes_timestamp_before_lookup_and_throttles(tmp_path, monkeypatch):
    monkeypatch.delenv("REVIT_MCP_NO_UPDATE_CHECK", raising=False)
    path = tmp_path / "update.json"
    now = datetime(2026, 9, 29, tzinfo=timezone.utc)
    with patch.object(updates.threading, "Thread") as thread:
        thread.side_effect = lambda *args, **kwargs: (
            updates.read_state(path)["lastChecked"] == now.isoformat()
        )
        updates.check_for_updates(path, now)
        updates.check_for_updates(path, now + timedelta(hours=23))
        assert thread.call_count == 1
        updates.check_for_updates(path, now + timedelta(hours=24))
        assert thread.call_count == 2
    # The check reads a release tag; it never installs or refreshes a package.
    assert not hasattr(updates, "subprocess")


def test_update_opt_out_does_not_spawn_or_request(tmp_path, monkeypatch):
    monkeypatch.setenv("REVIT_MCP_NO_UPDATE_CHECK", "1")
    with patch.object(updates.urllib.request, "urlopen") as request:
        updates.check_for_updates(tmp_path / "update.json")
    request.assert_not_called()
    assert updates.update_status()["updateCheck"] == "disabled"


def test_bundled_executable_never_checks_for_updates(tmp_path, monkeypatch):
    monkeypatch.delenv("REVIT_MCP_NO_UPDATE_CHECK", raising=False)
    monkeypatch.setattr(updates.sys, "frozen", True, raising=False)
    with patch.object(updates.urllib.request, "urlopen") as request:
        updates.check_for_updates(tmp_path / "update.json")
    request.assert_not_called()
    assert not (tmp_path / "update.json").exists()
    assert updates.update_status()["updateCheck"] == "disabled"


def test_the_update_source_is_this_fork_and_never_pypi():
    assert updates.RELEASES_URL == (
        "https://api.github.com/repos/vibe-bimer/revit-model-mcp/releases/latest"
    )
    assert not hasattr(updates, "PYPI_URL")


def test_release_lookup_records_the_tag_of_a_stable_release(tmp_path):
    path = tmp_path / "update.json"
    release = {"tag_name": "v1.2.0", "draft": False, "prerelease": False}
    with patch.object(
        updates.urllib.request, "urlopen", return_value=io.BytesIO(json.dumps(release).encode())
    ) as request:
        updates._fetch_latest(path)
    request.assert_called_once_with(updates.RELEASES_URL, timeout=5)
    assert updates.read_state(path)["latestKnown"] == "1.2.0"


@pytest.mark.parametrize(
    "release",
    [
        {"tag_name": "v2.0.0", "draft": True, "prerelease": False},
        {"tag_name": "v2.0.0-rc.1", "draft": False, "prerelease": True},
        {"tag_name": "v2.0.0rc1", "draft": False, "prerelease": False},
        {"tag_name": None, "draft": False, "prerelease": False},
        [],
    ],
)
def test_release_lookup_ignores_a_draft_prerelease_or_malformed_answer(tmp_path, release):
    path = tmp_path / "update.json"
    with patch.object(
        updates.urllib.request, "urlopen", return_value=io.BytesIO(json.dumps(release).encode())
    ):
        updates._fetch_latest(path)
    assert updates.read_state(path) == {}


def test_compatibility_gate_accepts_same_major():
    major = int(package_version().split(".")[0])
    current = package_version().split("+")[0]
    for version in (f"{current}-dev", f"{current}-dev+2e56c3f8a1b2c3d4e5f6"):
        check_addin_compatibility("ping", {"addinVersion": version, "commands": ["ping"]})
    for suffix in (".0.0", ".99.0", ".1.0-rc.1", ".1.0-rc.1+sha", ".1.0+sha", ".1.0-dev+2e56c3f"):
        check_addin_compatibility(
            "ping", {"addinVersion": f"{major}{suffix}", "commands": ["ping"]}
        )


@pytest.mark.parametrize("reported", [None, "", "unknown", 2, "other-major"])
def test_compatibility_gate_rejects_missing_invalid_or_different_major(reported):
    major = int(package_version().split(".")[0])
    if reported == "other-major":
        reported = f"{major - 1 if major > 0 else major + 1}.1.0"
    instance = {"commands": ["ping"]}
    if reported is not None:
        instance["addinVersion"] = reported
    with pytest.raises(
        RevitChannelError, match=f"needs a Model MCP add-in of major version {major}"
    ) as error:
        check_addin_compatibility("ping", instance)
    assert "Install the matching add-in from the releases page" in str(error.value)
    assert (reported if isinstance(reported, str) and reported else "no add-in version") in str(
        error.value
    )


def test_compatibility_gate_rejects_older_major():
    major = max(1, int(package_version().split(".")[0]))
    with patch("revit_model_mcp.package_version", return_value=f"{major}.0.0"):
        with pytest.raises(RevitChannelError, match=f"major version {major}"):
            check_addin_compatibility(
                "ping", {"addinVersion": f"{major - 1}.1.0", "commands": ["ping"]}
            )


@pytest.mark.parametrize("commands", [None, [], "ping", ["other-command"]])
def test_compatibility_gate_rejects_missing_command(commands):
    version = f"{package_version().split('.')[0]}.1.0"
    with pytest.raises(RevitChannelError, match=f"add-in {version} does not support ping"):
        check_addin_compatibility("ping", {"addinVersion": version, "commands": commands})


@pytest.mark.parametrize(
    ("cached", "current", "expected"),
    [
        ("0.7.0", "0.9.0", "0.9.0"),
        ("1.0.0", "0.9.0", "1.0.0"),
        (None, "0.9.0", "0.9.0"),
        (None, "0.0.0+unknown", None),
        ("0.7.0", "0.0.0+unknown", "0.7.0"),
    ],
)
def test_update_status_latest_known_is_never_older_than_current(cached, current, expected):
    state = {"latestKnown": cached} if cached else {}
    with patch.object(updates, "read_state", return_value=state):
        assert updates.update_status(current)["latestKnownVersion"] == expected
