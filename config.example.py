# pylint: skip-file
subreddit = "AmItheAsshole"

max_videos = 1
part_buffer_in_seconds = 2
video_end_buffer_in_seconds = 1
max_video_length_in_seconds = (max_videos * 60) - (max_videos * part_buffer_in_seconds) - video_end_buffer_in_seconds

discord_token = ""
discord_channel_id = ""
