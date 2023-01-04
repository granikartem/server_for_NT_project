import CommentsScraper
import major
import scraper
import csv
import argparse
import requests, sys, time, os
import pandas as pd
VIDEO_ID = None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--key_path',
                        help='Path to the file containing the api key, by default will use api_key.txt in the same directory',
                        default='api_key.txt')
    parser.add_argument('--country_code_path',
                        help='Path to the file containing the list of country codes to scrape, by default will use country_codes.txt in the same directory',
                        default='country_codes.txt')
    parser.add_argument('--output_dir', help='Path to save the outputted files in', default='output/')

    args = parser.parse_args()

    output_dir = args.output_dir
    api_key, country_codes = scraper.setup(args.key_path, args.country_code_path)
    scraper.get_data(api_key,country_codes)


    print('download comments')
    df = pd.read_csv('output/US_videos.csv')
    video_id = df['video_id']
    print(df)
    print(video_id)
    for l in video_id:
        print(l)
        major.VIDEO_ID = l
        print(major.VIDEO_ID)
        response = CommentsScraper.youtube()
        items = response.get("items")
        nextPageToke = response.get("nextPageToken")  # скачивается порциями, на каждую следующую выдаётся указатель
        i = 1
        while nextPageToke is not None:
            print(str(i * 100))  # показываем какая сотня комментариев сейчас скачивается
            response = CommentsScraper.youtube(nextPageToke)
            nextPageToke = response.get("nextPageToken")
            items = items + response.get("items")
            i += 1
        #класторизатор сюда

if __name__ == "__main__":
    main()