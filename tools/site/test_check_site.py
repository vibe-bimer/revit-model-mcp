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
