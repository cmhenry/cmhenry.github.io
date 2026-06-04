# What kind of tools are out there? — Presenter Notes

**Audience:** political science postdocs and faculty, mostly tool-curious but not tool-saturated.
**Goal:** install a working map of the AI tool landscape so the rest of the workshop has somewhere to stand.
**Posture:** orientation, not pitch. No vendor enthusiasm. Move briskly.
**Target time:** 15–18 minutes total. ~1 min/slide, longer on Cowork and Claude Code, shorter on category openers.

---

## Slide 1 — Title

Just name the module and move on.

> "Before we touch a tool, a quick map of what tools even exist. Otherwise the next two hours will feel like brand soup."

---

## Slide 2 — The landscape

The three-bucket frame is the whole module. If they leave with nothing else, they leave with this.

- Desktop apps — a chat window, sometimes with file access bolted on.
- Harnesses — a CLI loop that touches files and runs commands.
- Agentic systems — long-running, autonomous, you walk away.
- Underlying models are mostly the same. The *interface* is what changes the workflow.

Don't editorialize about which is "best". They have different jobs.

---

## Slide 3 — What actually differs

Three axes — name them, don't belabor them.

- **Autonomy** — how many steps without you.
- **Access** — what it can read, write, run.
- **Latency** — seconds vs. minutes vs. hours.

> "Most of the confusion about 'is AI good at X yet' goes away once you ask which of these three knobs you actually need."

If short on time: skip this slide. The categories carry the same idea.

---

## Slide 4 — Desktop apps opener

A beat. Section divider. Skip if running tight.

---

## Slide 5 — Chat + Projects

The thing everyone has touched.

- ChatGPT, Claude.ai, Gemini — same shape.
- Projects = a persistent system prompt + a small file store.
- It cannot reach into your filesystem. You paste, you copy out.
- Honest about what it's good at: drafting, brainstorming, asking dumb questions, reading something you pasted.
- The ceiling: if your answer needs to *be* a file in your project, the chat window is the wrong shape.

---

## Slide 6 — Cowork

The one they're literally watching right now.

- Same chat interface, but bound to a folder on your machine.
- Read, write, edit, run code in a sandbox. MCP connectors plug in external services.
- Wave at the screen — "this entire workshop site was built in here."
- Distinguish from Chat+Projects: Projects can see uploaded files. Cowork can *change* files on your disk.

> "If the deliverable is a file — a script, a doc, a dataset — Cowork is the cheapest path."

This is the slide where you can pause and field a question. They'll have one.

---

## Slide 7 — Scheduled · Dispatch

The often-missed features. Surface them.

- Scheduled tasks: cron for prompts. "Every Monday morning, summarize what landed in my inbox from PhD students."
- Dispatch: fire-and-forget long jobs. The conversation runs without you watching.
- These exist in Claude's desktop app today; the equivalents are appearing elsewhere.
- Right when you'd reach for one: recurring digests, slow batch work, anything where iteration speed doesn't matter.

> "If a task feels like it should be a script but you don't want to write a script — schedule it."

---

## Slide 8 — Harnesses opener

Beat. Brief.

---

## Slide 9 — What's a harness?

The key concept of the section. Land this.

- A CLI that runs the agentic loop: think, act, observe, repeat.
- "Act" = real shell access, file edits, web calls, subagents.
- You are *watching* the loop. You can interrupt, redirect, approve.
- Born in coding workflows because code lives in files — but anything that lives in files works.

> "If Cowork is a chat that happens to touch files, a harness is a file-toucher that happens to chat."

That line earns its keep. Use it.

---

## Slide 10 — Claude Code

Spend a beat here — and **actually show it**. Drop out of the deck, open a terminal, run `claude` in some throwaway directory, type one prompt. Even 30 seconds of watching the loop run lands the concept harder than the slide does.

- Terminal app. `cd` into a directory, type one command, you're in.
- Tools: bash, file edits, web fetch, subagents, MCP, custom skills.
- Parallel worktrees: spin up several instances on copies of the repo, compare results.
- For political scientists: think of it as the same tool Stata users have for managing analysis directories — but the assistant can actually edit the .do files.
- Same engine as Cowork. The CLI gives you more visibility into the loop and more control over each step.

We're *not* using Claude Code for today's hands-on tasks — everything we run is in Cowork — but this is the tool to graduate to once a workflow stabilizes.

---

## Slide 11 — Codex

Short.

- OpenAI's harness. Same shape — terminal, files, loop.
- Different model, different defaults, different rough edges.
- Useful for cross-checking: run the same task in both, see where they disagree.
- The category is converging. Skills you build in one tend to port.

---

## Slide 12 — Open source harnesses

The privacy/reproducibility escape hatch.

- aider, opencode, Cline, Continue, and a long tail.
- Bring your own model — including local open-weight models via Ollama, vLLM, llama.cpp.
- Trade-off: less polish, less integration, more control over the loop.
- Why a researcher might care:
  - **Privacy** — keep sensitive data off vendor servers.
  - **Reproducibility** — pin to a specific open model checkpoint that won't change under you.
  - **Cost** — at scale, local inference can be cheaper than API calls.

> "If you have data you can't ship to a vendor, this is the bucket you live in."

---

## Slide 13 — Agentic systems opener

Beat.

---

## Slide 14 — What's an agentic system?

The thing most journalists mean when they say "AI agents" today.

- Same loop as a harness — but you don't watch.
- Runs in the cloud, often hours. Has a browser. Has a virtual machine. Has broad tool access.
- Your job changes: from operator to reviewer.
- Risk profile changes too: a bad step in a chat is a wasted minute; a bad step in an agentic system is a wasted afternoon — or worse, an action you didn't authorize.

Flag the "you're reviewing what it did" framing. That's the right posture for using these.

---

## Slide 15 — The players

Brisk roll call. Don't get drawn into "which is best".

- OpenClaw — Anthropic's. Browser + VM + long-running agentic tasks.
- Hermes — independent agentic system, not affiliated with the big three labs. Worth knowing as a marker that this category isn't only owned by the model vendors.
- Gemini Spark — Google's, with Workspace/Search integration.

**Show Hermes here.** Drop out of the deck for ~1 min — open it up, point at the dashboard, kick off a trivial task. Pair it with the Claude Code demo two slides back: those two are the "live look" of the module. The contrast (a CLI loop you're watching vs. a hosted agent you've handed off) makes the harness-vs-agentic distinction tangible in a way the slides can't.

All three are early, expensive, and changing fast. Names will be different in six months. The *shape* won't.

> "I'm naming these so you recognize them when they show up in a talk. Not so you sign up for one tonight."

---

## Slide 16 — When to reach for one

This is the slide that prevents people from misusing agentic systems.

- Multi-hour, fully-scoped work — *not* exploration.
- Steps you could write down but don't want to babysit.
- Verifiable output — you can check it without redoing it.
- Bad fit: anything where your judgement is needed mid-flight, or where you can't tell whether the output is right.

If you sense skepticism here, lean into it. That's the correct response right now.

---

## Slide 17 — Picking one

The one-slide recap. Read it. Move on.

- Thinking with words → chat.
- Producing a file → Cowork.
- Editing a codebase or running scripts → a harness.
- Recurring → schedule it.
- Long-horizon and delegated → an agentic system.

---

## Slide 18 — What we'll use today

Tie the survey back to the workshop.

- Every hands-on task today runs in Cowork. That's the only tool you need installed for the rest of the workshop.
- Everything else on the map — Projects, Dispatch, Claude Code, Codex, OpenClaw, Hermes, Spark — is here so you recognize them later.
- Don't try to learn five tools this afternoon. Pick the one that fits the next thing on your list.

> "The point of this module was the map. The point of the next module is to actually walk somewhere on it."

---

## Pacing

- Target: 15–18 min. ~1 min/slide.
- The slides that earn extra time: **6 (Cowork)**, **9 (What's a harness)**, **10 (Claude Code)**, **16 (when to reach for an agent)**.
- The slides to compress if behind: 3 (Three axes), 4/8/13 (category openers), 17 (recap).
- If anyone asks "which model is best?" — defer. That's a different conversation and not the point here.
- If anyone asks "is this safe to use with sensitive data?" — point them at the open-source slide and at the ethics module.
