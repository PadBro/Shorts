import urllib.request
import requests
from src import helper
from src import youtube
from src import audio
from src import video
from config import maxVideos, uploadYoutube

def getPost ():
    subreddit = "AmItheAsshole"
    response = requests.get(f'https://www.reddit.com/r/{subreddit}/new.json?sort=new')

    helper.writeJson(f"response/{subreddit}.json", response.json())


def createShort(text, title, description):
    print("creating mp3 file")
    audioFile = audio.createMP3(text)
    # check if audio length is within the config

    print("choosing background")
    backgroundFile = video.getBackground()
    print("generating clip")
    clipDir = video.createClip(audioFile, backgroundFile)

    # uploading via api locked the video for now
    # print("uploading to youtube")
    # youtube.uploadVideo(fileName, title, description)

    print("saving meta data")
    helper.writeJson(f"{clipDir}/meta.json", {
        "main": {
            "title": title,
            "description": description
        }
    })
    video.splitParts(clipDir)

def main():
    response = helper.readJson("response/AmItheAsshole.json")
    oldPosts = helper.readJson("data/post.json")

    counter = 0
    for post in response["data"]["children"]:
        if (counter == maxVideos):
            break

        if post["data"]["permalink"] in oldPosts:
            continue

        title = post["data"]["title"] + " #" + post["data"]["subreddit_name_prefixed"] + " #Shorts"
        description = post["data"]["url"]
        text = post["data"]["title"] + " " + post["data"]["selftext"]
        createShort(text, title, description)
        oldPosts.append(post["data"]["permalink"])
        counter += 1

    helper.writeJson("data/post.json", oldPosts)

    print(f"created {counter} files!")

def devSinglePost():
    response = helper.readJson("response/AmItheAsshole.json")
    post = response["data"]["children"][0]
    subreddit = post["data"]["subreddit_name_prefixed"]
    title = post["data"]["title"] + f" #{subreddit} #Shorts"
    description = post["data"]["url"]
    text = post["data"]["title"] + " " + post["data"]["selftext"]
    createShort(text, title, description)

def test():
    video.splitParts("./output/2023-12-30_231908")


main()