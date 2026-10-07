from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

print("1")
response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Explain tokens in 2 lines",
    config=types.GenerateContentConfig(
        max_output_tokens=200,
        temperature=0.7,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        ),
    ),
)

print("2")
print(response.text)