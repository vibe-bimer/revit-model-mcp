"""Version-aware search and catalog navigation (spec 28, W3).

These tests describe the artefacts the site ships: the object grouping shared by both
catalogs, the version entries each catalog index carries, the migration table links, the
navigation subdivisions, the search index metadata and the search data file.
"""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

import catalogs
import check_site
import generate_features
import platform_catalog

ROOT = Path(__file__).resolve().parents[2]


def load_hooks():
    spec = importlib.util.spec_from_file_location(
        "docs_hooks_for_tests", ROOT / "docs/hooks.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ObjectGroupTests(unittest.TestCase):
    def test_groups_are_declared_in_object_order(self):
        groups = catalogs.object_groups()
        self.assertEqual(list(groups), ["views", "sheets", "schedules", "view-display"])
        for key, group in groups.items():
            self.assertEqual(set(group), {"zh", "en", "tools"}, key)
            self.assertTrue(group["zh"] and group["en"], key)
            self.assertTrue(group["tools"], key)

    def test_every_grouped_tool_exists_in_a_catalog(self):
        released = {
            tool["name"]
            for tool in json.loads(
                (ROOT / "tools/site/content/tools.json").read_text(encoding="utf-8")
            )
        }
        branch = {tool["name"] for tool in platform_catalog.load_platform()[0]}
        for key, group in catalogs.object_groups().items():
            for name in group["tools"]:
                self.assertIn(name, released | branch, f"{key} names unknown {name}")

    def test_no_tool_is_grouped_twice(self):
        seen = {}
        for key, group in catalogs.object_groups().items():
            for name in group["tools"]:
                self.assertNotIn(name, seen, f"{name} is in {seen.get(name)} and {key}")
                seen[name] = key

    def test_the_views_sheets_toolset_is_fully_grouped(self):
        branch = platform_catalog.load_platform()[0]
        toolset = {tool["name"] for tool in branch if tool["toolset"] == "views-sheets"}
        grouped = {
            name
            for group in catalogs.object_groups().values()
            for name in group["tools"]
        }
        self.assertEqual(toolset - grouped, set())


class FeatureIndexTests(unittest.TestCase):
    def setUp(self):
        self.tools = generate_features.load()[0]
        self.capabilities = generate_features.load()[1]
        self.branch_count = len(platform_catalog.load_platform()[0])

    def page(self, lang):
        return generate_features.index_page(
            self.tools, self.capabilities, lang, self.branch_count
        )

    def test_version_entry_links_the_branch_catalog_with_status_and_counts(self):
        for lang, label in (("zh", "已发布"), ("en", "Released")):
            page = self.page(lang)
            self.assertIn("{#versions}", page)
            self.assertIn(label, page)
            self.assertIn(generate_features.RELEASE_VERSION, page)
            self.assertIn(platform_catalog.BRANCH, page)
            self.assertIn(f"| {len(self.tools)} |", page)
            self.assertIn(f"| {self.branch_count} |", page)
            self.assertIn("(../platform/index.md)", page)

    def test_object_groups_carry_anchors_and_link_the_branch_for_empty_groups(self):
        for lang in ("zh", "en"):
            page = self.page(lang)
            self.assertIn("{#objects}", page)
            for key in ("views", "sheets", "schedules", "view-display"):
                self.assertIn(f"{{#objects-{key}}}", page)
            self.assertIn("(../platform/index.md#objects-sheets)", page)
            self.assertIn("(../platform/index.md#objects-schedules)", page)

    def test_an_empty_object_group_does_not_emit_a_header_only_table(self):
        # A table with nothing but its header reads as a defect; the pointer to the branch catalog
        # is the whole content of that section.
        for lang in ("zh", "en"):
            page = self.page(lang)
            for key in ("sheets", "schedules"):
                start = page.index(f"{{#objects-{key}}}")
                end = page.index("###", start)
                section = page[start:end]
                self.assertNotIn("| --- | --- |", section, section)

    def test_object_groups_list_every_grouped_release_tool(self):
        page = self.page("zh")
        grouped = [
            name
            for group in catalogs.object_groups().values()
            for name in group["tools"]
        ]
        released = {tool["name"] for tool in self.tools}
        for name in grouped:
            if name in released:
                self.assertIn(f"({name}.md)", page)


class PlatformIndexTests(unittest.TestCase):
    def setUp(self):
        self.tools, self.released = platform_catalog.load_platform()

    def page(self, lang):
        return platform_catalog.index_page(self.tools, self.released, lang)

    def test_index_links_the_release_catalog_with_status_and_counts(self):
        for lang, label in (("zh", "已发布"), ("en", "Released")):
            page = self.page(lang)
            self.assertIn("{#versions}", page)
            self.assertIn(label, page)
            self.assertIn(platform_catalog.RELEASE_VERSION, page)
            self.assertIn("(../features/index.md)", page)
            self.assertIn(f"| {len(self.released)} |", page)

    def test_object_groups_keep_the_toolset_anchor(self):
        for lang in ("zh", "en"):
            page = self.page(lang)
            self.assertIn("{#group-views-sheets}", page)
            for key in ("views", "sheets", "schedules", "view-display"):
                self.assertIn(f"{{#objects-{key}}}", page)

    def test_object_groups_list_the_branch_tools(self):
        page = self.page("zh")
        for group in catalogs.object_groups().values():
            for name in group["tools"]:
                self.assertIn("[", page)
                self.assertIn(f"({name}.md)", page)


class MigrationTableTests(unittest.TestCase):
    def test_every_row_points_at_a_page_or_a_status_anchor(self):
        tools, _ = platform_catalog.load_platform()
        names = {tool["name"] for tool in tools}
        for lang in ("zh", "en"):
            page = platform_catalog.fork_page(tools, lang)
            rows = [
                line
                for line in page.splitlines()
                if line.startswith("| ") and "`revit_" in line
            ]
            self.assertEqual(len(rows), len(platform_catalog.FORK_TOOLS))
            for line in rows:
                self.assertRegex(line, r"\]\([^)]+\)", line)
                name = line.split("`")[1]
                if name in names:
                    self.assertIn(f"({name}.md)", line)
                else:
                    anchor = "#" + name.replace("_", "-")
                    self.assertIn(f"({anchor})", line)


class NavigationTests(unittest.TestCase):
    def test_platform_navigation_subdivides_the_views_sheets_group(self):
        tools, _ = platform_catalog.load_platform()
        block = platform_catalog.nav_block(tools)
        groups = catalogs.object_groups()
        section = block.split(
            f"      - {platform_catalog.GROUP_LABELS['zh']['views-sheets']}:"
        )[1]
        section = section.split("\n      - ")[0]
        for group in groups.values():
            self.assertIn(f"          - {group['zh']}:", section)
        members = [tool["name"] for tool in tools if tool["toolset"] == "views-sheets"]
        for name in members:
            self.assertEqual(
                section.count(f"platform/{name}.md"), 1, f"{name} appears once"
            )


class SearchIndexEnrichmentTests(unittest.TestCase):
    def test_each_entry_carries_language_tool_and_status(self):
        hooks = load_hooks()
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "search").mkdir()
            (site / "search/search_index.json").write_text(
                json.dumps(
                    {
                        "config": {"lang": ["en", "zh"]},
                        "docs": [
                            {
                                "location": "",
                                "title": "Revit Model MCP",
                                "text": "home",
                            },
                            {
                                "location": "features/revit_export_view/",
                                "title": "导出视图图片",
                                "text": "已发布 0.9.0",
                            },
                            {
                                "location": "en/features/revit_export_view/",
                                "title": "Export view image",
                                "text": "Released 0.9.0",
                            },
                            {
                                "location": "platform/revit_export_view/",
                                "title": "导出视图为 PNG",
                                "text": "未发布（集成分支）",
                            },
                            {
                                "location": "features/#group-views",
                                "title": "视图与截图 (6)",
                                "text": "",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            hooks.enrich_search_index(site)
            data = json.loads((site / "search/search_index.json").read_text())
        docs = {doc["location"]: doc for doc in data["docs"]}
        self.assertEqual(docs[""]["lang"], "zh")
        self.assertIsNone(docs[""]["tool"])
        self.assertEqual(docs["features/revit_export_view/"]["lang"], "zh")
        self.assertEqual(
            docs["features/revit_export_view/"]["tool"], "revit_export_view"
        )
        self.assertEqual(docs["features/revit_export_view/"]["status"], "released")
        self.assertEqual(
            docs["features/revit_export_view/"]["version"],
            generate_features.RELEASE_VERSION,
        )
        self.assertEqual(docs["en/features/revit_export_view/"]["lang"], "en")
        self.assertEqual(docs["en/features/revit_export_view/"]["catalog"], "release")
        self.assertEqual(docs["platform/revit_export_view/"]["status"], "unreleased")
        self.assertEqual(
            docs["platform/revit_export_view/"]["branch"], platform_catalog.BRANCH
        )
        self.assertEqual(docs["features/#group-views"]["tool"], None)

    def test_enrichment_is_idempotent(self):
        hooks = load_hooks()
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "search").mkdir()
            payload = {
                "config": {"lang": ["en", "zh"]},
                "docs": [
                    {
                        "location": "platform/revit_ping/",
                        "title": "Ping",
                        "text": "",
                    }
                ],
            }
            index = site / "search/search_index.json"
            index.write_text(json.dumps(payload), encoding="utf-8")
            hooks.enrich_search_index(site)
            first = index.read_text()
            hooks.enrich_search_index(site)
            self.assertEqual(first, index.read_text())


class SearchCatalogDataTests(unittest.TestCase):
    def setUp(self):
        self.tools = generate_features.load()[0]
        self.capabilities = generate_features.load()[1]
        self.contracts = generate_features.load()[2]
        self.files = generate_features.generate(
            self.tools, self.capabilities, self.contracts
        )

    def test_the_search_data_file_ships_with_the_generated_site(self):
        path = ROOT / "docs/javascripts/search-catalog.js"
        self.assertIn(path, self.files)
        text = self.files[path]
        self.assertTrue(text.startswith("/*"))
        payload = json.loads(text[text.index("{") : text.rindex("}") + 1])
        release = payload["release"]
        self.assertEqual(release["version"], generate_features.RELEASE_VERSION)
        self.assertEqual(release["status"], "released")
        self.assertEqual(release["directory"], "features")
        self.assertEqual(len(release["tools"]), len(self.tools))
        self.assertEqual(
            release["tools"]["revit_export_view"]["zh"],
            self.capabilities["tools"]["revit_export_view"]["title"]["zh"],
        )
        self.assertEqual(
            release["tools"]["revit_export_view"]["en"],
            self.capabilities["tools"]["revit_export_view"]["title"]["en"],
        )
        branch = payload["branch"]
        self.assertEqual(branch["status"], "unreleased")
        self.assertEqual(branch["branch"], platform_catalog.BRANCH)
        self.assertEqual(branch["directory"], "platform")
        self.assertEqual(len(branch["tools"]), len(platform_catalog.load_platform()[0]))

    def test_the_search_scripts_are_registered_for_every_page(self):
        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        self.assertIn("javascripts/search-catalog.js", config)
        self.assertIn("javascripts/search-enhance.js", config)


class CheckSiteSearchTests(unittest.TestCase):
    def build(self, directory, index, pages):
        site = Path(directory)
        (site / "search").mkdir(parents=True)
        (site / "search/search_index.json").write_text(
            json.dumps({"config": {"lang": ["en", "zh"]}, "docs": index}),
            encoding="utf-8",
        )
        for relative, lang in pages.items():
            page = site / relative / "index.html"
            page.parent.mkdir(parents=True, exist_ok=True)
            page.write_text(
                f'<!doctype html><html lang="{lang}"><body><article>'
                f"<p>正文 revit_export_view 已发布</p></article></body></html>",
                encoding="utf-8",
            )
        return site

    def test_an_entry_without_language_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            site = self.build(
                directory,
                [
                    {
                        "location": "features/revit_export_view/",
                        "title": "导出",
                        "text": "",
                    }
                ],
                {"features/revit_export_view": "zh"},
            )
            errors = check_site.audit_search_index(site)
        self.assertTrue(any("missing lang" in error for error in errors), errors)

    def test_a_wrong_language_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            site = self.build(
                directory,
                [
                    {
                        "location": "features/revit_export_view/",
                        "title": "导出",
                        "text": "revit_export_view 已发布 0.9.0",
                        "lang": "en",
                        "tool": "revit_export_view",
                        "status": "released",
                    }
                ],
                {"features/revit_export_view": "zh"},
            )
            errors = check_site.audit_search_index(site)
        self.assertTrue(any("lang" in error for error in errors), errors)

    def test_a_tool_page_entry_needs_its_tool_name_and_status(self):
        with tempfile.TemporaryDirectory() as directory:
            site = self.build(
                directory,
                [
                    {
                        "location": "platform/revit_export_view/",
                        "title": "导出视图为 PNG",
                        "text": "没有标记",
                        "lang": "zh",
                        "tool": "revit_export_view",
                        "status": "unreleased",
                    }
                ],
                {"platform/revit_export_view": "zh"},
            )
            errors = check_site.audit_search_index(site)
        self.assertTrue(any("status marker" in error for error in errors), errors)
        self.assertTrue(any("tool name" in error for error in errors), errors)

    def test_a_complete_entry_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            site = self.build(
                directory,
                [
                    {
                        "location": "features/revit_export_view/",
                        "title": "导出视图图片",
                        "text": "revit_export_view 已发布 0.9.0",
                        "lang": "zh",
                        "tool": "revit_export_view",
                        "status": "released",
                    }
                ],
                {"features/revit_export_view": "zh"},
            )
            errors = check_site.audit_search_index(site)
        self.assertEqual(errors, [])

    def test_a_section_entry_inherits_its_page_entry(self):
        with tempfile.TemporaryDirectory() as directory:
            site = self.build(
                directory,
                [
                    {
                        "location": "features/revit_export_view/",
                        "title": "导出视图图片",
                        "text": "revit_export_view 已发布 0.9.0",
                        "lang": "zh",
                        "tool": "revit_export_view",
                        "status": "released",
                    },
                    {
                        "location": "features/revit_export_view/#parameters",
                        "title": "导出视图图片 - 参数",
                        "text": "dx_mm 单位",
                        "lang": "zh",
                        "tool": "revit_export_view",
                        "status": "released",
                    },
                ],
                {"features/revit_export_view": "zh"},
            )
            errors = check_site.audit_search_index(site)
        self.assertEqual(errors, [])

    def test_a_section_entry_without_its_page_entry_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            site = self.build(
                directory,
                [
                    {
                        "location": "features/revit_export_view/#parameters",
                        "title": "导出视图图片 - 参数",
                        "text": "dx_mm 单位",
                        "lang": "zh",
                        "tool": "revit_export_view",
                        "status": "released",
                    }
                ],
                {"features/revit_export_view": "zh"},
            )
            errors = check_site.audit_search_index(site)
        self.assertTrue(any("page entry" in error for error in errors), errors)


class CheckSiteNavigationTests(unittest.TestCase):
    def page(self, rows):
        body = "\n".join(f"<tr>{row}</tr>" for row in rows)
        return (
            "<!doctype html><html lang='zh'><body><article>"
            f"<table><tbody>{body}</tbody></table></article></body></html>"
        )

    def test_a_migration_row_without_a_link_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            page = site / "platform/fork-tools/index.html"
            page.parent.mkdir(parents=True)
            page.write_text(
                self.page(
                    [
                        "<td>创建标高<br><code>revit_create_level</code></td><td>自研</td>"
                    ]
                ),
                encoding="utf-8",
            )
            errors = check_site.audit_migration_table(site)
        self.assertTrue(any("revit_create_level" in error for error in errors), errors)

    def test_a_linked_migration_row_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            page = site / "platform/fork-tools/index.html"
            page.parent.mkdir(parents=True)
            page.write_text(
                self.page(
                    [
                        (
                            '<td><a href="#revit-create-level">创建标高</a><br>'
                            "<code>revit_create_level</code></td><td>自研</td>"
                        )
                    ]
                ),
                encoding="utf-8",
            )
            errors = check_site.audit_migration_table(site)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
