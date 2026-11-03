from __future__ import annotations

import os
from pathlib import Path


def canonical(path: str | os.PathLike[str]) -> str:
    """Return the path string the server reports for a written file.

    The server resolves the parent directory before writing, so an 8.3 short
    temp path expands to its long form and the directory keeps the case of the
    on-disk entry. On Windows tmp_path can differ in case from that entry, so
    assertions compare against this value instead of str(tmp_path).
    """
    candidate = Path(path).expanduser().absolute()
    return str(candidate.parent.resolve() / candidate.name)
