import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

sentences =["software engineering can be done via BTECH","software engineering can be done via BTECH and BE both","AI is good","AI is good if you know basics", "Sun is orange" , "River is blue"]


def cosine (a,b):
    dot_product= sum(i*j for i,j in zip(a,b))
    mag_a = sum(i*i for i in a) ** 0.5
    mag_b = sum(i*i for i in b) ** 0.5
    return dot_product / (mag_a * mag_b)

response = client.models.embed_content(
    model="gemini-embedding-2",
    contents=[
        types.Content(parts=[types.Part.from_text(text=s)])
        for s in sentences
    ],
)

vectors =[e.values for e in response.embeddings]

for i in range(len(sentences)):
    row = []
    for j in range(len(sentences)):
        row.append(f"{cosine(vectors[i],vectors[j]):.2f}")
    print(", ".join(row))