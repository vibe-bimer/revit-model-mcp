"""The identity check is a gate, not a note: this fork's own surfaces name the fork.

A release from here must never install upstream's add-in or upstream's server.
Both failures are silent, so the check is exercised here the same way CI runs
it, plus a few unit cases that prove each rule can actually fire.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent.parent.parent / "tools"
REPOSITORY_ROOT = TOOLS.parent


def load_identity_check():
    spec = importlib.util.spec_from_file_location(
        "check_fork_identity", TOOLS / "check_fork_identity.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def identity():
    return load_identity_check()


@pytest.fixture(scope="module")
def problems(identity):
    collected: list[str] = []
    for check in (
        identity.check_installer_upgrade_code,
        identity.check_registry_manifest,
        identity.check_bundle_manifest,
        identity.check_vendor_settings,
        identity.check_glama,
        identity.check_release_workflow,
        identity.check_package_launchers,
        identity.check_stray_references,
    ):
        check(collected)
    return collected


def test_this_tree_ships_only_the_fork_identity(problems):
    assert problems == []


def test_the_upgrade_code_is_the_fork_own(identity):
    installer = (REPOSITORY_ROOT / "build/install/Installer.cs").read_text(encoding="utf-8")
    assigned = [
        line for line in installer.splitlines() if "new Guid(" in line and "Guid.Empty" not in line
    ]
    assert len(assigned) == 1
    assert "8F2D710A-B967-4180-AB08-1678A02BA350" in assigned[0]
    assert identity.UPSTREAM_UPGRADE_CODE not in assigned[0]


def test_a_bare_launcher_is_recognised(identity):
    assert identity.PYPI_LAUNCHER.search("uvx revit-model-mcp")
    assert identity.PYPI_VERSION_SPEC.search("uvx revit-model-mcp==1.0.0")
    assert identity.PYPI_PROJECT_PAGE.search("https://pypi.org/project/revit-model-mcp/")


def test_a_fork_source_is_not_a_bare_launcher(identity):
    document = (
        "uvx --from https://github.com/vibe-bimer/revit-model-mcp/archive/refs/tags/"
        "v1.0.0.tar.gz#subdirectory=server revit-model-mcp\n"
    )
    assert identity.launcher_problems("README.md", document) == []


def test_the_launcher_scan_fires_in_every_scanned_file_type(identity):
    """A bare launcher in code or markup is caught, not only in Markdown."""
    for relative in ("install.ps1", "server/revit_model_mcp/updates.py", "docs/page.html"):
        assert identity.launcher_problems(relative, "uvx revit-model-mcp --help\n")
    assert identity.launcher_problems("README.md", "uvx revit-model-mcp==1.0.0\n")
    assert identity.launcher_problems("README.md", "https://pypi.org/project/revit-model-mcp/\n")
    assert identity.launcher_problems("README.md", "upstream ships uvx revit-model-mcp\n") == []


def test_the_bundle_installs_the_fork_and_never_the_package_name(identity):
    problems: list[str] = []
    identity.check_bundle_manifest(problems)
    assert problems == []
    manifest = identity.read_json("bundle/manifest.json")
    assert manifest["server"]["mcp_config"]["command"] == "uvx"
    assert "--from" in manifest["server"]["mcp_config"]["args"]
    assert "revit-model-mcp" in manifest["server"]["mcp_config"]["args"]


def test_no_registry_manifest_claims_upstream(identity):
    problems: list[str] = []
    identity.check_registry_manifest(problems)
    assert problems == []
