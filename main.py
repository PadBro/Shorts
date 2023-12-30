import urllib.request
import requests
from src import helper
from src import youtube
from src import audio
from src import video
from config import maxVideos

def getPost ():
    subreddit = "AmItheAsshole"
    response = requests.get(f'https://www.reddit.com/r/{subreddit}/new.json?sort=new')

    helper.writeJson(f"response/{subreddit}.json", response.json())


def createShort(text, title, description):
    audioFile = audio.createMP3(text)
    backgroundFile = video.getBackground()
    currentDir = video.createClip(audioFile, backgroundFile)
    helper.writeJson(f"{currentDir}/meta.json", {
        "title": title,
        "description": description
    })

response = helper.readJson("response/AmItheAsshole.json")
# oldPost = helper.readJson("data/post.json")
# usedPosts = []
post = response["data"]["children"][0]
subreddit = post["data"]["subreddit_name_prefixed"]
title = post["data"]["title"] + f" #{subreddit} #Shorts"
description = post["data"]["url"]
text = post["data"]["title"] + " " + post["data"]["selftext"]
createShort(text, title, description)

# counter = 0
# for post in response["data"]["children"]:
#     if (counter == maxVideos):
#         break

#     # todo:
#     # All videos need to be saved till the post get fetched again
#     # after fetching check for dublicates the rest can be deleted
#     usedPosts.append(post["data"]["permalink"])
#     if post["data"]["permalink"] in oldPost:
#         continue

#     subreddit = post["data"]["subreddit_name_prefixed"]
#     title = post["data"]["title"] + f" #{subreddit} #Shorts"
#     description = post["data"]["url"]
#     text = post["data"]["title"] + " " + post["data"]["selftext"]
#     createShort(text, title, description)
#     counter += 1

# helper.writeJson("data/post.json", usedPosts)

# print(f"created {counter} files!")