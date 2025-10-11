import speech_recognition as sr
from google import genai
import simpleaudio as sa
import tempfile
import os

# Initialize Google GenAI client
API_KEY=""
client = genai.Client(api_key=API_KEY)

# Models
LLM_MODEL = "models/gemini-2.5-flash"
TTS_MODEL = "models/gemini-2.5-flash-preview-tts"

# Speech recognizer
recognizer = sr.Recognizer()
mic = sr.Microphone()

print("🎤 Voice assistant ready. Speak anytime (say 'exit' to quit)...")

while True:
    try:
        # 1️⃣ Listen for user speech
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("\nListening...")
            audio = recognizer.listen(source)

        # 2️⃣ Convert speech → text
        user_text = recognizer.recognize_google(audio)
        print(f"🗣️ You said: {user_text}")

        if user_text.lower() in ["exit", "quit", "stop"]:
            print("👋 Exiting voice chat.")
            break

        # 3️⃣ Send to Gemini (LLM)
        response = client.models.generate_content(
            model=LLM_MODEL,
            contents=f"{user_text}",
        )

        reply = response.text
        print(f"🤖 Gemini: {reply}")

        # 4️⃣ Convert reply → speech (TTS)
        speech_response = client.models.generate_content(
            model=TTS_MODEL,
            contents=[{"role": "user", "parts": [reply]}],
            response_modalities=["AUDIO"],
            generation_config={"audio_config": {"voice_name": "aoede"}},
            # config={"speech": {"voice": "aoede"}}
        )

        # 5️⃣ Save temporary WAV file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(speech_response.audio)
            wav_path = f.name

        # 6️⃣ Play audio
        wave_obj = sa.WaveObject.from_wave_file(wav_path)
        play_obj = wave_obj.play()
        play_obj.wait_done()

        os.remove(wav_path)

    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
    except KeyboardInterrupt:
        print("\n👋 Exiting.")
        break
    except Exception as e:
        print(f"⚠️ Error: {e}")
