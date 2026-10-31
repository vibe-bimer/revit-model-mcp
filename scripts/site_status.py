#!/usr/bin/env python3
"""Summarize the documentation site's publish status.

The publisher records every attempt in ``<state>/manifest.json`` and the
timer records every run in ``<state>/cron-status.json``. This module reads
both files and turns them into one summary: the outcome of the last attempt,
the last successful release, the last failure, and whether the deployment
looks stale — a publisher that died leaves a successful release that ages.

The summary has two renderings: a machine-readable JSON document and a
bilingual HTML page. The served site answers them at ``/status.json`` and
``/status.html``; the watchdog script reads the same summary through this
module.

Usage:

    python3 scripts/site_status.py --json
    python3 scripts/site_status.py --record-timer --publish-exit 0
"""

from __future__ import annotations

import argparse
import datetime
import html
import json
import os
import sys
from pathlib import Path

SUMMARY_SCHEMA = "revit-model-mcp.site-status/v1"
TIMER_SCHEMA = "revit-model-mcp.site-timer/v1"
WATCHDOG_SCHEMA = "revit-model-mcp.site-watchdog/v1"

# A successful publish older than this means the publisher stopped working.
DEFAULT_STALE_HOURS = 26
# The timer runs every 15 minutes; two silent hours mean it stopped.
DEFAULT_TIMER_SILENT_HOURS = 2

STATE_ENV = "SITE_STATE_DIR"
STALE_ENV = "SITE_STATUS_STALE_HOURS"
TIMER_SILENT_ENV = "SITE_STATUS_TIMER_SILENT_HOURS"
ALERT_ENV = "SITE_ALERT_WEBHOOK"

MANIFEST_NAME = "manifest.json"
TIMER_NAME = "cron-status.json"
WATCHDOG_NAME = "watchdog-status.json"


def state_dir(env: dict | None = None) -> Path:
    """Return the state root the publisher and the timer share."""
    environment = os.environ if env is None else env
    configured = (environment.get(STATE_ENV) or "").strip()
    if configured:
        return Path(configured).expanduser()
    base = (environment.get("XDG_STATE_HOME") or "").strip()
    if not base:
        base = str(Path.home() / ".local" / "state")
    return Path(base).expanduser() / "revit-model-mcp"


def read_json(path: Path) -> dict:
    """Read one JSON document; a missing or broken file reads as empty."""
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text())
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def parse_utc(value: str | None) -> datetime.datetime | None:
    """Parse an ISO 8601 UTC stamp; anything else reads as unknown."""
    if not value:
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        stamp = datetime.datetime.fromisoformat(text)
    except ValueError:
        return None
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=datetime.timezone.utc)
    return stamp.astimezone(datetime.timezone.utc)


def utc_now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def hours_since(value: str | None, now: datetime.datetime) -> float | None:
    """Return the age in hours of an ISO stamp, or None when it is unknown."""
    stamp = parse_utc(value)
    if stamp is None:
        return None
    return max(0.0, (now - stamp).total_seconds() / 3600)


def _float_env(env: dict, name: str, default: float) -> float:
    raw = (env.get(name) or "").strip()
    if not raw:
        return default
    try:
        value = float(raw)
    except ValueError:
        return default
    return value if value > 0 else default


def summarize(
    state: Path | None = None,
    now: datetime.datetime | None = None,
    env: dict | None = None,
) -> dict:
    """Return the publish status of one deployment."""
    environment = os.environ if env is None else env
    root = state if state is not None else state_dir(environment)
    moment = now or datetime.datetime.now(datetime.timezone.utc)
    manifest = read_json(root / MANIFEST_NAME)
    timer = read_json(root / TIMER_NAME)
    watchdog = read_json(root / WATCHDOG_NAME)

    attempt = manifest.get("last_attempt") or {}
    success = manifest.get("last_success") or {}
    failure = manifest.get("last_failure") or {}
    outcome = str(attempt.get("outcome") or "").strip().lower()

    stale_hours = _float_env(environment, STALE_ENV, DEFAULT_STALE_HOURS)
    silent_hours = _float_env(environment, TIMER_SILENT_ENV, DEFAULT_TIMER_SILENT_HOURS)

    success_age = hours_since(success.get("utc"), moment)
    timer_age = hours_since(
        timer.get("finished_utc") or timer.get("started_utc"), moment
    )

    reasons = []
    if outcome in ("failure", "failed", "error"):
        reasons.append(
            f"the last publish attempt failed at stage {attempt.get('stage') or 'unknown'}"
        )
    if success_age is None:
        reasons.append("no successful publish is on record")
    elif success_age > stale_hours:
        reasons.append(
            f"the last successful publish is {success_age:.1f} hours old "
            f"(limit {stale_hours:.0f} hours)"
        )
    if timer.get("started_utc") and timer_age is not None and timer_age > silent_hours:
        reasons.append(
            f"the publish timer has been silent for {timer_age:.1f} hours "
            f"(limit {silent_hours:.0f} hours)"
        )

    return {
        "schema": SUMMARY_SCHEMA,
        "generated_utc": moment.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "state_dir": str(root),
        "outcome": outcome or "unknown",
        "current_release": manifest.get("current_release"),
        "last_attempt": attempt,
        "last_success": success,
        "last_failure": failure,
        "last_timer_run": timer,
        "last_watchdog_run": watchdog,
        "stale": bool(reasons),
        "stale_reasons": reasons,
        "thresholds": {
            "stale_hours": stale_hours,
            "timer_silent_hours": silent_hours,
        },
    }


def _row(label: str, value: str) -> str:
    return f'<tr><th scope="row">{html.escape(label)}</th><td>{html.escape(value)}</td></tr>'


def render_html(summary: dict) -> str:
    """Render the summary as a self-contained bilingual page."""
    attempt = summary.get("last_attempt") or {}
    success = summary.get("last_success") or {}
    failure = summary.get("last_failure") or {}
    timer = summary.get("last_timer_run") or {}
    reasons = summary.get("stale_reasons") or []

    def text(value, fallback="—"):
        if value is None or value == "":
            return fallback
        return str(value)

    rows = [
        _row("发布结果 / Outcome", text(summary.get("outcome"))),
        _row(
            "最近一次尝试 / Last attempt",
            f"{text(attempt.get('utc'))} · {text(attempt.get('stage'))} · "
            f"{text(attempt.get('release_id'))}",
        ),
        _row(
            "最近一次成功 / Last success",
            f"{text(success.get('utc'))} · {text(success.get('release_id'))} · "
            f"{text(success.get('source_commit'), '')[:10]}",
        ),
        _row(
            "最近一次失败 / Last failure",
            f"{text(failure.get('utc'))} · {text(failure.get('stage'))} · "
            f"{text(failure.get('reason'))}",
        ),
        _row(
            "定时器最近一次运行 / Last timer run",
            f"{text(timer.get('started_utc'))} → {text(timer.get('finished_utc'))} · "
            f"exit {text(timer.get('exit_code'))}",
        ),
        _row("当前发布 / Current release", text(summary.get("current_release"))),
        _row("状态目录 / State directory", text(summary.get("state_dir"))),
        _row("生成时间 / Generated", text(summary.get("generated_utc"))),
    ]

    if reasons:
        verdict = "；".join(reasons)
        banner = (
            '<p class="banner stale">发布通道异常 / The publish channel needs attention: '
            f"{html.escape(verdict)}</p>"
        )
    else:
        banner = (
            '<p class="banner ok">发布通道正常 / The publish channel is healthy.</p>'
        )

    return f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>发布状态 / Publish status</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
         margin: 0 auto; max-width: 60rem; padding: 2rem 1.25rem; line-height: 1.5; }}
  h1 {{ font-size: 1.5rem; margin-bottom: 0.25rem; }}
  p.sub {{ margin-top: 0; opacity: 0.75; }}
  table {{ border-collapse: collapse; width: 100%; margin-top: 1rem; }}
  th, td {{ border-bottom: 1px solid rgba(127, 127, 127, 0.35); padding: 0.5rem 0.6rem;
           text-align: left; vertical-align: top; font-size: 0.95rem; }}
  th {{ width: 22rem; font-weight: 600; }}
  .banner {{ padding: 0.75rem 1rem; border-radius: 0.5rem; border: 1px solid; }}
  .banner.stale {{ border-color: #c2410c; background: rgba(194, 65, 12, 0.12); }}
  .banner.ok {{ border-color: #15803d; background: rgba(21, 128, 61, 0.12); }}
  footer {{ margin-top: 2rem; font-size: 0.85rem; opacity: 0.75; }}
  code {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }}
</style>
</head>
<body>
<h1>发布状态 / Publish status</h1>
<p class="sub">文档站点的最后一次发布结果。The outcome of the last documentation publish.</p>
{banner}
<table>
{chr(10).join(rows)}
</table>
<footer>
  机器可读格式 / Machine-readable: <a href="/status.json">/status.json</a> ·
  生成器 / Generator: <code>scripts/site_status.py</code>
</footer>
</body>
</html>
"""


def write_timer_record(state: Path, record: dict) -> Path:
    """Write the timer's run record atomically; return the file path."""
    state.mkdir(parents=True, exist_ok=True)
    path = state / TIMER_NAME
    payload = dict(record)
    payload["schema"] = TIMER_SCHEMA
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, path)
    return path


def write_watchdog_record(state: Path, record: dict) -> Path:
    """Write the watchdog's last check atomically; return the file path."""
    state.mkdir(parents=True, exist_ok=True)
    path = state / WATCHDOG_NAME
    payload = dict(record)
    payload["schema"] = WATCHDOG_SCHEMA
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, path)
    return path


def record_watchdog_run(
    state: Path | None = None,
    exit_code: int = 0,
    verdict: str | None = None,
) -> Path:
    """Record one watchdog check in the state root."""
    root = state if state is not None else state_dir()
    return write_watchdog_record(
        root,
        {
            "checked_utc": utc_now(),
            "exit_code": int(exit_code),
            "verdict": verdict,
        },
    )


def post_alert(webhook: str, payload: dict, timeout: float = 10.0) -> tuple[bool, str]:
    """Post one alert to a webhook; return whether it was delivered."""
    import urllib.error
    import urllib.request

    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        webhook,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            code = getattr(response, "status", 200)
            return (200 <= int(code) < 300), f"HTTP {code}"
    except urllib.error.HTTPError as error:
        return False, f"HTTP {error.code}"
    except (urllib.error.URLError, OSError, ValueError) as error:
        return False, str(error)


def record_timer_run(
    state: Path | None = None,
    exit_code: int = 0,
    publish_exit: int | None = None,
    verification: str | None = None,
    note: str | None = None,
    started_utc: str | None = None,
) -> Path:
    """Record one timer run in the state root."""
    root = state if state is not None else state_dir()
    record = {
        "started_utc": started_utc or utc_now(),
        "finished_utc": utc_now(),
        "exit_code": int(exit_code),
        "publish_exit": publish_exit,
        "verification": verification,
        "note": note,
    }
    return write_timer_record(root, record)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--json", action="store_true", help="print the summary as JSON")
    parser.add_argument("--state", default=None, help="the state root to read")
    parser.add_argument(
        "--record-timer",
        action="store_true",
        help="record a timer run instead of printing the summary",
    )
    parser.add_argument(
        "--exit-code", type=int, default=0, help="the timer run exit code"
    )
    parser.add_argument(
        "--publish-exit", type=int, default=None, help="the publisher exit code"
    )
    parser.add_argument(
        "--verification", default=None, help="the serving verification result"
    )
    parser.add_argument("--note", default=None, help="a short note about the run")
    parser.add_argument(
        "--started", default=None, help="the ISO stamp the run started at"
    )
    args = parser.parse_args(argv)

    state = Path(args.state).expanduser() if args.state else state_dir()
    if args.record_timer:
        path = record_timer_run(
            state,
            exit_code=args.exit_code,
            publish_exit=args.publish_exit,
            verification=args.verification,
            note=args.note,
            started_utc=args.started,
        )
        print(path)
        return 0

    summary = summarize(state)
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(render_html(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
