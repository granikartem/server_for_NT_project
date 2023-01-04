from typing import List
import math
from server.schemas import Video


def find_best_video(videos: List[Video], anger: float, disgust: float, fear: float, joy: float, neutral: float, sad: float, surprise: float):
    min = 1.0
    url = ""
    for video in videos:
        dist = find_distance(video, anger, disgust, fear, joy, neutral, sad, surprise)
        if  dist < min:
           min = dist
           url = video.url
    return url

def find_distance(video: Video,
                    anger: float,
                    disgust: float,
                    fear: float,
                    joy: float,
                    neutral: float,
                    sad: float,
                    surprise: float):
    return math.sqrt(
        (video.anger_percentage - anger) ** 2 +
        (video.disgust_percentage - disgust) ** 2 +
        (video.fear_percentage - fear) ** 2 +
        (video.joy_percentage - joy) ** 2 +
        (video.neutral_percentage - neutral) ** 2 +
        (video.sadness_percentage - sad) ** 2 +
        (video.surprise_percentage - surprise) ** 2)