from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import psycopg2
import pandas as pd
import requests

data = []
# Define keywords for search
keywords = ['sea of thieves hack', 'valorant hack', 'fortnite skin swapper']

# Retrieve the developer key from keys module
DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# Function to get additional data for each video
def get_additional_data(row):
    global data
    video_id = []

    video_id.append(row['id']['videoId'])
    video_id.append(row['snippet']['description'].replace(",", " "))
    
    data.append(video_id)

# Function to run a search with a given keyword
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
        get_additional_data(item)
    #print(df)
 
    #return df

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
