#!/usr/bin/env python3
"""Generate the feature pages of the documentation site from the live registry.

The pages describe what the server serves, not what a hand-written list claims it
serves: the tool list is the server's own tools/list answer, so a page cannot
outlive the tool it documents. Two kinds of page come out of one run.

* Every tool gets a page rendered from its registry title, description and input
  schema, and sits in the toolset the server declares in
  server/revit_model_mcp/toolsets.py.
* The eight tools this fork adds also carry prose from
  tools/site/content/capabilities.yaml: a summary, copyable prompts, usage notes
  and per-parameter meanings.

The site is English only. The 1.0 base carries no translation plugin, so there
are no .zh twins and no translated labels.

Run --dump after a server change, then --write. CI runs --check.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CONTENT = HERE / "content"
TOOLS_JSON = CONTENT / "tools.json"
CAPABILITIES = CONTENT / "capabilities.yaml"
TOOLSETS_SOURCE = ROOT / "server" / "revit_model_mcp" / "toolsets.py"
PAGES = ROOT / "docs" / "features"
MKDOCS = ROOT / "mkdocs.yml"

NAV_START = "  # >>> features-nav"
NAV_END = "  # <<< features-nav"

SECTIONS = ("read", "action")
SECTION_LABELS = {"read": "Read tools", "action": "Action tools"}
KIND_LABELS = {"read": "Read (read-only)", "action": "Action (opt-in)"}

COMMON_PARAMETERS = ("document", "timeout_seconds")

# Labels for the toolsets the server declares. The keys must match
# server/revit_model_mcp/toolsets.py; the generator fails when they do not.
TOOLSET_LABELS = {
    "core": "Connection and core",
    "read": "Model queries",
    "actions": "Model actions",
    "documents": "Documents",
    "views-sheets": "Views and sheets",
    "family": "Families",
    "links": "Links",
    "cad-mep": "CAD and MEP",
    "export": "Export",
    "batch": "Batch processing",
    "code": "Code execution",
}

# The tools this fork adds. capabilities.yaml must describe exactly these.
FORK_TOOLS = (
    "revit_create_floor",
    "revit_create_level",
    "revit_export_element_ids",
    "revit_merge_phases",
    "revit_rebuild_model_ids",
    "revit_reset_element_ids",
    "revit_set_phase",
    "revit_set_view_lighting",
)

DEFAULT_YEARS = {"2020": "unsupported", "2026": "built", "other": "built"}
YEAR_ROWS = (("2020", "2020"), ("other", "2022–2025, 2027"), ("2026", "2026"))
YEAR_COLUMNS = ("2020", "2022", "2023", "2024", "2025", "2026", "2027")

STATE_LABELS = {
    "validated": "Validated live",
    "built": "Built",
    "unsupported": "Not supported yet",
}
STATE_CELLS = {"validated": "Validated", "built": "Built", "unsupported": "No"}

LEGEND = (
    "**Built** means the release workflow compiles that Revit configuration. "
    "**Not supported yet** means no build target exists on this branch: adr/0006 "
    "records Revit 2020 as a required follow-up and names no calendar date; the "
    "maintainer chooses the date when the follow-up is scheduled. Nothing on this "
    "branch has been verified against a running Revit instance, so no page claims "
    "a live result."
)

FOOTER = (
    "[Feature overview](index.md) · [Version support matrix](matrix.md) · "
    "[Prompt library](prompts.md)"
)


def load_toolsets() -> dict[str, tuple[str, ...]]:
    """Read TOOLSETS from the server source without importing the package."""
    tree = ast.parse(TOOLSETS_SOURCE.read_text(encoding="utf-8"))
    for node in tree.body:
        targets = []
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            targets = [node.target]
        elif isinstance(node, ast.Assign):
            targets = [
                target for target in node.targets if isinstance(target, ast.Name)
            ]
        if (
            any(target.id == "TOOLSETS" for target in targets)
            and node.value is not None
        ):
            return ast.literal_eval(node.value)
    raise SystemExit(f"{TOOLSETS_SOURCE.relative_to(ROOT)} does not declare TOOLSETS")


def load_registry() -> list[dict]:
    return json.loads(TOOLS_JSON.read_text(encoding="utf-8"))


def load_capabilities() -> dict:
    return yaml.safe_load(CAPABILITIES.read_text(encoding="utf-8"))


def kind(tool: dict) -> str:
    """Say whether the server lists a tool as a read or as an action."""
    return "read" if (tool.get("annotations") or {}).get("readOnlyHint") else "action"


def escape_cell(text: str) -> str:
    return " ".join(str(text).split()).replace("|", r"\|")


def normalize_block(text: str) -> str:
    """Strip the block indent the registry keeps inside a description."""
    lines = (text or "").splitlines()
    if not lines:
        return ""
    body = lines[1:]
    indent = min(
        (len(line) - len(line.lstrip()) for line in body if line.strip()), default=0
    )
    out = [lines[0].strip()]
    out += [line[indent:].rstrip() if line.strip() else "" for line in body]
    return "\n".join(out).strip()


def first_sentence(text: str) -> str:
    text = " ".join((text or "").split())
    if not text:
        return ""
    parts = text.split(". ", 1)
    sentence = parts[0] if len(parts) == 2 else text
    return sentence if sentence.endswith((".", "!", "?")) else f"{sentence}."


def type_label(spec: dict) -> str:
    if not isinstance(spec, dict) or not spec:
        return "—"
    if "anyOf" in spec:
        parts = [type_label(part) for part in spec["anyOf"]]
        return " / ".join(dict.fromkeys(parts))
    if spec.get("type") == "array":
        return f"array of {type_label(spec.get('items') or {})}"
    label = str(spec.get("type", "any"))
    if "enum" in spec:
        values = ", ".join(str(value) for value in spec["enum"])
        return f"{label} ({values})"
    return label


def default_label(spec: dict) -> str:
    if not isinstance(spec, dict) or "default" not in spec:
        return "—"
    return json.dumps(spec["default"], ensure_ascii=False)


def table(header: list[str], rows: list[list[str]]) -> list[str]:
    lines = ["| " + " | ".join(header) + " |"]
    lines.append("| " + " | ".join("---" for _ in header) + " |")
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return lines


class Site:
    """The registry, the declared toolsets and the fork's prose, grouped once."""

    def __init__(self, tools: list[dict], toolsets: dict, capabilities: dict) -> None:
        self.tools = tools
        self.toolsets = toolsets
        self.capabilities = capabilities
        self.fork = capabilities["tools"]
        self.group_titles = capabilities["groups"]
        self.by_name = {tool["name"]: tool for tool in tools}
        self.rows = self._group()
        self.group_of = {
            tool["name"]: title
            for _, groups in self.rows
            for _, title, members in groups
            for tool in members
        }

    def _group(self) -> list[tuple[str, list[tuple[str, str, list[dict]]]]]:
        """Return (section, [(group key, group title, tools)]) in display order.

        The fork's own groups come first, then the toolsets the server declares,
        in the order toolsets.py lists them. Every tool lands in exactly one
        group, or the run fails.
        """
        if set(self.fork) != set(FORK_TOOLS):
            raise SystemExit(
                "capabilities.yaml must describe exactly these tools: "
                + ", ".join(sorted(FORK_TOOLS))
                + "; it describes: "
                + ", ".join(sorted(self.fork))
            )
        unknown = sorted(
            {self.fork[key]["group"] for key in self.fork} - set(self.group_titles)
        )
        if unknown:
            raise SystemExit(
                "capabilities.yaml uses undeclared groups: " + ", ".join(unknown)
            )
        unlabelled = sorted(set(self.toolsets) - set(TOOLSET_LABELS))
        if unlabelled:
            raise SystemExit(
                "server/revit_model_mcp/toolsets.py declares toolsets the generator has no "
                "label for: " + ", ".join(unlabelled)
            )
        toolset_of = {
            name: key for key, members in self.toolsets.items() for name in members
        }
        missing = sorted(set(self.by_name) - set(toolset_of))
        if missing:
            raise SystemExit(
                "the registry serves tools no toolset declares: " + ", ".join(missing)
            )

        rows = []
        for section in SECTIONS:
            members = [tool for tool in self.tools if kind(tool) == section]
            groups = []
            for key, entry in self.group_titles.items():
                picked = [
                    tool
                    for tool in members
                    if self.fork.get(tool["name"], {}).get("group") == key
                ]
                if picked:
                    groups.append((key, entry["title"], picked))
            for key, names in self.toolsets.items():
                picked = [
                    tool
                    for tool in members
                    if tool["name"] in names and tool["name"] not in self.fork
                ]
                if picked:
                    groups.append((key, TOOLSET_LABELS[key], picked))
            covered = sum(len(picked) for _, _, picked in groups)
            if covered != len(members):
                raise SystemExit(
                    f"{len(members)} {section} tools but the groups hold {covered}; "
                    "a tool is grouped twice or not at all"
                )
            rows.append((section, groups))
        return rows

    def title(self, tool: dict) -> str:
        entry = self.fork.get(tool["name"])
        return entry["title"] if entry else str(tool.get("title") or tool["name"])

    def summary(self, tool: dict) -> str:
        entry = self.fork.get(tool["name"])
        return (
            entry["summary"] if entry else first_sentence(tool.get("description", ""))
        )

    def years(self, tool: dict) -> dict[str, str]:
        years = dict(DEFAULT_YEARS)
        entry = self.fork.get(tool["name"]) or {}
        for key, state in (entry.get("years") or {}).items():
            years[str(key)] = str(state)
        return years

    def state(self, tool: dict, year: str) -> str:
        years = self.years(tool)
        key = "other" if year not in years else year
        return years.get(key, "unsupported")


def parameter_meaning(site: Site, tool: dict, name: str, spec: dict) -> str:
    notes = (site.capabilities.get("param_notes") or {}).get(tool["name"], {})
    if name in notes:
        return str(notes[name])
    defaults = site.capabilities.get("param_defaults") or {}
    if name in defaults:
        return str(defaults[name])
    described = str((spec or {}).get("description", "")).strip()
    return described or "—"


def parameter_rows(site: Site, tool: dict) -> list[dict]:
    schema = tool.get("inputSchema") or {}
    properties = schema.get("properties") or {}
    required = set(schema.get("required") or [])
    order = sorted(properties, key=lambda name: (name not in required, name))
    return [
        {
            "name": name,
            "required": name in required,
            "default": default_label(properties[name]),
            "type": type_label(properties[name]),
            "meaning": parameter_meaning(site, tool, name, properties[name]),
        }
        for name in order
    ]


def gate_admonition() -> list[str]:
    return [
        '!!! warning "Runs only on a read-write workstation"',
        "",
        "    An action runs only while the workstation is not read-only: the machine policy",
        "    gate refuses action calls over every transport. The gate is the policy's",
        "    `ReadOnly` value, held in the registry under",
        "    `HKLM\\Software\\Policies\\RevitModelMcp` or in",
        "    `%ProgramData%\\RevitModelMcp\\policy.json`. The installer sets `ReadOnly` to",
        "    `1` by default and writes the default `policy.json`, so a fresh install refuses",
        "    actions until an administrator allows writes. When both stores exist, the",
        "    registry value wins for every value it sets, and a policy that cannot be read",
        "    fails closed to read-only. The call names its target document, and with more",
        "    than one open document it is refused. `dry_run` returns the same verification",
        "    block without changing the model.",
        "",
    ]


def year_section(site: Site, tool: dict) -> list[str]:
    years = site.years(tool)
    rows = [
        [label, STATE_LABELS[years.get(key, "unsupported")]] for key, label in YEAR_ROWS
    ]
    return (
        ["## Revit year support", ""]
        + table(["Revit year", "State"], rows)
        + ["", LEGEND, ""]
    )


def tool_page(site: Site, tool: dict) -> str:
    entry = site.fork.get(tool["name"])
    section = kind(tool)
    lines = [f"# {site.title(tool)}", ""]
    summary = site.summary(tool)
    if summary:
        lines += [summary, ""]
    facts = [
        f"**Group:** {site.group_of[tool['name']]}",
        f"**Kind:** {KIND_LABELS[section]}",
    ]
    if entry:
        facts.append(f"**Since:** this fork's {entry['since']}")
    lines += [" · ".join(facts), ""]
    if entry:
        lines += [
            "This fork adds this tool; the rest of the catalogue comes from upstream 1.0.",
            "",
        ]
        if section == "action":
            lines += gate_admonition()
        if entry.get("note"):
            lines += ['!!! note "Usage notes"', "", f"    {entry['note']}", ""]
        prompts = entry.get("prompts") or []
        if prompts:
            lines += ["## Copyable prompts", ""]
            for prompt in prompts:
                lines += ["```text", str(prompt), "```", ""]

    rows = parameter_rows(site, tool)
    own = [row for row in rows if row["name"] not in COMMON_PARAMETERS]
    common = [row for row in rows if row["name"] in COMMON_PARAMETERS]
    lines += ["## Parameters", ""]
    if own:
        lines += table(
            ["Name", "Required", "Default", "Type", "Meaning"],
            [
                [
                    f"`{row['name']}`",
                    "Yes" if row["required"] else "No",
                    row["default"],
                    f"`{row['type']}`",
                    escape_cell(row["meaning"]),
                ]
                for row in own
            ],
        )
        lines.append("")
    else:
        lines += ["This tool takes no parameters of its own.", ""]
    if common:
        lines += ["### Common parameters", ""]
        lines += table(
            ["Name", "Meaning"],
            [[f"`{row['name']}`", escape_cell(row["meaning"])] for row in common],
        )
        lines.append("")

    description = normalize_block(tool.get("description") or "")
    if description:
        lines += ["## Behavior and returned data", "", description, ""]
    lines += year_section(site, tool)
    lines += [FOOTER, ""]
    return "\n".join(lines).rstrip() + "\n"


def index_page(site: Site) -> str:
    reads = [tool for tool in site.tools if kind(tool) == "read"]
    actions = [tool for tool in site.tools if kind(tool) == "action"]
    total = len(site.tools)
    lines = [
        "# Feature overview",
        "",
        (
            f"The server serves {total} tools: {len(reads)} read and {len(actions)} action. "
            "A read returns model data and changes nothing; an action changes the model or a file."
        ),
        "",
        "## Browse by Revit year",
        "",
    ]
    lines += table(
        ["Revit year", "Tools", "Details"],
        [
            ["2020", f"0 of {total}", "[Revit 2020](v2020.md)"],
            [
                "2022–2025, 2027",
                f"{total} built",
                "[Version support matrix](matrix.md)",
            ],
            ["2026", f"{total} built, not live-verified", "[Revit 2026](v2026.md)"],
        ],
    )
    lines += ["", LEGEND, ""]
    for section, groups in site.rows:
        count = sum(len(members) for _, _, members in groups)
        lines += [f"## {SECTION_LABELS[section]} ({count})", ""]
        for _, title, members in groups:
            lines += [f"### {title}", ""]
            lines += table(
                ["Tool", "Summary"],
                [
                    [
                        f"[{escape_cell(site.title(tool))}]({tool['name']}.md)",
                        escape_cell(site.summary(tool)),
                    ]
                    for tool in members
                ],
            )
            lines.append("")
    lines += [FOOTER, ""]
    return "\n".join(lines).rstrip() + "\n"


def matrix_page(site: Site) -> str:
    lines = [
        "# Version support matrix",
        "",
        (
            "Every tool against every Revit year. `Built` means the release workflow compiles "
            "that configuration; `No` means there is no build target yet."
        ),
        "",
    ]
    for section, groups in site.rows:
        lines += [f"## {SECTION_LABELS[section]}", ""]
        rows = []
        for _, _, members in groups:
            for tool in members:
                cells = [STATE_CELLS[site.state(tool, year)] for year in YEAR_COLUMNS]
                rows.append(
                    [f"[{escape_cell(site.title(tool))}]({tool['name']}.md)"] + cells
                )
        lines += table(["Tool", *YEAR_COLUMNS], rows)
        lines.append("")
    lines += [LEGEND, "", FOOTER, ""]
    return "\n".join(lines).rstrip() + "\n"


def prompts_page(site: Site) -> str:
    lines = [
        "# Prompt library",
        "",
        (
            "Each prompt below is a sentence a client can send as it stands. The tools this "
            "fork adds carry prompts; an inherited tool is described by its parameters and "
            "its own page."
        ),
        "",
    ]
    for _, groups in site.rows:
        for _, title, members in groups:
            prompted = [
                tool
                for tool in members
                if site.fork.get(tool["name"], {}).get("prompts")
            ]
            if not prompted:
                continue
            lines += [f"## {title}", ""]
            for tool in prompted:
                lines += [f"### {escape_cell(site.title(tool))}", ""]
                for prompt in site.fork[tool["name"]]["prompts"]:
                    lines += ["```text", str(prompt), "```", ""]
    lines += [FOOTER, ""]
    return "\n".join(lines).rstrip() + "\n"


def year_page(site: Site, year: str) -> str:
    notes = (site.capabilities.get("year_notes") or {}).get(year) or []
    if year == "2020":
        heading = "Revit 2020 support"
        lead = "Revit 2020 is not supported yet."
        state = "unsupported"
    else:
        heading = "Revit 2026 support"
        lead = (
            "Revit 2026 is built, but nothing on this branch has been verified against a "
            "running Revit 2026."
        )
        state = "built"
    lines = [f"# {heading}", "", lead, ""]
    if notes:
        lines += ["## What this branch states", ""]
        lines += [f"- {note}" for note in notes]
        lines.append("")
    lines += ["## Tools", ""]
    total = sum(len(members) for _, groups in site.rows for _, _, members in groups)
    if state == "unsupported":
        lines += [f"No tool in the catalogue runs on Revit {year}.", ""]
    else:
        lines += [f"Every one of the {total} tools is built for Revit {year}.", ""]
    lines += [
        "The [version support matrix](matrix.md) lists every tool.",
        "",
        FOOTER,
        "",
    ]
    return "\n".join(lines).rstrip() + "\n"


def nav_key(text: str) -> str:
    if text != text.strip() or any(
        character in text for character in ":#{}[]&*!|>\"'%@`"
    ):
        return json.dumps(text, ensure_ascii=False)
    return text


def nav_block(site: Site) -> list[str]:
    lines = [
        "  - Features:",
        "      - Feature overview: features/index.md",
        "      - Version support matrix: features/matrix.md",
        "      - Revit 2020 support: features/v2020.md",
        "      - Revit 2026 support: features/v2026.md",
        "      - Prompt library: features/prompts.md",
    ]
    for section, groups in site.rows:
        for _, title, members in groups:
            lines.append(f"      - {SECTION_LABELS[section]} — {nav_key(title)}:")
            for tool in members:
                lines.append(
                    f"          - {nav_key(site.title(tool))}: features/{tool['name']}.md"
                )
    return lines


def with_nav(text: str, nav: list[str]) -> str:
    start = text.find(NAV_START)
    end = text.find(NAV_END)
    if start < 0 or end < 0 or end < start:
        raise SystemExit(
            "mkdocs.yml needs '"
            + NAV_START.strip()
            + "' and '"
            + NAV_END.strip()
            + "' "
            "around the Features nav"
        )
    head = text[: start + len(NAV_START)]
    tail = text[end:]
    return f"{head}\n" + "\n".join(nav) + f"\n{tail}"


def render_all() -> dict[Path, str]:
    site = Site(load_registry(), load_toolsets(), load_capabilities())
    pages: dict[Path, str] = {}
    for _, groups in site.rows:
        for _, _, members in groups:
            for tool in members:
                pages[PAGES / f"{tool['name']}.md"] = tool_page(site, tool)
    pages[PAGES / "index.md"] = index_page(site)
    pages[PAGES / "matrix.md"] = matrix_page(site)
    pages[PAGES / "prompts.md"] = prompts_page(site)
    for year in ("2020", "2026"):
        pages[PAGES / f"v{year}.md"] = year_page(site, year)
    pages[MKDOCS] = with_nav(MKDOCS.read_text(encoding="utf-8"), nav_block(site))
    return pages


def dump_registry() -> list[dict]:
    """Ask the server for its own tools/list answer."""
    executable = ROOT / "server" / ".venv" / "bin" / "revit-model-mcp"
    command = (
        [str(executable)]
        if executable.is_file()
        else [sys.executable, "-m", "revit_model_mcp"]
    )
    environment = dict(
        os.environ,
        REVIT_MCP_HOST="http://127.0.0.1:53110",
        REVIT_MCP_TOKEN="dump",
        REVIT_MCP_READ_ONLY="0",
    )
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        env=environment,
        cwd=ROOT,
    )

    def send(payload: dict) -> None:
        assert process.stdin is not None
        process.stdin.write(json.dumps(payload) + "\n")
        process.stdin.flush()

    def call(payload: dict) -> dict:
        assert process.stdout is not None
        send(payload)
        while True:
            line = process.stdout.readline()
            if not line:
                error = (process.stderr.read() if process.stderr else "").strip()
                raise SystemExit(f"the server closed the stream: {error}")
            message = json.loads(line)
            if message.get("id") != payload.get("id"):
                continue
            if "error" in message:
                raise SystemExit(
                    f"the server refused {payload['method']}: {message['error']}"
                )
            return message["result"]

    try:
        call(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "docs", "version": "1"},
                },
            }
        )
        send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        result = call({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    finally:
        process.terminate()
    return result["tools"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate the feature pages of the site."
    )
    parser.add_argument(
        "--dump",
        action="store_true",
        help="write content/tools.json from the live registry",
    )
    parser.add_argument(
        "--write", action="store_true", help="write the generated pages"
    )
    parser.add_argument(
        "--check", action="store_true", help="exit 1 when a generated page is stale"
    )
    parser.add_argument(
        "--verify-registry",
        action="store_true",
        help="exit 1 when content/tools.json is not the live registry",
    )
    args = parser.parse_args(argv)

    if args.dump:
        tools = dump_registry()
        TOOLS_JSON.write_text(
            json.dumps(tools, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"tools.json: {len(tools)} tools")
        if not (args.write or args.check or args.verify_registry):
            return 0

    if args.verify_registry:
        if load_registry() != dump_registry():
            raise SystemExit(
                "content/tools.json is not the live registry; "
                "run tools/site/generate_features.py --dump"
            )
        print("tools.json matches the live registry")
        if not (args.write or args.check):
            return 0

    pages = render_all()
    stale = [
        path
        for path, text in pages.items()
        if not path.is_file() or path.read_text(encoding="utf-8") != text
    ]
    if args.write:
        for path, text in pages.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
    elif args.check and stale:
        print("Generated pages are stale; run tools/site/generate_features.py --write:")
        for path in stale:
            print(f"  {path.relative_to(ROOT)}")
        return 1
    print(
        f"{'wrote' if args.write else 'checked'} {len(pages)} generated files; {len(stale)} changed"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
