#!/usr/bin/env python3
"""Fail closed on broken site links, anchors, language pairs and navigation gaps."""

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
    alternates: dict[str, str] = field(default_factory=dict)
    ids: set[str] = field(default_factory=set)
    article_text: list[str] = field(default_factory=list)
    canonical: str = ""
    language: str = ""


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.info = PageInfo()
        self.in_article = False
        self.ignored = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.info.language = attrs.get("lang", "")
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
        if tag == "link":
            rel = attrs.get("rel", "").split()
            if "alternate" in rel and "hreflang" in attrs:
                self.info.alternates[attrs["hreflang"]] = attrs.get("href", "")
            if "canonical" in rel:
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
    site = site.resolve()
    files = sorted(site.rglob("index.html"))
    if not files or not (site / "index.html").is_file():
        return [f"Missing built site: {site}"], {
            "pages": 0,
            "zh": 0,
            "en": 0,
            "links": 0,
        }
    parsed = {path: parse_page(path) for path in files}
    base_url = (
        base_url or parsed[site / "index.html"].canonical or "http://docs.invalid/"
    )
    base_url = base_url.rstrip("/") + "/"
    errors, total_links = [], 0
    for path, info in parsed.items():
        relative = path.relative_to(site).as_posix()
        english = relative.startswith("en/")
        expected_lang = "en" if english else "zh"
        origin = urljoin(base_url, page_url(path, site).lstrip("/"))
        if info.language != expected_lang:
            errors.append(
                f"{relative}: html language is {info.language!r}, expected {expected_lang}"
            )
        if set(info.alternates) != {"zh", "en"}:
            errors.append(
                f"{relative}: expected zh/en alternates, found {sorted(info.alternates)}"
            )
        for lang, href in info.alternates.items():
            sibling = relative.removeprefix("en/")
            expected = site / (f"en/{sibling}" if lang == "en" else sibling)
            target = local_target(site, urljoin(origin, href), base_url)
            if target is None or target[0] != expected or not expected.is_file():
                errors.append(
                    f"{relative}: wrong {lang} language-switch target {href!r}"
                )
        for href in info.links:
            target = local_target(site, urljoin(origin, href), base_url)
            if target is None:
                continue
            total_links += 1
            destination, anchor = target
            if not destination.is_file():
                errors.append(f"{relative}: missing target {href!r}")
            elif anchor and destination.suffix == ".html":
                if destination not in parsed:
                    parsed_info = parse_page(destination)
                else:
                    parsed_info = parsed[destination]
                if anchor not in parsed_info.ids:
                    errors.append(f"{relative}: missing anchor {href!r}")
        text = "".join(info.article_text).strip()
        cjk = sum("\u4e00" <= char <= "\u9fff" for char in text)
        ratio = cjk / max(len(text), 1)
        if not text:
            errors.append(f"{relative}: empty article")
        elif english and ratio > 0.05:
            errors.append(f"{relative}: excessive Chinese prose ({ratio:.1%})")
        elif not english and ratio < 0.05:
            errors.append(f"{relative}: too little Chinese prose ({ratio:.1%})")
    zh = sum(not path.relative_to(site).as_posix().startswith("en/") for path in files)
    return sorted(set(errors)), {
        "pages": len(files),
        "zh": zh,
        "en": len(files) - zh,
        "links": total_links,
    }


def source_anchors(path: Path) -> set[str]:
    """Anchors a page offers: explicit ids plus heading slugs, as MkDocs resolves them."""
    text = path.read_text(encoding="utf-8")
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
    anchors = {path: source_anchors(path) for path in sources}
    errors = []
    for path, source in sorted(sources.items(), key=lambda item: str(item[1])):
        relative = source.relative_to(root).as_posix()
        for target, anchor in re.findall(
            r"\]\(([^)\s#]+\.md)#([^)\s]+)\)", source.read_text(encoding="utf-8")
        ):
            destination = (source.parent / unquote(target)).resolve()
            if destination not in sources:
                continue
            expected = (
                relative.removesuffix(".md") + ".en.md"
                if relative.endswith(".en.md")
                else relative
            )
            sibling = (
                destination.with_name(destination.stem + ".en.md")
                if expected.endswith(".en.md")
                else destination
            )
            if expected.endswith(".en.md") and sibling in sources:
                destination = sibling
            if anchor in anchors[destination] or re.fullmatch(r"_\d+", anchor):
                continue
            errors.append(
                f"{relative}: anchor '#{anchor}' is not produced by {destination.relative_to(root).as_posix()}"
            )
    return errors


def audit_sources(root: Path) -> list[str]:
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
    chinese = {p for p in pages if not p.endswith(".en.md")}
    english = {p.removesuffix(".en.md") + ".md" for p in pages if p.endswith(".en.md")}
    for missing in sorted(chinese ^ english):
        errors.append(f"Unpaired source page: {missing}")
    for orphan in sorted(chinese - set(navigation)):
        errors.append(f"Page missing from navigation: {orphan}")
    for target in navigation:
        if target not in chinese:
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
    print(
        f"Pages: {stats['pages']} (zh {stats['zh']} / en {stats['en']}); checked internal references: {stats['links']}"
    )
    print(f"Site/source errors: {len(errors)}")
    for error in errors[:80]:
        print(f"  {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
