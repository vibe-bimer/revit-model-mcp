"""Keep the bundle manifest's tool list and the four code surfaces in agreement.

Four places have to name a tool for it to be reachable, and they drift silently:

1. ``server/revit_model_mcp/server.py`` — read tools, ``@addressed_tool``.
2. ``server/revit_model_mcp/actions.py`` — action tools, ``@action`` inside ``register_actions``.
3. ``bundle/manifest.json`` — ``tools[]``, what a bundle client sees.
4. The C# side: ``ActionJobParser.IsAction`` accepts a wire command, and
   ``ActionCommandExecutor.Mutate`` carries a ``case`` for every command it can run.

The parsing helpers below are the single source of truth for those surfaces; the
tests assert agreement and this script rewrites ``tools[]`` when it is behind.

Usage::

    python tools/sync_manifest_tools.py          # rewrite tools[] in place
    python tools/sync_manifest_tools.py --check  # exit 1 when out of date
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SERVER_MODULE_DIR = REPO_ROOT / "server" / "revit_model_mcp"
MANIFEST_PATH = REPO_ROOT / "bundle" / "manifest.json"
ACTION_PARSER_PATH = (
    REPO_ROOT / "src" / "RevitModelMcp.Core" / "Control" / "ActionJobParser.cs"
)
ACTION_EXECUTOR_PATH = (
    REPO_ROOT / "src" / "RevitModelMcp.Addin" / "Control" / "ActionCommandExecutor.cs"
)

# Commands the executor handles before Mutate rather than inside it. Derived from
# the source instead of hand-maintained: `batch` is a container, `select`/`show`
# drive the view, and `rebuild-model-ids` replaces the document so no surrounding
# transaction can hold it.
PRE_MUTATE_COMMANDS = frozenset({"select", "show", "batch", "rebuild-model-ids"})


def _decorator_names(node: ast.FunctionDef | ast.AsyncFunctionDef) -> set[str]:
    names: set[str] = set()
    for decorator in node.decorator_list:
        target = decorator.func if isinstance(decorator, ast.Call) else decorator
        if isinstance(target, ast.Name):
            names.add(target.id)
        elif isinstance(target, ast.Attribute):
            names.add(target.attr)
    return names


def _first_sentence(docstring: str | None) -> str:
    if not docstring:
        return ""
    for line in docstring.strip().splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def _send_command(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str | None:
    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue
        target = child.func
        name = (
            target.id if isinstance(target, ast.Name) else getattr(target, "attr", None)
        )
        if name != "send" or not child.args:
            continue
        first = child.args[0]
        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            return first.value
    return None


def read_tools() -> dict[str, str]:
    """Read tools declared in server.py, mapped to their one-sentence description.

    Two decorator spellings exist: ``@addressed_tool`` for tools that take a
    document reference, and a bare ``@mcp.tool(...)`` for instance listing.
    """
    tree = ast.parse((SERVER_MODULE_DIR / "server.py").read_text(encoding="utf-8"))
    tools: dict[str, str] = {}
    for node in tree.body:
        if not isinstance(node, ast.AsyncFunctionDef) and not isinstance(
            node, ast.FunctionDef
        ):
            continue
        if not node.name.startswith("revit_"):
            continue
        decorators = _decorator_names(node)
        if "addressed_tool" in decorators or "tool" in decorators:
            tools[node.name] = _first_sentence(ast.get_docstring(node))
    return tools


def pre_mutate_dispatch_commands() -> set[str]:
    """Commands the executor handles before Mutate, read from its ``command ==`` tests."""
    source = ACTION_EXECUTOR_PATH.read_text(encoding="utf-8")
    start = source.find("private static ActionResultData Mutate(")
    if start < 0:
        raise AssertionError("ActionCommandExecutor.Mutate not found")
    before = source[:start]
    return set(re.findall(r'(?:job\.)?[Cc]ommand == "([^"]+)"', before))


def action_tools() -> dict[str, tuple[str, str]]:
    """Action tools declared in actions.py, mapped to (wire command, description)."""
    tree = ast.parse((SERVER_MODULE_DIR / "actions.py").read_text(encoding="utf-8"))
    tools: dict[str, tuple[str, str]] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.AsyncFunctionDef) and not isinstance(
            node, ast.FunctionDef
        ):
            continue
        if "action" not in _decorator_names(node):
            continue
        command = _send_command(node)
        if command is None:
            raise AssertionError(
                f"{node.name} has an @action decorator but no send(<command>) call"
            )
        tools[node.name] = (command, _first_sentence(ast.get_docstring(node)))
    return tools


def _quoted_literals(text: str) -> list[str]:
    return re.findall(r'"([^"\\]+)"', text)


def action_parser_commands() -> set[str]:
    """Wire commands accepted by ActionJobParser.IsAction."""
    source = ACTION_PARSER_PATH.read_text(encoding="utf-8")
    match = re.search(
        r"IsAction\(string command\)\s*=>\s*command is\s*(.*?);", source, re.DOTALL
    )
    if match is None:
        raise AssertionError("ActionJobParser.IsAction pattern expression not found")
    return set(_quoted_literals(match.group(1)))


def mutate_switch_commands() -> set[str]:
    """Wire commands the executor's Mutate switch carries a case for."""
    source = ACTION_EXECUTOR_PATH.read_text(encoding="utf-8")
    start = source.find("private static ActionResultData Mutate(")
    if start < 0:
        raise AssertionError("ActionCommandExecutor.Mutate not found")
    end = source.find("private static", start + 1)
    body = source[start : end if end > 0 else len(source)]
    return set(re.findall(r'case\s+"([^"]+)"\s*:', body))


def batch_excluded_commands() -> set[str]:
    """Commands ActionJobParser refuses as a step inside batch."""
    source = ACTION_PARSER_PATH.read_text(encoding="utf-8")
    match = re.search(
        r"IsAction\(stepCommand\) && stepCommand is not \((.*?)\)", source, re.DOTALL
    )
    if match is None:
        return set()
    return set(_quoted_literals(match.group(1)))


def manifest_tool_names() -> list[str]:
    return [
        entry["name"]
        for entry in json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))["tools"]
    ]


def expected_manifest_tools() -> list[dict[str, str]]:
    """Manifest entries for every registered tool, read tools first."""
    entries = [
        {"name": name, "description": description}
        for name, description in read_tools().items()
    ]
    entries.extend(
        {"name": name, "description": description}
        for name, (_command, description) in action_tools().items()
    )
    return entries


def _write(entries: list[dict[str, str]]) -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest["tools"] = entries
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="report drift instead of fixing it"
    )
    args = parser.parse_args(argv)

    expected = expected_manifest_tools()
    current = manifest_tool_names()
    if current == [entry["name"] for entry in expected]:
        print("bundle manifest tools[] is up to date")
        return 0

    missing = [entry["name"] for entry in expected if entry["name"] not in current]
    extra = [
        name for name in current if name not in {entry["name"] for entry in expected}
    ]
    if args.check:
        print(
            f"bundle manifest tools[] is stale: missing={missing} extra={extra}",
            file=sys.stderr,
        )
        return 1
    _write(expected)
    print(f"bundle manifest tools[] updated: missing={missing} extra={extra}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
