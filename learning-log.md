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

  ## 2026-10-09 (Week 0, Day 3)
- **Did:** Turned my Gemini call into a streaming one (`generate_content_stream`), added token counts, a cost estimate and a finish-reason warning, and wrapped it in a reusable `ask()` that returns a `Result` dataclass. Explained "what is an LLM call and what does it cost" out loud.
- **Broke / confused:**
  - My price constants were 10x too high (used $3 / $25 per million instead of $0.30 / $2.50). Lesson: copy prices from the pricing page, with a source comment, and never from memory.
  - My first warning check printed "Ellipsis" (`{...}` is a Python value, not a placeholder), sat inside the stream loop instead of after it, and I accidentally overwrote `finish_reason` with `None` by moving a line out of its `if`.
  - Quoted three different prices when explaining cost aloud. I need to know my numbers cold.
- **Learned:**
  - **Cost:** input and output tokens are priced separately, per million tokens. Output costs about 8x more than input for this model, and thinking tokens are billed as output. Formula: input ÷ 1M × input price + output ÷ 1M × output price.
  - **Token types in the response:** `prompt_token_count` is input, `candidates_token_count` is the reply, and `thoughts_token_count` is thinking (if the model uses it).
  - **Streaming:** the response is a sequence of chunks, not one object. Each chunk carries a piece of text, and the finish reason and usage metadata show up on some of them (usually the last). I loop over the chunks, print each piece as it arrives, add it to a running string, and keep the latest finish reason and token counts I see. After the loop ends, I check the finish reason once.
  - **Finish reason:** `STOP` is a normal finish, and anything else (`MAX_TOKENS`, a safety stop) means the text may be incomplete. Check it after every call.
  - **Python:** `if __name__ == "__main__"` keeps demo code from running on import, and `@dataclass` returns several values as one named object.


  ## 2026-10-10 (Week 0, Day 4)
- **Did:** Built a multi-turn streaming chat CLI (`chat_cli.py`) that reuses `ask()` from `stream_call.py`. It keeps the conversation history, prints each reply live, and shows tokens and cost per turn and as running totals.
- **Broke / confused:**
  - My first version printed the whole `Result` object, so every reply showed up twice. Fixed by printing only the token and cost numbers.
  - `ask()` defaulted to `max_tokens=200`, which would cut chat replies short and store the cut-off text in the history. Raised the cap for chat.
  - The model said "I've added your last name to my memory", which is false. It only knows my name because I resend the history each turn.
- **Learned:**
  - **Calling code from another file:** `from stream_call import ask` loads the functions, and the `if __name__ == "__main__":` guard stops the demo code in `stream_call.py` from running on import.
  - **Real-time streaming:** the reply arrives as chunks. Inside `ask()`, a loop prints each chunk with `end=""` and `flush=True` so it appears as it's generated, and also adds it to a string. `chat_cli.py` only prints the `Gemini:` label and receives the finished text at the end.
  - **History:** it's a list of `Content` objects with a role (`user` or `model`) and parts. I add the user message before the call and the model reply after it finishes.
  - **Tokens grow every turn:** input(n) = input(n-1) + output(n-1) + new message. Over 5 turns my input went from 8 to 98 tokens. Cost grows because the whole history is resent each time.