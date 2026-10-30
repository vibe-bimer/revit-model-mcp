"""Black-box tests for the atomic site publisher (``scripts/publish_site.py``).

Every test drives the real publisher as a subprocess against a temporary git
repository, a temporary state root and a fake builder, per the site review
spec: the observable contract is exit codes, the release layout under the
state root, the ``current`` symlink and the recorded status.
"""

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

FAKE_BUILDER = """#!/bin/sh
# Minimal mkdocs stand-in: writes docs/index.md into the -d target as index.html.
d=""
prev=""
for a in "$@"; do
  [ "$prev" = "-d" ] && d="$a"
  prev="$a"
done
[ -n "$d" ] || { echo "fake builder: no -d target" >&2; exit 64; }
if [ "${FAKE_FAIL:-0}" = "1" ]; then
  echo "fake builder: injected build failure" >&2
  exit 1
fi
mkdir -p "$d"
{
  echo "<html><body>"
  if [ "${FAKE_PROBE_BAD:-0}" = "1" ]; then
    echo "broken build without the marker"
  else
    cat docs/index.md 2>/dev/null || echo "Revit Model MCP"
  fi
  echo "</body></html>"
} >"$d/index.html"
echo "<html><body>missing</body></html>" >"$d/404.html"
"""


class PublishHarness(unittest.TestCase):
    """A temporary git source repo, state root and publish root per test."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
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

    def publish(self, **overrides):
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
            [sys.executable, str(PUBLISH_SCRIPT), "--repo", str(self.repo)],
            capture_output=True,
            text=True,
            env=env,
            timeout=120,
            check=False,
        )

    # -- assertions ---------------------------------------------------------

    def status(self):
        return json.loads((self.state / "manifest.json").read_text())

    def current_target(self):
        link = self.state / "current"
        self.assertTrue(link.is_symlink(), "current must be a symlink")
        return os.readlink(link)

    def release_ids(self):
        return sorted(
            entry.name
            for entry in (self.state / "releases").iterdir()
            if entry.is_dir() and not entry.name.startswith(".")
        )


class DirtySourcePublishTests(PublishHarness):
    def test_dirty_development_tree_publishes_pinned_head_content(self):
        """A dirty dev tree neither blocks publishing nor leaks into it."""
        self.commit("v1")
        result = self.publish()
        self.assertEqual(result.returncode, 0, result.stderr)

        # New commit, then dirty the working tree with content that must
        # never reach the release: the publisher builds from the commit.
        self.write_source("v2")
        second = self.commit("v2")
        self.write_source("UNCOMMITTED DIRT")
        dirty = self.publish()
        self.assertEqual(dirty.returncode, 0, dirty.stderr)

        release = (self.state / "current").resolve()
        page = (release / "index.html").read_text()
        self.assertIn("v2", page)
        self.assertNotIn("UNCOMMITTED DIRT", page)
        self.assertEqual(self.status()["current_manifest"]["source_commit"], second)

    def test_publish_root_becomes_a_symlink_to_current(self):
        self.commit("v1")
        result = self.publish()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(self.publish_root.is_symlink())
        self.assertEqual(
            self.publish_root.resolve(),
            (self.state / "current").resolve(),
        )
        self.assertIn(MARKER, (self.publish_root / "index.html").read_text())


class ReleaseLayoutTests(PublishHarness):
    def test_switch_keeps_the_previous_release_on_disk(self):
        self.write_source("v1")
        self.commit("v1")
        self.assertEqual(self.publish().returncode, 0)
        first_release = self.current_target()

        self.write_source("v2")
        self.commit("v2")
        self.assertEqual(self.publish().returncode, 0)
        second_release = self.current_target()

        self.assertNotEqual(first_release, second_release)
        self.assertTrue((self.state / "releases" / Path(first_release).name).is_dir())
        self.assertTrue((self.state / "releases" / Path(second_release).name).is_dir())
        self.assertEqual(Path(second_release).name, self.status()["current_release"])

    def test_release_carries_a_public_manifest(self):
        self.commit("v1")
        self.assertEqual(self.publish().returncode, 0)
        manifest = json.loads(
            ((self.state / "current").resolve() / "manifest.json").read_text()
        )
        self.assertEqual(manifest["source_commit"], self.head())
        self.assertIn("tree_sha", manifest)
        self.assertIn("built_utc", manifest)
        self.assertIn("verification", manifest)
        # No home-directory paths may leak into the public manifest.
        self.assertNotIn(str(Path.home()), json.dumps(manifest))

    def test_old_releases_are_pruned_but_current_and_previous_survive(self):
        for version in range(6):
            self.write_source(f"v{version}")
            self.commit(f"v{version}")
            result = self.publish()
            self.assertEqual(result.returncode, 0, result.stderr)
        kept = self.release_ids()
        self.assertLessEqual(len(kept), 3, f"retention should prune, kept {kept}")
        self.assertIn(Path(self.current_target()).name, kept)


if __name__ == "__main__":
    unittest.main()


class FailureSemanticsTests(PublishHarness):
    def setUp(self):
        super().setUp()
        self.commit("v1")
        self.assertEqual(self.publish().returncode, 0)
        self.good_release = self.current_target()

    def test_build_failure_keeps_the_served_site_and_records_the_reason(self):
        self.write_source("v2")
        self.commit("v2")
        broken = self.publish(FAKE_FAIL="1")
        self.assertEqual(broken.returncode, 1)
        self.assertEqual(self.current_target(), self.good_release)
        status = self.status()
        self.assertEqual(status["last_attempt"]["outcome"], "failure")
        self.assertEqual(status["last_failure"]["stage"], "build")
        self.assertIn("mkdocs build failed", status["last_failure"]["reason"])
        self.assertEqual(status["current_release"], Path(self.good_release).name)
        # A failed build leaves no half release behind.
        self.assertNotIn(".staging", "".join(self.release_ids()))

    def test_sync_failure_is_a_distinguishable_non_success(self):
        self.git("branch", "-M", "main")
        self.git("remote", "add", "origin", "/nonexistent/remote.git")
        self.git("config", "branch.main.remote", "origin")
        self.git("config", "branch.main.merge", "refs/heads/main")
        broken = self.publish(SITE_SKIP_PULL="", SITE_COMMIT="")
        self.assertEqual(broken.returncode, 2)
        self.assertEqual(self.current_target(), self.good_release)
        self.assertEqual(self.status()["last_failure"]["stage"], "sync")

    def test_unknown_pinned_commit_is_a_sync_failure(self):
        broken = self.publish(SITE_COMMIT="0" * 40)
        self.assertEqual(broken.returncode, 2)
        self.assertEqual(self.status()["last_failure"]["stage"], "sync")
