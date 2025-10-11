import speech_recognition as sr
from google import genai
from google.genai import types
import simpleaudio as sa
import wave
import tempfile
import os

# ---------- SETUP ----------
API_KEY=""
client = genai.Client(api_key=API_KEY)

# Models
LLM_MODEL = "models/gemini-2.5-flash"
TTS_MODEL = "models/gemini-2.5-flash-preview-tts"

# Recognizer
recognizer = sr.Recognizer()
mic = sr.Microphone()

print("🎤 Voice assistant ready. Speak anytime (say 'exit' to quit)...")

while True:
    try:
        # 1️⃣ Record speech
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

        # 3️⃣ Send text → Gemini LLM
        llm_response = client.models.generate_content(
            model=LLM_MODEL,
            contents=user_text
        )
        reply = llm_response.text
        print(f"🤖 Gemini: {reply}")

        # 4️⃣ Convert reply → speech (TTS)
        tts_response = client.models.generate_content(
            model=TTS_MODEL,
            contents=reply,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name="aoede"  # change to another voice if desired
                        )
                    )
                )
            )
        )

        # 5️⃣ Save temporary WAV file and play
        audio_bytes = tts_response.candidates[0].content.parts[0].inline_data.data
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            wav_path = f.name
            with wave.open(wav_path, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(24000)
                wf.writeframes(audio_bytes)

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
