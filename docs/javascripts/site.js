/* Progressive enhancement for the documentation site.
 *
 * Nothing here is load-bearing: with scripting disabled every page still reads and navigates. Each
 * feature is additive, idempotent and honours prefers-reduced-motion.
 */
(function () {
  "use strict";

  var root = document.documentElement;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Reading progress ------------------------------------------------------ */

  function initProgress() {
    var bar = document.querySelector(".rmc-progress__bar");
    if (!bar) return;
    var pending = false;

    function update() {
      pending = false;
      var doc = document.documentElement;
      var max = doc.scrollHeight - doc.clientHeight;
      var ratio = max > 0 ? Math.min(1, Math.max(0, doc.scrollTop / max)) : 0;
      bar.style.transform = "scaleX(" + ratio + ")";
    }

    addEventListener(
      "scroll",
      function () {
        if (pending) return;
        pending = true;
        requestAnimationFrame(update);
      },
      { passive: true }
    );
    addEventListener("resize", update, { passive: true });
    update();
  }

  /* Reveal on scroll ------------------------------------------------------ */

  function initReveal() {
    var items = document.querySelectorAll(".rmc-reveal");
    if (!items.length) return;

    if (reduced || !("IntersectionObserver" in window)) {
      items.forEach(function (el) {
        el.classList.add("rmc-reveal--in");
      });
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("rmc-reveal--in");
          observer.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.05 }
    );

    items.forEach(function (el) {
      observer.observe(el);
    });

    /* Anything already on screen at load reveals immediately; a safety timer
       covers layouts where the observer never fires. */
    setTimeout(function () {
      items.forEach(function (el) {
        var box = el.getBoundingClientRect();
        if (box.top < innerHeight && box.bottom > 0) el.classList.add("rmc-reveal--in");
      });
    }, 60);
    setTimeout(function () {
      items.forEach(function (el) {
        el.classList.add("rmc-reveal--in");
      });
    }, 3000);
  }

  /* Copy-to-clipboard ----------------------------------------------------- */

  var COPY_LABEL = root.lang === "en" ? "Copy" : "复制";
  var COPIED_LABEL = root.lang === "en" ? "Copied" : "已复制";
  var FAILED_LABEL = root.lang === "en" ? "Copy failed" : "复制失败";

  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var area = document.createElement("textarea");
      area.value = text;
      area.setAttribute("readonly", "");
      area.style.position = "fixed";
      area.style.opacity = "0";
      document.body.appendChild(area);
      area.select();
      try {
        document.execCommand("copy") ? resolve() : reject(new Error("copy failed"));
      } catch (error) {
        reject(error);
      } finally {
        document.body.removeChild(area);
      }
    });
  }

  function initCopy() {
    document.querySelectorAll("[data-rmc-copy]").forEach(function (host) {
      if (host.dataset.rmcCopyReady) return;
      host.dataset.rmcCopyReady = "1";

      var button = document.createElement("button");
      button.type = "button";
      button.className = "rmc-copy";
      button.textContent = COPY_LABEL;
      button.setAttribute("aria-live", "polite");

      button.addEventListener("click", function () {
        var source = host.querySelector("[data-rmc-copy-source]") || host;
        var text = (source.innerText || source.textContent || "").trim();
        copyText(text).then(
          function () {
            button.textContent = COPIED_LABEL;
            button.classList.add("is-copied");
            setTimeout(function () {
              button.textContent = COPY_LABEL;
              button.classList.remove("is-copied");
            }, 1600);
          },
          function () {
            button.textContent = FAILED_LABEL;
            setTimeout(function () {
              button.textContent = COPY_LABEL;
            }, 1600);
          }
        );
      });

      host.appendChild(button);
    });
  }

  /* Hero draw-in ---------------------------------------------------------- */

  function initHero() {
    var hero = document.querySelector(".rmc-hero");
    if (!hero) return;
    if (reduced) {
      hero.classList.add("is-drawn");
      return;
    }
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        hero.classList.add("is-drawn");
      });
    });
  }

  /* Sticky-header state --------------------------------------------------- */

  function initHeader() {
    var header = document.querySelector(".md-header");
    if (!header) return;
    var ticking = false;

    function update() {
      ticking = false;
      header.classList.toggle("rmc-header--raised", window.scrollY > 8);
    }

    addEventListener(
      "scroll",
      function () {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(update);
      },
      { passive: true }
    );
    update();
  }

  /* Accessibility repairs -------------------------------------------------
   *
   * Three defects in the stock theme that only scripting can close:
   *   1. Below the drawer breakpoint the off-canvas navigation stays focusable
   *      while it is parked outside the viewport, so Tab walks into invisibility.
   *   2. The search overlay is role="dialog" with no accessible name.
   *   3. Navigation expanders are focusable labels with no role, no name and no
   *      state, so a screen reader announces nothing about what they do.
   * The theme already activates those labels on Enter and Space, so no key
   * handling is added here: role="button" is already true of them.
   */

  var DRAWER_QUERY = "(max-width: 76.234375em)";

  function initA11y() {
    var drawerInput = document.getElementById("__drawer");
    var drawerNav = document.querySelector(".md-sidebar--primary");
    if (drawerInput && drawerNav && "inert" in drawerNav) {
      var narrow = window.matchMedia(DRAWER_QUERY);
      var syncDrawer = function () {
        drawerNav.inert = narrow.matches && !drawerInput.checked;
      };
      drawerInput.addEventListener("change", syncDrawer);
      narrow.addEventListener("change", syncDrawer);
      syncDrawer();
    }

    var search = document.querySelector(".md-search");
    if (search && !search.getAttribute("aria-label")) {
      var field = search.querySelector(".md-search__input");
      var name = (field && field.placeholder) || search.getAttribute("data-md-component");
      if (name) search.setAttribute("aria-label", name);
    }

    document.querySelectorAll("label.md-nav__link[for]").forEach(function (label) {
      var toggle = document.getElementById(label.getAttribute("for"));
      if (!toggle || toggle.type !== "checkbox") return;
      label.setAttribute("role", "button");
      var sync = function () {
        label.setAttribute("aria-expanded", toggle.checked ? "true" : "false");
      };
      sync();
      toggle.addEventListener("change", sync);
      if (!label.textContent.trim()) {
        // An icon-only expander still names the section it opens.
        var item = label.closest(".md-nav__item");
        var link = item && item.querySelector("a.md-nav__link");
        var text = link && link.textContent.trim();
        if (text) label.setAttribute("aria-label", text);
      }
    });

    /* The theme's skip link points at the first heading of the page, and a heading only takes
       focus when it is told to. Without this the browser scrolls to the heading but leaves focus
       on the body, so the next Tab starts again from the top of the page. */
    document.querySelectorAll(".md-content :is(h1, h2, h3)[id]").forEach(function (heading) {
      if (!heading.hasAttribute("tabindex")) heading.setAttribute("tabindex", "-1");
    });
  }

  /* Wide tables ------------------------------------------------------------
   *
   * Three things the markup cannot do on its own:
   *   1. Hand-written tables arrive without header scopes, so a screen reader
   *      cannot say which column a cell belongs to.
   *   2. A table wider than its column scrolls; a scroll container is only
   *      reachable with the keyboard once it is focusable, so it becomes a
   *      labelled region while it overflows and a plain block when it fits.
   *   3. On a phone a five-column reference table is unreadable even when it
   *      fits, so each row becomes a block and every cell shows its header.
   */

  var STACK_QUERY = "(max-width: 30em)";
  /* The same number check_site gates the generated sources on (WIDE_TABLE_COLUMNS): below it a
     table still reads in its grid, at or above it the rows stack on a phone. Generated and
     hand-written tables share the rule, because the script wraps them all the same way. */
  var STACK_MIN_COLUMNS = 5;
  var SCROLL_LABEL = root.lang === "en" ? "Table, scrolls sideways" : "表格，可横向滚动";
  var stackQuery = window.matchMedia(STACK_QUERY);

  /* Pure decision, kept out of syncTable so it reads as one sentence: a table stacks when the
     viewport is the narrow one and the table carries this many columns or more. */
  function stacksWhenNarrow(columns, narrow) {
    return narrow && columns >= STACK_MIN_COLUMNS;
  }

  function tableWrap(table) {
    /* Material's own script may already have wrapped the table in its scroller, so walk up the
       ancestors instead of inspecting the parent alone: a second wrapper would nest a second
       scroll container. */
    var existing = table.closest(".rmc-tablewrap");
    if (existing) return existing;
    var host = table.parentElement;
    var wrap = document.createElement("div");
    wrap.className = "rmc-tablewrap";
    host.insertBefore(wrap, table);
    wrap.appendChild(table);
    return wrap;
  }

  function labelTable(table) {
    var head = table.tHead && table.tHead.rows[0];
    if (!head) return;
    var labels = [];
    Array.prototype.forEach.call(head.cells, function (cell) {
      if (cell.tagName === "TH" && !cell.getAttribute("scope")) {
        cell.setAttribute("scope", "col");
      }
      labels.push((cell.textContent || "").trim());
    });
    // Print needs a column count to lay a table out to the sheet width without guessing.
    table.setAttribute("data-rmc-cols", String(labels.length));
    Array.prototype.forEach.call(table.tBodies, function (body) {
      Array.prototype.forEach.call(body.rows, function (row) {
        Array.prototype.forEach.call(row.cells, function (cell, index) {
          if (cell.hasAttribute("data-rmc-label")) return;
          cell.setAttribute("data-rmc-label", labels[index] || "");
        });
      });
    });
  }

  function syncTable(wrap) {
    var table = wrap.querySelector("table");
    if (!table) return;
    var head = table.tHead && table.tHead.rows[0];
    var columns = head ? head.cells.length : 0;
    if (stacksWhenNarrow(columns, stackQuery.matches)) wrap.setAttribute("data-rmc-stack", "");
    else wrap.removeAttribute("data-rmc-stack");
    if (wrap.scrollWidth - wrap.clientWidth > 1) {
      wrap.setAttribute("data-rmc-scrollable", "");
      wrap.setAttribute("tabindex", "0");
      wrap.setAttribute("role", "region");
      wrap.setAttribute("aria-label", SCROLL_LABEL);
    } else {
      wrap.removeAttribute("data-rmc-scrollable");
      wrap.removeAttribute("tabindex");
      wrap.removeAttribute("role");
      wrap.removeAttribute("aria-label");
    }
  }

  function initTables() {
    var wraps = [];
    document.querySelectorAll(".md-typeset table").forEach(function (table) {
      var wrap = tableWrap(table);
      labelTable(table);
      wraps.push(wrap);
    });
    if (!wraps.length) return;

    var sync = function () {
      wraps.forEach(syncTable);
    };
    sync();
    /* Cell widths follow the webfonts, so a table can start overflowing after the first measure. */
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(sync);
    stackQuery.addEventListener("change", sync);
    addEventListener(
      "resize",
      function () {
        requestAnimationFrame(sync);
      },
      { passive: true }
    );
  }

  function boot() {
    initProgress();
    initReveal();
    initCopy();
    initHero();
    initHeader();
    initA11y();
    initTables();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
