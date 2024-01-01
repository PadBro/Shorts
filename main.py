"""Module to create short video from a reddit source."""

import requests
from config import max_videos
from src import helper
from src import audio
from src import video
from src import drive
from src import discord_bot

def get_post():
    """Function fetching post from subreddit."""
    subreddit = "AmItheAsshole"
    response = requests.get(f'https://www.reddit.com/r/{subreddit}/new.json?sort=new', timeout=30)

    helper.write_json(f"response/{subreddit}.json", response.json())


def create_short(text, title, description):
    """Function creating shorts."""
    print("creating mp3 file")
    audio_file = audio.create_mp3(text)
    # check if audio length is within the config

    print("choosing background")
    background_file = video.get_background()
    print("generating clip")
    clip_dir = video.create_clip(audio_file, background_file)

    # uploading via api locked the video for now
    # print("uploading to youtube")
    # youtube.uploadVideo(fileName, title, description)

    print("saving meta data")
    helper.write_json(f"{clip_dir}/meta.json", {
        "main": {
            "title": title,
            "description": description
        }
    })
    video.split_parts(clip_dir)
    folder_id = drive.upload_folder(clip_dir)
    discord_bot.send_message(folder_id)

def main():
    """Function main."""
    response = helper.read_json("response/AmItheAsshole.json")
    old_posts = helper.read_json("data/post.json")

    counter = 0
    for post in response["data"]["children"]:
        if counter == max_videos:
            break

        if post["data"]["permalink"] in old_posts:
            continue

        title = post["data"]["title"] + " #" + post["data"]["subreddit_name_prefixed"] + " #Shorts"
        description = post["data"]["url"]
        text = post["data"]["title"] + " " + post["data"]["selftext"]
        create_short(text, title, description)
        old_posts.append(post["data"]["permalink"])
        counter += 1

    helper.write_json("data/post.json", old_posts)

    print(f"created {counter} files!")

def dev_single_post():
    """Function dev."""
    response = helper.read_json("response/AmItheAsshole.json")
    post = response["data"]["children"][0]
    subreddit = post["data"]["subreddit_name_prefixed"]
    title = post["data"]["title"] + f" #{subreddit} #Shorts"
    description = post["data"]["url"]
    text = post["data"]["title"] + " " + post["data"]["selftext"]
    create_short(text, title, description)

main()
