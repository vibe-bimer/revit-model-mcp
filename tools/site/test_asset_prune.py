"""Dead lunr theme assets: the build prunes the locale files the search worker cannot load.

Material ships a lunr stemmer for every language it knows. The worker loads one only for a
language the index actually covers, plus a segmenter for Japanese or Hindi/Thai. This site builds
Chinese and English, so every other locale file is dead weight on every deploy. These tests pin
the prune and the keep-set that mirrors the worker.
"""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load_hooks():
    spec = importlib.util.spec_from_file_location(
        "docs_hooks_for_asset_prune_tests", ROOT / "docs/hooks.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_site(directory, languages):
    site = Path(directory)
    (site / "search").mkdir(parents=True)
    (site / "search/search_index.json").write_text(
        json.dumps({"config": {"lang": languages}, "docs": []}), encoding="utf-8"
    )
    lunr = site / "assets/javascripts/lunr"
    (lunr / "min").mkdir(parents=True)
    for name in (
        "min/lunr.zh.min.js",
        "min/lunr.multi.min.js",
        "min/lunr.stemmer.support.min.js",
        "min/lunr.fr.min.js",
        "min/lunr.ja.min.js",
        "min/lunr.de.min.js",
    ):
        (lunr / name).write_text(f"// {name}\n", encoding="utf-8")
    (lunr / "tinyseg.js").write_text("// tinyseg\n", encoding="utf-8")
    (lunr / "wordcut.js").write_text("// wordcut\n", encoding="utf-8")
    return site, lunr


def remaining(lunr):
    return sorted(p.relative_to(lunr).as_posix() for p in lunr.rglob("*.js"))


class KeepSetTests(unittest.TestCase):
    def test_an_english_and_chinese_index_keeps_its_stemmer_and_support(self):
        hooks = load_hooks()
        self.assertEqual(
            hooks.search_worker_assets(["en", "zh"]),
            {
                "min/lunr.zh.min.js",
                "min/lunr.multi.min.js",
                "min/lunr.stemmer.support.min.js",
            },
        )

    def test_a_japanese_index_keeps_the_tinyseg_segmenter(self):
        hooks = load_hooks()
        self.assertIn("tinyseg.js", hooks.search_worker_assets(["ja", "en"]))

    def test_a_hindi_or_thai_index_keeps_the_wordcut_segmenter(self):
        hooks = load_hooks()
        self.assertIn("wordcut.js", hooks.search_worker_assets(["hi", "en"]))
        self.assertIn("wordcut.js", hooks.search_worker_assets(["th", "en"]))

    def test_an_english_only_index_loads_no_extra_files(self):
        hooks = load_hooks()
        self.assertEqual(hooks.search_worker_assets(["en"]), set())


class PruneTests(unittest.TestCase):
    def test_pruning_leaves_only_what_the_worker_can_load(self):
        with tempfile.TemporaryDirectory() as directory:
            site, lunr = make_site(directory, ["en", "zh"])
            removed = load_hooks().prune_search_assets(site)
            names = remaining(lunr)
        self.assertGreater(removed, 0)
        self.assertEqual(
            names,
            [
                "min/lunr.multi.min.js",
                "min/lunr.stemmer.support.min.js",
                "min/lunr.zh.min.js",
            ],
        )

    def test_pruning_removes_the_segmenters_for_a_language_the_site_lacks(self):
        with tempfile.TemporaryDirectory() as directory:
            site, lunr = make_site(directory, ["en", "zh"])
            load_hooks().prune_search_assets(site)
            names = remaining(lunr)
        self.assertNotIn("tinyseg.js", names)
        self.assertNotIn("wordcut.js", names)
        self.assertNotIn("min/lunr.ja.min.js", names)

    def test_pruning_keeps_the_segmenter_a_japanese_index_needs(self):
        with tempfile.TemporaryDirectory() as directory:
            site, lunr = make_site(directory, ["ja", "en"])
            load_hooks().prune_search_assets(site)
            names = remaining(lunr)
        self.assertIn("tinyseg.js", names)
        self.assertIn("min/lunr.ja.min.js", names)
        self.assertNotIn("wordcut.js", names)

    def test_an_empty_directory_left_by_pruning_is_removed(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "search").mkdir()
            (site / "search/search_index.json").write_text(
                json.dumps({"config": {"lang": ["en", "zh"]}, "docs": []}),
                encoding="utf-8",
            )
            extra = site / "assets/javascripts/lunr/locale"
            extra.mkdir(parents=True)
            (extra / "lunr.fr.min.js").write_text("// fr\n", encoding="utf-8")
            (site / "assets/javascripts/lunr/min").mkdir()
            (site / "assets/javascripts/lunr/min/lunr.zh.min.js").write_text(
                "// zh\n", encoding="utf-8"
            )
            (site / "assets/javascripts/lunr/min/lunr.multi.min.js").write_text(
                "// multi\n", encoding="utf-8"
            )
            (
                site / "assets/javascripts/lunr/min/lunr.stemmer.support.min.js"
            ).write_text("// support\n", encoding="utf-8")
            load_hooks().prune_search_assets(site)
            self.assertFalse(extra.exists())

    def test_pruning_skips_a_site_with_no_index(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "assets/javascripts/lunr").mkdir(parents=True)
            (site / "assets/javascripts/lunr/tinyseg.js").write_text(
                "// t\n", encoding="utf-8"
            )
            removed = load_hooks().prune_search_assets(site)
            self.assertEqual(removed, 0)
            self.assertTrue((site / "assets/javascripts/lunr/tinyseg.js").is_file())

    def test_the_real_worker_bundle_names_the_files_the_keep_set_mirrors(self):
        # Cross-check the mirror against the shipped worker when a build is present.
        workers = list(
            (ROOT / "site/assets/javascripts/workers").glob("search.*.min.js")
        )
        if not workers:
            self.skipTest("no built worker bundle to check")
        source = workers[0].read_text(encoding="utf-8", errors="replace")
        for fragment in ("tinyseg.js", "wordcut.js", "min/lunr."):
            self.assertIn(fragment, source)


if __name__ == "__main__":
    unittest.main()
