"""Resolve the mkdocs executable for the publisher and the dual-build checker.

Both scripts used to carry their own copy of this lookup, and the copies drifted:
one split ``MKDOCS`` on whitespace (breaking a path with spaces), the other used
``shlex`` and also fell back to ``uv run --with-requirements``. This module is the
single source of that policy.
"""

from __future__ import annotations

import os
import shlex
import shutil
from pathlib import Path


class BuilderNotFound(Exception):
    """No mkdocs executable could be resolved."""


def builder_command(repo: Path, source: Path | None = None) -> list[str]:
    """Return the command that runs mkdocs for ``repo``.

    Resolution order: an explicit ``MKDOCS`` value (shell-quoted, so a path with
    spaces stays a single argument), a virtualenv inside ``repo``, the developer's
    ``~/.venv-docs``, a ``mkdocs`` on ``PATH``, and finally ``uv run
    --with-requirements source/docs/requirements.txt`` when ``source`` carries the
    requirements file and ``uv`` is available.
    """
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
    if source is not None:
        requirements = source / "docs" / "requirements.txt"
        if requirements.is_file() and shutil.which("uv"):
            return ["uv", "run", "--with-requirements", str(requirements), "mkdocs"]
    raise BuilderNotFound(
        "mkdocs was not found; install docs/requirements.txt or set MKDOCS"
    )
