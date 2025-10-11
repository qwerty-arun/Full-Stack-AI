import speech_recognition as sr

from google import genai
from google.genai import types

client = genai.Client(
    api_key=""
)

def main():
    rec = sr.Recognizer() # Speech to Text

    with sr.Microphone() as source: # Mic Access
        rec.adjust_for_ambient_noise(source) # Cut Background Noise
        rec.pause_threshold = 2 # If user pauses for 2 sec, then start recognition

        print("Speak Something...")
        audio = rec.listen(source)

        print("Processing Audio... (STT)")
        stt = rec.recognize_google(audio)

        print("You said:", stt)

        SYSTEM_PROMPT = f"""
            You are an expert voice agent. You are given the transcript of what user has said using voice.
            You need to output as if you are a voice agent and whatever you speak will be converted back to audio using AI and played back to user.
        """

        response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=stt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        )
    )

    print("🤖 AI Response:\n", response.text)

main()