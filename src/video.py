"""Module providing functionality to handle mp4 files."""

from datetime import datetime
from pathlib import Path
import random
import os
import math
from config import max_part_length_in_seconds
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    CompositeAudioClip,
    TextClip,
    CompositeVideoClip
)
from moviepy.video.tools.subtitles import SubtitlesClip
from mutagen.mp4 import MP4
from src.audio import get_audio_length, get_subtitles
from src import helper

def get_background(background=None):
    """Function chooses random background video."""
    path = "./background/"

    if background:
        file_path = Path(f"{path}background")
        if file_path.exists():
            print(f"background: {background}")
            return background
        print(f"could not find \"{background}\"")

    backgrounds = os.listdir(path)
    backgrounds.remove('.gitkeep')
    randomBackground = random.choice(backgrounds)
    print(f"random background: {randomBackground}")
    return path + randomBackground

def get_video_length (background_file):
    """Function getting the length of the provided mp4 file."""
    video = MP4(background_file)
    return int(video.info.length)

def create_clip (audio_file, background_file):
    """Function creating shorts clip."""
    print("creating clip")
    
    video_length = get_video_length(background_file)
    audio_length = get_audio_length(audio_file)

    clip_start = random.randint(0, video_length - audio_length)

    video_clip = VideoFileClip(background_file).subclip(clip_start, clip_start + audio_length)
    audio_clip = AudioFileClip(audio_file)

    new_audio_clip = CompositeAudioClip([audio_clip])
    video_clip.audio = new_audio_clip

    subtitles = SubtitlesClip(get_subtitles(audio_file), subtitles_generator)
    result = CompositeVideoClip([video_clip, subtitles.set_pos(('center','center'))])

    current_dir = create_dir()

    file_name = f"{current_dir}/clip.mp4"
    result.write_videofile(file_name)

    os.remove(audio_file)
    return current_dir

def subtitles_generator(txt):
    """Function generator for SubtitlesClip."""
    return TextClip(
        txt,
        font='Arial',
        method='caption',
        size=[680, 1240],
        fontsize=40,
        color='white'
    )

def create_dir ():
    """Function creating local folder for clips and meta data."""
    now = datetime.now()
    time = now.strftime("%Y-%m-%d_%H%M%S")
    current_dir = f"output/{time}"
    Path(current_dir).mkdir(parents=True, exist_ok=True)
    return current_dir

def split_parts(clip_dir):
    """Function splits the given clip into parts and saves the meta data."""

    video_length = get_video_length(f"{clip_dir}/clip.mp4")

    # check if need to be split into parts
    if video_length < max_part_length_in_seconds:
        print("no splitting needed")
        return

    print("split clip into parts")

    meta = helper.read_json(f"{clip_dir}/meta.json")

    # calculate amount of parts
    amount_parts = math.ceil(video_length / max_part_length_in_seconds)
    print(f"amount of parts: {amount_parts}")

    # calculate part length
    part_length = video_length / amount_parts

    # split video into parts
    print("split video into parts")
    parts = []
    for x in range(amount_parts):
        start = x * part_length
        end = start + part_length
        if x != 0:
            start -= 2
        parts.append({
            "start": start,
            "end": end,
        })
        video_clip = VideoFileClip(f"{clip_dir}/clip.mp4").subclip(start, end)

        # save parts
        video_clip.write_videofile(f"{clip_dir}/part_{x + 1}.mp4")
        meta[f"part_{x + 1}"] = {
            "title": meta["main"]["title"] + " Part " + str(x + 1),
            "description": meta["main"]["description"] +
                " Part " +
                str(x + 1) +
                " of " +
                str(amount_parts)
        }

    # add parts info to meta.json
    print("add parts info to meta.json")
    helper.write_json(f"{clip_dir}/meta.json", meta)
