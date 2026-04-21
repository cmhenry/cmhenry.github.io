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

  /* --- Fade transition --------------------------------------------------- */
  var isTransitioning = false;
  function transitionTo(era) {
    if (isTransitioning) return;
    isTransitioning = true;
    body.classList.add("is-transitioning");
    // fade to black
    setTimeout(function () {
      applyEra(era, true);
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
})();
