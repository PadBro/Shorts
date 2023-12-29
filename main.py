import urllib.request
import requests
from src import helper
from src import youtube
from src import audio
from src import video

def getPost ():
	subreddit = "AmItheAsshole"
	response = requests.get(f'https://www.reddit.com/r/{subreddit}/new.json?sort=new')

	helper.writeJson(f"response/{subreddit}.json", response.json())


def createShort(text, title, description):
	audioFile = audio.createMP3(text)
	backgroundFile = video.getBackground()
	fileName = video.createClip(audioFile, backgroundFile)
	# youtube.uploadVideo(fileName, title, description)
	return fileName

response = helper.readJson("response/AmItheAsshole.json")
oldPost = helper.readJson("post.json")
usedPost = []
post = response["data"]["children"][0]
subreddit = post["data"]["subreddit_name_prefixed"]
title = post["data"]["title"] + f" #{subreddit} #Shorts"
description = post["data"]["url"]
createShort(post["data"]["title"] + " " + post["data"]["selftext"], title, description)


# for post in response["data"]["children"]:
# 	usedPosts.append(post["data"]["permalink"])

# 	if post["data"]["permalink"] in oldPost:
# 		continue
# 	createShort(post["data"]["title"] + " " + post["data"]["selftext"])

# 	print(f"created file {fileName}")

# helper.writeJson("post.json", usedPosts)
