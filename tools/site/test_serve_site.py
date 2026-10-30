"""HTTP black-box tests for the documentation server.

The tests start the real server from ``scripts/serve-site.py`` on an ephemeral
port against a temporary site, then drive it with ``http.client``. GET and HEAD
are always compared under identical request headers, per the site review spec.
"""

import gzip
import http.client
import importlib.util
import tempfile
import threading
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_SPEC = importlib.util.spec_from_file_location(
    "serve_site", REPO_ROOT / "scripts" / "serve-site.py"
)
serve_site = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(serve_site)
# The server logs every request to stderr; tests assert through HTTP instead.
serve_site.DocsHandler.log_message = lambda *args, **kwargs: None

BIG_PAGE = "<html><body>" + "参数说明与工具契约正文。" * 80 + "</body></html>"
SITEMAP_XML = (
    '<?xml version="1.0" encoding="UTF-8"?>'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
)


def build_site(root: Path) -> None:
    """Create a minimal but representative static site under *root*."""
    (root / "index.html").write_text(
        "<html><body>home 首页</body></html>", encoding="utf-8"
    )
    (root / "big.html").write_text(BIG_PAGE, encoding="utf-8")
    (root / "features").mkdir()
    (root / "features" / "index.html").write_text(
        "<html><body>features 目录</body></html>", encoding="utf-8"
    )
    (root / "features" / "nested").mkdir(parents=True)
    (root / "features" / "nested" / "deep.html").write_text(
        "<html><body>deep page</body></html>", encoding="utf-8"
    )
    (root / "assets").mkdir()
    (root / "assets" / "main.0123456789ab.css").write_text(
        "body{color:#222}" * 40, encoding="utf-8"
    )
    (root / "assets" / "plain.css").write_text("body{margin:0}", encoding="utf-8")
    (root / "assets" / "logo.png").write_bytes(b"\x89PNG\r\n\x1a\n" + b"0" * 64)
    (root / "sitemap.xml").write_text(SITEMAP_XML, encoding="utf-8")
    (root / "sitemap.xml.gz").write_bytes(gzip.compress(SITEMAP_XML.encode("utf-8")))
    (root / "404.html").write_text(
        "<html><body>missing page 未找到</body></html>", encoding="utf-8"
    )
    (root / "emptydir").mkdir()


class ServeSiteTestCase(unittest.TestCase):
    """Starts one real server per test class against a temporary site."""

    site_root: Path

    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.site_root = Path(cls.temp.name)
        build_site(cls.site_root)
        serve_site.DocsHandler.root = cls.site_root
        cls.server = serve_site.Server(("127.0.0.1", 0), serve_site.DocsHandler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)
        cls.temp.cleanup()

    def request(self, method, target, headers=None):
        """Issue one request and return ``(status, lowercase headers, body)``."""
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
        try:
            conn.request(method, target, headers=headers or {})
            response = conn.getresponse()
            body = response.read()
            headers = {k.lower(): v for k, v in response.getheaders()}
            return response.status, headers, body
        finally:
            conn.close()


class ServingBaselineTests(ServeSiteTestCase):
    def test_root_page_serves_html(self):
        status, headers, body = self.request("GET", "/")
        self.assertEqual(status, 200)
        self.assertTrue(headers["content-type"].startswith("text/html"))
        self.assertIn("home", body.decode("utf-8"))
        self.assertEqual(int(headers["content-length"]), len(body))

    def test_missing_path_returns_site_404_page(self):
        status, headers, body = self.request("GET", "/missing")
        self.assertEqual(status, 404)
        self.assertIn("未找到", body.decode("utf-8"))
        self.assertEqual(headers["cache-control"], "no-cache")

    def test_deep_page_serves(self):
        status, _, body = self.request("GET", "/features/nested/deep.html")
        self.assertEqual(status, 200)
        self.assertIn("deep page", body.decode("utf-8"))

    def test_head_matches_identity_get(self):
        get_status, get_headers, get_body = self.request("GET", "/big.html")
        head_status, head_headers, head_body = self.request("HEAD", "/big.html")
        self.assertEqual(get_status, head_status, 200)
        self.assertEqual(head_body, b"")
        self.assertEqual(head_headers["content-length"], get_headers["content-length"])
        self.assertEqual(int(get_headers["content-length"]), len(get_body))

    def test_gzip_representation_round_trips(self):
        status, headers, body = self.request(
            "GET", "/big.html", {"Accept-Encoding": "gzip"}
        )
        self.assertEqual(status, 200)
        self.assertEqual(headers.get("content-encoding"), "gzip")
        self.assertEqual(gzip.decompress(body).decode("utf-8"), BIG_PAGE)

    def test_etag_revalidation_returns_304(self):
        _, headers, _ = self.request("GET", "/big.html")
        status, not_modified, _ = self.request(
            "GET", "/big.html", {"If-None-Match": headers["etag"]}
        )
        self.assertEqual(status, 304)
        self.assertEqual(not_modified["etag"], headers["etag"])

    def test_last_modified_revalidation_returns_304(self):
        _, headers, _ = self.request("GET", "/big.html")
        status, _, _ = self.request(
            "GET", "/big.html", {"If-Modified-Since": headers["last-modified"]}
        )
        self.assertEqual(status, 304)


class RobustnessTests(ServeSiteTestCase):
    def test_nul_percent_encoding_is_controlled_400(self):
        status, _, _ = self.request("GET", "/%00")
        self.assertEqual(status, 400)

    def test_nul_head_request_is_controlled_400(self):
        status, _, body = self.request("HEAD", "/%00")
        self.assertEqual(status, 400)
        self.assertEqual(body, b"")

    def test_invalid_utf8_percent_encoding_is_controlled_400(self):
        status, _, _ = self.request("GET", "/%ff%fe")
        self.assertEqual(status, 400)

    def test_parent_escape_variants_are_404(self):
        for target in (
            "/%2e%2e/secret",
            "/a/../index.html",
            "/features/../../etc/passwd",
            "/features/%2e%2e%2f%2e%2e%2fetc/passwd",
        ):
            with self.subTest(target=target):
                status, _, _ = self.request("GET", target)
                self.assertEqual(status, 404)

    def test_absolute_paths_are_404(self):
        for target in ("//etc/passwd", "/%2fetc%2fpasswd"):
            with self.subTest(target=target):
                status, _, _ = self.request("GET", target)
                self.assertEqual(status, 404)

    def test_server_keeps_answering_after_bad_targets(self):
        for target in ("/%00", "/%ff%fe", "/%2e%2e/secret"):
            try:
                self.request("GET", target)
            except (http.client.HTTPException, OSError):
                pass
        status, _, _ = self.request("GET", "/")
        self.assertEqual(status, 200)


class CanonicalRedirectTests(ServeSiteTestCase):
    def test_bare_directory_redirects_with_trailing_slash(self):
        status, headers, body = self.request("GET", "/features")
        self.assertEqual(status, 301)
        self.assertEqual(headers["location"], "/features/")
        self.assertEqual(body, b"")

    def test_redirect_preserves_query_string(self):
        status, headers, _ = self.request("GET", "/features?a=1&b=%E4%B8%AD")
        self.assertEqual(status, 301)
        self.assertEqual(headers["location"], "/features/?a=1&b=%E4%B8%AD")

    def test_explicit_index_redirects_to_directory(self):
        status, headers, _ = self.request("GET", "/features/index.html")
        self.assertEqual(status, 301)
        self.assertEqual(headers["location"], "/features/")

    def test_root_index_redirects_to_root(self):
        status, headers, _ = self.request("GET", "/index.html")
        self.assertEqual(status, 301)
        self.assertEqual(headers["location"], "/")

    def test_head_redirects_without_body(self):
        status, headers, body = self.request("HEAD", "/features")
        self.assertEqual(status, 301)
        self.assertEqual(headers["location"], "/features/")
        self.assertEqual(body, b"")

    def test_canonical_directory_url_serves_without_redirect(self):
        status, headers, body = self.request("GET", "/features/")
        self.assertEqual(status, 200)
        self.assertNotIn("location", headers)
        self.assertIn("features", body.decode("utf-8"))

    def test_missing_paths_stay_404_without_redirect(self):
        for target in ("/missing", "/missing/", "/features/absent.html"):
            with self.subTest(target=target):
                status, headers, _ = self.request("GET", target)
                self.assertEqual(status, 404)
                self.assertNotIn("location", headers)

    def test_directory_without_index_stays_404(self):
        for target in ("/emptydir", "/emptydir/"):
            with self.subTest(target=target):
                status, headers, _ = self.request("GET", target)
                self.assertEqual(status, 404)
                self.assertNotIn("location", headers)

    def test_redirect_chain_terminates_at_canonical_url(self):
        status, headers, _ = self.request("GET", "/features")
        location = headers["location"]
        status, headers, _ = self.request("GET", location)
        self.assertEqual(status, 200)
        self.assertNotIn("location", headers)


if __name__ == "__main__":
    unittest.main()
