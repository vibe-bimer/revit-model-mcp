"""Regression tests for the platform catalog: the integration branch's 80 tools.

The catalog is generated from a snapshot of an unreleased branch, so the failure modes worth
guarding are the quiet ones: a snapshot that drifts from its own count, a tool without Chinese
page text, or a nav block that stops matching the snapshot.
"""

import unittest

import platform_catalog
import yaml


class SnapshotAuditTests(unittest.TestCase):
    def payload(self):
        return platform_catalog.snapshot()

    def test_the_snapshot_counts_what_it_holds(self):
        payload = self.payload()
        self.assertEqual(payload["count"], len(payload["tools"]))
        self.assertEqual(payload["count"], 80)

    def test_the_snapshot_records_where_it_came_from(self):
        provenance = self.payload()["provenance"]
        self.assertEqual(provenance["branch"], platform_catalog.BRANCH)
        self.assertEqual(len(provenance["commit"]), 40)

    def test_audit_rejects_a_wrong_count(self):
        payload = self.payload()
        with self.assertRaises(SystemExit):
            platform_catalog.audit(payload["tools"], {**payload, "count": 79})

    def test_audit_rejects_a_duplicate_tool(self):
        payload = self.payload()
        tools = payload["tools"] + [payload["tools"][0]]
        with self.assertRaises(SystemExit):
            platform_catalog.audit(tools, {**payload, "count": len(tools)})

    def test_audit_rejects_an_unknown_toolset(self):
        payload = self.payload()
        tools = [dict(tool) for tool in payload["tools"]]
        tools[0]["toolset"] = "invented"
        with self.assertRaises(SystemExit):
            platform_catalog.audit(tools, payload)

    def test_audit_rejects_a_tool_without_chinese_text(self):
        payload = self.payload()
        tools = [tool for tool in payload["tools"] if tool["name"] != "revit_ping"]
        with self.assertRaises(SystemExit):
            platform_catalog.audit(tools, {**payload, "count": len(tools)})

    def test_every_tool_has_chinese_page_text(self):
        names = {tool["name"] for tool in self.payload()["tools"]}
        self.assertEqual(sorted(names - set(platform_catalog.ZH)), [])


class ForkToolTests(unittest.TestCase):
    def test_the_fork_owns_eight_tools(self):
        self.assertEqual(len(platform_catalog.FORK_TOOLS), 8)

    def test_only_the_lighting_tool_is_grafted(self):
        grafted = [
            name
            for name, item in platform_catalog.FORK_TOOLS.items()
            if item["status"] == "grafted"
        ]
        self.assertEqual(grafted, ["revit_set_view_lighting"])

    def test_the_grafted_tool_is_in_the_snapshot_and_the_rest_are_not(self):
        names = {tool["name"] for tool in platform_catalog.load_platform()[0]}
        self.assertIn("revit_set_view_lighting", names)
        pending = {
            name
            for name, item in platform_catalog.FORK_TOOLS.items()
            if item["status"] == "pending"
        }
        self.assertEqual(sorted(pending & names), [])
        self.assertEqual(len(pending), 7)

    def test_every_fork_tool_carries_both_note_languages(self):
        for name, item in platform_catalog.FORK_TOOLS.items():
            for field in ("zh", "en", "zh_note", "en_note", "status"):
                self.assertTrue(item.get(field), f"{name} is missing {field}")


def _body(page: str) -> str:
    """Strip the generated frontmatter so body assertions stay about the page text."""
    if page.startswith("---\n"):
        return page.split("\n---\n", 1)[1].lstrip("\n")
    return page


class PageTests(unittest.TestCase):
    def setUp(self):
        self.tools, self.released = platform_catalog.load_platform()
        self.released_names = {tool["name"] for tool in self.released}

    def test_generate_covers_every_tool_in_both_languages(self):
        files = platform_catalog.generate()
        self.assertEqual(len(files), 2 * (len(self.tools) + 2))
        for tool in self.tools:
            for suffix in ("", ".en"):
                self.assertIn(
                    platform_catalog.PAGES / f"{tool['name']}{suffix}.md", files
                )

    def test_the_chinese_page_shows_the_chinese_text_and_the_facts_strip(self):
        tool = next(t for t in self.tools if t["name"] == "revit_set_view_lighting")
        page = platform_catalog.tool_page(tool, self.released, "zh")
        title, summary = platform_catalog.ZH[tool["name"]]
        self.assertTrue(_body(page).startswith(f"# {title}"))
        self.assertIn(summary, page)
        self.assertIn('class="facts"', page)
        self.assertIn("已移植", page)

    def test_the_english_page_is_english(self):
        tool = next(t for t in self.tools if t["name"] == "revit_set_view_lighting")
        page = platform_catalog.tool_page(tool, self.released, "en")
        for line in page.splitlines():
            self.assertFalse(
                any("\u4e00" <= char <= "\u9fff" for char in line),
                f"Chinese in: {line}",
            )

    def test_the_index_separates_base_from_fork(self):
        page = platform_catalog.index_page(self.tools, self.released, "zh")
        self.assertIn("基座（上游）", page)
        self.assertIn("自研（本仓库）", page)
        self.assertIn("| **合计** | **79** | **1** |", page)
        self.assertIn(f"| 工具数 | {len(self.released)} | {len(self.tools)} |", page)

    def test_the_fork_page_lists_all_eight_with_status(self):
        page = platform_catalog.fork_page(self.tools, "zh")
        for name in platform_catalog.FORK_TOOLS:
            self.assertIn(f"`{name}`", page)
        self.assertIn("已移植", page)
        self.assertIn("待移植", page)

    def test_nav_block_lists_every_page_and_keeps_group_order(self):
        block = platform_catalog.nav_block(self.tools)
        lines = block.splitlines()
        self.assertEqual(lines[0], platform_catalog.NAV_START)
        self.assertEqual(lines[-1], platform_catalog.NAV_END)
        pages = [
            line.strip()[2:]
            for line in lines
            if line.strip().startswith("- platform/") and line.strip().endswith(".md")
        ]
        for tool in self.tools:
            self.assertIn(f"platform/{tool['name']}.md", pages)
        self.assertIn("platform/index.md", block)
        self.assertIn("platform/fork-tools.md", block)
        groups = [
            line.strip()[2:].rstrip(":")
            for line in lines
            if line.strip().startswith("- ") and line.strip().endswith(":")
        ]
        expected = [
            platform_catalog.GROUP_LABELS["zh"][key]
            for key in platform_catalog.GROUP_LABELS["zh"]
        ]
        self.assertEqual([g for g in groups if g in expected], expected)

    def test_a_same_name_page_shows_unreleased_status_and_links_its_twin(self):
        tool = next(t for t in self.tools if t["name"] == "revit_export_view")
        page = platform_catalog.tool_page(tool, self.released, "zh")
        self.assertIn("未发布", page)
        self.assertIn("integration/upstream-1.0", page)
        self.assertIn(platform_catalog.COMMIT, page)
        self.assertIn("(../features/revit_export_view.md)", page)
        self.assertIn("{#contract-diff}", page)
        self.assertIn("output_path", page)
        self.assertIn("save_to", page)

    def test_a_branch_only_tool_has_no_release_twin_section(self):
        name = next(
            tool["name"]
            for tool in self.tools
            if tool["name"] not in self.released_names
        )
        tool = next(t for t in self.tools if t["name"] == name)
        page = platform_catalog.tool_page(tool, self.released, "zh")
        self.assertIn("未发布", page)
        self.assertNotIn("{#contract-diff}", page)
        self.assertNotIn(f"(../features/{name}.md)", page)

    def test_generate_is_deterministic(self):
        self.assertEqual(platform_catalog.generate(), platform_catalog.generate())


class PagePathTests(unittest.TestCase):
    def test_written_pages_are_current(self):
        files = platform_catalog.generate()
        stale = [
            str(path.relative_to(platform_catalog.ROOT))
            for path, content in files.items()
            if not path.exists() or path.read_text(encoding="utf-8") != content
        ]
        self.assertEqual(stale, [], "run tools/site/generate_features.py --write")


def _frontmatter(page):
    if not page.startswith("---\n"):
        raise AssertionError(f"page does not start with frontmatter: {page[:60]!r}")
    end = page.find("\n---\n", 4)
    if end < 0:
        raise AssertionError("frontmatter is not closed")
    return yaml.safe_load(page[4:end])


class DescriptionFrontmatterTests(unittest.TestCase):
    def setUp(self):
        self.tools, self.released = platform_catalog.load_platform()

    def test_tool_pages_carry_a_localised_description(self):
        for name in ("revit_set_view_lighting", "revit_export_view"):
            tool = next(item for item in self.tools if item["name"] == name)
            for lang in ("zh", "en"):
                with self.subTest(tool=name, lang=lang):
                    description = _frontmatter(
                        platform_catalog.tool_page(tool, self.released, lang)
                    )["description"]
                    self.assertTrue(description)
                    has_cjk = any("\u4e00" <= char <= "\u9fff" for char in description)
                    self.assertEqual(has_cjk, lang == "zh")

    def test_index_and_fork_pages_carry_a_description(self):
        for lang in ("zh", "en"):
            for page in (
                platform_catalog.index_page(self.tools, self.released, lang),
                platform_catalog.fork_page(self.tools, lang),
            ):
                with self.subTest(lang=lang):
                    description = _frontmatter(page)["description"]
                    self.assertTrue(description)
                    has_cjk = any("\u4e00" <= char <= "\u9fff" for char in description)
                    self.assertEqual(has_cjk, lang == "zh")


if __name__ == "__main__":
    unittest.main()


class ParameterDefaultTests(unittest.TestCase):
    """A parameter table must keep "no default", an empty string and null apart.

    The three states mean different things to a caller: no default key means the schema does not
    say, an empty string is an explicit "clear it" value, and null means "leave it unchanged".
    Rendering the first two as the same dash hides a real difference in behavior.
    """

    def rows(self, properties: dict, lang: str = "zh") -> list[str]:
        tool = {"name": "revit_probe", "inputSchema": {"properties": properties}}
        return platform_catalog.parameter_rows(tool, False, lang)

    def test_a_missing_default_renders_as_a_dash(self):
        for lang in ("zh", "en"):
            rows = self.rows({"element_ids": {"type": "array"}}, lang)
            self.assertIn("| — |", rows[0], f"{lang}: {rows[0]}")

    def test_an_empty_string_default_renders_as_an_explicit_empty_string(self):
        for lang in ("zh", "en"):
            rows = self.rows({"prefix": {"type": "string", "default": ""}}, lang)
            self.assertIn('| `""` |', rows[0], f"{lang}: {rows[0]}")

    def test_a_null_default_renders_as_null_not_python_none(self):
        for lang in ("zh", "en"):
            rows = self.rows({"view": {"type": "string", "default": None}}, lang)
            self.assertIn("| `null` |", rows[0], f"{lang}: {rows[0]}")
            self.assertNotIn("None", rows[0], f"{lang}: {rows[0]}")

    def test_the_three_states_stay_distinct_side_by_side(self):
        rows = self.rows(
            {
                "element_ids": {"type": "array"},
                "prefix": {"type": "string", "default": ""},
                "view": {"type": "string", "default": None},
            }
        )
        defaults = [row.split(" | ")[2] for row in rows]
        self.assertEqual(defaults, ["—", '`""`', "`null`"])

    def test_a_generated_platform_page_shows_the_empty_string_default(self):
        tool = next(
            tool
            for tool in platform_catalog.load_platform()[0]
            if tool["name"] == "revit_align_link_datums"
        )
        for lang in ("zh", "en"):
            page = platform_catalog.tool_page(
                tool, platform_catalog.load_platform()[1], lang
            )
            self.assertIn("| `prefix` |", page)
            self.assertIn(
                '| `""` |', page, f"{lang} page lost the empty-string default"
            )
            self.assertIn("| `null` |", page, f"{lang} page lost a null default")

    def test_no_generated_platform_page_renders_python_none(self):
        files = platform_catalog.generate()
        offenders = [
            str(path.relative_to(platform_catalog.ROOT))
            for path, content in files.items()
            if "| None |" in content
        ]
        self.assertEqual(offenders, [])
