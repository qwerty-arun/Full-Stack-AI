from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key="", # use gemini API Key
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model = "gemini-2.5-flash", #model must be from google
    messages=[{
        "role": "user",
        "content": "Hey there, I am Arun!"
    }]
)

print(response.choices[0].message.content)