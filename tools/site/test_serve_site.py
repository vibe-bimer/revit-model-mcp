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
    (root / "assets" / "main.css").write_text("body{padding:0}", encoding="utf-8")
    (root / "assets" / "logo.png").write_bytes(b"\x89PNG\r\n\x1a\n" + b"0" * 64)
    (root / "assets" / "photo.0123456789ab.png").write_bytes(
        b"\x89PNG\r\n\x1a\n" + b"1" * 64
    )
    (root / "sitemap.xml").write_text(SITEMAP_XML, encoding="utf-8")
    (root / "sitemap.xml.gz").write_bytes(gzip.compress(SITEMAP_XML.encode("utf-8")))
    (root / "404.html").write_text(
        "<html><body>missing page 未找到</body></html>", encoding="utf-8"
    )
    (root / "en").mkdir()
    (root / "en" / "404.html").write_text(
        "<html><body>Page not found · 页面不存在</body></html>", encoding="utf-8"
    )
    # A deployment that asks crawlers to stay out still serves its own pages: robots is a hint,
    # not access control, and the error surface below does not consult it.
    (root / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    (root / "favicon.ico").write_bytes(b"\x00\x00\x01\x00" + b"0" * 60)
    (root / "emptydir").mkdir()


class ServeSiteTestCase(unittest.TestCase):
    """Starts one real server per test class against a temporary site."""

    site_root: Path

    @classmethod
    def prepare(cls, root: Path) -> None:
        """Create the site this class serves; subclasses may reshape the tree."""
        build_site(root)

    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.site_root = Path(cls.temp.name)
        cls.prepare(cls.site_root)
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


class EncodingNegotiationTests(ServeSiteTestCase):
    def test_gzip_disabled_by_q0_falls_back_to_identity(self):
        status, headers, body = self.request(
            "GET", "/big.html", {"Accept-Encoding": "gzip;q=0"}
        )
        self.assertEqual(status, 200)
        self.assertNotIn("content-encoding", headers)
        self.assertEqual(body.decode("utf-8"), BIG_PAGE)

    def test_identity_disabled_prefers_gzip_for_compressible(self):
        status, headers, body = self.request(
            "GET", "/big.html", {"Accept-Encoding": "identity;q=0"}
        )
        self.assertEqual(status, 200)
        self.assertEqual(headers.get("content-encoding"), "gzip")
        self.assertEqual(gzip.decompress(body).decode("utf-8"), BIG_PAGE)

    def test_all_representations_excluded_answers_406(self):
        cases = [
            ("/big.html", "gzip;q=0, identity;q=0"),
            ("/assets/logo.png", "identity;q=0"),
            ("/assets/logo.png", "*;q=0"),
            ("/assets/logo.png", "gzip;q=0, *;q=0"),
        ]
        for target, encoding in cases:
            with self.subTest(target=target, encoding=encoding):
                status, _, _ = self.request(
                    "GET", target, {"Accept-Encoding": encoding}
                )
                self.assertEqual(status, 406)

    def test_star_q0_with_explicit_gzip_still_serves_gzip(self):
        status, headers, _ = self.request(
            "GET", "/big.html", {"Accept-Encoding": "*;q=0, gzip"}
        )
        self.assertEqual(status, 200)
        self.assertEqual(headers.get("content-encoding"), "gzip")

    def test_x_gzip_is_accepted(self):
        status, headers, _ = self.request(
            "GET", "/big.html", {"Accept-Encoding": "x-gzip"}
        )
        self.assertEqual(status, 200)
        self.assertEqual(headers.get("content-encoding"), "gzip")

    def test_small_compressible_file_stays_identity(self):
        status, headers, body = self.request("GET", "/", {"Accept-Encoding": "gzip"})
        self.assertEqual(status, 200)
        self.assertNotIn("content-encoding", headers)
        self.assertIn("home", body.decode("utf-8"))

    def test_missing_accept_encoding_serves_identity(self):
        status, headers, body = self.request("GET", "/big.html")
        self.assertEqual(status, 200)
        self.assertNotIn("content-encoding", headers)
        self.assertEqual(body.decode("utf-8"), BIG_PAGE)

    def test_head_selects_the_same_gzip_representation_as_get(self):
        get = self.request("GET", "/big.html", {"Accept-Encoding": "gzip"})
        head = self.request("HEAD", "/big.html", {"Accept-Encoding": "gzip"})
        self.assertEqual(head[0], 200)
        self.assertEqual(head[2], b"")
        self.assertEqual(head[1].get("content-encoding"), "gzip")
        self.assertEqual(head[1]["content-length"], get[1]["content-length"])
        self.assertEqual(int(get[1]["content-length"]), len(get[2]))
        self.assertEqual(head[1]["etag"], get[1]["etag"])

    def test_etag_differs_between_encodings(self):
        _, gzipped, _ = self.request("GET", "/big.html", {"Accept-Encoding": "gzip"})
        _, plain, _ = self.request("GET", "/big.html", {"Accept-Encoding": "identity"})
        self.assertNotEqual(gzipped["etag"], plain["etag"])
        self.assertTrue(gzipped["etag"].startswith('"'))
        self.assertIn('-gzip"', gzipped["etag"])

    def test_vary_present_for_compressible_representations(self):
        for encoding in ("gzip", "identity"):
            with self.subTest(encoding=encoding):
                _, headers, _ = self.request(
                    "GET", "/big.html", {"Accept-Encoding": encoding}
                )
                self.assertEqual(headers.get("vary"), "Accept-Encoding")

    def test_no_vary_for_incompressible_assets(self):
        _, headers, _ = self.request(
            "GET", "/assets/logo.png", {"Accept-Encoding": "gzip"}
        )
        self.assertNotIn("vary", headers)


class ConditionalRequestTests(ServeSiteTestCase):
    def _fresh_headers(self, target, encoding="identity"):
        headers = self.request("GET", target, {"Accept-Encoding": encoding})[1]
        conditional = {"Accept-Encoding": encoding, "If-None-Match": headers["etag"]}
        return headers, conditional

    def test_if_none_match_star_returns_304(self):
        _, _, _ = self.request("GET", "/big.html")
        status, _, _ = self.request("GET", "/big.html", {"If-None-Match": "*"})
        self.assertEqual(status, 304)

    def test_if_none_match_takes_precedence_over_if_modified_since(self):
        _, headers, _ = self.request("GET", "/big.html")
        status, _, body = self.request(
            "GET",
            "/big.html",
            {
                "If-None-Match": '"stale-opaque-tag"',
                "If-Modified-Since": headers["last-modified"],
            },
        )
        self.assertEqual(status, 200)
        self.assertEqual(body.decode("utf-8"), BIG_PAGE)

    def test_stale_if_modified_since_still_returns_200(self):
        status, _, _ = self.request(
            "GET", "/big.html", {"If-Modified-Since": "Mon, 01 Jan 2001 00:00:00 GMT"}
        )
        self.assertEqual(status, 200)

    def test_gzip_304_keeps_validators_and_vary(self):
        _, headers, _ = self.request("GET", "/big.html", {"Accept-Encoding": "gzip"})
        status, not_modified, body = self.request(
            "GET",
            "/big.html",
            {"Accept-Encoding": "gzip", "If-None-Match": headers["etag"]},
        )
        self.assertEqual(status, 304)
        self.assertEqual(body, b"")
        self.assertEqual(not_modified["etag"], headers["etag"])
        self.assertIn('-gzip"', not_modified["etag"])
        self.assertEqual(not_modified.get("vary"), "Accept-Encoding")
        self.assertEqual(not_modified["cache-control"], headers["cache-control"])

    def test_identity_304_does_not_match_gzip_etag(self):
        _, headers, _ = self.request("GET", "/big.html", {"Accept-Encoding": "gzip"})
        status, _, _ = self.request(
            "GET",
            "/big.html",
            {"Accept-Encoding": "identity", "If-None-Match": headers["etag"]},
        )
        self.assertEqual(status, 200)

    def test_head_conditional_returns_304(self):
        _, headers, _ = self.request("GET", "/big.html")
        status, _, body = self.request(
            "HEAD", "/big.html", {"If-None-Match": headers["etag"]}
        )
        self.assertEqual(status, 304)
        self.assertEqual(body, b"")


class SitemapTests(ServeSiteTestCase):
    def test_gzipped_sitemap_downloads_as_application_gzip(self):
        status, headers, body = self.request("GET", "/sitemap.xml.gz")
        self.assertEqual(status, 200)
        self.assertEqual(headers["content-type"], "application/gzip")
        self.assertNotIn("content-encoding", headers)
        self.assertEqual(gzip.decompress(body).decode("utf-8"), SITEMAP_XML)

    def test_gzipped_sitemap_is_never_recompressed(self):
        status, headers, body = self.request(
            "GET", "/sitemap.xml.gz", {"Accept-Encoding": "gzip"}
        )
        self.assertEqual(status, 200)
        self.assertEqual(headers["content-type"], "application/gzip")
        self.assertNotIn("content-encoding", headers)
        self.assertEqual(gzip.decompress(body).decode("utf-8"), SITEMAP_XML)

    def test_plain_sitemap_serves_as_xml(self):
        status, headers, body = self.request("GET", "/sitemap.xml")
        self.assertEqual(status, 200)
        self.assertTrue(headers["content-type"].startswith("application/xml"))
        self.assertNotIn("content-encoding", headers)
        self.assertEqual(body.decode("utf-8"), SITEMAP_XML)


class CachePolicyTests(ServeSiteTestCase):
    def test_content_hashed_assets_cache_immutably(self):
        for target in (
            "/assets/main.0123456789ab.css",
            "/assets/photo.0123456789ab.png",
        ):
            with self.subTest(target=target):
                status, headers, _ = self.request("GET", target)
                self.assertEqual(status, 200)
                self.assertEqual(
                    headers["cache-control"], "public, max-age=31536000, immutable"
                )

    def test_unhashed_assets_revalidate(self):
        for target in (
            "/assets/plain.css",
            "/assets/main.css",
            "/assets/logo.png",
            "/big.html",
            "/sitemap.xml",
            "/sitemap.xml.gz",
        ):
            with self.subTest(target=target):
                status, headers, _ = self.request("GET", target)
                self.assertEqual(status, 200)
                self.assertEqual(headers["cache-control"], "no-cache")


class RootSwitchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.site_a = base / "site-a"
        self.site_b = base / "site-b"
        for site, label in ((self.site_a, "site A"), (self.site_b, "site B")):
            site.mkdir()
            (site / "index.html").write_text(f"<html>{label}</html>", encoding="utf-8")
        self.link = base / "current"
        self.link.symlink_to(self.site_a)
        serve_site.DocsHandler.root = self.link
        self.server = serve_site.Server(("127.0.0.1", 0), serve_site.DocsHandler)
        self.port = self.server.server_address[1]
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=10)
        self.tmp.cleanup()

    def _get_root(self):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
        try:
            conn.request("GET", "/")
            response = conn.getresponse()
            return response.status, response.read()
        finally:
            conn.close()

    def test_symlinked_root_follows_retargeting_without_restart(self):
        status, body = self._get_root()
        self.assertEqual(status, 200)
        self.assertIn(b"site A", body)

        self.link.unlink()
        self.link.symlink_to(self.site_b)

        status, body = self._get_root()
        self.assertEqual(status, 200)
        self.assertIn(b"site B", body)

    def test_index_absent_in_configured_root_still_serves_after_target_gains_one(self):
        empty = Path(self.tmp.name) / "empty"
        empty.mkdir()
        self.link.unlink()
        self.link.symlink_to(empty)
        status, _ = self._get_root()
        self.assertEqual(status, 404)

        (empty / "index.html").write_text("<html>late</html>", encoding="utf-8")
        status, body = self._get_root()
        self.assertEqual(status, 200)
        self.assertIn(b"late", body)


class AssetErrorTests(ServeSiteTestCase):
    """A missing asset gets a small plain-text error, not the whole error page."""

    ASSET_PATHS = (
        "/missing.png",
        "/screenshots/revit-model-mcp_gone.gif",
        "/assets/nope.js",
        "/stylesheets/gone.css",
        "/javascripts/gone.js",
        "/fonts/missing.woff2",
        "/nothing.txt",
        "/data.json",
    )

    def test_missing_assets_answer_404_with_a_light_body(self):
        for target in self.ASSET_PATHS:
            with self.subTest(target=target):
                status, headers, body = self.request("GET", target)
                self.assertEqual(status, 404)
                self.assertEqual(headers["content-type"], "text/plain; charset=utf-8")
                self.assertLess(len(body), 2048)
                self.assertNotIn(b"<html", body)
                self.assertEqual(headers["cache-control"], "no-store")

    def test_the_root_icon_serves_a_pinned_content_type(self):
        status, headers, _ = self.request("GET", "/favicon.ico")
        self.assertEqual(status, 200)
        self.assertEqual(headers["content-type"], "image/vnd.microsoft.icon")

    def test_a_document_path_still_gets_the_readable_error_page(self):
        for target in ("/missing", "/does-not-exist/", "/features/gone/"):
            with self.subTest(target=target):
                status, headers, body = self.request("GET", target)
                self.assertEqual(status, 404)
                self.assertTrue(headers["content-type"].startswith("text/html"))
                self.assertIn("未找到", body.decode("utf-8"))
                self.assertEqual(headers["cache-control"], "no-cache")

    def test_head_reports_the_same_length_as_get_for_asset_errors(self):
        get_status, get_headers, get_body = self.request("GET", "/missing.png")
        head_status, head_headers, head_body = self.request("HEAD", "/missing.png")
        self.assertEqual(get_status, head_status)
        self.assertEqual(head_body, b"")
        self.assertEqual(head_headers["content-length"], get_headers["content-length"])
        self.assertEqual(int(head_headers["content-length"]), len(get_body))

    def test_head_reports_the_same_length_as_get_for_document_errors(self):
        get_status, _, get_body = self.request("GET", "/missing/")
        head_status, head_headers, head_body = self.request("HEAD", "/missing/")
        self.assertEqual(get_status, head_status)
        self.assertEqual(head_body, b"")
        self.assertEqual(int(head_headers["content-length"]), len(get_body))
        self.assertGreater(len(get_body), 0)


class ErrorPageLanguageTests(ServeSiteTestCase):
    """English paths get the English error page; everything else gets the root one."""

    def test_english_path_gets_the_english_error_page(self):
        status, _, body = self.request("GET", "/en/does-not-exist/")
        self.assertEqual(status, 404)
        self.assertIn("Page not found", body.decode("utf-8"))
        self.assertNotIn("未找到", body.decode("utf-8"))

    def test_chinese_path_gets_the_root_error_page(self):
        status, _, body = self.request("GET", "/does-not-exist/")
        self.assertEqual(status, 404)
        self.assertIn("未找到", body.decode("utf-8"))
        self.assertNotIn("Page not found", body.decode("utf-8"))

    def test_english_asset_error_stays_light(self):
        status, headers, body = self.request("GET", "/en/missing.png")
        self.assertEqual(status, 404)
        self.assertEqual(headers["content-type"], "text/plain; charset=utf-8")
        self.assertLess(len(body), 2048)


class ErrorPageFallbackTests(ServeSiteTestCase):
    """A site built without the English variant falls back to the root page."""

    @classmethod
    def prepare(cls, root: Path) -> None:
        build_site(root)
        (root / "en" / "404.html").unlink()

    def test_english_path_falls_back_to_the_root_error_page(self):
        status, _, body = self.request("GET", "/en/does-not-exist/")
        self.assertEqual(status, 404)
        self.assertIn("未找到", body.decode("utf-8"))


class RobotsHintTests(ServeSiteTestCase):
    """robots.txt is served as a file and never gates a response."""

    def test_robots_is_served_as_plain_text(self):
        status, headers, body = self.request("GET", "/robots.txt")
        self.assertEqual(status, 200)
        self.assertTrue(headers["content-type"].startswith("text/plain"))
        self.assertIn(b"Disallow: /", body)

    def test_a_disallow_all_robots_does_not_gate_pages(self):
        status, _, _ = self.request("GET", "/")
        self.assertEqual(status, 200)

    def test_a_disallow_all_robots_does_not_change_error_surfaces(self):
        status, headers, _ = self.request("GET", "/missing.png")
        self.assertEqual(status, 404)
        self.assertEqual(headers["content-type"], "text/plain; charset=utf-8")
        status, headers, _ = self.request("GET", "/missing/")
        self.assertEqual(status, 404)
        self.assertTrue(headers["content-type"].startswith("text/html"))


if __name__ == "__main__":
    unittest.main()
