# cmhenry.github.io

A small HTML/CSS academic site inspired by [Ben Recht's homepage](https://people.eecs.berkeley.edu/~brecht/index.html): a dark left navigation, a small portrait, short biography, and plain text-led pages. On phones, navigation moves above the content. No JavaScript, external fonts, or new framework is required.

## Edit and build

The existing `data/*.yaml` files remain the source for publications, projects, contact information, and profile links. Page layout lives in `templates/*.html.jinja`; the redesign uses only `styles/academic.css`. The homepage biography and teaching descriptions live in their templates.

```sh
# Create an isolated build environment (Python, Jinja2, and PyYAML).
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python build.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v
```

Commit the generated `index.html`, `publications.html`, `projects.html`, `teaching.html`, and `contact.html` along with template/data edits: GitHub Pages serves checked-in HTML, not the Python build.

The course, workshop, dissertation page, PDFs, and legacy styles are retained. Only the personal-site pages use the new stylesheet. Older homepage section fragments remain as small links to the corresponding new pages.

## Delivery boundary

This design is isolated on `feat/terse-academic`. The existing Pages workflow deploys only `main`; pushing this feature branch does not deploy the redesign. Merge/deployment remains a separate decision.
