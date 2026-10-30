"""Accessibility contracts for the built site: skip links, table semantics and scroll regions.

These tests pin the structural markup the reading and keyboard requirements depend on. They cover
three layers: the page-level checks check_site runs over every built page, the templates and
generators that emit that markup, and the stylesheet and script that finish the job in the browser.
"""

import unittest
from pathlib import Path

import check_site
import generate_features
import platform_catalog

ROOT = Path(__file__).resolve().parents[2]

# A minimal page that satisfies the skip-link contract: the skip link is the first link in the
# document and its fragment resolves to a focusable content root.
SKIPPED_PAGE = """<!DOCTYPE html>
<html lang="zh">
<body>
<a class="md-skip" href="#rmc-main">跳转至内容</a>
<header><a href="/">Home</a></header>
<article><div id="rmc-main" tabindex="-1"><p>正文</p></div></article>
</body>
</html>
"""


def _page(body: str, skip: str | None = None) -> str:
    skip = (
        skip
        if skip is not None
        else '<a class="md-skip" href="#rmc-main">跳转至内容</a>'
    )
    return f"""<!DOCTYPE html>
<html lang="zh">
<body>
{skip}
<header><a href="/">Home</a></header>
<article>{body}</article>
</body>
</html>
"""


class ContrastTests(unittest.TestCase):
    """Text a reader can see holds the contrast floor in both colour schemes."""

    def setUp(self):
        self.css = (ROOT / "docs/stylesheets/extra.css").read_text(encoding="utf-8")
        self.landing_css = (ROOT / "docs/stylesheets/landing.css").read_text(
            encoding="utf-8"
        )
        self.script = (ROOT / "docs/javascripts/site.js").read_text(encoding="utf-8")

    def test_decorative_landing_text_holds_the_contrast_floor(self):
        # Both marks carried the hairline rule colour, which measured 1.6:1 as text.
        landing = (ROOT / "docs/stylesheets/landing.css").read_text(encoding="utf-8")
        for selector in ("\n.rmc-prompt__mark {", "\n.rmc-cap__num {"):
            block = landing.split(selector, 1)[1][:200]
            self.assertNotIn("--rmc-rule-strong", block)
            self.assertIn("--rmc-ink-3", block)

    def test_the_step_badge_flips_its_label_on_the_dark_palette(self):
        # White on the slate brand measured 2.63:1.
        landing = (ROOT / "docs/stylesheets/landing.css").read_text(encoding="utf-8")
        block = landing.split('[data-md-color-scheme="slate"] .rmc-flow__num {', 1)[1][
            :120
        ]
        self.assertIn("color: var(--rmc-paper);", block)

    def test_the_heading_anchor_holds_the_text_contrast_floor(self):
        # It is revealed on heading hover, so the glyph is text and needs a text colour.
        block = self.css.split(".md-typeset .headerlink {", 1)[1][:220]
        self.assertIn("color: var(--rmc-ink-3);", block)
        self.assertNotIn("--rmc-rule-strong", block)

    def test_the_primary_button_flips_its_label_on_the_dark_palette(self):
        # White on the dark palette's brand measures 2.6:1; dark ink on the same fill measures 7.5:1.
        landing = (ROOT / "docs/stylesheets/landing.css").read_text(encoding="utf-8")
        self.assertIn('[data-md-color-scheme="slate"] .rmc-btn--primary', landing)


class SkipLinkGateTests(unittest.TestCase):
    """The page-level gate: every built page opens with a skip link that works."""

    def test_a_working_skip_link_passes(self):
        self.assertEqual(check_site.audit_skip_link("index.html", SKIPPED_PAGE), [])

    def test_a_page_without_a_skip_link_is_an_error(self):
        page = _page("<p>正文</p>", skip="")
        self.assertIn(
            "index.html: missing skip link",
            check_site.audit_skip_link("index.html", page),
        )

    def test_a_skip_link_pointing_at_a_missing_id_is_an_error(self):
        page = _page(
            "<p>正文</p>", skip='<a class="md-skip" href="#nowhere">跳转至内容</a>'
        )
        errors = check_site.audit_skip_link("index.html", page)
        self.assertTrue(
            any("is not an element on this page" in e for e in errors), errors
        )

    def test_a_content_root_without_tabindex_is_an_error(self):
        page = _page('<div id="rmc-main"><p>正文</p></div>')
        errors = check_site.audit_skip_link("index.html", page)
        self.assertTrue(any('lacks tabindex="-1"' in e for e in errors), errors)

    def test_a_skip_link_that_is_not_the_first_link_is_an_error(self):
        page = """<!DOCTYPE html>
<html lang="zh">
<body>
<header><a href="/">Home</a></header>
<a class="md-skip" href="#rmc-main">跳转至内容</a>
<div id="rmc-main" tabindex="-1"><p>正文</p></div>
</body>
</html>
"""
        errors = check_site.audit_skip_link("index.html", page)
        self.assertTrue(any("not the first link" in e for e in errors), errors)

    def test_the_skip_link_uses_the_page_language(self):
        english = SKIPPED_PAGE.replace('lang="zh"', 'lang="en"')
        errors = check_site.audit_skip_link("en/index.html", english)
        self.assertTrue(any("page language" in e for e in errors), errors)
        translated = english.replace("跳转至内容", "Skip to content")
        self.assertEqual(check_site.audit_skip_link("en/index.html", translated), [])


class TableSemanticsGateTests(unittest.TestCase):
    """The page-level gate: header association survives, wide tables sit in a wrapper."""

    SCOPED = """<!DOCTYPE html>
<html lang="zh">
<body>
<div id="rmc-main" tabindex="-1">
<div class="rmc-tablewrap"><table>
<thead><tr><th scope="col">名称</th><th scope="col">说明</th></tr></thead>
<tbody><tr><td>a</td><td>b</td></tr></tbody>
</table></div>
</div>
</body>
</html>
"""

    def test_a_wrapped_scoped_table_passes(self):
        self.assertEqual(
            check_site.audit_table_semantics("features/x/index.html", self.SCOPED), []
        )

    def test_a_table_without_a_header_row_is_an_error(self):
        page = self.SCOPED.replace(
            '<thead><tr><th scope="col">名称</th><th scope="col">说明</th></tr></thead>',
            "",
        )
        errors = check_site.audit_table_semantics("features/x/index.html", page)
        self.assertTrue(any("without a header row" in e for e in errors), errors)

    def test_a_header_cell_without_scope_inside_a_wrapper_is_an_error(self):
        page = self.SCOPED.replace('<th scope="col">说明</th>', "<th>说明</th>")
        errors = check_site.audit_table_semantics("features/x/index.html", page)
        self.assertTrue(any('scope="col"' in e for e in errors), errors)

    def test_a_generated_page_must_wrap_a_wide_table(self):
        cells = "".join(f'<th scope="col">c{i}</th>' for i in range(5))
        page = f"""<!DOCTYPE html>
<html lang="zh">
<body><div id="rmc-main" tabindex="-1"><table>
<thead><tr>{cells}</tr></thead>
<tbody><tr><td>a</td></tr></tbody>
</table></div></body>
</html>
"""
        errors = check_site.audit_table_semantics("features/x/index.html", page)
        self.assertTrue(any("outside a scroll wrapper" in e for e in errors), errors)

    def test_a_generated_page_may_keep_a_narrow_table(self):
        page = self.SCOPED.replace('<div class="rmc-tablewrap">', "").replace(
            "</table></div>", "</table>"
        )
        self.assertEqual(
            check_site.audit_table_semantics("platform/x/index.html", page), []
        )

    def test_a_handwritten_page_may_keep_a_bare_table(self):
        cells = "".join(f'<th scope="col">c{i}</th>' for i in range(5))
        page = f"""<!DOCTYPE html>
<html lang="zh">
<body><div id="rmc-main" tabindex="-1"><table>
<thead><tr>{cells}</tr></thead>
<tbody><tr><td>a</td></tr></tbody>
</table></div></body>
</html>
"""
        self.assertEqual(
            check_site.audit_table_semantics("validation/index.html", page), []
        )


class AssetContractTests(unittest.TestCase):
    """The stylesheet and script that make the markup work in a browser."""

    def setUp(self):
        self.css = (ROOT / "docs/stylesheets/extra.css").read_text(encoding="utf-8")
        self.landing_css = (ROOT / "docs/stylesheets/landing.css").read_text(
            encoding="utf-8"
        )
        self.script = (ROOT / "docs/javascripts/site.js").read_text(encoding="utf-8")

    def test_the_wrapper_scrolls_and_wraps_long_words(self):
        block = self.css.split(".rmc-tablewrap {", 1)[1][:200]
        self.assertIn("overflow-x: auto;", block)
        narrow = self.css.split("@media screen and (max-width: 30em)", 1)[1]
        self.assertIn("overflow-wrap: anywhere;", narrow)
        self.assertIn("white-space: normal;", narrow)

    def test_the_script_makes_an_overflowing_table_keyboard_reachable(self):
        self.assertIn('wrap.setAttribute("tabindex", "0");', self.script)
        self.assertIn('wrap.setAttribute("role", "region");', self.script)
        self.assertIn("SCROLL_LABEL", self.script)

    def test_the_script_labels_a_stacked_cell_with_its_header(self):
        self.assertIn('cell.setAttribute("data-rmc-label"', self.script)
        self.assertIn('table.setAttribute("data-rmc-cols"', self.script)
        self.assertIn("data-rmc-stack", self.script)

    def test_the_wrapper_neutralises_the_theme_scroll_wrapper(self):
        self.assertIn(".rmc-tablewrap .md-typeset__scrollwrap {", self.css)
        self.assertIn(".rmc-tablewrap .md-typeset__table {", self.css)

    def test_the_script_does_not_wrap_a_table_twice(self):
        self.assertIn('table.closest(".rmc-tablewrap")', self.script)

    def test_the_script_resyncs_after_the_webfonts_load(self):
        self.assertIn("document.fonts", self.script)

    def test_the_script_makes_a_heading_focusable_for_the_theme_skip_link(self):
        self.assertIn('heading.setAttribute("tabindex", "-1")', self.script)

    def test_print_lets_a_table_wrap_instead_of_overflowing(self):
        printed = self.css.split("@media print", 1)[1]
        self.assertIn("white-space: normal;", printed)
        self.assertIn("overflow-wrap: anywhere;", printed)
        self.assertIn("overflow: visible;", printed)

    def test_print_lets_a_long_token_break_inside_a_cell(self):
        printed = self.css.split("@media print", 1)[1]
        block = printed.split(".md-typeset table:not([class]) code {", 1)[1][:120]
        self.assertIn("overflow-wrap: anywhere;", block)

    def test_print_lays_a_table_out_to_the_sheet(self):
        printed = self.css.split("@media print", 1)[1]
        self.assertIn("table-layout: fixed;", printed)
        self.assertIn('table[data-rmc-cols="5"] th:nth-child(5)', printed)
        self.assertIn('setAttribute("data-rmc-cols"', self.script)

    def test_print_collapses_the_landing_band_to_one_column(self):
        printed = self.landing_css.split("@media print", 1)[1]
        self.assertIn("grid-template-columns: minmax(0, 1fr);", printed)


class TemplateContractTests(unittest.TestCase):
    """The templates and generators that emit the markup in the first place."""

    def test_the_layout_adds_a_skip_link_where_the_theme_omits_one(self):
        layout = (ROOT / "docs/overrides/main.html").read_text(encoding="utf-8")
        self.assertIn("page.toc | first is not defined", layout)
        self.assertIn('class="md-skip" href="#rmc-main"', layout)

    def test_the_error_page_owns_the_skip_target(self):
        error = (ROOT / "docs/overrides/404.html").read_text(encoding="utf-8")
        self.assertIn('id="rmc-main"', error)
        self.assertIn('tabindex="-1"', error)

    def test_the_landing_pages_own_the_skip_target(self):
        for name in ("index.md", "index.en.md"):
            page = (ROOT / "docs" / name).read_text(encoding="utf-8")
            self.assertIn('id="rmc-main"', page, name)
            self.assertIn('tabindex="-1"', page, name)


class GeneratedTableTests(unittest.TestCase):
    """The generators scope their header cells and wrap their parameter tables."""

    def test_the_released_table_header_scopes_its_cells(self):
        labels = {
            "name": "Name",
            "required": "Required",
            "default": "Default",
            "type": "Type",
            "meaning": "Meaning",
        }
        heading = generate_features.table_heading(labels)
        self.assertEqual(heading[0].count("{scope=col}"), 5)

    def test_the_integration_table_header_scopes_its_cells(self):
        heading = platform_catalog.table_heading("en")
        self.assertEqual(heading[0].count("{scope=col}"), 5)

    def test_a_generated_page_wraps_its_parameter_table(self):
        labels = {
            "name": "Name",
            "required": "Required",
            "default": "Default",
            "type": "Type",
            "meaning": "Meaning",
        }
        lines = generate_features.parameter_table(labels, ["| a | b | c | d | e |"])
        self.assertEqual(lines[0], '<div class="rmc-tablewrap" markdown="1">')
        self.assertEqual(lines[-1], "</div>")

    def test_an_empty_parameter_list_says_so_without_a_wrapper(self):
        labels = {"no_specific": "This tool takes no parameters."}
        self.assertEqual(
            generate_features.parameter_table(labels, []),
            ["This tool takes no parameters."],
        )
