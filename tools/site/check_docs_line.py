"""Fail when the published documentation line is missing from the checkout.

PR #42 merged a rebase line that dropped the whole documentation tree, and
every CI pipeline stayed green while the scheduled publisher died and the
public site lost its platform pages. This gate asserts that the checkout can
still build and publish the site: the configuration, the generator, the
auditor, the server and the publisher all have to be present, and both tool
sections still have to carry every documented tool.

Run it from the repository root:

    python tools/site/check_docs_line.py
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Every entry is a file the site cannot be built or published without.
REQUIRED_FILES: tuple[tuple[str, str], ...] = (
    ("mkdocs.yml", "the public site configuration"),
    ("mkdocs-lan.yml", "the LAN site configuration"),
    ("docs/hooks.py", "the search index hook"),
    ("docs/overrides/main.html", "the metadata overrides"),
    ("docs/index.md", "the site landing page"),
    ("docs/features/index.md", "the released tool index"),
    ("docs/platform/index.md", "the integration branch tool index"),
    ("docs/requirements.txt", "the hashed documentation dependencies"),
    ("tools/site/check_site.py", "the site auditor"),
    ("tools/site/generate_features.py", "the page generator"),
    ("tools/site/verify_dual_build.py", "the dual configuration gate"),
    ("tools/site/catalogs.py", "the catalog loader"),
    ("scripts/serve-site.py", "the local server"),
    ("scripts/publish_site.py", "the release publisher"),
    ("scripts/site-cron.sh", "the scheduled publisher"),
)

# Each section lists one page per documented tool. The floor is the number of
# tools the section must carry; a smaller section means pages were dropped.
MINIMUM_TOOL_PAGES: tuple[tuple[str, int], ...] = (
    ("docs/features", 87),
    ("docs/platform", 80),
)


def repository_root() -> Path:
    """Return the repository root, which is the parent of tools/site."""
    return Path(__file__).resolve().parents[2]


def missing_files(root: Path) -> list[str]:
    """Return the required files that are absent from the checkout."""
    return [path for path, _ in REQUIRED_FILES if not (root / path).is_file()]


def tool_page_count(root: Path, section: str) -> int:
    """Return the number of Chinese tool pages in a section."""
    directory = root / section
    if not directory.is_dir():
        return 0
    return len(
        [
            page
            for page in directory.glob("revit_*.md")
            if not page.name.endswith(".en.md")
        ]
    )


def short_sections(root: Path) -> list[str]:
    """Return the sections that carry fewer tool pages than their floor."""
    problems = []
    for section, floor in MINIMUM_TOOL_PAGES:
        count = tool_page_count(root, section)
        if count < floor:
            problems.append(
                f"{section} has {count} tool pages, expected at least {floor}"
            )
    return problems


def check(root: Path) -> list[str]:
    """Return every problem that stops the site from being built and published."""
    problems = []
    for path in missing_files(root):
        reasons = dict(REQUIRED_FILES)
        problems.append(f"missing {path} ({reasons[path]})")
    problems.extend(short_sections(root))
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=None, help="the repository root to check"
    )
    args = parser.parse_args(argv)
    root = args.root.resolve() if args.root else repository_root()
    problems = check(root)
    if problems:
        print("The documentation line is incomplete:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1
    print(
        f"PASS: the documentation line is intact ({len(REQUIRED_FILES)} files, {len(MINIMUM_TOOL_PAGES)} tool sections)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
