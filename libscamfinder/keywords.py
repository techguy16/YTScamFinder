import json
import requests

def get_keywords(url):
    keywords = []
    temp = json.loads(requests.get(url).text)
    for item in temp["keywords"]:
        keywords.append(item)
    return keywords

def get_config():
    config = ""
    with open("config.json", "r") as c:
        for line in c:
            config += line.rstrip()
        config = json.loads(config)
    return config