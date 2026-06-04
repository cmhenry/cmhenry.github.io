# Projects tab strip — design

**Date:** 2026-04-25
**Branch:** `era-redesign`
**Touches:** `index.html`, `app.js`, `styles/era-1994.css`, `styles/era-2024.css`

## Goal

Convert the single `.card--highlight` "Dissertation" section into a multi-project area that holds three (and later more) project profiles, switchable via tabs in the 2024 era and stacked with anchor jumps in the 1994 era. Each project profile is hand-authored with arbitrary, renameable fields and one external link.

## Scope

- Three project tabs at launch, in this order:
  1. **SNSF Improving Public Discourse** (default / first) — `id="snsf"`
  2. **Dissertation** — `id="dissertation"`
  3. **VIRENA** (AI agents chatroom experiment) — `id="virena"`
- Field content is placeholder only — Colin will write the prose.
- Field names are not fixed — each `<p>` can use any bold prefix (e.g. `<strong>Methods.</strong>`, `<strong>Collaborators.</strong>`, `<strong>Funder.</strong>`).
- Each panel has exactly one outbound link styled as the existing `.btn`.
- Deep-linking via URL hash works on load and on era switch.

Out of scope:
- Adding/removing tabs at runtime (purely an authoring change to `index.html`).
- A formal field schema. Fields are just `<p><strong>Name.</strong> body</p>`.
- Animations beyond what already exists (the era fade is unchanged).

## DOM shape

Replace the current `<section id="research" class="card card--highlight">` with:

```html
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
    <p><strong>Core argument.</strong> Platform governance structures create competitive dynamics between communities that systematically drive radicalization.</p>
    <p><strong>Methods.</strong> Multi-platform analysis (Reddit, Twitter, Telegram, TikTok, YouTube), transformer models, network analysis, digital ethnography.</p>
    <p><strong>Advised by.</strong> Jennifer Larson (co-chair), Cassy Dorff (co-chair), Emily Ritter, Anita Gohdes (Hertie School).</p>
    <p class="project__cta">
      <a class="btn" href="https://github.com/cmhenry/cmhenry.github.io/raw/main/pdfs/Community_Competition.pdf" target="_blank" rel="noopener">job-market-paper.pdf ↗</a>
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

Authoring rules (informal):
- Add a project: append a `<li>` to the tab list and an `<article class="project" id="…" hidden>` panel. The first one omits `hidden` and gets `aria-selected="true"` on its tab.
- Rename a field: edit the `<strong>` text. No CSS or JS changes.
- Reorder fields: move the `<p>` elements within an `.project`.
- Tab labels can use the same `data-era-text` JSON pattern if a project ever needs different labels per era; not used at launch.

## Behavior (`app.js`)

Add a single function `initProjects()`:

- Selects all `[role="tab"]` inside `.projects__tabs` and all `.project` panels in the same section.
- **2024 branch:**
  - On boot/era-switch, read `location.hash`. If it matches a known panel id, activate that tab; otherwise activate the first one (SNSF).
  - "Activate" = set `aria-selected="true"` on the chosen tab and `false` on the rest; remove `hidden` from the chosen panel and set it on the rest.
  - On tab click, `preventDefault()`, activate, and update the hash via `history.replaceState({}, '', '#' + id)` (no scroll-jump).
- **1994 branch:**
  - Remove `hidden` from every panel so they all stack.
  - Tab `<a>` elements behave as native anchor links (no `preventDefault`).
- Bind once at boot, re-run after `applyEra()` inside `transitionTo()` so behavior matches the active era.
- Listen for `hashchange` (2024 only) so external deep links and browser back/forward switch tabs.

No-JS fallback: in both eras every panel is visible (acceptable degradation — content is all there, just stacked).

## Styling

### `styles/era-1994.css`

```css
[data-era="1994"] .projects__tabs {
  list-style: none;
  padding: 0;
  margin: 0 0 0.6em;
  display: inline;
  font-style: italic;
}
[data-era="1994"] .projects__tabs::before { content: "Jump to: "; font-style: italic; }
[data-era="1994"] .projects__tabs li { display: inline; }
[data-era="1994"] .projects__tabs li + li::before { content: " | "; color: #000; }
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
```

### `styles/era-2024.css`

- Apply the existing `.card--highlight::before` orange bar rule to `.card--projects` as well (either rename the selector or add a comma).
- Add tab-strip + panel rules:

```css
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
[data-era="2024"] .projects__tabs a:hover { background: #ff5c1f; color: #fff; }

[data-era="2024"] .project {
  grid-column: 2;
  font-family: "IBM Plex Sans", sans-serif;
  max-width: 62ch;
}
[data-era="2024"] .project > p { margin: 0 0 0.9em; font-size: 1rem; }
[data-era="2024"] .project > p strong { font-weight: 700; }
[data-era="2024"] .project__name { display: none; }
[data-era="2024"] .project__cta { margin-top: 1rem; }
```

Mobile (`@media (max-width: 720px)`): tabs already wrap via `flex-wrap`; the parent `.card` grid collapses to single-column via the existing rule. The orange `::before` bar already hides at this breakpoint via the existing `.card--highlight::before { display: none; }` rule — apply the same to `.card--projects`.

## Era-text considerations

- The section title uses `data-era-text` to flip "Projects" / "projects" — same casing convention as other titles.
- Tab labels are the same in both eras at launch (`snsf · public discourse`, `dissertation`, `virena`). 1994 reads them as italic anchor text, which fits. If a future project needs different per-era labels, it's a one-line `data-era-text` addition.
- Panel field names are author-controlled and not era-specific.

## Files changed

- `index.html` — replace the `#research` section block.
- `app.js` — add `initProjects()`, call it from boot and from `transitionTo` after `applyEra`.
- `styles/era-1994.css` — append projects/tabs rules at end of file.
- `styles/era-2024.css` — append projects/tabs rules; extend `.card--highlight::before` selector to also cover `.card--projects`.

## Acceptance

- Page loads at `index.html` (no hash) → 2024 era, SNSF panel visible, SNSF tab marked active.
- `index.html#dissertation` → dissertation panel visible, dissertation tab active.
- Clicking another tab swaps the panel and updates the URL hash without page jump.
- Switching to 1994 era via the hint button: tab strip becomes "Jump to: A | B | C", all three panels stack with `<hr>`-style separators, and `#dissertation` jump-link still scrolls to the right panel.
- Switching back to 2024 reactivates the last-selected tab (whatever's in the hash).
- No console errors. No-JS render shows all three panels stacked in both eras.
