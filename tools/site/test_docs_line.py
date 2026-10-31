"""Tests for the documentation line gate."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import check_docs_line


class DocumentationLineTests(unittest.TestCase):
    def test_every_required_file_exists_in_the_repository(self) -> None:
        missing = check_docs_line.missing_files(check_docs_line.repository_root())
        self.assertEqual([], missing)

    def test_the_repository_carries_every_tool_page(self) -> None:
        root = check_docs_line.repository_root()
        for section, floor in check_docs_line.MINIMUM_TOOL_PAGES:
            with self.subTest(section=section):
                self.assertGreaterEqual(
                    check_docs_line.tool_page_count(root, section), floor
                )

    def test_the_check_passes_for_the_repository(self) -> None:
        self.assertEqual([], check_docs_line.check(check_docs_line.repository_root()))

    def test_a_missing_file_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            problems = check_docs_line.check(root)
            self.assertTrue(
                any("missing mkdocs-lan.yml" in problem for problem in problems)
            )

    def test_a_short_tool_section_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            section = root / "docs/features"
            section.mkdir(parents=True)
            (section / "revit_ping.md").write_text("# ping\n", encoding="utf-8")
            problems = check_docs_line.check(root)
            self.assertTrue(
                any("docs/features has 1 tool pages" in problem for problem in problems)
            )

    def test_the_english_twins_do_not_count_as_tool_pages(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            section = root / "docs/features"
            section.mkdir(parents=True)
            (section / "revit_ping.md").write_text("# ping\n", encoding="utf-8")
            (section / "revit_ping.en.md").write_text("# ping\n", encoding="utf-8")
            self.assertEqual(1, check_docs_line.tool_page_count(root, "docs/features"))

    def test_main_returns_one_for_an_incomplete_tree(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(1, check_docs_line.main(["--root", directory]))

    def test_main_returns_zero_for_the_repository(self) -> None:
        self.assertEqual(0, check_docs_line.main([]))


if __name__ == "__main__":
    unittest.main()
