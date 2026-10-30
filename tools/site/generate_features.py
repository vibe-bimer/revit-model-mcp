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

import catalogs
import contract_diff
import landing
import platform_catalog
import tomllib
import yaml

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "tools/site/content"
TOOLS_JSON = CONTENT / "tools.json"
CAPABILITIES = CONTENT / "capabilities.yaml"
CONTRACTS = CONTENT / "contracts.yaml"
PAGES = ROOT / "docs/features"
JAVASCRIPTS = ROOT / "docs/javascripts"
MKDOCS = ROOT / "mkdocs.yml"
NAV_START = "  # >>> features-nav"
NAV_END = "  # <<< features-nav"
PLATFORM_JSON = platform_catalog.PLATFORM_JSON
PLATFORM_NAV_START = platform_catalog.NAV_START
PLATFORM_NAV_END = platform_catalog.NAV_END
COMMON_PARAMETERS = {"document", "timeout_seconds", "pickup_timeout_seconds"}
RELEASE_VERSION = catalogs.release().version
RELEASE_STATUS = catalogs.release().status
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
        "versions": "版本入口",
        "versions_intro": "本目录记录的是已发布的现有版本；集成分支尚未发布，两者工具数量与清单都不同。下表的状态、版本号与数量都从注册表读取。",
        "entry": "目录",
        "platform_page": "新版基座工具目录",
        "objects": "按模型对象浏览",
        "objects_intro": "视图相关工具按操作的模型对象再分一次：视图、图纸、明细表与视口显示。现有版本没有图纸和明细表的工具，对应位置指向集成分支的同类工具。",
        "branch_tools": "集成分支有 {count} 个同类工具",
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
        "version": "版本",
        "released": "已发布",
        "twin_fact": "集成分支有同名工具",
        "applies_fact": "本页契约适用于发布版",
        "applies_yes": "是",
        "twin_yes": "有",
        "twin_no": "没有",
        "twin_link": "同名集成分支页面",
        "contract_diff": "与集成分支的契约差异",
        "contract_diff_intro": "下表由注册表 inputSchema 自动比较得出，不是手写清单。",
        "contract_diff_note": "本页是发布版 {version} 的契约；集成分支上的同名工具参数不同，请勿混用。",
        "legend": "已实测表示记录过真机执行；仅构建表示通过编译，不代表已完成真机功能验证。Revit 2021 不在本项目构建范围。",
        "index_desc": "当前发布版全部工具的功能总览，按分组列出每个工具的用途、参数与 Revit 年份支持。",
        "matrix_desc": "读取工具与动作工具在 Revit 2020、2026 及 2022–2027 上的验证状态矩阵。",
        "prompts_desc": "可直接复制的提示词库，每个工具配有示例提示词与用途摘要。",
        "version_desc": "Revit {year} 下全部工具的支持范围与验证状态清单，按分组列出。",
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
        "versions": "Version entries",
        "versions_intro": "This catalog records the released version. The integration branch is unreleased, and the two differ in both count and tool list. The status, version number and counts below are read from the registries.",
        "entry": "Catalog",
        "platform_page": "Platform tool catalog",
        "objects": "Browse by model object",
        "objects_intro": "The view-related tools are split again by the model object they act on: views, sheets, schedules and viewport display. The release has no sheet or schedule tools, so those rows point at the same-named tools on the integration branch.",
        "branch_tools": "The integration branch has {count} tools of this kind",
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
        "version": "Version",
        "released": "Released",
        "twin_fact": "Same-name tool on the integration branch",
        "applies_fact": "This contract applies to the release",
        "applies_yes": "Yes",
        "twin_yes": "Yes",
        "twin_no": "No",
        "twin_link": "Same-name integration branch page",
        "contract_diff": "Contract differences from the integration branch",
        "contract_diff_intro": "The list below is computed from the registry inputSchema; it is not a hand-written list.",
        "contract_diff_note": "This page is the contract of release {version}; the same-name tool on the integration branch takes different parameters, so do not mix them.",
        "legend": "Validated live means an execution was recorded on a real workstation. Build only means compilation passed, not live functional validation. Revit 2021 is outside this project's build targets.",
        "index_desc": "Feature overview of every tool in the current release, grouped with each tool's purpose, parameters and Revit year support.",
        "matrix_desc": "Validation status matrix for read and action tools across Revit 2020, 2026 and 2022–2027.",
        "prompts_desc": "Copyable prompt library with a sample prompt and purpose summary for every tool.",
        "version_desc": "Support scope and validation status of every tool for Revit {year}, grouped by task area.",
    },
}


def frontmatter(description: str) -> str:
    """Render the YAML frontmatter that feeds the page description meta tag."""
    return (
        "---\ndescription: " + json.dumps(description, ensure_ascii=False) + "\n---\n\n"
    )


def capability_source(description: str) -> str:
    """Short fingerprint of the English description a capability translation was written from.

    The reviewed Chinese title, summary and prompts in capabilities.yaml are translations, so they
    age whenever the English description changes. Recording the fingerprint makes that drift a
    failing check instead of a silent mismatch a reader has to notice.
    """
    return hashlib.sha256(description.encode()).hexdigest()[:12]


def check_capability_sources(tools: list[dict], capabilities: dict) -> None:
    """Fail when a capability translation predates the English description it translates."""
    stale = [
        tool["name"]
        for tool in tools
        if capabilities["tools"][tool["name"]].get("source")
        != capability_source(tool["description"])
    ]
    if stale:
        raise SystemExit(
            "Stale capability translation source: "
            + ", ".join(sorted(stale))
            + "; review the zh title, summary and prompts, then run "
            "tools/site/generate_features.py --refresh-sources"
        )


def refresh_capability_sources(tools: list[dict]) -> int:
    """Write current fingerprints into capabilities.yaml without reformatting the file."""
    lines = CAPABILITIES.read_text(encoding="utf-8").splitlines(keepends=True)
    wanted = {tool["name"]: capability_source(tool["description"]) for tool in tools}
    header = re.compile(r"^  ([A-Za-z0-9_]+):\s*$")
    starts = [index for index, line in enumerate(lines) if header.match(line)]
    sections = []
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        for index in range(start + 1, len(lines)):
            if not lines[index].startswith((" ", "\n", "#")):
                end = min(end, index)
                break
        sections.append((start, end, header.match(lines[start]).group(1)))
    changed = 0
    for start, end, name in reversed(sections):
        if name not in wanted:
            continue
        block = lines[start + 1 : end]
        entry = f"    source: {wanted[name]}\n"
        for index, line in enumerate(block):
            if re.match(r"^    source: '?[0-9a-f]{12}'?\s*$", line):
                block[index] = entry
                break
        else:
            block.insert(0, entry)
        if block != lines[start + 1 : end]:
            changed += 1
            lines[start + 1 : end] = block
    CAPABILITIES.write_text("".join(lines), encoding="utf-8")
    return changed


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
    check_capability_sources(tools, capabilities)
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
    tool: dict,
    cap: dict,
    lang: str,
    capabilities: dict,
    contracts: dict,
    twin: dict | None = None,
) -> str:
    labels, name = LABELS[lang], tool["name"]
    read_only = bool(tool["annotations"].get("readOnlyHint"))
    facts = [
        f"<b>{labels['group']}</b> {capabilities['groups'][cap['group']][lang]}",
        f"<b>{labels['kind']}</b> {labels['read' if read_only else 'write']}",
        f"<b>{labels['since']}</b> {cap['since']}",
        f"<b>{labels['version']}</b> {labels['released']} {RELEASE_VERSION}",
        f"<b>{labels['twin_fact']}</b> {labels['twin_yes'] if twin is not None else labels['twin_no']}",
        f"<b>{labels['applies_fact']}</b> {labels['applies_yes']}",
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
    if cap.get("origin") == "fork":
        facts.append(
            f"<b>{'来源' if lang == 'zh' else 'Origin'}</b> "
            + ("自研（本仓库）" if lang == "zh" else "Fork (this repository)")
        )
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
    if twin is not None:
        changes = contract_diff.diff_schemas(tool["inputSchema"], twin)
        out += [f"[{labels['twin_link']}](../platform/{name}.md)", ""]
        if changes:
            out += [f"## {labels['contract_diff']} {{#contract-diff}}", ""]
            out += [labels["contract_diff_intro"], ""]
            out += [f"- {line}" for line in contract_diff.render_changes(changes, lang)]
            out += [
                "",
                labels["contract_diff_note"].format(version=RELEASE_VERSION),
                "",
            ]
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
    return frontmatter(cap["summary"][lang]) + "\n".join(out)


def origin_badge(cap: dict, lang: str) -> str:
    """Mark the tools this repository designed, so the base and the fork stay distinguishable."""
    if cap.get("origin") != "fork":
        return ""
    text = "自研" if lang == "zh" else "Fork"
    return f'<span class="state part">{text}</span> '


def index_page(
    tools: list[dict], capabilities: dict, lang: str, branch_count: int | None = None
) -> str:
    labels = LABELS[lang]
    if branch_count is None:
        branch_count = platform_catalog.snapshot()["count"]
    if lang == "zh":
        pointer = (
            f"这一节是现有版本的 {len(tools)} 个工具。集成分支的 {branch_count} 个工具按基座与自研分开，见"
            " [新版基座工具目录](../platform/index.md)。"
        )
    else:
        pointer = (
            f"This section covers the {len(tools)} tools of the current release. The integration branch's"
            f" {branch_count} tools, split into base and fork, are in the"
            " [platform tool catalog](../platform/index.md)."
        )
    branch_tools = platform_catalog.load_platform()[0]
    out = [
        f"# {labels['index']}",
        "",
        LABELS[lang]["counts"].format(**counts(tools)),
        "",
        pointer,
        "",
        f"## {labels['versions']} {{#versions}}",
        "",
        labels["versions_intro"],
        "",
        f"| | {labels['released']} {RELEASE_VERSION} | {platform_catalog.LABELS[lang]['platform']} |",
        "| --- | --- | --- |",
        f"| {labels['version']} | {RELEASE_VERSION} | {platform_catalog.LABELS[lang]['unreleased_fact']} |",
        f"| {platform_catalog.LABELS[lang]['branch']} | main | `{platform_catalog.BRANCH}` |",
        f"| {labels['tools']} | {len(tools)} | {branch_count} |",
        f"| {labels['entry']} | index.md | [{labels['platform_page']}](../platform/index.md) |",
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
                f"| {origin_badge(cap, lang)}[{cap['title'][lang]}]({tool['name']}.md)<br>`{tool['name']}` | {cap['summary'][lang]} |"
            )
        out.append("")
    object_groups = catalogs.object_groups()
    out += [f"## {labels['objects']} {{#objects}}", "", labels["objects_intro"], ""]
    for object_key, object_group in object_groups.items():
        members = [t for t in tools if t["name"] in object_group["tools"]]
        out.append(f"### {object_group[lang]} {{#objects-{object_key}}}")
        out.append("")
        if members:
            out += [
                f"| {labels['tools']} | {labels['summary']} |",
                "| --- | --- |",
            ]
            for tool in members:
                cap = capabilities["tools"][tool["name"]]
                out.append(
                    f"| {origin_badge(cap, lang)}[{cap['title'][lang]}]({tool['name']}.md)<br>`{tool['name']}` | {cap['summary'][lang]} |"
                )
        else:
            # The release has no tool for this object; the branch does, so point at it instead of
            # leaving an empty table with no way forward.
            branch_count_for_group = sum(
                1 for t in branch_tools if t["name"] in object_group["tools"]
            )
            out += [
                "",
                f"{labels['branch_tools'].format(count=branch_count_for_group)}："
                f"[{object_group[lang]}](../platform/index.md#objects-{object_key})。"
                if lang == "zh"
                else f"{labels['branch_tools'].format(count=branch_count_for_group)}: "
                f"[{object_group[lang]}](../platform/index.md#objects-{object_key}).",
                "",
            ]
        out.append("")
    out += [f'!!! warning "{labels["gate"]}"', f"    {labels['gate_body']}", ""]
    return frontmatter(labels["index_desc"]) + "\n".join(out)


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
            f"## {title} ({len(members)}) {{#{'read-tools' if read_only else 'action-tools'}}}",
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
                f"| {origin_badge(cap, lang)}[{cap['title'][lang]}]({tool['name']}.md)<br>`{tool['name']}` | {' | '.join(cells)} |"
            )
        out.append("")
    return frontmatter(labels["matrix_desc"]) + "\n".join(out)


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
                f"### {origin_badge(cap, lang)}[{cap['title'][lang]}]({tool['name']}.md)",
                "",
                f"`{tool['name']}` — {cap['summary'][lang]}",
                "",
            ]
            for prompt in cap["prompts"]:
                out += ["```text", prompt[lang], "```", ""]
    return frontmatter(labels["prompts_desc"]) + "\n".join(out)


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
    return frontmatter(labels["version_desc"].format(year=year)) + "\n".join(out)


def home_page(
    tools: list[dict], capabilities: dict, lang: str, branch_count: int | None = None
) -> str:
    """Render the landing page; the layout lives in landing.py so this file stays registry logic."""
    version = tomllib.loads((ROOT / "server/pyproject.toml").read_text())["project"][
        "version"
    ]
    if branch_count is None:
        branch_count = platform_catalog.snapshot()["count"]
    return landing.home_page(tools, capabilities, version, lang, branch_count)


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


def search_catalog_data(
    tools: list[dict], capabilities: dict, platform_tools: list[dict]
) -> str:
    """Ship the catalog behind the search results, so a result can name its version.

    The search index only knows a page's location, title and text. This file gives the browser the
    stable tool name, the human title and the catalog status for both surfaces, so a result can
    carry a status badge and an exact tool-name query can surface a page the engine did not rank.
    """
    release, integration = catalogs.release(), catalogs.integration()
    payload = {
        "release": {
            "catalog": "release",
            "status": release.status,
            "version": release.version,
            "branch": release.branch,
            "directory": release.directory,
            "tools": {
                tool["name"]: {
                    "zh": capabilities["tools"][tool["name"]]["title"]["zh"],
                    "en": capabilities["tools"][tool["name"]]["title"]["en"],
                }
                for tool in tools
            },
        },
        "branch": {
            "catalog": "branch",
            "status": integration.status,
            "version": "",
            "branch": integration.branch,
            "directory": integration.directory,
            "tools": {
                tool["name"]: {
                    "zh": platform_catalog.ZH[tool["name"]][0],
                    "en": tool["title"] or tool["name"],
                }
                for tool in platform_tools
            },
        },
        "objects": {
            key: {"zh": group["zh"], "en": group["en"]}
            for key, group in catalogs.object_groups().items()
        },
    }
    body = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return (
        "/* Generated by tools/site/generate_features.py from the catalog registries;"
        " do not edit. */\n"
        f"window.__RMM_CATALOG__ = {body};\n"
    )


def generate(tools: list[dict], capabilities: dict, contracts: dict) -> dict[Path, str]:
    platform_tools, _ = platform_catalog.load_platform()
    integration_schemas = {tool["name"]: tool["inputSchema"] for tool in platform_tools}
    branch_count = len(platform_tools)
    files = {}
    for lang, suffix in (("zh", ""), ("en", ".en")):

        def page(name: str, suffix: str = suffix) -> Path:
            return PAGES / f"{name}{suffix}.md"

        files[ROOT / f"docs/index{suffix}.md"] = home_page(
            tools, capabilities, lang, branch_count
        )
        files[page("index")] = index_page(tools, capabilities, lang, branch_count)
        files[page("matrix")] = matrix_page(tools, capabilities, lang)
        files[page("prompts")] = prompts_page(tools, capabilities, lang)
        for year in ("2020", "2026"):
            files[page(f"v{year}")] = version_page(tools, capabilities, lang, year)
        for tool in tools:
            files[page(tool["name"])] = tool_page(
                tool,
                capabilities["tools"][tool["name"]],
                lang,
                capabilities,
                contracts,
                integration_schemas.get(tool["name"]),
            )
    text = MKDOCS.read_text(encoding="utf-8")
    files[MKDOCS] = re.sub(
        re.escape(NAV_START) + r".*?" + re.escape(NAV_END),
        nav_block(tools, capabilities),
        text,
        flags=re.DOTALL,
    )
    files.update(platform_catalog.generate())
    files[JAVASCRIPTS / "search-catalog.js"] = search_catalog_data(
        tools, capabilities, platform_tools
    )
    files[MKDOCS] = re.sub(
        re.escape(PLATFORM_NAV_START) + r".*?" + re.escape(PLATFORM_NAV_END),
        platform_catalog.nav_block(platform_tools),
        files[MKDOCS],
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


def dump_platform(worktree: Path, branch: str) -> dict:
    """Snapshot the integration branch's registry without checking the branch out.

    The toolset and access flags are not in the MCP payload, so they are joined from the branch's
    generated manifest. The two name sets must agree, or the snapshot would describe a registry
    nobody is running.
    """
    server = worktree / "server"
    if not (server / "pyproject.toml").is_file():
        raise SystemExit(f"Not a server worktree: {server}")
    command = ["uv", "run", "revit-model-mcp"]
    env = dict(
        os.environ,
        REVIT_MCP_HOST="http://127.0.0.1:53110",
        REVIT_MCP_TOKEN="dump",
        REVIT_MCP_READ_ONLY="0",
    )
    with subprocess.Popen(
        command,
        cwd=server,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        text=True,
        bufsize=1,
    ) as proc:

        def call(method: str, rid: int, params: dict | None = None) -> dict:
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
            tools = call("tools/list", 2)["result"]["tools"]
        finally:
            proc.terminate()

    manifest = subprocess.run(
        ["git", "-C", str(worktree), "show", f"{branch}:docs/tool-manifest.json"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    declared = {item["name"]: item for item in json.loads(manifest)["tools"]}
    names = {tool["name"] for tool in tools}
    if names != set(declared):
        raise SystemExit(
            "The branch registry and its manifest disagree: "
            f"only in registry={sorted(names - set(declared))}, "
            f"only in manifest={sorted(set(declared) - names)}"
        )
    commit = subprocess.run(
        ["git", "-C", str(worktree), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    payload = {
        "count": len(tools),
        "provenance": {
            "branch": branch,
            "commit": commit,
            "source": "server tools/list plus docs/tool-manifest.json on the branch",
        },
        "tools": [
            {
                "name": tool["name"],
                "title": tool.get("title") or "",
                "description": tool.get("description") or "",
                "toolset": declared[tool["name"]]["toolset"],
                "readOnly": bool(tool["annotations"].get("readOnlyHint")),
                "destructive": bool(tool["annotations"].get("destructiveHint")),
                "inputSchema": tool["inputSchema"],
            }
            for tool in sorted(
                tools,
                key=lambda item: (declared[item["name"]]["toolset"], item["name"]),
            )
        ],
    }
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dump", action="store_true")
    parser.add_argument(
        "--dump-platform",
        metavar="WORKTREE",
        help="snapshot the integration branch registry from a checkout of that branch",
    )
    parser.add_argument(
        "--refresh-sources",
        action="store_true",
        help="record the current English description fingerprints in capabilities.yaml",
    )
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--verify-registry",
        action="store_true",
        help="fail if tools.json differs from the current MCP tool registry",
    )
    args = parser.parse_args()
    if args.dump_platform:
        payload = dump_platform(Path(args.dump_platform), platform_catalog.BRANCH)
        PLATFORM_JSON.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(
            f"platform-tools.json: {payload['count']} tools from {payload['provenance']['commit'][:7]}"
        )
        return 0
    if args.dump:
        tools = dump_registry()
        TOOLS_JSON.write_text(
            json.dumps(tools, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"tools.json: {len(tools)} tools")
        return 0
    if args.refresh_sources:
        changed = refresh_capability_sources(
            json.loads(TOOLS_JSON.read_text(encoding="utf-8"))
        )
        print(f"capabilities.yaml: {changed} source fingerprints updated")
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
