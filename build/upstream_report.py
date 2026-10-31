"""Say which upstream commits the fork's base contains and which it does not.

`adr/0001` sets the rhythm: once per minor release, read the upstream range the base does not contain. That range
should be a command, not a memory. This prints it.

Exit codes: 0 the report was produced, 2 it could not be produced.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = Path(__file__).resolve().parent / "fork.json"
UPSTREAM_REMOTE = "upstream"


def run(*arguments: str, repository_root: Path = REPOSITORY_ROOT) -> str:
    result = subprocess.run(
        list(arguments),
        cwd=repository_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(f"{' '.join(arguments)} failed: {result.stderr.strip()}")
    return result.stdout


def upstream_branch(repository_root: Path = REPOSITORY_ROOT) -> str:
    """The remote-tracking branch to compare against, preferring one that exists."""
    for candidate in (f"{UPSTREAM_REMOTE}/main", f"{UPSTREAM_REMOTE}/master"):
        result = subprocess.run(
            ["git", "rev-parse", "--verify", "--quiet", candidate],
            cwd=repository_root,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            return candidate
    raise SystemExit(
        f"no {UPSTREAM_REMOTE}/main or {UPSTREAM_REMOTE}/master ref; run git fetch {UPSTREAM_REMOTE}"
    )


def report(
    config: dict,
    repository_root: Path = REPOSITORY_ROOT,
    branch: str | None = None,
) -> str:
    # branch defaults to the remote-tracking upstream branch; callers that only
    # exercise the report pass a ref that exists in their own clone.
    base = config["base"]
    branch = branch or upstream_branch(repository_root)
    behind = run("git", "rev-list", "--count", f"{base}..{branch}").strip()
    ahead = run("git", "rev-list", "--count", f"{branch}..{base}").strip()
    log = run("git", "log", "--oneline", "--no-decorate", f"{base}..{branch}")
    lines = [
        f"base      {base}",
        f"upstream  {branch}",
        f"behind    {behind} upstream commits after the base",
        f"ahead     {ahead} upstream commits the base carries alone",
        "",
        "not in the base:"
        if log.strip()
        else "not in the base: nothing, the base is current",
    ]
    lines.extend(f"  {line}" for line in log.splitlines())
    return "\n".join(lines)


def main() -> int:
    print(report(json.loads(CONFIG_PATH.read_text(encoding="utf-8"))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
