#!/usr/bin/env python3
"""Generate paired feature pages and navigation from the MCP registry and reviewed translations.

Run --dump after a tool change, update capabilities.yaml and contracts.yaml,
then run --write. --check fails on missing translations or stale generated pages.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import tomllib
import yaml

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "tools/site/content"
TOOLS_JSON = CONTENT / "tools.json"
CAPABILITIES = CONTENT / "capabilities.yaml"
CONTRACTS = CONTENT / "contracts.yaml"
PAGES = ROOT / "docs/features"
MKDOCS = ROOT / "mkdocs.yml"
NAV_START = "  # >>> features-nav"
NAV_END = "  # <<< features-nav"
COMMON_PARAMETERS = {"document", "timeout_seconds", "pickup_timeout_seconds"}
LABELS = {
    "zh": {
        "group": "分组",
        "kind": "类型",
        "read": "读取（只读）",
        "write": "动作（需授权）",
        "since": "起始版本",
        "parameters": "参数",
        "common": "通用参数",
        "name": "参数",
        "required": "必填",
        "default": "默认值",
        "type": "类型",
        "meaning": "说明",
        "prompts": "可复制提示词",
        "years": "Revit 年份支持",
        "year": "Revit 年份",
        "state": "验证状态",
        "note": "备注",
        "notes": "使用提示",
        "tools": "工具",
        "yes": "是",
        "no": "否",
        "verified": "已实测",
        "built": "仅构建，未实测",
        "unsupported": "不支持",
        "other": "2022–2025 / 2027",
        "summary": "用途",
        "index": "功能总览",
        "matrix": "版本支持矩阵",
        "prompts_page": "提示词库",
        "all_tools": "全部功能",
        "by_version": "按 Revit 年份查阅",
        "contract": "功能说明与返回结果",
        "gate": "动作工具需要双门禁",
        "gate_body": "客户端设置 `REVIT_MCP_ALLOW_WRITE=1`，工作站创建 `allow-write` 文件。动作连接必须指向单一 Revit 实例；实例中有多个文档时，用 `document` 明确目标。选择、显示和隔离还要求目标文档处于活动状态。",
        "counts": "{read} 个读取 + {write} 个动作，共 {total} 个工具",
        "effect": "影响范围",
        "ui": "选择 / 视图状态",
        "file": "新模型文件；源模型不变",
        "model": "模型构件 / 参数",
        "no_specific": "此工具没有额外业务参数，使用下列通用参数即可。",
        "legend": "已实测表示记录过真机执行；仅构建表示通过编译，不代表已完成真机功能验证。Revit 2021 不在本项目构建范围。",
    },
    "en": {
        "group": "Group",
        "kind": "Kind",
        "read": "Read (read-only)",
        "write": "Action (opt-in)",
        "since": "Since",
        "parameters": "Parameters",
        "common": "Common parameters",
        "name": "Parameter",
        "required": "Required",
        "default": "Default",
        "type": "Type",
        "meaning": "Meaning",
        "prompts": "Copyable prompts",
        "years": "Revit year support",
        "year": "Revit year",
        "state": "Validation",
        "note": "Note",
        "notes": "Usage notes",
        "tools": "Tool",
        "yes": "Yes",
        "no": "No",
        "verified": "Validated live",
        "built": "Build only, not live-tested",
        "unsupported": "Unsupported",
        "other": "2022–2025 / 2027",
        "summary": "Purpose",
        "index": "Feature overview",
        "matrix": "Version support matrix",
        "prompts_page": "Prompt library",
        "all_tools": "All features",
        "by_version": "Browse by Revit year",
        "contract": "Behavior and returned data",
        "gate": "Actions require both write gates",
        "gate_body": "Set `REVIT_MCP_ALLOW_WRITE=1` in the client and create the workstation `allow-write` file. The action connection must address one Revit instance; use `document` when it has multiple open documents. Selection, navigation and isolation also require the target document to be active.",
        "counts": "{read} read + {write} action tools, {total} in total",
        "effect": "Effect",
        "ui": "Selection / view state",
        "file": "New model files; source unchanged",
        "model": "Model elements / parameters",
        "no_specific": "No additional business parameters; use the common parameters below.",
        "legend": "Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.",
    },
}


def load() -> tuple[list[dict], dict, dict]:
    tools = json.loads(TOOLS_JSON.read_text(encoding="utf-8"))
    capabilities = yaml.safe_load(CAPABILITIES.read_text(encoding="utf-8"))
    contracts = yaml.safe_load(CONTRACTS.read_text(encoding="utf-8"))["tools"]
    known = {tool["name"] for tool in tools}
    for source, mapping in (
        ("capabilities.yaml", capabilities["tools"]),
        ("contracts.yaml", contracts),
    ):
        if set(mapping) != known:
            raise SystemExit(
                f"{source} tool mismatch: missing={sorted(known - set(mapping))}, extra={sorted(set(mapping) - known)}"
            )
    for tool in tools:
        name = tool["name"]
        cap = capabilities["tools"][name]
        digest = hashlib.sha256(tool["description"].encode()).hexdigest()
        if contracts[name]["source"] != digest or not contracts[name].get("zh"):
            raise SystemExit(f"Missing or stale Chinese contract: {name}")
        for lang in ("zh", "en"):
            for field in ("title", "summary"):
                if not cap.get(field, {}).get(lang):
                    raise SystemExit(f"Missing {lang} {field}: {name}")
            if not cap.get("prompts") or any(
                not item.get(lang) for item in cap["prompts"]
            ):
                raise SystemExit(f"Missing {lang} prompt: {name}")
            for param, spec in tool["inputSchema"]["properties"].items():
                parameter_meaning(tool, param, spec, capabilities, lang)
    return tools, capabilities, contracts


def parameter_meaning(
    tool: dict, name: str, spec: dict, capabilities: dict, lang: str
) -> str:
    written = capabilities.get("param_notes", {}).get(tool["name"], {}).get(name, {})
    shared = capabilities.get("param_defaults", {}).get(name, {})
    for note in (written, shared):
        if note.get(lang):
            return note[lang]
    if lang == "en" and spec.get("description"):
        return " ".join(spec["description"].split())
    raise SystemExit(f"Missing {lang} parameter meaning: {tool['name']}.{name}")


def schema_type(spec: dict) -> str:
    if "anyOf" in spec:
        return " / ".join(schema_type(item) for item in spec["anyOf"])
    kind = spec.get("type", "any")
    return f"array<{schema_type(spec.get('items', {}))}>" if kind == "array" else kind


def table_rows(tool: dict, common: bool, capabilities: dict, lang: str) -> list[str]:
    labels = LABELS[lang]
    schema = tool["inputSchema"]
    required = set(schema.get("required", []))
    rows = []
    for name, spec in sorted(
        schema["properties"].items(),
        key=lambda item: (item[0] not in required, item[0]),
    ):
        if (name in COMMON_PARAMETERS) != common:
            continue
        default = (
            f"`{json.dumps(spec['default'], ensure_ascii=False)}`"
            if "default" in spec
            else "—"
        )
        meaning = parameter_meaning(tool, name, spec, capabilities, lang).replace(
            "|", "\\|"
        )
        rows.append(
            f"| `{name}` | {labels['yes'] if name in required else labels['no']} | {default} | `{schema_type(spec)}` | {meaning} |"
        )
    return rows


def table_heading(labels: dict) -> list[str]:
    return [
        f"| {labels['name']} | {labels['required']} | {labels['default']} | {labels['type']} | {labels['meaning']} |",
        "| --- | :--: | --- | --- | --- |",
    ]


def state_badge(state: str, labels: dict) -> str:
    style, key = {
        "validated": ("ok", "verified"),
        "built": ("part", "built"),
        "no": ("no", "unsupported"),
    }[state]
    return f'<span class="state {style}">{labels[key]}</span>'


def counts(tools: list[dict]) -> dict:
    read = sum(bool(t["annotations"].get("readOnlyHint")) for t in tools)
    return {"read": read, "write": len(tools) - read, "total": len(tools)}


def year_counts(tools: list[dict], capabilities: dict, year: str, lang: str) -> str:
    result = {}
    for read_only, label in ((True, "read"), (False, "write")):
        members = [
            t for t in tools if bool(t["annotations"].get("readOnlyHint")) == read_only
        ]
        result[label] = sum(
            capabilities["tools"][t["name"]]["years"][year]["state"] == "validated"
            for t in members
        )
        result[f"{label}_total"] = len(members)
    if lang == "zh":
        return f"读取 {result['read']}/{result['read_total']}、动作 {result['write']}/{result['write_total']} 已实测；其余仅构建"
    return f"{result['read']}/{result['read_total']} reads and {result['write']}/{result['write_total']} actions validated live; the rest are build-only"


def tool_page(
    tool: dict, cap: dict, lang: str, capabilities: dict, contracts: dict
) -> str:
    labels, name = LABELS[lang], tool["name"]
    read_only = bool(tool["annotations"].get("readOnlyHint"))
    facts = [
        f"<b>{labels['group']}</b> {capabilities['groups'][cap['group']][lang]}",
        f"<b>{labels['kind']}</b> {labels['read' if read_only else 'write']}",
        f"<b>{labels['since']}</b> {cap['since']}",
    ]
    if not read_only:
        effect = (
            "ui"
            if cap["group"] == "display"
            else "file"
            if name == "revit_rebuild_model_ids"
            else "model"
        )
        facts.append(f"<b>{labels['effect']}</b> {labels[effect]}")
    out = [
        f"# {cap['title'][lang]}",
        "",
        f"`{name}`",
        "",
        '<p class="facts">'
        + "".join(f"<span>{fact}</span>" for fact in facts)
        + "</p>",
        "",
        cap["summary"][lang],
        "",
    ]
    if not read_only:
        out += [f'!!! warning "{labels["gate"]}"', f"    {labels['gate_body']}", ""]
    if cap.get("note", {}).get(lang):
        out += [f'!!! note "{labels["notes"]}"', f"    {cap['note'][lang]}", ""]
    out += [f"## {labels['prompts']} {{#prompts}}", ""]
    for prompt in cap["prompts"]:
        out += ["```text", prompt[lang], "```", ""]
    out += [f"## {labels['parameters']} {{#parameters}}", ""]
    rows = table_rows(tool, False, capabilities, lang)
    out += table_heading(labels) + rows if rows else [labels["no_specific"]]
    common = table_rows(tool, True, capabilities, lang)
    if common:
        out += (
            ["", f"### {labels['common']} {{#common-parameters}}", ""]
            + table_heading(labels)
            + common
        )
    description = contracts[name]["zh"] if lang == "zh" else tool["description"]
    description = "\n".join(line.strip() for line in description.strip().splitlines())
    out += ["", f"## {labels['contract']} {{#contract}}", ""]
    if read_only and name != "revit_list_instances":
        warning = (
            "以下保留当前工具声明的完整译文。文件通道实现仍有例外：它可能返回 `success:false`、`partial:true` 的终态部分数据，而不抛出声明中的错误。完整结果必须满足 `success:true` 且 `partial:false`（或没有该字段）；等待超时不取消任务。详见[读取响应契约](../tools.md)。"
            if lang == "zh"
            else "The complete current tool declaration is preserved below. The file channel has an implementation exception: it may return terminal `success:false`, `partial:true` data instead of the promised error. Accept complete results only with `success:true` and `partial:false` (or no partial field); a wait timeout does not cancel the job. See the [read response contract](../tools.md)."
        )
        out += [f'!!! note "{labels["notes"]}"', f"    {warning}", ""]
    out += [
        description,
        "",
        f"## {labels['years']} {{#year-support}}",
        "",
        f"| {labels['year']} | {labels['state']} |",
        "| --- | --- |",
    ]
    for year in ("2020", "2026", "other"):
        out.append(
            f"| {labels['other'] if year == 'other' else year} | {state_badge(cap['years'][year]['state'], labels)} |"
        )
    out += [
        "",
        labels["legend"],
        "",
        "---",
        "",
        f"[{labels['all_tools']}](index.md) · [{labels['matrix']}](matrix.md) · [{labels['prompts_page']}](prompts.md)",
        "",
    ]
    return "\n".join(out)


def index_page(tools: list[dict], capabilities: dict, lang: str) -> str:
    labels = LABELS[lang]
    out = [
        f"# {labels['index']}",
        "",
        LABELS[lang]["counts"].format(**counts(tools)),
        "",
        f"## {labels['by_version']} {{#by-version}}",
        "",
        f"| {labels['year']} | {labels['state']} |",
        "| --- | --- |",
    ]
    for year in ("2020", "2026"):
        out.append(
            f"| [Revit {year}](v{year}.md) | {year_counts(tools, capabilities, year, lang)} |"
        )
    out += [
        f"| 2022–2025 / 2027 | {labels['built']} |",
        "",
        labels["legend"],
        "",
        f"## {labels['all_tools']} {{#all-features}}",
        "",
    ]
    for key, group in capabilities["groups"].items():
        members = [t for t in tools if capabilities["tools"][t["name"]]["group"] == key]
        out += [
            f"### {group[lang]} ({len(members)}) {{#group-{key}}}",
            "",
            f"| {labels['tools']} | {labels['summary']} |",
            "| --- | --- |",
        ]
        for tool in members:
            cap = capabilities["tools"][tool["name"]]
            out.append(
                f"| [{cap['title'][lang]}]({tool['name']}.md)<br>`{tool['name']}` | {cap['summary'][lang]} |"
            )
        out.append("")
    out += [f'!!! warning "{labels["gate"]}"', f"    {labels['gate_body']}", ""]
    return "\n".join(out)


def matrix_page(tools: list[dict], capabilities: dict, lang: str) -> str:
    labels = LABELS[lang]
    out = [f"# {labels['matrix']}", "", labels["legend"], ""]
    for read_only in (True, False):
        members = [
            t for t in tools if bool(t["annotations"].get("readOnlyHint")) == read_only
        ]
        title = (
            ("读取工具" if read_only else "动作工具")
            if lang == "zh"
            else ("Read tools" if read_only else "Action tools")
        )
        out += [
            f"## {title} ({len(members)}) {{'#read-tools' if read_only else '#action-tools'}}",
            "",
            f"| {labels['tools']} | 2020 | 2026 | {labels['other']} |",
            "| --- | :--: | :--: | :--: |",
        ]
        for tool in members:
            cap = capabilities["tools"][tool["name"]]
            cells = [
                state_badge(cap["years"][year]["state"], labels)
                for year in ("2020", "2026", "other")
            ]
            out.append(
                f"| [{cap['title'][lang]}]({tool['name']}.md)<br>`{tool['name']}` | {' | '.join(cells)} |"
            )
        out.append("")
    return "\n".join(out)


def prompts_page(tools: list[dict], capabilities: dict, lang: str) -> str:
    labels = LABELS[lang]
    out = [
        f"# {labels['prompts_page']}",
        "",
        labels["counts"].format(**counts(tools)),
        "",
        labels["gate_body"],
        "",
    ]
    for key, group in capabilities["groups"].items():
        out += [f"## {group[lang]} {{#group-{key}}}", ""]
        for tool in tools:
            cap = capabilities["tools"][tool["name"]]
            if cap["group"] != key:
                continue
            out += [
                f"### [{cap['title'][lang]}]({tool['name']}.md)",
                "",
                f"`{tool['name']}` — {cap['summary'][lang]}",
                "",
            ]
            for prompt in cap["prompts"]:
                out += ["```text", prompt[lang], "```", ""]
    return "\n".join(out)


def version_page(tools: list[dict], capabilities: dict, lang: str, year: str) -> str:
    labels = LABELS[lang]
    out = [
        f"# Revit {year}",
        "",
        labels["counts"].format(**counts(tools)),
        "",
        year_counts(tools, capabilities, year, lang),
        "",
        labels["legend"],
        "",
    ]
    notes = capabilities.get("year_notes", {}).get(year, {}).get(lang, [])
    if notes:
        out += (
            [
                "## "
                + ("年份差异" if lang == "zh" else "Year-specific differences")
                + " {#year-differences}",
                "",
            ]
            + [f"- {line}" for line in notes]
            + [""]
        )
    for key, group in capabilities["groups"].items():
        members = [t for t in tools if capabilities["tools"][t["name"]]["group"] == key]
        out += [
            f"## {group[lang]} {{#group-{key}}}",
            "",
            f"| {labels['tools']} | {labels['summary']} | {labels['state']} |",
            "| --- | --- | --- |",
        ]
        for tool in members:
            cap = capabilities["tools"][tool["name"]]
            out.append(
                f"| [{cap['title'][lang]}]({tool['name']}.md)<br>`{tool['name']}` | {cap['summary'][lang]} | {state_badge(cap['years'][year]['state'], labels)} |"
            )
        out.append("")
    return "\n".join(out)


def home_page(tools: list[dict], lang: str) -> str:
    version = tomllib.loads((ROOT / "server/pyproject.toml").read_text())["project"][
        "version"
    ]
    info = LABELS[lang]["counts"].format(**counts(tools))
    if lang == "zh":
        return f"""# Revit Model MCP

<p class="facts"><span><b>插件 / MCP 版本 {version}</b></span><span>Revit <b>2020 / 2022–2027</b></span><span>{info}</span></p>

面向 Revit 技术人员的功能手册：查参数与几何、统计构件、检查模型、导出清单、编辑构件，以及复制模型并换新 ID。默认只读，动作需要双门禁。**Revit 年份**与**插件发布版本**是两种不同的版本；实测覆盖以支持矩阵为准。

## 选择查阅入口 {{#entry-points}}

<div class="grid cards" markdown>

- **确认 Revit 年份支持**

    [Revit 2020](features/v2020.md) · [Revit 2026](features/v2026.md) · [支持矩阵](features/matrix.md)

- **查某个功能和参数**

    [功能总览](features/index.md)：按场景分类，每项都有用途、参数、返回结果与限制。

- **复制提示词使用**

    [提示词库](features/prompts.md)：按功能分组，复制后替换模型、标高、构件 ID 和文件路径。

- **安装并连接 MCP**

    [安装与配置](server.md) · [传输与接入](transport.md) · [动作门禁](actions.md#gates)

</div>

## 三步上手 {{#get-started}}

1. 在 Windows Revit 工作站安装插件，在 AI 客户端配置 MCP 服务器；具体步骤见[安装与配置](server.md)。
2. 先做只读查询，例如 `统计 1F 上各种墙类型各有多少个`。过滤名称应先从模型目录获取。
3. 需要动作时再打开双门禁。修改前优先使用支持该参数的工具做 `dry_run`；超时后先核对模型，不要盲目重试。

## 常用提示词 {{#common-prompts}}

| 场景 | 提示词 |
| --- | --- |
| 统计 | `统计 1F 上各种墙类型各有多少个` |
| 检查 | `做一次交付前体检：文件大小、各类数量、单位设置、最多的警告` |
| 导出 | `把模型中已绘制构件的 ID 清单导出成 Excel，按类别、族、类型排序` |
| 移动 | `把 ID 为 123456 的构件沿 X 移动 500 mm，先彩排` |
| 新模型 ID | `把当前三维视图里能选中的构件重建到 E:\\out\\copy-{{n}}.rvt，出 10 份，逐份检查构件数量和 ID 映射` |

## 进一步查阅 {{#further-reading}}

<a id="tools"></a>
<a id="actions-opt-in"></a>

- 功能用法：[功能总览](features/index.md) · [提示词库](features/prompts.md)
- 跨工具契约：[读取契约](tools.md) · [动作契约](actions.md)
- 项目信息：[更新记录](changelog.md) · [隐私说明](privacy.md)

右上角切换中文 / English 和浅色 / 深色；同一页面切换语言后保留对应内容。
"""
    return f"""# Revit Model MCP

<p class="facts"><span><b>Add-in / MCP version {version}</b></span><span>Revit <b>2020 / 2022–2027</b></span><span>{info}</span></p>

A feature handbook for Revit technical users: inspect parameters and geometry, count elements, check models, export registers, edit elements, and copy models with new IDs. Read-only by default; actions require both gates. **Revit years** and **add-in release versions** are different version axes. See the support matrix for live validation coverage.

## Choose an entry point {{#entry-points}}

<div class="grid cards" markdown>

- **Check your Revit year**

    [Revit 2020](features/v2020.md) · [Revit 2026](features/v2026.md) · [Support matrix](features/matrix.md)

- **Look up a feature and its parameters**

    [Feature overview](features/index.md): grouped by task, with behavior, parameters, returned data and limits.

- **Copy a prompt**

    [Prompt library](features/prompts.md): replace the model, level, element IDs and file paths with your own.

- **Install and connect MCP**

    [Installation and configuration](server.md) · [Transport and connection](transport.md) · [Action gates](actions.md#gates)

</div>

## Get started in three steps {{#get-started}}

1. Install the add-in on the Windows Revit workstation and configure the MCP server in your AI client. See [installation and configuration](server.md).
2. Start with a read-only query, such as `How many of each wall type are on 1F?` Discover filter names from the model catalog first.
3. Enable both gates only when actions are needed. Preview edits with tools supporting `dry_run`; after a timeout, inspect the model before retrying.

## Common prompts {{#common-prompts}}

| Task | Prompt |
| --- | --- |
| Count | `How many of each wall type are on 1F?` |
| Check | `Run a pre-handover health check: size, category counts, units and top warnings` |
| Export | `Export the ID register of the drawn model components to Excel, ordered by category, family and type` |
| Move | `Move element 123456 by 500 mm along X, dry run first` |
| New-model IDs | `Rebuild selectable components from the current 3D view into E:\\out\\copy-{{n}}.rvt, ten copies; check each copy's count and ID mapping` |

## Further reading {{#further-reading}}

<a id="tools"></a>
<a id="actions-opt-in"></a>

- Feature usage: [overview](features/index.md) · [prompts](features/prompts.md)
- Cross-tool contracts: [read contracts](tools.md) · [action contracts](actions.md)
- Project information: [changelog](changelog.md) · [privacy](privacy.md)

Use the top-right controls for Chinese / English and light / dark. Switching language keeps you on the corresponding page.
"""


def nav_block(tools: list[dict], capabilities: dict) -> str:
    lines = [
        NAV_START,
        "  - 功能:",
        "      - features/index.md",
        "      - 按 Revit 年份:",
        "          - Revit 2020: features/v2020.md",
        "          - Revit 2026: features/v2026.md",
        "          - features/matrix.md",
    ]
    for read_only, section in ((True, "读取功能"), (False, "动作功能")):
        lines.append(f"      - {section}:")
        for key, group in capabilities["groups"].items():
            members = [
                t
                for t in tools
                if capabilities["tools"][t["name"]]["group"] == key
                and bool(t["annotations"].get("readOnlyHint")) == read_only
            ]
            if members:
                lines.append(f"          - {group['zh']}:")
                lines.extend(
                    f"              - features/{t['name']}.md" for t in members
                )
    lines += ["      - features/prompts.md", NAV_END]
    return "\n".join(lines)


def generate(tools: list[dict], capabilities: dict, contracts: dict) -> dict[Path, str]:
    files = {}
    for lang, suffix in (("zh", ""), ("en", ".en")):

        def page(name: str, suffix: str = suffix) -> Path:
            return PAGES / f"{name}{suffix}.md"

        files[ROOT / f"docs/index{suffix}.md"] = home_page(tools, lang)
        files[page("index")] = index_page(tools, capabilities, lang)
        files[page("matrix")] = matrix_page(tools, capabilities, lang)
        files[page("prompts")] = prompts_page(tools, capabilities, lang)
        for year in ("2020", "2026"):
            files[page(f"v{year}")] = version_page(tools, capabilities, lang, year)
        for tool in tools:
            files[page(tool["name"])] = tool_page(
                tool, capabilities["tools"][tool["name"]], lang, capabilities, contracts
            )
    text = MKDOCS.read_text(encoding="utf-8")
    files[MKDOCS] = re.sub(
        re.escape(NAV_START) + r".*?" + re.escape(NAV_END),
        nav_block(tools, capabilities),
        text,
        flags=re.DOTALL,
    )
    return files


def dump_registry() -> list[dict]:
    executable = ROOT / "server/.venv/bin/revit-model-mcp"
    command = (
        [str(executable)]
        if executable.exists()
        else [sys.executable, "-m", "revit_model_mcp"]
    )
    env = dict(
        os.environ,
        REVIT_MCP_HOST="http://127.0.0.1:53110",
        REVIT_MCP_TOKEN="dump",
        REVIT_MCP_ALLOW_WRITE="1",
    )
    with subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        text=True,
        bufsize=1,
    ) as proc:

        def call(method: str, rid: int, params: dict | None = None):
            proc.stdin.write(
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": rid,
                        "method": method,
                        "params": params or {},
                    }
                )
                + "\n"
            )
            proc.stdin.flush()
            while line := proc.stdout.readline():
                try:
                    message = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if message.get("id") == rid:
                    return message
            raise SystemExit("The MCP server closed the connection while listing tools")

        try:
            call(
                "initialize",
                1,
                {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "docs", "version": "1"},
                },
            )
            proc.stdin.write(
                json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"})
                + "\n"
            )
            proc.stdin.flush()
            return call("tools/list", 2)["result"]["tools"]
        finally:
            proc.terminate()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dump", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--verify-registry",
        action="store_true",
        help="fail if tools.json differs from the current MCP tool registry",
    )
    args = parser.parse_args()
    if args.dump:
        tools = dump_registry()
        TOOLS_JSON.write_text(
            json.dumps(tools, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"tools.json: {len(tools)} tools")
        return 0
    if args.verify_registry and json.loads(TOOLS_JSON.read_text()) != dump_registry():
        raise SystemExit(
            "tools.json is stale; run --dump and update both languages before publishing"
        )
    tools, capabilities, contracts = load()
    files = generate(tools, capabilities, contracts)
    stale = []
    for path, content in files.items():
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            stale.append(path.relative_to(ROOT))
            if args.write:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
    if args.check and stale:
        print("Generated pages are stale; run tools/site/generate_features.py --write:")
        for path in stale:
            print(f"  {path}")
        return 1
    print(
        f"{'wrote' if args.write else 'checked'} {len(files)} generated files; {len(stale)} changed"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
