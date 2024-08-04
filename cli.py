from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from colorama import Fore, Back, Style
import requests
import json
# import sys

data = []

config = ""
# Params for API
with open("config.json", "r") as c:
    for line in c:
        config += line.rstrip()
    config = json.loads(config)

# Define keywords for search
keywords = []
temp = json.loads(requests.get("https://techguy16.github.io/YTScamFinder/keywords/keywords.json").text)
for item in temp["keywords"]:
    keywords.append(item)
    
DEVELOPER_KEY = config["API_KEY"]
print(f"{Style.BRIGHT}{Fore.GREEN}Using API Key: {Style.RESET_ALL}{DEVELOPER_KEY}")
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
    print(f"{Style.BRIGHT}{Fore.BLUE}Starting searches...{Style.RESET_ALL}")
    for item in keywords:
        print(f"Searching query \"{Style.BRIGHT}{Fore.GREEN}{item}{Style.RESET_ALL}\"...")
        run_search(item)
    
    csvData = ""
    for item in data:
        for item2 in item:
            csvData += item2 + ","
        csvData += "\n"

    with open("data.csv", "a+") as w:
        w.write(csvData)
        w.close()

    print(f"Data saved to {Fore.MAGENTA}{Style.BRIGHT}data.csv{Style.RESET_ALL}.")