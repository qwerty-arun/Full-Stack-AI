from google import genai

API_KEY=""
client = genai.Client(api_key=API_KEY)

for m in client.models.list():
    print(m.name)