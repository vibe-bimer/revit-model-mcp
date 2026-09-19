# Claude instructions

Follow [AGENTS.md](AGENTS.md) for repository instructions, checks and hard rules.

## Agent skills

### Issue tracker

Issues live in the fork's GitHub Issues, driven by the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

The five canonical triage roles use their default label strings. See `docs/agents/triage-labels.md`.

### Adding Revit tools

Query the local Revit 2026 API corpus before writing or reviewing any Revit
API code, then follow the read and action tool checklists. See
`docs/agents/adding-revit-tools.md`.

### Domain docs

Single-context: one `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
