"""Regression tests for the documentation generator and fail-closed site audit."""

import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

import check_site
import generate_features


class SiteAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name)
        self.make_page("index.html", "zh")
        self.make_page("en/index.html", "en")

    def make_page(self, relative, lang, extra="", zh=None, en=None, text=None):
        sibling = relative.removeprefix("en/").removesuffix("index.html")
        zh = "/" + sibling if zh is None else zh
        en = "/en/" + sibling if en is None else en
        text = text or (
            "完整的中文功能说明与参数使用指南。"
            if lang == "zh"
            else "Complete feature documentation and parameter guidance."
        )
        destination = self.site / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            f'<html lang="{lang}"><head><link rel="canonical" href="https://docs.example/{relative.removesuffix("index.html")}"><link rel="alternate" hreflang="zh" href="{zh}"><link rel="alternate" hreflang="en" href="{en}"></head><body><article><h1 id="heading">{text}</h1>{extra}</article></body></html>',
            encoding="utf-8",
        )
        return destination

    def errors(self):
        return check_site.audit_site(self.site)[0]

    def test_valid_language_pair(self):
        self.assertEqual(self.errors(), [])

    def test_relative_and_url_encoded_anchors(self):
        self.make_page(
            "index.html",
            "zh",
            '<a href="en/#heading">English</a><a href="#%68eading">标题</a>',
        )
        self.assertEqual(self.errors(), [])

    def test_missing_target_is_an_error(self):
        self.make_page("index.html", "zh", '<img src="missing.svg">')
        self.assertTrue(any("missing target" in error for error in self.errors()))

    def test_missing_anchor_is_an_error(self):
        self.make_page("index.html", "zh", '<a href="en/#not-present">English</a>')
        self.assertTrue(any("missing anchor" in error for error in self.errors()))

    def test_external_links_are_not_local_errors(self):
        self.make_page(
            "index.html",
            "zh",
            '<a href="https://outside.example/missing/#no">外部</a><a href="mailto:help@example.com">联系</a>',
        )
        self.assertEqual(self.errors(), [])

    def test_same_host_absolute_links_are_checked(self):
        self.make_page(
            "index.html", "zh", '<a href="https://docs.example/missing/">链接</a>'
        )
        self.assertTrue(any("missing target" in error for error in self.errors()))

    def test_wrong_language_switch_is_an_error(self):
        self.make_page("index.html", "zh", en="/")
        self.assertTrue(any("language-switch" in error for error in self.errors()))

    def test_absent_language_sibling_is_an_error(self):
        self.make_page("feature/index.html", "zh")
        self.assertTrue(any("language-switch" in error for error in self.errors()))

    def test_english_fallback_in_chinese_page_is_an_error(self):
        self.make_page("index.html", "zh", text="This page was never translated.")
        self.assertTrue(any("too little Chinese" in error for error in self.errors()))

    def test_code_samples_do_not_count_as_untranslated_prose(self):
        self.make_page(
            "en/index.html", "en", "<code>" + "模型标高中文示例" * 100 + "</code>"
        )
        self.assertEqual(self.errors(), [])

    def test_missing_new_build_does_not_check_old_build(self):
        errors, stats = check_site.audit_site(self.site / "site.new")
        self.assertTrue(errors)
        self.assertEqual(stats["pages"], 0)
        self.assertEqual(self.errors(), [])

    def test_github_pages_prefix(self):
        self.make_page(
            "index.html", "zh", zh="/revit-model-mcp/", en="/revit-model-mcp/en/"
        )
        self.make_page(
            "en/index.html", "en", zh="/revit-model-mcp/", en="/revit-model-mcp/en/"
        )
        errors, _ = check_site.audit_site(
            self.site, "https://docs.example/revit-model-mcp/"
        )
        self.assertEqual(errors, [])

    def test_source_pair_and_navigation_coverage(self):
        root = self.site / "source"
        (root / "docs").mkdir(parents=True)
        (root / "mkdocs.yml").write_text("nav:\n  - Home: index.md\n")
        (root / "docs/index.md").write_text("# 中文\n")
        (root / "docs/index.en.md").write_text("# English\n")
        self.assertEqual(check_site.audit_sources(root), [])
        (root / "docs/orphan.md").write_text("# 孤立\n")
        self.assertEqual(len(check_site.audit_sources(root)), 2)

    def test_source_anchor_check_covers_explicit_ids_and_heads(self):
        root = self.site / "anchors"
        (root / "docs").mkdir(parents=True)
        (root / "mkdocs.yml").write_text("nav: []\n")
        # A quoted '<title>' string stops MkDocs' raw-HTML scan, so explicit heading ids must be used.
        (root / "docs/actions.md").write_text(
            "## 门禁 {#gates}\n原文返回 `Cannot run '<command>' on '<title>'`。\n"
        )
        (root / "docs/actions.en.md").write_text("## Gates {#gates}\n")
        (root / "docs/index.md").write_text("[门禁](actions.md#gates)\n")
        (root / "docs/index.en.md").write_text("[Gates](actions.md#gates)\n")
        anchors = check_site.source_anchors(root / "docs/actions.md")
        self.assertIn("gates", anchors)
        self.assertEqual(check_site.audit_source_anchors(root), [])
        (root / "docs/index.md").write_text("[门禁](actions.md#missing)\n")
        errors = check_site.audit_source_anchors(root)
        self.assertEqual(len(errors), 1)
        self.assertIn("'#missing'", errors[0])

    def test_generated_chinese_anchor_is_not_reported(self):
        root = self.site / "auto"
        (root / "docs").mkdir(parents=True)
        (root / "mkdocs.yml").write_text("nav: []\n")
        (root / "docs/target.md").write_text("## 参数\n")
        (root / "docs/source.md").write_text("[参数](target.md#_1)\n")
        self.assertEqual(check_site.audit_source_anchors(root), [])

    def test_repository_sources_have_valid_anchors_and_pairs(self):
        root = Path(check_site.__file__).resolve().parents[2]
        self.assertEqual(check_site.audit_source_anchors(root), [])
        self.assertEqual(check_site.audit_sources(root), [])


class FeatureGeneratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tools, cls.capabilities, cls.contracts = generate_features.load()

    def test_every_tool_has_both_complete_contracts(self):
        for tool in self.tools:
            cap = self.capabilities["tools"][tool["name"]]
            with self.subTest(tool=tool["name"]):
                zh = generate_features.tool_page(
                    tool, cap, "zh", self.capabilities, self.contracts
                )
                en = generate_features.tool_page(
                    tool, cap, "en", self.capabilities, self.contracts
                )
                self.assertIn("## 功能说明与返回结果", zh)
                self.assertIn("## Behavior and returned data", en)
                for paragraph in tool["description"].strip().split("\n\n"):
                    paragraph = "\n".join(
                        line.strip() for line in paragraph.splitlines()
                    )
                    self.assertIn(paragraph, en)

    def test_missing_parameter_translation_fails_closed(self):
        with self.assertRaisesRegex(SystemExit, "Missing zh parameter meaning"):
            generate_features.parameter_meaning(
                self.tools[0],
                "undocumented",
                {"type": "string", "description": "English only"},
                {},
                "zh",
            )

    def test_required_nullable_parameter_is_not_optional(self):
        tool = next(item for item in self.tools if item["name"] == "revit_place_family")
        rows = generate_features.table_rows(tool, False, self.capabilities, "en")
        self.assertTrue(
            any(
                row.startswith("| `type_name` | Yes | — | `string / null`")
                for row in rows
            )
        )

    def test_missing_business_parameters_use_explicit_message(self):
        tool = next(item for item in self.tools if item["name"] == "revit_ping")
        page = generate_features.tool_page(
            tool,
            self.capabilities["tools"][tool["name"]],
            "zh",
            self.capabilities,
            self.contracts,
        )
        self.assertIn("此工具没有额外业务参数", page)
        self.assertIn("### 通用参数", page)

    def test_regenerated_navigation_covers_each_tool_once(self):
        nav = generate_features.nav_block(self.tools, self.capabilities)
        for tool in self.tools:
            self.assertEqual(nav.count(f"features/{tool['name']}.md"), 1)

    def test_stale_contract_hash_blocks_generation(self):
        contracts = deepcopy(self.contracts)
        contracts[self.tools[0]["name"]]["source"] = "0" * 64
        original = generate_features.yaml.safe_load

        def load_yaml(text):
            loaded = original(text)
            return (
                {"tools": contracts}
                if loaded.get("tools") == self.contracts
                else loaded
            )

        with (
            patch.object(generate_features.yaml, "safe_load", side_effect=load_yaml),
            self.assertRaisesRegex(SystemExit, "stale Chinese contract"),
        ):
            generate_features.load()


if __name__ == "__main__":
    unittest.main()
