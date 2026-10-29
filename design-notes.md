If I give a computer two sentences, how could it tell whether they mean the same thing, when they share no words?
Your chatbot has 5,000 doc pages. The model can’t read them all per question. What would you do?

## Known limitations

### 2026-10-12: Code examples stripped from corpus (Day 1)
- **What:** `clean_markdown` deletes every `{* ... *}` include macro. In the FastAPI docs those lines are the code examples, so many pages lose their code.
- **Evidence:** the shortest page, `global-dependencies.md`, is only 992 chars after cleaning. (Confirm after comparing with the raw file.)
- **Decision:** option (a). Accept it for now. Week 1 goal is to understand the whole RAG pipeline, not to perfect the loader.
- **Expected impact:** questions like "how do I write X?" will retrieve explanation text but no code, so the answers will be weaker.
- **Revisit:** Saturday, after the 20-question test. If code questions fail, try option (c): read the file from `docs_src/` and inline it as a fenced Python block. Compare scores before and after.

## Embedding lab (2026-10-29)

- Got right: pair 1 & 2 was highest (0.94). Guessed 0.96.
- Score: each sentence is 3072 numbers. Cosine = angle between two of them. Same meaning, same direction, high score.
- Surprise: unrelated text scored 0.47 to 0.59, not 0.
- Why not 0: real sentences always share something (language, sentence shape), and 3072 numbers describe many features, not only topic.
- Meaning for project: related is about 0.9, unrelated about 0.5. The "I don't know" cutoff must come from my own data.