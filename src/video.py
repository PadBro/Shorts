from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from datetime import datetime
from mutagen.mp4 import MP4
from src.audio import getAudioLength, getSubtitles
from pathlib import Path
from src import helper
import random
import os
import math

def getBackground ():
	path = "./background/"
	backgrounds = os.listdir(path)
	backgrounds.remove('.gitkeep')
	return path + random.choice(backgrounds)

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

	generator = lambda txt: TextClip(txt, font='Arial', method='caption', size=[680, 1240], fontsize=40, color='white')
	subtitles = SubtitlesClip(getSubtitles(audioFile), generator)
	result = CompositeVideoClip([videoClip, subtitles.set_pos(('center','center'))])

	currentDir = createDir()

	fileName = f"{currentDir}/clip.mp4"
	result.write_videofile(fileName)

	os.remove(audioFile)
	return currentDir

def createDir ():
	now = datetime.now()
	time = now.strftime("%Y-%m-%d_%H%M%S")
	currentDir = f"output/{time}"
	Path(currentDir).mkdir(parents=True, exist_ok=True)
	return currentDir

def splitParts(clipDir):
    videoLength = getVideoLength(f"{clipDir}/clip.mp4")

    # check if need to be split into parts
    if (videoLength < 60):
    	return

    meta = helper.readJson(f"{clipDir}/meta.json")

    # calculate amount of parts
    print("calculate amount of parts")
    amountParts = math.ceil(videoLength / 60)

    # calculate part length
    partLength = videoLength / amountParts

    # split video into parts
    print("split video into parts")
    parts = []
    for x in range(amountParts):
        start = x * partLength
        end = start + partLength
        if (x != 0):
            start -= 2
        parts.append({
            "start": start,
            "end": end,
        })
        videoClip = VideoFileClip(f"{clipDir}/clip.mp4").subclip(start, end)

        # save parts
        videoClip.write_videofile(f"{clipDir}/part_{x}.mp4")
        meta[f"part_{x}"] = {
            "title": meta["main"]["title"] + " Part " + str(x + 1),
            "description": meta["main"]["description"] + " Part " + str(x + 1) + " of " + str(amountParts)
        }

    # add parts info to meta.json
    print("add parts info to meta.json")
    helper.writeJson(f"{clipDir}/meta.json", meta)