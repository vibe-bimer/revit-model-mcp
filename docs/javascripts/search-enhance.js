/* Version-aware search results for the two catalogs.
 *
 * The search plugin builds one index for the whole site, so a result cannot say which language it
 * is written in, which catalog it belongs to, or which of two same-name tools it is. This script
 * re-renders the modal's result list from that same index, filtered to the page's language by
 * default, with an explicit all-languages switch, status badges and a no-result guide. An exact
 * tool-name query puts the applicable tool pages first, release before integration branch.
 *
 * Progressive enhancement: without this script the modal still shows the plugin's own results.
 */
(function () {
  "use strict";

  var TEXT = {
    zh: {
      allLanguages: "所有语言",
      onlyThis: "仅简体中文",
      results: "条结果",
      noResult: "当前语言没有匹配结果。",
      noResultAll: "换用所有语言再搜一次",
      noResultCatalog: "去目录里找",
      release: "已发布",
      branch: "未发布",
      branchNote: "集成分支",
      language: "英文",
      loading: "正在搜索…",
    },
    en: {
      allLanguages: "All languages",
      onlyThis: "English only",
      results: "results",
      noResult: "No match in this language.",
      noResultAll: "Search all languages",
      noResultCatalog: "Browse the catalog",
      release: "Released",
      branch: "Unreleased",
      branchNote: "integration branch",
      language: "Chinese",
      loading: "Searching…",
    },
  };

  var TOOL_NAME = /^revit_[a-z0-9_]+$/;
  var ALL_KEY = "rmm-search-all-languages";

  var config = readConfig();
  var lang = document.documentElement.lang === "en" ? "en" : "zh";
  var labels = TEXT[lang];
  var base = config.base || "/";
  var catalog = window.__RMM_CATALOG__ || { release: {}, branch: {} };
  var pages = null;
  var pending = null;

  function readConfig() {
    var node = document.getElementById("__config");
    if (!node) {
      return {};
    }
    try {
      return JSON.parse(node.textContent);
    } catch (error) {
      return {};
    }
  }

  function allLanguages() {
    try {
      return window.sessionStorage.getItem(ALL_KEY) === "1";
    } catch (error) {
      return false;
    }
  }

  function setAllLanguages(value) {
    try {
      window.sessionStorage.setItem(ALL_KEY, value ? "1" : "0");
    } catch (error) {
      /* private mode: the switch still works for this page view */
    }
  }

  function loadIndex() {
    if (pages) {
      return Promise.resolve(pages);
    }
    if (pending) {
      return pending;
    }
    pending = fetch(base + "search/search_index.json", { credentials: "same-origin" })
      .then(function (response) {
        return response.ok ? response.json() : { docs: [] };
      })
      .then(function (data) {
        pages = collect(data.docs || []);
        return pages;
      })
      .catch(function () {
        pages = [];
        return pages;
      });
    return pending;
  }

  /* One entry per page: the index has one entry per heading, and a result list wants pages. */
  function collect(docs) {
    var byPath = Object.create(null);
    var order = [];
    docs.forEach(function (doc) {
      var path = String(doc.location || "").split("#")[0];
      var entry = byPath[path];
      if (!entry) {
        entry = byPath[path] = {
          path: path,
          title: doc.title || path,
          text: "",
          lang: doc.lang || (path.indexOf("en/") === 0 ? "en" : "zh"),
          tool: doc.tool || null,
          status: doc.status || null,
          version: doc.version || "",
          branch: doc.branch || "",
          catalog: doc.catalog || null,
        };
        order.push(path);
      }
      entry.text += " " + (doc.text || "");
      if (!doc.location.split("#")[1]) {
        entry.title = doc.title || entry.title;
      }
    });
    return order.map(function (path) {
      return byPath[path];
    });
  }

  function score(entry, tokens, phrase) {
    var title = entry.title.toLowerCase();
    var text = entry.text.toLowerCase();
    var total = 0;
    for (var i = 0; i < tokens.length; i++) {
      var token = tokens[i];
      var inTitle = title.indexOf(token) >= 0;
      var inText = text.indexOf(token) >= 0;
      if (!inTitle && !inText) {
        return 0;
      }
      if (inTitle) {
        total += 1000 + Math.min(count(title, token), 20);
      }
      total += Math.min(count(text, token), 50);
    }
    if (phrase && title.indexOf(phrase) >= 0) {
      total += 5000;
    }
    return total;
  }

  function count(haystack, needle) {
    var found = 0;
    var at = haystack.indexOf(needle);
    while (at >= 0) {
      found++;
      at = haystack.indexOf(needle, at + needle.length);
    }
    return found;
  }

  function toolPages(name) {
    var found = [];
    ["release", "branch"].forEach(function (key) {
      var surface = catalog[key] || {};
      if (!surface.tools || !surface.tools[name]) {
        return;
      }
      var path = surface.directory + "/" + name + "/";
      var known = (pages || []).filter(function (entry) {
        return entry.path === path;
      })[0];
      found.push({
        path: path,
        title: (known && known.title) || surface.tools[name][lang] || name,
        text: (known && known.text) || "",
        lang: lang,
        tool: name,
        status: surface.status,
        version: surface.version || "",
        branch: surface.branch || "",
        catalog: surface.catalog || key,
      });
    });
    return found;
  }

  function search(query) {
    var trimmed = query.trim();
    var phrase = trimmed.toLowerCase();
    var tokens = phrase.split(/\s+/).filter(Boolean);
    var showAll = allLanguages();
    if (!tokens.length) {
      return { query: trimmed, results: [], total: 0, exact: false };
    }
    var exact = TOOL_NAME.test(phrase);
    var ranked = [];
    (pages || []).forEach(function (entry) {
      if (!showAll && entry.lang !== lang) {
        return;
      }
      var value = score(entry, tokens, phrase);
      if (value > 0) {
        ranked.push({ entry: entry, score: value });
      }
    });
    ranked.sort(function (left, right) {
      return right.score - left.score || left.entry.path.localeCompare(right.entry.path);
    });
    var results = ranked.map(function (item) {
      return item.entry;
    });
    if (exact) {
      // An exact tool name is a lookup, not a keyword match: the applicable tool pages come first,
      // release before integration branch, and nothing else may be placed above them.
      var leading = toolPages(phrase);
      var seen = Object.create(null);
      leading.forEach(function (entry) {
        seen[entry.path] = true;
      });
      results = leading.concat(
        results.filter(function (entry) {
          return !seen[entry.path];
        })
      );
    }
    return { query: trimmed, results: results, total: results.length, exact: exact };
  }

  function statusBadge(entry) {
    if (!entry.status) {
      return null;
    }
    var badge = document.createElement("span");
    badge.className = "rmm-search-badge";
    if (entry.status === "released") {
      badge.classList.add("rmm-search-badge--release");
      badge.textContent = labels.release + (entry.version ? " " + entry.version : "");
    } else {
      badge.classList.add("rmm-search-badge--branch");
      badge.textContent = labels.branch + " · " + labels.branchNote;
    }
    return badge;
  }

  function item(entry) {
    var node = document.createElement("li");
    node.className = "md-search-result__item";
    node.setAttribute("data-rmm", "1");
    var link = document.createElement("a");
    link.className = "md-search-result__link";
    link.href = base + entry.path;
    link.setAttribute("tabindex", "-1");
    var article = document.createElement("article");
    article.className = "md-search-result__article md-search-result__article--document";
    var heading = document.createElement("h1");
    heading.textContent = entry.title;
    article.appendChild(heading);
    var badges = document.createElement("p");
    badges.className = "rmm-search-meta";
    var status = statusBadge(entry);
    if (status) {
      badges.appendChild(status);
    }
    if (entry.tool) {
      var tool = document.createElement("code");
      tool.textContent = entry.tool;
      badges.appendChild(tool);
    }
    if (allLanguages() && entry.lang !== lang) {
      var other = document.createElement("span");
      other.className = "rmm-search-badge rmm-search-badge--language";
      other.textContent = labels.language;
      badges.appendChild(other);
    }
    if (badges.childNodes.length) {
      article.appendChild(badges);
    }
    var teaser = document.createElement("p");
    teaser.className = "md-search-result__teaser";
    teaser.textContent = (entry.text || "").trim().slice(0, 160);
    if (teaser.textContent) {
      article.appendChild(teaser);
    }
    link.appendChild(article);
    node.appendChild(link);
    return node;
  }

  function guidance() {
    var box = document.createElement("div");
    box.className = "rmm-search-empty";
    var text = document.createElement("p");
    text.textContent = labels.noResult;
    box.appendChild(text);
    if (!allLanguages()) {
      var all = document.createElement("button");
      all.type = "button";
      all.className = "rmm-search-action";
      all.textContent = labels.noResultAll;
      all.addEventListener("click", function () {
        setAllLanguages(true);
        syncToggle();
        rerender();
      });
      box.appendChild(all);
    }
    var links = document.createElement("p");
    links.className = "rmm-search-links";
    [catalog.release, catalog.branch].forEach(function (surface) {
      if (!surface || !surface.directory) {
        return;
      }
      var link = document.createElement("a");
      link.href = base + surface.directory + "/";
      link.textContent =
        surface.directory === "features"
          ? lang === "zh"
            ? "现有版本目录"
            : "Released catalog"
          : lang === "zh"
          ? "集成分支目录"
          : "Integration branch catalog";
      links.appendChild(link);
    });
    box.appendChild(links);
    return box;
  }

  function render(query) {
    var host = document.querySelector("[data-md-component=search-result]");
    if (!host) {
      return;
    }
    var list = host.querySelector(".md-search-result__list");
    var meta = host.querySelector(".md-search-result__meta");
    var custom = host.querySelector(".rmm-search-results");
    if (!list || !meta) {
      return;
    }
    if (!custom) {
      custom = document.createElement("div");
      custom.className = "rmm-search-results";
      host.appendChild(custom);
    }
    if (!query.trim()) {
      custom.hidden = true;
      list.hidden = false;
      return;
    }
    var outcome = search(query);
    list.hidden = true;
    custom.hidden = false;
    custom.textContent = "";
    var suffix = allLanguages() ? "" : " · " + labels.onlyThis;
    meta.textContent = outcome.total + " " + labels.results + suffix;
    var shown = outcome.results.slice(0, 20);
    if (!shown.length) {
      custom.appendChild(guidance());
      return;
    }
    var container = document.createElement("ol");
    container.className = "md-search-result__list";
    shown.forEach(function (entry) {
      container.appendChild(item(entry));
    });
    custom.appendChild(container);
    if (outcome.total > shown.length) {
      var more = document.createElement("p");
      more.className = "rmm-search-more";
      more.textContent = outcome.total - shown.length + " " + labels.results;
      custom.appendChild(more);
    }
  }

  function rerender() {
    var input = document.querySelector(".md-search__input");
    if (input) {
      render(input.value);
    }
  }

  function syncToggle() {
    var toggle = document.querySelector(".rmm-search-toggle");
    if (!toggle) {
      return;
    }
    toggle.setAttribute("aria-pressed", allLanguages() ? "true" : "false");
    toggle.textContent = labels.allLanguages;
    toggle.classList.toggle("rmm-search-toggle--on", allLanguages());
  }

  function addToggle() {
    var options = document.querySelector(".md-search__options");
    if (!options || options.querySelector(".rmm-search-toggle")) {
      return;
    }
    var toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "rmm-search-toggle";
    toggle.addEventListener("click", function () {
      setAllLanguages(!allLanguages());
      syncToggle();
      rerender();
    });
    options.appendChild(toggle);
    syncToggle();
  }

  function watch() {
    var input = document.querySelector(".md-search__input");
    if (!input) {
      return;
    }
    addToggle();
    input.addEventListener("input", function () {
      var query = input.value;
      window.setTimeout(function () {
        render(query);
      }, 260);
    });
    input.addEventListener("keyup", function () {
      render(input.value);
    });
    var host = document.querySelector("[data-md-component=search-result]");
    if (!host) {
      return;
    }
    // The plugin re-renders the list when its worker answers; keep the language filter and the
    // badges in place after every answer without touching the plugin's own index.
    new MutationObserver(function () {
      var value = input.value;
      if (!value.trim()) {
        return;
      }
      var custom = host.querySelector(".rmm-search-results");
      var list = host.querySelector(".md-search-result__list");
      if (custom && !custom.hidden) {
        if (list) {
          list.hidden = true;
        }
        return;
      }
      render(value);
    }).observe(host, { childList: true, subtree: true, characterData: true });
  }

  function start() {
    if (!document.querySelector(".md-search__input")) {
      window.setTimeout(start, 120);
      return;
    }
    watch();
    loadIndex();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
