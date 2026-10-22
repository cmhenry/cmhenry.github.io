# Literature review — presenter notes

Target: 30 minutes. Compare search procedures without predetermining which gives the best result. This is a discovery exercise, not a systematic review.

## Before the session

- Prepare `openalex-lit-review.md` and `content-moderation-sources.md` in an interface that can retrieve OpenAlex records.
- Confirm credentials through the approved secret-handling route. Do not print credentials, read a secret file into the chat transcript, or project a URL containing a key. Check current service terms rather than quoting a fixed quota.
- Fix the topic, model, available tools, date window, ordering, and page limit. Translate “last six months” into explicit start and end dates once; reuse them in all passes.
- Rehearse the requests and retain sanitized query receipts and responses. This revision does not supply a newly rehearsed model run or a cached live response.

## Slides 1–4: ordinary request and inspection

Run the exact ordinary request on slide 3 in a fresh conversation. Record the interface, model, date, and enabled tools. Do not engineer a failure. If the answer is useful, inspect and retain that success.

Check a cited work's title, author, date, and identifier against the original source. Then inspect whether the source supports the attributed claim. A real DOI does not verify a summary. Missing full text means claim support remains unverified.

## Slides 5–8: instructions and scope

A skill is reusable instructions. It does not create network access or guarantee compliance. The slide shows an excerpt; the linked markdown file is the complete retrieval request.

The three source IDs and two author IDs in the slides and reference document were checked against OpenAlex during this revision. Resolve newly added names before filtering. Venue lists define coverage, not a universal quality ranking.

## Slides 9–11: scoped searches

1. **Recipe:** retrieve one bounded page with the topic and explicit dates. Preserve actual returned records and the matching total separately.
2. **Journals:** add only the source filter. Restricted coverage may exclude important work elsewhere.
3. **Authors:** retain the journal results and run a separate query with the same topic and dates, filtered by author. Combine by union, not journal-and-author intersection. Deduplicate by OpenAlex work ID and preserve query membership.

Do not predict result counts. Zero additions and overlapping results are informative. A truncated first page is not the full matching set. Do not broaden dates to rescue the demonstration without explicitly starting a different comparison.

## Slides 12–14: compare and transfer

Compare citation identity, claim support, coverage, and verification effort. A single run is not a general performance estimate. The ordinary query can outperform the configured route for some purposes.

Participants change one scope decision, predict its effect, run it if retrieval is available, and explain one omission. A chat-only participant can inspect the scope document and audit an accessible source without claiming to have executed the API search.

## Outage route

Use a real, dated, sanitized response retained during rehearsal if available. Otherwise inspect the supplied query and source list manually. Say “retrieval not run”; do not fabricate citations. Keep source-identity verification separate from full-text claim checking.
