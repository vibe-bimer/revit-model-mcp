"""Every tool must be named in all four surfaces, or it is unreachable in some build.

A tool that exists in ``server.py``/``actions.py`` but not in ``bundle/manifest.json``
is invisible to bundle clients; a wire command the Python side sends but
``ActionJobParser.IsAction`` rejects fails at runtime, after the user asked for it.
These checks are cheap and catch the drift that grafted tools are prone to.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
REPO_ROOT = TEST_DIR.parent.parent
SYNC_MODULE = REPO_ROOT / "tools" / "sync_manifest_tools.py"


def _load_sync_module():
    spec = importlib.util.spec_from_file_location("sync_manifest_tools", SYNC_MODULE)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


sync = _load_sync_module()


def test_manifest_lists_every_registered_tool():
    read = set(sync.read_tools())
    actions = set(sync.action_tools())
    listed = set(sync.manifest_tool_names())
    assert listed == read | actions, (
        f"bundle/manifest.json is out of step; missing={sorted((read | actions) - listed)} "
        f"extra={sorted(listed - (read | actions))}. "
        "Run `python tools/sync_manifest_tools.py`."
    )


def test_manifest_entries_are_ordered_read_tools_first():
    listed = sync.manifest_tool_names()
    read = list(sync.read_tools())
    assert listed[: len(read)] == read, (
        "read tools must come first in bundle/manifest.json so a bundle client's "
        "read-only surface is listed before any action tool"
    )


def test_every_action_tool_sends_an_accepted_command():
    accepted = sync.action_parser_commands()
    sent = {name: command for name, (command, _d) in sync.action_tools().items()}
    unknown = {name: command for name, command in sent.items() if command not in accepted}
    assert not unknown, (
        f"these action tools send a command ActionJobParser.IsAction rejects: {unknown}; "
        f"accepted={sorted(accepted)}"
    )


def test_every_accepted_command_is_reachable():
    """Each accepted command must be runnable: a Mutate case, or pre-Mutate dispatch."""
    accepted = sync.action_parser_commands()
    cases = sync.mutate_switch_commands()
    pre_mutate = sync.pre_mutate_dispatch_commands()
    unreachable = accepted - cases - pre_mutate
    assert not unreachable, (
        f"ActionJobParser accepts commands nothing can run: {sorted(unreachable)}. "
        "Add the wire command to the Mutate switch, or dispatch it before Mutate."
    )
    assert cases <= accepted, (
        f"the executor has cases for commands ActionJobParser rejects: {sorted(cases - accepted)}"
    )
    assert pre_mutate <= accepted, (
        f"the executor dispatches commands ActionJobParser never accepts: {sorted(pre_mutate - accepted)}"
    )


def test_batch_step_exclusions_are_real_commands():
    excluded = sync.batch_excluded_commands()
    accepted = sync.action_parser_commands()
    assert excluded <= accepted, (
        f"batch excludes names that are not action commands: {sorted(excluded - accepted)}"
    )
    # Two tools cannot run as a step inside a batch: `batch` would recurse, and
    # `show` opens a view. The rebuild family is excluded because each run
    # replaces the document, which no surrounding transaction can survive.
    assert {"show", "batch", "merge-phases", "rebuild-model-ids"} <= excluded, (
        "the documented batch exclusions must stay in ActionJobParser"
    )


def test_action_tool_count_matches_manifest_action_entries():
    actions = sync.action_tools()
    listed = sync.manifest_tool_names()
    action_entries = [name for name in listed if name not in set(sync.read_tools())]
    assert sorted(action_entries) == sorted(actions), (
        f"manifest action entries ({sorted(action_entries)}) do not match registered "
        f"action tools ({sorted(actions)})"
    )
