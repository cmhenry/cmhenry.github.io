# Framing: what is AI? — presenter notes

Target: 20 minutes. The slides introduce working terms, not a complete account of model training.

1. **Title:** distinguish the model from the application around it.
2. **Shared vocabulary:** ask which terms participants have encountered. Do not equate familiarity with technical competence.
3. **Transformers:** one architecture within deep learning; the diagram is a simplification.
4. **Tokens:** fragments, whole words, punctuation, and other units. Segmentation varies by tokenizer and language. The image illustrates one tokenizer, not universal counts.
5. **Generating text:** explain next-token generation. Tool retrieval and code execution are additional application operations, not evidence that generated text is true.
6. **Training overview:** pre-training, continued pre-training, and post-training are useful distinctions, not three compulsory stages with disjoint datasets.
7. **Pre-training:** broad training does not give a model an inspectable bibliography. Avoid claims about the precise data mixture of an undisclosed model.
8. **Continued pre-training:** domain and context-length training vary by developer. “Mid-training” has no single universal boundary.
9. **Post-training:** instruction examples and preference learning can shape behavior. RLHF is one method; AI feedback and verifiable rewards are others. A reasoning model may itself be an adapted foundation model, rather than a separate category.
10. **Reward and validity:** training updates weights; ordinary inference normally does not. Neither preference ratings nor fluent presentation are a direct test of a research claim. Do not attribute every error, refusal, or expression of uncertainty to RLHF.
11. **Cutoff:** information can enter through context or tools after training. Coverage before a cutoff is incomplete too. Ask where a particular claim came from.
12. **Context:** the application may insert memories, project instructions, or summaries. A new visible conversation is not proof of an empty context. Explain the difference between persistent application state and changed model weights.
13. **Reasoning:** intermediate steps can help some tasks. A visible explanation is not necessarily a faithful transcript of internal computation; assess the answer using external evidence.
14. **Recap:** connect each term to a question participants can ask about the interface in front of them.

If time is short, combine the three training-stage slides. Preserve the distinction between training, inference, and retrieval.
