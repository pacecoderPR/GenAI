from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

load_dotenv()
MODEL = "gemini-3.5-flash-lite"
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set. Check your .env file.")
client = genai.Client(
    api_key=api_key
)

def ask(prompt : str , temperature:float , maxtokens:int):
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=maxtokens,
            temperature=temperature,
        ),
    )
    return response.text ,response.candidates[0].finish_reason ,response.usage_metadata.total_token_count 
for temp in (0, 1):
    for i in range(5):
        text, reason, tokens = ask("Explain tokens in 2 lines", temp, 100)
        print(temp, reason, tokens, text[:80])

