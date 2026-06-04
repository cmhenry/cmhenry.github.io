# Handoff — Site Redesign

Session notes for picking up the redesign of `cmhenry.github.io` against `DESIGN.md`.
Read `DESIGN.md` first for the aesthetic principles; this doc captures the decisions
already locked in, the current state of the build, and the open questions.

---

## Thesis (locked)

**Working document × small press.**

- *Working document* — drafts are visible, status of every paper is on the surface,
  "last build" is shown, the site reads as in-process not as marketing.
- *Small press* — publications are the structural center; the site is a pamphlet
  for the work, not a portfolio.

Status taxonomy (used across `papers.yaml` and `projects.yaml`):
`draft | working-paper | under-review | r-and-r | published | active | wrapped`.

---

## Design decisions (locked)

| Decision | Choice | Rationale |
|---|---|---|
| Era toggle | Dropped from main page; preserved as an easter egg at `/1994.html` (not yet built). Hint lives in an HTML comment at the top of `index.html`. | DESIGN.md's mk.gg lesson: commit fully to one aesthetic. Dual-mode dilutes the print-editorial principle and doubles maintenance. |
| Type — body | Charter (system stack, with Iowan Old Style / Sitka Text / Georgia fallback) | Print-editorial pedigree (Matthew Carter, designed under constraint). |
| Type — metadata | JetBrains Mono via Google Fonts | Real monospace for status labels, dates, kv-pairs — the "working document" half. |
| Palette | Monochrome: ink on warm off-white paper (`#111` on `#f6f3eb`). No accent color; hover inverts (paper-on-ink). | DESIGN.md "severe palette constraint." |
| Layout | Single column, `max-width: 38rem`, hr-driven structure. | DESIGN.md "horizontal rules as structure." |
| JavaScript | Zero. | DESIGN.md "near-zero JS"; site is fully static. |
| Headshot | Replaced with small dithered/pixel portrait (existing `thumbnail2.png`) at 110px, grayscaled, with a `fig. 1` caption — used as a craft/constraint specimen, not as a hero. | Per user pref: dithering as craft note. |
| Visitor counter | Kept (52,847), even if fictional, as metadata-as-design. Joined by `iss. YYYY`, `build YYYY-MM-DD`. | Nous Research lesson surfaced via masthead ID line. |
| Maintenance | YAML + tiny Python build (PyYAML + Jinja2). One `build.py`, ~80 lines. Output `index.html` is committed; GitHub Pages serves it directly. | User preference: not expecting growth; lightweight is right. |

---

## File map

### New (generated / authored this session)
```
data/
  meta.yaml         site name, role, affiliation, email, CV url, visitor count, about text
  papers.yaml       every paper-shaped artifact, with a `status` field
  projects.yaml     ongoing programs/infrastructure (SNSF, VIRENA, dissertation, ABM)
  links.yaml        elsewhere/social/profile links

templates/
  index.html.jinja  the layout — masthead, nav, status, papers grouped by status, projects, elsewhere, contact, colophon

styles/
  main.css          fresh stylesheet (Charter + JetBrains Mono, monochrome, hr-driven)

build.py            ~80 lines: load yaml, group/sort, render template, write index.html
requirements.txt    PyYAML>=6.0, Jinja2>=3.1
index.html          REGENERATED — do not edit by hand; edit data/ and rebuild
HANDOFF.md          this file
DESIGN.md           the source spec (untouched)
```

### Preserved but unused (scaffolding for the `/1994.html` easter egg)
```
app.js                       (era-toggle JS)
styles/base.css              (shared CSS for both eras)
styles/era-1994.css          (1994-mode styles — extract from here for the easter egg)
styles/era-2024.css          (2024-mode — obsoleted by the new main.css)
styles/switcher.css          (the toggle button styles)
index-archive.html           (an earlier version, not the dual-era one)
```

### Untouched
```
pdfs/, img/, fonts/, css/, media/, pages/, thumbnail.jpg, thumbnail2.png, etc.
```

---

## Maintenance workflow

Updating content is now data-driven. Code is not touched for content edits.

```bash
# 1. edit one of the YAML files
vim data/papers.yaml          # e.g., change `status: r-and-r` → `status: published`

# 2. regenerate the static HTML
python3 build.py              # writes index.html

# 3. commit both the data change and the regenerated HTML
git add data/papers.yaml index.html
git commit -m "publication: <paper> moved to published"
```

To preview locally:
```bash
python3 -m http.server 8000
# open http://localhost:8000
```

**Important:** never hand-edit `index.html` — it's a build artifact and will be overwritten.
Edit `templates/index.html.jinja` (for structure/markup changes) or `data/*.yaml` (for content).

---

## What's still open

These are unresolved as of session end. Pick up here.

### Visual review pending
The draft has been built but not yet reviewed in a browser. Likely points of iteration:

1. **Name scale** — currently `clamp(3.25rem, 14vw, 6.5rem)`. May be too large or too small once viewed.
2. **Portrait** — placement (currently left of status text, grid layout collapses to single column under 480px), size, border treatment.
3. **Paper-group rules** — currently a thin line trailing each status label. Decide if this reads as structure or noise.
4. **Section headers** — currently `§ STATUS` in mono uppercase. Could push more or less aggressive.
5. **Paper grain background** — a very subtle radial-gradient stipple. Could be removed entirely if it feels gimmicky.
6. **Charter fallback chain** — Charter ships with macOS but not Linux; on Linux it'll fall back to Sitka/Georgia. Decide whether to self-host Charter (a TTF/WOFF is in `fonts/`?) to guarantee.
7. **Wrapped projects** — currently rendered in `--ink-soft` (slightly muted). The `:has()` selector used to apply this isn't supported in older browsers; verify or fall back to explicit classing.

### Deferred (not started)
1. **`/1994.html` easter egg.** Build a standalone 1994-mode page from the preserved `era-1994.css` + `base.css`. Should be statically rendered (no toggle JS), discoverable only via the HTML comment in `index.html` or by guessing the URL. The `T` keystroke mentioned in the comment could either:
   - (a) be a literal lie that only rewards readers who view-source then visit the URL, or
   - (b) be wired up with ~10 lines of JS that navigates to `/1994.html`. Decide.
2. **Cleanup of obsoleted files.** Once `/1994.html` is built and the easter egg works, the leftover `styles/era-2024.css`, `styles/switcher.css`, `app.js` can be deleted. Keep `styles/era-1994.css` and `styles/base.css` if `/1994.html` references them.
3. **Build automation.** Currently `python3 build.py` is manual. Could add:
   - A pre-commit hook that rebuilds on `data/` or `templates/` changes.
   - A GitHub Action that rebuilds on push and commits the result.
   For a site of this size, manual is probably fine. Defer until friction is felt.
4. **README.** The current `README.md` is 48 bytes (basically empty). Worth replacing with the maintenance-workflow snippet from above.

### Open questions for the user
- Self-host Charter, or accept the system-stack fallback chain?
- Keep the paper grain or remove it?
- For the easter egg: keystroke wiring, or pure URL discovery?

---

## Anti-patterns to avoid in future sessions

These came up in the discussion and were ruled out — listing them so they don't re-emerge.

- **Tabbed projects.** The old `index.html` used JS tabs for the four projects. DESIGN.md explicitly rejects this. The new layout stacks them flat.
- **Conventional academic nav** (`About / Research / Publications / Teaching / CV`). Replaced with tilde-separated structural punctuation.
- **Circle-cropped headshot.** Gone. The dithered portrait replaces it.
- **Inter / Roboto / Source Sans.** DESIGN.md flags these as "I didn't think about this." Avoid.
- **Color accent.** Resisted; pure monochrome was the discipline. If an accent is added later, it should carry meaning (a status indicator, a link state) — not be decoration.
- **Generic blue links.** Underlined-ink with hover-inversion is the convention here.

---

*Last updated: 2026-05-10. Resume from "What's still open."*
