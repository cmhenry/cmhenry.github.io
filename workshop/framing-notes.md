# Framing: What is AI? — Presenter Notes

**Audience:** political science postdocs and faculty, mostly no ML background.
**Goal:** install a shared working vocabulary — not a CS course.
**Posture:** demystifying, not technical. Move fast.

---

## Slide 1 — Title

Just announce the module.

> "This module is the boring one. It's the one where we agree on what words mean. After this we can have real conversations."

---

## Slide 2 — Why shared vocabulary

- Press uses "AI" to mean everything; vendors use it to mean whatever sells.
- We're researchers — we name our variables. Same discipline here.
- Promise: by the end you'll know what a token is, what RLHF actually does, and why those things matter for your data.

---

## Slide 3 — Where transformers fit (ML family tree)

> *Image: nested-set or family-tree diagram, AI ⊃ ML ⊃ Deep Learning ⊃ Transformers.*

- "AI" is the outer container — anything that mimics cognition.
- "Machine learning" — systems that learn patterns from data, no hard rules.
- "Deep learning" — ML with stacked neural networks.
- "Transformers" — one specific architecture, invented 2017, that turned out to scale.
- LLMs, ChatGPT, Claude, Gemini — all transformers.

Punchline: when someone says "AI" today, they usually mean the innermost circle.

---

## Slide 4 — Token

> *Image: tokenizer view — a sentence broken into colored chunks.*

- The model doesn't see characters or words. It sees tokens.
- A token is a sub-word piece. "Researcher" might be 1; "Zürich" might be 3.
- Every limit and price you'll see — "200k context", "$15 per million tokens" — is in this unit.
- The first thing that happens to your prompt is tokenization. After that it's all numbers.

---

## Slide 5 — The transformer in one minute

> *Image: simplified attention / transformer block (Comet-style, not the full 2017 paper figure).*

- The model receives a sequence of tokens.
- It computes attention — which tokens matter for predicting the next one.
- It outputs a probability distribution over the next token.
- That's it. Everything else you see — reasoning, code, essays — is this one step run thousands of times.

Optional aside: this is why these models are sometimes called "stochastic parrots" — they're producing the next likely token, conditioned on everything that came before.

---

## Slide 6 — Three stages of training

> *Image: pipeline diagram, pre-train → mid-train → post-train.*

- Modern LLMs are built in stages. Each stage has a different goal and a different dataset.
- This matters because the behavior you experience is the *last* stage shaping the first one.
- Walk through each stage on the next three slides.

---

## Slide 7 — Pre-training

- Most expensive stage. Months of compute, web-scale data.
- Single task: predict the next token.
- Output is a "foundation model" — fluent but unguided. It will complete your sentence, not answer your question.
- The "knowledge" lives here. So does most of the bias, the leaked PII, the cultural defaults.

---

## Slide 8 — Mid-training

- The middle stage. Newer term — not all labs use the same vocabulary.
- Curated data: code, math, longer documents, multilingual material, sometimes synthetic.
- Builds up specific capabilities the post-train stage will lean on.
- Still next-token prediction, just with cleaner and more targeted text.

---

## Slide 9 — Post-training / RLHF

- This is where a foundation model becomes a chatbot.
- Step 1: instruction tuning — show the model examples of good Q/A pairs.
- Step 2: RLHF — reinforcement learning from human feedback. Humans rank outputs; the model is trained to produce outputs that rank higher.
- This is where helpfulness, refusals, tone, formatting all come from.
- "Personality" lives here. So do most of the guardrails.

---

## Slide 10 — What RLHF actually does (key concept)

Slow down. This is the slide that pays back the whole module.

- RLHF isn't teaching truth. It's teaching "what got high ratings".
- The model converges toward a *local* maximum of that reward signal.
- Side effects:
  - Confident, well-formatted prose (humans rate confident answers higher).
  - Sycophancy (agreeing with you raises ratings).
  - Hedging and refusal patterns (safety raters).
  - Reluctance to say "I don't know".
- Your researcher takeaway: when the model sounds sure, that's a *learned style*, not evidence.

> "You're not talking to a knower. You're talking to an optimizer that learned what sounds like knowing."

---

## Slide 11 — Knowledge cutoff

- Every model has a training data cutoff date.
- Things after it: invisible. Recent papers, retractions, elections, deaths.
- "But I asked it about something from last week and it answered" — that came from a *tool* (web search, retrieval), not the model.
- For research: you need to know which output came from weights and which came from a live tool. Different reliability profiles.

---

## Slide 12 — In-context learning

- "Prompting" is the only programming most users will ever do.
- The **context window** is everything the model can currently see: your prompt, prior turns, attached files, tool outputs.
- **Roles**: system (instructions and persona), user (you), assistant (the model). Same conversation, three different speaker tags.
- Crucially: nothing you do in a session changes the weights. Close the window, the lesson is gone.
- Every new session is amnesia. This will matter for reproducibility later.

---

## Slide 13 — Reasoning / chain of thought

- Chain of thought = the model generates intermediate steps before its final answer.
- More steps = more tokens = more compute spent on your question.
- "Reasoning models" (o1, Claude with extended thinking, etc.) do this by default, often with hidden traces.
- The trace *looks like* deliberate thought, but mechanically it's still next-token prediction extended over more tokens.
- Useful heuristic: chain of thought tends to help on math, multi-step logic, code. It does not magically grant truthfulness.

---

## Slide 14 — Vocabulary recap

Brisk. Just confirm the kit they're walking out with.

- Token · context window · foundation model
- Pre-train · mid-train · post-train · RLHF
- Knowledge cutoff · in-context learning · roles
- Chain of thought

> "If a paper, a vendor, or a colleague uses one of these terms loosely, you now have ground to push back. That's the whole point of this module."

---

## Pacing

- Target ~18–22 minutes total. Roughly 1.5 min per slide, more on slides 9–10 (RLHF + the optimizer point), less on the recap.
- If you're behind: compress slides 7 and 8 (pre-train + mid-train) into a single beat. The RLHF slide is the one that earns its keep.
- If anyone asks "but does it understand?" — don't get drawn in. Defer to the next module.
