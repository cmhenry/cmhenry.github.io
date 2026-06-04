/* app.js — minimal 1994/2024 toggle with a clean fade transition */
(function () {
  var ERAS = ["1994", "2024"];
  var STORAGE_KEY = "cmhenry.era";
  var DEFAULT_ERA = "2024";

  var html = document.documentElement;
  var body = document.body;
  var hint = document.getElementById("era-hint");

  function applyEraText(era) {
    document.querySelectorAll("[data-era-text]").forEach(function (n) {
      try {
        var map = JSON.parse(n.getAttribute("data-era-text"));
        if (map && typeof map[era] !== "undefined") n.innerHTML = map[era];
      } catch (e) {}
    });
  }

  function applyEra(era, persist) {
    if (ERAS.indexOf(era) === -1) era = DEFAULT_ERA;
    html.setAttribute("data-era", era);
    applyEraText(era);
    if (persist) {
      try { localStorage.setItem(STORAGE_KEY, era); } catch (e) {}
    }
  }

  function otherEra() {
    return html.getAttribute("data-era") === "1994" ? "2024" : "1994";
  }

  /* --- Projects tabs ----------------------------------------------------- */
  function initProjects() {
    var tablist = document.querySelector(".projects__tabs");
    if (!tablist) return;
    var tabs = Array.prototype.slice.call(tablist.querySelectorAll('[role="tab"]'));
    var panels = Array.prototype.slice.call(
      document.querySelectorAll(".card--projects .project")
    );
    var era = html.getAttribute("data-era");

    function activate(id) {
      tabs.forEach(function (t) {
        t.setAttribute("aria-selected", t.getAttribute("aria-controls") === id ? "true" : "false");
      });
      panels.forEach(function (p) {
        if (p.id === id) p.removeAttribute("hidden");
        else p.setAttribute("hidden", "");
      });
    }

    if (era === "2024") {
      var ids = panels.map(function (p) { return p.id; });
      var hashId = (location.hash || "").replace(/^#/, "");
      var initial = ids.indexOf(hashId) !== -1 ? hashId : ids[0];
      activate(initial);

      tabs.forEach(function (t) {
        t.onclick = function (e) {
          e.preventDefault();
          var id = t.getAttribute("aria-controls");
          activate(id);
          history.replaceState({}, "", "#" + id);
        };
      });
    } else {
      // 1994: show everything stacked, no click interception
      panels.forEach(function (p) { p.removeAttribute("hidden"); });
      tabs.forEach(function (t) { t.onclick = null; });
    }
  }

  /* --- Fade transition --------------------------------------------------- */
  var isTransitioning = false;
  function transitionTo(era) {
    if (isTransitioning) return;
    isTransitioning = true;
    body.classList.add("is-transitioning");
    // fade to black
    setTimeout(function () {
      applyEra(era, true);
      initProjects();
      // hold briefly, then fade back out
      setTimeout(function () {
        body.classList.remove("is-transitioning");
        isTransitioning = false;
      }, 120);
    }, 280);
  }

  /* --- Boot -------------------------------------------------------------- */
  var initial = DEFAULT_ERA;
  try {
    var saved = localStorage.getItem(STORAGE_KEY);
    if (saved && ERAS.indexOf(saved) !== -1) initial = saved;
  } catch (e) {}
  applyEra(initial, false);
  initProjects();

  if (hint) {
    hint.addEventListener("click", function (e) {
      e.preventDefault();
      transitionTo(otherEra());
    });
  }

  // Keyboard shortcut — `T` for "time travel". Ignore if user is typing.
  document.addEventListener("keydown", function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    var tag = (e.target && e.target.tagName || "").toUpperCase();
    if (tag === "INPUT" || tag === "TEXTAREA" || e.target.isContentEditable) return;
    if (e.key === "t" || e.key === "T") {
      transitionTo(otherEra());
    }
  });

  window.addEventListener("hashchange", function () {
    if (html.getAttribute("data-era") !== "2024") return;
    initProjects();
  });
})();
