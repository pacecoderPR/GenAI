import os
from dataclasses import dataclass

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL = "gemini-3.5-flash-lite"

# USD per 1M tokens. Source: https://ai.google.dev/gemini-api/docs/pricing (paid tier, checked 2026-10-09)
INPUT_PRICE_PER_M = 0.30
OUTPUT_PRICE_PER_M = 2.50  # thinking tokens are billed at this rate too

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set. Check your .env file.")

client = genai.Client(api_key=api_key)


@dataclass
class Result:
    text: str
    finish_reason: str | None
    input_tokens: int
    output_tokens: int  # reply tokens + thinking tokens (both billed as output)
    cost: float


def estimate_cost(input_tokens: int, output_tokens: int) -> float:
    return (
        input_tokens / 1_000_000 * INPUT_PRICE_PER_M
        + output_tokens / 1_000_000 * OUTPUT_PRICE_PER_M
    )


def ask(prompt: str, temperature: float = 0.7, max_tokens: int = 200) -> Result:
    text = ""
    finish_reason = None
    input_tokens = reply_tokens = thinking_tokens = 0

    stream = client.models.generate_content_stream(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=max_tokens,
            temperature=temperature,
        ),
    )

    for chunk in stream:
        if chunk.text:
            print(chunk.text, end="", flush=True)
            text += chunk.text

        for candidate in chunk.candidates or []:
            if candidate.finish_reason:
                finish_reason = candidate.finish_reason.name

        usage = chunk.usage_metadata
        if usage:
            input_tokens = usage.prompt_token_count or input_tokens
            reply_tokens = usage.candidates_token_count or reply_tokens
            thinking_tokens = usage.thoughts_token_count or thinking_tokens

    print()

    # Check once, after the stream has ended.
    if finish_reason is None:
        print("[WARNING] No finish reason was reported.")
    elif finish_reason == "MAX_TOKENS":
        print("[WARNING] Cut off at the token limit. Raise max_tokens.")
    elif finish_reason != "STOP":
        print(f"[WARNING] Stopped early: {finish_reason}")

    output_tokens = reply_tokens + thinking_tokens
    return Result(
        text=text,
        finish_reason=finish_reason,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cost=estimate_cost(input_tokens, output_tokens),
    )


if __name__ == "__main__":
    for prompt, cap in [("Explain tokens in detail", 20), ("Say hi in 5 words", 300)]:
        print(f"\n--- max_tokens={cap} ---")
        r = ask(prompt, max_tokens=cap)
        print(
            f"finish={r.finish_reason}  in={r.input_tokens}  "
            f"out={r.output_tokens}  cost=${r.cost:.6f}"
        )