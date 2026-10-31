"""The identity check is a gate, not a note: this fork's own surfaces name the fork.

A release from here must never install upstream's add-in or upstream's server.
Both failures are silent, so the check is exercised here the same way CI runs
it, plus a few unit cases that prove each rule can actually fire.
"""

from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent.parent.parent / "tools"


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


def test_naming_upstream_does_not_excuse_a_launcher(identity):
    """Prose that warns about the trap must still not quote a runnable command."""
    assert identity.launcher_problems("README.md", "upstream ships uvx revit-model-mcp\n")


def test_a_foreign_from_source_is_flagged(identity):
    assert identity.launcher_problems(
        "README.md",
        "uvx --from https://pypi.org/simple/revit-model-mcp/ revit-model-mcp\n",
    )


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


def git(repository: Path, *arguments: str) -> None:
    subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=True,
        capture_output=True,
    )


def shipped_repository(tmp_path: Path) -> Path:
    """A repository with one shipped file, one ignored build and one scratch dir."""
    repository = tmp_path / "repository"
    (repository / "docs").mkdir(parents=True)
    (repository / "docs" / "guide.md").write_text("shipped\n", encoding="utf-8")
    (repository / "site").mkdir()
    (repository / "site" / "index.html").write_text("uvx revit-model-mcp\n", encoding="utf-8")
    (repository / "scratch").mkdir()
    (repository / "scratch" / "note.md").write_text("uvx revit-model-mcp\n", encoding="utf-8")
    git(repository, "init")
    git(repository, "config", "user.email", "identity@example.com")
    git(repository, "config", "user.name", "identity check")
    git(repository, "add", "docs/guide.md")
    git(repository, "commit", "-m", "shipped")
    (repository / ".gitignore").write_text("site/\n", encoding="utf-8")
    return repository


def test_the_scan_reads_the_shipped_tree_and_not_local_scratch(identity, tmp_path, monkeypatch):
    """A built site or a tool workspace is not shipped drift."""
    repository = shipped_repository(tmp_path)
    monkeypatch.setattr(identity, "REPO_ROOT", repository)
    scanned = {path.relative_to(repository).as_posix() for path in identity.iter_scanned_files()}
    assert scanned == {"docs/guide.md"}


def test_an_untracked_file_in_a_shipped_directory_is_still_scanned(identity, tmp_path, monkeypatch):
    """A new file is checked before it is committed."""
    repository = shipped_repository(tmp_path)
    (repository / "docs" / "draft.md").write_text("draft\n", encoding="utf-8")
    monkeypatch.setattr(identity, "REPO_ROOT", repository)
    scanned = {path.relative_to(repository).as_posix() for path in identity.iter_scanned_files()}
    assert scanned == {"docs/guide.md", "docs/draft.md"}


def test_the_tool_workspace_is_pruned(identity):
    """A local agent workspace never belongs to the fork's shipped tree."""
    assert ".agent-teams" in identity.PRUNED_DIRECTORIES
