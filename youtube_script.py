import csv
import json
import requests
from constants import MY_API_KEY, REQ_CHANNEL_ID

channel_id = REQ_CHANNEL_ID

def make_csv(page_id):
	api_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={page_id}&key={MY_API_KEY}"
	api_response = requests.get(api_url)
	videos = json.loads(api_response.text)

	with open("youtube_videos.csv", "w") as csv_file:
		csv_writer = csv.writer(csv_file)
		csv_writer.writerow([
			"publishedAt",
			"title",
			"description",
			"thumbnailurl"])

		has_another_page = True
		while has_another_page:
			if videos.get("items") is not None:
				for video in videos.get("items"):
					video_data_row = [
						video["snippet"]["publishedAt"],
						video["snippet"]["title"],
						video["snippet"]["description"],
						video["snippet"]["thumbnails"]["default"]["url"]
					]
					csv_writer.writerow(video_data_row)
			if "nextPageToken" in videos.keys():
				next_page_url = api_url + "&pageToken="+videos["nextPageToken"]
				next_page_post = requests.get(next_page_url)
				videos = json.loads(next_page_post.text)
			else:
				print("no more videos...")
				has_another_page = False

make_csv(channel_id)