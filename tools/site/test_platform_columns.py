"""The Meaning column of a platform parameter table stays honest about missing text.

The integration-branch contract ships no description for many branch-only parameters, so
the fallback that renders the Meaning/说明 cell finds nothing. These tests pin the rule
that keeps the generated pages readable without inventing descriptions:

  * no row of a table has a meaning: the column is dropped and one line under the
    table says that the branch contract ships no parameter descriptions;
  * only some rows have one: the column stays and undocumented rows render the
    meaning-missing placeholder instead of an empty cell.
"""

import unittest

import platform_catalog


def _tool(properties: dict) -> dict:
    return {"name": "revit_probe", "inputSchema": {"properties": properties}}


def _cells(row: str) -> list[str]:
    return [cell.strip() for cell in row.strip().strip("|").split("|")]


class UndocumentedTableTests(unittest.TestCase):
    """A table where no row has a meaning drops the column and says so."""

    def test_the_column_is_dropped_and_the_note_follows_the_table(self):
        tool = _tool({"type_name": {"type": "string"}})
        for lang, note in (
            ("zh", "集成分支契约未提供参数说明。"),
            ("en", "The branch contract ships no parameter descriptions."),
        ):
            with self.subTest(lang=lang):
                rows, has_meaning = platform_catalog._parameter_rows(tool, False, lang)
                self.assertFalse(has_meaning)
                lines = platform_catalog.parameter_table(lang, rows, has_meaning)
                heading = next(
                    line
                    for line in lines
                    if line.startswith(("| 参数 ", "| Parameter "))
                )
                self.assertNotIn(platform_catalog.LABELS[lang]["meaning"], heading)
                self.assertEqual(heading.count("{scope=col}"), 4)
                separator = lines[lines.index(heading) + 1]
                self.assertEqual(_cells(separator), ["---", ":--:", "---", "---"])
                self.assertEqual(lines[-1], note)
                self.assertEqual(lines[lines.index("</div>") + 2], note)

    def test_the_note_wording_is_the_one_the_issue_specifies(self):
        self.assertEqual(
            platform_catalog.LABELS["zh"]["meaning_missing_note"],
            "集成分支契约未提供参数说明。",
        )
        self.assertEqual(
            platform_catalog.LABELS["en"]["meaning_missing_note"],
            "The branch contract ships no parameter descriptions.",
        )


class PartlyDocumentedTableTests(unittest.TestCase):
    """A table with at least one meaning keeps the column and fills the gaps."""

    def setUp(self):
        self.tool = _tool(
            {
                "output_path": {
                    "type": "string",
                    "description": "Where to write the report.",
                },
                "type_name": {"type": "string"},
            }
        )

    def test_the_column_stays_and_undocumented_rows_use_the_placeholder(self):
        for lang in ("zh", "en"):
            with self.subTest(lang=lang):
                labels = platform_catalog.LABELS[lang]
                rows, has_meaning = platform_catalog._parameter_rows(
                    self.tool, False, lang
                )
                self.assertTrue(has_meaning)
                self.assertEqual(len(rows), 2)
                documented, undocumented = rows
                self.assertEqual(_cells(documented)[-1], "Where to write the report.")
                self.assertEqual(_cells(undocumented)[-1], labels["meaning_missing"])
                self.assertNotEqual(_cells(undocumented)[-1], "")
                heading = platform_catalog.table_heading(lang, with_meaning=True)
                self.assertIn(labels["meaning"], heading[0])
                self.assertEqual(heading[0].count("{scope=col}"), 5)

    def test_the_kept_table_carries_no_note_line(self):
        rows, has_meaning = platform_catalog._parameter_rows(self.tool, False, "en")
        lines = platform_catalog.parameter_table("en", rows, has_meaning)
        self.assertNotIn(platform_catalog.LABELS["en"]["meaning_missing_note"], lines)


class GeneratedPageTests(unittest.TestCase):
    """The whole generated platform catalog honours the rule."""

    def setUp(self):
        self.tools, self.released = platform_catalog.load_platform()
        self.by_name = {tool["name"]: tool for tool in self.tools}

    def test_no_generated_page_renders_an_empty_meaning_cell(self):
        """A five-cell row ends in the meaning; a four-cell row dropped the column.

        A schema can still render an empty Type cell (a ``$ref`` property has no inline
        type), which predates this rule and stays out of scope: such a row is only legal
        as a four-cell row whose meaning cell was dropped.
        """
        for path, content in platform_catalog.generate().items():
            with self.subTest(path=path.name):
                for line in content.splitlines():
                    if not line.startswith("| `"):
                        continue
                    cells = _cells(line)
                    self.assertIn(len(cells), (4, 5), line)
                    if len(cells) == 5:
                        self.assertTrue(cells[-1], line)

    def test_every_row_matches_its_heading_width(self):
        for tool in self.tools:
            for common in (False, True):
                for lang in ("zh", "en"):
                    with self.subTest(tool=tool["name"], common=common, lang=lang):
                        rows, has_meaning = platform_catalog._parameter_rows(
                            tool, common, lang
                        )
                        heading = platform_catalog.table_heading(
                            lang, with_meaning=has_meaning
                        )
                        width = heading[0].count("{scope=col}")
                        self.assertEqual(width, 5 if has_meaning else 4)
                        for row in rows:
                            self.assertEqual(len(_cells(row)), width, row)
                            if width == 5:
                                self.assertTrue(_cells(row)[-1], row)

    def test_a_page_may_decide_per_table(self):
        """revit_change_type drops the column in the main table but keeps the common one."""
        page = platform_catalog.tool_page(
            self.by_name["revit_change_type"], self.released, "en"
        )
        self.assertEqual(page.count("| Meaning {scope=col} |"), 1)
        self.assertEqual(
            page.count(platform_catalog.LABELS["en"]["meaning_missing_note"]),
            1,
        )

    def test_the_chinese_page_keeps_the_column_when_it_has_hand_written_meanings(self):
        page = platform_catalog.tool_page(
            self.by_name["revit_change_type"], self.released, "zh"
        )
        self.assertGreaterEqual(page.count("| 说明 {scope=col} |"), 1)
        self.assertNotIn(platform_catalog.LABELS["zh"]["meaning_missing_note"], page)
        self.assertIn(platform_catalog.LABELS["zh"]["meaning_missing"], page)


if __name__ == "__main__":
    unittest.main()
