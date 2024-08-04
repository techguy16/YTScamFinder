from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import requests
import json
import sys

data = []

# Define keywords for search
keywords = []
temp = json.loads(requests.get("https://techguy16.github.io/YTScamFinder/keywords/keywords.json").text)
for item in temp["keywords"]:
    keywords.append(item)

# Params for API
DEVELOPER_KEY = sys.argv[1]
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# Get data from JSON
def get_data(row):
    global data
    video_id = []

    video_id.append(row['id']['videoId'])
    video_id.append(row['snippet']['description'].replace(",", " "))
    
    data.append(video_id)

# Run search with given word
def run_search(keyword):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(
        part='snippet',
        q=keyword,
        order='date',
        maxResults=50
    ).execute()
    
    items = search_response['items']
    df = items
    for item in df:
        get_data(item)


if __name__ == "__main__":
    for item in keywords:
        run_search(item)
    
    csvData = "video id,description,\n"
    for item in data:
        for item2 in item:
            csvData += item2 + ","
        csvData += "\n"

    with open("data.csv", "a+") as w:
        w.write(csvData)
        w.close()
