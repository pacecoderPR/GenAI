# Learning Log

## 2026-10-07 (Week 0, Day 1)
- **Did:** Set up Git, uv, Docker, and Postgres with pgvector in a container with a named volume. Read the Messages API docs, watched Karpathy's Intro to LLMs, took a quiz.
- **Broke:** Multi-line docker command failed on Windows because `\` only works in Linux/macOS shells. Fixed by putting it on one line.
- **Learned:** The API is stateless, so the full history is resent every turn, and total cost grows roughly quadratically. `max_tokens` is a per-request output cap, not a quota. Context window is like RAM and pgvector is like disk.