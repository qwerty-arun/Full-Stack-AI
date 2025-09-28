from google import genai
from google.genai import types

client = genai.Client(
    api_key=''
)

# Zero Shot Prompting: Directly giving the instruction to the model without prior examples
# The model must rely only on its pre-trained knowledge to solve the task
SYSTEM_PROMPT = "You should only answer coding related questions. Do not answer anything else. Your name is Jarvis. If user asks anything other than coding, just ask sorry."

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Write a python code to translate the word 'hello' to Kannada",
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT
    )
)

print(response.text)