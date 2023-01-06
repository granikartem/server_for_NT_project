import comment_scrapper
import major
import scrapper
import csv
import argparse
import requests, sys, time, os
import pandas as pd
VIDEO_ID = None
import torch
def main():
    video_id = scrapper.get_videos()
    for video in video_id:
        print(comment_scrapper.get_comments(video))


if __name__ == "__main__":
    torch.cuda.empty_cache()

    print(torch.cuda.is_available())