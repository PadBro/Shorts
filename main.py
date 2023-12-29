import urllib.request
import requests
from helper import readJson, writeJson
from src import youtube
from src import audio
from src import video

def getPost ():
	subreddit = "AmItheAsshole"
	response = requests.get(f'https://www.reddit.com/r/{subreddit}/new.json?sort=new')

	with open(f"response/{subreddit}.json", "w") as jsonFile:
		json.dump(response.json(), jsonFile)


def createShort(text, title, description):
	audioFile = audio.createMP3(text)
	backgroundFile = video.getBackground()
	fileName = video.createClip(audioFile, backgroundFile)
	# youtube.uploadVideo(fileName, title, description)
	return fileName

response = readJson("response/AmItheAsshole.json")
oldPost = readJson("post.json")
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

# writeJson("post.json", usedPosts)
