"""Tests for the declaration-driven checks in check_site: twin contract hints and coverage."""

import tempfile
import unittest
from pathlib import Path

import catalogs
import check_site


def _schema(properties, required=None):
    return {
        "properties": properties,
        "required": required or [],
        "type": "object",
    }


class TwinHintTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        content = self.root / "tools/site/content"
        content.mkdir(parents=True)
        self.content = content

    def _write(self, name, payload):
        (self.content / name).write_text(payload, encoding="utf-8")

    def _manifest(self):
        data = {
            "release": {
                "directory": "features",
                "status": "released",
                "branch": "main",
                "languages": ("zh", "en"),
                "page_languages": {},
                "version": {
                    "file": "server/pyproject.toml",
                    "format": "toml",
                    "pointer": "project.version",
                },
            },
            "integration": {
                "directory": "platform",
                "status": "unreleased",
                "branch": "integration/upstream-1.0",
                "languages": ("zh", "en"),
                "page_languages": {},
                "provenance": {"file": "tools/site/content/platform-tools.json"},
            },
        }
        (self.content / "catalogs.yaml").write_text(
            catalogs.dump_yaml(data), encoding="utf-8"
        )

    def _pages(self, marker_on=(), omit=()):
        for directory in ("features", "platform"):
            target = self.root / "docs" / directory
            target.mkdir(parents=True, exist_ok=True)
            if directory in omit:
                continue
            marker = "{#contract-diff}" if directory in marker_on else ""
            (target / "widget.md").write_text(
                f"# Widget\n\n{marker}\n", encoding="utf-8"
            )

    def _write_pair(self, release_schema, integration_schema):
        import json

        self._write(
            "tools.json",
            json.dumps([{"name": "widget", "inputSchema": release_schema}]),
        )
        self._write(
            "platform-tools.json",
            json.dumps(
                {
                    "count": 1,
                    "provenance": {"branch": "integration/upstream-1.0"},
                    "tools": [{"name": "widget", "inputSchema": integration_schema}],
                }
            ),
        )

    def test_differing_pair_without_hint_is_an_error(self):
        self._manifest()
        self._write_pair(
            _schema({"save_to": {"type": "string"}}, ["save_to"]),
            _schema({"output_path": {"type": "string"}}, ["output_path"]),
        )
        self._pages()
        errors = check_site.audit_twin_hints(self.root)
        self.assertEqual(len(errors), 2)
        self.assertTrue(all("missing contract-diff hint" in e for e in errors))

    def test_differing_pair_with_hint_passes(self):
        self._manifest()
        self._write_pair(
            _schema({"save_to": {"type": "string"}}, ["save_to"]),
            _schema({"output_path": {"type": "string"}}, ["output_path"]),
        )
        self._pages(marker_on=("features", "platform"))
        self.assertEqual(check_site.audit_twin_hints(self.root), [])

    def test_identical_pair_needs_no_hint(self):
        self._manifest()
        same = _schema({"view": {"type": "string"}}, ["view"])
        self._write_pair(same, same)
        self._pages()
        self.assertEqual(check_site.audit_twin_hints(self.root), [])

    def test_missing_twin_page_is_an_error(self):
        self._manifest()
        self._write_pair(
            _schema({"save_to": {"type": "string"}}, ["save_to"]),
            _schema({"output_path": {"type": "string"}}, ["output_path"]),
        )
        self._pages(marker_on=("features",), omit=("platform",))
        errors = check_site.audit_twin_hints(self.root)
        self.assertTrue(any("Twin page missing" in e for e in errors))

    def test_absent_content_returns_no_errors(self):
        self._manifest()
        self.assertEqual(check_site.audit_twin_hints(self.root), [])


class CoverageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def _manifest(self, release_langs, page_languages=None):
        data = {
            "release": {
                "directory": "features",
                "status": "released",
                "branch": "main",
                "languages": tuple(release_langs),
                "page_languages": page_languages or {},
                "version": {
                    "file": "server/pyproject.toml",
                    "format": "toml",
                    "pointer": "project.version",
                },
            },
            "integration": {
                "directory": "platform",
                "status": "unreleased",
                "branch": "integration/upstream-1.0",
                "languages": ("zh", "en"),
                "page_languages": {},
                "provenance": {"file": "tools/site/content/platform-tools.json"},
            },
        }
        content = self.root / "tools/site/content"
        content.mkdir(parents=True)
        (content / "catalogs.yaml").write_text(
            catalogs.dump_yaml(data), encoding="utf-8"
        )

    def _page(self, relative, text):
        path = self.root / "docs" / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_missing_promised_translation_fails(self):
        self._manifest(("zh", "en"))
        self._page("features/widget.md", "# 中文\n")
        errors = catalogs.coverage_errors(self.root)
        self.assertTrue(any("promised en translation missing" in e for e in errors))

    def test_explicit_monolingual_inherited_passes(self):
        self._manifest(("zh", "en"), page_languages={"widget": ("en",)})
        self._page("features/widget.en.md", "# English\n")
        self.assertEqual(catalogs.coverage_errors(self.root), [])

    def test_declared_language_present_passes(self):
        self._manifest(("zh", "en"))
        self._page("features/widget.md", "# 中文\n")
        self._page("features/widget.en.md", "# English\n")
        self.assertEqual(catalogs.coverage_errors(self.root), [])


class NoHardcodedCountsTests(unittest.TestCase):
    def _source(self, name):
        return (Path(check_site.__file__).parent / name).read_text(encoding="utf-8")

    def test_generators_have_no_literal_tool_counts_or_version(self):
        for name in ("generate_features.py", "platform_catalog.py", "landing.py"):
            source = self._source(name)
            self.assertNotIn("35 个工具", source, name)
            self.assertNotIn("80 个工具", source, name)
            self.assertNotIn("35 tools", source, name)
            self.assertNotIn("80 tools", source, name)
            self.assertNotIn("0.9.0", source, name)

    def test_counts_come_from_the_registry(self):
        source = self._source("generate_features.py")
        self.assertIn("branch_count", source)
        self.assertIn("len(tools)", source)


if __name__ == "__main__":
    unittest.main()


class TerminologyTests(unittest.TestCase):
    """Chinese prose keeps one word per concept; UI literals and code stay untouched."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "docs").mkdir()

    def page(self, name, text):
        path = self.root / "docs" / name
        path.write_text(text, encoding="utf-8")
        return path

    def test_element_written_as_yuansu_is_an_error(self):
        self.page("probe.md", "读取选中元素的参数。\n")
        errors = check_site.audit_terminology(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("元素", errors[0])
        self.assertIn("构件", errors[0])
        self.assertIn("docs/probe.md", errors[0])

    def test_the_agreed_word_passes(self):
        self.page("probe.md", "读取选中构件的参数。\n")
        self.assertEqual(check_site.audit_terminology(self.root), [])

    def test_a_fenced_code_block_is_not_prose(self):
        self.page("probe.md", "说明：\n\n```text\n元素\n```\n")
        self.assertEqual(check_site.audit_terminology(self.root), [])

    def test_an_inline_code_span_is_not_prose(self):
        self.page("probe.md", "界面值 `元素` 保持原样。\n")
        self.assertEqual(check_site.audit_terminology(self.root), [])

    def test_a_whitelisted_literal_passes(self):
        self.page("probe.md", "界面写作 元素。\n")
        self.assertEqual(
            check_site.audit_terminology(self.root, whitelist={"probe.md": {"元素"}}),
            [],
        )

    def test_the_write_gate_named_as_a_switch_is_an_error(self):
        self.page("gates.md", "写入开关打开后才允许修改模型。\n")
        errors = check_site.audit_terminology(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("门禁", errors[0])

    def test_toggling_display_keeps_the_verb(self):
        self.page("views.md", "开关阴影显示即可。\n")
        self.assertEqual(check_site.audit_terminology(self.root), [])

    def test_english_pages_are_not_checked(self):
        self.page("probe.en.md", "Read the parameters of the selected elements.\n")
        self.assertEqual(check_site.audit_terminology(self.root), [])

    def test_the_repository_prose_agrees(self):
        root = Path(__file__).resolve().parents[2]
        self.assertEqual(check_site.audit_terminology(root), [])


class ShippedAssetTests(unittest.TestCase):
    """A shipped file is referenced, conventional, or an error naming the file."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name)

    def _write(self, name, payload, encoding="utf-8"):
        target = self.site / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(payload, bytes):
            target.write_bytes(payload)
        else:
            target.write_text(payload, encoding=encoding)

    def _conventional(self):
        self._write("404.html", "<html></html>")
        self._write("en/404.html", "<html></html>")
        self._write("robots.txt", "User-agent: *\nDisallow: /\n")
        self._write("favicon.ico", b"\x00\x00\x01\x00")
        self._write("sitemap.xml", "<urlset></urlset>")
        self._write("features/sitemap.xml", "<urlset></urlset>")
        self._write("search/search_index.json", "{}")
        self._write("assets/javascripts/lunr/min/lunr.zh.min.js", "x")
        self._write("overrides/404.html", "<html></html>")

    def test_a_referenced_image_passes(self):
        self._conventional()
        self._write("index.html", '<html><img src="assets/mark.png"></html>')
        self._write("assets/mark.png", b"png")
        errors, stats = check_site.audit_assets(self.site)
        self.assertEqual(errors, [])
        self.assertEqual(stats["files"], 10)
        self.assertEqual(stats["referenced"], 1)

    def test_an_unreferenced_asset_is_named(self):
        self._conventional()
        self._write("index.html", "<html></html>")
        self._write("screenshots/unused.gif", b"gif")
        errors, _ = check_site.audit_assets(self.site)
        self.assertEqual(len(errors), 1)
        self.assertIn("screenshots/unused.gif", errors[0])

    def test_social_metadata_counts_as_a_reference(self):
        self._conventional()
        self._write(
            "index.html",
            '<html><meta property="og:image" content="https://example.com/assets/card.png"></html>',
        )
        self._write("assets/card.png", b"png")
        errors, _ = check_site.audit_assets(self.site)
        self.assertEqual(errors, [])

    def test_a_stylesheet_reference_counts(self):
        self._conventional()
        self._write(
            "index.html", '<html><link rel="stylesheet" href="assets/site.css"></html>'
        )
        self._write("assets/site.css", "body{background:url(../assets/bg.png)}")
        self._write("assets/bg.png", b"png")
        errors, _ = check_site.audit_assets(self.site)
        self.assertEqual(errors, [])

    def test_a_srcset_reference_counts(self):
        self._conventional()
        self._write(
            "index.html",
            '<html><img src="a.png" srcset="a.png 1x, assets/b.png 2x"></html>',
        )
        self._write("a.png", b"png")
        self._write("assets/b.png", b"png")
        errors, _ = check_site.audit_assets(self.site)
        self.assertEqual(errors, [])

    def test_a_deployment_base_path_is_tolerated(self):
        self._conventional()
        self._write(
            "index.html",
            '<html><img src="https://example.com/revit-model-mcp/assets/mark.png"></html>',
        )
        self._write("assets/mark.png", b"png")
        errors, _ = check_site.audit_assets(self.site)
        self.assertEqual(errors, [])

    def test_theme_files_shipped_for_their_own_reason_pass(self):
        self._conventional()
        self._write("index.html", "<html></html>")
        self._write("assets/logo-white.svg", "<svg></svg>")
        errors, _ = check_site.audit_assets(self.site)
        self.assertEqual(errors, [])


class DeploymentFileTests(unittest.TestCase):
    """robots.txt, the favicon alias and the two error pages are part of every build."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name)

    def _write(self, name, payload):
        target = self.site / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(payload, encoding="utf-8")

    def _complete(self, robots):
        self._write("robots.txt", robots)
        self._write("favicon.ico", "")
        self._write("404.html", "<html></html>")
        self._write("en/404.html", "<html></html>")

    def test_a_private_origin_must_not_name_a_sitemap(self):
        self._complete("User-agent: *\nDisallow: /\n")
        self.assertEqual(check_site.audit_deployment(self.site), [])

    def test_a_public_origin_must_name_its_sitemap(self):
        self._complete(
            "User-agent: *\nAllow: /\nSitemap: https://example.com/sitemap.xml\n"
        )
        self.assertEqual(check_site.audit_deployment(self.site), [])

    def test_a_public_origin_without_a_sitemap_is_an_error(self):
        self._complete("User-agent: *\nAllow: /\n")
        errors = check_site.audit_deployment(self.site)
        self.assertEqual(len(errors), 1)
        self.assertIn("names no sitemap", errors[0])

    def test_a_private_origin_naming_a_sitemap_is_an_error(self):
        self._complete(
            "User-agent: *\nDisallow: /\nSitemap: https://example.com/sitemap.xml\n"
        )
        errors = check_site.audit_deployment(self.site)
        self.assertEqual(len(errors), 1)
        self.assertIn("still names a sitemap", errors[0])

    def test_missing_deployment_files_are_named(self):
        errors = check_site.audit_deployment(self.site)
        self.assertEqual(len(errors), 4)
        self.assertIn("robots.txt: missing from the build", errors[0])
