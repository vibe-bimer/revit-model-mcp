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
HASHED = ("main.", "palette.", "bundle.", "search.")


def cache_control(path: Path) -> str:
    name = path.name
    if path.suffix in (".css", ".js") and any(h in name for h in HASHED):
        # The theme puts a content hash in the filename, so the bytes behind the URL never change.
        return "public, max-age=31536000, immutable"
    if path.suffix in (".woff2", ".png", ".gif", ".jpg", ".jpeg", ".webp", ".ico"):
        return "public, max-age=604800"
    # Everything else keeps its name across a rebuild, so it must be revalidated.
    return "no-cache"


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

    def _resolve(self) -> Path | None:
        raw = urlsplit(self.path).path
        parts = [part for part in unquote(raw).split("/") if part not in ("", ".")]
        if any(part == ".." for part in parts):
            return None
        target = self.root.joinpath(*parts)
        if raw.endswith("/") or target.is_dir():
            target = target / "index.html"
        try:
            resolved = target.resolve()
        except OSError:
            return None
        if resolved != self.root and self.root not in resolved.parents:
            return None
        return resolved if resolved.is_file() else None

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

    def _respond(self, body: bool) -> None:
        path = self._resolve()
        if path is None:
            self._not_found(body)
            return

        stat = path.stat()
        etag = f'"{stat.st_mtime_ns:x}-{stat.st_size:x}"'
        last_modified = formatdate(stat.st_mtime, usegmt=True)

        if self._is_fresh(etag, stat.st_mtime):
            self.send_response(HTTPStatus.NOT_MODIFIED)
            self.send_header("ETag", etag)
            self.send_header("Cache-Control", cache_control(path))
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

        data = path.read_bytes() if body else b""
        encoding = None
        if (
            body
            and path.suffix in COMPRESSIBLE
            and stat.st_size >= MIN_GZIP_BYTES
            and "gzip" in self.headers.get("Accept-Encoding", "")
        ):
            data = self._compressed(path, data)
            encoding = "gzip"

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", self._content_type(path))
        self.send_header("Content-Length", str(stat.st_size if not body else len(data)))
        self.send_header("Last-Modified", last_modified)
        self.send_header("ETag", etag)
        self.send_header("Cache-Control", cache_control(path))
        self.send_header("X-Content-Type-Options", "nosniff")
        if encoding:
            self.send_header("Content-Encoding", encoding)
            self.send_header("Vary", "Accept-Encoding")
        self.end_headers()
        if body:
            self.wfile.write(data)

    def _is_fresh(self, etag: str, mtime: float) -> bool:
        if self.headers.get("If-None-Match"):
            return etag in [
                candidate.strip()
                for candidate in self.headers["If-None-Match"].split(",")
            ]
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
        page = self.root / "404.html"
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
    root = Path(sys.argv[2] if len(sys.argv) > 2 else "site").resolve()
    if not (root / "index.html").is_file():
        print(f"{root} holds no index.html; build the site first", file=sys.stderr)
        return 1
    DocsHandler.root = root
    server = Server(("0.0.0.0", port), DocsHandler)
    print(f"serving {root} on http://0.0.0.0:{port}/", file=sys.stderr)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
