import speech_recognition as sr
from google import genai
from google.genai import types
import wave
import simpleaudio as sa
import tempfile
import os

# ---------- SETUP ----------
API_KEY=""
client = genai.Client(api_key=API_KEY)


def record_speech():
    """Record speech from microphone and convert to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎙 Speak now (press Ctrl+C to stop)...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"🗣 You said: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Sorry, I couldn't understand you.")
        return ""
    except sr.RequestError as e:
        print("⚠️ Speech Recognition error:", e)
        return ""


def generate_reply(user_text):
    """Send user's text to Gemini LLM and get reply."""
    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",  # ✅ fixed model name
            contents=f"The user said: {user_text}. Respond conversationally."
        )
        reply = response.text.strip()
        print(f"🤖 Gemini: {reply}")
        return reply
    except Exception as e:
        print("⚠️ LLM error:", e)
        return "Sorry, I encountered an error."


def play_audio(filename):
    """Play audio using simpleaudio."""
    try:
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        play_obj.wait_done()
    except Exception as e:
        print("⚠️ Audio playback error:", e)


def synthesize_speech(text, voice_name="Kore"):
    """Convert text to speech using Gemini TTS and play it."""
    try:
        tts_response = client.models.generate_content(
            model="models/gemini-2.5-flash-preview-tts",  # ✅ correct TTS model
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=voice_name,
                        )
                    )
                ),
            ),
        )

        audio_bytes = tts_response.candidates[0].content.parts[0].inline_data.data

        # Save temp WAV file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            filename = f.name
            with wave.open(filename, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(24000)
                wf.writeframes(audio_bytes)

        play_audio(filename)
        os.remove(filename)

    except Exception as e:
        print("⚠️ TTS error:", e)


def main():
    print("🎧 Voice Chat with Google Gemini (v2.5)")
    print("Press Ctrl+C to exit anytime.")

    while True:
        user_text = record_speech()
        if not user_text:
            continue

        reply = generate_reply(user_text)
        synthesize_speech(reply)


if __name__ == "__main__":
    main()
