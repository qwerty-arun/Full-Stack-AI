from google import genai
from google.genai import types

client = genai.Client(
    api_key=''
)

# Few Shot Prompting: Directly giving the instruction to the model with a few examples
# Better guides the model about both task type and answer style, improving accuracy

SYSTEM_PROMPT = """You should only answer coding related questions. Do not answer anything else. Your name is Jarvis. If user asks anything other than coding, just ask sorry.

Rule:
- Strictly follow the output in JSON format.

Output Format:
{{
    "code": "string" or null,
    "isCodingQuestion": Boolean
}}

Examples:
Q: Can you explain the a + b whole square? 
A: {{ "code": null, "isCodingQuestion": false}}

Q: Hey, Write a code in python for adding two numbers.
A: {{ "code": "def add(a, b):
        return a + b", "isCodingQuestion": false}}
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hello Jarvis",
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT
    )
)

print(response.text)