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
    released_version: str = ""


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
    payload = {}
    for key, value in data.items():
        if isinstance(value, dict):
            payload[key] = dict(value)
        elif isinstance(value, (list, tuple)):
            payload[key] = list(value)
        else:
            payload[key] = value
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
        released_version=str(data.get("released_version") or "").strip(),
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


def inherited_pages(root: Path | None = None) -> frozenset[str]:
    """Docs paths the site ships in English only until a zh translation exists.

    Inherited upstream pages arrive as English prose in the default (Chinese) tree. ADR-0007
    keeps them bilingual-by-declaration instead of forcing a translation, so the language
    audits exempt exactly the paths listed here and still fail on anything undeclared.
    """
    try:
        pages = load(root).get("inherited_pages") or []
    except FileNotFoundError:
        return frozenset()
    return frozenset(str(page).strip() for page in pages if str(page).strip())


OBJECT_ORDER = ("views", "sheets", "schedules", "view-display")


def _catalog_tool_names(root: Path | None = None) -> set[str]:
    """Every tool name either catalog publishes, from the snapshots the site is built from."""
    root = root or ROOT
    names: set[str] = set()
    released = root / "tools/site/content/tools.json"
    if released.is_file():
        names.update(
            tool["name"] for tool in json.loads(released.read_text(encoding="utf-8"))
        )
    source = load(root)["integration"].get("provenance") or {}
    if source:
        path = root / source["file"]
        if path.is_file():
            data = json.loads(path.read_text(encoding="utf-8"))
            names.update(tool["name"] for tool in data.get("tools") or [])
    return names


def object_groups(root: Path | None = None) -> dict[str, dict]:
    """Return the object grouping both catalogs browse by, in declaration order.

    Membership is data so the two indexes and the platform navigation cannot drift apart.
    A tool that neither catalog publishes, or one listed twice, fails the load instead of
    quietly vanishing from the navigation.
    """
    root = root or ROOT
    path = root / "tools/site/content/object-groups.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    groups = data.get("groups") or {}
    known = _catalog_tool_names(root)
    seen: dict[str, str] = {}
    result: dict[str, dict] = {}
    for key in OBJECT_ORDER:
        group = groups.get(key)
        if not group:
            raise SystemExit(f"object-groups.yaml is missing group {key!r}")
        tools = [str(name) for name in group.get("tools") or []]
        for name in tools:
            if name in seen:
                raise SystemExit(
                    f"object-groups.yaml lists {name} in {seen[name]} and {key}"
                )
            if name not in known:
                raise SystemExit(
                    f"object-groups.yaml names {name}, which neither catalog publishes"
                )
            seen[name] = key
        result[key] = {
            "zh": str(group["zh"]),
            "en": str(group["en"]),
            "tools": tools,
        }
    unknown = sorted(set(groups) - set(OBJECT_ORDER))
    if unknown:
        raise SystemExit(f"object-groups.yaml declares unknown groups: {unknown}")
    return result


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
