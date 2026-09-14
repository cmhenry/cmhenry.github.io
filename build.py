#!/usr/bin/env python3
"""Build index.html from data/*.yaml + templates/index.html.jinja."""

from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).parent
DATA = ROOT / "data"
TEMPLATES = ROOT / "templates"

STATUS_LABELS = {
    "published":    "published",
    "r-and-r":      "r & r",
    "under-review": "under review",
    "working-paper":"working paper",
    "draft":        "draft",
    "active":       "active",
    "wrapped":      "wrapped",
}

# display order for paper status groups
PAPER_STATUS_ORDER = [
    "published",
    "r-and-r",
    "under-review",
    "working-paper",
    "draft",
]

# display order for projects within their section
PROJECT_STATUS_ORDER = ["active", "wrapped"]


def load(name):
    return yaml.safe_load((DATA / name).read_text()) or []


# the grid layout splits papers into two cells
PAPERS_OUT = ["published", "r-and-r", "under-review"]
PAPERS_WIP = ["working-paper", "draft"]


def label_papers(papers):
    for p in papers:
        s = p.get("status", "draft")
        p["status_label"] = STATUS_LABELS.get(s, s)
    return papers


def split_papers(papers):
    """Return (out, wip): papers that are out in the world, and papers that aren't."""
    rank = {s: i for i, s in enumerate(PAPER_STATUS_ORDER)}
    key = lambda p: rank.get(p.get("status", "draft"), 99)
    out = sorted((p for p in papers if p.get("status") in PAPERS_OUT), key=key)
    wip = sorted((p for p in papers if p.get("status") in PAPERS_WIP), key=key)
    return out, wip


def sort_projects(projects):
    for p in projects:
        s = p.get("status", "active")
        p["status_label"] = STATUS_LABELS.get(s, s)
    order = {s: i for i, s in enumerate(PROJECT_STATUS_ORDER)}
    return sorted(projects, key=lambda p: order.get(p.get("status", "active"), 99))


def main():
    meta = yaml.safe_load((DATA / "meta.yaml").read_text())
    papers = load("papers.yaml")
    projects = load("projects.yaml")
    links = load("links.yaml")
    also = load("also.yaml")
    papers_out, papers_wip = split_papers(label_papers(papers))

    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("index.html.jinja")
    rendered = template.render(
        meta=meta,
        papers_out=papers_out,
        papers_wip=papers_wip,
        projects=sort_projects(projects),
        links=links,
        also=also,
    )
    out = ROOT / "index.html"
    out.write_text(rendered)
    print(f"wrote {out.relative_to(ROOT)}  ({len(rendered):,} bytes)")


if __name__ == "__main__":
    main()
