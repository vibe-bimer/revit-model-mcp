"""Regression tests for the documentation generator and fail-closed site audit."""

import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

import check_site
import generate_features

PAGE_TEXT = "Complete feature documentation and parameter guidance."


def page(text=None, extra=""):
    body = PAGE_TEXT if text is None else text
    return (
        '<html lang="en"><head><link rel="canonical" href="https://docs.example/">'
        "</head><body><article>"
        f'<h1 id="heading">{body}</h1>{extra}'
        "</article></body></html>"
    )


class SiteAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name)
        self.make_page("index.html")

    def make_page(self, relative, extra="", text=None):
        destination = self.site / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(page(text=text, extra=extra), encoding="utf-8")
        return destination

    def errors(self):
        return check_site.audit_site(self.site)[0]

    def test_valid_site(self):
        self.make_page("feature/index.html")
        self.assertEqual(self.errors(), [])

    def test_relative_and_url_encoded_anchors(self):
        self.make_page("feature/index.html")
        self.make_page(
            "index.html",
            '<a href="feature/#heading">Feature</a><a href="#%68eading">Here</a>',
        )
        self.assertEqual(self.errors(), [])

    def test_missing_target_is_an_error(self):
        self.make_page("index.html", '<img src="missing.svg">')
        self.assertTrue(any("missing target" in error for error in self.errors()))

    def test_missing_anchor_is_an_error(self):
        self.make_page("feature/index.html")
        self.make_page("index.html", '<a href="feature/#not-present">Feature</a>')
        self.assertTrue(any("missing anchor" in error for error in self.errors()))

    def test_external_links_are_not_local_errors(self):
        self.make_page(
            "index.html",
            '<a href="https://outside.example/missing/#no">Outside</a>'
            '<a href="mailto:help@example.com">Mail</a>',
        )
        self.assertEqual(self.errors(), [])

    def test_same_host_absolute_links_are_checked(self):
        self.make_page("index.html", '<a href="https://docs.example/missing/">Link</a>')
        self.assertTrue(any("missing target" in error for error in self.errors()))

    def test_empty_article_is_an_error(self):
        self.make_page("index.html", text=" ")
        self.assertTrue(any("empty article" in error for error in self.errors()))

    def test_missing_new_build_does_not_check_old_build(self):
        errors, stats = check_site.audit_site(self.site / "site.new")
        self.assertTrue(errors)
        self.assertEqual(stats["pages"], 0)
        self.assertEqual(self.errors(), [])

    def test_github_pages_prefix(self):
        self.make_page("feature/index.html")
        errors, _ = check_site.audit_site(
            self.site, "https://docs.example/revit-model-mcp/"
        )
        self.assertEqual(errors, [])

    def test_source_navigation_coverage(self):
        root = self.site / "source"
        (root / "docs").mkdir(parents=True)
        (root / "mkdocs.yml").write_text("nav:\n  - Home: index.md\n")
        (root / "docs/index.md").write_text("# Home\n")
        self.assertEqual(check_site.audit_sources(root), [])
        (root / "docs/orphan.md").write_text("# Orphan\n")
        self.assertEqual(check_site.audit_sources(root), [])
        (root / "docs/features").mkdir()
        (root / "docs/features/orphan.md").write_text("# Orphan\n")
        self.assertEqual(len(check_site.audit_sources(root)), 1)
        (root / "docs/features/orphan.md").unlink()
        (root / "mkdocs.yml").write_text(
            "nav:\n  - Home: index.md\n  - Orphan: orphan.md\n  - Home again: index.md\n"
        )
        errors = check_site.audit_sources(root)
        self.assertEqual(len(errors), 1)
        self.assertIn("Duplicate navigation entry", errors[0])
        (root / "mkdocs.yml").write_text(
            "nav:\n  - Home: index.md\n  - Gone: gone.md\n"
        )
        self.assertIn(
            "Navigation references missing source: gone.md",
            check_site.audit_sources(root),
        )

    def test_source_anchor_check_covers_explicit_ids_and_heads(self):
        root = self.site / "anchors"
        (root / "docs").mkdir(parents=True)
        (root / "mkdocs.yml").write_text("nav: []\n")
        # A quoted '<title>' string stops MkDocs' raw-HTML scan, so explicit heading ids must be used.
        (root / "docs/actions.md").write_text(
            "## Gates {#gates}\nThe call returns 'Cannot run <command> on <title>'.\n"
        )
        (root / "docs/index.md").write_text("[Gates](actions.md#gates)\n")
        anchors = check_site.source_anchors(root / "docs/actions.md")
        self.assertIn("gates", anchors)
        self.assertEqual(check_site.audit_source_anchors(root), [])
        (root / "docs/index.md").write_text("[Gates](actions.md#missing)\n")
        errors = check_site.audit_source_anchors(root)
        self.assertEqual(len(errors), 1)
        self.assertIn("'#missing'", errors[0])

    def test_snippet_includes_contribute_anchors(self):
        root = self.site / "snippets"
        (root / "docs").mkdir(parents=True)
        (root / "mkdocs.yml").write_text("nav: []\n")
        (root / "CONTRIBUTING.md").write_text("## Labels and milestones\n")
        (root / "docs/contributing.md").write_text('--8<-- "CONTRIBUTING.md"\n')
        (root / "docs/roadmap.md").write_text(
            "[Labels](contributing.md#labels-and-milestones)\n"
        )
        self.assertIn(
            "labels-and-milestones",
            check_site.source_anchors(root / "docs/contributing.md", root),
        )
        self.assertEqual(check_site.audit_source_anchors(root), [])

    def test_generated_anchor_is_not_reported(self):
        root = self.site / "auto"
        (root / "docs").mkdir(parents=True)
        (root / "mkdocs.yml").write_text("nav: []\n")
        (root / "docs/target.md").write_text("## Parameters\n")
        (root / "docs/source.md").write_text("[Parameters](target.md#_1)\n")
        self.assertEqual(check_site.audit_source_anchors(root), [])

    def test_repository_sources_have_valid_anchors_and_navigation(self):
        root = Path(check_site.__file__).resolve().parents[2]
        self.assertEqual(check_site.audit_source_anchors(root), [])
        self.assertEqual(check_site.audit_sources(root), [])


class FeatureGeneratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tools = generate_features.load_registry()
        cls.toolsets = generate_features.load_toolsets()
        cls.capabilities = generate_features.load_capabilities()
        cls.site = generate_features.Site(cls.tools, cls.toolsets, cls.capabilities)
        cls.by_name = {tool["name"]: tool for tool in cls.tools}

    def tool_page(self, name):
        return generate_features.tool_page(self.site, self.by_name[name])

    def test_every_registry_tool_is_grouped_once(self):
        self.assertEqual(len(self.site.group_of), len(self.tools))
        self.assertEqual(
            sum(
                len(members) for _, groups in self.site.rows for _, _, members in groups
            ),
            len(self.tools),
        )

    def test_every_tool_page_carries_its_registry_description(self):
        for tool in self.tools:
            with self.subTest(tool=tool["name"]):
                rendered = generate_features.tool_page(self.site, tool)
                self.assertTrue(rendered.startswith(f"# {self.site.title(tool)}"))
                self.assertIn("## Behavior and returned data", rendered)
                description = generate_features.normalize_block(tool["description"])
                self.assertIn(description.split("\n\n")[0], rendered)

    def test_fork_action_carries_the_gate_admonition(self):
        rendered = self.tool_page("revit_create_floor")
        self.assertIn("Runs only on a read-write workstation", rendered)
        self.assertIn("read-only", rendered)
        self.assertIn("**Since:** 1.0.0", rendered)
        self.assertIn("```text", rendered)

    def test_fork_read_does_not_carry_the_gate_admonition(self):
        rendered = self.tool_page("revit_export_element_ids")
        self.assertNotIn("Runs only on a read-write workstation", rendered)
        self.assertIn("**Since:** 1.0.0", rendered)

    def test_inherited_tool_does_not_claim_fork_authorship(self):
        rendered = self.tool_page("revit_ping")
        self.assertNotIn("This fork adds this tool", rendered)
        self.assertNotIn("**Since:**", rendered)

    def test_required_nullable_parameter_is_not_optional(self):
        rows = generate_features.parameter_rows(
            self.site, self.by_name["revit_place_family"]
        )
        row = next(item for item in rows if item["name"] == "type_name")
        self.assertTrue(row["required"])
        self.assertEqual(row["type"], "string / null")
        self.assertEqual(row["default"], "—")

    def test_tool_without_own_parameters_states_it(self):
        rendered = self.tool_page("revit_list_instances")
        self.assertIn("This tool takes no parameters of its own.", rendered)
        self.assertIn("### Common parameters", rendered)

    def test_undocumented_parameter_meaning_falls_back_to_a_dash(self):
        self.assertEqual(
            generate_features.parameter_meaning(
                self.site,
                self.by_name["revit_ping"],
                "undocumented",
                {"type": "string"},
            ),
            "—",
        )

    def test_description_block_indent_is_normalized(self):
        text = "Lead sentence.\n\n        A continuation the registry indents.\n        And another."
        self.assertEqual(
            generate_features.normalize_block(text),
            "Lead sentence.\n\nA continuation the registry indents.\nAnd another.",
        )

    def test_regenerated_navigation_covers_each_tool_once(self):
        nav = "\n".join(generate_features.nav_block(self.site))
        for tool in self.tools:
            self.assertEqual(nav.count(f"features/{tool['name']}.md"), 1)
        for page in ("index", "matrix", "prompts", "v2020", "v2026"):
            self.assertEqual(nav.count(f"features/{page}.md"), 1)

    def test_capabilities_must_describe_exactly_the_fork_tools(self):
        capabilities = deepcopy(self.capabilities)
        capabilities["tools"]["revit_ping"] = capabilities["tools"][
            "revit_create_floor"
        ]
        with self.assertRaisesRegex(SystemExit, "must describe exactly these tools"):
            generate_features.Site(self.tools, self.toolsets, capabilities)

    def test_undeclared_group_fails_closed(self):
        capabilities = deepcopy(self.capabilities)
        capabilities["tools"]["revit_create_floor"]["group"] = "nowhere"
        with self.assertRaisesRegex(SystemExit, "undeclared groups"):
            generate_features.Site(self.tools, self.toolsets, capabilities)

    def test_unlabelled_toolset_fails_closed(self):
        labels = dict(generate_features.TOOLSET_LABELS)
        labels.pop(next(iter(labels)))
        with (
            patch.object(generate_features, "TOOLSET_LABELS", labels),
            self.assertRaisesRegex(SystemExit, "no label for"),
        ):
            generate_features.Site(self.tools, self.toolsets, self.capabilities)

    def test_tool_no_toolset_declares_fails_closed(self):
        toolsets = {key: tuple(members) for key, members in self.toolsets.items()}
        first = next(iter(toolsets))
        toolsets[first] = toolsets[first][1:]
        with self.assertRaisesRegex(SystemExit, "tools no toolset declares"):
            generate_features.Site(self.tools, toolsets, self.capabilities)

    def test_tool_in_two_toolsets_fails_closed(self):
        toolsets = {key: tuple(members) for key, members in self.toolsets.items()}
        first, second = list(toolsets)[:2]
        toolsets[second] = toolsets[second] + (toolsets[first][0],)
        with self.assertRaisesRegex(SystemExit, "grouped twice or not at all"):
            generate_features.Site(self.tools, toolsets, self.capabilities)

    def test_year_pages_state_the_truth_on_this_base(self):
        page_2020 = generate_features.year_page(self.site, "2020")
        self.assertIn("Revit 2020 is not supported yet.", page_2020)
        self.assertIn("adr/0006", page_2020)
        page_2026 = generate_features.year_page(self.site, "2026")
        self.assertIn("verified against a running Revit 2026", page_2026)
        self.assertNotIn("Validated live", page_2020 + page_2026)

    def test_generated_pages_are_current(self):
        stale = [
            path.relative_to(generate_features.ROOT).as_posix()
            for path, text in generate_features.render_all().items()
            if not path.is_file() or path.read_text(encoding="utf-8") != text
        ]
        self.assertEqual(stale, [])


if __name__ == "__main__":
    unittest.main()
