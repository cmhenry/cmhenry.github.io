# Software vs. Research — Presenter Notes

**Audience:** political science postdocs and faculty.
**Goal:** make visible the gap between how LLM tools were built and what research demands of them.
**Posture:** plainspoken, a little sharp. The point isn't to scold the tools — it's to name the assumptions before we start using them.

---

## Slide 1 — Title

Brief. Just frame the move.

> "We've talked about what these things are. Now we talk about what they were *built for* — and why that's not the same as what we use them for."

---

## Slide 2 — The premise

The setup for the whole module. Don't rush.

- LLM tools are products. Anthropic, OpenAI, Google ship them the way they ship every other piece of software.
- That shipping process has a 25-year history. It has values baked in.
- When a political scientist picks up Claude or ChatGPT, they are not just getting a "model" — they are getting a worldview about what *good output* means.
- That worldview is not ours. It wasn't designed against our standards. It was designed against product standards.

> "The dangerous part isn't that the values are different. It's that they're invisible."

---

## Slide 3 — Where it came from

The history beat. Keep it short — context, not a CS lecture.

- Modern software practice converged on a way of working over ~25 years.
- The problem it was solving: how do you coordinate large teams to ship products into uncertain markets?
- Agile, Scrum, MVP, abstraction-as-design — all answers to *that* question.
- "Done" became a pragmatic concept: ships, works, can be improved later.

Punchline: this is good engineering. It is not good epistemology.

---

## Slide 4 — Software says…

Read the four maxims out loud. They should sound familiar — and harmless.

- Move fast, iterate later.
- Abstraction is a feature.
- "Done" = ships and works.
- Optimize for the user's convenience.

Then the line at the bottom is the move:

> "These aren't wrong. They are answers to a specific question. Pause on that. They are not universal goods — they are local maxima for a particular problem."

---

## Slide 5 — Research says…

Same rhythm. Read them. Let the contrast land.

- Get it right, then publish.
- Transparency is an obligation.
- "Done" = withstands scrutiny.
- Optimize for epistemic accountability.

> "Different question, different answers. Neither set is corrupt. They just don't compose."

---

## Slide 6 — The paradigm mismatch

The keystone slide. Walk down the table line by line. Use the rows to land the *kind* of mismatch, not just the existence of it.

- **Move fast vs. get it right.** Speed is a methodological liability in our field, not a virtue.
- **Abstraction vs. transparency.** A "magic" tool is exactly the wrong kind of tool to put in a methods section.
- **Ships and works vs. withstands scrutiny.** Different standards of "finished" — and the chatbot will always tell you it's finished.
- **Docs explain how vs. why you should believe.** API docs tell you how to call something. A methods section tells you why to trust it.
- **Convenience vs. accountability.** Convenience pushes friction off the user. In research, that friction *is* the work.

This is the slide to slow down on. If anyone is going to remember one thing from the module, it should be this.

---

## Slide 7 — Where it bites

Make the abstract concrete. Examples they'll recognize from their own use.

- **Confident prose.** RLHF rewards confidence — it ranks higher with raters. In a journal review, confident wrong is the worst possible failure mode.
- **Abstraction hiding provenance.** ChatGPT giving you a polished paragraph with no citations isn't a bug; it's the abstraction layer doing exactly its job.
- **"Done" in chat.** The session ends when an answer arrives — not when it's been checked.
- **Convenience moves friction.** It feels great. The cost shows up later: in the peer review, in the replication file, in the colleague who can't reconstruct what you did.

Optional anecdote: a story where a student leaned on the abstraction and got caught by a reviewer.

---

## Slide 8 — The trap

The emotional beat. This is the one the audience needs to feel, not just understand.

- The interface is engineered to feel productive. That feeling is the product.
- A tool that *feels finished* trains you to *call things finished* sooner.
- You don't notice you're operating to the tool's standard instead of yours — until someone external (reviewer, editor, colleague) checks.
- "Move fast, iterate later" maps onto a dissertation timeline as "publish first, retract later". That's the disciplinary cost.

> "These tools are perfectly aligned with the values of the people who made them. The question is whether those are *your* values."

---

## Slide 9 — What we need instead

Pivot from diagnosis to criteria. Brisk.

- **Traceability** — every claim back to a source. No floating assertions.
- **Auditability** — someone else can follow the trail. The methods section is the test.
- **Reproducibility** — re-run the workflow and the result holds up to scrutiny again.
- **Transparency** — record the prompt, the tool, the model name, the version, the date. All of it.

These aren't tool features. They're disciplines we impose *on top of* the tool.

---

## Slide 10 — Looking ahead

Tee up the rest of the workshop.

- Every tool in the next two hours gets scored against those four criteria.
- A few of them clear the bar by default. Most clear it only with deliberate effort.
- That effort is not overhead — it's the methods section.
- The thing we're practicing today: noticing the moment the tool's convenience starts to cost you your standards. Once you can name it, you can resist it.

> "The rest of the workshop is just this slide, applied."

---

## Pacing

- Target ~20–24 minutes total. Slides 6 (the table) and 8 (the trap) deserve the most time. Slides 3 and 4 can move quickly — they're scaffolding.
- If you're behind: compress slides 4 and 5 into a single reading of the two lists, side by side.
- If anyone says "but the tools are getting better" — agree, then redirect: better at *their* objective, which is not ours. The mismatch is structural, not a current-generation problem.
- The exit takeaway: the four criteria on slide 9. If the audience leaves with those words, the module has done its job.
