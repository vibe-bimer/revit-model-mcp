"""Tests for the publish-status summary and its watchdog.

The publisher and the timer write their state into one directory; these tests
drive that directory directly and assert on the summary, the HTML rendering,
the records the scripts write, and the watchdog's exit codes.
"""

import contextlib
import datetime
import importlib.util
import io
import json
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "scripts"

_spec = importlib.util.spec_from_file_location(
    "site_status", SCRIPTS / "site_status.py"
)
site_status = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(site_status)

_watchdog_spec = importlib.util.spec_from_file_location(
    "check_site_status", SCRIPTS / "check-site-status.py"
)
check_site_status = importlib.util.module_from_spec(_watchdog_spec)
_watchdog_spec.loader.exec_module(check_site_status)

NOW = datetime.datetime(2026, 5, 1, 12, 0, tzinfo=datetime.timezone.utc)


def stamp(hours_ago: float) -> str:
    moment = NOW - datetime.timedelta(hours=hours_ago)
    return moment.strftime("%Y-%m-%dT%H:%M:%SZ")


class StateDirTests(unittest.TestCase):
    def test_configured_state_dir_wins(self):
        self.assertEqual(
            site_status.state_dir({"SITE_STATE_DIR": "/tmp/site-state"}),
            Path("/tmp/site-state"),
        )

    def test_xdg_state_home_is_the_default_base(self):
        self.assertEqual(
            site_status.state_dir({"XDG_STATE_HOME": "/tmp/xdg"}),
            Path("/tmp/xdg/revit-model-mcp"),
        )

    def test_home_fallback(self):
        self.assertEqual(
            site_status.state_dir({}),
            Path.home() / ".local" / "state" / "revit-model-mcp",
        )


class SummarizeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.state = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def write(self, name, payload):
        (self.state / name).write_text(json.dumps(payload), encoding="utf-8")

    def healthy_manifest(self):
        return {
            "schema": "revit-model-mcp.site-status/v1",
            "current_release": "20260501T110000Z-abc1234",
            "last_attempt": {
                "outcome": "noop",
                "utc": stamp(1),
                "stage": "noop",
                "release_id": "20260501T110000Z-abc1234",
            },
            "last_success": {
                "utc": stamp(1),
                "noop": True,
                "release_id": "20260501T110000Z-abc1234",
            },
        }

    def summary(self, **kwargs):
        return site_status.summarize(self.state, now=NOW, env={}, **kwargs)

    def test_a_fresh_noop_is_healthy(self):
        self.write("manifest.json", self.healthy_manifest())
        summary = self.summary()
        self.assertEqual(summary["outcome"], "noop")
        self.assertFalse(summary["stale"])
        self.assertEqual(summary["stale_reasons"], [])
        self.assertEqual(summary["current_release"], "20260501T110000Z-abc1234")
        self.assertEqual(summary["thresholds"]["stale_hours"], 26)

    def test_a_failed_attempt_is_reported_with_its_stage(self):
        manifest = self.healthy_manifest()
        manifest["last_attempt"] = {
            "outcome": "failure",
            "utc": stamp(0.5),
            "stage": "build",
            "release_id": None,
        }
        manifest["last_failure"] = {
            "utc": stamp(0.5),
            "stage": "build",
            "reason": "mkdocs build failed",
        }
        self.write("manifest.json", manifest)
        summary = self.summary()
        self.assertEqual(summary["outcome"], "failure")
        self.assertTrue(summary["stale"])
        self.assertIn("failed at stage build", " ".join(summary["stale_reasons"]))
        self.assertEqual(summary["last_failure"]["reason"], "mkdocs build failed")

    def test_an_old_success_is_stale(self):
        manifest = self.healthy_manifest()
        manifest["last_success"]["utc"] = stamp(40)
        manifest["last_attempt"]["utc"] = stamp(40)
        self.write("manifest.json", manifest)
        summary = self.summary()
        self.assertTrue(summary["stale"])
        self.assertIn("hours old", " ".join(summary["stale_reasons"]))

    def test_the_stale_threshold_is_configurable(self):
        manifest = self.healthy_manifest()
        manifest["last_success"]["utc"] = stamp(40)
        self.write("manifest.json", manifest)
        relaxed = site_status.summarize(
            self.state,
            now=NOW,
            env={"SITE_STATUS_STALE_HOURS": "48"},
        )
        self.assertFalse(relaxed["stale"])
        self.assertEqual(relaxed["thresholds"]["stale_hours"], 48)

    def test_a_missing_success_is_reported_as_never(self):
        self.write("manifest.json", {"last_attempt": {"outcome": "noop"}})
        summary = self.summary()
        self.assertTrue(summary["stale"])
        self.assertIn("no successful publish is on record", summary["stale_reasons"])

    def test_a_silent_timer_is_stale(self):
        self.write("manifest.json", self.healthy_manifest())
        self.write(
            "cron-status.json",
            {"schema": "revit-model-mcp.site-timer/v1", "started_utc": stamp(5)},
        )
        summary = self.summary()
        self.assertTrue(summary["stale"])
        self.assertIn("timer has been silent", " ".join(summary["stale_reasons"]))

    def test_a_recent_timer_run_keeps_the_deployment_fresh(self):
        self.write("manifest.json", self.healthy_manifest())
        self.write(
            "cron-status.json",
            {
                "schema": "revit-model-mcp.site-timer/v1",
                "started_utc": stamp(0.1),
                "finished_utc": stamp(0.05),
                "exit_code": 0,
            },
        )
        summary = self.summary()
        self.assertFalse(summary["stale"])
        self.assertEqual(summary["last_timer_run"]["exit_code"], 0)

    def test_a_watchdog_record_is_carried(self):
        self.write("manifest.json", self.healthy_manifest())
        self.write(
            "watchdog-status.json",
            {
                "schema": "revit-model-mcp.site-watchdog/v1",
                "checked_utc": stamp(0.2),
                "exit_code": 0,
                "verdict": "the publish channel is healthy",
            },
        )
        summary = self.summary()
        self.assertEqual(summary["last_watchdog_run"]["exit_code"], 0)

    def test_an_unreadable_manifest_reads_as_unknown(self):
        (self.state / "manifest.json").write_text("{not json", encoding="utf-8")
        summary = self.summary()
        self.assertEqual(summary["outcome"], "unknown")
        self.assertTrue(summary["stale"])


class RenderTests(unittest.TestCase):
    def test_the_page_names_the_release_and_links_the_json(self):
        summary = {
            "outcome": "noop",
            "current_release": "20260501T110000Z-abc1234",
            "last_attempt": {"utc": stamp(1), "stage": "noop"},
            "last_success": {"utc": stamp(1), "release_id": "20260501T110000Z-abc1234"},
            "last_failure": {},
            "last_timer_run": {"started_utc": stamp(0.1), "exit_code": 0},
            "state_dir": "/tmp/state",
            "generated_utc": stamp(0),
            "stale": False,
            "stale_reasons": [],
        }
        page = site_status.render_html(summary)
        self.assertIn("20260501T110000Z-abc1234", page)
        self.assertIn("/status.json", page)
        self.assertIn("发布通道正常", page)
        self.assertIn('content="noindex"', page)

    def test_a_stale_page_shows_the_reasons(self):
        summary = {
            "outcome": "failure",
            "current_release": "20260501T110000Z-abc1234",
            "last_attempt": {"utc": stamp(1), "stage": "build"},
            "last_success": {"utc": stamp(30)},
            "last_failure": {"utc": stamp(1), "stage": "build", "reason": "boom"},
            "last_timer_run": {},
            "state_dir": "/tmp/state",
            "generated_utc": stamp(0),
            "stale": True,
            "stale_reasons": ["the last publish attempt failed at stage build"],
        }
        page = site_status.render_html(summary)
        self.assertIn("发布通道异常", page)
        self.assertIn("failed at stage build", page)


class RecordTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.state = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_a_timer_run_is_recorded_atomically(self):
        path = site_status.record_timer_run(
            self.state, started_utc="2026-05-01T11:00:00Z", exit_code=0, publish_exit=0
        )
        self.assertEqual(path, self.state / "cron-status.json")
        payload = json.loads(path.read_text())
        self.assertEqual(payload["schema"], "revit-model-mcp.site-timer/v1")
        self.assertEqual(payload["started_utc"], "2026-05-01T11:00:00Z")
        self.assertEqual(payload["exit_code"], 0)
        self.assertEqual(list(self.state.glob("*.tmp")), [])

    def test_a_watchdog_run_is_recorded(self):
        path = site_status.record_watchdog_run(self.state, exit_code=2, verdict="stale")
        payload = json.loads(path.read_text())
        self.assertEqual(payload["schema"], "revit-model-mcp.site-watchdog/v1")
        self.assertEqual(payload["exit_code"], 2)
        self.assertEqual(payload["verdict"], "stale")
        self.assertTrue(payload["checked_utc"])

    def test_the_timer_cli_writes_a_record(self):
        code = site_status.main(
            [
                "--record-timer",
                "--state",
                str(self.state),
                "--exit-code",
                "1",
                "--publish-exit",
                "2",
                "--verification",
                "failed",
                "--started",
                "2026-05-01T11:00:00Z",
                "--note",
                "mkdocs build failed",
            ]
        )
        self.assertEqual(code, 0)
        payload = json.loads((self.state / "cron-status.json").read_text())
        self.assertEqual(payload["exit_code"], 1)
        self.assertEqual(payload["publish_exit"], 2)
        self.assertEqual(payload["verification"], "failed")
        self.assertEqual(payload["note"], "mkdocs build failed")


class AlertTests(unittest.TestCase):
    def setUp(self):
        self.received = []

    def start_server(self, status_code):
        received = self.received

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                length = int(self.headers.get("content-length") or 0)
                received.append(
                    {
                        "path": self.path,
                        "body": json.loads(self.rfile.read(length) or b"{}"),
                        "content_type": self.headers.get("content-type"),
                    }
                )
                self.send_response(status_code)
                self.send_header("content-length", "0")
                self.end_headers()

            def log_message(self, *args, **kwargs):
                pass

        server = HTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.shutdown)
        self.addCleanup(server.server_close)
        self.addCleanup(thread.join, 5)
        return f"http://127.0.0.1:{server.server_address[1]}/hook"

    def test_a_healthy_post_is_delivered(self):
        webhook = self.start_server(204)
        delivered, detail = site_status.post_alert(webhook, {"verdict": "stale"})
        self.assertTrue(delivered, detail)
        self.assertEqual(self.received[0]["body"], {"verdict": "stale"})
        self.assertEqual(self.received[0]["content_type"], "application/json")

    def test_a_rejected_post_is_reported(self):
        webhook = self.start_server(500)
        delivered, detail = site_status.post_alert(webhook, {"verdict": "stale"})
        self.assertFalse(delivered)
        self.assertIn("500", detail)

    def test_an_unreachable_webhook_is_reported(self):
        delivered, detail = site_status.post_alert(
            "http://127.0.0.1:9/hook", {"verdict": "stale"}, timeout=1
        )
        self.assertFalse(delivered)
        self.assertTrue(detail)


class WatchdogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.state = Path(self.temp.name)
        self.now = site_status.utc_now()

    def tearDown(self):
        self.temp.cleanup()

    def write(self, name, payload):
        (self.state / name).write_text(json.dumps(payload), encoding="utf-8")

    def healthy(self):
        self.write(
            "manifest.json",
            {
                "current_release": "20260501T110000Z-abc1234",
                "last_attempt": {"outcome": "noop", "utc": self.now, "stage": "noop"},
                "last_success": {"utc": self.now, "release_id": "x"},
            },
        )

    def run_watchdog(self, *extra):
        """Run the watchdog, capturing its report; return its exit code."""
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = check_site_status.main(["--state", str(self.state), *extra])
        self.report = buffer.getvalue()
        return code

    def test_a_healthy_deployment_exits_zero(self):
        self.healthy()
        self.assertEqual(self.run_watchdog("--json"), 0)
        payload = json.loads(self.report)
        self.assertEqual(payload["exit_code"], 0)
        self.assertEqual(payload["verdict"], "the publish channel is healthy")

    def test_a_failed_publish_exits_one(self):
        self.write(
            "manifest.json",
            {
                "last_attempt": {"outcome": "failure", "stage": "build"},
                "last_success": {"utc": self.now},
            },
        )
        self.assertEqual(self.run_watchdog(), 1)

    def test_a_stale_deployment_exits_two(self):
        self.write(
            "manifest.json",
            {
                "last_attempt": {"outcome": "noop", "stage": "noop"},
                "last_success": {"utc": "2026-01-01T00:00:00Z"},
            },
        )
        self.assertEqual(self.run_watchdog(), 2)
        self.assertIn("hours old", self.report)

    def test_the_verdict_is_recorded_for_the_status_page(self):
        self.healthy()
        self.run_watchdog()
        payload = json.loads((self.state / "watchdog-status.json").read_text())
        self.assertEqual(payload["exit_code"], 0)
        self.assertEqual(payload["schema"], "revit-model-mcp.site-watchdog/v1")

    def test_the_verdict_function_orders_failure_before_stale(self):
        summary = {
            "outcome": "failure",
            "stale": True,
            "stale_reasons": ["the last publish attempt failed at stage build"],
        }
        code, message = check_site_status.verdict(summary)
        self.assertEqual(code, 1)
        self.assertIn("failed at stage build", message)


if __name__ == "__main__":
    unittest.main()
