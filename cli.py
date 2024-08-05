from googleapiclient.discovery import build
from colorama import Fore, Style
import libscamfinder.keywords
import argparse
import re

data = []
extracted_links = []

config = libscamfinder.keywords.get_config()
keywords = libscamfinder.keywords.get_keywords()
    
DEVELOPER_KEY = config["API_KEY"]
libscamfinder.check_key(DEVELOPER_KEY)
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# Get data from JSON
def get_data(row):
    global data, extracted_links
    video_id = []

    video_id.append(row['id']['videoId'])
    video_id.append(row['snippet']['description'].replace(",", " "))
    
    found_links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', row['snippet']['description'].replace(",", " "))
    if not len(found_links) == 0:
        print(f"{Style.BRIGHT}{Fore.GREEN}Links found in description: {Style.RESET_ALL}{len(found_links)}")
        for item in found_links:
            if not item in extracted_links:
                extracted_links.append(item)
    else:
        print(f"{Style.BRIGHT}{Fore.RED}No links found in description.{Style.RESET_ALL}")
        
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
    
    csvData = ""
    for item in extracted_links:
        if item == extracted_links[-1]:
            csvData += item
        else:
            csvData += item + ",\n"
        
    with open("links.csv", "a+") as w:
        w.write(csvData)
        w.close()
        
    print(f"Extracted links saved to {Fore.MAGENTA}{Style.BRIGHT}links.csv{Style.RESET_ALL}.")