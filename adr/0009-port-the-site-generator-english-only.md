# 0009. Port the site generator to the 1.0 base, English only

- Status: Accepted
- Date: 2026-10-31
- Amends: [0007](0007-keep-the-site-generator-drop-the-translated-prose.md)

## Context

[0007](0007-keep-the-site-generator-drop-the-translated-prose.md) kept `tools/site/` and dropped the translated
prose. It assumed the site it generated, and a base that could render two languages.

The 1.0 base has no translation plugin. `docs/requirements.in` pins mkdocs-material 9.7.7, mkdocs-llmstxt 0.5.0
and pymdown-extensions 12.1, and `mkdocs.yml` declares `search` and `llmstxt` only. The trunk generator wrote
`.zh.md` and `.en.md` twins and read a `contracts.yaml` of Chinese tool contracts. On this base neither has a
reader, and the `i18n` plugin the twins needed is not installed.

The base also serves 87 tools: 79 from upstream and the fork's eight. The trunk generator rendered the fork's
eight from a hand-written capability file and never looked at the rest. On this base the registry is the only
complete description of the surface, and the generator already knows how to export it.

## Decision

1. **English only.** One page per tool. No twins, no `i18n` plugin, no Chinese labels or headings.
2. **`contracts.yaml` is deleted.** It carried Chinese contract prose only. The English contract for a tool is
   the description the registry already serves.
3. **`capabilities.yaml` keeps the fork's own statements about its eight tools**: group, since, title, summary,
   per-year state, copyable prompts and a usage note, plus the shared groups, year notes, parameter notes and
   parameter defaults. It no longer names the other 79 tools.
4. **The generator renders all 87.** It writes an index, a year matrix, a prompt page, one page per tool and two
   year pages. The eight fork tools additionally carry the prompts, the notes, the read-write gate admonition and
   the `Since` fact; the other 79 render from the registry description and input schema alone.
5. **The generator leaves `docs/index.md` alone.** It writes `docs/features/` and the navigation between
   `# >>> features-nav` and `# <<< features-nav` in `mkdocs.yml`. Upstream's home page stays upstream's.
6. **Grouping follows what the server declares.** Read or action comes from the read-only annotation, and the
   groups come from the toolsets in `server/revit_model_mcp/toolsets.py`. The fork's eight use the groups in
   `capabilities.yaml`. The generator stops when a served tool belongs to no group, to two, or to a toolset with no
   label, so the site cannot quietly drift from the surface.
7. **Year pages state this base's truth.** Revit 2022 to 2027 are the built configurations; Revit 2026 is
   build-only until a workstation verification lands; Revit 2020 is not supported yet, as
   [0006](0006-port-on-2026-first-restore-revit-2020-as-required-follow-up.md) records. No page claims a live
   validation this branch does not have.

## Gate

`pr-checks.yml` runs the generator, its tests, the strict build and the link audit in the step that builds the
documentation. The registry check needs the server, so the step installs it with `uv sync --frozen --no-dev`
first; without that the check would fail on every pull request for a missing console script rather than for a
stale page.

## Consequences

[0007](0007-keep-the-site-generator-drop-the-translated-prose.md)'s bilingual consequence is withdrawn. There is no
uneven language coverage, because there is no second language. Restoring it is a follow-up with its own decision: it
needs a translation plugin on this base and prose that someone owns.

The site now documents the whole surface, so an upstream tool appears without hand-editing and a fork tool appears
with its own prose. Adding a fork action is still two edits: the capability entry and a `--write` run.

## Alternatives rejected

**Carry the trunk pages across.** They describe a 35-tool surface, claim Revit 2020 support this base does not
have, and carry Chinese prose nothing on this base can render.

**Keep `contracts.yaml` for the eight fork tools.** A second English copy of the registry description is a copy that
drifts; the capability file already holds everything the fork says beyond the registry.

**Re-add the translation plugin and port the twins.** That spends the port on a plugin this base does not ship, for
pages upstream rewrote in 1.0 and will rewrite again.
