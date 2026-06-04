# Task: Literature Review — Presenter Notes

**Target time:** ~30 minutes
**Goal of this module:** Make the contrast between a chatbot prompt and a configured workflow concrete. By the end, every person in the room should understand that a "skill + reference doc + real API" is a small, learnable thing — not a software project.

---

## Slide 1 — Title: "Literature Review"

Brief. Set up the running example.

> "We're going to do the same task four times. Each time we'll add one piece. Watch what each piece fixes."

---

## Slide 2 — A familiar request

The framing slide. Don't oversell.

- Content moderation, last 6 months — chosen because (a) the field genuinely is moving fast, (b) it's broad enough that several people in the room have a stake, (c) there's a clean answer for what "good" looks like.
- Substitute a different topic if the room's interests are visibly elsewhere — the structure transfers.
- Resist the urge to explain the four passes here. Just say "we'll add a piece each time."

---

## Slide 3 — Pass 0: Just ask the chatbot

**Do this live.** Open Claude Desktop. Paste the prompt verbatim. Let it run.

- Don't pre-edit the prompt. Don't add "with citations from the last 6 months only." The whole point is that the naive ask doesn't include any of that.
- While it runs, narrate: "This is what most people do. This is what most people will do tomorrow."
- If the output is surprisingly good — happens occasionally — pick one citation and ask: "Where did this come from? When was it published? Can I find the DOI?" The answer is almost always vague.

If the demo is offline / API key issues, fall back to a pre-recorded screenshot of a chatbot output with three plausible-looking citations and walk through what's wrong with each.

---

## Slide 4 — Likely failure modes

Walk these slowly. Each one motivates a piece we add later.

- **Stale.** Models don't know "the last 6 months." Even if the knowledge cutoff is recent, the training data isn't indexed by date for retrieval — it's diffused into weights.
- **Fabricated.** The classic hallucinated-citation problem. Plausible author + plausible journal + made-up paper or wrong DOI. Reviewer Two will catch this.
- **Unscoped.** No way to say "from journals I trust." The chatbot has no notion of your field's venue hierarchy.
- **Unverifiable.** This is the real one for academics. Every step has to be reconstructible by someone else. The chatbot can't show its work.

> "These are not bugs. This is the chatbot working exactly as designed. The chatbot is the wrong tool."

---

## Slide 5 — The plan: building a skill

Preview, don't explain. We'll spend a slide on each.

- 1 · Real index → OpenAlex
- 2 · Custom skill → query recipe
- 3 · Canonical doc → your taste, written down

Possible aside: *"You're going to feel like this is a lot of files. It is. That's the point — every file is a place a reviewer (or future you) can audit."*

---

## Slide 6 — Piece 1: OpenAlex

The factual slide. Hit the numbers cleanly.

- [openalex.org](https://openalex.org) — open replacement for Scopus / Web of Science. ~250M works. CC0 license. Started as an offshoot of Unpaywall.
- **Free tier specifics** (as of June 2026):
  - Sign up at [openalex.org/settings/api](https://openalex.org/settings/api). 30 seconds, no credit card.
  - Free key gives **$1/day of usage**.
  - Per their pricing table: that's roughly **1,000 search calls** OR **10,000 list+filter calls** OR unlimited single-entity (DOI) lookups OR 100 full-text downloads per day.
  - You can mix. A typical lit review for one topic spends pennies.
  - Higher-volume plans exist for institutions doing bulk work — not relevant for the workshop.
- Authentication is a single query parameter: `?api_key=YOUR_KEY` appended to every request.
- If anyone asks: there's also a free bulk snapshot (CC0, quarterly), and paid tiers ($/month) for higher API limits and daily change files. None of that matters for a lit review.

> "$1 a day is a lot. You'd have to be running a thousand searches before lunch to notice."

---

## Slide 7 — Piece 2: The skill

The "what is a skill" moment. Many people in the room have not heard the word `skill` used this way.

- A **skill** is a markdown file with frontmatter (`name`, `description`) and a body. Claude reads the description; if the user's prompt looks relevant, Claude loads the body and follows it.
- Not a plugin, not a library, not code. Just a file.
- Triggers on natural language — phrases in the prompt that match the description.
- The body teaches Claude the *recipe*: which endpoint, which filters, how to interpret the JSON that comes back, what to do if a field is missing.

### How the skill "installs" in Cowork

This is the question that always comes up. Be ready with the concrete answer.

- Skills live in `~/.claude/skills/<skill-name>/SKILL.md` (user-scoped) or in a project's `.claude/skills/` directory (project-scoped).
- Cowork picks them up automatically — no install command, no restart. Drop the folder in, start a new conversation, the skill is available.
- For the workshop: I'll distribute a `workshop-skills` folder. Audience members copy `openalex-lit-review/` into `~/.claude/skills/`. That's the install.
- Alternative path: package as a `.plugin` and install via Cowork's plugin UI. Same end state. More overhead for a one-skill use case.

### How the API key gets to the skill

Important: **the API key does NOT live in the SKILL.md file.** SKILL.md is shareable, version-controllable, and probably ends up in a repo eventually. Keys do not belong there.

Three workable patterns — recommend the first for the workshop:

1. **Project `.env` file** (recommended).
   - In the connected folder, create `.env` with `OPENALEX_API_KEY=...`.
   - `.gitignore` it.
   - SKILL.md tells Claude: "Before making any request, read `.env` and use the value of `OPENALEX_API_KEY` as the `api_key` parameter."
   - Portable, explicit, easy to swap.

2. **Home-directory key file.**
   - `~/.openalex-key` containing just the key.
   - SKILL.md tells Claude to `cat ~/.openalex-key` before each call.
   - Survives folder switches; less explicit.

3. **Shell environment variable.**
   - `export OPENALEX_API_KEY=...` in `~/.zshrc`.
   - Only works if Cowork inherits the shell environment (it does for bash tool calls).
   - Most "system-engineery" of the three.

> "Yes, three options. No, you don't have to pick. I'll show you one and you'll be fine."

---

## Slide 8 — Piece 3: Canonical reference doc

The least-software-engineery slide. This is the one that lands hardest with academics.

- It's just a markdown list of journals and authors with OpenAlex IDs. That's it.
- Why IDs and not names? OpenAlex IDs are stable; journal name strings are not. "Political Communication" disambiguates to a specific source ID.
- How to find the ID: search at [openalex.org](https://openalex.org) for the journal or author, open the result, copy the ID from the URL (or use the OpenAlex autocomplete API — but for the workshop, the web UI is fine).
- The doc is **editable**. As the field moves, you edit the file. The skill always reads it fresh.
- The IDs in the slide example are illustrative — verify before the live demo. (`S4210204868` = Journal of Politics, `S125754415` = Nature Communications, `S2764455111` = Political Communication, `A5043469610` = Karsten Donnay, `A5008582293` = Fabrizio Gilardi — confirm at openalex.org/works ahead of the workshop.)

The bigger point — say it explicitly:

> "Most of what makes an academic a domain expert is taste. Taste about which journals matter, which authors matter, which methods matter. This file is your taste, written down. The skill executes against it."

---

## Slide 9 — Pass 1: Skill only

Run live. Keep narration tight.

- Prompt is exactly what's on the slide.
- Expect: a clean list of works on content moderation, real DOIs, dates within the last 6 months. Could be 20–50 results.
- Skim the results live. Point out: a real venue you recognize, a venue you don't recognize, maybe a preprint, maybe something in a publication that exists but isn't where you'd look first.
- That's the lesson — the universe just got real, but it's still the *whole* universe.

> "This is better than Pass 0 by an enormous margin. It's also still not what we want."

---

## Slide 10 — Pass 2: + journals

Run live.

- Same prompt with the reference doc added.
- Expect: a much shorter list. Probably 3–10 works, all from the three named journals.
- Walk through the result alongside Pass 1's output. The contrast is the lesson.
- Acknowledge the trade-off: if there's a great piece in *American Political Science Review* on this topic, you missed it. The fix is to add APSR to the doc. Edit the doc, re-run, see the change.

---

## Slide 11 — Pass 3: + authors

Run live.

- Same prompt with authors added.
- Expect: the Pass 2 results, plus any recent Donnay or Gilardi work in any venue — likely some working papers, possibly a special issue, possibly something in a journal not on the list.
- This is where to land the "research-front sensor" idea. The doc is no longer a filter — it's a feed.

> "You can run this once a week. The doc is the configuration. The skill is the engine. You own both."

---

## Slide 12 — Reading the passes

Recap slide. Brisk.

- Pass 0 → fabrication.
- + skill → real, no scope.
- + journals → venue scope.
- + authors → venue scope plus watch-list.

The deeper point: **every decision in the workflow lives in a file.** You can show a reviewer the skill, the doc, the prompt, the output. Full provenance.

---

## Slide 13 — Takeaways

The transferable pieces. Say them slowly.

- A skill is a reusable recipe. Write the OpenAlex one today; reuse it forever.
- A canonical doc is taste, written down. The doc is a research artifact in its own right.
- The chat box is the wrong tool for anything you'd cite. Repeat this verbatim — it's the line that sticks.
- The pattern transfers. ArXiv, SSRN, ICPSR, court filings, FOIA archives — anywhere there's an API and a notion of "the venues / sources I trust," this same pattern works.

---

## Slide 14 — Async exercise

Set expectations.

- ~30 minutes if they're focused. Possibly more if they get nerd-sniped by the OpenAlex IDs.
- They need: a Cowork install, an OpenAlex key, the workshop materials folder (skill + sample sources.md).
- The deliverable is one paragraph. Not a polished writeup. Just: what surprised you.
- I'll collect the responses and bring trends back at a follow-up session.

> "If the only thing you take from this workshop is the muscle to do this once, on a topic you actually care about — that's enough."

---

## Things to watch for during this module

- **Don't skip Pass 0.** The whole rest of the module reads as theater if the audience doesn't feel the failure. If you're tempted to skip because "obviously you wouldn't really do this" — remember most of the room *would* really do this.
- **Don't apologize for the scaffolding.** Three files feels like a lot until you contrast it with the one file (the SKILL.md) you'll reuse for the next ten lit reviews.
- **Be ready for "couldn't I just have Claude Google it?"** Answer: web search is unscoped, rate-limited, not deduplicated, and produces results from blog posts and content farms next to journals. OpenAlex is the index academics actually need.
- **Be ready for "what about Google Scholar?"** Answer: no API, ToS prohibits scraping, no programmatic access. OpenAlex was built specifically because Scholar isn't open.
- **Have a backup.** If the API is down or the key isn't working live, have cached outputs for Pass 1 and Pass 3 ready as text files you can `cat` and walk through.
- **Watch the clock.** If you're at 25 minutes and haven't finished Pass 3, cut the live execution and walk through cached output for Passes 2 and 3 side-by-side. Don't drop the takeaways slide.
- **Don't oversell the API key step.** It's two minutes of friction. If someone hasn't signed up by the time the demo runs, they can pair with a neighbor.
