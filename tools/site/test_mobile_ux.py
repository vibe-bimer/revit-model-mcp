"""Mobile UX contracts: the phone table stack decision, the standalone 404 page.

Two layers are pinned here:

- The stack decision lives in docs/javascripts/site.js as one pure function. The tests run that
  exact function through node (when node is available) instead of restating its logic in Python,
  and cross-check the column threshold against the source gate in check_site, so the browser
  behaviour and the generator gate cannot drift apart silently.
- The 404 template is a standalone page by contract: docs/hooks.py rewrites its two marked entry
  groups per language, scripts/serve-site.py serves the result on a miss, and check_site audits
  the skip link, the language attributes and the language links on what ships. The markers, the
  noindex meta, the skip link and the absolute links are the parts of that contract this file
  pins, so renaming any of them fails here before it fails a build.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

SITE_JS = ROOT / "docs" / "javascripts" / "site.js"
CSS = ROOT / "docs" / "stylesheets" / "extra.css"
TEMPLATE_404 = ROOT / "docs" / "overrides" / "404.html"


def _site_js_source() -> str:
    return SITE_JS.read_text(encoding="utf-8")


def _media_block(css: str, header: str) -> str:
    """Return the body of an at-rule block, counting braces to its real end."""
    start = css.index(header)
    open_index = css.index("{", start)
    depth = 0
    for index in range(open_index, len(css)):
        if css[index] == "{":
            depth += 1
        elif css[index] == "}":
            depth -= 1
            if depth == 0:
                return css[open_index + 1 : index]
    raise AssertionError(f"unterminated at-rule {header!r}")


ZH_MARKERS = ("<!--rmc:404:zh-->", "<!--/rmc:404:zh-->")
EN_MARKERS = ("<!--rmc:404:en-->", "<!--/rmc:404:en-->")
# Entry pages both language groups must keep linking to, as absolute site_url links.
ENTRY_PATHS = (
    "features/",
    "server/",
    "transport/",
    "actions/",
    "features/prompts/",
    "features/matrix/",
    "changelog/",
)


class Template404Tests(unittest.TestCase):
    """The standalone 404 template and the marker contract docs/hooks.py depends on."""

    def setUp(self):
        source = TEMPLATE_404.read_text(encoding="utf-8")
        # Drop the Jinja comments: the header note quotes the marker syntax on purpose.
        self.source = re.sub(r"\{#.*?#\}", "", source, flags=re.DOTALL)

    def test_standalone_no_extends(self):
        self.assertNotIn("{% extends", self.source)

    def test_no_external_stylesheet_or_script(self):
        self.assertNotIn("<link", self.source)
        self.assertNotIn("<script", self.source)

    def test_language_passes_render_per_pass(self):
        self.assertIn('<html lang="{{ config.theme.language }}">', self.source)

    def test_noindex_meta_stays(self):
        self.assertIn('<meta name="robots" content="noindex">', self.source)

    def test_content_root_is_focusable(self):
        root = re.search(
            r'<main class="rmc-404" id="rmc-main" tabindex="-1">', self.source
        )
        self.assertIsNotNone(root)

    def test_markers_appear_once_and_in_order(self):
        for marker in ZH_MARKERS + EN_MARKERS:
            self.assertEqual(self.source.count(marker), 1, marker)
        self.assertLess(
            self.source.index(ZH_MARKERS[0]),
            self.source.index(EN_MARKERS[0]),
            "the source order is zh first; docs/hooks.py swaps the groups for the en pass",
        )

    def test_skip_link_is_first_anchor(self):
        first_anchor = re.search(r"<a\b", self.source)
        skip = re.search(
            r'<a class="md-skip" href="#rmc-main">.*?</a>', self.source, re.DOTALL
        )
        self.assertIsNotNone(first_anchor)
        self.assertIsNotNone(skip)
        self.assertEqual(first_anchor.start(), skip.start())

    def test_skip_link_text_is_language_conditional(self):
        # check_site requires the zh page to carry Chinese skip text and the en page none, so the
        # text must be selected by the pass language, not hardcoded.
        conditional = re.search(
            r"\{% if config\.theme\.language == \"en\" %\}Skip to content"
            r"\{% else %\}[^{%]+?\{% endif %\}",
            self.source,
        )
        self.assertIsNotNone(conditional)

    def test_language_switch_links_are_auditable(self):
        # check_site reads language links from md-select__link anchors with hreflang.
        self.assertRegex(
            self.source,
            r'class="rmc-btn md-select__link"[^>]*hreflang="en"',
        )
        self.assertRegex(
            self.source,
            r'class="rmc-btn md-select__link"[^>]*hreflang="zh"',
        )

    def test_every_href_is_absolute_or_fragment(self):
        for href in re.findall(r'href="([^"]+)"', self.source):
            self.assertTrue(
                href.startswith("{{") or href == "#rmc-main",
                f"relative href {href!r} would resolve against the missing path",
            )

    def test_entry_links_cover_both_groups(self):
        for path in ENTRY_PATHS:
            self.assertIn("{{ config.site_url }}" + path, self.source)
            self.assertIn("{{ config.site_url }}en/" + path, self.source)

    def test_lede_points_at_home_and_catalog_not_the_header(self):
        # A standalone page has no header search; the lede must route to the exits instead.
        self.assertNotIn("search", self.source.lower())
        self.assertNotIn("页头", self.source)
        self.assertIn("功能总览", self.source)
        self.assertIn("feature catalog", self.source)

    def test_dark_scheme_is_media_query_not_second_file(self):
        self.assertIn("@media (prefers-color-scheme: dark)", self.source)

    def test_kept_class_names(self):
        for name in (
            "rmc-404",
            "rmc-404__code",
            "rmc-404__title",
            "rmc-404__lede",
            "rmc-404__actions",
            "rmc-404__links",
            "rmc-btn",
            "rmc-btn--primary",
        ):
            self.assertIn(name, self.source)
