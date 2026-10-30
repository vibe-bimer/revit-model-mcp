"""Tests for the deployment surface the site hooks write after a build.

The built site is a static tree, so the deployment-specific files cannot be
templates: ``robots.txt``, the root ``favicon.ico`` alias and the English
variant of the error page are all derived from the build configuration. These
tests pin the derivation rules without running mkdocs.
"""

import importlib.util
import re
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOOKS_PATH = ROOT / "docs" / "hooks.py"
FAVICON_SVG = ROOT / "docs" / "assets" / "favicon.svg"

_SPEC = importlib.util.spec_from_file_location("rmm_hooks", HOOKS_PATH)
hooks = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(hooks)


class RobotsPolicyTests(unittest.TestCase):
    """robots.txt follows the deployment origin; it never gates access."""

    def test_lan_origin_disallows_indexing(self):
        self.assertEqual(
            hooks.robots_txt("http://192.168.100.120:8099/"),
            "User-agent: *\nDisallow: /\n",
        )

    def test_public_origin_allows_indexing_and_names_its_sitemap(self):
        self.assertEqual(
            hooks.robots_txt("https://vibe-bimer.github.io/revit-model-mcp/"),
            "User-agent: *\nAllow: /\n"
            "Sitemap: https://vibe-bimer.github.io/revit-model-mcp/sitemap.xml\n",
        )

    def test_loopback_and_private_origins_are_not_indexed(self):
        for origin in (
            "http://127.0.0.1:8099/",
            "http://localhost:8099/",
            "http://[::1]:8099/",
            "http://10.0.0.5/",
            "http://172.20.1.1:8099/",
            "http://192.168.0.1/",
        ):
            with self.subTest(origin=origin):
                self.assertEqual(
                    hooks.robots_txt(origin), "User-agent: *\nDisallow: /\n"
                )

    def test_private_origin_names_no_sitemap(self):
        self.assertNotIn("Sitemap:", hooks.robots_txt("http://192.168.100.120:8099/"))

    def test_public_origin_without_trailing_slash_still_names_one_sitemap(self):
        self.assertEqual(
            hooks.robots_txt("https://example.com/docs"),
            "User-agent: *\nAllow: /\nSitemap: https://example.com/docs/sitemap.xml\n",
        )

    def test_an_empty_site_url_is_not_indexed(self):
        self.assertEqual(hooks.robots_txt(""), "User-agent: *\nDisallow: /\n")

    def test_the_file_is_plain_lf_ascii_with_one_trailing_newline(self):
        text = hooks.robots_txt("https://example.com/")
        self.assertNotIn("\r", text)
        self.assertTrue(text.isascii())
        self.assertTrue(text.endswith("\n"))
        self.assertFalse(text.endswith("\n\n"))


class FaviconIcoTests(unittest.TestCase):
    """The root alias is a real icon, derived from the shipped SVG mark."""

    def setUp(self):
        self.svg = FAVICON_SVG.read_text(encoding="utf-8")

    def test_every_polygon_in_the_source_svg_is_read(self):
        polygons = hooks.svg_polygons(self.svg)
        self.assertEqual(len(polygons), 9)
        self.assertEqual(len(polygons[0][0]), 4)
        self.assertEqual(polygons[0][1], (0x00, 0x5F, 0xB8))

    def test_rasterization_paints_the_mark_and_leaves_the_corner_clear(self):
        pixels = hooks.rasterize(hooks.svg_polygons(self.svg), 32)
        self.assertEqual(len(pixels), 32)
        self.assertEqual(pixels[0][0][3], 0)
        # The top plate's face covers the upper middle of the 64-unit viewBox; the centre of the
        # raster falls on the side face the next plate paints over it. Both were checked against
        # rsvg-convert at 32 px: every pure-colour pixel matches.
        self.assertEqual(pixels[8][8], (0x00, 0x5F, 0xB8, 0xFF))
        self.assertEqual(pixels[16][16], (0x00, 0x3C, 0x78, 0xFF))

    def test_the_icon_names_two_sizes_with_png_payloads(self):
        data = hooks.favicon_ico(self.svg)
        self.assertEqual(data[:4], b"\x00\x00\x01\x00")
        count = int.from_bytes(data[4:6], "little")
        self.assertEqual(count, 2)
        sizes = set()
        for index in range(count):
            entry = data[6 + 16 * index : 6 + 16 * (index + 1)]
            width = entry[0] or 256
            length = int.from_bytes(entry[8:12], "little")
            offset = int.from_bytes(entry[12:16], "little")
            sizes.add(width)
            self.assertEqual(data[offset : offset + 8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual(len(data[offset : offset + length]), length)
        self.assertEqual(sizes, {16, 32})

    def test_the_icon_is_deterministic(self):
        self.assertEqual(hooks.favicon_ico(self.svg), hooks.favicon_ico(self.svg))


class ErrorPageVariantTests(unittest.TestCase):
    """The English variant swaps the two marked language groups."""

    HTML = (
        "<html><body>"
        "<!--rmc:404:zh--><nav>中文入口</nav><!--/rmc:404:zh-->"
        "<!--rmc:404:en--><nav>English entries</nav><!--/rmc:404:en-->"
        "</body></html>"
    )

    def test_english_variant_puts_the_english_group_first(self):
        text = hooks.english_error_variant(self.HTML)
        self.assertLess(text.index("English entries"), text.index("中文入口"))

    def test_english_variant_is_idempotent(self):
        once = hooks.english_error_variant(self.HTML)
        self.assertEqual(hooks.english_error_variant(once), once)

    def test_html_without_markers_is_returned_unchanged(self):
        plain = "<html><body>no groups here</body></html>"
        self.assertEqual(hooks.english_error_variant(plain), plain)


class DeploymentFilesTests(unittest.TestCase):
    """One call writes every file the static tree cannot template."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name)
        (self.site / "en").mkdir()
        (self.site / "404.html").write_text(
            ErrorPageVariantTests.HTML, encoding="utf-8"
        )
        hooks._ERROR_RENDERS.clear()
        self.addCleanup(hooks._ERROR_RENDERS.clear)

    def test_writes_robots_for_the_configured_origin(self):
        hooks.write_deployment_files(self.site, "http://192.168.100.120:8099/")
        self.assertEqual(
            (self.site / "robots.txt").read_text(encoding="utf-8"),
            "User-agent: *\nDisallow: /\n",
        )

    def test_writes_the_root_and_asset_favicon_alias(self):
        hooks.write_deployment_files(self.site, "https://example.com/")
        expected = hooks.favicon_ico(FAVICON_SVG.read_text(encoding="utf-8"))
        self.assertEqual((self.site / "favicon.ico").read_bytes(), expected)
        self.assertEqual((self.site / "assets" / "favicon.ico").read_bytes(), expected)

    def test_each_language_pass_renders_its_own_page(self):
        # Each pass overwrites the same file, so both renders are captured instead.
        hooks.remember_error_page(self.site, "zh")
        (self.site / "404.html").write_text(
            hooks.english_error_variant(ErrorPageVariantTests.HTML), encoding="utf-8"
        )
        hooks.remember_error_page(self.site, "en")
        written = hooks.write_error_pages(self.site, "zh")
        self.assertEqual(sorted(written), ["404.html", "en/404.html"])
        english = (self.site / "en" / "404.html").read_text(encoding="utf-8")
        self.assertLess(english.index("English entries"), english.index("中文入口"))
        chinese = (self.site / "404.html").read_text(encoding="utf-8")
        self.assertLess(chinese.index("中文入口"), chinese.index("English entries"))

    def test_the_primary_language_wins_regardless_of_render_order(self):
        hooks.remember_error_page(self.site, "en")
        (self.site / "404.html").write_text(
            ErrorPageVariantTests.HTML, encoding="utf-8"
        )
        hooks.remember_error_page(self.site, "zh")
        hooks.write_error_pages(self.site, "zh")
        chinese = (self.site / "404.html").read_text(encoding="utf-8")
        self.assertLess(chinese.index("中文入口"), chinese.index("English entries"))

    def test_shipped_error_pages_carry_no_build_markers(self):
        hooks.remember_error_page(self.site, "zh")
        (self.site / "404.html").write_text(
            hooks.english_error_variant(ErrorPageVariantTests.HTML), encoding="utf-8"
        )
        hooks.remember_error_page(self.site, "en")
        hooks.write_error_pages(self.site, "zh")
        for name in ("404.html", "en/404.html"):
            with self.subTest(name=name):
                text = (self.site / name).read_text(encoding="utf-8")
                self.assertNotIn("rmc:404", text)

    def test_missing_error_page_is_reported_not_crashed(self):
        (self.site / "404.html").unlink()
        self.assertEqual(hooks.write_error_pages(self.site, "zh"), [])

    def test_a_single_language_build_ships_the_rendered_copy(self):
        written = hooks.write_error_pages(self.site, "zh")
        self.assertEqual(written, ["404.html"])
        self.assertNotIn(
            "rmc:404", (self.site / "404.html").read_text(encoding="utf-8")
        )


class _Extra(dict):
    """Stand-in for mkdocs' LegacyConfig: a dict that also carries instance attributes."""


class _I18n:
    def __init__(self):
        self.config = {
            "languages": [
                {"locale": "zh", "default": True},
                {"locale": "en", "default": False},
            ]
        }


class _Plugins:
    def get(self, name):
        return _I18n() if name == "i18n" else None


class ErrorPageContextTests(unittest.TestCase):
    """The error page's switcher points at the language home pages, not a tool page."""

    class Config:
        site_url = "https://example.com/revit-model-mcp/"

        def __init__(self):
            self.extra = _Extra({"alternate": []})
            self.plugins = _Plugins()

    def test_entries_become_the_language_home_pages(self):
        config = self.Config()
        stale = [
            {"lang": "zh", "link": "platform/revit_walls_from_cad/"},
            {"lang": "en", "link": "en/platform/revit_walls_from_cad/"},
        ]
        config.extra["alternate"] = stale
        config.extra.alternate = stale
        hooks.on_template_context({}, "404.html", config)
        homes = {entry["lang"]: entry["link"] for entry in config.extra["alternate"]}
        self.assertEqual(
            homes, {"zh": "/revit-model-mcp/", "en": "/revit-model-mcp/en/"}
        )
        # Jinja reads the attribute before the key, so both must carry the same pages.
        self.assertEqual(config.extra.alternate, config.extra["alternate"])

    def test_other_templates_are_untouched(self):
        config = self.Config()
        stale = [{"lang": "zh", "link": "features/"}]
        config.extra["alternate"] = stale
        hooks.on_template_context({}, "main.html", config)
        self.assertEqual(config.extra["alternate"], stale)

    def test_primary_language_reads_the_i18n_configuration(self):
        self.assertEqual(hooks.primary_language(self.Config()), "zh")


class SourceReferenceTests(unittest.TestCase):
    """The screenshots the build excludes are exactly the unreferenced ones."""

    def test_the_unreferenced_gif_is_the_only_excluded_screenshot(self):
        import yaml

        config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
        patterns = [
            line.strip()
            for line in str(config.get("exclude_docs", "")).splitlines()
            if line.strip()
        ]
        excluded = {p for p in patterns if p.startswith("screenshots/")}
        self.assertEqual(excluded, {"screenshots/revit-model-mcp_claude-desktop.gif"})

    def test_docs_sources_reference_every_other_screenshot(self):
        referenced = set()
        for source in list((ROOT / "docs").rglob("*.md")) + [
            ROOT / "tools" / "site" / "landing.py"
        ]:
            text = source.read_text(encoding="utf-8")
            referenced.update(re.findall(r"screenshots/[\w.-]+", text))
        on_disk = {
            f"screenshots/{p.name}" for p in (ROOT / "docs/screenshots").iterdir()
        }
        self.assertEqual(
            on_disk - referenced, {"screenshots/revit-model-mcp_claude-desktop.gif"}
        )
        self.assertIn("screenshots/revit-model-mcp_export-view_dark.png", referenced)
        self.assertIn("screenshots/revit-model-mcp_export-view_light.png", referenced)


if __name__ == "__main__":
    unittest.main()


class DirectorySitemapTests(unittest.TestCase):
    """Every page directory gets a sitemap, including under a deployment path."""

    SITEMAP = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        "<url><loc>{base}features/</loc></url>"
        "<url><loc>{base}features/revit_ping/</loc></url>"
        "<url><loc>{base}</loc></url>"
        "</urlset>"
    )

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name)
        for directory in ("features", "features/revit_ping"):
            target = self.site / directory
            target.mkdir(parents=True)
            (target / "index.html").write_text("<html></html>", encoding="utf-8")

    def _sitemap(self, base):
        (self.site / "sitemap.xml").write_text(
            self.SITEMAP.format(base=base), encoding="utf-8"
        )

    def test_locations_under_a_deployment_path_resolve_against_the_tree(self):
        self._sitemap("https://example.com/revit-model-mcp/")
        written = hooks._write_directory_sitemaps(
            self.site, "https://example.com/revit-model-mcp/"
        )
        self.assertEqual(written, 2)
        self.assertTrue((self.site / "features" / "sitemap.xml").is_file())
        self.assertTrue(
            (self.site / "features" / "revit_ping" / "sitemap.xml").is_file()
        )
        self.assertFalse((self.site / "revit-model-mcp").exists())

    def test_root_locations_still_work_without_a_deployment_path(self):
        self._sitemap("http://192.168.100.120:8099/")
        written = hooks._write_directory_sitemaps(
            self.site, "http://192.168.100.120:8099/"
        )
        self.assertEqual(written, 2)
        self.assertTrue((self.site / "features" / "sitemap.xml").is_file())

    def test_the_written_sitemap_lists_only_its_own_directory(self):
        self._sitemap("https://example.com/revit-model-mcp/")
        hooks._write_directory_sitemaps(
            self.site, "https://example.com/revit-model-mcp/"
        )
        text = (self.site / "features" / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn("features/</loc>", text)
        self.assertNotIn("revit_ping", text)
