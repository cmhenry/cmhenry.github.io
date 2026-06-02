---
name: openalex-lit-review
description: Search OpenAlex for recent scholarly works on a topic, with optional filtering by journal and author. Use when the user asks for a literature review, recent papers, or to find work on a topic.
---

# OpenAlex Literature Review

This skill helps Claude search [OpenAlex](https://openalex.org) — an open catalog of ~250M scholarly works — and return clean, citable results.

It is deliberately small. It does one thing: take a topic, an optional date range, and optional journal and author scopes, and return a markdown table of real, verifiable works.

---

## Before searching

1. Read the OpenAlex API key from a `.env` file in the project folder. Look for a line like `OPENALEX_API_KEY=...`. If `.env` is missing or the key is empty, stop and ask the user to add it.
2. If the user references a canonical sources doc (typically a file like `*-sources.md`), read it. It contains OpenAlex journal IDs (start with `S`) and author IDs (start with `A`).

---

## How to build the query

OpenAlex endpoint: `https://api.openalex.org/works`

Always include these parameters:

- `api_key=<KEY>` — the value from `.env`
- `per-page=25` — keep results focused
- `select=id,title,authorships,primary_location,publication_date,doi,abstract_inverted_index,open_access`

### For a topic + date range

- `search=<topic phrase>` — URL-encoded
- `filter=from_publication_date:YYYY-MM-DD` — typically six months before today

### To scope by journal

Add to the `filter` parameter, comma-separated:

- `primary_location.source.id:S123|S456|S789`

Pipe (`|`) is OR. Comma between filter keys is AND.

### To include specific authors regardless of venue

Run a **second** query with author IDs:

- `filter=from_publication_date:YYYY-MM-DD,authorships.author.id:A123|A456`

Then merge with the first query's results. Deduplicate by DOI.

---

## How to return results

Return a single markdown table with these columns: **Author(s)**, **Title**, **Venue**, **Date**, **DOI**.

If `abstract_inverted_index` is present in the response, reconstruct the abstract (it's a dictionary of `word → [positions]`; sort by position and join) and include a two-sentence plain-language summary under each row.

Sort results by `publication_date` descending.

---

## What not to do

- Never invent fields. If a paper has no DOI in the response, write "no DOI" — do not guess one.
- Never silently fall back to model knowledge if the API returns zero results. Tell the user the query was empty and suggest a broader filter.
- Never include the API key in any output shown to the user.
- Never paginate past page 4 without asking. If there are more results, summarize the count and ask whether to continue.

---

## Minimal example

If the user says: *"Find content moderation work from the last 6 months in the journals listed in `content-moderation-sources.md`"* —

1. Read `content-moderation-sources.md`, extract source IDs.
2. Compute the date six months ago.
3. Build:
   ```
   https://api.openalex.org/works
     ?api_key=KEY
     &per-page=25
     &select=id,title,authorships,primary_location,publication_date,doi,abstract_inverted_index,open_access
     &search=content%20moderation
     &filter=from_publication_date:2025-12-01,primary_location.source.id:S4210204868|S125754415|S2764455111
   ```
4. Render the table.
