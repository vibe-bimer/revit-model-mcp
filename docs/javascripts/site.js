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
  }

  function boot() {
    initProgress();
    initReveal();
    initCopy();
    initHero();
    initHeader();
    initA11y();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
