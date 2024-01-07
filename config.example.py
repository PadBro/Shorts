# pylint: skip-file
subreddit = "AmItheAsshole"

max_videos = 1
part_buffer_in_seconds = 2
video_end_buffer_in_seconds = 1
max_part_length_in_seconds = 57 # 2 seconds for the part buffer 1 second for youtube
max_video_length_in_seconds = (max_videos * 60) - (max_videos * part_buffer_in_seconds) - video_end_buffer_in_seconds

subtitles = {
	"marginX": 20,
	"marginY": 20,
	"fontsize": 40,
}

discord = {
	"token": "",
	"channel_id": 1111111111111111111,
	"links": [
		{
			"label": "YT",
			"url": "https://youtube.com/",
		},
	]
}