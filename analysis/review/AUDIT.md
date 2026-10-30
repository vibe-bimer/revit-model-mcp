# Revit Model MCP documentation site — quality review

Target: <http://192.168.100.120:8099>
Bar: awwwards / Webby / FWA award standard.
Method: live capture (Playwright, desktop 1440 + mobile 390, light + dark), source inspection,
build pipeline review (`mkdocs-lan.yml`, `scripts/update-site.sh`, `tools/site/check_site.py`).

Build facts: MkDocs 1.6.1 + Material 9.7.7, mkdocs-static-i18n 1.3.1, 126 built pages
(64 zh / 62 en), 124 Markdown sources, ~16 MB site, build time ~5 s.

## Findings

### P1 — functional defects (visible to every visitor)

| # | Finding | Evidence | Impact |
| --- | --- | --- | --- |
| F1 | `sitemap.xml` is requested with a **relative** URL, so every subpage 404s twice (zh + en) | Material 9.7.7 bundle does `new URL("sitemap.xml", pageUrl)`; Playwright network log shows `404 /features/sitemap.xml`, `404 /en/features/sitemap.xml` on every non-root page | Broken Material alternate-language prefetch, 2 failed requests per page view, console noise |
| F2 | **Dark mode ignores the OS preference** — a dark-preference visitor always lands in light mode | `prefers-color-scheme: dark` → `body[data-md-color-scheme="default"]`, `background: rgb(255,255,255)`; palette CSS contains no `prefers-color-scheme` query | Site fights the user's system setting on first visit |
| F3 | **No social/SEO metadata at all** — the whole `<head>` is charset, viewport, generator | `grep '<meta'` on the built homepage returns 3 tags; no description, OG, Twitter card, `theme-color`, robots | No share preview, weak search result, no brand control |
| F4 | A social card exists but is **unused and stale** | `docs/assets/social-card.{html,png}` built into the site but referenced nowhere; footer says `github.com/sharafutdinovdi/revit-model-mcp` while `repo_url` is `vibe-bimer/revit-model-mcp` | Dead asset, wrong project URL |
| F5 | Web fonts are loaded from the **Google Fonts CDN** | `<link rel="preconnect" href="https://fonts.gstatic.com">` in every page | LAN/offline visitors get fallback fonts (the site is served over LAN); third-party request per page load |

### P2 — design quality (the award-standard gap)

| # | Finding | Evidence | Impact |
| --- | --- | --- | --- |
| D1 | **No art direction.** Stock MkDocs Material with 1.8 KB of custom CSS that only sets a brand colour and table tweaks | `docs/stylesheets/extra.css` is 55 lines, mostly table/code fixes | Indistinguishable from thousands of Material sites |
| D2 | **No landing page.** The homepage is a Markdown page: an `h1`, a facts line, a paragraph and a card grid | `home_page()` in `tools/site/generate_features.py` | No value proposition above the fold, no product visual, no narrative |
| D3 | **No typographic system.** Default Roboto at the Material default scale; no display face, no scale, no optical rhythm | Rendered screenshots | Flat hierarchy; headings and body read at nearly the same weight |
| D4 | **No colour system.** One flat `#005FB8` used for primary, light and dark; no accent or semantic ramp beyond three ad-hoc badge colours | `extra.css` lines 1–5, 52–55 | No depth, no state language, no dark-mode tuning |
| D5 | **No motion or interaction design.** Nothing beyond Material defaults | Source inspection | No delight, no scroll craft, no feedback |
| D6 | **No imagery.** Two PNGs and one 3.1 MB GIF total | `docs/screenshots/` | Nothing to look at; the product's visual nature is unrepresented |
| D7 | Landing page has **no mobile-specific treatment** and the card grid is unmodified Material | mobile captures | Generic |

### P3 — performance and hygiene

| # | Finding | Evidence |
| --- | --- | --- |
| P1 | 3.1 MB unoptimised GIF shipped as-is | `site/screenshots/revit-model-mcp_claude-desktop.gif` |
| P2 | Source maps shipped to production (+1.2 MB) | `bundle.*.min.js.map` (1.0 MB), `search.*.min.js.map` |
| P3 | Images have no `loading="lazy"`, no width/height | built HTML |
| P4 | Search index is 0.9 MB and loaded eagerly | `site/search/search_index.json` |

### P4 — verified as already good (do not regress)

- One `h1` per page, no heading-level skips, `lang` correct per build.
- Skip link present; `main`/`nav`/`footer` landmarks present.
- Every `<img>` has non-empty `alt`.
- zh/en page pairs complete; `check_site.py` enforces links, anchors, language pairs and
  prose-language ratio, and fails closed.
- `scripts/update-site.sh` keeps the previous build until the new one passes, then swaps atomically.
- `prefers-reduced-motion` is honoured for CSS animation and hides the GIF.
