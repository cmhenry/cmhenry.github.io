# AI in survey research

A 25-minute practical adapted from the survey section of the current AI for Social Science Research workshop draft. All items and responses below are constructed teaching examples, not participant data or recorded model output. The tasks can be completed without a model.

## 1. Question wording (8 minutes)

Intended construct: acceptability of sending de-identified interview transcripts to a commercial AI service for analysis. Target population: university researchers. Intended use: describing attitudes, not measuring whether respondents actually use such services.

Compare these candidate questions before requesting model output:

- A: “Should researchers stop using unreliable AI tools that threaten privacy?”
- B: “How acceptable is AI use in academic research?”

A uses leading language and combines reliability, privacy, and a policy recommendation. B removes some loaded language but broadens the construct: it no longer specifies transcripts, commercial processing, or the relevant use. Better prose is not necessarily a better measure.

Write one more specific item, a response scale, and a question for a cognitive interview. Compare what each version measures. Do not treat the following candidate as validated:

> How acceptable or unacceptable do you consider it for a university researcher to send interview transcripts with names and direct identifiers removed to a commercial AI service for analysis?

Possible scale: completely unacceptable; somewhat unacceptable; neither acceptable nor unacceptable; somewhat acceptable; completely acceptable; cannot judge with the information given. Keep nonresponse distinct from the midpoint. Removing direct identifiers does not guarantee anonymity.

Complete optional model request (start a fresh chat):

```text
Intended construct: acceptability of sending de-identified interview transcripts
to a commercial AI service for analysis. Population: university researchers.
Purpose: describe attitudes, not infer actual behavior.

Candidate A: Should researchers stop using unreliable AI tools that threaten privacy?
Candidate B: How acceptable is AI use in academic research?

Compare both questions with the intended construct. Identify leading language,
combined constructs, missing conditions, and changes in what is measured.
Propose one item and a balanced response scale with an uncertainty option.
Suggest two cognitive-interview probes for real participants.
Do not claim your wording, scale, or translation is validated.
```

Human check: does the proposed item preserve the construct? What do respondents understand by “commercial service,” and what assumptions do they make about consent or data retention? Human cognitive pretesting and a design-appropriate pilot remain necessary. A model playing a respondent is not a human cognitive interview.

## 2. Coding open responses (8 minutes)

Question: “What concerns you about AI use in research?”

Illustrative multi-label codebook:

- P — privacy/confidentiality: explicit concern about disclosure, identifiable material, or third-party access.
- V — accuracy/evidence/verification: explicit concern about correctness, real sources, or ability to check a result.
- E — unequal access/representation: explicit concern about unequal resources, inclusion, or representation.
- O — other/unclear: no supported P/V/E label. Do not combine O with another label.

Use only explicit text. Do not infer concerns from presumed respondent identity. Record your labels and supporting text before requesting model output.

- A: “I do not want interviews sent to a vendor, even after names are removed.”
- B: “The references look convincing; how do I know they are real?”
- C: “Better-funded colleagues buy better tools; we cannot check every translation.”

Complete optional model request (start a fresh chat):

```text
Code the constructed responses below to: What concerns you about AI use in research?
Use only explicit text. Multiple labels are allowed.

P = privacy/confidentiality: disclosure, identifiable material, or third-party access.
V = accuracy/evidence/verification: correctness, real sources, or checking a result.
E = unequal access/representation: unequal resources, inclusion, or representation.
O = other/unclear: no supported P/V/E label; never combine O with another label.

A: I do not want interviews sent to a vendor, even after names are removed.
B: The references look convincing; how do I know they are real?
C: Better-funded colleagues buy better tools; we cannot check every translation.

Return response_id, labels, and the exact text supporting each label.
Flag ambiguity separately. Do not infer demographics or change the codebook.
These are teaching examples, not real respondents or a deployment benchmark.
```

Human check: compare each label and quotation with your initial decision. A plausibly supports P, B supports V, and C supports E and V under these definitions. Discuss disagreement rather than treating this interpretation as a validated gold standard. If you revise the codebook, record the revision and apply it consistently to all cases; do not present changed definitions as improved model performance.

For real use, retain a separate evaluation sample with human coding and adjudication, inspect errors by relevant language or subgroup, and assess how errors affect the intended estimate. Three constructed responses cannot establish accuracy or construct validity.

## 3. Synthetic respondents (6 minutes)

Compare two proposals:

- Fill an underrepresented subgroup with generated answers and analyze them as ordinary human observations.
- Generate explicitly marked cases to test skip logic, file formats, and an analysis script.

For each, identify what was observed, the population quantity claimed, and the human evidence needed. Testing code paths does not establish representativeness. Matching marginal percentages does not establish joint distributions, subgroup differences, or causal effects. Keep simulated and human data distinguishable.

No respondent generation or external data upload is required for this discussion.

## 4. Apply to a project (3 minutes)

Name one bounded use, the comparison that would make its output useful, and the inference that still requires human evidence. A supported decision not to use the model is a valid outcome.

## Reading

[Pew Research Center: Writing Survey Questions](https://www.pewresearch.org/writing-survey-questions/) provides background on question wording and response options. The teaching cases here are adaptations, not quotations from that guidance.
