#!/usr/bin/env python3
"""Fail closed on broken site links, missing anchors and navigation gaps."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

import yaml


@dataclass
class PageInfo:
    links: list[str] = field(default_factory=list)
    ids: set[str] = field(default_factory=set)
    article_text: list[str] = field(default_factory=list)
    canonical: str = ""


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.info = PageInfo()
        self.in_article = False
        self.ignored = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.info.ids.add(attrs["id"])
        if tag == "a" and "name" in attrs:
            self.info.ids.add(attrs["name"])
        for key in ("href", "src"):
            if attrs.get(key):
                self.info.links.append(attrs[key])
        if attrs.get("srcset"):
            self.info.links.extend(
                item.strip().split()[0]
                for item in attrs["srcset"].split(",")
                if item.strip()
            )
        if tag == "link" and "canonical" in attrs.get("rel", "").split():
            self.info.canonical = attrs.get("href", "")
        if tag == "article":
            self.in_article = True
        if self.in_article and tag in ("code", "script", "style"):
            self.ignored += 1

    def handle_endtag(self, tag):
        if self.in_article and tag in ("code", "script", "style"):
            self.ignored = max(0, self.ignored - 1)
        if tag == "article":
            self.in_article = False

    def handle_data(self, data):
        if self.in_article and not self.ignored:
            self.info.article_text.append(data)


def parse_page(path: Path) -> PageInfo:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.info


def page_url(path: Path, site: Path) -> str:
    relative = path.relative_to(site).as_posix()
    return "/" + relative.removesuffix("index.html")


def local_target(site: Path, url: str, base_url: str) -> tuple[Path, str] | None:
    parts, base = urlsplit(url), urlsplit(base_url)
    if parts.scheme not in ("", "http", "https") or parts.netloc != base.netloc:
        return None
    path = unquote(parts.path)
    prefix = base.path.rstrip("/")
    if prefix and path != prefix and not path.startswith(prefix + "/"):
        return None
    path = path[len(prefix) :].lstrip("/")
    candidate = (site / path).resolve()
    if not candidate.is_relative_to(site.resolve()):
        return site / "__outside_site__", unquote(parts.fragment)
    if candidate.is_dir() or parts.path.endswith("/"):
        candidate /= "index.html"
    return candidate, unquote(parts.fragment)


def audit_site(site: Path, base_url: str | None = None) -> tuple[list[str], dict]:
    """Check every internal link and anchor in the built site."""
    site = site.resolve()
    files = sorted(site.rglob("index.html"))
    if not files or not (site / "index.html").is_file():
        return [f"Missing built site: {site}"], {"pages": 0, "links": 0}
    parsed = {path: parse_page(path) for path in files}
    base_url = (
        base_url or parsed[site / "index.html"].canonical or "http://docs.invalid/"
    )
    base_url = base_url.rstrip("/") + "/"
    errors, total_links = [], 0
    for path, info in parsed.items():
        relative = path.relative_to(site).as_posix()
        origin = urljoin(base_url, page_url(path, site).lstrip("/"))
        for href in info.links:
            target = local_target(site, urljoin(origin, href), base_url)
            if target is None:
                continue
            total_links += 1
            destination, anchor = target
            if not destination.is_file():
                errors.append(f"{relative}: missing target {href!r}")
            elif anchor and destination.suffix == ".html":
                parsed_info = parsed.get(destination) or parse_page(destination)
                if anchor not in parsed_info.ids:
                    errors.append(f"{relative}: missing anchor {href!r}")
        if not "".join(info.article_text).strip():
            errors.append(f"{relative}: empty article")
    return sorted(set(errors)), {"pages": len(files), "links": total_links}


def expand_snippets(text: str, root: Path, depth: int = 0) -> str:
    """Inline `--8<-- "path"` includes the way docs/hooks.py does before MkDocs sees them."""
    if depth > 5:
        return text
    lines = []
    for line in text.splitlines():
        include = re.match(r'\s*--8<--\s+"([^"]+)"\s*$', line)
        if include:
            target = root / include.group(1)
            if target.is_file():
                lines.append(
                    expand_snippets(target.read_text(encoding="utf-8"), root, depth + 1)
                )
                continue
        lines.append(line)
    return "\n".join(lines)


def source_anchors(path: Path, root: Path | None = None) -> set[str]:
    """Anchors a page offers: explicit ids plus heading slugs, as MkDocs resolves them."""
    text = path.read_text(encoding="utf-8")
    if root is not None:
        text = expand_snippets(text, root)
    anchors = set(re.findall(r'<a\s+(?:id|name)="([^"]+)"', text))
    anchors |= set(re.findall(r"\{#([A-Za-z0-9_.:-]+)\}", text))
    for line in text.splitlines():
        heading = re.match(r"#{1,6}\s+(.*?)\s*$", line)
        if not heading:
            continue
        title = re.sub(r"\{#[^}]*\}\s*$", "", heading.group(1))
        title = re.sub(r"[`*_]", "", title).strip().lower()
        title = re.sub(r"[^\w\s-]", "", title)
        anchors.add(re.sub(r"[\s]+", "-", title).strip("-"))
    return anchors


def audit_source_anchors(root: Path) -> list[str]:
    """Verify every cross-file Markdown anchor target exists, including raw-HTML ids MkDocs can miss."""
    docs = root / "docs"
    sources = {
        path.resolve(): path
        for path in list(docs.rglob("*.md"))
        + list(root.glob("*.md"))
        + list((root / "server").glob("*.md"))
    }
    anchors = {path: source_anchors(path, root) for path in sources}
    errors = []
    for path, source in sorted(sources.items(), key=lambda item: str(item[1])):
        relative = source.relative_to(root).as_posix()
        for target, anchor in re.findall(
            r"\]\(([^)\s#]+\.md)#([^)\s]+)\)", source.read_text(encoding="utf-8")
        ):
            destination = (source.parent / unquote(target)).resolve()
            if destination not in sources:
                continue
            if anchor in anchors[destination] or re.fullmatch(r"_\d+", anchor):
                continue
            errors.append(
                f"{relative}: anchor '#{anchor}' is not produced by {destination.relative_to(root).as_posix()}"
            )
    return errors


def audit_sources(root: Path) -> list[str]:
    """Every documentation page is in the navigation, once, and every entry exists."""
    docs = root / "docs"
    config = yaml.safe_load((root / "mkdocs.yml").read_text(encoding="utf-8"))

    def flatten(node):
        if isinstance(node, str):
            yield node
        elif isinstance(node, list):
            for child in node:
                yield from flatten(child)
        elif isinstance(node, dict):
            for child in node.values():
                yield from flatten(child)

    navigation = list(flatten(config["nav"]))
    errors = []
    pages = {p.relative_to(docs).as_posix() for p in docs.rglob("*.md")}
    generated = {page for page in pages if page.startswith("features/")}
    for orphan in sorted(generated - set(navigation)):
        errors.append(f"Page missing from navigation: {orphan}")
    for target in navigation:
        if target not in pages:
            errors.append(f"Navigation references missing source: {target}")
        if navigation.count(target) > 1:
            errors.append(f"Duplicate navigation entry: {target}")
    errors += audit_source_anchors(root)
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", type=Path, default=Path("site"))
    parser.add_argument("--base-url")
    args = parser.parse_args()
    errors, stats = audit_site(args.site_dir, args.base_url)
    errors += audit_sources(Path(__file__).resolve().parents[2])
    print(f"Pages: {stats['pages']}; checked internal references: {stats['links']}")
    print(f"Site/source errors: {len(errors)}")
    for error in errors[:80]:
        print(f"  {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
