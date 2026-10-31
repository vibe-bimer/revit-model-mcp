"""Behaviour tests for the three operational publish defaults (issue #38).

Covers the decisions recorded in the release receipt (section 6): a pinned
``SITE_COMMIT`` is honoured end to end; the export builds its own server
environment with ``uv sync`` when possible and falls back to a symlink of the
checkout's virtualenv, with the chosen path visible in the log and the
manifest; and ``SITE_KEEP_RELEASES`` controls retention, failing loudly on
values that would drop the current or previous release.
"""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PUBLISH_SCRIPT = REPO_ROOT / "scripts" / "publish_site.py"

# The publisher runs this suite as a build gate; skip to avoid recursion.
if os.environ.get("SITE_PUBLISH_RUNNING"):
    raise unittest.SkipTest("publisher gate: the publish suite already ran outside")

MARKER = "Revit Model MCP"

_spec = importlib.util.spec_from_file_location(
    "publish_site_defaults_under_test", PUBLISH_SCRIPT
)
publisher = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(publisher)

FAKE_BUILDER = """#!/bin/sh
# Minimal mkdocs stand-in: writes docs/index.md into the -d target as index.html.
d=""
prev=""
for a in "$@"; do
  [ "$prev" = "-d" ] && d="$a"
  prev="$a"
done
[ -n "$d" ] || { echo "fake builder: no -d target" >&2; exit 64; }
mkdir -p "$d"
{
  echo '<html><body><div data-md-component="announce"><a class="md-logo" href="/">Docs</a></div>'
  cat docs/index.md 2>/dev/null || echo "Revit Model MCP"
  echo "</body></html>"
} >"$d/index.html"
echo "<html><body>missing</body></html>" >"$d/404.html"
"""

FAKE_UV = """#!/bin/sh
# Test double for uv: records the call, builds a minimal venv skeleton.
mkdir -p .venv/bin
printf '#!/bin/sh\\n' > .venv/bin/python
chmod +x .venv/bin/python
echo "$(pwd)|$*" >> "$UV_SPY"
exit ${FAKE_UV_FAIL:-0}
"""


class PublishHarness(unittest.TestCase):
    """A temporary git source repo, state root and publish root per test."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.base = base
        self.repo = base / "repo"
        self.state = base / "state"
        self.publish_root = base / "web" / "site"
        self.builder = base / "fake-mkdocs"
        self._init_repo()
        self.builder.write_text(FAKE_BUILDER)
        self.builder.chmod(0o755)

    # -- fixture helpers ---------------------------------------------------

    def _init_repo(self):
        self.repo.mkdir(parents=True)
        self.git("init", "-q")
        self.git("config", "user.email", "site@example.invalid")
        self.git("config", "user.name", "Site Test")
        (self.repo / "mkdocs-lan.yml").write_text("site_name: test\n")
        self.write_source("v1")

    def git(self, *args, cwd=None):
        return subprocess.run(
            ["git", *args],
            cwd=cwd or self.repo,
            check=True,
            capture_output=True,
            text=True,
        )

    def write_source(self, text):
        docs = self.repo / "docs"
        docs.mkdir(exist_ok=True)
        (docs / "index.md").write_text(f"# {MARKER} {text}")

    def commit(self, message):
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)
        return self.head()

    def head(self):
        return self.git("rev-parse", "HEAD").stdout.strip()

    # -- publisher invocation ----------------------------------------------

    def publish(self, *arguments, **overrides):
        env = {
            **os.environ,
            "SITE_SKIP_PULL": "1",
            "SITE_STATE_DIR": str(self.state),
            "SITE_PUBLISH_ROOT": str(self.publish_root),
            "MKDOCS": str(self.builder),
            "PYTHON": sys.executable,
        }
        env.update({key: str(value) for key, value in overrides.items()})
        return subprocess.run(
            [
                sys.executable,
                str(PUBLISH_SCRIPT),
                "--repo",
                str(self.repo),
                *arguments,
            ],
            capture_output=True,
            text=True,
            env=env,
            timeout=180,
            check=False,
        )

    # -- assertions ---------------------------------------------------------

    def status(self):
        return json.loads((self.state / "manifest.json").read_text())

    def current_release(self):
        return (self.state / "current").resolve()

    def release_ids(self):
        return sorted(
            entry.name
            for entry in (self.state / "releases").iterdir()
            if entry.is_dir() and not entry.name.startswith(".")
        )


class FakeUvHarness(unittest.TestCase):
    """A fake uv binary plus an export/repo pair for environment tests."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.base = base
        self.bin = base / "bin"
        self.bin.mkdir()
        self.uv = self.bin / "uv"
        self.uv.write_text(FAKE_UV)
        self.uv.chmod(0o755)
        self.spy = base / "uv-calls.log"
        self.export = base / "export"
        self.repo = base / "repo"
        self.export.mkdir()
        self.repo.mkdir()

    def uv_env(self, fail=False):
        env = dict(os.environ, UV_SPY=str(self.spy))
        if fail:
            env["FAKE_UV_FAIL"] = "1"
        return env

    def add_export_project(self):
        server = self.export / "server"
        server.mkdir()
        (server / "pyproject.toml").write_text(
            '[project]\nname = "fake-server"\nversion = "0"\n'
        )

    def add_repo_venv(self):
        venv = self.repo / "server" / ".venv" / "bin"
        venv.mkdir(parents=True)
        (venv / "revit-model-mcp").write_text("#!/bin/sh\n")
        (self.repo / "server" / ".venv" / "bin" / "revit-model-mcp").chmod(0o755)

    def without_uv_on_path(self):
        """Hide every real uv from the environment for the duration."""
        import contextlib
        import io
        from unittest import mock

        stripped = os.pathsep.join(
            entry
            for entry in os.environ.get("PATH", "").split(os.pathsep)
            if not (Path(entry) / "uv").exists()
        )
        self.stdout = io.StringIO()
        stack = contextlib.ExitStack()
        self.addCleanup(stack.close)
        stack.enter_context(mock.patch.dict(os.environ, {"PATH": stripped}))
        stack.enter_context(contextlib.redirect_stdout(self.stdout))


class PinnedCommitTests(PublishHarness):
    def test_a_pinned_commit_is_published_even_when_head_is_newer(self):
        first = self.commit("v1")
        self.write_source("v2")
        self.commit("v2")

        result = self.publish(SITE_COMMIT=first)

        self.assertEqual(result.returncode, 0, result.stderr)
        page = (self.current_release() / "index.html").read_text()
        self.assertIn("v1", page)
        self.assertNotIn("v2", page)
        manifest = self.status()["current_manifest"]
        self.assertEqual(manifest["source_commit"], first)
        self.assertEqual(manifest["source_resolution"], "pin")

    def test_a_short_pinned_sha_is_resolved_to_the_full_commit(self):
        first = self.commit("v1")

        result = self.publish(SITE_COMMIT=first[:7])

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.status()["current_manifest"]["source_commit"], first)

    def test_republishing_the_same_pin_is_a_noop(self):
        first = self.commit("v1")
        self.assertEqual(self.publish(SITE_COMMIT=first).returncode, 0)

        again = self.publish(SITE_COMMIT=first)

        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertEqual(self.status()["last_attempt"]["outcome"], "noop")
        self.assertEqual(len(self.release_ids()), 1)


class ServerEnvironmentTests(FakeUvHarness):
    def test_uv_sync_builds_the_export_environment(self):
        self.add_export_project()

        record = publisher.prepare_server_environment(
            self.export, self.repo, self.uv_env(), uv=str(self.uv)
        )

        self.assertEqual(
            record, {"mode": "uv-sync", "command": "uv sync", "fallback": None}
        )
        venv = self.export / "server" / ".venv"
        self.assertFalse(venv.is_symlink())
        self.assertTrue((venv / "bin" / "python").is_file())
        calls = self.spy.read_text()
        self.assertIn("sync", calls)
        self.assertIn(str(self.export / "server"), calls)

    def test_a_failed_sync_falls_back_to_the_checkout_venv_and_says_so(self):
        self.add_export_project()
        self.add_repo_venv()
        import contextlib
        import io

        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            record = publisher.prepare_server_environment(
                self.export, self.repo, self.uv_env(fail=True), uv=str(self.uv)
            )

        self.assertEqual(record["mode"], "linked")
        self.assertIn("uv sync failed with exit 1", record["fallback"])
        self.assertTrue((self.export / "server" / ".venv").is_symlink())
        self.assertIn("falling back", buffer.getvalue())

    def test_a_partial_sync_venv_is_replaced_by_the_fallback_link(self):
        self.add_export_project()
        self.add_repo_venv()
        # The failing fake uv still creates the skeleton, like a real sync
        # that dies halfway through.
        record = publisher.prepare_server_environment(
            self.export, self.repo, self.uv_env(fail=True), uv=str(self.uv)
        )

        self.assertEqual(record["mode"], "linked")
        self.assertTrue((self.export / "server" / ".venv").is_symlink())
        self.assertFalse((self.export / "server" / ".venv" / "bin" / "python").exists())

    def test_without_uv_the_checkout_venv_is_linked_with_a_visible_reason(self):
        self.add_export_project()
        self.add_repo_venv()
        self.without_uv_on_path()

        record = publisher.prepare_server_environment(self.export, self.repo, {})

        self.assertEqual(record["mode"], "linked")
        self.assertEqual(record["fallback"], "uv is not installed")
        self.assertTrue((self.export / "server" / ".venv").is_symlink())
        self.assertIn("falling back", self.stdout.getvalue())

    def test_no_uv_and_no_checkout_venv_is_recorded_as_absent(self):
        self.add_export_project()
        self.without_uv_on_path()

        record = publisher.prepare_server_environment(self.export, self.repo, {})

        self.assertEqual(record["mode"], "absent")
        self.assertEqual(record["fallback"], "uv is not installed")
        self.assertFalse((self.export / "server" / ".venv").exists())

    def test_uv_without_a_server_project_falls_back_to_the_checkout_venv(self):
        self.add_repo_venv()

        record = publisher.prepare_server_environment(
            self.export, self.repo, self.uv_env(), uv=str(self.uv)
        )

        self.assertEqual(record["mode"], "linked")
        self.assertEqual(record["fallback"], "the export carries no server project")


class FlowEnvironmentTests(PublishHarness):
    """The full publish flow records the environment path in the manifest."""

    def add_server_project(self):
        server = self.repo / "server"
        server.mkdir(exist_ok=True)
        (server / "pyproject.toml").write_text(
            '[project]\nname = "fake-server"\nversion = "0"\n'
        )

    def add_repo_venv(self):
        venv = self.repo / "server" / ".venv" / "bin"
        venv.mkdir(parents=True)
        (venv / "revit-model-mcp").write_text("#!/bin/sh\n")
        (venv / "revit-model-mcp").chmod(0o755)

    def path_without_uv(self):
        return os.pathsep.join(
            entry
            for entry in os.environ.get("PATH", "").split(os.pathsep)
            if not (Path(entry) / "uv").exists()
        )

    def test_a_publish_with_uv_records_uv_sync_in_the_manifest(self):
        self.add_server_project()
        self.commit("add server project")
        bin_dir = self.base / "bin"
        bin_dir.mkdir(exist_ok=True)
        uv = bin_dir / "uv"
        uv.write_text(FAKE_UV)
        uv.chmod(0o755)

        result = self.publish(PATH=f"{bin_dir}{os.pathsep}{os.environ['PATH']}")

        self.assertEqual(result.returncode, 0, result.stderr)
        manifest = self.status()["current_manifest"]
        self.assertEqual(manifest["server_environment"]["mode"], "uv-sync")
        self.assertEqual(manifest["server_environment"]["command"], "uv sync")
        self.assertIsNone(manifest["server_environment"]["fallback"])
        self.assertNotIn(
            "server/.venv", manifest["verification"].get("linked_environments", "")
        )

    def test_a_publish_without_uv_records_the_symlink_fallback(self):
        self.add_server_project()
        self.commit("add server project")
        self.add_repo_venv()

        result = self.publish(PATH=self.path_without_uv())

        self.assertEqual(result.returncode, 0, result.stderr)
        manifest = self.status()["current_manifest"]
        self.assertEqual(manifest["server_environment"]["mode"], "linked")
        self.assertEqual(
            manifest["server_environment"]["fallback"], "uv is not installed"
        )
        self.assertIn("falling back", result.stdout)

    def test_an_export_without_a_server_project_is_recorded_as_absent(self):
        self.commit("v1")

        result = self.publish()

        self.assertEqual(result.returncode, 0, result.stderr)
        manifest = self.status()["current_manifest"]
        self.assertEqual(manifest["server_environment"]["mode"], "absent")
        self.assertEqual(
            manifest["server_environment"]["fallback"],
            "the export carries no server project",
        )

    def test_the_missing_project_reason_does_not_depend_on_uv(self):
        """The record must read the same on a machine with uv and on one without it."""
        self.commit("v1")

        with_uv = self.publish()
        without_uv = self.publish(PATH=self.path_without_uv())

        for result in (with_uv, without_uv):
            self.assertEqual(result.returncode, 0, result.stderr)
            manifest = self.status()["current_manifest"]
            self.assertEqual(manifest["server_environment"]["mode"], "absent")
            self.assertEqual(
                manifest["server_environment"]["fallback"],
                "the export carries no server project",
            )


class KeepReleasesTests(PublishHarness):
    def test_site_keep_releases_controls_retention(self):
        for version in ("v1", "v2", "v3", "v4"):
            self.write_source(version)
            self.commit(version)
            result = self.publish(SITE_KEEP_RELEASES="2")
            self.assertEqual(result.returncode, 0, result.stderr)

        self.assertEqual(len(self.release_ids()), 2)
        self.assertIn("v4", (self.current_release() / "index.html").read_text())

    def test_a_bad_keep_releases_value_fails_loudly_before_anything_changes(self):
        result = self.publish(SITE_KEEP_RELEASES="banana")

        self.assertEqual(result.returncode, 1)
        status = self.status()
        self.assertEqual(status["last_failure"]["stage"], "config")
        self.assertIn("SITE_KEEP_RELEASES", status["last_failure"]["reason"])
        self.assertEqual(status["last_attempt"]["outcome"], "failure")
        self.assertEqual(self.release_ids(), [])
        self.assertFalse((self.state / "current").exists())

    def test_keep_releases_below_two_fails_loudly(self):
        self.commit("v1")

        result = self.publish(SITE_KEEP_RELEASES="1")

        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.status()["last_failure"]["stage"], "config")
        self.assertIn("at least 2", self.status()["last_failure"]["reason"])
        self.assertEqual(self.release_ids(), [])


if __name__ == "__main__":
    unittest.main()
