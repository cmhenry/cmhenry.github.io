# Comparing review instructions

All excerpts and fallback statements below are constructed teaching examples. They are not real findings, published text, or recorded model output. Use an available chatbot or assess them manually. No installation is required.

## Shared excerpt

> We surveyed 120 volunteers from two university departments after circulating an open invitation. Participants reported whether they used an AI assistant and whether they had submitted a manuscript during the previous six months. Sixty-five percent of AI users reported a submission, compared with forty-five percent of non-users. The comparison is descriptive: it does not adjust for career stage, research time, or prior productivity. These results demonstrate that AI assistants increase researchers' publication output.

Before seeing a model response, record one supported criticism, one defensible aspect of the excerpt, and one question that cannot be answered from the text.

## Pass 0: ordinary request

Start a fresh chat, include the exact excerpt, and ask:

```text
Review this excerpt and tell me what is wrong with it.
```

Save the response unchanged. Do not repeat the request until it fails or produces the expected criticism.

## Pass 1: explicit criteria

Start another fresh chat with the same model and tools. Include the same excerpt and this request:

```text
Review only the supplied excerpt. Identify its stated claim and compare that claim
with its sample, measures, and design. Do not assume the full paper contains
information absent here, and do not invent numerical tests.

For each concern, return:
- the exact passage;
- what is wrong or uncertain and why it matters for the stated claim;
- whether it changes the claim, needs further evidence, or concerns presentation;
- a possible correction and what remains unknown.

Distinguish a supported criticism from a question to ask the author.
Do not demand causal identification for a purely descriptive claim.
Include one defensible aspect of the excerpt if you find one.
Do not issue a journal acceptance verdict.
```

## Optional specialist comparison

Use two fresh chats with the excerpt and complete criteria above. Add “Focus on sampling, measurement, and inference” to one and “Focus on whether the conclusion accurately states the reported evidence” to the other. Do not show either reviewer the other's response. Record extra calls and time: this comparison changes both specialization and effort.

Compare manually. Automatic coordination requires actual subagent support. Agreement between models is not independent confirmation.

## Human check

For each criticism, inspect the quoted passage and mark it supported, unsupported, or unresolved. Compare useful findings, missed issues, and false alarms. A longer or harsher review is not necessarily better.

## Manual fallback

Evaluate these constructed statements; they are not model outputs:

- “The conclusion is causal, but the reported comparison is descriptive and unadjusted.”
- “The study measured manuscript submissions, not publication output.”
- “The difference is statistically significant at p < .01.”
- “The authors conceal the use of volunteers.”
- “The full paper may explain missing responses; this excerpt does not.”

The first two identify visible mismatches. The third invents a test: the excerpt supplies neither group sizes nor test results. The fourth contradicts the stated recruitment. The fifth asks about missing information rather than demonstrating a defect. Make your judgments before consulting this discussion.

A later assessment needs a fresh excerpt, defined criteria, and an appropriate human comparison. This exercise cannot estimate a population error rate or validate an automated reviewer.
