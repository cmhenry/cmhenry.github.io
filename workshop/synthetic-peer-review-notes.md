# Synthetic Peer Review — Presenter Notes

**Target time:** ~25–30 minutes (longest task module of the three)
**Audience:** political science postdocs and faculty. Most have used Claude Desktop chat; few have written a skill file.
**Goal:** teach the *anatomy* of a complex skill — frontmatter, role, rubric, gate — by building one that can plausibly act as Reviewer Two.
**Posture:** the chatbot will flatter you. The skill is how you stop it.

---

## Slide 1 — Title

Brief. Just announce.

> "This is the second of three task modules. We're going to write a skill — a real, complex one — that does synthetic peer review on a draft."

If anyone is fuzzy on what a "skill" is from the literature-review module, reassure them: we'll re-anchor on slide 5.

---

## Slide 2 — The task: Reviewer Two, on demand

Set the stakes.

- Everyone in this room has had a draft they were nervous about. Everyone has wished for an honest pre-read.
- The promise of a chatbot: paste, ask, get critique.
- The reality of a chatbot: paste, ask, get praise.
- Today we close that gap — not by changing models, but by writing a file that constrains what the model is allowed to say.

> "By the end of this module you'll have built a skill that can refuse to bless your paper. That's the move."

---

## Slide 3 — Pass 0: just ask

Live or hypothetical demo, either works.

- Show the prompt. Ideally do it live on screen with a real draft (a published paper of yours is fine — they can't embarrass you about it).
- Resist the urge to engineer the prompt. The point is to expose the floor.

> "The chatbot's default reviewer is hired by the author."

---

## Slide 4 — What you get back: the praise sandwich

Walk the four bullets, slowly.

- **Flattery first.** RLHF taught the model that helpful-sounding answers rate higher. A draft is a vulnerable artifact; the model softens.
- **Vague middle.** "Consider clarifying the framing" — the model's hedge of last resort. Useless because unactionable.
- **No teeth.** Nothing about your IV. Nothing about how you keep slipping from "associated with" to "drives" between sentences 3 and 4.
- **No role, no rubric, no exit criteria.** The model has nothing to compare your draft *to* — no standard, no list of dimensions, no way to refuse.

The punchline at the bottom of the slide — *"RLHF rewards sounding helpful. Helpful ≠ rigorous."* — is the through-line for the rest of the module. Land it.

> "If you tell the model nothing about what good looks like, it falls back to what sounds good. We're going to tell it what good looks like."

---

## Slide 5 — What a skill is

Anchor slide. Some people will not have written one before.

- A skill is a markdown file with **YAML frontmatter at the top** and instructions below.
- `name` is the handle. `description` is what triggers it — Claude reads descriptions to decide whether to load the skill.
- The body is whatever you want the model to do when the skill fires: a role, steps, an output format, a gate.
- Where it lives: `~/.claude/skills/<skill-name>/SKILL.md` for user-wide; in your project folder for project-scoped.
- In Cowork, you write skills the same way — just in the connected folder.

Point at the right column. That tiny file *is* a working skill. Skills aren't magic; they're constrained prompts you don't have to retype.

> "This is the entire artifact. A name, a description, some instructions, and a gate. It's a recipe."

If anyone asks "can a skill call tools?": yes — web search, file reads, subagents. We'll see the subagent pattern on slide 9.

---

## Slide 6 — Installing a skill (Claude Desktop)

Practical interlude. Most of the room hasn't installed one yet — show them the three paths.

- **Write one with Claude.** In a chat, describe what you want the skill to do. Claude scaffolds the SKILL.md, then you save it. Lowest barrier; good for the first try.
- **Upload.** Drop a `SKILL.md` or a `.skill` bundle into Settings → Capabilities → Skills. Useful when you're cribbing from a repo like Blattman's.
- **Browse.** The built-in Skill Library has pre-built skills you can install in one click. Worth scanning before you write your own.
- Reference: [claude.com/docs/skills/how-to](https://claude.com/docs/skills/how-to).
- Cowork users: same picture, just in the Cowork settings panel.

> "However you get the file in there, the file is what matters. Today we're writing one."

---

## Slide 7 — Pass 1: a reviewer skill

The first iteration. One reviewer, one rubric.

- Show the invocation prompt. Make the point that the human's job at this stage is just "use this skill on this thing."
- Talk through what's different from Pass 0:
  - Output has **sections**. The skill specified the format.
  - Findings are **anchored to passages**, not vibes.
  - But — it's one generalist. The methodology critique is thin; the writing critique is thin. The skill is doing too much in one file.

> "One reviewer beats no reviewer. Two specialized reviewers beats one generalist. That's where we're going next."

---

## Slide 8 — Pass 2: specialize

This is the slide where you introduce composition — and where Blattman's repo earns its keep.

- Two skills, not one. Each does one job well.
- The methodology reviewer (right column, summarized): cribbed from [chrisblattman/claudeblattman/agents/review-methodology.md](https://github.com/chrisblattman/claudeblattman/blob/main/agents/review-methodology.md). It enforces a five-dimension rubric: causal language, identification, statistical claims, robustness, data/measurement.
- The writing reviewer (don't show on slide but mention out loud): [review-writing.md](https://github.com/chrisblattman/claudeblattman/blob/main/agents/review-writing.md). Argument structure, clarity, evidence integration, voice.
- Each file is short. Short is the point — you can audit them, edit them, version-control them.
- Cite Blattman openly. The room respects this is borrowed thinking.

> "Chris Blattman has been publishing these for free. We're going to crib his methodology-review file and his writing-review file, then write a third file on top that runs them both."

---

## Slide 9 — Pass 3: orchestrate

This is the conceptual peak of the module. Slow down.

- The orchestrator is the skill the human invokes. It doesn't critique the paper itself; it **dispatches** two sub-tasks, in **parallel**, in **fresh contexts**.
- Why fresh contexts: if the methodology reviewer's critique is in the writing reviewer's context, the writing reviewer anchors. You lose independence.
- Why parallel: faster, but also intellectually independent. Each is a separate vote.
- The synthesis section is the conductor's job:
  - **Agreements** — issues both critics flagged. Highest confidence.
  - **Disagreements** — surface them. Don't pick a winner; the human reads them.
  - **Unique per-critic insight** — the writing reviewer caught a structural problem the methodologist missed. That's the value of two critics.
- Reference [review-plan.md](https://github.com/chrisblattman/claudeblattman/blob/main/skills/review-plan.md) on Blattman's repo — it implements this pattern (peer critic dispatch, parallel calls, synthesis).

> "This pattern — orchestrator on top, specialists underneath, fresh context per call — is how every complex skill ends up structured. Learn it once, reuse it everywhere."

If someone asks how this works in Cowork specifically: the Task / Agent tool is what dispatches. Mention briefly, don't go deep — it's covered in module 4.

---

## Slide 10 — Build a quality gate

The slide that turns the skill from a reviewer into a *useful* reviewer.

- Every finding gets a color. **🔴 Red** = critical, blocks acceptance. **🟡 Yellow** = important, but not blocking. **🟢 Green** = minor.
- The verdict rule is hard-coded in the skill text: **any Red ⇒ REVISE**. No discretion. No "but it's promising."
- Why this matters: without the gate, the skill drifts back toward the praise sandwich. RLHF wants to be nice; the gate makes niceness impossible without a clean rubric.
- This is the part of skill-writing that people skip. Don't skip it.

> "The gate is how you build something the model can't talk its way out of. ACCEPT, REVISE, REJECT — and a deterministic rule for which one applies."

Optional aside: this is also why structured outputs (JSON, tables, scoring) tend to beat open-ended prose for evaluation tasks. Constraint is your friend.

---

## Slide 11 — Evaluate the evaluator

The slide where you become a methodologist about your own tool.

- The skill is a research instrument. Like any instrument, it needs validation.
- Two methods for new users:
  - Run it on your own published paper. You know the strengths and weaknesses; check what it catches and what it invents.
  - Run it on a famous flawed paper (Reinhart–Rogoff, LaCour, anything in the replication-crisis canon). Check whether it catches the *known* flaw.
- The two failure modes are symmetric:
  - **False Reds** — model hallucinates a critique that isn't grounded in the paper. Symptom of an overheated prompt.
  - **Missed Reds** — model fails to flag something it should. Symptom of a too-permissive rubric, or sycophancy creeping back in.
- Iterate the *skill file*, not the prompt. The skill is the artifact you keep.

> "If the synthetic reviewer can't catch a flaw you can already see, the skill isn't ready. Edit the skill until it can."

---

## Slide 12 — Reading the four passes

The recap. Brisk.

- Pass 0: nothing. Flattery, no rigor.
- Pass 1: role and rubric. Real, but generic.
- Pass 2: two specialists. Methods get attacked; prose gets attacked.
- Pass 3: orchestrator + gate. A verdict that can refuse.

Punchline: same model, same draft. The skill file is the only thing that changed.

> "The skill is the difference between a chatbot and an instrument. Same engine. Different scaffolding."

---

## Slide 13 — Takeaways

Walk them in order.

- A skill is a contract — role, steps, output format, gate. If any of those is missing, you have a wish, not a skill.
- Compose, don't bloat. Two short skills are easier to audit and easier to fix than one long one.
- The gate is the point. A reviewer that can only say "this is interesting" isn't a reviewer.
- The pattern generalizes:
  - **Grant pre-reads** — funder rubric in the skill, parallel critics for narrative and budget.
  - **Response to reviewers** — orchestrator that drafts replies and a second critic that checks tone.
  - **Conference abstracts** — fast scan against acceptance criteria.

> "You learned one skill today. You can write the next one tomorrow."

---

## Slide 14 — Async exercise

The take-home. Make sure people leave with this.

- ~45 minutes is honest. Less if they already have a draft and Claude Desktop / Cowork open.
- Minimal install: Claude Desktop or Cowork. No CLI required.
- Steps:
  1. Pick a draft. Their own, ideally. Or a working paper they've read recently.
  2. Run Pass 0 in chat. Save the output as a baseline.
  3. Create `peer-review/SKILL.md`. Start from Blattman's [review-plan.md](https://github.com/chrisblattman/claudeblattman/blob/main/skills/review-plan.md). Strip out anything plan-specific; keep the rubric structure and the verdict gate.
  4. Split into [review-methodology.md](https://github.com/chrisblattman/claudeblattman/blob/main/agents/review-methodology.md) + [review-writing.md](https://github.com/chrisblattman/claudeblattman/blob/main/agents/review-writing.md). These are agents in Blattman's repo; you can write them as skills if you're not on Claude Code.
  5. Run the orchestrator. Compare to Pass 0.
- The diagnostic question: *which Red did the skill catch that you'd missed in your own re-read?* If the answer is "none," the skill isn't ready yet.

> "The exercise is self-contained. You'll know it worked when the skill flags something you'd talked yourself out of."

---

## Pacing

- 25–30 minutes total. The literature-review module covered the basics of skills; this module compounds on that.
- Heaviest slides: 5 (skill anatomy), 9 (orchestrator), 10 (the gate). Spend 2–3 minutes each.
- If you're behind: compress slide 8 (specialization) — just say "two files, here's why" and move to slide 9.
- If you're ahead: open the actual Blattman repo on screen during slide 8 or 9 and click through `review-plan.md`. Showing real code that exists in the wild is the most persuasive thing you can do.

---

## Things to watch for

- People will ask "but does Claude actually do the parallel dispatch?" Yes — the Task tool / Agent tool in Claude Code and Cowork dispatches subagents with fresh contexts. Don't promise capabilities that aren't there in the chat-only Claude Desktop product; if they're chat-only, they can simulate the pattern by running two separate conversations and pasting outputs into a third. It's manual, but the *structure* is the lesson.
- People will ask about reproducibility. Honest answer: skills don't make the model deterministic. They make the *scaffolding* reproducible. Same skill file, same paper → same rubric applied. The findings may vary at the margin; the verdict gate constrains the variance.
- If someone says "this is just prompting with extra steps" — agree. That's the point. The extra steps are the file you can edit and version-control instead of retyping.
- Don't oversell. Synthetic peer review is a pre-read, not a substitute for a real referee. Be explicit.

---

## Further reading (drop into chat or share via slack)

- [Blattman's skills repo](https://github.com/chrisblattman/claudeblattman/tree/main/skills) — the source we're cribbing from.
- [`review-plan.md`](https://github.com/chrisblattman/claudeblattman/blob/main/skills/review-plan.md) — the orchestrator pattern we're echoing.
- [`review-methodology.md`](https://github.com/chrisblattman/claudeblattman/blob/main/agents/review-methodology.md) — the methods critic.
- [`review-writing.md`](https://github.com/chrisblattman/claudeblattman/blob/main/agents/review-writing.md) — the writing critic.
- [Anthropic — Skills documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) — official reference.
- [Anthropic — Equipping agents for the real world with Agent Skills](https://www.anthropic.com/news/skills) — overview of skill architecture.
