"""Module to create short video from a reddit source."""

import argparse
import requests
from config import max_videos, subreddit
from src import helper
from src import audio
from src import video
from src import drive
from src import discord_bot

def get_posts():
    """Function fetching post from subreddit."""
    print("fetching posts")
    response = requests.get(f'https://www.reddit.com/r/{subreddit}/new.json?sort=new', timeout=30)
    if response.status_code == 200:
        print("succesfully fetched post")
        helper.write_json(f"response/{subreddit}.json", response.json())
    else:
        print("Error while fetching posts")
        print(f"Resposne code: {response.status_code}")
        print(f"Reason: {response.reason}")

def main(background=None, fetch_posts=False):
    """Function main."""
    print("\n\n")

    if fetch_posts:
        get_posts()
    response = helper.read_json(f"response/{subreddit}.json")
    old_posts = helper.read_json("data/post.json")

    counter = 0
    for post in response["data"]["children"]:
        if counter == max_videos:
            break

        if post["data"]["permalink"] in old_posts:
            continue

        title = post["data"]["title"] + " #aita #reddit"
        description = post["data"]["url"]
        text = post["data"]["title"] + " " + post["data"]["selftext"]
        print("generating clip for: " + post["data"]["url"])

        audio_file = audio.create_mp3(text)
        # check if audio length is within the config

        background_file = video.get_background(background)
        clip_dir = video.create_clip(audio_file, background_file)

        # uploading via api locks the video for now
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

        old_posts.append(post["data"]["permalink"])
        counter += 1

    helper.write_json("data/post.json", old_posts)

    print(f"created {counter} files!")
    if counter != 0:
        return

    result = input(
        "No clips created. Do you want to rerun the command with --fetch-posts argument? (Y/n): "
    ).lower()
    if result in ('', 'y', 'yes'):
        main(background=background, fetch_posts=True)

def dev(background=None, fetch_posts=False):
    """Function dev."""

    # folder_id = drive.upload_folder("./output/2024-03-03_213911")
    # discord_bot.send_message(folder_id)
    if fetch_posts:
        get_posts()
    background_file = video.get_background(background)
    # print(background_file)
    response = helper.read_json(f"response/{subreddit}.json")
    post = response["data"]["children"][4]

    # title = post["data"]["title"] + " #aita #reddit"
    # description = post["data"]["url"]
    text = post["data"]["title"] + " " + post["data"]["selftext"]
    # print("generating clip for: " + post["data"]["url"])

    audio_file = audio.create_mp3(text)

    # print("choosing background")
    # background_file = video.get_background(background)
    # print("generating clip")
    # clip_dir = video.create_clip(audio_file, background_file)

    # print("saving meta data")
    # helper.write_json(f"{clip_dir}/meta.json", {
    #     "main": {
    #         "title": title,
    #         "description": description
    #     }
    # })
    # video.split_parts(clip_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Short Generator',
        description='Parses Reddit posts and creates a clip',
    )

    parser.add_argument(
        '-b',
        '--background',
        help='Name of background file'
    )

    parser.add_argument(
        '-d',
        '--dev',
        action='store_true',
        help='Execute dev function'
    )

    parser.add_argument(
        '-fp',
        '--fetch-posts',
        action='store_true',
        help='Fetches posts from reddit'
    )

    args = parser.parse_args()

    if args.dev:
        dev(background=args.background, fetch_posts=args.fetch_posts)
    else:
        main(background=args.background, fetch_posts=args.fetch_posts)
