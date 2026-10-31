"""Tests for the declarative catalog manifest: versions, status, provenance, ownership, languages.

The manifest is the single place that knows which catalog is released, which one is the
integration branch, where the release version lives and which pages are promised in which
languages. The generators and the site checker only consume it, so a drift here is a quiet
wrong page, which is exactly what these tests guard.
"""

import json
import tempfile
import unittest
from pathlib import Path

import catalogs
import tomllib

REAL_ROOT = Path(__file__).resolve().parents[2]


class ReleaseVersionTests(unittest.TestCase):
    def test_release_version_is_read_from_project_metadata(self):
        expected = tomllib.loads(
            (REAL_ROOT / "server/pyproject.toml").read_text(encoding="utf-8")
        )["project"]["version"]
        self.assertEqual(catalogs.release().version, expected)

    def test_the_version_is_not_a_literal_in_the_module(self):
        source = (REAL_ROOT / "tools/site/catalogs.py").read_text(encoding="utf-8")
        version = catalogs.release().version
        self.assertNotIn(f'"{version}"', source)
        self.assertNotIn(f"'{version}'", source)


class IntegrationCatalogTests(unittest.TestCase):
    def test_integration_declares_the_unreleased_branch_and_its_sha(self):
        integration = catalogs.integration()
        self.assertEqual(integration.status, "unreleased")
        self.assertEqual(integration.branch, "integration/upstream-1.0")
        self.assertEqual(integration.languages, ("zh", "en"))

    def test_the_declared_branch_matches_the_snapshot_provenance(self):
        provenance = json.loads(
            (REAL_ROOT / "tools/site/content/platform-tools.json").read_text(
                encoding="utf-8"
            )
        )["provenance"]
        self.assertEqual(catalogs.integration().branch, provenance["branch"])
        catalogs.audit(REAL_ROOT)  # must not raise

    def test_the_release_catalog_is_marked_released_on_main(self):
        release = catalogs.release()
        self.assertEqual(release.status, "released")
        self.assertEqual(release.branch, "main")
        self.assertEqual(release.directory, "features")
        self.assertEqual(catalogs.integration().directory, "platform")


class ForkOwnershipTests(unittest.TestCase):
    def test_fork_tools_are_declared_with_status_and_both_languages(self):
        tools = catalogs.fork_tools()
        self.assertEqual(len(tools), 8)
        for name, item in tools.items():
            for field in ("status", "zh", "en", "zh_note", "en_note"):
                self.assertTrue(item.get(field), f"{name} is missing {field}")
        grafted = [n for n, i in tools.items() if i["status"] == "grafted"]
        self.assertEqual(grafted, ["revit_set_view_lighting"])


class AuditTests(unittest.TestCase):
    def _root(self, branch="integration/upstream-1.0", commit="a" * 40):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        content = root / "tools/site/content"
        content.mkdir(parents=True)
        (root / "server").mkdir()
        (root / "server/pyproject.toml").write_text(
            '[project]\nname = "x"\nversion = "1.2.3"\n', encoding="utf-8"
        )
        data = catalogs.load(REAL_ROOT)  # start from the real declaration
        data["integration"]["branch"] = branch
        (content / "catalogs.yaml").write_text(
            catalogs.dump_yaml(data), encoding="utf-8"
        )
        (content / "platform-tools.json").write_text(
            json.dumps(
                {
                    "count": 0,
                    "provenance": {"branch": branch, "commit": commit},
                    "tools": [],
                }
            ),
            encoding="utf-8",
        )
        return root

    def test_audit_rejects_a_branch_mismatch(self):
        root = self._root(branch="integration/other")
        # rewrite provenance to a different branch than the declaration
        (root / "tools/site/content/platform-tools.json").write_text(
            json.dumps(
                {
                    "count": 0,
                    "provenance": {"branch": "integration/other", "commit": "a" * 40},
                    "tools": [],
                }
            ),
            encoding="utf-8",
        )
        data = catalogs.load(root)
        data["integration"]["branch"] = "integration/upstream-1.0"
        (root / "tools/site/content/catalogs.yaml").write_text(
            catalogs.dump_yaml(data), encoding="utf-8"
        )
        with self.assertRaises(SystemExit):
            catalogs.audit(root)

    def test_audit_rejects_a_short_commit(self):
        root = self._root(commit="abc123")
        with self.assertRaises(SystemExit):
            catalogs.audit(root)


class LanguageCoverageTests(unittest.TestCase):
    def _root(self, integration_pages):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        content = root / "tools/site/content"
        content.mkdir(parents=True)
        data = {
            "release": {
                "directory": "features",
                "status": "released",
                "branch": "main",
                "languages": ["zh", "en"],
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
                "languages": ["zh", "en"],
                "page_languages": integration_pages,
                "provenance": {"file": "tools/site/content/platform-tools.json"},
            },
            "fork_tools": {},
        }
        (content / "catalogs.yaml").write_text(
            catalogs.dump_yaml(data), encoding="utf-8"
        )
        (root / "docs/features").mkdir(parents=True)
        (root / "docs/platform").mkdir(parents=True)
        return root

    def test_a_promised_translation_that_is_missing_fails(self):
        root = self._root(integration_pages={})
        (root / "docs/platform/foo.md").write_text("# 中文\n", encoding="utf-8")
        errors = catalogs.coverage_errors(root)
        self.assertTrue(any("promised en translation" in e for e in errors), errors)

    def test_an_explicitly_monolingual_inherited_page_passes(self):
        root = self._root(integration_pages={"foo": ["en"]})
        (root / "docs/platform/foo.en.md").write_text("# English\n", encoding="utf-8")
        self.assertEqual(catalogs.coverage_errors(root), [])

    def test_a_translation_beyond_the_declaration_fails(self):
        root = self._root(integration_pages={"foo": ["en"]})
        (root / "docs/platform/foo.en.md").write_text("# English\n", encoding="utf-8")
        (root / "docs/platform/foo.md").write_text("# 中文\n", encoding="utf-8")
        errors = catalogs.coverage_errors(root)
        self.assertTrue(any("undeclared zh" in e for e in errors), errors)

    def test_the_real_repository_declares_what_it_ships(self):
        self.assertEqual(catalogs.coverage_errors(REAL_ROOT), [])


if __name__ == "__main__":
    unittest.main()
