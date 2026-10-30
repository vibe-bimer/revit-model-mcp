"""Tests for the metadata, canonical, locale, hreflang and edit-source audit.

Every generated or hand-written page must ship a same-language description, a
correct ``og:locale``, absolute canonical/``og:url``/``hreflang`` URLs, and an
edit link that points at the real maintenance source rather than a build
artifact.
"""

import tempfile
import unittest
from pathlib import Path

import check_site

BASE = "https://docs.example/"
REPO = "https://github.com/vibe-bimer/revit-model-mcp"


def default_edit(relative):
    rel = relative.removeprefix("en/")
    if rel == "index.html":
        return f"{REPO}/blob/main/tools/site/landing.py"
    if rel.startswith("features/"):
        return f"{REPO}/blob/main/tools/site/generate_features.py"
    if rel.startswith("platform/"):
        return f"{REPO}/blob/main/tools/site/platform_catalog.py"
    return f"{REPO}/edit/main/docs/{rel.removesuffix('index.html')}index.md"


class MetadataAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name)
        self.root = None
        (self.site / "404.html").write_text(
            '<html lang="zh"><body><a class="md-skip" href="#rmc-main">跳转至内容</a>'
            '<div id="rmc-main" tabindex="-1">页面不存在</div></body></html>',
            encoding="utf-8",
        )

    def page(
        self,
        relative,
        lang,
        *,
        description=None,
        og_locale=None,
        canonical=None,
        og_url=None,
        alternates="default",
        edit=None,
        text=None,
    ):
        sibling = relative.removeprefix("en/").removesuffix("index.html")
        origin = BASE + relative.removesuffix("index.html")
        desc = (
            description
            if description is not None
            else (
                "中文摘要描述与用途说明。"
                if lang == "zh"
                else "English summary description."
            )
        )
        default_locale = "zh_CN" if lang == "zh" else "en_US"
        if og_locale is None:
            og_locale = default_locale
        if canonical is None:
            canonical = origin
        if og_url is None:
            og_url = origin
        if alternates == "default":
            alternates = {"zh": BASE + sibling, "en": BASE + "en/" + sibling}
        if edit is None:
            edit = default_edit(relative)
        links = "".join(
            f'<link rel="alternate" hreflang="{lang_code}" href="{href}">'
            for lang_code, href in alternates.items()
        )
        edit_html = f'<a rel="edit" href="{edit}">Edit</a>' if edit else ""
        skip = (
            '<a class="md-skip" href="#rmc-main">Skip to content</a>'
            if lang == "en"
            else '<a class="md-skip" href="#rmc-main">跳转至内容</a>'
        )
        body_text = text or (
            "完整的中文功能说明与参数使用指南。"
            if lang == "zh"
            else "Complete feature documentation and parameter guidance."
        )
        destination = self.site / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            f'<html lang="{lang}"><head>'
            f'<meta name="description" content="{desc}">'
            f'<meta property="og:locale" content="{og_locale}">'
            f'<meta property="og:url" content="{og_url}">'
            f'<meta property="og:description" content="{desc}">'
            f'<meta name="twitter:description" content="{desc}">'
            f'<link rel="canonical" href="{canonical}">'
            f"{links}</head>"
            f"{skip}"
            f'<body><article id="rmc-main" tabindex="-1"><h1 id="heading">{body_text}</h1></article>{edit_html}</body></html>',
            encoding="utf-8",
        )

    def home(self):
        self.page("index.html", "zh")
        self.page("en/index.html", "en")
        (self.site / "404.html").write_text(
            '<html lang="zh"><body><a class="md-skip" href="#rmc-main">跳转至内容</a>'
            '<div id="rmc-main" tabindex="-1">页面不存在</div></body></html>',
            encoding="utf-8",
        )

    def errors(self):
        return check_site.audit_site(self.site, root=self.root)[0]

    def test_valid_pair_passes(self):
        self.page("index.html", "zh")
        self.page("en/index.html", "en")
        self.assertEqual(self.errors(), [])

    def test_generated_page_with_absolute_urls_passes(self):
        self.home()
        self.page("features/revit_ping/index.html", "zh")
        self.page("en/features/revit_ping/index.html", "en")
        self.assertEqual(self.errors(), [])

    def test_missing_description_is_an_error(self):
        self.page("index.html", "zh", description="")
        self.assertTrue(any("description" in e for e in self.errors()))

    def test_english_description_with_chinese_is_an_error(self):
        self.page("index.html", "zh")
        self.page("en/index.html", "en", description="这段英文摘要其实是中文。")
        self.assertTrue(any("description" in e for e in self.errors()))

    def test_chinese_description_without_chinese_is_an_error(self):
        self.page("index.html", "zh", description="This is only English.")
        self.assertTrue(any("description" in e for e in self.errors()))

    def test_wrong_og_locale_is_an_error(self):
        self.page("index.html", "zh")
        self.page("en/index.html", "en", og_locale="zh_CN")
        self.assertTrue(any("og:locale" in e for e in self.errors()))

    def test_relative_hreflang_is_an_error(self):
        self.page("index.html", "zh", alternates={"zh": "/", "en": "/en/"})
        self.assertTrue(any("language-switch" in e for e in self.errors()))

    def test_monolingual_page_declaring_absent_language_is_an_error(self):
        self.home()
        self.page(
            "features/solo/index.html",
            "zh",
            alternates={
                "zh": BASE + "features/solo/",
                "en": BASE + "en/features/solo/",
            },
        )
        self.assertTrue(any("language-switch" in e for e in self.errors()))

    def test_monolingual_page_with_only_its_language_passes(self):
        self.home()
        self.page(
            "features/solo/index.html", "zh", alternates={"zh": BASE + "features/solo/"}
        )
        self.assertEqual(self.errors(), [])

    def test_canonical_must_be_absolute(self):
        self.page("index.html", "zh", canonical="/")
        self.assertTrue(any("canonical" in e for e in self.errors()))

    def test_canonical_must_match_build_base(self):
        self.page("index.html", "zh", canonical="https://elsewhere.example/")
        self.assertTrue(any("canonical" in e for e in self.errors()))

    def test_og_url_must_match_canonical(self):
        self.page("index.html", "zh", og_url="https://elsewhere.example/")
        self.assertTrue(any("og:url" in e for e in self.errors()))

    def test_feature_page_edit_must_point_to_generator(self):
        self.home()
        self.page(
            "features/revit_ping/index.html",
            "zh",
            edit=f"{REPO}/edit/main/docs/features/revit_ping.md",
        )
        self.assertTrue(
            any("edit" in e and "generate_features.py" in e for e in self.errors())
        )

    def test_feature_page_edit_to_generator_passes(self):
        self.home()
        self.page("features/revit_ping/index.html", "zh")
        self.page("en/features/revit_ping/index.html", "en")
        self.assertEqual(self.errors(), [])

    def test_home_edit_must_point_to_landing(self):
        self.page("index.html", "zh", edit=f"{REPO}/edit/main/README.md")
        self.assertTrue(any("edit" in e and "landing.py" in e for e in self.errors()))

    def test_home_edit_to_landing_passes(self):
        self.home()
        self.assertEqual(self.errors(), [])

    def test_handwritten_edit_target_must_exist(self):
        self.root = Path(self.temp.name) / "repo"
        (self.root / "docs").mkdir(parents=True)
        self.site = Path(self.temp.name) / "site"
        self.home()
        self.page(
            "guide/index.html",
            "zh",
            alternates={"zh": BASE + "guide/"},
            edit=f"{REPO}/edit/main/docs/guide.md",
        )
        self.assertTrue(any("does not exist" in e for e in self.errors()))
        (self.root / "docs/guide.md").write_text("# 指南\n", encoding="utf-8")
        self.assertEqual(self.errors(), [])


if __name__ == "__main__":
    unittest.main()
