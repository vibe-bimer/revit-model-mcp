"""Build the bilingual landing page from the live tool registry.

The landing page is generated rather than hand-written so every number on it comes from
`content/tools.json` and every prompt comes from `capabilities.yaml`: a tool added to the registry
appears here without anyone remembering to edit prose. The structure is hand-authored HTML because
the page is a composed layout, not Markdown prose.

Anchors `#tools` and `#actions-opt-in` are linked from six repository files outside the site, so the
sections that carry them keep their identifiers.
"""

from __future__ import annotations

from pathlib import Path

CONTENT = Path(__file__).resolve().parent / "content"

# Prompts shown on the landing page, in reading order. Each entry names a tool whose first reviewed
# prompt is quoted verbatim from capabilities.yaml.
SHOWCASE = [
    ("revit_aggregate_elements", "read"),
    ("revit_model_health", "read"),
    ("revit_query_elements", "read"),
    ("revit_export_element_ids", "read"),
    ("revit_move", "action"),
]

TEXT = {
    "zh": {
        "title": "Revit Model MCP",
        "eyebrow": "插件 / MCP 版本 {version}",
        "lede": "把 Autodesk Revit 模型接到 AI 助手上：查参数与几何、统计构件、检查模型、导出清单、编辑构件，"
        "以及复制模型并换新 ID。默认只读，动作需要双门禁。",
        "cta_install": "开始安装",
        "cta_browse": "浏览 {total} 个功能",
        "stat_read": "读取工具",
        "stat_action": "动作工具",
        "stat_years": "Revit 年份",
        "stat_transport": "传输方式",
        "stat_read_note": "只读模型与视图",
        "stat_action_note": "需双门禁授权",
        "stat_years_note": "2020 与 2022–2027",
        "stat_transport_note": "本机 · SSH · HTTP",
        "s1_num": "01",
        "s1_title": "先问一句",
        "s1_lede": "提示词原样复制即可使用，替换模型、标高、构件 ID 和文件路径换成你自己的。",
        "s1_link": "提示词库",
        "s1_band": "写入时同样是一句话，但需要双门禁",
        "s2_num": "02",
        "s2_title": "能力范围",
        "s2_lede": "按场景分成 {groups} 组，共 {total} 个工具。每个工具页都有用途、参数、返回结果与限制。",
        "s2_link": "功能总览",
        "s3_num": "03",
        "s3_title": "看见结果",
        "s3_lede": "下面这张图是 Revit 示例项目的三维视图，由 revit_export_view 直接导出，没有做过任何后处理。",
        "s3_link": "导出视图图片",
        "s3_caption": "revit_export_view 导出的视图 PNG，跟随当前深浅色主题切换。",
        "s3_alt": "由 revit_export_view 从 Revit 示例项目导出的三层办公楼三维视图",
        "s4_num": "04",
        "s4_title": "工作原理",
        "s4_lede": "服务器在 MCP 客户端所在机器上，插件在 Windows 的 Revit 进程内；两者通过本机通道、SSH 或 HTTP 通信。",
        "s4_link": "工作原理",
        "s5_num": "05",
        "s5_title": "安全边界",
        "s5_lede": "默认只读。写入需要同时打开两道门禁，任一道关闭即回到只读。",
        "s5_link": "动作契约",
        "s6_num": "06",
        "s6_title": "三步上手",
        "s6_link": "安装与配置",
        "s7_num": "07",
        "s7_title": "继续查阅",
        "read": "读取",
        "action": "动作",
        "copy": "复制",
        "step1": "在 Windows Revit 工作站安装插件，在 AI 客户端配置 MCP 服务器。",
        "step2": "先做只读查询：过滤用的名称先从模型目录获取，再按类别、族、类型或标高统计。",
        "step3": "需要动作时再打开双门禁；修改前先用支持该参数的工具做 dry_run，超时后先核对模型。",
        "flow": [
            ("AI 客户端", "通过 stdio 调用 MCP 工具"),
            ("Python 服务器", "构造命令，选择本机通道、SSH 或 HTTP"),
            ("Revit 插件", "在 ExternalEvent 中调用 Revit API"),
            ("模型", "返回 JSON；写操作在同一事务内完成"),
        ],
        "gate1": "客户端设置 REVIT_MCP_ALLOW_WRITE=1",
        "gate2": "工作站创建 allow-write 门禁文件",
        "safety_points": [
            ("默认只读", "工具默认只读取模型数据，或将视图导出为 PNG。"),
            ("双门禁", "环境变量与门禁文件必须同时存在，动作工具才会注册与执行。"),
            ("先彩排", "支持 dry_run 的工具会执行后回滚，返回同样的校验结果。"),
            ("超时须核对", "超时或校验失败之后，改动可能已经提交；先核对模型再重试。"),
        ],
        "entries": [
            (
                "按 Revit 年份",
                "确认某一年份支持哪些功能，以及哪些已实测。",
                "features/matrix/",
                "支持矩阵",
            ),
            ("跨工具契约", "读取契约、动作契约与文件通道格式。", "tools/", "读取契约"),
            (
                "验证资料",
                "实测证据、手工测试计划与性能记录。",
                "validation/",
                "实测证据",
            ),
            (
                "项目信息",
                "更新记录、路线图、贡献指南与隐私说明。",
                "changelog/",
                "更新记录",
            ),
        ],
    },
    "en": {
        "title": "Revit Model MCP",
        "eyebrow": "Add-in / MCP version {version}",
        "lede": "Bring Autodesk Revit models to your AI assistant: inspect parameters and geometry, count "
        "elements, check models, export registers, edit elements, and copy models with new IDs. "
        "Read-only by default; actions need both gates.",
        "cta_install": "Install and connect",
        "cta_browse": "Browse {total} features",
        "stat_read": "Read tools",
        "stat_action": "Action tools",
        "stat_years": "Revit years",
        "stat_transport": "Transports",
        "stat_read_note": "Models and views",
        "stat_action_note": "Both gates required",
        "stat_years_note": "2020 and 2022–2027",
        "stat_transport_note": "Local · SSH · HTTP",
        "s1_num": "01",
        "s1_title": "Start by asking",
        "s1_lede": "Copy a prompt as it stands and swap in your own model, level, element IDs and file paths.",
        "s1_link": "Prompt library",
        "s1_band": "Writing is one sentence too, behind both gates",
        "s2_num": "02",
        "s2_title": "What it covers",
        "s2_lede": "Grouped into {groups} task areas, {total} tools in total. Every tool page carries its "
        "purpose, parameters, returned data and limits.",
        "s2_link": "Feature overview",
        "s3_num": "03",
        "s3_title": "See the output",
        "s3_lede": "This is a 3D view of the Revit sample project, exported straight by revit_export_view with no post-processing.",
        "s3_link": "Export a view",
        "s3_caption": "The PNG revit_export_view returned, shown in the theme the reader is using.",
        "s3_alt": "Three-storey office building exported from the Revit sample project by revit_export_view",
        "s4_num": "04",
        "s4_title": "How it works",
        "s4_lede": "The server runs on the MCP client's machine; the add-in runs inside Revit on Windows. "
        "They talk over a local channel, SSH or HTTP.",
        "s4_link": "How it works",
        "s5_num": "05",
        "s5_title": "Security boundaries",
        "s5_lede": "Read-only unless both gates are open. Close either one and the tool set returns to read-only.",
        "s5_link": "Action contracts",
        "s6_num": "06",
        "s6_title": "Get started in three steps",
        "s6_link": "Installation and configuration",
        "s7_num": "07",
        "s7_title": "Keep reading",
        "read": "Read",
        "action": "Action",
        "copy": "Copy",
        "step1": "Install the add-in on the Windows Revit workstation and configure the MCP server in your AI client.",
        "step2": "Start read-only: discover filter names from the model catalog, then count by category, family, type or level.",
        "step3": "Open both gates only when actions are needed; preview with dry_run first, and inspect the model after a timeout.",
        "flow": [
            ("AI client", "Calls MCP tools over stdio"),
            ("Python server", "Builds the command and picks local, SSH or HTTP"),
            ("Revit add-in", "Calls the Revit API inside ExternalEvent"),
            ("Model", "Returns JSON; writes commit in one transaction"),
        ],
        "gate1": "Set REVIT_MCP_ALLOW_WRITE=1 in the client",
        "gate2": "Create the allow-write gate file on the workstation",
        "safety_points": [
            ("Read-only by default", "Tools read model data, or export a view to PNG."),
            (
                "Both gates",
                "The environment variable and the gate file must both be present before actions register or run.",
            ),
            (
                "Dry run first",
                "Tools that support dry_run execute, roll back, and return the same verification block.",
            ),
            (
                "Check after a timeout",
                "A timeout or failed verification can follow a committed change; inspect the model before retrying.",
            ),
        ],
        "entries": [
            (
                "By Revit year",
                "Which features a year supports, and which were validated live.",
                "features/matrix/",
                "Support matrix",
            ),
            (
                "Cross-tool contracts",
                "Read contracts, action contracts and the file channel format.",
                "tools/",
                "Read contracts",
            ),
            (
                "Validation records",
                "Live evidence, the manual test plan and performance records.",
                "validation/",
                "Validation evidence",
            ),
            (
                "Project",
                "Changelog, roadmap, contributing guide and privacy.",
                "changelog/",
                "Changelog",
            ),
        ],
    },
}


def count_tools(tools: list[dict]) -> tuple[int, int]:
    read = sum(1 for tool in tools if tool["annotations"].get("readOnlyHint"))
    return read, len(tools) - read


def render_hero(
    text: dict, version: str, read: int, write: int, total: int, art: str
) -> str:
    return f"""<section class="rmc-hero">
  <div class="rmc-hero__grid" aria-hidden="true"></div>
  <div class="rmc-hero__inner">
    <div class="rmc-hero__copy">
      <p class="rmc-eyebrow"><span class="rmc-eyebrow__dot" aria-hidden="true"></span>{text["eyebrow"].format(version=version)}</p>
      <h1 class="rmc-hero__title">{text["title"]}</h1>
      <p class="rmc-hero__lede">{text["lede"]}</p>
      <p class="rmc-hero__actions">
        <a class="rmc-btn rmc-btn--primary" href="server/">{text["cta_install"]}</a>
        <a class="rmc-btn" href="features/">{text["cta_browse"].format(total=total)}</a>
      </p>
    </div>
    <div class="rmc-hero__art">{art}</div>
  </div>
  <dl class="rmc-spec">
    <div class="rmc-spec__cell">
      <dt>{text["stat_read"]}</dt>
      <dd>{read}</dd>
      <p>{text["stat_read_note"]}</p>
    </div>
    <div class="rmc-spec__cell">
      <dt>{text["stat_action"]}</dt>
      <dd>{write}</dd>
      <p>{text["stat_action_note"]}</p>
    </div>
    <div class="rmc-spec__cell">
      <dt>{text["stat_years"]}</dt>
      <dd class="rmc-spec__text">2020 · 2022–2027</dd>
      <p>{text["stat_years_note"]}</p>
    </div>
    <div class="rmc-spec__cell">
      <dt>{text["stat_transport"]}</dt>
      <dd class="rmc-spec__text">local · ssh · http</dd>
      <p>{text["stat_transport_note"]}</p>
    </div>
  </dl>
</section>"""


def _prompt_card(text: dict, capabilities: dict, name: str, kind: str) -> str:
    cap = capabilities["tools"][name]
    label = text["read"] if kind == "read" else text["action"]
    return f"""      <figure class="rmc-prompt rmc-prompt--{kind}" data-rmc-copy>
        <span class="rmc-prompt__kind">{label}</span>
        <span class="rmc-prompt__mark" aria-hidden="true">“</span>
        <blockquote class="rmc-prompt__text" data-rmc-copy-source>{cap["prompts"][0][text["lang"]]}</blockquote>
        <figcaption class="rmc-prompt__foot">
          <a href="features/{name}/"><code>{name}</code></a>
          <span class="rmc-prompt__go">{cap["summary"][text["lang"]]}</span>
        </figcaption>
      </figure>"""


def render_development(lang: str) -> str:
    """Describe the integration branch separately from the released tool catalog."""
    if lang == "zh":
        title = "新版底座与移植进展"
        intro = "当前网站的 35 个工具对应现有版本。新版正在独立分支上集成，尚未作为当前版本发布。"
        base = "上游底座包含文档管理、视图与图纸、族和链接、模型导出、批处理等能力；集成分支的工具清单目前有 80 项。"
        sample = "视图光照工具已完成 Python 工具注册和测试；C# 编译与 Revit 真机验证尚待完成。"
        pending = "楼板、标高、阶段设置与合并、元素 ID 导出、重置和模型重建仍待移植。Revit 2020 和 2026 均为目标工作站年份。"
        source = "查看集成规格与进展"
        catalog = "按基座与自研查阅 80 个工具"
    else:
        title = "New platform and migration progress"
        intro = "The 35 tools on this site describe the current release. The new platform is being integrated on a separate branch and is not yet released."
        base = "The upstream platform adds document management, views and sheets, families and links, export, and batch processing. The integration branch currently lists 80 tools."
        sample = "The view-lighting tool is registered and tested in Python; C# compilation and live Revit validation remain outstanding."
        pending = "Floor, level, phase setting and merging, element ID export and reset, and model rebuilding remain to be migrated. Revit 2020 and 2026 are both target workstation versions."
        source = "View the integration specification and progress"
        catalog = "Browse the 80 tools by origin"
    catalog_href = "platform/"
    return f'''<section class="rmc-section rmc-reveal" id="development-status">
  <header class="rmc-section__head">
    <span class="rmc-section__num" aria-hidden="true">↗</span>
    <h2 class="rmc-section__title">{title}</h2>
    <p class="rmc-section__lede">{intro}</p>
    <a class="rmc-section__link" href="{catalog_href}">{catalog}</a>
    <a class="rmc-section__link" href="https://github.com/vibe-bimer/revit-model-mcp/issues/27">{source}</a>
  </header>
  <ul class="rmc-development">
    <li>{base}</li>
    <li>{sample}</li>
    <li>{pending}</li>
  </ul>
</section>'''


def render_prompts(text: dict, capabilities: dict) -> str:
    """Read prompts tile in a grid; the action prompt gets a band of its own, because the read/write
    split is the single most important thing to understand about this server."""
    reads = [n for n, k in SHOWCASE if k == "read"]
    actions = [n for n, k in SHOWCASE if k == "action"]
    cards = "\n".join(_prompt_card(text, capabilities, n, "read") for n in reads)
    bands = "\n".join(_prompt_card(text, capabilities, n, "action") for n in actions)
    band = ""
    if actions:
        band = f"""
  <div class="rmc-band">
    <span class="rmc-band__label">{text["s1_band"]}</span>
{bands}
  </div>"""
    return f"""<section class="rmc-section rmc-reveal" id="common-prompts">
  <header class="rmc-section__head">
    <span class="rmc-section__num" aria-hidden="true">{text["s1_num"]}</span>
    <h2 class="rmc-section__title">{text["s1_title"]}</h2>
    <p class="rmc-section__lede">{text["s1_lede"]}</p>
    <a class="rmc-section__link" href="features/prompts/">{text["s1_link"]}</a>
  </header>
  <div class="rmc-prompts">
{cards}
  </div>{band}
</section>"""


def render_capabilities(
    text: dict, tools: list[dict], capabilities: dict, total: int
) -> str:
    groups = capabilities["groups"]
    cards = []
    for index, (key, names) in enumerate(groups.items()):
        members = [t for t in tools if capabilities["tools"][t["name"]]["group"] == key]
        # The first reviewed prompt of the first member reads as a concrete example of the group.
        example = capabilities["tools"][members[0]["name"]]["summary"][text["lang"]]
        cards.append(
            f"""      <a class="rmc-cap" href="features/#group-{key}">
        <span class="rmc-cap__num" aria-hidden="true">{index + 1:02d}</span>
        <span class="rmc-cap__body">
          <span class="rmc-cap__name">{names[text["lang"]]}</span>
          <span class="rmc-cap__desc">{example}</span>
        </span>
        <span class="rmc-cap__count">{len(members)}</span>
      </a>"""
        )
    return f"""<section class="rmc-section rmc-reveal" id="entry-points">
  <a id="tools"></a>
  <header class="rmc-section__head">
    <span class="rmc-section__num" aria-hidden="true">{text["s2_num"]}</span>
    <h2 class="rmc-section__title">{text["s2_title"]}</h2>
    <p class="rmc-section__lede">{text["s2_lede"].format(groups=len(groups), total=total)}</p>
    <a class="rmc-section__link" href="features/">{text["s2_link"]}</a>
  </header>
  <div class="rmc-caps">
{chr(10).join(cards)}
  </div>
</section>"""


def render_flow(text: dict) -> str:
    steps = []
    for index, (name, detail) in enumerate(text["flow"]):
        steps.append(
            f"""      <li class="rmc-flow__step">
        <span class="rmc-flow__num" aria-hidden="true">{index + 1}</span>
        <span class="rmc-flow__name">{name}</span>
        <span class="rmc-flow__detail">{detail}</span>
      </li>"""
        )
    return f"""<section class="rmc-section rmc-reveal" id="how-it-works">
  <header class="rmc-section__head">
    <span class="rmc-section__num" aria-hidden="true">{text["s4_num"]}</span>
    <h2 class="rmc-section__title">{text["s4_title"]}</h2>
    <p class="rmc-section__lede">{text["s4_lede"]}</p>
    <a class="rmc-section__link" href="how-it-works/">{text["s4_link"]}</a>
  </header>
  <ol class="rmc-flow">
{chr(10).join(steps)}
  </ol>
</section>"""


def render_output(text: dict) -> str:
    """Show what a tool actually returns: the image is the real output of revit_export_view on the
    Revit sample project, shipped once and selected per colour scheme by the browser."""
    return f"""<section class="rmc-section rmc-reveal" id="exported-view">
  <header class="rmc-section__head">
    <span class="rmc-section__num" aria-hidden="true">{text["s3_num"]}</span>
    <h2 class="rmc-section__title">{text["s3_title"]}</h2>
    <p class="rmc-section__lede">{text["s3_lede"]}</p>
    <a class="rmc-section__link" href="features/revit_export_view/">{text["s3_link"]}</a>
  </header>
  <figure class="rmc-shot">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="@@ROOT@@screenshots/revit-model-mcp_export-view_dark.png">
      <img src="@@ROOT@@screenshots/revit-model-mcp_export-view_light.png" alt="{text["s3_alt"]}" width="2100" height="806" loading="lazy" decoding="async">
    </picture>
    <figcaption>{text["s3_caption"]}</figcaption>
  </figure>
</section>"""


def render_safety(text: dict) -> str:
    points = "".join(
        f"""      <li class="rmc-safety__item">
        <span class="rmc-safety__name">{name}</span>
        <span class="rmc-safety__detail">{detail}</span>
      </li>"""
        for name, detail in text["safety_points"]
    )
    return f"""<section class="rmc-section rmc-reveal" id="actions-opt-in">
  <header class="rmc-section__head">
    <span class="rmc-section__num" aria-hidden="true">{text["s5_num"]}</span>
    <h2 class="rmc-section__title">{text["s5_title"]}</h2>
    <p class="rmc-section__lede">{text["s5_lede"]}</p>
    <a class="rmc-section__link" href="actions/#gates">{text["s5_link"]}</a>
  </header>
  <div class="rmc-gates">
    <span class="rmc-gates__gate"><span class="rmc-gates__mark" aria-hidden="true">1</span><code>REVIT_MCP_ALLOW_WRITE=1</code></span>
    <span class="rmc-gates__and" aria-hidden="true">+</span>
    <span class="rmc-gates__gate"><span class="rmc-gates__mark" aria-hidden="true">2</span><code>allow-write</code></span>
  </div>
  <ul class="rmc-safety">
{points}
  </ul>
</section>"""


def render_start(text: dict) -> str:
    return f"""<section class="rmc-section rmc-reveal" id="get-started">
  <header class="rmc-section__head">
    <span class="rmc-section__num" aria-hidden="true">{text["s6_num"]}</span>
    <h2 class="rmc-section__title">{text["s6_title"]}</h2>
    <a class="rmc-section__link" href="server/">{text["s6_link"]}</a>
  </header>
  <ol class="rmc-steps">
    <li class="rmc-steps__item"><span class="rmc-steps__num" aria-hidden="true">1</span><p>{text["step1"]}</p></li>
    <li class="rmc-steps__item"><span class="rmc-steps__num" aria-hidden="true">2</span><p>{text["step2"]}</p></li>
    <li class="rmc-steps__item"><span class="rmc-steps__num" aria-hidden="true">3</span><p>{text["step3"]}</p></li>
  </ol>
</section>"""


def render_entries(text: dict) -> str:
    cards = "".join(
        f"""      <a class="rmc-entry" href="{href}">
        <span class="rmc-entry__name">{name}</span>
        <span class="rmc-entry__desc">{desc}</span>
        <span class="rmc-entry__link">{link} →</span>
      </a>"""
        for name, desc, href, link in text["entries"]
    )
    return f"""<section class="rmc-section rmc-reveal" id="further-reading">
  <header class="rmc-section__head">
    <span class="rmc-section__num" aria-hidden="true">{text["s7_num"]}</span>
    <h2 class="rmc-section__title">{text["s7_title"]}</h2>
  </header>
  <div class="rmc-entries">
{cards}
  </div>
</section>"""


def home_page(tools: list[dict], capabilities: dict, version: str, lang: str) -> str:
    """Return the landing page for one language, ending with the literal text of its anchors."""
    text = dict(TEXT[lang], lang=lang)
    read, write = count_tools(tools)
    total = len(tools)
    art = (CONTENT / "hero.svg").read_text(encoding="utf-8").strip()
    body = "\n\n".join(
        [
            render_hero(text, version, read, write, total, art),
            render_development(lang),
            render_prompts(text, capabilities),
            render_capabilities(text, tools, capabilities, total),
            render_output(text),
            render_flow(text),
            render_safety(text),
            render_start(text),
            render_entries(text),
        ]
    )
    return f"""---
title: {text["title"]}
hide:
  - toc
---

<div class="rmc-landing">

{body}

</div>
"""
