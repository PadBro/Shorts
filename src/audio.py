"""Module providing functionality to handle mp3 files."""

from datetime import datetime
from mutagen.mp3 import MP3
import whisper_timestamped
from tts.tiktok.main import tts
from config import tts_voices
import random

def create_mp3 (text):
    """Function creating a mp3 file from text."""
    print("creating mp3 file")
    now = datetime.now()
    time = now.strftime("%Y-%m-%d_%H%M%S")
    file_name = f'audio/{time}.mp3'

    print("choosing voice")
    voice = random.choice(tts_voices)
    print(f"picked voice: {voice}")

    tts(text, voice, file_name)
    return file_name

def get_audio_length (audio_file):
    """Function getting the length of the provided mp3 file."""
    audio = MP3(audio_file)
    return int(audio.info.length)

def get_subtitles (audio_file):
    """Function generating timestamped subtitles."""
    print("transcribing audio")
    model = whisper_timestamped.load_model("base")
    result = whisper_timestamped.transcribe(model, audio_file, language="en")
    subs = []
    for segment in result["segments"]:
        subs.append(((segment["start"], segment["end"]), segment["text"]))
    return subs
