from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from datetime import datetime
from mutagen.mp4 import MP4
from src.audio import getAudioLength, getSubtitles
import random

def getBackground ():
	return "./background/Splitgate.mp4"

def getVideoLength (backgroundFile):
	video = MP4(backgroundFile)
	return int(video.info.length)

def createClip (audioFile, backgroundFile):
	videoLength = getVideoLength(backgroundFile)
	audioLength = getAudioLength(audioFile)

	clipStart = random.randint(0, videoLength - audioLength)

	videoClip = VideoFileClip(backgroundFile).subclip(clipStart, clipStart + audioLength)
	audioClip = AudioFileClip(audioFile)

	newAudioClip = CompositeAudioClip([audioClip])
	videoClip.audio = newAudioClip

	generator = lambda txt: TextClip(txt, font='Arial', method='caption', size=[720, 1280], fontsize=40, color='white')
	subtitles = SubtitlesClip(getSubtitles(audioFile), generator)
	result = CompositeVideoClip([videoClip, subtitles.set_pos(('center','center'))])

	now = datetime.now()
	time = now.strftime("%Y-%m-%d_%H%M%S")
	fileName = f"output/{time}.mp4"
	result.write_videofile(fileName)

	os.remove(audioFile)
	return fileName