import os
import googleapiclient.discovery
import csv
import re
from googleapiclient.errors import HttpError


DEVELOPER_KEY = "AIzaSyCKIYghp5s5BJEhMlKVuczeep2UCx1JtuI"


# Функция для скачивания корневых комментариев
def youtube(video_id: str, nextPageToken=None):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)
    request = youtube.commentThreads().list(
        part="id,snippet",
        maxResults=100,
        pageToken=nextPageToken,
        videoId= video_id
    )
    response = request.execute()
    return response


def get_comments(video_id: str):
    comments = []
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    try:
        response = youtube(video_id)
        items = response.get("items")
        nextPageToken = response.get("nextPageToken")  # скачивается порциями, на каждую следующую выдаётся указатель
        while nextPageToken is not None:
            response = youtube(video_id, nextPageToken)
            nextPageToken = response.get("nextPageToken")
            items = items + response.get("items")
        for item in items:
            text = item.get("snippet").get("topLevelComment").get("snippet").get("textDisplay")
            if(len(re.findall(r'http\S+', text)) == 0 and len(text.split()) <= 512):
                text = emoji_pattern.sub(r'', text)
                comments.append(text)
    except HttpError:
        print('sosi')
        pass
    return comments
