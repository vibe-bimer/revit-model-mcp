#!/usr/bin/env python3
"""Serve the built documentation on a LAN.

`python3 -m http.server` sends no compression, no validators and no cache headers, so every page view
re-downloads the whole site: the audit measured 1.3 MB per view of the homepage, of which gzip alone
removes about 80%. This server keeps the same "static files from a directory" contract and adds:

  * gzip for compressible types, with the compressed body cached against the file's mtime;
  * ETag and Last-Modified with If-None-Match / If-Modified-Since, so a repeat view is a 304;
  * Cache-Control: one year immutable for the theme's content-hashed bundles, revalidation for
    everything else, because stylesheets/extra.css and javascripts/site.js are not hashed;
  * HTTP/1.1 with keep-alive instead of one connection per file;
  * the site's own 404.html instead of a bare error page, and no directory listings.

Usage: serve-site.py [port] [directory]
"""

from __future__ import annotations

import gzip
import mimetypes
import re
import sys
import threading
from email.utils import formatdate, parsedate_to_datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import ClassVar
from urllib.parse import unquote, urlsplit

COMPRESSIBLE = {
    ".css",
    ".html",
    ".js",
    ".json",
    ".map",
    ".md",
    ".svg",
    ".txt",
    ".xml",
}
# Fonts and images are already compressed; running gzip over them costs CPU and saves nothing.
MIN_GZIP_BYTES = 1024
# A run of eight or more hex digits in the filename stem is the build's content hash.
FINGERPRINT = re.compile(r"[0-9a-f]{8,}")


def cache_control(path: Path) -> str:
    if FINGERPRINT.search(path.stem):
        # The filename embeds a content hash, so the bytes behind the URL never change.
        return "public, max-age=31536000, immutable"
    # Everything else keeps its name across a rebuild, so it must be revalidated.
    return "no-cache"


def parse_accept_encoding(header: str | None) -> tuple[dict[str, float], float | None]:
    """Split an Accept-Encoding header into named codings and the star quality.

    Codings that are not named inherit the star quality when present, and the
    default of 1.0 otherwise, per RFC 9110 section 12.5.3.
    """
    entries: dict[str, float] = {}
    star: float | None = None
    for item in (header or "").split(","):
        parts = item.strip().split(";")
        coding = parts[0].strip().lower()
        quality = 1.0
        for param in parts[1:]:
            name, _, value = param.strip().partition("=")
            if name.strip().lower() == "q":
                try:
                    quality = float(value)
                except ValueError:
                    pass
        if not coding:
            continue
        if coding == "*":
            star = quality
        else:
            entries[coding] = quality
    return entries, star


def _quality(coding: str, entries: dict[str, float], star: float | None) -> float:
    if coding in entries:
        return entries[coding]
    return star if star is not None else 1.0


def _gzip_quality(entries: dict[str, float], star: float | None) -> float:
    if "gzip" in entries:
        return entries["gzip"]
    if "x-gzip" in entries:
        return entries["x-gzip"]
    return star if star is not None else 1.0


def select_encoding(suffix: str, size: int, header: str | None) -> str | None:
    """Choose the representation to serve, or None when none is acceptable.

    Unlisted codings default to quality 1, so excluding identity with
    ``identity;q=0`` still allows the (implicit) gzip representation, and a
    star rule excludes everything it covers. The server only compresses on
    its own initiative when the client explicitly named gzip, x-gzip or *.
    """
    entries, star = parse_accept_encoding(header)
    identity_ok = _quality("identity", entries, star) > 0
    gzip_ok = _gzip_quality(entries, star) > 0
    gzip_endorsed = any(k in entries for k in ("gzip", "x-gzip")) or star is not None
    if (
        suffix in COMPRESSIBLE
        and size >= MIN_GZIP_BYTES
        and gzip_ok
        and (gzip_endorsed or not identity_ok)
    ):
        return "gzip"
    if identity_ok:
        return "identity"
    return None


def etag_for(stat, encoding: str) -> str:
    """Strong validator of one representation, distinct per content coding."""
    base = f"{stat.st_mtime_ns:x}-{stat.st_size:x}"
    return f'"{base}-gzip"' if encoding == "gzip" else f'"{base}"'


class _BadRequest(Exception):
    """The request target cannot be decoded into a safe path."""


class DocsHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "RevitModelMcpDocs"
    sys_version = ""

    root: ClassVar[Path]
    _cache: ClassVar[dict[tuple[str, int, int], bytes]] = {}
    _lock: ClassVar[threading.Lock] = threading.Lock()

    def log_message(self, fmt, *args):
        # Name and signature are fixed by BaseHTTPRequestHandler.
        sys.stderr.write(f"{self.address_string()} - {fmt % args}\n")

    # -- request handling ---------------------------------------------------

    def do_GET(self):
        # Name is fixed by BaseHTTPRequestHandler.
        self._respond(body=True)

    def do_HEAD(self):
        # Name is fixed by BaseHTTPRequestHandler.
        self._respond(body=False)

    def _resolve(self) -> tuple[Path | None, str | None]:
        """Map the request target to a file, a redirect target, or a 404."""
        # Resolve the root on every request so swapping the served symlink
        # takes effect without a restart.
        root = self.root.resolve()
        split = urlsplit(self.path)
        raw = split.path
        try:
            decoded = unquote(raw, errors="strict")
        except UnicodeDecodeError:
            # Percent escapes that are not valid UTF-8 cannot name a file.
            raise _BadRequest from None
        if "\x00" in decoded:
            raise _BadRequest
        parts = [part for part in decoded.split("/") if part not in ("", ".")]
        if any(part == ".." for part in parts):
            return None, None
        target = root.joinpath(*parts)
        is_dir = target.is_dir()
        trailing = decoded.endswith("/")

        if parts and parts[-1] == "index.html":
            # An explicit index URL only serves content when its directory is
            # canonical; otherwise it falls through to a plain 404.
            if (target.parent / "index.html").is_file():
                return None, self._canonical(parts[:-1], split.query)
        elif is_dir and not trailing and (target / "index.html").is_file():
            # A bare directory URL redirects to its canonical form once; a
            # directory without an index has no canonical form to serve.
            return None, self._canonical(parts, split.query)

        if trailing or is_dir:
            target = target / "index.html"
        try:
            resolved = target.resolve()
        except (OSError, ValueError):
            # ValueError covers paths the filesystem layer cannot even name.
            raise _BadRequest from None
        if resolved != root and root not in resolved.parents:
            return None, None
        return (resolved if resolved.is_file() else None), None

    def _canonical(self, segments: list[str], query: str) -> str:
        url = "/" + "/".join(segments + [""]) if segments else "/"
        return f"{url}?{query}" if query else url

    def _redirect(self, location: str) -> None:
        self.send_response(HTTPStatus.MOVED_PERMANENTLY)
        self.send_header("Location", location)
        self.send_header("Content-Length", "0")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()

    def _compressed(self, path: Path, data: bytes) -> bytes:
        stat = path.stat()
        key = (str(path), stat.st_mtime_ns, stat.st_size)
        with self._lock:
            cached = self._cache.get(key)
        if cached is None:
            cached = gzip.compress(data, 6)
            with self._lock:
                if len(self._cache) > 256:
                    self._cache.clear()
                self._cache[key] = cached
        return cached

    def _representation(self, path: Path, encoding: str) -> bytes:
        data = path.read_bytes()
        if encoding == "gzip":
            data = self._compressed(path, data)
        return data

    def _respond(self, body: bool) -> None:
        try:
            path, redirect = self._resolve()
        except _BadRequest:
            self.send_error(HTTPStatus.BAD_REQUEST, "Invalid request target")
            return
        if redirect is not None:
            self._redirect(redirect)
            return
        if path is None:
            self._not_found(body)
            return

        stat = path.stat()
        encoding = select_encoding(
            path.suffix, stat.st_size, self.headers.get("Accept-Encoding")
        )
        if encoding is None:
            self.send_error(HTTPStatus.NOT_ACCEPTABLE, "No acceptable representation")
            return
        etag = etag_for(stat, encoding)

        if self._is_fresh(etag, stat.st_mtime):
            self.send_response(HTTPStatus.NOT_MODIFIED)
            self.send_header("ETag", etag)
            self.send_header("Cache-Control", cache_control(path))
            if path.suffix in COMPRESSIBLE:
                self.send_header("Vary", "Accept-Encoding")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

        # GET and HEAD under identical headers must see the same
        # representation, so the payload is built regardless of the method.
        payload = self._representation(path, encoding)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", self._content_type(path))
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Last-Modified", formatdate(stat.st_mtime, usegmt=True))
        self.send_header("ETag", etag)
        self.send_header("Cache-Control", cache_control(path))
        self.send_header("X-Content-Type-Options", "nosniff")
        if encoding == "gzip":
            self.send_header("Content-Encoding", "gzip")
        if path.suffix in COMPRESSIBLE:
            self.send_header("Vary", "Accept-Encoding")
        self.end_headers()
        if body:
            self.wfile.write(payload)

    def _is_fresh(self, etag: str, mtime: float) -> bool:
        if_none_match = self.headers.get("If-None-Match")
        if if_none_match:
            candidates = [c.strip() for c in if_none_match.split(",")]
            # "*" matches any current representation of the resource.
            return "*" in candidates or etag in candidates
        if self.headers.get("If-Modified-Since"):
            try:
                since = parsedate_to_datetime(self.headers["If-Modified-Since"])
            except (TypeError, ValueError):
                return False
            return int(mtime) <= int(since.timestamp())
        return False

    _TYPES: ClassVar[dict[str, str]] = {
        ".woff2": "font/woff2",
        ".js": "text/javascript; charset=utf-8",
        ".mjs": "text/javascript; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".json": "application/json; charset=utf-8",
        ".svg": "image/svg+xml",
        ".xml": "application/xml; charset=utf-8",
        # A stored *.xml.gz file is a gzip download, not XML with a coding.
        ".gz": "application/gzip",
        ".webmanifest": "application/manifest+json",
    }

    def _content_type(self, path: Path) -> str:
        known = self._TYPES.get(path.suffix)
        if known:
            return known
        guessed, _ = mimetypes.guess_type(path.name)
        if not guessed:
            return "application/octet-stream"
        if guessed.startswith("text/") and "charset" not in guessed:
            return f"{guessed}; charset=utf-8"
        return guessed

    def _not_found(self, body: bool) -> None:
        page = self.root.resolve() / "404.html"
        if not page.is_file():
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return
        data = page.read_bytes() if body else b""
        self.send_response(HTTPStatus.NOT_FOUND)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        if body:
            self.wfile.write(data)


class Server(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def main() -> int:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8099
    root = Path(sys.argv[2] if len(sys.argv) > 2 else "site")
    if not (root / "index.html").is_file():
        print(f"{root} holds no index.html; build the site first", file=sys.stderr)
        return 1
    # Keep the configured path; each request resolves it so a symlinked root
    # can be retargeted while the server keeps running.
    DocsHandler.root = root
    server = Server(("0.0.0.0", port), DocsHandler)
    print(f"serving {root.resolve()} on http://0.0.0.0:{port}/", file=sys.stderr)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
