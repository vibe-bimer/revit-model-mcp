#!/usr/bin/env python3
"""Build and publish the documentation site with provenance and recovery.

The publisher never builds from the development checkout. It resolves a
target commit, exports it with ``git archive`` (so a dirty development tree
can neither block nor leak into a release), runs the repository's own gates
on the exported tree, builds into an immutable release directory and flips a
``current`` symlink atomically. Every attempt is recorded in a status file
under the state root, and failures leave the served site untouched.

Layout under the state root (``SITE_STATE_DIR``, default
``${XDG_STATE_HOME:-$HOME/.local/state}/revit-model-mcp``):

    releases/<utcstamp>-<shortsha>/   immutable build + public manifest.json
    current -> releases/<id>          atomically replaced symlink
    manifest.json                     latest status: attempt/success/failure
    publish.lock                      flock for concurrent publishers

The publish root (``SITE_PUBLISH_ROOT``, default ``<repo>/site``) is served
by ``serve-site.py``, which resolves it on every request, so swapping
``current`` switches the site without a restart and without a window.

Exit codes: 0 success (or recorded no-op), 1 build/check failure,
2 sync failure, 3 another publisher holds the lock, 4 health probe failure.
"""

from __future__ import annotations

import argparse
import datetime
import errno
import fcntl
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

EXIT_OK = 0
EXIT_FAILED = 1
EXIT_SYNC = 2
EXIT_LOCKED = 3
EXIT_HEALTH = 4

MANIFEST_SCHEMA = "revit-model-mcp.site-manifest/v1"
STATUS_SCHEMA = "revit-model-mcp.site-status/v1"


def log(message: str) -> None:
    print(message, flush=True)


def utc_now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(
    command: list[str], cwd: Path | None = None, env: dict | None = None
) -> subprocess.CompletedProcess:
    """Run a gate/build step, streaming its output into our own log."""
    log(f"$ {' '.join(shlex.quote(part) for part in command)}")
    return subprocess.run(command, cwd=cwd, env=env, check=False)


class Status:
    """Atomic reads and writes of the state-root manifest.json."""

    def __init__(self, path: Path):
        self.path = path
        self.data: dict = {}
        if path.is_file():
            try:
                self.data = json.loads(path.read_text())
            except ValueError:
                log(f"status file {path} is unreadable; starting a fresh one")
                self.data = {}

    def save(self) -> None:
        self.data["schema"] = STATUS_SCHEMA
        tmp = self.path.with_name(self.path.name + ".tmp")
        tmp.write_text(json.dumps(self.data, indent=2, sort_keys=True) + "\n")
        os.replace(tmp, self.path)

    def attempt(self, utc: str, commit: str, release: str, outcome: str, stage: str):
        self.data["last_attempt"] = {
            "utc": utc,
            "target_commit": commit,
            "release_id": release,
            "outcome": outcome,
            "stage": stage,
        }

    def succeeded(
        self, utc: str, release: str, commit: str, noop: bool, manifest: dict
    ):
        self.data["current_release"] = release
        self.data["current_manifest"] = manifest
        self.data["last_success"] = {
            "utc": utc,
            "release_id": release,
            "source_commit": commit,
            "noop": noop,
        }

    def failed(self, utc: str, stage: str, reason: str):
        self.data["last_failure"] = {"utc": utc, "stage": stage, "reason": reason}


def tree_sha256(root: Path) -> str:
    """Content hash of a built tree: paths and bytes, never timestamps."""
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        digest.update(str(path.relative_to(root)).encode())
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1 << 16), b""):
                digest.update(chunk)
    return digest.hexdigest()


def make_read_only(root: Path) -> None:
    for path in sorted(root.rglob("*"), reverse=True):
        mode = path.stat().st_mode
        os.chmod(path, mode & ~0o222)
    os.chmod(root, root.stat().st_mode & ~0o222)


def make_writable(root: Path) -> None:
    for path in sorted(root.rglob("*"), reverse=True):
        os.chmod(path, path.stat().st_mode | 0o200)
    os.chmod(root, root.stat().st_mode | 0o200)


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def resolve_target(repo: Path, skip_pull: bool, pinned: str | None) -> tuple[str, str]:
    """Return (commit sha, resolution mode) or raise with a sync failure."""
    if pinned:
        check = git(repo, "cat-file", "-e", f"{pinned}^{{commit}}")
        if check.returncode != 0:
            raise SystemExitMessage(
                EXIT_SYNC, f"pinned commit {pinned} does not exist in {repo}"
            )
        return git(repo, "rev-parse", pinned).stdout.strip(), "pin"
    if skip_pull:
        return git(repo, "rev-parse", "HEAD").stdout.strip(), "head"
    upstream = git(repo, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    if upstream.returncode != 0 or "/" not in upstream.stdout:
        log("no upstream branch; publishing the local HEAD")
        return git(repo, "rev-parse", "HEAD").stdout.strip(), "head"
    remote = upstream.stdout.strip().split("/", 1)[0]
    fetched = git(repo, "fetch", remote)
    if fetched.returncode != 0:
        raise SystemExitMessage(
            EXIT_SYNC,
            f"git fetch {remote} failed: {fetched.stderr.strip()}",
        )
    tip = git(repo, "rev-parse", upstream.stdout.strip())
    if tip.returncode != 0:
        raise SystemExitMessage(
            EXIT_SYNC, f"cannot resolve {upstream.stdout.strip()} after fetch"
        )
    return tip.stdout.strip(), "upstream"


class SystemExitMessage(Exception):
    """A terminal outcome with an exit code and a human-readable reason."""

    def __init__(self, code: int, reason: str, stage: str = "failed"):
        super().__init__(reason)
        self.code = code
        self.reason = reason
        self.stage = stage


def export_source(repo: Path, commit: str, destination: Path) -> None:
    """Extract the committed tree; the working tree is never consulted."""
    destination.mkdir(parents=True, exist_ok=True)
    archive = subprocess.Popen(
        ["git", "-C", str(repo), "archive", "--format=tar", commit],
        stdout=subprocess.PIPE,
    )
    assert archive.stdout is not None
    extract = subprocess.Popen(
        ["tar", "-x", "-C", str(destination)],
        stdin=archive.stdout,
    )
    archive.stdout.close()
    extract_rc = extract.wait()
    archive_rc = archive.wait()
    if extract_rc != 0 or archive_rc != 0:
        raise SystemExitMessage(
            EXIT_FAILED, f"git archive of {commit} failed", "export"
        )


def builder_command(repo: Path, source: Path) -> list[str]:
    configured = os.environ.get("MKDOCS", "").strip()
    if configured:
        return shlex.split(configured)
    for candidate in (
        repo / ".venv-docs" / "bin" / "mkdocs",
        Path.home() / ".venv-docs" / "bin" / "mkdocs",
    ):
        if candidate.is_file():
            return [str(candidate)]
    found = shutil.which("mkdocs")
    if found:
        return [found]
    requirements = source / "docs" / "requirements.txt"
    if requirements.is_file() and shutil.which("uv"):
        return [
            "uv",
            "run",
            "--with-requirements",
            str(requirements),
            "mkdocs",
        ]
    raise SystemExitMessage(
        EXIT_FAILED,
        "mkdocs was not found; install docs/requirements.txt or set MKDOCS",
        "build",
    )


def tool_version(command: list[str]) -> str:
    probe = subprocess.run(
        command + ["--version"], capture_output=True, text=True, check=False
    )
    match = re.search(r"version (\S+)", probe.stdout or "")
    if probe.returncode == 0 and match:
        return match.group(1)
    return Path(command[0]).name


def gate(label: str, present: bool, command: list[str], cwd: Path, env: dict) -> str:
    """Run one verification step; absent steps are recorded, never assumed."""
    if not present:
        log(f"== {label}: not present in the source tree; skipping")
        return "absent"
    result = run(command, cwd=cwd, env=env)
    if result.returncode != 0:
        raise SystemExitMessage(
            EXIT_FAILED, f"{label} failed with exit {result.returncode}", label
        )
    return "pass"


def switch_current(state: Path, release_id: str) -> str | None:
    """Atomically point ``current`` at a release; return the previous id."""
    current = state / "current"
    previous = None
    if current.is_symlink():
        previous = Path(os.readlink(current)).name
    tmp = state / f".current-{os.getpid()}"
    if tmp.is_symlink() or tmp.exists():
        tmp.unlink()
    os.symlink(f"releases/{release_id}", tmp)
    os.replace(tmp, current)
    return previous


def ensure_publish_root(publish_root: Path, state: Path) -> None:
    """The served root is a symlink to the state's current pointer."""
    if publish_root.is_symlink():
        return
    if publish_root.exists():
        raise SystemExitMessage(
            EXIT_FAILED,
            f"publish root {publish_root} is a real directory; "
            "migrate it with --adopt or point SITE_PUBLISH_ROOT at a symlink",
            "publish-root",
        )
    publish_root.parent.mkdir(parents=True, exist_ok=True)
    tmp = publish_root.parent / f".{publish_root.name}-{os.getpid()}"
    os.symlink(state / "current", tmp)
    os.replace(tmp, publish_root)


def prune_releases(state: Path, keep: int, protected: set[str]) -> None:
    releases = state / "releases"
    stale = [entry for entry in releases.glob(".staging-*") if entry.is_dir()]
    for entry in stale:
        make_writable(entry)
        shutil.rmtree(entry, ignore_errors=True)
    keepable = [
        entry.name
        for entry in releases.iterdir()
        if entry.is_dir() and not entry.name.startswith(".")
    ]
    for name in sorted(keepable, reverse=True)[max(0, keep - len(protected)) :]:
        if name in protected:
            continue
        victim = releases / name
        make_writable(victim)
        shutil.rmtree(victim, ignore_errors=True)
        log(f"pruned old release {name}")


def load_release_manifest(state: Path, release_id: str) -> dict | None:
    path = state / "releases" / release_id / "manifest.json"
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text())
    except ValueError:
        return None


def publish(repo: Path, state: Path, publish_root: Path) -> int:
    state.mkdir(parents=True, exist_ok=True)
    (state / "releases").mkdir(exist_ok=True)

    lock_path = state / "publish.lock"
    lock_handle = lock_path.open("w")
    try:
        fcntl.flock(lock_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError as error:
        if error.errno in (errno.EACCES, errno.EAGAIN):
            log("another publisher holds the lock; leaving the site unchanged")
            return EXIT_LOCKED
        raise
    status = Status(state / "manifest.json")

    try:
        commit, resolution = resolve_target(
            repo,
            os.environ.get("SITE_SKIP_PULL", "") == "1",
            os.environ.get("SITE_COMMIT", "").strip() or None,
        )
    except SystemExitMessage as failure:
        status.attempt(utc_now(), "?", None, "failure", "sync")
        status.failed(utc_now(), failure.stage, failure.reason)
        status.save()
        log(f"sync failed: {failure.reason}")
        return failure.code

    current_release = status.data.get("current_release")
    current_manifest = (
        load_release_manifest(state, current_release) if current_release else None
    )
    if current_manifest and current_manifest.get("source_commit") == commit:
        utc = utc_now()
        status.attempt(utc, commit, current_release, "noop", "noop")
        status.succeeded(utc, current_release, commit, True, current_manifest)
        status.save()
        log(f"release {current_release} already serves commit {commit[:10]}; no-op")
        ensure_publish_root(publish_root, state)
        return EXIT_OK

    release_id = f"{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{commit[:7]}"
    staging = state / "releases" / f".staging-{release_id}-{os.getpid()}"
    if staging.exists():
        make_writable(staging)
        shutil.rmtree(staging)
    verification: dict[str, str] = {}

    try:
        with tempfile.TemporaryDirectory(prefix="site-src-") as raw_source:
            source = Path(raw_source)
            log(f"== exporting {resolution} commit {commit[:10]}")
            export_source(repo, commit, source)

            gate_env = dict(os.environ, SITE_PUBLISH_RUNNING="1")
            python = os.environ.get("PYTHON") or sys.executable
            verification["generate_check"] = gate(
                "generate --verify-registry --check",
                (source / "tools" / "site" / "generate_features.py").is_file(),
                [
                    python,
                    "tools/site/generate_features.py",
                    "--verify-registry",
                    "--check",
                ],
                source,
                gate_env,
            )
            verification["unit_tests"] = gate(
                "site unit tests",
                bool(list((source / "tools" / "site").glob("test_*.py")))
                if (source / "tools" / "site").is_dir()
                else False,
                [
                    python,
                    "-m",
                    "unittest",
                    "discover",
                    "-s",
                    "tools/site",
                    "-p",
                    "test_*.py",
                ],
                source,
                gate_env,
            )

            log(f"== building release {release_id}")
            builder = builder_command(repo, source)
            config_name = (
                os.environ.get("MKDOCS_CONFIG", "").strip() or "mkdocs-lan.yml"
            )
            config_path = Path(config_name)
            if not config_path.is_absolute():
                config_path = source / config_path
            result = run(
                builder
                + ["build", "--strict", "-f", str(config_path), "-d", str(staging)],
                cwd=source,
            )
            verification["build"] = "pass" if result.returncode == 0 else "fail"
            if result.returncode != 0:
                raise SystemExitMessage(EXIT_FAILED, "mkdocs build failed", "build")

            verification["check_site"] = gate(
                "check_site",
                (source / "tools" / "site" / "check_site.py").is_file(),
                [python, "tools/site/check_site.py", "--site-dir", str(staging)],
                source,
                gate_env,
            )

            manifest = {
                "schema": MANIFEST_SCHEMA,
                "release_id": release_id,
                "source_commit": commit,
                "source_resolution": resolution,
                "tree_sha": tree_sha256(staging),
                "config": {
                    "name": config_path.name,
                    "sha256": hashlib.sha256(config_path.read_bytes()).hexdigest(),
                },
                "tools": {
                    "python": sys.version.split()[0],
                    "builder": tool_version(builder),
                },
                "built_utc": utc_now(),
                "verification": verification,
            }
            (staging / "manifest.json").write_text(
                json.dumps(manifest, indent=2, sort_keys=True) + "\n"
            )
            make_read_only(staging)
            release_dir = state / "releases" / release_id
            if release_dir.exists():
                existing = load_release_manifest(state, release_id)
                if existing and existing.get("source_commit") == commit:
                    make_writable(staging)
                    shutil.rmtree(staging)
                    release_id_back = current_release or release_id
                    log(f"release {release_id} already exists; keeping it")
                else:
                    raise SystemExitMessage(
                        EXIT_FAILED,
                        f"release id collision at {release_id}",
                        "publish",
                    )
            else:
                os.rename(staging, release_dir)
                release_id_back = release_id

            previous = switch_current(state, release_id_back)
            log(f"== current -> {release_id_back} (was {previous or 'nothing'})")
            utc = utc_now()
            manifest["release_id"] = release_id_back
            status.attempt(utc, commit, release_id_back, "success", "publish")
            status.succeeded(utc, release_id_back, commit, False, manifest)
            status.save()
            ensure_publish_root(publish_root, state)
            keep = int(os.environ.get("SITE_KEEP_RELEASES", "3"))
            protected = {release_id_back} | ({previous} if previous else set())
            prune_releases(state, keep, protected)
            log(f"published {release_id_back}")
            return EXIT_OK
    except SystemExitMessage as failure:
        utc = utc_now()
        status.attempt(
            utc, commit, release_id if release_id else None, "failure", failure.stage
        )
        status.failed(utc, failure.stage, failure.reason)
        status.save()
        log(f"publish failed at {failure.stage}: {failure.reason}")
        return failure.code
    finally:
        if staging.exists():
            make_writable(staging)
            shutil.rmtree(staging, ignore_errors=True)


def main() -> int:
    default_repo = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--repo", default=str(default_repo), help="git repository to publish from"
    )
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    state = Path(
        os.environ.get("SITE_STATE_DIR")
        or os.path.join(
            os.environ.get("XDG_STATE_HOME", str(Path.home() / ".local" / "state")),
            "revit-model-mcp",
        )
    ).resolve()
    # Keep the configured path, not its resolution: after migration it is a
    # symlink chain the server resolves per request, and the publisher must
    # keep flipping the link, not write into its target.
    publish_root = Path(os.environ.get("SITE_PUBLISH_ROOT") or repo / "site")
    return publish(repo, state, publish_root)


if __name__ == "__main__":
    sys.exit(main())
