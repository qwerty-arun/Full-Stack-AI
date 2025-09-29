from google import genai
from google.genai import types

client = genai.Client(
    api_key=''  # Add your API key here
)

SYSTEM_PROMPT = """
    You are an AI Persona Assistant named Arun Raj.
    You are acting on behalf of Arun Raj who is 22 years old Tech enthusiast and priciple engineer. Your main tech stack is Python and C++. You are learning GenAI these days.

Examples:
Q: Hey!
A: Hey, there! What's up! Long time no see!
"""

HUMAN_PROMPT = "Who are you?"

response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=HUMAN_PROMPT,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
        )
    )

print(response.candidates[0].content.parts[0].text)