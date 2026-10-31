"""Fail when the fork layer grows past what it is allowed to touch.

The layer is a bounded set of edits to upstream's own files plus code of its own. The bound is what makes a
rebase predictable, so it is measured rather than trusted: this check counts the changed lines in the dispatch
hooks against the base commit, and fails when a changed file is neither a hook, a known read side effect, nor
fork code.

Exit codes: 0 inside the bound, 1 outside it, 2 the check could not run.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = Path(__file__).resolve().parent / "fork.json"


def load_config(path: Path = CONFIG_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def classify(path: str, config: dict) -> str:
    """Say which rule a changed file answers to: fork, hook, read or unowned."""
    if any(path.startswith(prefix) for prefix in config["forkPaths"]):
        return "fork"
    if path in config["hooks"]:
        return "hook"
    if path in config["reads"]:
        return "read"
    if path in config.get("removed", {}):
        return "removed"
    return "unowned"


def changed_lines(
    numstat: str, config: dict
) -> tuple[dict[str, int], dict[str, int], list[str]]:
    """Split a `git diff --numstat` into hook changes, other changes and files no rule owns."""
    hooks: dict[str, int] = {}
    other: dict[str, int] = {}
    removed: list[str] = []
    unowned: list[str] = []
    for line in numstat.splitlines():
        if not line.strip():
            continue
        added, deleted, path = line.split("\t", 2)
        path = path.split("\t")[-1]
        if added == "-":
            # A binary file: counted by name, not by lines.
            added, deleted = "0", "0"
        kind = classify(path, config)
        if kind == "unowned":
            unowned.append(path)
        elif kind == "hook":
            hooks[path] = int(added) + int(deleted)
        elif kind == "removed":
            # A removal is a deliberate act, not a silent read: it is asserted below instead of counted.
            removed.append(path)
        elif kind != "fork":
            other[path] = int(added) + int(deleted)
    return hooks, other, unowned, removed


def numstat(base: str, repository_root: Path = REPOSITORY_ROOT) -> str:
    result = subprocess.run(
        # --no-renames keeps the split free of `a/{old => new}/b` path artifacts.
        ["git", "diff", "--numstat", "--no-renames", f"{base}...HEAD"],
        cwd=repository_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(f"git diff failed against {base}: {result.stderr.strip()}")
    return result.stdout


def main() -> int:
    config = load_config()
    base = config["base"]
    hooks, other, unowned, removed = changed_lines(numstat(base), config)
    budget = config["hookBudgetLines"]
    spent = sum(hooks.values())

    for path, lines in sorted(hooks.items()):
        print(f"hook  {path}: {lines} changed lines")
    for path, lines in sorted(other.items()):
        print(f"read  {path}: {lines} changed lines ({config['reads'][path]})")
    print(f"hook budget: {spent} of {budget} changed lines across {len(hooks)} hooks")

    failed = False
    if spent > budget:
        print(f"FAIL the hooks spend {spent} lines of a {budget}-line budget")
        failed = True
    for path in sorted(removed):
        print(f"removed  {path}: {config['removed'][path]}")
    for path in sorted(config.get("removed", {})):
        if (REPOSITORY_ROOT / path).exists():
            print(f"FAIL {path} is listed as removed but still exists")
            failed = True
    if unowned:
        print("FAIL these changed files answer to no rule in build/fork.json:")
        for path in sorted(unowned):
            print(f"  {path}")
        print(
            "Either move the change into a fork path, or add the file to the hooks or reads list with its reason."
        )
        failed = True
    if not failed:
        print(f"OK the layer stays inside its bounds against {base[:7]}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
