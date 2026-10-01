"""Resolve included Markdown links relative to their repository source."""

import posixpath
import re
from pathlib import Path
from urllib.parse import urlsplit

from markdown import Markdown

# Each entry maps the repository files that back a documentation page to its Chinese and English page, so a
# link to any of those files resolves to the page the current language build actually has.
SOURCES = [
    (["README.md"], "index.md", "index.en.md"),
    (["server/README.zh.md", "server/README.md"], "server.md", "server.en.md"),
    (
        ["CONTRIBUTING.zh.md", "CONTRIBUTING.md"],
        "contributing.md",
        "contributing.en.md",
    ),
    (["SECURITY.zh.md", "SECURITY.md"], "security-policy.md", "security-policy.en.md"),
    (["CHANGELOG.zh.md", "CHANGELOG.md"], "changelog.md", "changelog.en.md"),
]


def on_page_markdown(markdown, page, config, files):
    root = Path(config.config_file_path).parent
    for sources, chinese_page, english_page in SOURCES:
        if page.file.src_uri == chinese_page:
            source = sources[0]
            break
        if page.file.src_uri == english_page:
            source = sources[-1]
            break
    else:
        source = f"docs/{page.file.src_uri}"
    # Expand snippets before MkDocs validates links, retaining one source of content.
    processor = Markdown(
        extensions=["pymdownx.snippets"],
        extension_configs={
            "pymdownx.snippets": {"base_path": [str(root)], "check_paths": True}
        },
    )
    markdown = "\n".join(processor.preprocessors["snippet"].run(markdown.splitlines()))
    # One repository file can back more than one page (the README backs the Chinese landing page and the
    # English home), so keep every candidate and prefer the one this language build actually has.
    pages: dict[str, list[str]] = {}
    for sources, chinese_page, english_page in SOURCES:
        for repository_file in sources:
            pages.setdefault(repository_file, []).extend([chinese_page, english_page])
    if any(
        page.file.src_uri == pair[1] or page.file.src_uri == pair[2] for pair in SOURCES
    ):
        page.edit_url = f"{config.repo_url}/edit/main/{source}"

    def resolve(target):
        if target.startswith(config.site_url):
            relative = target[len(config.site_url) :]
            path, separator, anchor = relative.partition("#")
            candidate = f"{path.rstrip('/')}.md" if path else "index.md"
            if files.get_file_from_path(candidate):
                return candidate + (separator + anchor if separator else "")
        url = urlsplit(target)
        if url.scheme or url.netloc or not url.path:
            return target
        path = posixpath.normpath(posixpath.join(posixpath.dirname(source), url.path))
        suffix = (f"?{url.query}" if url.query else "") + (
            f"#{url.fragment}" if url.fragment else ""
        )
        if path in pages:
            for candidate in pages[path]:
                if files.get_file_from_path(candidate):
                    return candidate + suffix
            return pages[path][0] + suffix
        if path.startswith("docs/"):
            return (
                posixpath.relpath(path[5:], posixpath.dirname(page.file.src_uri))
                + suffix
            )
        if (root / path).is_file():
            return f"{config.repo_url}/blob/main/{path}{suffix}"
        return target

    markdown = re.sub(
        r"(\]\()([^\s)]+)(\))", lambda m: m[1] + resolve(m[2]) + m[3], markdown
    )
    markdown = re.sub(
        r'(\b(?:src|srcset)=")([^"]+)(")',
        lambda m: m[1] + resolve(m[2]) + m[3],
        markdown,
    )
    return markdown
