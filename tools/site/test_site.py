"""Regression tests for the documentation generator and fail-closed site audit."""

import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

import check_site
import generate_features
import landing
import platform_catalog
import yaml

BASE = "https://docs.example/"
REPO = "https://github.com/vibe-bimer/revit-model-mcp"


def _default_edit(relative):
    rel = relative.removeprefix("en/")
    if rel == "index.html":
        return f"{REPO}/blob/main/tools/site/landing.py"
    if rel.startswith("features/"):
        return f"{REPO}/blob/main/tools/site/generate_features.py"
    if rel.startswith("platform/"):
        return f"{REPO}/blob/main/tools/site/platform_catalog.py"
    return f"{REPO}/edit/main/docs/{rel.removesuffix('index.html')}index.md"


def _skip_link(lang):
    text = "Skip to content" if lang == "en" else "跳转至内容"
    return f'<body><a class="md-skip" href="#rmc-main">{text}</a>'


def _write_error_page(site):
    (site / "404.html").write_text(
        '<html lang="zh"><body><a class="md-skip" href="#rmc-main">跳转至内容</a>'
        '<div id="rmc-main" tabindex="-1">页面不存在</div></body></html>',
        encoding="utf-8",
    )


class SiteAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name)
        self.make_page("index.html", "zh")
        self.make_page("en/index.html", "en")
        _write_error_page(self.site)

    def make_page(
        self,
        relative,
        lang,
        extra="",
        zh=None,
        en=None,
        text=None,
        edit=None,
        base=None,
    ):
        base = BASE if base is None else base
        sibling = relative.removeprefix("en/").removesuffix("index.html")
        origin = base + relative.removesuffix("index.html")
        zh = base + sibling if zh is None else zh
        en = base + "en/" + sibling if en is None else en
        canonical = origin
        description = (
            "完整的中文功能说明与参数使用指南。"
            if lang == "zh"
            else "Complete feature documentation and parameter guidance."
        )
        locale = "zh_CN" if lang == "zh" else "en_US"
        text = text or (
            "完整的中文功能说明与参数使用指南。"
            if lang == "zh"
            else "Complete feature documentation and parameter guidance."
        )
        edit = _default_edit(relative) if edit is None else edit
        edit_html = f'<a rel="edit" href="{edit}">Edit</a>' if edit else ""
        destination = self.site / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            f'<html lang="{lang}"><head>'
            f'<meta name="description" content="{description}">'
            f'<meta property="og:locale" content="{locale}">'
            f'<meta property="og:url" content="{canonical}">'
            f'<meta property="og:description" content="{description}">'
            f'<meta name="twitter:description" content="{description}">'
            f'<link rel="canonical" href="{canonical}">'
            f'<link rel="alternate" hreflang="zh" href="{zh}">'
            f'<link rel="alternate" hreflang="en" href="{en}">'
            f"</head>{_skip_link(lang)}"
            f'<body><article id="rmc-main" tabindex="-1"><h1 id="heading">{text}</h1>{extra}</article>{edit_html}</body></html>',
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
        base = "https://docs.example/revit-model-mcp/"
        self.make_page("index.html", "zh", base=base)
        self.make_page("en/index.html", "en", base=base)
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

    def test_released_page_names_the_release_version_and_status(self):
        tool = self.tools[0]
        cap = self.capabilities["tools"][tool["name"]]
        page = generate_features.tool_page(
            tool, cap, "zh", self.capabilities, self.contracts
        )
        self.assertIn(generate_features.RELEASE_VERSION, page)
        self.assertIn("已发布", page)

    def test_released_page_links_and_diffs_its_integration_twin(self):
        platform_tools, _ = platform_catalog.load_platform()
        integration = {t["name"]: t["inputSchema"] for t in platform_tools}
        tool = next(t for t in self.tools if t["name"] == "revit_export_view")
        page = generate_features.tool_page(
            tool,
            self.capabilities["tools"][tool["name"]],
            "zh",
            self.capabilities,
            self.contracts,
            integration["revit_export_view"],
        )
        self.assertIn("(../platform/revit_export_view.md)", page)
        self.assertIn("{#contract-diff}", page)
        self.assertIn("output_path", page)
        self.assertIn("save_to", page)

    def test_released_page_without_twin_has_no_diff_section(self):
        platform_tools, _ = platform_catalog.load_platform()
        integration = {t["name"] for t in platform_tools}
        tool = next(t for t in self.tools if t["name"] not in integration)
        page = generate_features.tool_page(
            tool,
            self.capabilities["tools"][tool["name"]],
            "zh",
            self.capabilities,
            self.contracts,
        )
        self.assertNotIn("{#contract-diff}", page)

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


def _frontmatter(page):
    if not page.startswith("---\n"):
        raise AssertionError(f"page does not start with frontmatter: {page[:60]!r}")
    end = page.find("\n---\n", 4)
    if end < 0:
        raise AssertionError("frontmatter is not closed")
    return yaml.safe_load(page[4:end])


class FrontmatterDescriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tools, cls.capabilities, cls.contracts = generate_features.load()

    def test_tool_pages_carry_the_localised_summary_description(self):
        for tool in self.tools:
            cap = self.capabilities["tools"][tool["name"]]
            for lang in ("zh", "en"):
                with self.subTest(tool=tool["name"], lang=lang):
                    page = generate_features.tool_page(
                        tool, cap, lang, self.capabilities, self.contracts
                    )
                    data = _frontmatter(page)
                    self.assertEqual(data["description"], cap["summary"][lang])

    def test_section_pages_carry_a_frontmatter_description(self):
        for lang in ("zh", "en"):
            pages = {
                "index": generate_features.index_page(
                    self.tools, self.capabilities, lang
                ),
                "matrix": generate_features.matrix_page(
                    self.tools, self.capabilities, lang
                ),
                "prompts": generate_features.prompts_page(
                    self.tools, self.capabilities, lang
                ),
                "v2020": generate_features.version_page(
                    self.tools, self.capabilities, lang, "2020"
                ),
                "v2026": generate_features.version_page(
                    self.tools, self.capabilities, lang, "2026"
                ),
            }
            for name, page in pages.items():
                with self.subTest(lang=lang, page=name):
                    description = _frontmatter(page)["description"]
                    self.assertTrue(description)
                    has_cjk = any("\u4e00" <= char <= "\u9fff" for char in description)
                    self.assertEqual(has_cjk, lang == "zh")

    def test_home_page_carries_a_frontmatter_description(self):
        for lang in ("zh", "en"):
            with self.subTest(lang=lang):
                page = landing.home_page(self.tools, self.capabilities, "9.9.9", lang)
                description = _frontmatter(page)["description"]
                self.assertTrue(description)
                has_cjk = any("\u4e00" <= char <= "\u9fff" for char in description)
                self.assertEqual(has_cjk, lang == "zh")


if __name__ == "__main__":
    unittest.main()
