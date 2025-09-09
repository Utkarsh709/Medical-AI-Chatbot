#-------------------------------------------BRAIN OF THE DOCTOR---------------------------------------------

# Groq API setup
import os
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Image conversion
import base64

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


from groq import Groq

def analyze_image_with_query(query, model, encoded_image):
    client = Groq(api_key=GROQ_API_KEY)

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}"
                    }
                }
            ]
        }
    ]

    chat_completions = client.chat.completions.create(
        messages=messages,
        model=model
    )

    return chat_completions.choices[0].message.content


#--------------------------------------------VOICE OF THE DOCTOR----------- -------------------------------

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


# gTTS FUNCTION
def text_to_speech_with_gtts(input_text, output_filepath):
    audioobj = gTTS(text=input_text, lang="en", slow=False)
    audioobj.save(output_filepath)
    play_audio_ffplay(output_filepath)


# ELEVENLABS FUNCTION
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    voice_id = "21m00Tcm4TlvDq8ikWAM"
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id="eleven_turbo_v2",
        text=input_text,
        output_format="mp3_22050_32"
    )
    save(audio, output_filepath)
    play_audio_ffplay(output_filepath)


#------------------------------------VOICE OF THE PATIENT-----------------------------------------------------

import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s-%(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Simplified function to record audio from the microphone and save it as an MP3 file.

    Args:
    file_path (str): Path to save the recorded audio file.
    timeout (int): Maximum time to wait for a phrase to start (in seconds).
    phrase_time_limit (int): Maximum time for the phrase to be recorded (in seconds).
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")
            
            # Record the audio
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")
            
            # Convert the recorded audio to an MP3 file
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            
            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")


def transcribe_with_groq(audio_filepath, stt_model="whisper-large-v3"):
    """Transcribe audio file using Groq API"""
    try:
        client = Groq(api_key=GROQ_API_KEY)
        with open(audio_filepath, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=stt_model,
                file=audio_file,
                language="en"
            )
        return transcription.text
    except Exception as e:
        logging.error(f"Transcription error: {e}")
        return "Error in transcription"


#------------------------------------------------GRADIO APP--------------------------------------------------

import gradio as gr

system_prompt = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""


def process_inputs(audio_filepath, image_filepath):
    # Handle audio input
    if audio_filepath:
        speech_to_text_output = transcribe_with_groq(audio_filepath=audio_filepath)
    else:
        speech_to_text_output = "No audio provided"

    # Handle the image input
    if image_filepath:
        try:
            doctor_response = analyze_image_with_query(
                query=system_prompt + " " + speech_to_text_output, 
                encoded_image=encode_image(image_filepath), 
                model="meta-llama/llama-4-scout-17b-16e-instruct"
            )
            
            # Generate audio response
            audio_output_path = "doctor_response.mp3"
            text_to_speech_with_elevenlabs(input_text=doctor_response, output_filepath=audio_output_path)
            
        except Exception as e:
            doctor_response = f"Error analyzing image: {str(e)}"
            audio_output_path = None
    else:
        doctor_response = "No image provided for me to analyze"
        audio_output_path = None

    return speech_to_text_output, doctor_response, audio_output_path


# Create the interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath", label="Record your question"),
        gr.Image(type="filepath", label="Upload medical image")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(label="Doctor's Voice Response")
    ],
    title="AI Doctor with Vision and Voice",
    description="Upload an image and record your question to get medical analysis"
)

# Only launch if this script is run directly (not imported)
if __name__ == "__main__":
    # Test audio recording functionality
    # audio_file_path = "AI_DOCTOR/patient_voice.mp3"
    # record_audio(file_path=audio_file_path)
    
    # Launch the Gradio interface
    iface.launch(debug=True)