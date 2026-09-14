# Handoff — Site Redesign

Session notes for `cmhenry.github.io`. Read `DESIGN.md` first for the aesthetic
principles; this doc captures the decisions already locked in, the current state of
the build, and the open questions.

---

## Thesis (locked)

**Working document × small press, in a geometric frame.**

- *Working document* — status of every paper is on the surface, "last build" is shown,
  the site reads as in-process rather than as marketing.
- *Small press* — publications are the structural center; the site is a pamphlet for
  the work, not a portfolio.
- *Geometric frame* — the masthead and the grid are the visual argument. Structure is
  drawn, not implied by whitespace.

Status taxonomy (used across `papers.yaml` and `projects.yaml`):
`draft | working-paper | under-review | r-and-r | published | active | wrapped`.

---

## Design decisions (locked)

| Decision | Choice | Rationale |
|---|---|---|
| Layout | Two-column `article`: a header of two geometric panels (60%) beside a six-column grid of bordered cells (39%). After ashleyblewer.com. | Replaced the single-column print-editorial layout in Sept 2026. See the revision note in `DESIGN.md`. |
| Masthead | A square panel carrying the name on a -45&deg; diagonal, and a 45&deg;-rotated diamond carrying the role words horizontally. Halftone dot fill over an ink gradient, 1px outline, hard offset shadow, CSS-animated diagonal sweep lines. | The referent's central move. |
| Palette | Monochrome: ink (`#111110`) on warm off-white paper (`#f6f3eb`). Panels are ink-filled with paper-colored dots. No accent color; links invert on hover. | `DESIGN.md` "severe palette constraint." The referent's blue/concrete was deliberately not ported. |
| Type — display | Space Grotesk (name, role words, section headings) | The referent's. Grotesque with enough character to carry the panels. |
| Type — body | Inconsolata | The referent's. Real monospace throughout; the whole page reads as a document. |
| Content density | Compressed to fit the grid. Papers and projects are terse titled links with a bracketed status mark; long summaries live in the YAML but are not rendered. | The grid cells are sized for brevity. Detail belongs in the CV and the linked PDFs. |
| Decoration | Two CSS-only isometric boxes, monochrome, in `#surf` and `#also`. | Drawn, not fetched. Credit to the codepen the referent cites is in the stylesheet. |
| JavaScript | Zero. | `DESIGN.md` "near-zero JS"; the site is fully static. |
| Headshot | Dropped. The panels carry the identity now. | A portrait in a bordered grid cell fought with the panels. `thumbnail2.png` is still in the repo. |
| Visitor counter | Kept, in the colophon cell, alongside `iss. YYYY` and `build YYYY-MM-DD`. | Metadata-as-design. |
| Maintenance | YAML + a small Python build (PyYAML + Jinja2). One `build.py`. Output `index.html` is committed; GitHub Pages serves it directly. | Lightweight is right for a site this size. |

---

## File map

### Generated / authored
```
data/
  meta.yaml         name, roles, tagline, affiliation, email, cv url, short_about,
                    source url, visitor count, last build
  papers.yaml       every paper, with `status`, plus `short` and `mark` for the grid
  projects.yaml     ongoing programs, with `short` and `short_note` for the grid
  links.yaml        the "see also" cell
  also.yaml         pages and PDFs hosted on this site ("also here" cell)

templates/
  index.html.jinja  two geometric panels + the six-column content grid

styles/
  main.css          the whole stylesheet: panels, grid, isometric boxes, responsive

build.py            load yaml, split papers into out/wip, render, write index.html
requirements.txt    PyYAML>=6.0, Jinja2>=3.1
index.html          REGENERATED — do not edit by hand; edit data/ and rebuild
```

### Preserved but unused (scaffolding for the `/1994.html` easter egg)
```
app.js                       (era-toggle JS)
styles/base.css              (shared CSS for both eras)
styles/era-1994.css          (1994-mode styles — extract from here for the easter egg)
styles/era-2024.css          (obsolete)
styles/switcher.css          (obsolete)
index-archive.html           (an earlier version)
thumbnail2.png               (the dithered portrait, no longer placed)
```

---

## The grid

Cells and their column spans, in source order:

| Cell | Columns | Holds |
|---|---|---|
| `#bio` | 1/7 | `short_about` plus a one-line footnote. The only left-aligned cell. |
| `#surf` | 1/3 | Decorative isometric box. |
| `#see-also` | 3/7 | Email and off-site profiles, from `links.yaml`. |
| `#papers` | 1/4 | published, r&r, under review. |
| `#in-progress` | 4/7 | working papers and drafts. |
| `#projects` | 1/4 | `projects.yaml`, compressed. |
| `#also` | 4/7 | `also.yaml`, plus the second isometric box. |
| `#colophon` | 1/7 | Type, stack, page source, build metadata. Flex row, right-aligned. |

To add a cell: give it a `grid-column` in `main.css` next to the others, add it to the
`@media (max-width: 620px)` rule that collapses everything to `1/7`, and put it in the
template in grid order.

---

## Maintenance workflow

```bash
# 1. edit one of the YAML files
vim data/papers.yaml          # e.g., change `status: r-and-r` → `status: published`
                              # keep `short` under ~45 characters — the cells are narrow

# 2. regenerate the static HTML
python3 build.py              # writes index.html

# 3. commit both the data change and the regenerated HTML
git add data/papers.yaml index.html
git commit -m "publication: <paper> moved to published"
```

Preview locally with `python3 -m http.server 8000`.

**Never hand-edit `index.html`** — it's a build artifact. Edit
`templates/index.html.jinja` (structure) or `data/*.yaml` (content).

---

## What's still open

1. **Vertical void on the left.** Below the panels, the header column is empty for
   roughly half the page height. The referent has the same void and it reads as
   deliberate, but a third panel, a rule, or a drop-cap-scale initial could fill it if
   it starts to look like an accident.
2. **The `&` in the tagline** sits directly under the descender of "engineer" inside
   the diamond. Clear at every width tested, but tight.
3. **`short` fields drift from `title` fields.** Nothing enforces that the compressed
   title still names the same paper. A check in `build.py` could warn when they
   diverge past some threshold.
4. **`/1994.html` easter egg.** Still unbuilt. The HTML comment at the top of
   `index.html` still points at it. Either build it from `era-1994.css` + `base.css`,
   or remove the comment.
5. **Cleanup.** Once the easter egg is built or abandoned, `styles/era-2024.css`,
   `styles/switcher.css`, and `app.js` can go.
6. **README.** Still 48 bytes. The maintenance workflow above belongs in it.

---

## Anti-patterns to avoid in future sessions

- **Prose in the grid cells.** The cells are sized for terse lines. A paragraph in one
  blows out the row and the whole grid loses its rhythm. Long-form belongs in the
  YAML's full `summary` fields, or on a linked page.
- **Tabbed projects.** An earlier `index.html` used JS tabs. `DESIGN.md` rejects this.
- **Conventional academic nav** (`About / Research / Publications / Teaching / CV`).
  The grid cells are the navigation.
- **Color accent.** Resisted twice now. If one is ever added it should carry meaning —
  a status indicator, a link state — not decoration.
- **Raster decoration.** The boxes and the paper texture are CSS. Keep it that way.

---

*Last updated: 2026-09-14. Resume from "What's still open."*
