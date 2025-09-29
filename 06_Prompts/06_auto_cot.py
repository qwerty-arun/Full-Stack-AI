from google import genai
from google.genai import types
import json

client = genai.Client(
    api_key=''  # Add your API key here
)

SYSTEM_PROMPT = """
You are an expert AI Assistant in resolving user queries using chain of thought.
You work on START, PLAN AND OUTPUT steps.
You need to first PLAN what needs to be done. The PLAN can be multiple steps.
Once you think enough PLAN has been done, finally you can give an OUTPUT.

Rules:
- Strictly follow the given JSON output format
- Only run one step at a time.
- The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and finally OUTPUT (which is going to be displayed to the user).

Output JSON Format:
{ "step": "START" | "PLAN" | "OUTPUT", "content": "string" }

Example:
START: Hey, can you solve 2 + 3 * 5 / 10
PLAN: { "step": "PLAN", "content": "Seems like user is interested in maths problem" }
PLAN: { "step": "PLAN", "content": "Looking at the problem, we should solve this using BODMAS method" }
...
OUTPUT: { "step": "OUTPUT", "content": "The final answer is 3.5" }
"""

response_schema = {
    "type": "object",
    "properties": {
        "step": {"type": "string"},
        "content": {"type": "string"}
    },
    "required": ["step", "content"]
}


def format_message_history_as_text(messages):
    lines = []
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        # Format roles like SYSTEM:, USER:, ASSISTANT:
        lines.append(f"{role.upper()}: {content}")
    return "\n".join(lines)


print("\n\n\n")

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

user_query = input("👉 ")
message_history.append({"role": "user", "content": user_query})

while True:
    prompt_text = format_message_history_as_text(message_history)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt_text,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=response_schema
        )
    )

    raw_result = response.candidates[0].content.parts[0].text
    message_history.append({"role": "assistant", "content": raw_result})

    # Parse JSON string from model response
    parsed_result = json.loads(raw_result)
    content = parsed_result.get("content", "")

    # Print only the content string (no JSON, no step label)
    print("🧠", content)

    step = parsed_result.get("step")

    if step == "OUTPUT":
        print("🎂", content)
        break


print("\n\n\n")
