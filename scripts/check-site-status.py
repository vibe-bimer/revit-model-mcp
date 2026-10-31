#!/usr/bin/env python3
"""Report on the documentation site's publish health.

The publisher writes every attempt into the state root and the timer writes
every run there, so the deployment knows its own health. This script turns
that state into an exit code an operator or a monitor can act on:

    0  the publish channel is healthy
    1  the last publish attempt failed
    2  the deployment is stale: no recent success, or the timer stopped running

Every run records its verdict in the state root, so the deployment's own
status page shows the last watchdog result too. When ``SITE_ALERT_WEBHOOK``
points at a webhook, an unhealthy verdict is posted there as JSON.

Usage:

    python3 scripts/check-site-status.py
    python3 scripts/check-site-status.py --json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import site_status  # the sibling module is imported by path

EXIT_HEALTHY = 0
EXIT_FAILED = 1
EXIT_STALE = 2


def verdict(summary: dict) -> tuple[int, str]:
    """Return the exit code and a one-line verdict for one summary."""
    outcome = str(summary.get("outcome") or "").lower()
    reasons = summary.get("stale_reasons") or []
    if outcome in ("failure", "failed", "error"):
        return EXIT_FAILED, "; ".join(reasons) or "the last publish attempt failed"
    if summary.get("stale"):
        return EXIT_STALE, "; ".join(reasons)
    return EXIT_HEALTHY, "the publish channel is healthy"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--json", action="store_true", help="print the summary as JSON")
    parser.add_argument("--state", default=None, help="the state root to read")
    parser.add_argument(
        "--no-alert", action="store_true", help="do not post to the alert webhook"
    )
    args = parser.parse_args(argv)

    state = Path(args.state).expanduser() if args.state else site_status.state_dir()
    summary = site_status.summarize(state)
    code, message = verdict(summary)

    alert = None
    webhook = (os.environ.get(site_status.ALERT_ENV) or "").strip()
    if webhook and code != EXIT_HEALTHY and not args.no_alert:
        delivered, detail = site_status.post_alert(
            webhook,
            {
                "source": "revit-model-mcp-site",
                "verdict": message,
                "exit_code": code,
                "summary": summary,
            },
        )
        alert = {"webhook": webhook, "delivered": delivered, "detail": detail}

    site_status.record_watchdog_run(state, exit_code=code, verdict=message)

    if args.json:
        print(
            json.dumps(
                {"exit_code": code, "verdict": message, "alert": alert, **summary},
                indent=2,
                sort_keys=True,
            )
        )
    else:
        print(f"exit {code}: {message}")
        for reason in summary.get("stale_reasons") or []:
            print(f"  - {reason}")
        if alert is not None:
            state_text = "delivered" if alert["delivered"] else "not delivered"
            print(f"  alert {state_text}: {alert['detail']}")
    return code


if __name__ == "__main__":
    sys.exit(main())
