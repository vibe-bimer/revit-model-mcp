"""Search index slimming: the per-entry text cap and the leaner annotation payload.

The search plugin indexes the whole page body, and Material's worker downloads the entire file
before the search box answers a keystroke. These tests pin the two reductions the build applies:
a prefix cap on each entry's text, and a smaller annotation block, while every parameter name a
tool accepts stays findable.
"""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

import platform_catalog

ROOT = Path(__file__).resolve().parents[2]


def load_hooks():
    spec = importlib.util.spec_from_file_location(
        "docs_hooks_for_search_index_tests", ROOT / "docs/hooks.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def enriched(site, docs, config=None):
    """Write an index, run the annotation, and return the parsed result."""
    hooks = load_hooks()
    (site / "search").mkdir(parents=True, exist_ok=True)
    payload = {"config": config or {"lang": ["en", "zh"]}, "docs": docs}
    index = site / "search/search_index.json"
    index.write_text(json.dumps(payload), encoding="utf-8")
    hooks.enrich_search_index(site)
    return json.loads(index.read_text(encoding="utf-8")), hooks


class TextCapTests(unittest.TestCase):
    def test_a_long_text_is_cut_to_the_limit(self):
        long_entry = "x" * 5000
        with tempfile.TemporaryDirectory() as directory:
            data, hooks = enriched(
                Path(directory),
                [
                    {
                        "location": "manual-test-plan/",
                        "title": "Plan",
                        "text": long_entry,
                    }
                ],
            )
        text = data["docs"][0]["text"]
        self.assertEqual(len(text), hooks.SEARCH_TEXT_LIMIT)
        self.assertEqual(text, "x" * hooks.SEARCH_TEXT_LIMIT)

    def test_a_short_text_is_left_alone(self):
        with tempfile.TemporaryDirectory() as directory:
            data, _ = enriched(
                Path(directory),
                [
                    {
                        "location": "manual-test-plan/",
                        "title": "Plan",
                        "text": "short body",
                    }
                ],
            )
        self.assertEqual(data["docs"][0]["text"], "short body")

    def test_the_cap_keeps_an_early_token_and_drops_a_late_one(self):
        # A token inside the limit survives; one past it leaves this entry. Another entry that
        # indexes the late token still answers for it, which is how a parameter deep in one table
        # stays searchable through a shorter entry.
        limit = load_hooks().SEARCH_TEXT_LIMIT
        body = "a" * 100 + " early_token " + "b" * 2000 + " late_token"
        with tempfile.TemporaryDirectory() as directory:
            data, _ = enriched(
                Path(directory),
                [
                    {"location": "long/", "title": "Long", "text": body},
                    {"location": "short/", "title": "Short", "text": "late_token only"},
                ],
            )
        long_text = next(d for d in data["docs"] if d["location"] == "long/")["text"]
        self.assertLessEqual(len(long_text), limit)
        self.assertIn("early_token", long_text)
        self.assertNotIn("late_token", long_text)
        self.assertTrue(any("late_token" in d["text"] for d in data["docs"]))

    def test_capping_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            hooks = load_hooks()
            (site / "search").mkdir()
            index = site / "search/search_index.json"
            index.write_text(
                json.dumps(
                    {
                        "config": {"lang": ["en", "zh"]},
                        "docs": [
                            {"location": "x/", "title": "X", "text": "y" * 3000},
                        ],
                    }
                ),
                encoding="utf-8",
            )
            hooks.enrich_search_index(site)
            first = index.read_text()
            hooks.enrich_search_index(site)
            self.assertEqual(first, index.read_text())


class AnnotationSlimmingTests(unittest.TestCase):
    def test_a_release_entry_keeps_its_version_but_drops_the_default_branch(self):
        with tempfile.TemporaryDirectory() as directory:
            data, _ = enriched(
                Path(directory),
                [
                    {
                        "location": "features/revit_export_view/",
                        "title": "导出视图",
                        "text": "已发布 0.9.0",
                    }
                ],
            )
        doc = data["docs"][0]
        self.assertEqual(doc["status"], "released")
        self.assertIn("version", doc)
        self.assertNotIn("branch", doc)

    def test_a_branch_entry_keeps_the_branch_but_stores_no_empty_version(self):
        with tempfile.TemporaryDirectory() as directory:
            data, _ = enriched(
                Path(directory),
                [
                    {
                        "location": "platform/revit_export_view/",
                        "title": "导出视图",
                        "text": "未发布",
                    }
                ],
            )
        doc = data["docs"][0]
        self.assertEqual(doc["status"], "unreleased")
        self.assertEqual(doc["branch"], platform_catalog.BRANCH)
        self.assertNotIn("version", doc)

    def test_a_plain_entry_carries_only_language_and_a_null_tool(self):
        with tempfile.TemporaryDirectory() as directory:
            data, _ = enriched(
                Path(directory),
                [{"location": "", "title": "Home", "text": "home"}],
            )
        doc = data["docs"][0]
        self.assertEqual(doc["lang"], "zh")
        self.assertIsNone(doc["tool"])
        self.assertEqual(set(doc), {"location", "title", "text", "lang", "tool"})


class ParameterBudgetTests(unittest.TestCase):
    """Against a real build, prove the cap loses no tool parameter name.

    The cap is only safe if every parameter name a tool accepts still appears in at least one
    entry's text. The real index is copied into a temp site and re-enriched, so the check proves
    the shipped pipeline on real page text whatever state the ambient build happens to be in. It
    skips in a bare checkout with no build.
    """

    INDEX = ROOT / "site/search/search_index.json"

    def parameter_names(self):
        import generate_features

        names = set()
        for tool in generate_features.load()[0]:
            names.update((tool.get("inputSchema") or {}).get("properties", {}))
        for tool in platform_catalog.load_platform()[0]:
            names.update((tool.get("inputSchema") or {}).get("properties", {}))
        return names

    def rebuilt(self):
        if not self.INDEX.is_file():
            self.skipTest("no built search index to check")
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "search").mkdir()
            index = json.loads(self.INDEX.read_text(encoding="utf-8"))
            # A stale index was truncated by an older cap; its lost text is unrecoverable, so the
            # check must run on an index the current code produced (a fresh build).
            if index.get("rmc_text_limit") != load_hooks().SEARCH_TEXT_LIMIT:
                self.skipTest(
                    "ambient index predates the current text cap; rebuild first"
                )
            (site / "search/search_index.json").write_text(
                self.INDEX.read_text(encoding="utf-8"), encoding="utf-8"
            )
            hooks = load_hooks()
            hooks.enrich_search_index(site)
            return json.loads((site / "search/search_index.json").read_text("utf-8"))

    def test_every_parameter_name_survives_in_some_entry(self):
        data = self.rebuilt()
        texts = [doc.get("text", "") for doc in data["docs"]]
        missing = sorted(
            name
            for name in self.parameter_names()
            if not any(name in text for text in texts)
        )
        self.assertEqual(missing, [])

    def test_every_entry_text_is_within_the_limit(self):
        limit = load_hooks().SEARCH_TEXT_LIMIT
        data = self.rebuilt()
        over = [
            len(doc.get("text", ""))
            for doc in data["docs"]
            if len(doc.get("text", "")) > limit
        ]
        self.assertEqual(over, [])


if __name__ == "__main__":
    unittest.main()
