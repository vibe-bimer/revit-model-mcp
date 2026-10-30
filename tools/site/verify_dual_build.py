#!/usr/bin/env python3
"""Build both deployment configs strictly and cross-check the two outputs.

The site ships in two configurations: the GitHub Pages build (``mkdocs.yml``,
served under a project path) and the LAN build (``mkdocs-lan.yml``, served from
the root of a plain file server). Both must build under ``--strict`` and both
must pass :mod:`check_site` with their own ``--base-url``. On top of that the
two outputs are compared deterministically: after normalizing the deployment
base (absolute URLs, root-relative prefixes, robots policy and volatile
manifest fields) the two trees must match file for file. The comparison never
asserts a fixed page, asset or tool count.

Usage::

    python tools/site/verify_dual_build.py [--work-root DIR] [--skip-build]
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

# Manifest fields that legitimately change between builds: timestamps and
# release/tree identifiers produced by the publishing pipeline.
VOLATILE_MANIFEST_FIELDS = (
    "built_utc",
    "release_id",
    "source_commit",
    "tree_sha",
    "tree_sha256",
)
VOLATILE_MANIFEST_SECTIONS = ("verification",)


def load_site_url(config_path: Path) -> str:
    """Return the ``site_url`` declared by an mkdocs config file."""

    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    url = (data or {}).get("site_url")
    if not url or not isinstance(url, str):
        raise SystemExit(f"{config_path}: site_url is missing")
    return url


def builder_command() -> list[str]:
    """Find the mkdocs executable the same way publish_site.py does."""

    configured = os.environ.get("MKDOCS", "").strip()
    if configured:
        return configured.split()
    for candidate in (
        ROOT / ".venv-docs" / "bin" / "mkdocs",
        Path.home() / ".venv-docs" / "bin" / "mkdocs",
    ):
        if candidate.is_file():
            return [str(candidate)]
    found = shutil.which("mkdocs")
    if found:
        return [found]
    raise SystemExit(
        "mkdocs was not found; install docs/requirements.txt or set MKDOCS"
    )


def normalize_text(text: str, base_url: str) -> str:
    """Erase deployment-base differences and volatile fields from text.

    Absolute ``site_url`` values collapse onto one placeholder, and
    root-relative attribute URLs drop the project path prefix. The prefix
    strip is anchored on the quote that opens the attribute value so that
    unrelated URLs which merely contain the same path segment (GitHub repo
    links, prose samples) are left untouched.
    """

    base_url = base_url.rstrip("/") + "/"
    prefix = urlsplit(base_url).path.strip("/")
    text = text.replace(base_url, "<site-base>/")
    if prefix:
        for quote in ('"', "'"):
            text = text.replace(f"{quote}/{prefix}/", f"{quote}/")
    return normalize_volatile(text)


def normalize_volatile(text: str) -> str:
    """Blank out volatile timestamps and artifact ids in embedded manifests."""

    try:
        data = json.loads(text)
    except (ValueError, TypeError):
        return text
    changed = False

    def scrub(node):
        nonlocal changed
        if isinstance(node, dict):
            for key in list(node):
                if key in VOLATILE_MANIFEST_SECTIONS:
                    node[key] = "<volatile-section>"
                    changed = True
                elif key in VOLATILE_MANIFEST_FIELDS:
                    node[key] = "<volatile>"
                    changed = True
                else:
                    scrub(node[key])
        elif isinstance(node, list):
            for item in node:
                scrub(item)

    scrub(data)
    if not changed:
        return text
    return json.dumps(data, indent=2, sort_keys=True)


def normalize_bytes(payload: bytes, base_url: str) -> str | bytes:
    """Normalize text-like artifacts; decompress gzip streams for comparison."""

    if payload[:2] == b"\x1f\x8b":
        try:
            payload = gzip.decompress(payload)
        except OSError:
            return payload
    try:
        return normalize_text(payload.decode("utf-8"), base_url)
    except UnicodeDecodeError:
        return payload


def compare_robots(gh_text: str, lan_text: str, gh_base: str) -> list[str]:
    """Assert the expected robots policy per deployment target."""

    problems = []
    gh_base = gh_base.rstrip("/") + "/"
    if "Allow: /" not in gh_text or f"Sitemap: {gh_base}sitemap.xml" not in gh_text:
        problems.append(
            "robots.txt (pages build) must allow crawling and point at the "
            f"pages sitemap (expected 'Sitemap: {gh_base}sitemap.xml')"
        )
    if "Disallow: /" not in lan_text:
        problems.append("robots.txt (lan build) must disallow crawling")
    return problems


def relative_files(root: Path) -> set[str]:
    return {str(path.relative_to(root)) for path in root.rglob("*") if path.is_file()}


def compare_sites(
    gh_dir: Path, lan_dir: Path, gh_base: str, lan_base: str, max_report: int = 10
) -> list[str]:
    """Compare two site trees deterministically; never assert fixed counts."""

    problems: list[str] = []
    gh_files, lan_files = relative_files(gh_dir), relative_files(lan_dir)
    missing = sorted(gh_files - lan_files)
    extra = sorted(lan_files - gh_files)
    if missing:
        problems.append(f"files only in pages build: {missing[:max_report]}")
    if extra:
        problems.append(f"files only in lan build: {extra[:max_report]}")
    for rel in sorted(gh_files & lan_files):
        gh_raw = (gh_dir / rel).read_bytes()
        lan_raw = (lan_dir / rel).read_bytes()
        if rel == "robots.txt":
            problems.extend(
                compare_robots(
                    gh_raw.decode("utf-8", "replace"),
                    lan_raw.decode("utf-8", "replace"),
                    gh_base,
                )
            )
            continue
        gh_norm = normalize_bytes(gh_raw, gh_base)
        lan_norm = normalize_bytes(lan_raw, lan_base)
        if gh_norm != lan_norm:
            problems.append(f"normalized content differs: {rel}")
    return problems


def run(command: list[str], *, cwd: Path) -> None:
    print(f"+ {' '.join(command)}", flush=True)
    subprocess.run(command, cwd=cwd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Strictly build both site configs and cross-check them."
    )
    parser.add_argument(
        "--work-root",
        default=str(ROOT),
        help="directory receiving site/ and site-lan/ (default: repo root)",
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="reuse existing output directories, build nothing",
    )
    parser.add_argument(
        "--max-report",
        type=int,
        default=10,
        help="maximum mismatches to list per category",
    )
    args = parser.parse_args()

    work_root = Path(args.work_root).resolve()
    gh_dir = work_root / "site"
    lan_dir = work_root / "site-lan"
    gh_config = ROOT / "mkdocs.yml"
    lan_config = ROOT / "mkdocs-lan.yml"
    gh_base = load_site_url(gh_config)
    lan_base = load_site_url(lan_config)

    if not args.skip_build:
        mkdocs = builder_command()
        run(
            mkdocs + ["build", "--strict", "-f", str(gh_config), "-d", str(gh_dir)],
            cwd=ROOT,
        )
        run(
            mkdocs + ["build", "--strict", "-f", str(lan_config), "-d", str(lan_dir)],
            cwd=ROOT,
        )

    for label, site_dir, base in (
        ("pages", gh_dir, gh_base),
        ("lan", lan_dir, lan_base),
    ):
        run(
            [
                sys.executable,
                "tools/site/check_site.py",
                "--site-dir",
                str(site_dir),
                "--base-url",
                base,
            ],
            cwd=ROOT,
        )
        print(f"check_site ({label}, base {base}): pass", flush=True)

    problems = compare_sites(
        gh_dir, lan_dir, gh_base, lan_base, max_report=args.max_report
    )
    if problems:
        for problem in problems[: args.max_report]:
            print(f"FAIL {problem}", file=sys.stderr)
        return 1
    print("dual-config deterministic comparison: pass", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
