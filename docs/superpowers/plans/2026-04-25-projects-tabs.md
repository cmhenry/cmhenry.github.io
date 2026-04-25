# Projects Tab Strip Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the single-project dissertation card into a flexible multi-project section with tabs in the 2024 era and stacked anchor jumps in the 1994 era.

**Architecture:** Same DOM in both eras (tab list + project panels). CSS reskins per `data-era`. A single `initProjects()` function in `app.js` handles tab activation in 2024 and lets native anchor jumps work in 1994.

**Tech Stack:** Vanilla HTML/CSS/JS. No build step. Static site.

**Spec:** `docs/superpowers/specs/2026-04-25-projects-tabs-design.md`

**Note on testing:** This is a static site with no test harness. Verification is manual in the browser — the final task lists explicit checks.

---

## File Structure

- `index.html` — replace the `<section id="research">` block.
- `styles/era-1994.css` — append projects/tabs rules at end of file.
- `styles/era-2024.css` — append projects/tabs rules; extend `.card--highlight::before` selector to also apply to `.card--projects`.
- `app.js` — add `initProjects()`, call it from boot and from `transitionTo()` after `applyEra()`. Add `hashchange` listener.

---

### Task 1: Replace `#research` section in `index.html`

**Files:**
- Modify: `index.html` (lines 76-90)

- [ ] **Step 1: Replace the section**

Replace the existing `<section id="research" class="card card--highlight">…</section>` block with:

```html
  <!-- Projects (tabbed in 2024, stacked in 1994) -->
  <section id="research" class="card card--projects">
    <h2 class="card__title">
      <span data-era-text='{"1994":"Projects","2024":"projects"}'>projects</span>
    </h2>

    <ul class="projects__tabs" role="tablist">
      <li role="presentation">
        <a id="tab-snsf" role="tab" href="#snsf" aria-controls="snsf" aria-selected="true">snsf · public discourse</a>
      </li>
      <li role="presentation">
        <a id="tab-dissertation" role="tab" href="#dissertation" aria-controls="dissertation" aria-selected="false">dissertation</a>
      </li>
      <li role="presentation">
        <a id="tab-virena" role="tab" href="#virena" aria-controls="virena" aria-selected="false">virena</a>
      </li>
    </ul>

    <article class="project" id="snsf" role="tabpanel" aria-labelledby="tab-snsf">
      <h3 class="project__name">SNSF Improving Public Discourse</h3>
      <p><strong>Title.</strong> [placeholder]</p>
      <p><strong>Description.</strong> [placeholder]</p>
      <p><strong>Collaborators.</strong> [placeholder]</p>
      <p class="project__cta">
        <a class="btn" href="#" target="_blank" rel="noopener">project site ↗</a>
      </p>
    </article>

    <article class="project" id="dissertation" role="tabpanel" aria-labelledby="tab-dissertation" hidden>
      <h3 class="project__name">Dissertation</h3>
      <p><strong>Title.</strong> "Governance, Competition, &amp; Extremism: How the Structure of Social Media Platforms Radicalizes Communities"</p>
      <p><strong>Core argument.</strong> Platform governance structures create competitive dynamics between communities that systematically drive radicalization. A comparative study of digital architectures and how they shape collective behavior.</p>
      <p><strong>Methods.</strong> Multi-platform analysis (Reddit, Twitter, Telegram, TikTok, YouTube), transformer models, network analysis, digital ethnography.</p>
      <p><strong>Advised by.</strong> Jennifer Larson (co-chair), Cassy Dorff (co-chair), Emily Ritter, Anita Gohdes (Hertie School).</p>
      <p class="project__cta">
        <a class="btn" href="https://github.com/cmhenry/cmhenry.github.io/raw/main/pdfs/Community_Competition.pdf" target="_blank" rel="noopener">
          <span data-era-text='{"1994":"[ Job Market Paper ]","2024":"job-market-paper.pdf ↗"}'>job-market-paper.pdf ↗</span>
        </a>
      </p>
    </article>

    <article class="project" id="virena" role="tabpanel" aria-labelledby="tab-virena" hidden>
      <h3 class="project__name">VIRENA</h3>
      <p><strong>Title.</strong> [placeholder]</p>
      <p><strong>Description.</strong> [placeholder]</p>
      <p><strong>Collaborators.</strong> [placeholder]</p>
      <p class="project__cta">
        <a class="btn" href="#" target="_blank" rel="noopener">repo ↗</a>
      </p>
    </article>
  </section>
```

The dissertation panel preserves the existing PDF link (with the era-text wrapper for "[ Job Market Paper ]" / "job-market-paper.pdf ↗"). SNSF and VIRENA tabs use `[placeholder]` text since the user will fill in real content manually.

---

### Task 2: Add 1994 era CSS rules

**Files:**
- Modify: `styles/era-1994.css` (append at end)

- [ ] **Step 1: Append projects rules**

Append:

```css

/* Projects tabs — 1994: stacked panels with a "Jump to" link strip */
[data-era="1994"] .projects__tabs {
  list-style: none;
  padding: 0;
  margin: 0 0 0.6em;
  display: inline;
  font-style: italic;
}
[data-era="1994"] .projects__tabs::before { content: "Jump to: "; font-style: italic; }
[data-era="1994"] .projects__tabs li { display: inline; }
[data-era="1994"] .projects__tabs li + li::before { content: " | "; color: #000; font-style: normal; }
[data-era="1994"] .projects__tabs a[aria-selected="true"] { font-weight: bold; }

[data-era="1994"] .project {
  border-top: 1px solid #808080;
  padding-top: 0.6em;
  margin-top: 0.6em;
}
[data-era="1994"] .project__name {
  font-size: 1.2em;
  font-weight: bold;
  margin: 0 0 0.4em;
}
[data-era="1994"] .project__cta { margin-top: 0.6em; }

/* Override: in 1994 stacked mode, force panels visible even with [hidden] */
[data-era="1994"] .project[hidden] { display: block; }
```

The last rule defends against a race during era switch where `app.js` hasn't yet removed the `hidden` attribute from panels.

---

### Task 3: Add 2024 era CSS rules

**Files:**
- Modify: `styles/era-2024.css`

- [ ] **Step 1: Extend the orange highlight bar selector**

Find the existing rules:

```css
[data-era="2024"] .card--highlight {
  position: relative;
}
[data-era="2024"] .card--highlight::before {
  content: "";
  grid-column: 1;
  grid-row: 1 / span 10;
  width: 4px;
  background: #ff5c1f;
  margin-top: 0.2rem;
  height: 100%;
}
```

Change both selectors to include `.card--projects`:

```css
[data-era="2024"] .card--highlight,
[data-era="2024"] .card--projects {
  position: relative;
}
[data-era="2024"] .card--highlight::before,
[data-era="2024"] .card--projects::before {
  content: "";
  grid-column: 1;
  grid-row: 1 / span 10;
  width: 4px;
  background: #ff5c1f;
  margin-top: 0.2rem;
  height: 100%;
}
```

- [ ] **Step 2: Extend the mobile override**

Find:

```css
  [data-era="2024"] .card--highlight::before { display: none; }
```

Change to:

```css
  [data-era="2024"] .card--highlight::before,
  [data-era="2024"] .card--projects::before { display: none; }
```

- [ ] **Step 3: Append projects rules at end of file**

Append:

```css

/* Projects tabs — 2024: brutalist tab strip + single-panel display */
[data-era="2024"] .projects__tabs {
  list-style: none;
  padding: 0;
  margin: 0 0 1.2rem;
  grid-column: 2;
  display: flex;
  flex-wrap: wrap;
  border-bottom: 2px solid #111;
}
[data-era="2024"] .projects__tabs a {
  display: inline-block;
  padding: 0.55em 1em;
  font-family: "IBM Plex Mono", monospace;
  font-size: 0.78rem;
  text-transform: lowercase;
  letter-spacing: 0.06em;
  text-decoration: none;
  color: #111;
  border-left: 1px solid #111;
}
[data-era="2024"] .projects__tabs li:first-child a { border-left: 0; }
[data-era="2024"] .projects__tabs a[aria-selected="true"] {
  background: #111;
  color: #fafaf7;
}
[data-era="2024"] .projects__tabs a:hover {
  background: #ff5c1f;
  color: #fff;
}

[data-era="2024"] .project {
  grid-column: 2;
  font-family: "IBM Plex Sans", sans-serif;
  max-width: 62ch;
}
[data-era="2024"] .project > p {
  margin: 0 0 0.9em;
  font-size: 1rem;
}
[data-era="2024"] .project > p strong { font-weight: 700; }
[data-era="2024"] .project__name { display: none; }
[data-era="2024"] .project__cta { margin-top: 1rem; }
```

---

### Task 4: Add `initProjects()` to `app.js`

**Files:**
- Modify: `app.js`

- [ ] **Step 1: Add the function and wire it up**

Inside the IIFE, after `applyEra()` definition and before the boot block, add:

```javascript
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
```

- [ ] **Step 2: Call `initProjects()` on boot**

Find the boot block:

```javascript
  applyEra(initial, false);
```

Add immediately after:

```javascript
  initProjects();
```

- [ ] **Step 3: Re-run on era switch**

Find inside `transitionTo()`:

```javascript
    setTimeout(function () {
      applyEra(era, true);
      // hold briefly, then fade back out
```

Change to:

```javascript
    setTimeout(function () {
      applyEra(era, true);
      initProjects();
      // hold briefly, then fade back out
```

- [ ] **Step 4: Add hashchange listener (2024 deep links)**

After the keyboard shortcut block at the bottom of the IIFE, add:

```javascript
  window.addEventListener("hashchange", function () {
    if (html.getAttribute("data-era") !== "2024") return;
    initProjects();
  });
```

---

### Task 5: Manual smoke test in browser

**Files:** none (verification step)

- [ ] **Step 1: Start a local server**

Run: `cd /Users/cohenr/Projects/cmhenry.github.io && python3 -m http.server 8765`

- [ ] **Step 2: Verify default load**

Open `http://localhost:8765/`. Expect:
- 2024 era active. Projects section visible with three tabs: `snsf · public discourse` (active, dark fill), `dissertation`, `virena`.
- The SNSF panel shows below. Orange vertical bar to the left of the tab strip.

- [ ] **Step 3: Verify tab clicks**

Click `dissertation`. Expect: SNSF tab loses dark fill, dissertation tab gains it; SNSF panel hides; dissertation panel shows with full content; URL bar shows `#dissertation`; page does not jump-scroll.

Click `virena`, then `snsf · public discourse`. Each click swaps the panel and updates the URL.

- [ ] **Step 4: Verify deep link**

Open `http://localhost:8765/#dissertation` directly. Expect: dissertation tab is active, dissertation panel visible.

- [ ] **Step 5: Verify era switch**

Click the corner "view as 1994 ↗" link (or press `T`). Expect: page fades to dark, comes back as 1994 — gray bg, Times serif. The Projects section now shows:
- "Projects" h2
- "Jump to: snsf · public discourse | dissertation | virena" (italic line)
- All three project panels stacked, each with a thin gray top border, with `<h3>` title visible.

Click the "Jump to: dissertation" link. Expect: page scrolls to the dissertation `<article>`.

- [ ] **Step 6: Verify era switch back**

Click the corner toggle again to return to 2024. Expect: 2024 tabs return; the active tab is whichever the URL hash names (likely `dissertation` from the previous step's anchor jump, since that updates `location.hash`).

- [ ] **Step 7: Stop the server**

Ctrl+C in the server terminal.

---

### Task 6: Commit

- [ ] **Step 1: Commit all changes**

```bash
git add index.html app.js styles/era-1994.css styles/era-2024.css
git commit -m "feat: convert dissertation card into projects tab strip

Replaces single-project highlight with a flexible multi-project
section. 2024 era renders as brutalist tab strip with single-panel
display and deep-link support; 1994 era stacks all panels with
italic 'Jump to:' anchor links. Three launch tabs: SNSF, Dissertation,
VIRENA."
```
