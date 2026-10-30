#!/usr/bin/env python3
"""Check that every upstream commit since the last intake has been classified.

The ledger is the single hand-written source: a commit counts as classified when
its SHA appears anywhere in the ledger's Markdown. The cursor in
analysis/upstream-seen.json says where the last intake stopped. This tool joins
the two and reports what fell through.

Run after `git fetch upstream --tags`, before moving the cursor:

    python3 tools/check_upstream_intake.py

Exit status is 1 while any commit in the range is unclassified. Classify each
one in the ledger, then move the cursor:

    python3 tools/check_upstream_intake.py --update-seen
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEEN = ROOT / "analysis/upstream-seen.json"
SHA_IN_LEDGER = re.compile(r"`([0-9a-f]{7,40})`")
LOG_FORMAT = "%H%x09%s"


class IntakeError(Exception):
    """A condition the caller must fix before the intake can be trusted."""


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise IntakeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout


def load_seen() -> dict:
    if not SEEN.is_file():
        raise IntakeError(
            f"{SEEN.relative_to(ROOT)} is missing; it records the intake cursor"
        )
    return json.loads(SEEN.read_text(encoding="utf-8"))


def resolve(ref: str) -> str:
    try:
        return git("rev-parse", "--verify", f"{ref}^{{commit}}").strip()
    except IntakeError:
        raise IntakeError(
            f"{ref} is not available; run `git fetch upstream --tags` first"
        ) from None


def commits_between(start: str, end: str) -> list[tuple[str, str]]:
    raw = git("log", f"--format={LOG_FORMAT}", f"{start}..{end}")
    rows = []
    for line in raw.splitlines():
        if "\t" in line:
            sha, subject = line.split("\t", 1)
            rows.append((sha, subject))
    return rows


def ledger_shas(ledger: Path) -> set[str]:
    if not ledger.is_file():
        raise IntakeError(f"{ledger.relative_to(ROOT)} is missing")
    return {
        match.lower()
        for match in SHA_IN_LEDGER.findall(ledger.read_text(encoding="utf-8"))
    }


def classified(sha: str, known: set[str]) -> bool:
    return any(sha.startswith(entry) or entry.startswith(sha) for entry in known)


def resolves(sha: str) -> bool:
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0


def report(pending: list[tuple[str, str]], known: set[str], in_range: set[str]) -> int:
    unclassified = [
        (sha, subject) for sha, subject in pending if not classified(sha, known)
    ]
    unresolved = sorted(entry for entry in known if not resolves(entry))

    print(f"upstream commits in range: {len(pending)}")
    print(f"classified in ledger:      {len(pending) - len(unclassified)}")
    print(f"unclassified:              {len(unclassified)}")

    if unresolved:
        print()
        print("ledger names SHAs that are not commits in this repository (typos?):")
        for entry in unresolved:
            print(f"  {entry}")

    if not unclassified:
        return 0

    print()
    print("unclassified commits:")
    for sha, subject in unclassified:
        print(f"  {sha[:9]}  {subject}")
    print()
    print(
        "Add each one to analysis/upstream-port-ledger.md under a batch, then re-run."
    )
    return 1


def update_seen(seen: dict, head: str) -> None:
    subject = (
        git("log", "-1", f"--format={LOG_FORMAT}", head).strip().split("\t", 1)[-1]
    )
    seen["last_seen"] = head
    seen["last_seen_subject"] = subject
    SEEN.write_text(
        json.dumps(seen, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print()
    print(f"cursor moved to {head[:9]}  {subject}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--ref",
        help="upstream ref to inspect (default: the ref recorded in upstream-seen.json)",
    )
    parser.add_argument(
        "--update-seen",
        action="store_true",
        help="move the cursor to the inspected ref; refuses while commits are unclassified",
    )
    args = parser.parse_args()

    try:
        seen = load_seen()
        ref = args.ref or seen.get("ref") or "upstream/main"
        head = resolve(ref)
        start = seen["last_seen"]
        pending = commits_between(start, head)
        known = ledger_shas(
            ROOT / seen.get("ledger", "analysis/upstream-port-ledger.md")
        )
    except (IntakeError, KeyError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    if not pending:
        print(f"nothing new since {start[:9]} on {ref}")
        return 0

    print(f"range: {start[:9]}..{head[:9]} on {ref}")
    print()
    status = report(pending, known, {sha for sha, _ in pending})

    if args.update_seen and status == 0:
        update_seen(seen, head)
    elif args.update_seen:
        print()
        print("cursor not moved: classify the commits above first.", file=sys.stderr)

    return status


if __name__ == "__main__":
    sys.exit(main())
