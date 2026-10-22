---
name: openalex-lit-review
description: Retrieve bounded OpenAlex records for a topic and explicit dates, optionally scoped to journals or authors.
---

# OpenAlex literature search

This teaching recipe retrieves candidate records. It is not a systematic-review protocol or evidence that a paper supports a claim.

## Before searching

1. Confirm the interface can make the request. Otherwise say retrieval is unavailable; do not simulate records or a successful call.
2. Use an already configured, approved credential route. The execution environment should supply credentials without displaying them to the model or including them in prompts, screenshots, shared URLs, or receipts. Prefer header authentication when supported. Never ask for a key in chat.
3. Fix `search=content moderation`, explicit start/end dates for the agreed six-month window, `sort=publication_date:desc`, `page=1`, and `per_page=25`. Report these teaching limits and keep them constant across passes.
4. Check that source and author IDs identify the intended entities. Do not guess IDs or correct them silently.

## Requests

Endpoint: `https://api.openalex.org/works`

Common parameters:

- `search=content moderation`
- `filter=from_publication_date:START,to_publication_date:END`
- `sort=publication_date:desc`
- `page=1`
- `per_page=25`
- `select=id,title,authorships,primary_location,publication_date,doi,open_access`

`START` and `END` stand for dates agreed before the run. Do not send them literally. The client must URL-encode the parameters.

**Journal pass:** append `primary_location.source.id:S95650557|S64187185|S27211427` to the filter. Pipe means OR within a field; commas mean AND across fields.

**Author pass:** make a separate request with the same topic and dates and `authorships.author.id:A5057940546|A5046475081`, without the journal filter. Retain journal results and take the union of the returned sets. Adding an author filter to the journal request would instead produce an intersection.

Deduplicate by OpenAlex work ID, including records without a DOI. Preserve query membership. Flag conflicting metadata rather than silently choosing a value. Report actual overlap and additions; do not predict counts.

## Save and report

Retain the sanitized query, filters, sort, page/limit, retrieval time, service matching total, actual returned count, and raw returned records. The matching total is not the number downloaded. State when only a first-page slice was retrieved. Stop at the agreed page; further retrieval requires a new decision.

Return ID, title, authors, venue, publication date, DOI, and supplied landing-page or open-access link. Keep missing values missing. Do not turn metadata into an invented abstract or summary.

An empty response is not an API failure; a failed request is not evidence of zero matches. Do not fall back to model memory as though it were retrieval.

## Verification beyond retrieval

Open a candidate's original source to check identity. Separately inspect relevant text to check claim support. Metadata alone is insufficient. Record inaccessible text as unverified. Index coverage, metadata errors, scope restrictions, and first-page truncation remain limitations.

Authentication reference: <https://help.openalex.org/api/authentication>
