# Upstream update delta: 1.0.0 shipped and what changed since the 2026-10-13 research

- Research date: 2026-10-30, Asia/Shanghai.
- Upstream: `sharafutdinovdi/revit-model-mcp`, HEAD `760bb7c` (2026-10-20). Released `v0.10.0` (`24a23cc`, 2026-10-12) and `v1.0.0` (`27c1c45`, 2026-10-16), plus 11 post-1.0.0 commits.
- Local baseline: unchanged since the prior research — HEAD `5afcb55` (2026-10-02), fork version `0.9.0`, 55 fork-only commits, merge base `5a65afc` (v0.5.0+6).
- Relationship to [`upstream-update-research-2026-10-13.md`](upstream-update-research-2026-10-13.md): that report covers upstream through `c1e23f5`, which already contained all 0.10.0 feature content. This delta report covers only `c1e23f5..760bb7c` and refreshes the merge numbers. Nothing from the prior report has been implemented on `main` yet.

## 1. What is new upstream since the prior research

Sixteen commits: the `0.10.0` and `1.0.0` release commits themselves, plus:

| Commit | Change | Value for this fork |
| --- | --- | --- |
| `27c1c45` | **v1.0.0 published.** The 1.x stability promise is now anchored at a released tag, not a HEAD claim. | Raises the value and lowers the long-term cost of aligning to upstream now; the gap keeps growing (~133 commits, +67k lines vs fork's +21k). |
| `bdf5cdf` (#298) | Recover from document switches mid-session; bounded catalog results (`name` filter + `limit`); code dry-run transaction fix; wildcard family audits bounded with a complete skipped list; URLs preserved during redaction. | Directly relevant to long MCP sessions and to the fork's rebuild/export flows. Port the "resolve the addressed open document" pattern when porting anything. |
| `d765ecb` (#297) | Read-path performance: process-wide caches for built-in parameter names, JSON serializers, warning reads; streaming JSON for top-level flags; lazy workbook/report imports. | Borrow the caching pattern for the fork's read path; especially the element-id export and instance listing. |
| `32b6528` (#302) | Transport loss reported as retryable structured error (`transport_unavailable`) instead of an opaque failure. | Small, self-contained, portable as-is into the fork's channel error handling. |
| `058bb28` (#305) | `pickup_timeout_seconds` removed from every tool schema; now only the `REVIT_MCP_PICKUP_TIMEOUT_SECONDS` server environment variable (default 300 s). Old spellings get a migration message. | Largest single contract drift vs the fork: 43 local sites still pass it as an explicit argument. |
| `dc1bcd4` (#301) | `family_audit` compact by default; unlabelable dimensions skipped quietly. | Only relevant after porting the family audit. |
| `3b0969d` (#300) | Missing target document reported as "not open" (2-line change in `ControlChannel.cs`). | Trivially portable wording fix. |
| `dc5c1f6`, `ebc4d98`, `f6e8f56`, `760bb7c` | CI parallelization with caches; Revit SDK/Toolkit/Polyfill bumps (SDK 6.3.2); drop tests asserting on C# source text; uv 0.13.4. | Infra only; take with the build alignment slice. |
| `8ddd24a`, `33d2639`, `9b488cb`, `8436cb5` | README live footage + quick start refresh; `inputSchema` in the store MCP manifest; test polish. | Reference material. |

## 2. Refreshed comparison numbers

- Tools: merge base 27 (18 read + 9 action) → local 35 (19 read + 16 opt-in action) → upstream 79. Fork-only tools: 8 (`revit_create_floor`, `revit_create_level`, `revit_set_phase`, `revit_merge_phases`, `revit_set_view_lighting`, `revit_reset_element_ids`, `revit_rebuild_model_ids`, `revit_export_element_ids`). None exist upstream.
- Server architecture: local `server/revit_model_mcp/` is 8 modules (v0.5.x layout); upstream is 24 (`actions.py` 323 → 1967 lines, `revit_channel.py` 525 → 1018). The fork's `0.9.0` version string and upstream's `0.9.x` line are number collisions, not shared code.
- Merge preview (`git merge --no-ff upstream/main`, temp worktree): **50 conflicted paths** — `docs/` 13, Addin 9, root 8, all 7 workflows, `server/revit_model_mcp/` 4, Core 3. Worst single file: `src/RevitModelMcp.Core/Control/ActionJobParser.cs` (13 hunks, both sides extended the action enum). Upstream adds two new projects (`RevitModelMcp.BatchSupervisor`, `RevitModelMcp.Updater`), so the `.sln` conflicts structurally. Cherry-picking through this divergence is not realistic file-by-file.
- Parameter drift vs upstream `server.py` `_RENAMED_ARGUMENTS`: `timeout_seconds`/`wait_seconds`/`dest_dir` already clean locally; `save_to` → `output_path` still wrong in 22 local sites; `pickup_timeout_seconds` now an unknown argument upstream (43 local sites).
- Same-name, different-contract hazards: `revit_list_instances` returns a bare list locally vs `{instances, ...}` upstream; local `revit_batch` (one multi-step undoable action) collides in prefix with upstream `revit_batch_start/status/cancel/fetch` (supervised model collection) and upstream renamed the local semantic to `revit_run_actions`; upstream `revit_set_parameter` takes `ParameterValue` (str|int|float) plus `parameter_id`, local only `value: str`.

## 3. Decision points that gate any update

1. **Write-permission default.** Upstream 1.0 removed `REVIT_MCP_ALLOW_WRITE`/`allow-write` and ships actions enabled by default with `REVIT_MCP_READ_ONLY` opt-out plus a three-layer machine policy (registry → ProgramData `policy.json`, fail-closed, ADMX templates, MSI properties `READONLY`/`EXECUTECODE`/`UPDATEMODE`). The fork's hard rule is read-only by default with dual opt-in gates. Aligning the skeleton without a decision silently flips users to default-on actions. Either re-impose the fork gates on top of the aligned skeleton or consciously adopt the upstream model with policy as the restriction layer.
2. **Same-major pairing.** The upstream server refuses a different-major add-in (`fileChannelVersion` = 2, legacy feed files and `views-dump` removed). Server and add-in must move to upstream 1.x as one deployed pair; a half-upgraded mix cannot work.
3. **Version line.** `release-please-config.json` is byte-identical on both sides; only the manifest differs (`0.9.0` vs `1.0.0`). After any alignment the fork's releases continue from `1.x` (`bump-minor-pre-major: false` → next feat is `1.1.0`). Fork release history 0.6.0–0.9.0 stays in `CHANGELOG.md`.
4. **Local bug found during the audit, independent of upstream:** `bundle/manifest.json` `tools[]` lists only the 19 read tools — none of the fork's 16 action tools are registered in the bundle manifest. Fix first; it is a live defect.

## 4. Updated recommendation

The prior report's family-by-family adoption order stands, with two amendments:

1. **Prefer skeleton alignment over slice-by-slice porting if more than the security batch is wanted.** With upstream at a stable 1.0 contract and the fork at 50-way conflicts, re-basing the fork's unique value onto the upstream skeleton (re-inserting the 8 tools under upstream's `@action` + `ActionStep` + three allowlists convention, R20 build entries, bilingual site, and the chosen write gates) is now cheaper than hand-porting 52 tools and the channel rewrite. Security fixes (#7 of the prior report) stay independently portable as a first batch regardless.
2. **New borrow-now items from the post-1.0 commits:** the `transport_unavailable` retryable error shape (`32b6528`), the missing-document wording fix (`3b0969d`), the document-switch recovery pattern (`bdf5cdf`), and the read-path caching pattern (`d765ecb`). The `pickup_timeout_seconds` → environment variable move (`058bb28`) should be adopted with any channel work to erase the largest drift.

Contribution candidates back to upstream (smallest surface first): `revit_export_element_ids` + `XlsxWriter`, `isModified`, `PluginVersion`, `revit_set_view_lighting`, `revit_create_floor`/`revit_create_level`, `revit_set_phase`/`revit_merge_phases` (must carry the batch-exclusion rule), Revit 2020 support (largest), the id-reset/rebuild family (largest). Do not contribute the local `revit_batch` semantic or the bilingual site.

## 5. Evidence boundaries

All numbers come from git objects in this checkout (`git log/show/diff/merge --no-commit` in a temporary worktree, removed afterwards) plus reading the current working tree. The user's 47 uncommitted working-tree changes (docs/site WIP plus this file) were not touched. No builds, tests, Revit runs or live tool registrations were executed. Upstream behavior descriptions cite its own commit messages and docs; they are not locally reproduced.
