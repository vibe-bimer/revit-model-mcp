# 0007. Keep the site generator, drop the translated prose

- Status: Accepted
- Date: 2026-10-30

## Context

This fork carries a documentation site generator and a bilingual site.

The generator is a small system: `tools/site/generate_features.py` (632 lines) reads the live MCP registry, exports `tools/site/content/tools.json`, and renders the tool and contract pages from two hand-written sources, `capabilities.yaml` (1131 lines) and `contracts.yaml` (351 lines). `check_site.py` (275 lines) verifies internal references, and the whole thing is already gated in CI with `--verify-registry --check`.

The bilingual half is content: eighteen `.en.md` files paired with Chinese originals, plus translated README, CONTRIBUTING and SECURITY files.

The two halves have opposite economics under a rebase. The generator depends on the MCP registry, which this fork owns and which upstream cannot invalidate; it keeps working and keeps being true. The translations are prose about pages upstream rewrote: upstream 1.0 restructured thirteen documentation files, and every one of them has a translated twin here that would need re-translating against new content.

## Decision

Keep the mechanism. Drop the prose.

- Keep `tools/site/`, its tests, its CI gate and its operational scripts.
- Keep `capabilities.yaml` and `contracts.yaml` as the fork's own statements about its own tool surface. They describe actions upstream does not have.
- Drop the eighteen `.en.md` pairs and the translated top-level documents. Re-add translations only for pages the fork writes itself.
- Upstream documentation arrives in English and stays English. Translating it is a maintenance debt with no owner.

## Consequences

The site's language coverage becomes uneven for a while: fork-specific pages bilingual, inherited pages English only. That is visible and honest. The alternative is a site whose translations silently describe a previous release.

Whoever wants a translated page now argues for that specific page, instead of the repository carrying a blanket promise.

The generator keeps paying off: adding a fork action updates the tool pages without hand-editing them, and the `--verify-registry` check fails the build when the published surface and the registry disagree.

## Alternatives rejected

**Drop the site completely.** Would remove a working generator that costs nothing under the rebase, and would delete the only place the fork states its own tool surface in a user-facing form.

**Keep everything, re-translate the thirteen rewritten pages.** That is roughly the same work as porting an action, spent on prose that upstream will rewrite again. It also competes with the eight actions for the same weeks.
