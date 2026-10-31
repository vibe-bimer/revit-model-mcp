# CI gates and their blind spots

Every push and pull request runs a set of gates, and each gate proves exactly one thing.
This page lists what each gate proves, what it does **not** prove, and how the gap found on 2026-10-31 was closed.

## The chain

| Gate | Where | What it proves |
| --- | --- | --- |
| Documentation line present | `tools/site/check_docs_line.py` | The 15 files publishing needs all exist, and `docs/features` and `docs/platform` carry enough tool pages |
| Dual-config build | `tools/site/verify_dual_build.py` | `mkdocs.yml` and `mkdocs-lan.yml` both build with `--strict`, `check_site.py` is green, and the two builds normalize to the same tree |
| Generator consistency | `tools/site/generate_features.py --check` | The committed generated pages match the registry, the contracts and the catalogs |
| Tool inventory | the bundle job in `ci.yml` | `bundle/manifest.json` names the same tools as `docs/features/index.md` |
| Python tests | `server/` and `tools/site/` | The server and the site tooling behave as their tests say |
| Budget | `build/check_fork_budget.py` | Every changed file belongs to a declared path |

## What each gate cannot prove

- **The dual-config build** fails only while a configuration still points at a file that exists.
  Delete the whole `docs/platform/` subtree and the nav in `mkdocs-lan.yml` points at a missing file, so the build fails — that it catches.
  Delete a file the build never reads (`scripts/serve-site.py`, `tools/site/check_site.py`, the timer scripts) and the build still passes, with CI green.
- **Generator consistency** compares the committed generated pages with the current registry; it never asks whether the generator itself is still there.
- **The tool inventory** only compares two sets for equality. Delete both sides and they still agree, so it stays quiet.
- **The budget** checks ownership, not usefulness: a file declared as a fork path never fails, even when nothing uses it any more.

## The incident on 2026-10-31

A merge from a rebase branch took the whole documentation line off `main`: 327 files disappeared, including `scripts/`, `tools/site/`, `docs/platform/` and `mkdocs-lan.yml`.
CI was green at that moment, because what remained was still self-consistent: no nav pointed at a missing file, and no generated page disagreed with the registry.
The timer finished its last successful publish at 13:46; from 14:01 `scripts/site-cron.sh` was gone, the failure went only to a local log, and nobody noticed until the next day.

## How the blind spot is covered

**An existence assertion.** `tools/site/check_docs_line.py` asserts the files and minimum page counts the published line needs. The `docs-line` job in `ci.yml` runs it, and so does the first step of `docs.yml`.
It does not care whether a build succeeds; it only cares that these files are still there.

**Visible publish health.** The publisher writes every attempt into `manifest.json` in the state root, the timer writes every run into `cron-status.json`, and the deployment exposes itself at two read-only endpoints:

- `/status.json` — the same summary, machine-readable
- `/status.html` — a bilingual page whose banner states the reason when something is wrong

The summary carries the outcome and stage of the last attempt, the last successful release, the reason of the last failure, the last timer run, and whether the deployment is stale (no successful publish for 26 hours, or a timer silent for 2 hours).
Tune the thresholds with `SITE_STATUS_STALE_HOURS` and `SITE_STATUS_TIMER_SILENT_HOURS`.

**A watchdog exit code.** `scripts/check-site-status.py` reads the same summary and exits `0` when healthy, `1` when the last publish failed, and `2` when the deployment is stale.
`scripts/install-site-timer.sh` installs an hourly watchdog in the cron branch, appending to `site-update.log`; set `SITE_ALERT_WEBHOOK` and an unhealthy verdict is posted there as JSON.
Each watchdog run also writes `watchdog-status.json`, so the status page shows whether the watchdog itself is running.

## Judging whether a gate is enough

Ask two questions:

1. When this gate fails, will someone see it within the hour?
2. When this gate passes, which "looks fine, is broken" states has it ruled out?

The answer to the second question is the blind spot list. A gate earns its place not by what it catches but by what it cannot catch being written down and covered by another gate.
