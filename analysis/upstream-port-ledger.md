> **Superseded as a direction, kept as a record.** This ledger classifies what
> upstream shipped, one commit per bucket, for the model where local stays the
> trunk. That model is replaced: the product now sits on upstream 1.0 with a
> bounded fork layer (`adr/0001`). The classification below is still
> accurate and still useful for reading upstream; what changed is that syncing
> means merging a release, not replaying commits. `tools/check_upstream_intake.py`
> remains a reader for what upstream shipped.

# Upstream port ledger

This was written for a model where local stayed the trunk and upstream was a
catalogue to draw from. Read the rules below as the record of that model, not as
current policy: the product now sits on upstream 1.0 (`adr/0001`). The
classification is what survives, because it is a reading of what upstream
shipped.

Baseline: local `main` @ `5afcb55`, upstream `760bb7c`, merge-base `5a65afc`.
133 upstream commits since the merge-base, all classified below.

The cursor lives in `analysis/upstream-seen.json`; `tools/check_upstream_intake.py`
fails while any commit in `last_seen..upstream/main` is missing from this file.

Rules this ledger follows:

1. A port must be self-contained: it must not require upstream's 8-module → 20-module
   restructure, its channel protocol v2, or its policy layer.
2. A port lands as a normal local change with local tests. No merge, no anchors,
   no graft directory.
3. Upstream renames and product-level decisions are not followed. Local keeps its
   own names and its own tool surface.

---

## Batch 0 — not a port: keep the local install from being overwritten

Local must own its install identity before anything else matters. Done on
2026-10-30; this section records what the work actually was, because the
original four-line estimate was wrong in two directions.

Two of the four items were not applicable: this tree has no `Updates/`
directory at all, so there is no upstream update feed to re-point and no
default update mode to turn off. Both arrive only with upstream's updater,
which this fork does not carry. The real work was elsewhere.

| Item | Evidence | State |
| --- | --- | --- |
| Own `UpgradeCode` | `build/install/Installer.cs:18` held upstream's `75e1b812-23a4-45ce-9e7c-84d7d43b8c70`; upstream `:179` says the codes are shared on purpose | Done — `8F2D710A-B967-4180-AB08-1678A02BA350` |
| Own product name and manufacturer | Same file, plus `build/appsettings.json` `VendorName` | Done — `Revit Model MCP (vibe-bimer)`, `vibe-bimer`. `outputName` stays `RevitModelMcp` because release download links are built from it |
| Stop publishing upstream's package | `.github/workflows/release.yml` had a `pypi` job (upstream's pending publisher) and an `mcp-registry` job | Done — both jobs removed; the fork installs from its release wheel |
| Stop resolving the server by PyPI name | `bundle/manifest.json` ran `uvx revit-model-mcp==<version>`, and `release.yml` only used the wheel for prereleases | Done — always the release wheel. This was the worst defect: both projects ship the same version numbers, so a stable fork bundle installed upstream's server silently and CI asserted that shape was correct |
| Point shipped links at the fork | README badges, `SECURITY.md` report form, `CONTRIBUTING.md`, `server/README.md` `mcp-name`, issue forms, `docs/{security,privacy,transport,validation}` bilingual pairs, `glama.json`, bundle manifest and README | Done — 20 files |
| Guard the above | — | Done — `tools/check_fork_identity.py`, wired into `pr-checks.yml`, plus a hard rule in `AGENTS.md` |

Deliberately kept: `sharafutdinovdi/.github` reusable workflows, the inherited
code of conduct, and `docs/agents/issue-tracker.md` explaining which remote is
which. Reusing an upstream org workflow is honest; claiming its install
identity is not.

Still open: builds up to v0.9.0 shipped upstream's `UpgradeCode`, so the next
release installs beside them instead of upgrading. `README.md` tells users to
uninstall first. Nothing else can fix that after the fact.

---

## Batch 1 — security and transport (port first, they are live bugs locally)

| Commit | Subject | Local exposure |
| --- | --- | --- |
| `69af8d0` | require the add-in to prove the token before jobs | HTTP token has no nonce/HMAC: replayable on the same machine |
| `4b09359` | validate network and aliased paths in file arguments | No path/UNC validation on file arguments |
| `2f9f172` | restrict the file channel directory to the current user | Channel directory has no per-user ACL |
| `6c557aa` | redact paths in confirmation text, summaries and errors | Redaction covers `documentPath`/`path` only |
| `db5ed7d` | reject oversized declared HTTP jobs | No declared-size cap |
| `61a3567` | harden the HTTP host with limits, read deadline, graceful shutdown | No size cap or read deadline |
| `b9b8e44` | bound confirmation tokens, logs and query limits | Tokens, logs and limits unbounded |
| `002fb17` | harden the ssh channel and artifact download | ssh invocation lacks `-T -a -x` |
| `a10a0cc` | validate `save_to` before deleting the remote capture | Delete-before-validate ordering |
| `1e93efe` | bound the SSH limiter wait by the caller timeout | Limiter wait unbounded |
| `3ad9969` | serialize the HTTP health payload | Health payload is assembled ad hoc |
| `b1ae1d5` | keep terminal results intact on Local and SSH | Terminal results can be truncated at the boundary |

These are fixes to code local already has, in the shape local already has. They
are the cheapest ports in the ledger and the highest value.

---

## Batch 2 — correctness and message quality (small, independent)

| Commit | Subject |
| --- | --- |
| `60c1abe` | resolve parameter filters that share a built-in field name |
| `dd11997` | resolve set parameters explicitly |
| `4da8b64` | report skipped fields |
| `46841e8` | replace stale per-process channel directory |
| `6af4dee` | refuse shared coordinates on family documents |
| `50eba5c` | predict group failures for move, rotate, copy, mirror and change_type |
| `89b30d7` | make dry runs predict group and join failures |
| `36cf71e` | keep `undo_last` available after element captures |
| `c912f2d` | report elements that move, rotate or mirror cannot change |
| `2ff406c` | truthful summaries for dry runs and empty scripts |
| `bff8d7c` | reject unknown tool arguments |
| `3b0969d` | say a missing target document is not open |
| `32b6528` | report transport loss as a retryable structured error |
| `59b7000` | confirmation tokens and job polling papercuts |
| `e1b82a7` | papercuts found by live validation of 0.9.0 |
| `6be592f` | make the discovery payload UTF-8 safe |
| `013e45d` | say why HTTP is disabled or serving 503 |
| `b14926c` | keep finished image exports complete after 60 seconds |
| `47f4b76` | keep the job scheduler running when result persistence fails |

Several of these land directly on the eight actions' verification story, which
is where local already invests most: `36cf71e`, `c912f2d` and `2ff406c` are
about telling the truth after a change, which is the local product's whole point.

---

## Batch 3 — performance (measured upstream, portable)

| Commit | Subject |
| --- | --- |
| `d765ecb` | cache parameter resolution, serializers and warnings on the read path |
| `dc1bcd4` | compact family audit by default, skip unlabelable dimensions quietly |
| `ba59335` | keep capture and tool budgets independent of clock resolution |

`d765ecb` is process-level caching of parameter names, serializers and warnings.
It does not depend on the new architecture.

---

## Batch 4 — capability, medium effort, needs adaptation

| Commit | Subject | Adaptation needed |
| --- | --- | --- |
| `bdf5cdf` | recover from document switches, bound catalog results, fix small usage errors | Catalog limits and doc-switch recovery are independent; the "small usage errors" part is mostly already local |
| `058bb28` | move the pickup timeout out of the tool schemas | Local passes `pickup_timeout_seconds` in 43 places; the upstream shape is an environment variable with a 300 s default |
| `2240b49` | uniform read-only refusals for job control and batch start | Local has its own write gate; the *shape* of the refusal is worth copying, not the gate |

---

## Batch 5 — build and CI (cheap, mechanical)

| Commit | Subject |
| --- | --- |
| `171b472` | pin merged Revit API references to the lowest build of each year |
| `1d463dd` | allow same-version MSI upgrades |
| `e154b6a` | refuse to install both installer scopes at once |
| `a5ec995` | upgrade MSI over developer builds and stale manifests |
| `2463b5f` | publish SHA256SUMS.txt with LF line endings |
| `03d8488` | grant the HTTP URL ACL to all local users |
| `dc5c1f6` | run checks in parallel with caches and fix time-budget tests |
| `ebc4d98` | update Revit SDK, Toolkit, Extensions and Polyfill |
| `760bb7c` | bump uv to 0.13.4 |
| `f6e8f56` | drop tests that assert on C# source text |
| `1f60a8e` | version development builds from the repository version |
| `03605cd` | pin release tooling and verify downloads |
| `2e670df` | pin release tooling and lock dependency restores |
| `2dad037` | make WinGet release submission reliable |
| `c94ba6e` | prepare release signing through SignPath |
| `cd43aa4` | submit WinGet updates weekly instead of on every release |
| `a35b1d8` | wait for each response in the bundled server smoke test |
| `a10c0b2` | give early budget timer tests real headroom |
| `dffc3bc` | remove wall-clock margins from heartbeat retry tests |
| `27e9414` | make the external event retry test deterministic |
| `8436cb5` | derive the fake add-in version from the server package |
| `3d9dbf1` | frame the redirect fixture response |
| `dc5e839` | ignore editor and local tool state |
| `4c3eaf4` | repository hygiene and contributor onboarding |
| `1a12f52` | bump the all dependency group |
| `43a2629` | bump the all group across three directories |
| `e9af4fb` | bump the all dependency group |
| `3498163` | bump Polyfill and TUnit |

`171b472` is the one with real substance: local uses a floating
`[$(RevitVersion).0.0,next.0.0)` range per year, upstream pins to the lowest
build of each year. The pin is why upstream builds are reproducible.

---

## Reference only — read the design, do not port

These are large and structurally bound. Read them when local needs the same
capability; do not attempt to bring them across.

| Area | Commits |
| --- | --- |
| Channel protocol v2, process scoping, activity pane | `90cbeee`, `42b6aa3` |
| Server and add-in auto-update | `4aacbf0`, `c876e33` |
| Supervised batch collection + 13 follow-up fixes | `e7654de`, `c51ab3f`, `2db6698`, `bc3f318`, `30a7786`, `ad6fe67`, `09a7f07`, `2a4c02e`, `ecb5fcc`, `5c0695f`, `d98c5d2`, `fac5499`, `7778d0c`, `26dadc0` |
| Multi-model processing cleanup | `53f002d` |
| Snapshot reader and reports | `27a1cd2`, `ca8963e`, `5ceed32`, `2dba958` |
| Revit session actions | `f646389` |
| Machine policy, update channels, tagging, schedule tools | `41be1fe` |
| Managed install, App Store build, ribbon help | `4bc733f`, `9ecaa57`, `7b86e56` |
| Coordinator prompts and skill | `c262beb` |
| Confirmation for link removal and large deletions | `9412a8e`, `2e1fa85` |
| Tool manifest and bundle validation | `6932778`, `9b488cb`, `b1519e0` |

Two of these deserve a specific read even though they are not ports:

- `53f002d` and the batch fixes are the industrial version of local's rebuild
  farm. Local's `ModelRebuild` (1003 lines) solves a similar problem with a
  different shape. Reading them is worth a day; porting them is a quarter.
- `9412a8e` and `2e1fa85` are the confirmation UX local has not built. Local's
  actions are reversible, so the value is lower, but the wording is worth copying.

---

## Do not follow — local deliberately diverges

| Commit | Subject | Why not |
| --- | --- | --- |
| `f00bf37` | rename the server and internal job classes | Local's names are its own |
| `a9e14a5` | one name for timeouts and output paths | Breaking rename with no local benefit |
| `5c56f89` | rename the product display name to Model MCP | Local keeps its name |
| `936c599` | one rule for errors and refusals | Local's error surface is already consistent; adopting upstream's costs a rewrite |
| all `docs:` commits | — | Upstream rewrote 13 documents; local's docs are local |

### Not followed: upstream housekeeping

Enumerated so the intake check stays meaningful. These change nothing local owns.

| Kind | Commits |
| --- | --- |
| Release commits (release-please's own) | `7f736d1`, `223f9a1`, `794e152`, `eefef58`, `d61094f`, `24a23cc`, `27c1c45` |
| Documentation rewrites and roadmap posts | `b99218b`, `e1effdd`, `79ebead`, `5a23383`, `6dfd07d`, `0b661d7`, `2426c40`, `6456b47`, `7df8fb4`, `0d7659d`, `a68b2f1`, `a853115`, `cc03f56`, `d51f403`, `d781658`, `8ddd24a`, `2e56c3f`, `33d2639` |
| Product-level identity | `c1e23f5` (package homepage points at the upstream project page) |

### Not applicable: the local code has no counterpart

| Commit | Subject | Why it does not apply |
| --- | --- | --- |
| `fa336b9` | refuse batch start and cancel in read-only mode | Local gates the whole action surface at registration (`actions.py:219` returns early when `REVIT_MCP_ALLOW_WRITE` is off), so there is no batch-start tool to refuse |
| `8c4e13b` | list unprocessed models as cancelled in process-models | Local has no `revit_process_models` |
| `99dfba8` | stop throttling multiplexed ssh sessions | Local has no SSH session throttle to remove |
| `6d3ab51` | own the named pipe and verify its server process | Local has no named-pipe transport |

---

### Not followed: upstream housekeeping (continued)

| Commit | What it is | Why not followed |
| --- | --- | --- |
| `6d19760` | docs(privacy): state cross-border processing and access rights (#324, 2026-10-30) | Upstream's privacy page, answering an Autodesk review item. The fork ships its own privacy page and own legal entity; porting upstream's wording would misattribute it. Revisit if the fork's privacy page ever needs the same statements. |

## Standing process

Upstream keeps shipping. The intake list only stays useful if new commits get
classified instead of piling up.

This file is the single hand-written source: a commit counts as classified when
its SHA appears anywhere below. `analysis/upstream-seen.json` records the cursor.
`tools/check_upstream_intake.py` joins the two and fails while anything in the
range is unclassified.

Once per upstream minor release:

1. `git fetch upstream --tags`
2. `python3 tools/check_upstream_intake.py` — prints every commit since the
   cursor that has no entry in this file. Exit status 1 means the backlog is real.
3. Classify each one into a batch below. Anything touching a file local also owns
   gets read in full, whether or not it is ported. That is where a security fix
   hides.
4. `python3 tools/check_upstream_intake.py --update-seen` — moves the cursor,
   and refuses while anything is unclassified.

The number to watch is the unclassified count. If it grows past one release, the
ledger has stopped being read.

---

## What this model costs

Permanent divergence. Local will never receive an upstream feature without
rework, and the gap widens with every upstream release. That is the price of
owning the trunk.

It is a reasonable price here: local's value is eight precise, reversible,
verifiable actions, and upstream's value is a platform local does not need.
The cost that must not be ignored is security: upstream fixes arrive by hand
now, so the once-per-release read in the standing process is not optional.
