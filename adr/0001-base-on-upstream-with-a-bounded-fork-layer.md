# 0001. Base the product on upstream and keep local features in a bounded fork layer

- Status: Accepted
- Date: 2026-10-30
- Supersedes: the "local is the trunk, absorb upstream through a classified intake" direction recorded in issue #27 and in `analysis/upstream-port-ledger.md`

## Context

The upstream product and this fork diverged at `5a65afc` (2026-09-16, upstream v0.5.0). Since then upstream shipped 133 commits, including a 1.0 release that rewrote the action pipeline into a 20-module server, added 53 tools, added a machine policy layer, a batch supervisor, an updater and a store build. This fork shipped 55 commits that add eight actions the upstream product does not have, plus Revit 2020 support, an element-id toolkit and a bilingual site.

Measured size on each side:

- Upstream since the split: 458 files, +67236 / −5115.
- This fork: 219 files, +21606 / −1176. New files account for 142 of them; 77 are upstream files that were edited, and only 18.2% of added lines land in those.
- Merging the fork into 1.0 produces 50 conflicted files, including 13 hunks in one 1700-line parser. Resolving them is a rewrite with worse tooling.

The alternative, staying on the v0.5.x architecture and hand-porting upstream fixes one at a time, was tried first and recorded as a ledger of 133 classified commits. It keeps the fork on an architecture upstream no longer maintains, and every security fix has to be re-derived by hand from a codebase that no longer looks the same.

## Decision

Upstream is the base. The fork is a thin layer on top of it.

1. The base is the upstream commit `760bb7c`, the tip of `upstream/main` at the time of this decision. It carries v1.0.0 plus eleven post-release fixes, three of which sit on error paths used daily. The base is recorded as a full SHA, never a branch name.
2. The eight fork actions are rewritten against the upstream contracts. They are not merged, not cherry-picked, and not ported file by file.
3. Fork code lives only in `src/RevitModelMcp.Core/Fork/`, `src/RevitModelMcp.Addin/Fork/` and `server/revit_model_mcp/fork_actions.py`.
4. The fork touches upstream files only at seven named dispatch hooks plus one Python registration line.
5. "Thin" is a number, not a feeling: at most 80 changed lines across those hooks. The prototype measured the anchor set at 35, so 80 leaves a factor of two.
6. Re-syncing means merging upstream into the fork. With the fork confined to fallback branches, conflicts land in the hooks and nowhere else.

## Consequences

The eight actions must be re-expressed against contracts that changed shape: several argument names moved, the action DTO grew, and the step vocabulary is a closed union. That work is real and is what ADR 0002 bounds.

Upstream improvements arrive for free: the 53 extra tools, the policy layer, the batch supervisor, the updater, the store build. This fork deletes its own implementations of things upstream now does better, including its failure-preprocessor hook and its plugin-version plumbing.

The fork keeps a permanent divergence. Upstream fixes do not reach the fork layer, and the fork layer does not reach upstream. The mitigation is a rhythm, not a guarantee: read upstream once per minor release and run the intake check.

Upstream renames stay upstream's. `revit_batch` becomes `revit_run_actions`, and the fork keeps no alias (ADR 0004).

## Alternatives rejected

**Merge the 55 fork commits into 1.0.** 50 conflicted files concentrated in exactly the files the fork edited most. The conflicts are not mechanical: they are the same functions rewritten from different premises. Cost is a rewrite plus 50 resolutions.

**Stay on the trunk and port fixes individually.** Preserves full control and requires no re-expression of the eight actions. Rejected because the base architecture is frozen at v0.5.x while upstream keeps moving, so the gap grows monotonically, and because the policy layer that upstream 1.0 relies on for safe writes cannot be back-ported without also re-expressing the action pipeline.

**Rewrite the fork from scratch on 1.0.** Discards 22 commits of hard-won Revit behaviour: which elements cannot be treated as ordinary elements, which copies need rehosting, which dialogs Revit raises. The knowledge is the expensive part, not the code (ADR 0002).
