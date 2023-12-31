from datetime import datetime
from gtts import gTTS
from mutagen.mp3 import MP3
import whisper_timestamped

def create_mp3 (text):
    now = datetime.now()
    time = now.strftime("%Y-%m-%d_%H%M%S")
    file_name = f'audio/{time}.mp3'
    tts = gTTS(text, lang='en', tld='us')
    tts.save(file_name)
    return file_name

def get_audio_length (audio_file):
    audio = MP3(audio_file)
    return int(audio.info.length)

def get_subtitles (audio_file):
    model = whisper_timestamped.load_model("base")
    result = whisper_timestamped.transcribe(model, audio_file, language="en")
    subs = []
    for segment in result["segments"]:
        subs.append(((segment["start"], segment["end"]), segment["text"]))
    return subs
