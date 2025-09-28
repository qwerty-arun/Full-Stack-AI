from google import genai
from google.genai import types

client = genai.Client(
    api_key=''
)

# Few Shot Prompting: Directly giving the instruction to the model with a few examples
# Better guides the model about both task type and answer style, improving accuracy

SYSTEM_PROMPT = """You should only answer coding related questions. Do not answer anything else. Your name is Jarvis. If user asks anything other than coding, just ask sorry.
Examples:
Q: Can you explain the a + b whole square? 
A: Sorry, I can only help with Coding related questions.

Q: Hey, Write a code in python for adding two numbers.
A: def add(a, b):
        return a + b
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Write me Python code to calculate a + b whole squared.",
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT
    )
)

print(response.text)