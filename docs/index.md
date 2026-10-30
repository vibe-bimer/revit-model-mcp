---
title: Revit Model MCP
description: "把 Autodesk Revit 模型接到 AI 助手：查询参数与几何、统计构件、检查模型、导出清单并编辑构件，默认只读。"
hide:
  - toc
---

<div class="rmc-landing">

<section class="rmc-hero">
  <div class="rmc-hero__grid" aria-hidden="true"></div>
  <div class="rmc-hero__inner">
    <div class="rmc-hero__copy">
      <p class="rmc-eyebrow"><span class="rmc-eyebrow__dot" aria-hidden="true"></span>插件 / MCP 版本 0.9.0</p>
      <h1 class="rmc-hero__title">Revit Model MCP</h1>
      <p class="rmc-hero__lede">把 Autodesk Revit 模型接到 AI 助手上：查参数与几何、统计构件、检查模型、导出清单、编辑构件，以及复制模型并换新 ID。默认只读，动作需要双门禁。</p>
      <p class="rmc-hero__actions">
        <a class="rmc-btn rmc-btn--primary" href="server/">开始安装</a>
        <a class="rmc-btn" href="features/">浏览 35 个功能</a>
      </p>
    </div>
    <div class="rmc-hero__art"><svg class="rmc-frame" xmlns="http://www.w3.org/2000/svg" viewBox="8 52 620 400" role="img" aria-labelledby="rmc-frame-title">
  <title id="rmc-frame-title">Axonometric frame of a three-level structural model with dimension callouts</title>
  <g class="rmc-frame__site">
    <polygon class="rmc-frame__ground" points="214.0,208.0 404.5,318.0 214.0,428.0 23.5,318.0"/>
  </g>
  <g class="rmc-frame__cols">
    <line class="rmc-frame__col" style="--i:0" x1="214.0" y1="208.0" x2="214.0" y2="60.0"/>
    <line class="rmc-frame__col" style="--i:1" x1="118.7" y1="263.0" x2="118.7" y2="115.0"/>
    <line class="rmc-frame__col" style="--i:2" x1="23.5" y1="318.0" x2="23.5" y2="170.0"/>
    <line class="rmc-frame__col" style="--i:3" x1="309.3" y1="263.0" x2="309.3" y2="115.0"/>
    <line class="rmc-frame__col" style="--i:4" x1="214.0" y1="318.0" x2="214.0" y2="170.0"/>
    <line class="rmc-frame__col" style="--i:5" x1="118.7" y1="373.0" x2="118.7" y2="225.0"/>
    <line class="rmc-frame__col" style="--i:6" x1="404.5" y1="318.0" x2="404.5" y2="170.0"/>
    <line class="rmc-frame__col" style="--i:7" x1="309.3" y1="373.0" x2="309.3" y2="225.0"/>
    <line class="rmc-frame__col" style="--i:8" x1="214.0" y1="428.0" x2="214.0" y2="280.0"/>
  </g>
  <g class="rmc-frame__slab" style="--i:0">
    <polygon class="rmc-frame__deck" points="214.0,208.0 404.5,318.0 214.0,428.0 23.5,318.0"/>
    <polygon class="rmc-frame__edge" points="23.5,318.0 214.0,428.0 214.0,437.0 23.5,327.0"/>
    <polygon class="rmc-frame__edge" points="404.5,318.0 214.0,428.0 214.0,437.0 404.5,327.0"/>
  </g>
  <g class="rmc-frame__slab" style="--i:1">
    <polygon class="rmc-frame__deck" points="214.0,134.0 404.5,244.0 214.0,354.0 23.5,244.0"/>
    <polygon class="rmc-frame__edge" points="23.5,244.0 214.0,354.0 214.0,363.0 23.5,253.0"/>
    <polygon class="rmc-frame__edge" points="404.5,244.0 214.0,354.0 214.0,363.0 404.5,253.0"/>
  </g>
  <g class="rmc-frame__slab" style="--i:2">
    <polygon class="rmc-frame__deck" points="214.0,60.0 404.5,170.0 214.0,280.0 23.5,170.0"/>
    <polygon class="rmc-frame__edge" points="23.5,170.0 214.0,280.0 214.0,289.0 23.5,179.0"/>
    <polygon class="rmc-frame__edge" points="404.5,170.0 214.0,280.0 214.0,289.0 404.5,179.0"/>
  </g>
  <g class="rmc-frame__leader" style="--i:0">
    <path class="rmc-frame__line" d="M214.0,280.0 H456"/>
    <circle class="rmc-frame__dot" cx="214.0" cy="280.0" r="3.6"/>
  </g>
  <g class="rmc-frame__leader" style="--i:1">
    <path class="rmc-frame__line" d="M118.7,299.0 H456"/>
    <circle class="rmc-frame__dot" cx="118.7" cy="299.0" r="3.6"/>
  </g>
  <g class="rmc-frame__leader" style="--i:2">
    <path class="rmc-frame__line" d="M214.0,431.0 H456"/>
    <circle class="rmc-frame__dot" cx="214.0" cy="431.0" r="3.6"/>
  </g>
  <g class="rmc-frame__note" style="--i:0">
    <text class="rmc-frame__key" x="470" y="96">L03</text>
    <text class="rmc-frame__val" x="470" y="123">+7.200</text>
  </g>
  <g class="rmc-frame__note" style="--i:1">
    <text class="rmc-frame__key" x="470" y="214">COL</text>
    <text class="rmc-frame__val" x="470" y="241">GRID 3×3</text>
  </g>
  <g class="rmc-frame__note" style="--i:2">
    <text class="rmc-frame__key" x="470" y="352">AREA</text>
    <text class="rmc-frame__val" x="470" y="379">268.4 m²</text>
  </g>
</svg></div>
  </div>
  <dl class="rmc-spec">
    <div class="rmc-spec__cell">
      <dt>读取工具</dt>
      <dd>19</dd>
      <p>只读模型与视图</p>
    </div>
    <div class="rmc-spec__cell">
      <dt>动作工具</dt>
      <dd>16</dd>
      <p>需双门禁授权</p>
    </div>
    <div class="rmc-spec__cell">
      <dt>Revit 年份</dt>
      <dd class="rmc-spec__text">2020 · 2022–2027</dd>
      <p>2020 与 2022–2027</p>
    </div>
    <div class="rmc-spec__cell">
      <dt>传输方式</dt>
      <dd class="rmc-spec__text">local · ssh · http</dd>
      <p>本机 · SSH · HTTP</p>
    </div>
  </dl>
</section>

<section class="rmc-section rmc-reveal" id="development-status">
  <header class="rmc-section__head">
    <span class="rmc-section__num" aria-hidden="true">↗</span>
    <h2 class="rmc-section__title">新版底座与移植进展</h2>
    <p class="rmc-section__lede">当前网站的 35 个工具对应现有版本。新版正在独立分支上集成，尚未作为当前版本发布。</p>
    <a class="rmc-section__link" href="platform/">按基座与自研查阅 80 个工具</a>
    <a class="rmc-section__link" href="https://github.com/vibe-bimer/revit-model-mcp/issues/27">查看集成规格与进展</a>
  </header>
  <ul class="rmc-development">
    <li>上游底座包含文档管理、视图与图纸、族和链接、模型导出、批处理等能力；集成分支的工具清单目前有 80 项。</li>
    <li>视图光照工具已完成 Python 工具注册和测试；C# 编译与 Revit 真机验证尚待完成。</li>
    <li>楼板、标高、阶段设置与合并、构件 ID 导出、重置和模型重建仍待移植。Revit 2020 和 2026 均为目标工作站年份。</li>
  </ul>
</section>

<section class="rmc-section rmc-reveal" id="common-prompts">
  <header class="rmc-section__head">
    <span class="rmc-section__num" aria-hidden="true">01</span>
    <h2 class="rmc-section__title">先问一句</h2>
    <p class="rmc-section__lede">提示词原样复制即可使用，替换模型、标高、构件 ID 和文件路径换成你自己的。</p>
    <a class="rmc-section__link" href="features/prompts/">提示词库</a>
  </header>
  <div class="rmc-prompts">
      <figure class="rmc-prompt rmc-prompt--read" data-rmc-copy>
        <span class="rmc-prompt__kind">读取</span>
        <span class="rmc-prompt__mark" aria-hidden="true">“</span>
        <blockquote class="rmc-prompt__text" data-rmc-copy-source>统计 1F 上各种墙类型各有多少个</blockquote>
        <figcaption class="rmc-prompt__foot">
          <a href="features/revit_aggregate_elements/"><code>revit_aggregate_elements</code></a>
          <span class="rmc-prompt__go">按 1–2 个字段分组统计数量，可附加求和与平均（mm / m² / m³）</span>
        </figcaption>
      </figure>
      <figure class="rmc-prompt rmc-prompt--read" data-rmc-copy>
        <span class="rmc-prompt__kind">读取</span>
        <span class="rmc-prompt__mark" aria-hidden="true">“</span>
        <blockquote class="rmc-prompt__text" data-rmc-copy-source>做一次交付前体检：文件大小、各类数量、单位设置、最多的警告</blockquote>
        <figcaption class="rmc-prompt__foot">
          <a href="features/revit_model_health/"><code>revit_model_health</code></a>
          <span class="rmc-prompt__go">交付前体检：文件大小、各类计数、单位设置、数量最多的警告</span>
        </figcaption>
      </figure>
      <figure class="rmc-prompt rmc-prompt--read" data-rmc-copy>
        <span class="rmc-prompt__kind">读取</span>
        <span class="rmc-prompt__mark" aria-hidden="true">“</span>
        <blockquote class="rmc-prompt__text" data-rmc-copy-source>列出 2F 上所有没填防火等级的门，给出 ID</blockquote>
        <figcaption class="rmc-prompt__foot">
          <a href="features/revit_query_elements/"><code>revit_query_elements</code></a>
          <span class="rmc-prompt__go">按类别/族/类型/标高/视图/工作集/参数过滤，分页读取构件明细</span>
        </figcaption>
      </figure>
      <figure class="rmc-prompt rmc-prompt--read" data-rmc-copy>
        <span class="rmc-prompt__kind">读取</span>
        <span class="rmc-prompt__mark" aria-hidden="true">“</span>
        <blockquote class="rmc-prompt__text" data-rmc-copy-source>把模型中已绘制构件的 ID 清单导出成 Excel，按类别、族、类型排序</blockquote>
        <figcaption class="rmc-prompt__foot">
          <a href="features/revit_export_element_ids/"><code>revit_export_element_ids</code></a>
          <span class="rmc-prompt__go">把模型中已绘制构件的 ID 清单写成 Excel（类别/族/类型/标高/构件ID/名称/工作集）</span>
        </figcaption>
      </figure>
  </div>
  <div class="rmc-band">
    <span class="rmc-band__label">写入时同样是一句话，但需要双门禁</span>
      <figure class="rmc-prompt rmc-prompt--action" data-rmc-copy>
        <span class="rmc-prompt__kind">动作</span>
        <span class="rmc-prompt__mark" aria-hidden="true">“</span>
        <blockquote class="rmc-prompt__text" data-rmc-copy-source>把这 3 个构件沿 X 移动 500 mm，先彩排</blockquote>
        <figcaption class="rmc-prompt__foot">
          <a href="features/revit_move/"><code>revit_move</code></a>
          <span class="rmc-prompt__go">按模型轴平移构件（mm）</span>
        </figcaption>
      </figure>
  </div>
</section>

<section class="rmc-section rmc-reveal" id="entry-points">
  <a id="tools"></a>
  <header class="rmc-section__head">
    <span class="rmc-section__num" aria-hidden="true">02</span>
    <h2 class="rmc-section__title">能力范围</h2>
    <p class="rmc-section__lede">按场景分成 8 组，共 35 个工具。每个工具页都有用途、参数、返回结果与限制。</p>
    <a class="rmc-section__link" href="features/">功能总览</a>
  </header>
  <div class="rmc-caps">
      <a class="rmc-cap" href="features/#group-connection">
        <span class="rmc-cap__num" aria-hidden="true">01</span>
        <span class="rmc-cap__body">
          <span class="rmc-cap__name">连接与文档</span>
          <span class="rmc-cap__desc">检查连接与插件版本</span>
        </span>
        <span class="rmc-cap__count">3</span>
      </a>
      <a class="rmc-cap" href="features/#group-query">
        <span class="rmc-cap__num" aria-hidden="true">02</span>
        <span class="rmc-cap__body">
          <span class="rmc-cap__name">查询与统计</span>
          <span class="rmc-cap__desc">查可用名字：类别、族类型、标高、面积方案、视图、工作集、阶段、参数</span>
        </span>
        <span class="rmc-cap__count">5</span>
      </a>
      <a class="rmc-cap" href="features/#group-views">
        <span class="rmc-cap__num" aria-hidden="true">03</span>
        <span class="rmc-cap__body">
          <span class="rmc-cap__name">视图与截图</span>
          <span class="rmc-cap__desc">列出视图，可按视图类型与名称过滤</span>
        </span>
        <span class="rmc-cap__count">6</span>
      </a>
      <a class="rmc-cap" href="features/#group-export">
        <span class="rmc-cap__num" aria-hidden="true">04</span>
        <span class="rmc-cap__body">
          <span class="rmc-cap__name">导出与检验</span>
          <span class="rmc-cap__desc">交付前体检：文件大小、各类计数、单位设置、数量最多的警告</span>
        </span>
        <span class="rmc-cap__count">6</span>
      </a>
      <a class="rmc-cap" href="features/#group-display">
        <span class="rmc-cap__num" aria-hidden="true">05</span>
        <span class="rmc-cap__body">
          <span class="rmc-cap__name">选中与显示</span>
          <span class="rmc-cap__desc">在 Revit 里选中指定构件（空列表=清除选择）</span>
        </span>
        <span class="rmc-cap__count">3</span>
      </a>
      <a class="rmc-cap" href="features/#group-edit">
        <span class="rmc-cap__num" aria-hidden="true">06</span>
        <span class="rmc-cap__body">
          <span class="rmc-cap__name">编辑</span>
          <span class="rmc-cap__desc">按模型轴平移构件（mm）</span>
        </span>
        <span class="rmc-cap__count">7</span>
      </a>
      <a class="rmc-cap" href="features/#group-phases">
        <span class="rmc-cap__num" aria-hidden="true">07</span>
        <span class="rmc-cap__body">
          <span class="rmc-cap__name">阶段</span>
          <span class="rmc-cap__desc">赋创建阶段 / 拆除阶段（空串清除，null 不变）</span>
        </span>
        <span class="rmc-cap__count">2</span>
      </a>
      <a class="rmc-cap" href="features/#group-ids">
        <span class="rmc-cap__num" aria-hidden="true">08</span>
        <span class="rmc-cap__body">
          <span class="rmc-cap__name">批量与 ID</span>
          <span class="rmc-cap__desc">同文档内换 ID：只对无宿主、无依赖的独立构件有效</span>
        </span>
        <span class="rmc-cap__count">3</span>
      </a>
  </div>
</section>

<section class="rmc-section rmc-reveal" id="exported-view">
  <header class="rmc-section__head">
    <span class="rmc-section__num" aria-hidden="true">03</span>
    <h2 class="rmc-section__title">看见结果</h2>
    <p class="rmc-section__lede">下面这张图是 Revit 示例项目的三维视图，由 revit_export_view 直接导出，没有做过任何后处理。</p>
    <a class="rmc-section__link" href="features/revit_export_view/">导出视图图片</a>
  </header>
  <figure class="rmc-shot">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="@@ROOT@@screenshots/revit-model-mcp_export-view_dark.png">
      <img src="@@ROOT@@screenshots/revit-model-mcp_export-view_light.png" alt="由 revit_export_view 从 Revit 示例项目导出的三层办公楼三维视图" width="2100" height="806" loading="lazy" decoding="async">
    </picture>
    <figcaption>revit_export_view 导出的视图 PNG，跟随当前深浅色主题切换。</figcaption>
  </figure>
</section>

<section class="rmc-section rmc-reveal" id="how-it-works">
  <header class="rmc-section__head">
    <span class="rmc-section__num" aria-hidden="true">04</span>
    <h2 class="rmc-section__title">工作原理</h2>
    <p class="rmc-section__lede">服务器在 MCP 客户端所在机器上，插件在 Windows 的 Revit 进程内；两者通过本机通道、SSH 或 HTTP 通信。</p>
    <a class="rmc-section__link" href="how-it-works/">工作原理</a>
  </header>
  <ol class="rmc-flow">
      <li class="rmc-flow__step">
        <span class="rmc-flow__num" aria-hidden="true">1</span>
        <span class="rmc-flow__name">AI 客户端</span>
        <span class="rmc-flow__detail">通过 stdio 调用 MCP 工具</span>
      </li>
      <li class="rmc-flow__step">
        <span class="rmc-flow__num" aria-hidden="true">2</span>
        <span class="rmc-flow__name">Python 服务器</span>
        <span class="rmc-flow__detail">构造命令，选择本机通道、SSH 或 HTTP</span>
      </li>
      <li class="rmc-flow__step">
        <span class="rmc-flow__num" aria-hidden="true">3</span>
        <span class="rmc-flow__name">Revit 插件</span>
        <span class="rmc-flow__detail">在 ExternalEvent 中调用 Revit API</span>
      </li>
      <li class="rmc-flow__step">
        <span class="rmc-flow__num" aria-hidden="true">4</span>
        <span class="rmc-flow__name">模型</span>
        <span class="rmc-flow__detail">返回 JSON；写操作在同一事务内完成</span>
      </li>
  </ol>
</section>

<section class="rmc-section rmc-reveal" id="actions-opt-in">
  <header class="rmc-section__head">
    <span class="rmc-section__num" aria-hidden="true">05</span>
    <h2 class="rmc-section__title">安全边界</h2>
    <p class="rmc-section__lede">默认只读。写入需要同时打开两道门禁，任一道关闭即回到只读。</p>
    <a class="rmc-section__link" href="actions/#gates">动作契约</a>
  </header>
  <div class="rmc-gates">
    <span class="rmc-gates__gate"><span class="rmc-gates__mark" aria-hidden="true">1</span><code>REVIT_MCP_ALLOW_WRITE=1</code></span>
    <span class="rmc-gates__and" aria-hidden="true">+</span>
    <span class="rmc-gates__gate"><span class="rmc-gates__mark" aria-hidden="true">2</span><code>allow-write</code></span>
  </div>
  <ul class="rmc-safety">
      <li class="rmc-safety__item">
        <span class="rmc-safety__name">默认只读</span>
        <span class="rmc-safety__detail">工具默认只读取模型数据，或将视图导出为 PNG。</span>
      </li>      <li class="rmc-safety__item">
        <span class="rmc-safety__name">双门禁</span>
        <span class="rmc-safety__detail">环境变量与门禁文件必须同时存在，动作工具才会注册与执行。</span>
      </li>      <li class="rmc-safety__item">
        <span class="rmc-safety__name">先彩排</span>
        <span class="rmc-safety__detail">支持 dry_run 的工具会执行后回滚，返回同样的校验结果。</span>
      </li>      <li class="rmc-safety__item">
        <span class="rmc-safety__name">超时须核对</span>
        <span class="rmc-safety__detail">超时或校验失败之后，改动可能已经提交；先核对模型再重试。</span>
      </li>
  </ul>
</section>

<section class="rmc-section rmc-reveal" id="get-started">
  <header class="rmc-section__head">
    <span class="rmc-section__num" aria-hidden="true">06</span>
    <h2 class="rmc-section__title">三步上手</h2>
    <a class="rmc-section__link" href="server/">安装与配置</a>
  </header>
  <ol class="rmc-steps">
    <li class="rmc-steps__item"><span class="rmc-steps__num" aria-hidden="true">1</span><p>在 Windows Revit 工作站安装插件，在 AI 客户端配置 MCP 服务器。</p></li>
    <li class="rmc-steps__item"><span class="rmc-steps__num" aria-hidden="true">2</span><p>先做只读查询：过滤用的名称先从模型目录获取，再按类别、族、类型或标高统计。</p></li>
    <li class="rmc-steps__item"><span class="rmc-steps__num" aria-hidden="true">3</span><p>需要动作时再打开双门禁；修改前先用支持该参数的工具做 dry_run，超时后先核对模型。</p></li>
  </ol>
</section>

<section class="rmc-section rmc-reveal" id="further-reading">
  <header class="rmc-section__head">
    <span class="rmc-section__num" aria-hidden="true">07</span>
    <h2 class="rmc-section__title">继续查阅</h2>
  </header>
  <div class="rmc-entries">
      <a class="rmc-entry" href="features/matrix/">
        <span class="rmc-entry__name">按 Revit 年份</span>
        <span class="rmc-entry__desc">确认某一年份支持哪些功能，以及哪些已实测。</span>
        <span class="rmc-entry__link">支持矩阵 →</span>
      </a>      <a class="rmc-entry" href="tools/">
        <span class="rmc-entry__name">跨工具契约</span>
        <span class="rmc-entry__desc">读取契约、动作契约与文件通道格式。</span>
        <span class="rmc-entry__link">读取契约 →</span>
      </a>      <a class="rmc-entry" href="validation/">
        <span class="rmc-entry__name">验证资料</span>
        <span class="rmc-entry__desc">实测证据、手工测试计划与性能记录。</span>
        <span class="rmc-entry__link">实测证据 →</span>
      </a>      <a class="rmc-entry" href="changelog/">
        <span class="rmc-entry__name">项目信息</span>
        <span class="rmc-entry__desc">更新记录、路线图、贡献指南与隐私说明。</span>
        <span class="rmc-entry__link">更新记录 →</span>
      </a>
  </div>
</section>

</div>
