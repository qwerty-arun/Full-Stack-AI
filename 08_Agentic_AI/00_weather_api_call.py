from google import genai
from google.genai import types
import requests

client = genai.Client(
    api_key=''
)

def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    else:
        return f"Failed to fetch weather."

def main():
    user_query = input("> ")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_query,
        # config=types.GenerateContentConfig(
        #     system_instruction=""
        # )
    )

    print("🤖:", response.candidates[0].content.parts[0].text)

print(get_weather("bengaluru"))
# main()