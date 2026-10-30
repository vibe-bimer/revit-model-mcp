"""Tests for the dual-config gate: normalization and deterministic comparison."""

import gzip
import json
import tempfile
import unittest
from pathlib import Path

import verify_dual_build as gate

GH_BASE = "https://vibe-bimer.github.io/revit-model-mcp/"
LAN_BASE = "http://192.168.100.120:8099/"


class NormalizeTextTests(unittest.TestCase):
    def test_erases_absolute_base_url(self):
        text = f'canonical="{GH_BASE}features/x/"'
        self.assertIn(
            'canonical="<site-base>/features/x/"', gate.normalize_text(text, GH_BASE)
        )

    def test_erases_root_relative_prefix_in_attributes(self):
        html = '<a href="/revit-model-mcp/en/">en</a>'
        self.assertIn('<a href="/en/">', gate.normalize_text(html, GH_BASE))

    def test_prefix_strip_is_anchored_on_the_opening_quote(self):
        prose = "Open <code>http://127.0.0.1:8000/revit-model-mcp/</code>."
        self.assertEqual(prose, gate.normalize_text(prose, GH_BASE))

    def test_prefix_strip_keeps_github_repo_links_intact(self):
        repo = "https://github.com/vibe-bimer/revit-model-mcp/edit/main/docs/a.md"
        self.assertIn(repo, gate.normalize_text(f'href="{repo}"', GH_BASE))

    def test_prefix_strip_covers_single_quoted_attributes(self):
        html = "<script>scope('/revit-model-mcp/x/')</script>"
        self.assertIn("scope('/x/')", gate.normalize_text(html, GH_BASE))

    def test_root_relative_prefix_not_stripped_for_root_base(self):
        text = '<a href="/en/">en</a>'
        self.assertEqual(text, gate.normalize_text(text, LAN_BASE))


class NormalizeVolatileTests(unittest.TestCase):
    def test_manifest_timestamps_and_ids_are_blanked(self):
        manifest = json.dumps(
            {
                "built_utc": "2026-10-31T01:02:03Z",
                "release_id": "20261031-010203-ab12cd3",
                "tree_sha": "deadbeef",
                "source_commit": "d188736",
                "config": {"name": "mkdocs-lan.yml"},
                "verification": {"build": "pass", "unit_tests": "pass"},
            }
        )
        scrubbed = json.loads(gate.normalize_volatile(manifest))
        self.assertEqual(scrubbed["built_utc"], "<volatile>")
        self.assertEqual(scrubbed["release_id"], "<volatile>")
        self.assertEqual(scrubbed["tree_sha"], "<volatile>")
        self.assertEqual(scrubbed["source_commit"], "<volatile>")
        self.assertEqual(scrubbed["verification"], "<volatile-section>")
        self.assertEqual(scrubbed["config"]["name"], "mkdocs-lan.yml")

    def test_nested_volatile_fields_are_blanked(self):
        manifest = json.dumps({"a": {"b": [{"release_id": "x", "keep": 1}]}})
        scrubbed = json.loads(gate.normalize_volatile(manifest))
        self.assertEqual(scrubbed["a"]["b"][0]["release_id"], "<volatile>")
        self.assertEqual(scrubbed["a"]["b"][0]["keep"], 1)

    def test_plain_text_is_returned_unchanged(self):
        text = "<html>no json here</html>"
        self.assertEqual(text, gate.normalize_volatile(text))


class NormalizeBytesTests(unittest.TestCase):
    def test_gzip_stream_is_decompressed_and_normalized(self):
        payload = f"<loc>{GH_BASE}x/</loc>".encode()
        self.assertEqual(
            gate.normalize_bytes(gzip.compress(payload), GH_BASE),
            "<loc><site-base>/x/</loc>",
        )

    def test_binary_payload_is_returned_as_bytes(self):
        payload = b"\x89PNG\r\n\x1a\n\x00\xff\xfe"
        self.assertEqual(gate.normalize_bytes(payload, GH_BASE), payload)


class CompareRobotsTests(unittest.TestCase):
    def test_expected_pair_passes(self):
        gh = f"User-agent: *\nAllow: /\nSitemap: {GH_BASE}sitemap.xml\n"
        lan = "User-agent: *\nDisallow: /\n"
        self.assertEqual(gate.compare_robots(gh, lan, GH_BASE), [])

    def test_pages_build_without_sitemap_line_fails(self):
        gh = "User-agent: *\nAllow: /\n"
        lan = "User-agent: *\nDisallow: /\n"
        problems = gate.compare_robots(gh, lan, GH_BASE)
        self.assertEqual(len(problems), 1)
        self.assertIn("pages sitemap", problems[0])

    def test_lan_build_allowing_crawl_fails(self):
        gh = f"User-agent: *\nAllow: /\nSitemap: {GH_BASE}sitemap.xml\n"
        problems = gate.compare_robots(gh, "User-agent: *\nAllow: /\n", GH_BASE)
        self.assertEqual(len(problems), 1)
        self.assertIn("lan build", problems[0])


class CompareSitesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.gh = self.root / "gh"
        self.lan = self.root / "lan"

    def _mirror(self, rel: str, gh_text: str, lan_text: str):
        for base, text in ((self.gh, gh_text), (self.lan, lan_text)):
            target = base / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")

    def test_equivalent_trees_pass(self):
        self._mirror(
            "features/x/index.html",
            f'<a href="{GH_BASE}features/y/">y</a>',
            '<a href="http://192.168.100.120:8099/features/y/">y</a>',
        )
        self._mirror(
            "robots.txt",
            f"User-agent: *\nAllow: /\nSitemap: {GH_BASE}sitemap.xml\n",
            "User-agent: *\nDisallow: /\n",
        )
        self._mirror(
            "sitemap.xml.gz",
            "",
            "",
        )
        (self.gh / "sitemap.xml.gz").write_bytes(
            gzip.compress(f"<loc>{GH_BASE}a/</loc>".encode())
        )
        (self.lan / "sitemap.xml.gz").write_bytes(
            gzip.compress(b"<loc>http://192.168.100.120:8099/a/</loc>")
        )
        (self.gh / "assets").mkdir(parents=True, exist_ok=True)
        (self.lan / "assets").mkdir(parents=True, exist_ok=True)
        (self.gh / "assets/logo.svg").write_bytes(b"<svg/>")
        (self.lan / "assets/logo.svg").write_bytes(b"<svg/>")
        self.assertEqual(gate.compare_sites(self.gh, self.lan, GH_BASE, LAN_BASE), [])

    def test_missing_file_is_reported_without_fixed_counts(self):
        self._mirror("a.html", "x", "x")
        (self.lan / "b.html").write_text("only lan", encoding="utf-8")
        problems = gate.compare_sites(self.gh, self.lan, GH_BASE, LAN_BASE)
        self.assertTrue(any("only in lan build" in p for p in problems))

    def test_content_mismatch_is_reported(self):
        self._mirror("a.html", f'link="{GH_BASE}x/"', 'link="http://other/x/"')
        problems = gate.compare_sites(self.gh, self.lan, GH_BASE, LAN_BASE)
        self.assertEqual(problems, ["normalized content differs: a.html"])

    def test_robots_policy_mismatch_is_reported(self):
        self._mirror(
            "robots.txt", "User-agent: *\nAllow: /\n", "User-agent: *\nAllow: /\n"
        )
        problems = gate.compare_sites(self.gh, self.lan, GH_BASE, LAN_BASE)
        self.assertTrue(any("lan build" in p for p in problems))


class LoadSiteUrlTests(unittest.TestCase):
    def test_missing_site_url_exits(self):
        with tempfile.TemporaryDirectory() as temp:
            config = Path(temp) / "mkdocs.yml"
            config.write_text("site_name: x\n", encoding="utf-8")
            with self.assertRaises(SystemExit):
                gate.load_site_url(config)

    def test_reads_site_url(self):
        with tempfile.TemporaryDirectory() as temp:
            config = Path(temp) / "mkdocs-lan.yml"
            config.write_text(
                f"INHERIT: mkdocs.yml\nsite_url: {LAN_BASE}\n", encoding="utf-8"
            )
            self.assertEqual(gate.load_site_url(config), LAN_BASE)


if __name__ == "__main__":
    unittest.main()
