import os
import subprocess
import platform
from gtts import gTTS
from elevenlabs import save
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Function to play audio using ffplay (works for mp3)
def play_audio_ffplay(file_path):
    try:
        subprocess.run(
            ["ffplay", "-nodisp", "-autoexit", file_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print(f"Error playing audio with ffplay: {e}")

# -------------------------------
# gTTS FUNCTION
# -------------------------------
def text_to_speech_with_gtts(input_text, output_filepath):
    audioobj = gTTS(text=input_text, lang="en", slow=False)
    audioobj.save(output_filepath)
    print(f"✅ gTTS audio saved at {output_filepath}")
    play_audio_ffplay(output_filepath)

# -------------------------------
# ELEVENLABS FUNCTION
# -------------------------------
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    # Replace with your valid voice ID
    voice_id = "21m00Tcm4TlvDq8ikWAM"
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id="eleven_turbo_v2",
        text=input_text,
        output_format="mp3_22050_32"
    )
    save(audio, output_filepath)
    print(f"✅ ElevenLabs audio saved at {output_filepath}")
    play_audio_ffplay(output_filepath)

# -------------------------------
# TEST
# -------------------------------
if __name__ == "__main__":
    text = "Hello! This is the AI Doctor speaking with two voices."
    #text_to_speech_with_gtts(text, "AI_DOCTOR/gtts_testing_autoplay.mp3")
    text_to_speech_with_elevenlabs(text, "AI_DOCTOR/elevenlabs_testing_autoplay.mp3")
