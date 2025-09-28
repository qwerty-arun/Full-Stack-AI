from google import genai
from google.genai import types

client = genai.Client(
    api_key=''
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hello, I am Arun. Nice to meet you!",
    config=types.GenerateContentConfig(
        system_instruction="You are an expert in Maths and only answer math related questions. If the query is not related to maths. Just say sorry and don't answer that."
    )
)

print(response.text)