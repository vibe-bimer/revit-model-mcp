"""Tests for the capability translation freshness gate.

capabilities.yaml holds the reviewed Chinese text for every tool. The English description in
tools.json is the source that text translates, so a description edit silently leaves the
translation behind. Each entry records a short fingerprint of the description it was written
from; these tests pin the three states that matter: matching, stale and absent.
"""

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import generate_features
import yaml

DESCRIPTION = "Report the parameters of the selected elements"
DERIVE = object()


def source_of(description: str) -> str:
    return hashlib.sha256(description.encode()).hexdigest()[:12]


def tool_payload(description: str = DESCRIPTION) -> list[dict]:
    return [
        {
            "name": "revit_probe",
            "description": description,
            "inputSchema": {
                "type": "object",
                "properties": {
                    "element_ids": {"type": "array", "description": "Element ids"},
                },
            },
        }
    ]


def capability_payload(source: str | None | object = DERIVE) -> dict:
    entry = {
        "group": "query",
        "since": "0.1.0",
        "title": {"zh": "探测", "en": "Probe"},
        "summary": {"zh": "读取构件参数", "en": "Read element parameters"},
        "years": {"other": {"state": "built"}},
        "prompts": [{"zh": "探测一下", "en": "Probe it"}],
    }
    if source is DERIVE:
        source = source_of(DESCRIPTION)
    if source is not None:
        entry["source"] = source
    return {
        "groups": {"query": {"zh": "查询", "en": "Query"}},
        "tools": {"revit_probe": entry},
        "param_notes": {"revit_probe": {"element_ids": {"zh": "构件 ID"}}},
    }


def contract_payload(description: str = DESCRIPTION) -> dict:
    return {
        "tools": {
            "revit_probe": {
                "zh": "读取构件参数。",
                "source": hashlib.sha256(description.encode()).hexdigest(),
            }
        }
    }


class FixtureCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.tools = self.root / "tools.json"
        self.capabilities = self.root / "capabilities.yaml"
        self.contracts = self.root / "contracts.yaml"
        self.saved = (
            generate_features.TOOLS_JSON,
            generate_features.CAPABILITIES,
            generate_features.CONTRACTS,
        )
        self.addCleanup(self.restore)
        generate_features.TOOLS_JSON = self.tools
        generate_features.CAPABILITIES = self.capabilities
        generate_features.CONTRACTS = self.contracts

    def restore(self):
        (
            generate_features.TOOLS_JSON,
            generate_features.CAPABILITIES,
            generate_features.CONTRACTS,
        ) = self.saved

    def write(self, description=DESCRIPTION, source=DERIVE, text=None):
        if source is DERIVE:
            source = source_of(description)
        self.tools.write_text(json.dumps(tool_payload(description)), encoding="utf-8")
        if text is None:
            text = yaml.safe_dump(
                capability_payload(source), allow_unicode=True, sort_keys=False
            )
        self.capabilities.write_text(text, encoding="utf-8")
        self.contracts.write_text(
            yaml.safe_dump(
                contract_payload(description), allow_unicode=True, sort_keys=False
            ),
            encoding="utf-8",
        )


class FreshnessGateTests(FixtureCase):
    def test_a_matching_source_loads(self):
        self.write()
        tools, _, _ = generate_features.load()
        self.assertEqual([tool["name"] for tool in tools], ["revit_probe"])

    def test_a_changed_english_description_fails_the_old_fingerprint(self):
        self.write(
            description=DESCRIPTION + " and their worksets",
            source=source_of(DESCRIPTION),
        )
        with self.assertRaises(SystemExit) as caught:
            generate_features.load()
        message = str(caught.exception)
        self.assertIn("revit_probe", message)
        self.assertIn("--refresh-sources", message)

    def test_a_missing_fingerprint_fails(self):
        self.write(source=None)
        with self.assertRaises(SystemExit) as caught:
            generate_features.load()
        self.assertIn("revit_probe", str(caught.exception))

    def test_the_fingerprint_is_twelve_hex_characters(self):
        self.assertEqual(len(source_of(DESCRIPTION)), 12)
        self.assertTrue(
            all(char in "0123456789abcdef" for char in source_of(DESCRIPTION))
        )


class RefreshTests(FixtureCase):
    def test_refresh_writes_the_current_fingerprint(self):
        self.write(description=DESCRIPTION + " and their worksets", source="0" * 12)
        generate_features.refresh_capability_sources(
            tool_payload(DESCRIPTION + " and their worksets")
        )
        capabilities = yaml.safe_load(self.capabilities.read_text(encoding="utf-8"))
        self.assertEqual(
            capabilities["tools"]["revit_probe"]["source"],
            source_of(DESCRIPTION + " and their worksets"),
        )

    def test_refresh_adds_a_missing_fingerprint_and_keeps_comments(self):
        body = (
            "# hand-written comments survive a refresh\n"
            "tools:\n"
            "  revit_probe:\n"
            "    group: query\n"
            "    title:\n"
            "      zh: 探测\n"
            "      en: Probe\n"
        )
        self.write(source=None, text=body)
        changed = generate_features.refresh_capability_sources(tool_payload())
        self.assertEqual(changed, 1)
        text = self.capabilities.read_text(encoding="utf-8")
        self.assertIn("# hand-written comments survive a refresh", text)
        self.assertIn(f"    source: '{source_of(DESCRIPTION)}'", text)
        self.assertEqual(text.count("source:"), 1)


class CommittedBaselineTests(unittest.TestCase):
    def test_every_capability_entry_records_its_source_fingerprint(self):
        tools = json.loads(generate_features.TOOLS_JSON.read_text(encoding="utf-8"))
        capabilities = yaml.safe_load(
            generate_features.CAPABILITIES.read_text(encoding="utf-8")
        )
        for tool in tools:
            with self.subTest(tool=tool["name"]):
                self.assertEqual(
                    capabilities["tools"][tool["name"]].get("source"),
                    source_of(tool["description"]),
                )


class ServerCommandTests(unittest.TestCase):
    """The registry dump must find the server in a checkout, in CI and in a branch worktree."""

    def test_module_form_is_the_last_resort(self):
        with mock.patch.object(generate_features.shutil, "which", return_value=None):
            candidates = generate_features.server_command_candidates()
        self.assertEqual(candidates[-1], [sys.executable, "-m", "revit_model_mcp"])

    def test_checkout_environment_is_preferred(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            executable = root / "server/.venv/bin/revit-model-mcp"
            executable.parent.mkdir(parents=True)
            executable.write_text("#!/bin/sh\n", encoding="utf-8")
            with (
                mock.patch.object(generate_features, "ROOT", root),
                mock.patch.object(generate_features.shutil, "which", return_value=None),
            ):
                candidates = generate_features.server_command_candidates()
        self.assertEqual(candidates[0], [str(executable)])

    def test_installed_console_script_ranks_before_the_module_form(self):
        with mock.patch.object(
            generate_features.shutil, "which", return_value="/usr/bin/revit-model-mcp"
        ):
            candidates = generate_features.server_command_candidates()
        self.assertIn(["/usr/bin/revit-model-mcp"], candidates)
        self.assertLess(
            candidates.index(["/usr/bin/revit-model-mcp"]),
            len(candidates) - 1,
        )

    def test_worktree_prefers_its_own_environment(self):
        with tempfile.TemporaryDirectory() as directory:
            server = Path(directory) / "server"
            executable = server / ".venv/bin/revit-model-mcp"
            executable.parent.mkdir(parents=True)
            executable.write_text("#!/bin/sh\n", encoding="utf-8")
            with mock.patch.object(
                generate_features.shutil, "which", return_value=None
            ):
                candidates = generate_features.worktree_command_candidates(server)
        self.assertEqual(candidates[0], [str(executable)])
        self.assertEqual(candidates[-1], [sys.executable, "-m", "revit_model_mcp"])
