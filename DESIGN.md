# Design Specification: Personal Academic Website
### Distilled from a curated collection of notable personal sites

---

## Preamble: What This Taste Is, Actually

The sites in this collection don't share a visual style so much as a *set of values*. Cataloguing them reveals a consistent anti-convention stance: every entry refuses the default form for its genre (portfolio, personal page, syllabus, corporate site) and replaces it with something that has a strong, deliberate point of view. The operative aesthetic categories are:

1. **Print/editorial lineage** — feels typeset, not designed; owes more to zines and small-press than to Dribbble
2. **Performs its subject** — the form of the site embodies what it's about, not just what it says
3. **Constraint as craft** — minimal or zero JS treated not as limitation but as precision
4. **Structural elements as decoration** — horizontal rules, tildes, em-dashes, whitespace do the visual work that other sites give to UI widgets
5. **Small institution** — quietly does the work of a publisher or curator without being one; the site *is* the scholarly presence, not a marketing page for it

A standard academic website template (two-column CV layout, Bootstrap theme, blue links on white, profile photo in a circle) violates all five. This document specifies how to build something that honors all five.

---

## Referent Sites

### Primary References

**[ashleyblewer.com](https://ashleyblewer.com/)**
The closest single referent for the target aesthetic. A static index page that reads like a typewritten zine page — her name split across two massive display lines flanked by `---` horizontal rules, the entire layout feeling *printed* rather than designed. No JavaScript. The structural rhythm comes entirely from `<hr>` elements and typographic scale. The page names alone (`throttled.html`, `lando.html`, `how-did-i-get-here.html`) telegraph the sensibility: idiosyncratic, hand-built, unmistakably personal.

*Key extractions*: horizontal rules as primary structural device; name/title as the visual anchor at maximum scale; flat list navigation over hierarchical menus; everything feeling hand-assembled.

**[bits.ashleyblewer.com/halt-and-catch-fire-syllabus/](https://bits.ashleyblewer.com/halt-and-catch-fire-syllabus/classes/01.html)**
Demonstrates "performs its subject": a syllabus about early computing history presented in early-web aesthetic. Tilde-separated navigation (`~ #01 ~ #02 ~ #03 ~`), dithered black-and-white images, animated construction GIF. The costume isn't ironic — it's the argument. For an academic site, the implication is that the form should somehow *be* the scholarship, or at least not contradict it.

*Key extractions*: tilde or punctuation-mark navigation as a design gesture; dithered/high-contrast imagery; the syllabus-as-object that functions as both document and site.

**[mk.gg](https://mk.gg/) (Hypersite)**
A personal site built as a faithful 1990 HyperCard stack recreation — historically accurate fonts (Chicago, Geneva), original Susan Kare icons, essentially zero client-side JS. The point is that strong aesthetic fidelity doesn't require runtime weight. The site demonstrates that picking a specific media-historical reference point and executing it with precision beats a generic "modern" design every time.

*Key extractions*: commit fully to a specific aesthetic lineage; accuracy over approximation; deliberate font choices with historical weight; JS-light is achievable even for complex aesthetics.

### Secondary References

**[nousresearch.com](https://nousresearch.com/)**
Terminal/generative aesthetic where the UI *behaves* like it's running something — `OUTPUT 96 / SEED: 3573860127` as section metadata, alternating hero copy like a reloading model. This is the "performs its subject" principle applied to an AI research organization. The lesson for an academic site: a researcher's site could subtly reflect their methods or subject matter in its form.

*Key extractions*: metadata-as-design (dates, identifiers, provenance information rendered as visual elements); monochrome with a single accent color; structural metadata visible at the surface.

**[hypertext.tv](https://hypertext.tv/)**
A broadcast television simulator for indie web content — scheduled programming, no on-demand, no algorithm. Anti-streaming as thesis. Relevant less for its specific aesthetic than for its *editorial stance*: a strong organizing principle (broadcast, not feed) that shapes every design decision. The lesson: a personal site should have a thesis about what it *is*, not just display information.

*Key extractions*: the site's form embodies an argument; editorial curation over algorithmic neutrality; strong genre commitment executed with fidelity.

---

## Core Design Principles

### 1. Typography Does All the Work
No hero images, no decorative photography, no background textures. The typographic hierarchy *is* the layout. Use a maximum of two typefaces: one for display/headings (characterful, perhaps with historical associations), one for body/running text (legible, with some personality). Both should feel like they were chosen with intention.

**Suggested directions** (pick one and commit):
- A **bitmap or early-Mac-adjacent serif** for headings (something in the tradition of Charter, or an academic serif like Freight Text) paired with a **technical monospace** for metadata, dates, page labels
- A **grotesque with unusual weight distribution** (something like Dharma Gothic, or an older grotesque revival like Franklin Gothic) used at scale for the name/title, with a clean readable serif for body
- **All-monospace** if the subject matter warrants it — everything in a well-chosen mono creates a document/terminal feeling that reads as principled rather than lazy

Whatever is chosen: set the name/title at a size that feels almost uncomfortably large. The Blewer move — splitting the name across two lines at display scale, flanked by horizontal rules — is the right instinct.

### 2. Horizontal Rules as Structure
Use `<hr>` or CSS border-based rules as the primary structural element. Not as decoration between sections — as the thing *holding* the sections together. The rhythm of rule → content → rule → content is the layout. This is the zine/print-editorial inheritance.

Variations: a thick rule above the name and a thin rule below; rules that extend full-width while content is constrained; using `---` or `* * *` in visible text as typographic markers rather than rendered rules.

### 3. Severe Palette Constraint
Maximum two colors. The default stance should be **black and white with one accent**, or pure monochrome. This isn't minimalism for minimalism's sake — it's that every site in the collection that uses color uses it sparingly enough that the color carries meaning. A link hover color, a date label, a section marker — these are the interventions.

Avoid: gradients, drop shadows, glassmorphism, blue as a neutral, colored backgrounds behind text blocks.

### 4. Metadata Visible at the Surface
Dates, DOIs, version numbers, file sizes, word counts — whatever provenance or structural information exists about the content, surface it as a design element rather than hiding it in hover states or tooltips. This is the Nous Research lesson: `OUTPUT 96 / SEED: 3573860127` is a design choice, not a debug artifact.

Applied to an academic site: publication years rendered as oversized numerals, citation counts as labels, draft status visible. The metadata *is* the design.

### 5. Navigation as Structural Punctuation
Avoid conventional nav bars, dropdown menus, hamburger menus, sidebar navigation. Instead: navigation that reads like table of contents entries, or like the tilde-separated markers on the HCF syllabus. A horizontal sequence of short labels separated by `·` or `—` or `~`. Or a flat bulleted list in the footer. The navigation should feel like it belongs to the document rather than to the chrome around it.

### 6. Zero or Near-Zero JavaScript
Not a hard rule, but the gravitational pull of the collection is strongly toward static HTML/CSS. If JavaScript is used, it should be for something that genuinely can't be done in CSS (a theme toggle, a search index, a generated-on-the-fly CV download). Decorative JS — parallax, cursor followers, scroll animations — is out of register with this aesthetic entirely.

### 7. The Site Has a Thesis
The hardest thing to hand to a code tool, but the most important: the site should have a point of view about *what it is*. Not "here is my information" but "here is how I understand a personal academic site to function." The HCF syllabus is a small institution. Ashleyblewer.com is a zine-maker's index. Hypersite is a media archaeology artifact.

For an academic personal site, some possible theses:
- *The site as working document* — everything is a draft, timestamps visible, "last updated" prominent
- *The site as syllabus* — organized around what you're teaching and reading, not just what you've published
- *The site as index* — a flat list of everything, navigable by date or tag, with no hierarchy beyond that
- *The site as small press* — the publications are the center; everything else is supporting apparatus

---

## What to Avoid

These are not aesthetic preferences — they are failures of nerve that this collection consistently rejects:

- **Academic template aesthetics**: the two-column CV layout, the Bootstrap/WordPress Academia theme, the circle-cropped headshot, the "Research / Publications / Teaching / CV" tab structure
- **Portfolio conventions**: project cards with cover images, hover-revealed descriptions, "featured work" sections
- **Performative minimalism**: white space used to signal sophistication rather than to serve the typography
- **Generic type choices**: Inter, Roboto, Lato, Source Sans, or any font that says "I didn't think about this"
- **Neutral professionalism**: the site that could belong to anyone; the site that is afraid of being remembered

---

## Implementation Notes for Claude Code

- **Stack**: Static HTML + CSS is the first choice. If a framework is needed, Astro (zero-JS by default) is appropriate — notably, both mk.gg and hypertext.tv use it.
- **Fonts**: Load via Google Fonts or self-host; do not use system fonts as a substitute for a deliberate type choice.
- **CSS variables**: Use them for the entire palette and type scale from the start; makes the "severe constraint" approach easy to enforce.
- **File naming**: Consider the Blewer move of giving pages idiosyncratic, specific names rather than generic slugs (`/writing` instead of `/blog`, `/working-on` instead of `/projects`).
- **Responsive**: The typographic/print approach scales well — a single column layout with careful type sizing is naturally responsive. Avoid responsive breakpoints that radically change the layout; the print sensibility should hold at all sizes.
- **Accessibility**: High-contrast monochrome palettes are typically excellent for accessibility. Use semantic HTML throughout — the document structure *is* the design.

---

*This document was assembled from a curated collection of notable personal sites maintained as a side project. The referent links are live as of May 2026.*
