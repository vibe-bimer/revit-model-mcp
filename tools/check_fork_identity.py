#!/usr/bin/env python3
"""Fail when upstream's identity reappears in a surface this fork ships.

This fork descends from ``sharafutdinovdi/revit-model-mcp`` and shares its
version numbers. That makes identity drift silent: an installer with upstream's
UpgradeCode replaces this fork's install as a major upgrade, and a bundle that
resolves ``revit-model-mcp`` on PyPI installs upstream's server while looking
like this fork's release. Both failures leave the user with a working product
that has none of this fork's tools.

The checks below are deliberately narrow. Reusing ``sharafutdinovdi/.github``
reusable workflows and inheriting its code of conduct are honest and allowed;
claiming upstream's install identity, package name, or security contact is not.

Run with no arguments to check. Exit codes: 0 clean, 1 identity drift, 2 the
check could not run.
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections.abc import Iterator
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

UPSTREAM_OWNER = "sharafutdinovdi"
UPSTREAM_UPGRADE_CODE = "75e1b812-23a4-45ce-9e7c-84d7d43b8c70"
UPSTREAM_REPO = f"{UPSTREAM_OWNER}/revit-model-mcp"

FORK_OWNER = "vibe-bimer"
FORK_REPO = f"{FORK_OWNER}/revit-model-mcp"

# Files allowed to name upstream, with the reason each is correct. Everything
# else must name this fork: the fork owns its install identity, its package
# name, and the pages it publishes.
UPSTREAM_REFERENCES_ALLOWED = {
    "AGENTS.md": "states the rule that forbids reusing upstream's identity",
    "CONTRIBUTING.md": "points at sharafutdinovdi/.github for the code of conduct and caller workflows",
    "CHANGELOG.md": "historical release record",
    "CHANGELOG.zh.md": "historical release record (Chinese translation)",
    "docs/roadmap.md": "upstream issue numbers in the inherited roadmap",
    "docs/validation.md": "cites the upstream validation branch, issues and pull requests",
    "docs/design/model-audit.md": "cites upstream issues for the inherited audit design",
    "docs/agents/issue-tracker.md": "names the upstream remote because it says where the fork's issues live",
    "docs/agents/issue-tracker.en.md": "names the upstream remote because it says where the fork's issues live",
    "tools/check_fork_identity.py": "names upstream's repository because it is the check for that drift",
}

# Paths scanned for upstream repository claims. Generated docs, the site build
# output, the vendored Revit corpus and this fork's own analysis notes are
# excluded. Directories are pruned during the walk, not filtered afterwards,
# because the corpus alone holds tens of thousands of files.
SCAN_SUFFIXES = (
    ".md",
    ".yml",
    ".yaml",
    ".json",
    ".toml",
    ".cs",
    ".html",
    ".ps1",
    ".py",
)
PRUNED_DIRECTORIES = {
    ".agent-teams",
    ".git",
    ".venv",
    "analysis",
    "artifacts",
    "bin",
    "dist",
    "docs/features",
    "node_modules",
    "obj",
    "revit-corpus",
    "site",
    "site-lan",
}

UPSTREAM_REPO_PATTERN = re.compile(re.escape(UPSTREAM_REPO))
UPSTREAM_OWNER_FLAG = re.compile(r"--owner\s+" + re.escape(UPSTREAM_OWNER) + r"\b")
# ``sharafutdinovdi/.github`` is a different repository and stays allowed.
UPSTREAM_SITE_PATTERN = re.compile(
    re.escape(UPSTREAM_OWNER) + r"\.github\.io/revit-model-mcp"
)
PYPI_PUBLISH_ACTIONS = ("pypa/gh-action-pypi-publish", "mcp-publisher")

# A launcher installs this fork's server only from this fork's release wheel.
# Any of these forms resolves upstream's package instead, because both projects
# share version numbers: an exact pin, a version floor, a bare package name, or
# an explicit PyPI index.
FORK_SOURCE_URL = re.compile(
    r"https://github\.com/"
    + re.escape(FORK_REPO)
    + r"/(?:releases/download/v[0-9A-Za-z.\-]+/revit_model_mcp-[0-9A-Za-z.\-]+\.whl"
    r"|archive/refs/(?:tags/v[0-9A-Za-z.\-]+|heads/main)\.tar\.gz#subdirectory=server)"
)
BARE_PYPI_PACKAGE = re.compile(r"(?:^|[\s\"'])revit-model-mcp(?![\w.\-/])")

# A document that tells a reader to run this package name installs upstream's
# server, because both projects share version numbers and upstream owns the
# PyPI project. The check reads prose, workflows and launchers, not source
# tests: a fixture that asserts the validator rejects such a launcher is
# allowed to contain one.
PYPI_LAUNCHER = re.compile(r"\buvx\s+revit-model-mcp\b")
PYPI_VERSION_SPEC = re.compile(r"\brevit-model-mcp\s*(?:==|>=|<=|~=|!=)\s*\S")
PYPI_PROJECT_PAGE = re.compile(r"pypi\.org/project/revit-model-mcp")
PACKAGE_NAME_ALLOWED = {
    "CHANGELOG.md": "historical release notes name the package as it was published",
    "docs/admin/deployment.md": "an offline --no-index wheelhouse install cannot reach PyPI",
    "docs/validation.md": "upstream's own v0.9.0 evidence, framed as such",
    "server/tests/test_fork_identity.py": "the fixtures prove each rule can fire",
    "server/tests/test_validate_bundle.py": "a negative fixture asserts the validator rejects this launcher",
    "tests/RevitModelMcp.Core.Tests/Connect/McpClientConfiguratorTests.cs": "negative fixtures assert the editor leaves a foreign launcher alone",
    "tools/check_fork_identity.py": "the patterns themselves",
}


class IdentityError(Exception):
    """The check could not run, as opposed to finding drift."""


def read_text(relative: str) -> str:
    path = REPO_ROOT / relative
    if not path.is_file():
        raise IdentityError(f"missing file: {relative}")
    return path.read_text(encoding="utf-8")


def read_json(relative: str) -> dict:
    try:
        return json.loads(read_text(relative))
    except json.JSONDecodeError as error:
        raise IdentityError(f"{relative} is not valid JSON: {error}") from error


def iter_scanned_files() -> list[Path]:
    files = []
    for directory, subdirectories, names in os.walk(REPO_ROOT):
        root = Path(directory)
        relative_root = root.relative_to(REPO_ROOT).as_posix()
        prefix = "" if relative_root == "." else f"{relative_root}/"
        subdirectories[:] = sorted(
            name
            for name in subdirectories
            if f"{prefix}{name}" not in PRUNED_DIRECTORIES
        )
        for name in names:
            if Path(name).suffix in SCAN_SUFFIXES:
                files.append(root / name)
    return sorted(files)


def check_installer_upgrade_code(problems: list[str]) -> None:
    text = read_text("build/install/Installer.cs")
    match = re.search(r'GUID\s*=\s*new\s+Guid\("([0-9A-Fa-f-]{36})"\)', text)
    if match is None:
        problems.append("build/install/Installer.cs: no UpgradeCode GUID found")
        return
    if match.group(1).lower() == UPSTREAM_UPGRADE_CODE:
        problems.append(
            "build/install/Installer.cs: UpgradeCode is upstream's "
            f"{UPSTREAM_UPGRADE_CODE}, so installing upstream would replace this fork"
        )


def check_registry_manifest(problems: list[str]) -> None:
    if not (REPO_ROOT / "server/server.json").is_file():
        # This fork publishes no registry package, so no manifest is the
        # expected state; one that appears must not claim upstream's identity.
        return
    manifest = read_json("server/server.json")
    name = str(manifest.get("name", ""))
    if UPSTREAM_OWNER in name:
        problems.append(
            f"server/server.json: name {name!r} claims upstream's registry identity"
        )
    url = str(manifest.get("repository", {}).get("url", ""))
    if UPSTREAM_REPO in url:
        problems.append(
            f"server/server.json: repository.url {url!r} points at upstream"
        )


def mcp_config_arg_lists(manifest: dict) -> list[tuple[str, list[str]]]:
    """Return every launcher argument list, with the name used in messages."""
    config = manifest.get("server", {}).get("mcp_config", {})
    lists = [("args", [str(arg) for arg in config.get("args", [])])]
    for platform, override in config.get("platform_overrides", {}).items():
        lists.append(
            (
                f"platform_overrides.{platform}.args",
                [str(arg) for arg in override.get("args", [])],
            )
        )
    return lists


def check_bundle_manifest(problems: list[str]) -> None:
    manifest = read_json("bundle/manifest.json")
    author = str(manifest.get("author", {}).get("name", ""))
    if author == UPSTREAM_OWNER:
        problems.append("bundle/manifest.json: author.name is upstream's account")
    for field in ("homepage", "documentation"):
        value = str(manifest.get(field, ""))
        if UPSTREAM_SITE_PATTERN.search(value):
            problems.append(
                f"bundle/manifest.json: {field} {value!r} points at upstream's site"
            )
    url = str(manifest.get("repository", {}).get("url", ""))
    if UPSTREAM_REPO in url:
        problems.append(
            f"bundle/manifest.json: repository.url {url!r} points at upstream"
        )
    for policy in manifest.get("privacy_policies", []):
        if UPSTREAM_SITE_PATTERN.search(str(policy)):
            problems.append(
                f"bundle/manifest.json: privacy_policies entry {policy!r} points at upstream"
            )

    for name, args in mcp_config_arg_lists(manifest):
        command = " ".join(args)
        spec = PYPI_VERSION_SPEC.search(command)
        if spec is not None:
            problems.append(
                f"bundle/manifest.json: {name} resolve {spec.group(0)!r} on PyPI, "
                "which installs upstream's server because both projects share "
                "version numbers; point at this fork's release wheel instead"
            )
            continue
        if FORK_SOURCE_URL.search(command) is None and BARE_PYPI_PACKAGE.search(
            command
        ):
            problems.append(
                f"bundle/manifest.json: {name} install the bare package "
                "'revit-model-mcp', which uvx resolves on PyPI to upstream's "
                "server; install this fork's release wheel with --from instead"
            )


def check_vendor_settings(problems: list[str]) -> None:
    settings = read_json("build/appsettings.json")
    vendor = str(settings.get("VendorName", ""))
    if vendor == UPSTREAM_OWNER:
        problems.append("build/appsettings.json: VendorName is upstream's account")
    url = str(settings.get("VendorUrl", ""))
    if UPSTREAM_REPO in url:
        problems.append(f"build/appsettings.json: VendorUrl {url!r} points at upstream")


def check_glama(problems: list[str]) -> None:
    glama = read_json("glama.json")
    maintainers = [str(entry) for entry in glama.get("maintainers", [])]
    if UPSTREAM_OWNER in maintainers:
        problems.append("glama.json: maintainers lists upstream's account")


def check_release_workflow(problems: list[str]) -> None:
    text = read_text(".github/workflows/release.yml")
    for action in PYPI_PUBLISH_ACTIONS:
        if action in text:
            problems.append(
                f".github/workflows/release.yml: still references {action!r}; this fork "
                "cannot publish upstream's package name or registry identity"
            )
    if re.search(r"^\s+pypi:\s*$", text, re.MULTILINE):
        problems.append(".github/workflows/release.yml: still defines a pypi job")
    for number, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith("#"):
            continue
        if "revit-model-mcp==" in line:
            problems.append(
                f".github/workflows/release.yml:{number}: references a bare PyPI version "
                "spec, which resolves to upstream's package"
            )


# uvx with --from installs the named source, not the package index, so a
# --from line is drift only when the source itself serves upstream's package:
# an upstream repository URL (check_stray_references flags those) or PyPI.
FOREIGN_PYPI_SOURCE = re.compile(
    r"--from\s+\S*(?:sharafutdinovdi/|pypi\.org/|files\.pythonhosted\.org/)"
)


def launcher_problems(relative: str, text: str) -> list[str]:
    """Name every line of one file that would start the server from PyPI."""
    found: list[str] = []
    for number, line in enumerate(text.splitlines(), start=1):
        # Naming upstream does not excuse a runnable command: prose that warns
        # about the trap must reword it, not quote it.
        if PYPI_PROJECT_PAGE.search(line):
            found.append(
                f"{relative}:{number}: links upstream's PyPI project, which publishes "
                "a different server under the same name"
            )
            continue
        if "--from" in line:
            if FOREIGN_PYPI_SOURCE.search(line):
                found.append(
                    f"{relative}:{number}: installs the server with --from from a "
                    "source that serves upstream's package; both projects share "
                    "version numbers, so use this fork's release wheel or tag archive"
                )
            continue
        match = PYPI_LAUNCHER.search(line) or PYPI_VERSION_SPEC.search(line)
        if match is not None:
            found.append(
                f"{relative}:{number}: starts the server with {match.group(0)!r}, "
                "which uvx resolves on PyPI to upstream's server; use "
                "--from with this fork's release wheel or tag archive"
            )
    return found


def scanned_sources(allowlist: dict[str, str]) -> Iterator[tuple[str, str]]:
    """Yield (relative path, text) for every scanned file outside the allowlist."""
    for path in iter_scanned_files():
        relative = path.relative_to(REPO_ROOT).as_posix()
        if relative in allowlist:
            continue
        yield relative, path.read_text(encoding="utf-8")


def check_package_launchers(problems: list[str]) -> None:
    """Fail when a shipped file starts the server by the bare package name."""
    for relative, text in scanned_sources(PACKAGE_NAME_ALLOWED):
        problems.extend(launcher_problems(relative, text))


def check_stray_references(problems: list[str]) -> None:
    for relative, text in scanned_sources(UPSTREAM_REFERENCES_ALLOWED):
        for pattern, description in (
            (UPSTREAM_REPO_PATTERN, "upstream repository"),
            (UPSTREAM_SITE_PATTERN, "upstream documentation site"),
            (UPSTREAM_OWNER_FLAG, "upstream attestation owner"),
        ):
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                problems.append(
                    f"{relative}:{line}: names the {description} ({match.group(0)!r})"
                )


def main() -> int:
    problems: list[str] = []
    checks = (
        check_installer_upgrade_code,
        check_registry_manifest,
        check_bundle_manifest,
        check_vendor_settings,
        check_glama,
        check_release_workflow,
        check_package_launchers,
        check_stray_references,
    )
    try:
        for check in checks:
            check(problems)
    except IdentityError as error:
        print(f"identity check could not run: {error}", file=sys.stderr)
        return 2

    if problems:
        print("This fork ships under its own identity. Found drift:\n", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        print(
            f"\n{len(problems)} problem(s). Upstream is {UPSTREAM_REPO}; "
            f"this fork is {FORK_REPO}.",
            file=sys.stderr,
        )
        return 1

    print(f"identity check clean ({len(checks)} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
