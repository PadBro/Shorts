from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from gtts import gTTS
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from datetime import datetime
import speech_recognition as sr
import random
import urllib.request
import requests
import json
import os
import whisper_timestamped
from helper import readJson, writeJson

def getPost ():
	subreddit = "AmItheAsshole"
	response = requests.get(f'https://www.reddit.com/r/{subreddit}/new.json?sort=new')

	with open(f"response/{subreddit}.json", "w") as jsonFile:
		json.dump(response.json(), jsonFile)

def createMP3 (text):
	now = datetime.now()
	time = now.strftime("%Y-%m-%d_%H%M%S")
	fileName = f'audio/{time}.mp3'
	tts = gTTS(text, lang='en', tld='us')
	tts.save(fileName)
	return fileName

def getBackground ():
	return "./background/Splitgate.mp4"

def getVideoLength (backgroundFile):
	video = MP4(backgroundFile)
	return int(video.info.length)

def getAudioLength (audioFile):
	audio = MP3(audioFile)
	return int(audio.info.length)

def getSubtitles (audioFile):
	model = whisper_timestamped.load_model("base")
	result = whisper_timestamped.transcribe(model, audioFile)
	subs = []
	for segment in result["segments"]:
		subs.append(((segment["start"], segment["end"]), segment["text"]))
	return subs

def createClip (audioFile, backgroundFile):
	videoLength = getVideoLength(backgroundFile)
	audioLength = getAudioLength(audioFile)

	clipStart = random.randint(0, videoLength - audioLength)

	videoClip = VideoFileClip(backgroundFile).subclip(clipStart, clipStart + audioLength)
	audioClip = AudioFileClip(audioFile)

	newAudioClip = CompositeAudioClip([audioClip])
	videoClip.audio = newAudioClip

	generator = lambda txt: TextClip(txt, font='Arial', method='caption', size=[720, 1280], fontsize=64, color='white')
	subtitles = SubtitlesClip(getSubtitles(audioFile), generator)
	result = CompositeVideoClip([videoClip, subtitles.set_pos(('center','center'))])

	now = datetime.now()
	time = now.strftime("%Y-%m-%d_%H%M%S")
	fileName = f"output/{time}.mp4"
	result.write_videofile(fileName)

	os.remove(audioFile)
	return fileName

# def addSubtitles (fileName, audioFile):
# 	generator = lambda txt: TextClip(txt, font='Arial', method='caption', size=[720, 1280], fontsize=64, color='white')
# 	subtitles = SubtitlesClip(getSubtitles(), generator)

# 	video = VideoFileClip(fileName)

# 	result = CompositeVideoClip([video, subtitles.set_pos(('center','center'))])
# 	result.write_videofile(fileName)

def createShort(text):
	audioFile = createMP3(text)
	backgroundFile = getBackground()
	fileName = createClip(audioFile, backgroundFile)
	return fileName

response = readJson("response/AmItheAsshole.json")
oldPost = readJson("post.json")
usedPost = []
# selftext
# title
# subreddit_name_prefixed
# permalink
# url
post = response["data"]["children"][0]
createShort(post["data"]["title"] + " " + post["data"]["selftext"])

# for post in response["data"]["children"]:
# 	usedPosts.append(post["data"]["permalink"])

# 	if post["data"]["permalink"] in oldPost:
# 		continue
# 	createShort(post["data"]["title"] + " " + post["data"]["selftext"])

# 	print(f"created file {fileName}")

# writeJson("post.json", usedPosts)
