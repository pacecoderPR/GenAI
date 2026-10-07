# Learning Log

## 2026-10-07 (Week 0, Day 1)
- **Did:** Set up Git, uv, Docker, and Postgres with pgvector in a container with a named volume. Read the Messages API docs, watched Karpathy's Intro to LLMs, took a quiz.
- **Broke:** Multi-line docker command failed on Windows because `\` only works in Linux/macOS shells. Fixed by putting it on one line.
- **Learned:** The API is stateless, so the full history is resent every turn, and total cost grows roughly quadratically. `max_tokens` is a per-request output cap, not a quota. Context window is like RAM and pgvector is like disk.

## 2026-10-08 (Week 0, Day 2)
- **Did:** Made my first Gemini API call from Python, wrapped it in an `ask()` function, and ran a temperature experiment (5 runs each at temperature 0 and 1). Tested errors on purpose.
- **Broke / confused:** My first conclusion (temp 0 is wordier, temp 1 is more direct) didn't hold up once I ran more samples. Also had a stray config line (`automatic_function_calling`) that I couldn't explain, so I removed it. Altered key gave 401, fake model name gave 404.
- **Learned:**
  - **Temperature** controls how random the model's next-token choice is. Low means more focused and consistent, high means more varied. Temp 0 is not fully deterministic: my five runs gave 45-55 tokens with slightly different wording.
  - **Finish reason** tells why generation stopped: `STOP` means it finished naturally, `MAX_TOKENS` means it was cut off by my cap. Check it after every call before trusting the text.
  - **Gemini response structure:** the text is in `response.text` (a shortcut), the full path is `response.candidates[0].content.parts`, the finish reason is on `response.candidates[0].finish_reason`, and token counts are in `response.usage_metadata` (prompt, candidates and total).