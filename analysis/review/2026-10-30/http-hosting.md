# HTTP and hosting review

Probes: `http://192.168.100.120:8099`, 2026-10-30 22:19–22:31 (+0800); build `site/` (288 pages), pid 969. **No P0**: nothing breaks for a visitor landing on `/` and following links.

| # | Severity | Finding | Evidence | Fix |
| --- | --- | --- | --- | --- |
| 1 | P1 | Production serves uncommitted work, and the guarded publish path has been dead 27 days: the 900 s timer skips on any dirty tree, exits 0, and systemd reports success. | Log: 2,716 blocks, 2,591 `skipping pull AND publish`; last automated publish `2026-10-03T00:00:52` (124 pages); `git status --porcelain` = 57 files; live `/en/features/` has `class="state part"` ×8, absent at HEAD (`git show HEAD:docs/features/index.en.md`). | Gate the dirty test inside `scripts/update-site.sh:26` so the manual path honours it; exit non-zero on skip (`scripts/site-cron.sh:14-17`). |
| 2 | P1 | No redirect to the canonical trailing-slash URL: `/features` and `/features/index.html` serve identical bytes to `/features/`, and on the no-slash form sibling-relative links resolve one level too high. | All three → 200, 107595 B, one ETag. Links of `/features` resolved against `/features`: 40 refs 404; `/platform/revit_ping` 81; `/en/platform/revit_ping` 81. | `scripts/serve-site.py:86-88`: 301 slashless dir paths and `/index.html` to the dir URL. |
| 3 | P1 | HEAD does not mirror GET: compression is skipped while Content-Length reports the uncompressed size and Content-Encoding is dropped. | GET `/`+gzip → `15066` + `Content-Encoding: gzip`; HEAD `/` → `114395`, no encoding. HEAD `/nope.html` → `Content-Length: 0`, GET → 95039 B. | `serve-site.py:128-148`: build headers before branching on `body`; real 404 length at `:194-197`. |
| 4 | P1 | hreflang alternates are relative URLs, which the spec forbids, so the alternate set is void. Canonical is correct. | `/en/features/`: canonical `http://192.168.100.120:8099/en/features/`, but `alternate href="../../features/"`, `href="./"`. Plugin-emitted (`grep -rn hreflang docs/overrides` → no hits). | Absolutise `rel="alternate"` hrefs against `config.site_url` in `docs/hooks.py` `on_post_build`. |
| 5 | P2 | `/sitemap.xml.gz` is served as `application/xml` with no `Content-Encoding`: 4,748 B of gzip labelled XML; `nosniff` blocks recovery. | `curl -sI /sitemap.xml.gz` → 200, `Content-Type: application/xml`; body gunzips to 115,874 B. Encoding discarded at `serve-site.py:182`. | Delete the unreferenced `.gz` in `on_post_build`, or map `.gz` → `application/gzip`. |
| 6 | P2 | Every miss (`/favicon.ico`, `/robots.txt`, `/manifest.webmanifest`, `/.well-known/security.txt`) returns the 95,039 B HTML 404 page; only `assets/favicon.svg` is declared. | Each returns `404 text/html; charset=utf-8 95039`. | Add `robots.txt`, `favicon.ico`, a manifest; serve a 200 B `text/plain` 404 for non-HTML. |
| 7 | P2 | `Vary: Accept-Encoding` is sent only on the compressed 200; 304s omit `Last-Modified` which the 200 sets. | `curl -sI /` (no gzip) → no Vary; 304 `/search/search_index.json` → ETag + Cache-Control + `Content-Length: 0` (`serve-site.py:146-148` vs `:120-126`). | Send Vary on every compressible response; add `Last-Modified` to 304 (RFC 9110 §15.4.5). |
| 8 | P2 | Unfingerprinted images and fonts get a 7-day non-revalidating TTL, so rebuilt screenshots stay stale for a week. | `/assets/social-card.png`, `/screenshots/*.png`, `/assets/fonts/*.woff2` → `public, max-age=604800`; none carry a hash. | `serve-site.py:52-53`: `no-cache` for unhashed assets, or hash the names. |
| 9 | P2 | `GET /%00` gets no response and dumps a traceback: the null byte raises `ValueError`, and `_resolve` catches only `OSError` (`target.is_dir()` sits outside the try). | `curl /%00` → exit 52; journal 22:24:51 `ValueError: embedded null byte`. | `serve-site.py:81-95`: `except (OSError, ValueError)` around the resolve. |
| 10 | P2 | Publish is two renames: between them the served path is gone, so concurrent requests hit `send_error`'s bare page. No rollback — `site.prev` is deleted straight after. | `scripts/update-site.sh:56-62`; `ls site.prev site.new` → absent; `serve-site.py:190-192`. | Serve through a `current` symlink swapped with `mv -T`; keep one generation. |
| 11 | P3 | `If-None-Match: *` → 200 not 304, weak validators never match; no `Range`/`Accept-Ranges`; `Server:` has a trailing space. | `serve-site.py:153-158`; `If-None-Match: *` → 200; `Range: bytes=0-99` → 200, no `Content-Range`; `curl -sI / \| grep -i server \| cat -A` → `RevitModelMcpDocs $`. | Handle `*`/`W/`; decline Range; drop `sys_version`. |

## Verified good (do not regress)

- 288/288 sitemap URLs return 200; 334 page-referenced assets resolve; 0 content-type mismatches.
- Every `immutable` response is genuinely hashed (three theme bundles plus `workers/search.*.js`); no unhashed file is immutable.
- ETag and If-Modified-Since both yield 304 with 0 bytes; keep-alive reuses a socket; TTFB 2.1–2.3 ms; homepage 114,395 → 15,066 B; search index 1,252,304 → 237,178 B.
- The Oct-3 per-directory sitemap fix holds: `/features/`, `/en/features/`, `/platform/`, `/features/revit_ping/`, `/en/platform/revit_ping/` each hold exactly their own entry.
- Canonical and `og:url` carry the LAN origin at all six sampled depths — `mkdocs-lan.yml` wins, the Pages `site_url` does not leak.
- Traversal blocked in four encodings; 0 symlinks; the 404 status is real and its links root-absolute, so it renders at depth.
- `check_site.py` exits 1 before the rename; `flock -n` blocks concurrent builds.

## Latent risks (not defects today)

- `HASHED` is a substring rule (`serve-site.py:44,49-51`): a future unhashed `main.*`/`bundle.*`/`search.*` asset inherits one-year immutable, uncorrectable for returning visitors.
- The gzip body cache clears wholesale past 256 entries (`:105-106`), so the 1.2 MB search index is recompressed under churn.
- `mkdocs-lan.yml` hardcodes `192.168.100.120:8099`: canonical, sitemap and `og:url` break silently if the IP or port moves.
- No alert on skip or failure beyond a log line (`scripts/site-cron.sh:16`) — which is how 27 days of no-ops passed unnoticed, and it rebuilds unconditionally even when HEAD is unchanged.
