import os
import requests
import tempfile
import subprocess
import whisper
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-pro")

whisper_model = whisper.load_model("base")


def download_and_convert_ogg(url: str) -> str:
    """Download an OGG audio file and convert it to WAV for transcription"""
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to download audio")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as ogg_file:
        ogg_file.write(response.content)
        ogg_path = ogg_file.name

    wav_path = ogg_path.replace(".ogg", ".wav")
    command = ["ffmpeg", "-y", "-i", ogg_path, wav_path]
    subprocess.run(command, check=True)

    os.remove(ogg_path)
    return wav_path


def transcribe_audio(wav_path: str) -> str:
    """Transcribe audio using Whisper and respond using Gemini"""
    result = whisper_model.transcribe(wav_path)
    transcript = result["text"]
    print(f"Transcription: {transcript}")
    
    try:
        gemini_response = gemini_model.generate_content(transcript)
        return gemini_response.text.strip()
    except Exception as e:
        return f"(Error from Gemini: {e})"
