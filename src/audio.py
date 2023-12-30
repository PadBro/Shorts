from gtts import gTTS
from mutagen.mp3 import MP3
from datetime import datetime
import whisper_timestamped

def createMP3 (text):
	now = datetime.now()
	time = now.strftime("%Y-%m-%d_%H%M%S")
	fileName = f'audio/{time}.mp3'
	tts = gTTS(text, lang='en', tld='us')
	tts.save(fileName)
	return fileName

def getAudioLength (audioFile):
	audio = MP3(audioFile)
	return int(audio.info.length)

def getSubtitles (audioFile):
	model = whisper_timestamped.load_model("base")
	result = whisper_timestamped.transcribe(model, audioFile, language="en")
	subs = []
	for segment in result["segments"]:
		subs.append(((segment["start"], segment["end"]), segment["text"]))
	return subs