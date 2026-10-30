---
title: Revit Model MCP
hide:
  - toc
---

<div class="rmc-landing">

<section class="rmc-hero">
  <div class="rmc-hero__grid" aria-hidden="true"></div>
  <div class="rmc-hero__inner">
    <div class="rmc-hero__copy">
      <p class="rmc-eyebrow"><span class="rmc-eyebrow__dot" aria-hidden="true"></span>Add-in / MCP version 0.9.0</p>
      <h1 class="rmc-hero__title">Revit Model MCP</h1>
      <p class="rmc-hero__lede">Bring Autodesk Revit models to your AI assistant: inspect parameters and geometry, count elements, check models, export registers, edit elements, and copy models with new IDs. Read-only by default; actions need both gates.</p>
      <p class="rmc-hero__actions">
        <a class="rmc-btn rmc-btn--primary" href="server/">Install and connect</a>
        <a class="rmc-btn" href="features/">Browse 35 features</a>
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
      <dt>Read tools</dt>
      <dd>19</dd>
      <p>Models and views</p>
    </div>
    <div class="rmc-spec__cell">
      <dt>Action tools</dt>
      <dd>16</dd>
      <p>Both gates required</p>
    </div>
    <div class="rmc-spec__cell">
      <dt>Revit years</dt>
      <dd class="rmc-spec__text">2020 · 2022–2027</dd>
      <p>2020 and 2022–2027</p>
    </div>
    <div class="rmc-spec__cell">
      <dt>Transports</dt>
      <dd class="rmc-spec__text">local · ssh · http</dd>
      <p>Local · SSH · HTTP</p>
    </div>
  </dl>
</section>

<section class="rmc-section rmc-reveal" id="development-status">
  <header class="rmc-section__head">
    <span class="rmc-section__num" aria-hidden="true">↗</span>
    <h2 class="rmc-section__title">New platform and migration progress</h2>
    <p class="rmc-section__lede">The 35 tools on this site describe the current release. The new platform is being integrated on a separate branch and is not yet released.</p>
    <a class="rmc-section__link" href="platform/">Browse the 80 tools by origin</a>
    <a class="rmc-section__link" href="https://github.com/vibe-bimer/revit-model-mcp/issues/27">View the integration specification and progress</a>
  </header>
  <ul class="rmc-development">
    <li>The upstream platform adds document management, views and sheets, families and links, export, and batch processing. The integration branch currently lists 80 tools.</li>
    <li>The view-lighting tool is registered and tested in Python; C# compilation and live Revit validation remain outstanding.</li>
    <li>Floor, level, phase setting and merging, element ID export and reset, and model rebuilding remain to be migrated. Revit 2020 and 2026 are both target workstation versions.</li>
  </ul>
</section>

<section class="rmc-section rmc-reveal" id="common-prompts">
  <header class="rmc-section__head">
    <span class="rmc-section__num" aria-hidden="true">01</span>
    <h2 class="rmc-section__title">Start by asking</h2>
    <p class="rmc-section__lede">Copy a prompt as it stands and swap in your own model, level, element IDs and file paths.</p>
    <a class="rmc-section__link" href="features/prompts/">Prompt library</a>
  </header>
  <div class="rmc-prompts">
      <figure class="rmc-prompt rmc-prompt--read" data-rmc-copy>
        <span class="rmc-prompt__kind">Read</span>
        <span class="rmc-prompt__mark" aria-hidden="true">“</span>
        <blockquote class="rmc-prompt__text" data-rmc-copy-source>How many of each wall type sit on 1F?</blockquote>
        <figcaption class="rmc-prompt__foot">
          <a href="features/revit_aggregate_elements/"><code>revit_aggregate_elements</code></a>
          <span class="rmc-prompt__go">Group by one or two fields, with counts and optional sum and average</span>
        </figcaption>
      </figure>
      <figure class="rmc-prompt rmc-prompt--read" data-rmc-copy>
        <span class="rmc-prompt__kind">Read</span>
        <span class="rmc-prompt__mark" aria-hidden="true">“</span>
        <blockquote class="rmc-prompt__text" data-rmc-copy-source>Run a pre-handover health check: size, counts, units, top warnings</blockquote>
        <figcaption class="rmc-prompt__foot">
          <a href="features/revit_model_health/"><code>revit_model_health</code></a>
          <span class="rmc-prompt__go">Check file size, model counts, units and frequent warnings</span>
        </figcaption>
      </figure>
      <figure class="rmc-prompt rmc-prompt--read" data-rmc-copy>
        <span class="rmc-prompt__kind">Read</span>
        <span class="rmc-prompt__mark" aria-hidden="true">“</span>
        <blockquote class="rmc-prompt__text" data-rmc-copy-source>List the doors on 2F whose fire rating is empty, with ids</blockquote>
        <figcaption class="rmc-prompt__foot">
          <a href="features/revit_query_elements/"><code>revit_query_elements</code></a>
          <span class="rmc-prompt__go">Filter and page through individual element rows</span>
        </figcaption>
      </figure>
      <figure class="rmc-prompt rmc-prompt--read" data-rmc-copy>
        <span class="rmc-prompt__kind">Read</span>
        <span class="rmc-prompt__mark" aria-hidden="true">“</span>
        <blockquote class="rmc-prompt__text" data-rmc-copy-source>Export the ID register of drawn model components to Excel, ordered by category, family and type</blockquote>
        <figcaption class="rmc-prompt__foot">
          <a href="features/revit_export_element_ids/"><code>revit_export_element_ids</code></a>
          <span class="rmc-prompt__go">Write the ID register of drawn model components to an Excel workbook</span>
        </figcaption>
      </figure>
  </div>
  <div class="rmc-band">
    <span class="rmc-band__label">Writing is one sentence too, behind both gates</span>
      <figure class="rmc-prompt rmc-prompt--action" data-rmc-copy>
        <span class="rmc-prompt__kind">Action</span>
        <span class="rmc-prompt__mark" aria-hidden="true">“</span>
        <blockquote class="rmc-prompt__text" data-rmc-copy-source>Move these three elements 500 mm along X, dry run first</blockquote>
        <figcaption class="rmc-prompt__foot">
          <a href="features/revit_move/"><code>revit_move</code></a>
          <span class="rmc-prompt__go">Move elements by offsets along model axes in millimetres</span>
        </figcaption>
      </figure>
  </div>
</section>

<section class="rmc-section rmc-reveal" id="entry-points">
  <a id="tools"></a>
  <header class="rmc-section__head">
    <span class="rmc-section__num" aria-hidden="true">02</span>
    <h2 class="rmc-section__title">What it covers</h2>
    <p class="rmc-section__lede">Grouped into 8 task areas, 35 tools in total. Every tool page carries its purpose, parameters, returned data and limits.</p>
    <a class="rmc-section__link" href="features/">Feature overview</a>
  </header>
  <div class="rmc-caps">
      <a class="rmc-cap" href="features/#group-connection">
        <span class="rmc-cap__num" aria-hidden="true">01</span>
        <span class="rmc-cap__body">
          <span class="rmc-cap__name">Connection and documents</span>
          <span class="rmc-cap__desc">Check whether the Revit add-in is reachable</span>
        </span>
        <span class="rmc-cap__count">3</span>
      </a>
      <a class="rmc-cap" href="features/#group-query">
        <span class="rmc-cap__num" aria-hidden="true">02</span>
        <span class="rmc-cap__body">
          <span class="rmc-cap__name">Query and totals</span>
          <span class="rmc-cap__desc">Discover categories, family types, levels, area schemes, views, worksets, phases and parameters</span>
        </span>
        <span class="rmc-cap__count">5</span>
      </a>
      <a class="rmc-cap" href="features/#group-views">
        <span class="rmc-cap__num" aria-hidden="true">03</span>
        <span class="rmc-cap__body">
          <span class="rmc-cap__name">Views and snapshots</span>
          <span class="rmc-cap__desc">List views filtered by type and name</span>
        </span>
        <span class="rmc-cap__count">6</span>
      </a>
      <a class="rmc-cap" href="features/#group-export">
        <span class="rmc-cap__num" aria-hidden="true">04</span>
        <span class="rmc-cap__body">
          <span class="rmc-cap__name">Export and checks</span>
          <span class="rmc-cap__desc">Check file size, model counts, units and frequent warnings</span>
        </span>
        <span class="rmc-cap__count">6</span>
      </a>
      <a class="rmc-cap" href="features/#group-display">
        <span class="rmc-cap__num" aria-hidden="true">05</span>
        <span class="rmc-cap__body">
          <span class="rmc-cap__name">Selection and display</span>
          <span class="rmc-cap__desc">Select elements in Revit; an empty list clears the selection</span>
        </span>
        <span class="rmc-cap__count">3</span>
      </a>
      <a class="rmc-cap" href="features/#group-edit">
        <span class="rmc-cap__num" aria-hidden="true">06</span>
        <span class="rmc-cap__body">
          <span class="rmc-cap__name">Editing</span>
          <span class="rmc-cap__desc">Move elements by offsets along model axes in millimetres</span>
        </span>
        <span class="rmc-cap__count">7</span>
      </a>
      <a class="rmc-cap" href="features/#group-phases">
        <span class="rmc-cap__num" aria-hidden="true">07</span>
        <span class="rmc-cap__body">
          <span class="rmc-cap__name">Phases</span>
          <span class="rmc-cap__desc">Assign created/demolished phases; an empty string clears and null leaves unchanged</span>
        </span>
        <span class="rmc-cap__count">2</span>
      </a>
      <a class="rmc-cap" href="features/#group-ids">
        <span class="rmc-cap__num" aria-hidden="true">08</span>
        <span class="rmc-cap__body">
          <span class="rmc-cap__name">Batch and ids</span>
          <span class="rmc-cap__desc">Replace eligible standalone elements with copies to obtain new IDs</span>
        </span>
        <span class="rmc-cap__count">3</span>
      </a>
  </div>
</section>

<section class="rmc-section rmc-reveal" id="exported-view">
  <header class="rmc-section__head">
    <span class="rmc-section__num" aria-hidden="true">03</span>
    <h2 class="rmc-section__title">See the output</h2>
    <p class="rmc-section__lede">This is a 3D view of the Revit sample project, exported straight by revit_export_view with no post-processing.</p>
    <a class="rmc-section__link" href="features/revit_export_view/">Export a view</a>
  </header>
  <figure class="rmc-shot">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="@@ROOT@@screenshots/revit-model-mcp_export-view_dark.png">
      <img src="@@ROOT@@screenshots/revit-model-mcp_export-view_light.png" alt="Three-storey office building exported from the Revit sample project by revit_export_view" width="2100" height="806" loading="lazy" decoding="async">
    </picture>
    <figcaption>The PNG revit_export_view returned, shown in the theme the reader is using.</figcaption>
  </figure>
</section>

<section class="rmc-section rmc-reveal" id="how-it-works">
  <header class="rmc-section__head">
    <span class="rmc-section__num" aria-hidden="true">04</span>
    <h2 class="rmc-section__title">How it works</h2>
    <p class="rmc-section__lede">The server runs on the MCP client's machine; the add-in runs inside Revit on Windows. They talk over a local channel, SSH or HTTP.</p>
    <a class="rmc-section__link" href="how-it-works/">How it works</a>
  </header>
  <ol class="rmc-flow">
      <li class="rmc-flow__step">
        <span class="rmc-flow__num" aria-hidden="true">1</span>
        <span class="rmc-flow__name">AI client</span>
        <span class="rmc-flow__detail">Calls MCP tools over stdio</span>
      </li>
      <li class="rmc-flow__step">
        <span class="rmc-flow__num" aria-hidden="true">2</span>
        <span class="rmc-flow__name">Python server</span>
        <span class="rmc-flow__detail">Builds the command and picks local, SSH or HTTP</span>
      </li>
      <li class="rmc-flow__step">
        <span class="rmc-flow__num" aria-hidden="true">3</span>
        <span class="rmc-flow__name">Revit add-in</span>
        <span class="rmc-flow__detail">Calls the Revit API inside ExternalEvent</span>
      </li>
      <li class="rmc-flow__step">
        <span class="rmc-flow__num" aria-hidden="true">4</span>
        <span class="rmc-flow__name">Model</span>
        <span class="rmc-flow__detail">Returns JSON; writes commit in one transaction</span>
      </li>
  </ol>
</section>

<section class="rmc-section rmc-reveal" id="actions-opt-in">
  <header class="rmc-section__head">
    <span class="rmc-section__num" aria-hidden="true">05</span>
    <h2 class="rmc-section__title">Security boundaries</h2>
    <p class="rmc-section__lede">Read-only unless both gates are open. Close either one and the tool set returns to read-only.</p>
    <a class="rmc-section__link" href="actions/#gates">Action contracts</a>
  </header>
  <div class="rmc-gates">
    <span class="rmc-gates__gate"><span class="rmc-gates__mark" aria-hidden="true">1</span><code>REVIT_MCP_ALLOW_WRITE=1</code></span>
    <span class="rmc-gates__and" aria-hidden="true">+</span>
    <span class="rmc-gates__gate"><span class="rmc-gates__mark" aria-hidden="true">2</span><code>allow-write</code></span>
  </div>
  <ul class="rmc-safety">
      <li class="rmc-safety__item">
        <span class="rmc-safety__name">Read-only by default</span>
        <span class="rmc-safety__detail">Tools read model data, or export a view to PNG.</span>
      </li>      <li class="rmc-safety__item">
        <span class="rmc-safety__name">Both gates</span>
        <span class="rmc-safety__detail">The environment variable and the gate file must both be present before actions register or run.</span>
      </li>      <li class="rmc-safety__item">
        <span class="rmc-safety__name">Dry run first</span>
        <span class="rmc-safety__detail">Tools that support dry_run execute, roll back, and return the same verification block.</span>
      </li>      <li class="rmc-safety__item">
        <span class="rmc-safety__name">Check after a timeout</span>
        <span class="rmc-safety__detail">A timeout or failed verification can follow a committed change; inspect the model before retrying.</span>
      </li>
  </ul>
</section>

<section class="rmc-section rmc-reveal" id="get-started">
  <header class="rmc-section__head">
    <span class="rmc-section__num" aria-hidden="true">06</span>
    <h2 class="rmc-section__title">Get started in three steps</h2>
    <a class="rmc-section__link" href="server/">Installation and configuration</a>
  </header>
  <ol class="rmc-steps">
    <li class="rmc-steps__item"><span class="rmc-steps__num" aria-hidden="true">1</span><p>Install the add-in on the Windows Revit workstation and configure the MCP server in your AI client.</p></li>
    <li class="rmc-steps__item"><span class="rmc-steps__num" aria-hidden="true">2</span><p>Start read-only: discover filter names from the model catalog, then count by category, family, type or level.</p></li>
    <li class="rmc-steps__item"><span class="rmc-steps__num" aria-hidden="true">3</span><p>Open both gates only when actions are needed; preview with dry_run first, and inspect the model after a timeout.</p></li>
  </ol>
</section>

<section class="rmc-section rmc-reveal" id="further-reading">
  <header class="rmc-section__head">
    <span class="rmc-section__num" aria-hidden="true">07</span>
    <h2 class="rmc-section__title">Keep reading</h2>
  </header>
  <div class="rmc-entries">
      <a class="rmc-entry" href="features/matrix/">
        <span class="rmc-entry__name">By Revit year</span>
        <span class="rmc-entry__desc">Which features a year supports, and which were validated live.</span>
        <span class="rmc-entry__link">Support matrix →</span>
      </a>      <a class="rmc-entry" href="tools/">
        <span class="rmc-entry__name">Cross-tool contracts</span>
        <span class="rmc-entry__desc">Read contracts, action contracts and the file channel format.</span>
        <span class="rmc-entry__link">Read contracts →</span>
      </a>      <a class="rmc-entry" href="validation/">
        <span class="rmc-entry__name">Validation records</span>
        <span class="rmc-entry__desc">Live evidence, the manual test plan and performance records.</span>
        <span class="rmc-entry__link">Validation evidence →</span>
      </a>      <a class="rmc-entry" href="changelog/">
        <span class="rmc-entry__name">Project</span>
        <span class="rmc-entry__desc">Changelog, roadmap, contributing guide and privacy.</span>
        <span class="rmc-entry__link">Changelog →</span>
      </a>
  </div>
</section>

</div>
