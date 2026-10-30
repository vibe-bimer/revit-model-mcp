"""Accessibility contracts for the built site: skip links, table semantics and scroll regions.

These tests pin the structural markup the reading and keyboard requirements depend on. They cover
three layers: the page-level checks check_site runs over every built page, the templates and
generators that emit that markup, and the stylesheet and script that finish the job in the browser.
"""

import unittest
from pathlib import Path

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
