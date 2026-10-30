# IA, UX and accessibility review

Target: http://192.168.100.120:8099 (288 pages = 144 pairs). Rendered with Playwright 1.58 at 1280/768/390, both themes, print. Shots in `shots/`.

## Findings

| # | Sev | Finding | Evidence | Fix |
|---|---|---|---|---|
| 1 | P1 | Two surfaces are peers, and the newer-sounding one is unpublished. 115 identities are documented twice (35 released + 80 integration); nav puts 功能 before 新版基座, which reads "new platform", and no tool page says "branch, not release". | `mkdocs.yml:233`; the "尚未发布" sentence exists only on the deep landing page, `docs/platform/index.md:3` | Badge the nav labels (`功能 · 0.9.0 已发布` / `新版基座 · 未发布`); persistent 未发布分支 banner above the `h1` on all 80 branch pages |
| 2 | P1 | A reader cannot tell two pages cover one tool. 27 names sit in both sections; 20 carry a **different display title** per surface (`revit_export_view` = 导出视图图片 vs 导出视图为 PNG), 7 carry **identical** ones and collide in `<title>`. Zero pages link to a counterpart. | `docs/features/revit_export_view.md:1` vs `docs/platform/revit_export_view.md:1`; grep `docs/platform/*.md` for `features/` = 0 hits | One canonical title per tool; a generated "发布版：链接" row on every duplicated page, keyed on registry name |
| 3 | P1 | Search is not language-scoped: a Chinese and an English query return the identical set and order — both homes ranked 1–2, released page 4, branch page 5, mixed scripts in every hit. | `mkdocs.yml:94` (no locale config); 28 results for both queries; `shots/ux-search-zh.png`, `ux-search-en.png` | Two indexes keyed on the `/en/` prefix, or a `lang` field plus a filter defaulting to the current locale |
| 4 | P2 | Mobile tables read only sideways, and the squeezed column is the one that matters. 253/288 pages overflow their inner scroller at 390px; 说明 gets 90px of a 462px table. Document width is correct, so nothing looks broken. | `docs/stylesheets/extra.css:580-586`; measured 462/390 and 456/390 on the same tool page; `shots/ux-390-tool.png` | Below 600px fold 默认值/类型 into the 参数 cell; give 说明 the full measure |
| 5 | P2 | The page explaining the split is a dead end: it states the surfaces cannot be mixed, then links to no released tool page, and the site's only bridge runs the wrong way for a reader starting on the branch. | `docs/platform/index.md` → 0 `features/` links; `docs/features/index.md:5` → 1 | Turn it into a decision page: two rows, "want the release / want the branch", entry links both ways, linked from both landings |
| 6 | P2 | Skip link is missing on the three pages a keyboard user lands on first: both homes and 404. It survives on 286/288 and drops wherever the `h1` has no `id`, which is the generated landing markup. | `/`, `/en/`, `/404.html` → `a.md-skip` null; tool page → `href="#png"`; `docs/index.md:14` | Give the landing `h1` an `id`, or hand-write the link in `docs/overrides/main.html` |
| 7 | P2 | "Edit this page" on the homes points at `README.md`, which cannot change them; all other pages route correctly, and contributor guidance repeats the stale claim. | `docs/hooks.py:13`, `:50-53` shadow the generator branch at `:54-66`; homes come from `tools/site/landing.py:479-509`; `CONTRIBUTING.md:108` | Drop the `README.md` entry from the `SOURCES` map so the landing branch wins; fix `CONTRIBUTING.md:108` in the same commit |
| 8 | P2 | The migration page cannot be acted on: 7 of 8 rows are text with no page behind them, and its footer returns only to the platform index. | `docs/platform/fork-tools.md:7-14` (1 linked row of 8), `:48` | Link every row, or say plainly no page exists yet |
| 9 | P3 | Nav hits both limits: 22 tools flat in 视图、图纸与明细表, 12 in 查询与统计, depth 4. Finding a known name means reading 22 siblings. | `mkdocs.yml` nav: 175 nodes, depth 4 | Split the 22 into 视图 / 图纸 / 明细表, or add a nav filter |
| 10 | P3 | A tool page links back only to three indexes, never its own group; the breadcrumb names the group without linking it, so there is no route to a sibling tool. | `tools/site/generate_features.py:322`; `platform_catalog.py:733` | Point the group breadcrumb at its existing `features/index#group-…` anchor |
| 11 | P3 | Search gives no suggestions, and the whole bilingual index downloads every visit. | `.md-search__suggest` empty after 1.8 s with 36 matches; index 1 252 304 B raw / 237 178 B gzip for 288 pages | Suggestions from the same index; size halves once finding 3 is fixed |
| 12 | P3 | Two fact schemas for one tool, and availability is inferred from name equality rather than from the surface — so 有 can appear on a branch page whose contract differs from the released one. | `tools/site/generate_features.py:250-259`; `tools/site/platform_catalog.py:692-696` | One shared fact row, availability derived from the release manifest |

## Template consistency

Counts are per language; zh and en are structurally identical, so every figure doubles site-wide.

- **Released surface (`docs/features/revit_*.md`): 35/35 uniform.** One heading sequence — prompts → parameters → common-parameters → contract → year-support. Two heading sets exist; the second is its English translation.
- **Branch surface (`docs/platform/revit_*.md`): 80/80 uniform.** One sequence — parameters → behavior. 75/80 add common-parameters; the 5 without it (`batch_cancel`, `batch_fetch`, `batch_start`, `batch_status`, `build_report`) have no common fields, so that variation is correct.
- **Deviation is cross-surface, not within a surface.** 0/80 branch pages carry the prompts block or the year-support table that 35/35 released pages have. 32/70 released files carry the write-gate `!!! warning`; 0/160 branch files do. 66/70 released files carry a `!!! note`; 2/160 branch files do.
- **One tool, two documents.** Of 27 shared identities, 20 disagree on display title and 7 agree — and those 7 produce the duplicate `<title>` values. 10 duplicate title pairs total (7 tool collisions + home, v2020, v2026 locale pairs).
- The generators enforce consistency inside each surface; nothing reconciles them: uniform pages, incoherent catalogue.

## A11y verification table

| Check | Result | Evidence |
|---|---|---|
| One `h1`, no level skips | pass | 288/288, full-site scan |
| `img` alt meaningful | pass | 2 content images, bilingual and descriptive |
| Tables have header rows | pass | `th` on every table |
| Tables keyboard-scrollable | pass | `tabindex=0`; Tab reached `.md-typeset__table focus-visible` |
| Code focusable, copy buttons named | pass | 420 buttons, 0 unnamed; 0 overflowing `pre` without `tabindex` |
| Contrast AA, both themes | pass | min sampled 4.57:1 (partial badge); body 18.31 light / 16.82 dark |
| `focus-visible` | pass | `rgb(0,95,184) solid 2px` |
| Reduced motion | pass | durations → 0.001 ms, reveal opacity 1 |
| SR names: icons, toggle, expanders, search | pass | labelled; expanders carry `role` + `aria-expanded` |
| Landmarks | pass | exactly 1 `main` + `article` everywhere |
| Skip link | **fail** | absent on `/`, `/en/`, `/404.html` |
| Unique document titles | **fail** | 10 duplicate pairs |
| Print | pass | nav hidden; tables 794/792 at A4; code `pre-wrap` |
| Dark/light parity | pass | nothing breaks on landing or deep page |

## Verified good (do not regress)

Per-directory sitemaps; OS-driven dark mode; OG/Twitter meta; self-hosted fonts; table measure inside the column; 404 entry links; inert drawer (`inert=true` closed, 217.8px open); named search dialog; AA contrast on six sampled pages in both themes; mobile tab order; `prefers-reduced-motion`; `toc.follow` on a 16-heading page (active link y=463.8); prev/next and breadcrumbs on 286 pages; expanders keyboard-operable; clean print; the drawing-sheet tokens (`extra.css:115`, `:577-638`) hold on deep pages.
