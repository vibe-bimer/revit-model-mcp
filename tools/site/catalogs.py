#!/usr/bin/env python3
"""Declarative catalog manifest: version, status, provenance, ownership and language coverage.

The documentation publishes two tool catalogs side by side: the released surface under
docs/features and the unreleased integration branch under docs/platform. Everything that
distinguishes them is data in tools/site/content/catalogs.yaml, so no generator or checker
hard-codes a version string, a branch name, a tool count or a fork tool name.

The release version is read from project metadata (server/pyproject.toml) through the pointer
declared in the manifest, so it moves with the package on release.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

import tomllib
import yaml

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "tools/site/content"
MANIFEST = CONTENT / "catalogs.yaml"

SHA = re.compile(r"[0-9a-f]{40}")


@dataclass(frozen=True)
class Catalog:
    key: str
    directory: str
    status: str
    branch: str
    languages: tuple[str, ...]
    page_languages: dict[str, tuple[str, ...]]
    version: str


def manifest_path(root: Path | None = None) -> Path:
    return (root or ROOT) / "tools/site/content/catalogs.yaml"


def load(root: Path | None = None) -> dict:
    """Return the raw manifest, with language lists normalised to tuples."""
    data = yaml.safe_load(manifest_path(root).read_text(encoding="utf-8"))
    for key in ("release", "integration"):
        data[key]["languages"] = tuple(data[key]["languages"])
        data[key]["page_languages"] = {
            stem: tuple(langs)
            for stem, langs in (data[key].get("page_languages") or {}).items()
        }
    return data


def dump_yaml(data: dict) -> str:
    """Serialise a manifest back to YAML; used by tests that build temporary roots."""
    payload = {key: dict(value) for key, value in data.items()}
    for key in ("release", "integration"):
        payload[key]["languages"] = list(payload[key]["languages"])
        payload[key]["page_languages"] = {
            stem: list(langs) for stem, langs in payload[key]["page_languages"].items()
        }
    return yaml.safe_dump(payload, allow_unicode=True, sort_keys=False)


def _walk(data: dict, pointer: str):
    value = data
    for part in pointer.split("."):
        value = value[part]
    return value


def read_version(source: dict, root: Path | None = None) -> str:
    """Read a version string from the declared file and pointer, never a literal."""
    path = (root or ROOT) / source["file"]
    text = path.read_text(encoding="utf-8")
    fmt = source.get("format", "toml")
    if fmt == "toml":
        data = tomllib.loads(text)
    elif fmt == "json":
        data = json.loads(text)
    else:
        raise SystemExit(f"Unsupported version source format: {fmt}")
    value = _walk(data, source["pointer"])
    if not isinstance(value, str) or not value.strip():
        raise SystemExit(
            f"Version at {source['file']}:{source['pointer']} is not a non-empty string"
        )
    return value.strip()


def release(root: Path | None = None) -> Catalog:
    data = load(root)["release"]
    return Catalog(
        key="release",
        directory=data["directory"],
        status=data["status"],
        branch=data["branch"],
        languages=data["languages"],
        page_languages=data["page_languages"],
        version=read_version(data["version"], root),
    )


def integration(root: Path | None = None) -> Catalog:
    data = load(root)["integration"]
    return Catalog(
        key="integration",
        directory=data["directory"],
        status=data["status"],
        branch=data["branch"],
        languages=data["languages"],
        page_languages=data["page_languages"],
        version="",
    )


def fork_tools(root: Path | None = None) -> dict:
    return dict(load(root).get("fork_tools") or {})


def catalog_for_directory(directory: str, root: Path | None = None) -> Catalog | None:
    for catalog in (release(root), integration(root)):
        if catalog.directory == directory:
            return catalog
    return None


def provenance(root: Path | None = None) -> dict:
    data = load(root)["integration"]
    source = data.get("provenance") or {}
    path = (root or ROOT) / source["file"]
    return json.loads(path.read_text(encoding="utf-8"))["provenance"]


def audit(root: Path | None = None) -> None:
    """Fail closed when the manifest disagrees with the snapshot it describes."""
    root = root or ROOT
    rel = release(root)
    if rel.status != "released":
        raise SystemExit(
            f"release catalog status must be 'released', got {rel.status!r}"
        )
    integration_catalog = integration(root)
    if integration_catalog.status != "unreleased":
        raise SystemExit(
            "integration catalog status must be 'unreleased', "
            f"got {integration_catalog.status!r}"
        )
    prov = provenance(root)
    if integration_catalog.branch != prov.get("branch"):
        raise SystemExit(
            f"catalogs.yaml integration branch {integration_catalog.branch!r} "
            f"disagrees with platform-tools.json provenance {prov.get('branch')!r}"
        )
    commit = str(prov.get("commit", ""))
    if not SHA.fullmatch(commit):
        raise SystemExit(
            f"platform-tools.json provenance commit is not a full 40-char SHA: {commit!r}"
        )


def coverage_errors(root: Path | None = None) -> list[str]:
    """Every page must ship exactly the languages it declares: no missing, no extra.

    A catalog's default languages apply to each page unless page_languages overrides one
    stem. This is what lets an inherited page stay English-only while a promised translation
    that is not there fails the build.
    """
    root = root or ROOT
    data = load(root)
    errors: list[str] = []
    for key in ("release", "integration"):
        catalog = data[key]
        directory = root / "docs" / catalog["directory"]
        if not directory.is_dir():
            continue
        stems = {
            path.name.removesuffix(".en.md").removesuffix(".md")
            for path in directory.glob("*.md")
        }
        for stem in sorted(stems):
            promised = catalog["page_languages"].get(stem, catalog["languages"])
            for lang in promised:
                filename = f"{stem}.en.md" if lang == "en" else f"{stem}.md"
                if not (directory / filename).is_file():
                    errors.append(
                        f"{key}: promised {lang} translation missing for {stem}"
                    )
            for lang in ("zh", "en"):
                if lang in promised:
                    continue
                filename = f"{stem}.en.md" if lang == "en" else f"{stem}.md"
                if (directory / filename).is_file():
                    errors.append(f"{key}: {stem} has undeclared {lang} translation")
    return sorted(set(errors))
