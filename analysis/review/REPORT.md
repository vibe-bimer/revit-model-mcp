# Revit Model MCP documentation site — review and remediation

Target: <http://192.168.100.120:8099> · Bar: awwwards / Webby / FWA standard
Method: live capture (Playwright, 1440 and 390 px, light and dark), source and pipeline review,
two independent deep audits (content accuracy; accessibility and performance), then measure–fix–remeasure.

## Outcome

| Measure | Before | After |
| --- | --- | --- |
| Homepage wire transfer | 1,367.9 KiB | **626.4 KiB** (−54%) |
| Feature page wire transfer | 1,357.0 KiB | **382.0 KiB** (−72%) |
| Homepage HTML (wire) | 57.7 KiB uncompressed | **12.5 KiB** gzipped (−78%) |
| First contentful paint | 1112 ms median | **828–1044 ms**, no third-party font round trip |
| Contrast failures (6 pages × 2 themes) | 1 light / 3–4 dark per page | **0** |
| Mobile tab stops outside the viewport | 23 of first 30 | **1 of 30** (a deliberate scroll-region stop) |
| Requests returning 4xx per page view | 2 (sitemap) | **0** |
| Deployed source maps | 1.29 MB | **0** |
| Documentation-site URL correctness | `site_url` 404s; deep links stale | **flagged**, not changed — a maintainer decision |

## What was wrong, and what was done

### Functional defects (every visitor saw these)

1. **`sitemap.xml` 404 on every subpage.** Material 9.7.7 resolves the alternate-language lookup as
   `new URL("sitemap.xml", pageUrl)`, so `/features/` asked for `/features/sitemap.xml`. Fixed in
   `docs/hooks.py` with an `on_post_build` hook that writes a real per-directory sitemap (124 of them,
   each the subset of the root sitemap that covers its own pages).
2. **Dark mode ignored the operating system.** The palette had no `media` condition, so a
   dark-preference visitor always landed in light mode. Both palette entries now declare
   `media: "(prefers-color-scheme: ...)"`, in the base config and in the i18n English override.
3. **No social or search metadata at all** — the entire `<head>` was charset, viewport, generator.
   Added a description, Open Graph and Twitter card (including the social card that already existed in
   `docs/assets` but was referenced nowhere), `theme-color` for both schemes, and JSON-LD.
4. **Web fonts came from the Google Fonts CDN**, which is wrong for a LAN-served site and cost
   ~660 ms of first paint. Three variable families are now self-hosted as six woff2 files (224 KB
   total, latin and latin-ext only, CJK falls through to the platform face).
5. **Tables rendered at half the column width** — Material wraps them in an `inline-block` that
   shrink-wraps, so a two-column table was 511 px wide inside a 908 px column. Pre-existing; fixed.
6. **`content.action.edit` pointed at generated files.** Editing `docs/index.md` or a feature page by
   hand is overwritten by the next generator run. The hook now points those pages at the file that
   produces them, and the landing page hides the control entirely.

### Design — the award-standard gap

The site was stock Material with 1.8 KB of custom CSS: no art direction, no landing page, no type
scale, no motion, no imagery.

The direction taken is **the drawing sheet**, because the product is architectural documentation:
hairline rules with end ticks, a modular grid, monospaced data, sheet-numbered sections and measured
motion. The mark's three-plate isometric stack is grown into a full structural frame for the hero.

- **Design system** (`docs/stylesheets/extra.css`): colour, type, space and motion tokens for both
  schemes; a mapped Material variable layer; Space Grotesk for display, Inter for text, JetBrains Mono
  for data; restyled header, navigation, search, tables, code, admonitions and footer.
- **Landing page** (`tools/site/landing.py` + `docs/stylesheets/landing.css`): hero with an animated
  axonometric SVG that draws itself in, a spec strip, a prompt showcase that separates read from action,
  the eight capability groups, the real output of `revit_export_view`, the request path, the two-gate
  model and the setup steps. Every number comes from the tool registry and every prompt from
  `capabilities.yaml`, so the page cannot drift from the product.
- **404** (`docs/overrides/404.html`): was a bare `404 - Not found` heading on an empty page. Now
  carries the code in the display face, bilingual copy, three entry buttons and six common
  destinations, with every link absolute against `site_url` because the page answers at any depth.
- **Footer** (`docs/overrides/partials/copyright.html`): the theme's bare attribution line now names
  the project, its licence, the source repository and the privacy and security pages, per locale,
  while keeping the Material credit.
- **Motion** (`docs/javascripts/site.js`): scroll reveal, hero draw-in, reading-progress hairline,
  copy-to-clipboard on prompt cards — all disabled under `prefers-reduced-motion`, and content stays
  visible if the script never runs.

### Accessibility

- **23 of the first 30 mobile tab stops were off-screen**: the closed off-canvas drawer stayed
  focusable. Now `inert` when parked, which removes all of them.
- **Search overlay was `role="dialog"` with an empty name**; navigation expanders were focusable labels
  with no role, name or state. Now named, `role="button"` with `aria-expanded` kept in sync, and the
  icon-only expander carries its section name (the theme already activated these on Enter and Space, so
  no key handling was invented).
- **Contrast**: the tertiary ink token measured 4.36:1 on white and 4.10:1 on the panel surface. Every
  text/surface pair on six pages in both themes now passes WCAG AA.

### Content

An independent audit of both languages found, and a second pass fixed: action-tool counts of 14
against the registry's 16 in `server/README`, the manual test plan and the validation page;
`revit_create_level` missing from the manual test plan and from the batch allow-list; "nine model-edit
tools" where the registry has thirteen with `dry_run`; a stale as-of date and a stale 2026 action list;
`since` values that contradicted the changelog; a README action list missing four of sixteen tools;
stale "before the first PyPI release" hedging; a Chinese term split between 接单 and 拾取; an
unexplained `RevitDevLoader` path; and a roadmap still listing gaps its own note calls closed.

Two real bugs were found by reading the generator rather than the site:

- **`tools/site/generate_features.py:376`** escaped its f-string braces, so the support matrix published
  the literal text `{'#read-tools' if read_only else '#action-tools'}` as a heading, and neither anchor
  existed.
- **`docs/features/revit_export_view.md`** inherited a third spelling, `任务领取等待预算`, from
  `contracts.yaml`.

### Serving

The LAN site was served by `python3 -m http.server`: no compression, no validators, no cache headers,
HTTP/1.0. `scripts/serve-site.py` replaces it with gzip (cached against file mtime), ETag and
`If-None-Match`/`If-Modified-Since`, `Cache-Control` (one year immutable for the theme's hashed bundles,
revalidation for the unhashed ones), HTTP/1.1 keep-alive, the site's own `404.html`, and no directory
listings. The systemd unit and `scripts/serve-site.sh` use it.

## Escalated, not changed

These are maintainer decisions about which repository publishes, not documentation defects:

- `README.md` and `install.ps1` send readers to `sharafutdinovdi/revit-model-mcp`, whose latest release
  is **v0.7.0**, while the docs describe **0.9.0 / 35 tools**. The current release line lives in the
  fork, `vibe-bimer/revit-model-mcp`.
- `mkdocs.yml`'s `site_url` (`https://vibe-bimer.github.io/revit-model-mcp/`) returns **404**, while
  every deep link in the docs points at the upstream Pages site, which is a build roughly a year behind
  and 404s on `/features/revit_model_health/` and `/features/matrix/`.
- `server/server.json` advertises PyPI version 0.9.0; PyPI's latest is 0.7.0.

## Known limitations

- The search index is 0.9 MB (243 KiB on the wire). It is requested after `load`, so it does not affect
  first paint, and removing `search.suggest` does not avoid it — measured, then restored.
- The exported-view PNG is 243 KiB at 2100×806, displayed at about half that. Optimising it is a
  one-line change for whoever owns the asset.
- `api.github.com` is called for repository statistics; it fails while the unauthenticated rate limit is
  exhausted on this host, which is environmental rather than a site defect.
- 4.6 MiB of `docs/screenshots/` is copied into the build and referenced only by the GitHub README,
  never by a page. Left in place rather than silently excluded.
- `docs/modeling-tools.md` was skimmed rather than read end to end in the content audit.

## Verification

```
python3 tools/site/generate_features.py --verify-registry --check   # 83 files, 0 changed
python3 -m unittest discover -s tools/site -p 'test_*.py'           # 22 tests, OK
python3 tools/site/check_site.py --site-dir site                    # 124 pages, 14308 refs, 0 errors
uvx ruff==0.16.7 check tools/site/ docs/hooks.py scripts/serve-site.py   # All checks passed
uvx ruff==0.16.7 format --check ...                                 # 4 files already formatted
```

Live checks: zero 4xx on five pages in both locales; zero contrast failures across six pages in both
themes; drawer `inert`; search dialog named; 19 expanders with role and state; one off-screen tab stop,
which is Material's intentional scroll-region stop. Content is served gzip-encoded with ETag and
Cache-Control; the theme's content-hashed bundles are immutable for a year.
