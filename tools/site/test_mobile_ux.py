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

import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

import check_site

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


class StackDecisionTests(unittest.TestCase):
    """The pure stack-decision helper in site.js, executed as written."""

    JS_BLOCK = re.compile(
        r"var STACK_MIN_COLUMNS = (\d+);.*?function stacksWhenNarrow\(columns, narrow\) \{(.*?)\n  \}",
        re.DOTALL,
    )

    def _helper(self) -> tuple[int, str]:
        match = self.JS_BLOCK.search(_site_js_source())
        self.assertIsNotNone(
            match, "stacksWhenNarrow and STACK_MIN_COLUMNS must stay in site.js"
        )
        return int(match.group(1)), match.group(2)

    @unittest.skipIf(shutil.which("node") is None, "node is not installed")
    def test_decision_thresholds(self):
        threshold, body = self._helper()
        script = (
            f"var STACK_MIN_COLUMNS = {threshold};\n"
            + "function stacksWhenNarrow(columns, narrow) {"
            + body
            + "\n}\n"
        )
        cases = [(4, False), (5, False), (4, True), (5, True), (6, True), (12, True)]
        calls = ";".join(
            "console.log(JSON.stringify([{c}, {n}, stacksWhenNarrow({c}, {n})]))".format(
                c=columns, n=str(narrow).lower()
            )
            for columns, narrow in cases
        )
        result = subprocess.run(
            ["node", "-e", script + calls],
            capture_output=True,
            text=True,
            check=True,
        )
        observed = [tuple(json.loads(line)) for line in result.stdout.splitlines()]
        # Narrow viewport stacks at the threshold and above; wide viewport never stacks.
        expected = [
            (4, False, False),
            (5, False, False),
            (4, True, False),
            (5, True, True),
            (6, True, True),
            (12, True, True),
        ]
        self.assertEqual(observed, expected)

    def test_threshold_matches_source_gate(self):
        threshold, _ = self._helper()
        self.assertEqual(
            threshold,
            check_site.WIDE_TABLE_COLUMNS,
            "the script and the source gate must agree on what counts as a wide table",
        )

    def test_sync_table_uses_the_helper(self):
        source = _site_js_source()
        self.assertIn("stacksWhenNarrow(columns, stackQuery.matches)", source)
        self.assertNotIn("columns >= 5", source)


class StackLayoutTests(unittest.TestCase):
    """The stacked layout shows every field, and nothing else regressed."""

    def test_stack_block_reveals_labels_and_hides_nothing(self):
        css = CSS.read_text(encoding="utf-8")
        block = _media_block(css, "@media screen and (max-width: 30em)")
        self.assertIn(".rmc-tablewrap[data-rmc-stack]", block)
        # Cells render as blocks and name themselves from the pinned header text.
        self.assertIn("content: attr(data-rmc-label)", block)
        # Nothing is dropped from a stacked row: the header is only visually clipped and no
        # rule in the block hides a cell.
        self.assertIn("clip-path: inset(50%)", block)
        self.assertNotIn("display: none", block)

        td_rule = re.search(
            r"\.rmc-tablewrap\[data-rmc-stack\] td \{(.*?)\}", block, re.DOTALL
        )
        self.assertIsNotNone(td_rule)
        self.assertNotIn("font-size", td_rule.group(1))


class ContentReinitTests(unittest.TestCase):
    """The content-change re-run is wired once, debounced, and idle when nothing navigates."""

    def setUp(self):
        self.source = _site_js_source()

    def test_boot_runs_content_setup_then_watches(self):
        boot = re.search(r"function boot\(\) \{(.*?)\n  \}", self.source, re.DOTALL)
        self.assertIsNotNone(boot)
        body = boot.group(1)
        self.assertIn("initContent();", body)
        self.assertIn("watchContent();", body)

    def test_reinit_uses_document_observable_or_observer(self):
        self.assertIn("window.document$.subscribe", self.source)
        self.assertIn("new MutationObserver", self.source)
        # The first document$ emission is the boot load, already initialised.
        self.assertIn("if (first) {", self.source)

    def test_reinit_is_debounced(self):
        self.assertIn("var CONTENT_DEBOUNCE_MS = 150;", self.source)
        self.assertIn("setTimeout(flushContentInit, CONTENT_DEBOUNCE_MS)", self.source)

    def test_watchers_install_once(self):
        self.assertIn("if (contentWatched) return;", self.source)
        self.assertIn("if (!runTableSync.registered) {", self.source)

    def test_own_writes_do_not_retrigger_the_observer(self):
        # The table wrap is a content write; the re-run pauses the observer around it.
        self.assertIn("pauseContentWatch", self.source)
        self.assertIn("resumeContentWatch", self.source)
