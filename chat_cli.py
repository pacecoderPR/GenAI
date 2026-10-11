from google.genai import types
from stream_call import ask

history: list[types.Content] = []
total_in = total_out = 0
total_cost = 0.0
turn = 0

def message(role: str, text: str) -> types.Content:
    return types.Content(role=role, parts=[types.Part(text=text)])

while True:
    user_text = input("\nYou: ").strip()
    if user_text.lower() == "quit":
        break
    if not user_text:
        continue

    history.append(message("user", user_text))

    print("LLM reponse:", end=" ", flush=True)

    result = ask(history, max_tokens=1024)

    history.append(message("model", result.text))
    turn+=1
    total_in += result.input_tokens
    total_out += result.output_tokens
    total_cost += result.cost
    print(f"\n[Turn {turn}] Input tokens: {result.input_tokens}, Output tokens: {result.output_tokens}, Cost: ${result.cost:.6f}")
    print(f"[Total] Input tokens: {total_in}, Output tokens: {total_out}, Cost: ${total_cost:.6f}")

