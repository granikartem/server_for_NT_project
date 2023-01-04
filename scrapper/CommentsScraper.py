
import os
import googleapiclient.discovery
import csv
import major

DEVELOPER_KEY = "AIzaSyCKIYghp5s5BJEhMlKVuczeep2UCx1JtuI"
#VIDEO_ID = "r3Ol4hgvSL4"


# Функция для скачивания корневых комментариев
def youtube(nextPageToken=None):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    print(major.VIDEO_ID)

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="id,snippet",
        maxResults=100,
        pageToken=nextPageToken,
        videoId= major.VIDEO_ID
    )
    response = request.execute()
    return response


# Функция для скачивания реплаев на комментарии
def youtubechild(NextParentId, nextPageToken=None):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.comments().list(
        part="id,snippet",
        maxResults=100,
        pageToken=nextPageToken,
        parentId=NextParentId
    )
    response = request.execute()
    return response


# Главная функция
def main():
    # Скачиваем комментарии
    print('download comments')
    response = youtube()
    items = response.get("items")
    nextPageToken = response.get("nextPageToken")  # скачивается порциями, на каждую следующую выдаётся указатель
    i = 1
    while nextPageToken is not None:
        print(str(i * 100))  # показываем какая сотня комментариев сейчас скачивается
        response = youtube(nextPageToken)
        nextPageToken = response.get("nextPageToken")
        items = items + response.get("items")
        i += 1

    print(len(items))  # Отображаем количество скачаных комментариев

    # Скачиваем реплаи на комментарии
    #print('download replies')
    #replies = []
    #for line in items:  # Проходим по корневым комментам
    #    if line.get("snippet").get("totalReplyCount") > 0:  # если есть реплаи
    #        print(line.get("snippet").get("totalReplyCount"))  # показываем сколько реплаев будет подгружено
    #        response = youtubechild(line.get("snippet").get("topLevelComment").get("id"))
    #        replies = replies + response.get("items")
    #        nextPageToken = response.get("nextPageToken")
    #        i = 1
    #        while nextPageToken is not None:  # догружаем реплаи, если есть ещё порции
    #            response = youtubechild(line.get("snippet").get("topLevelComment").get("id"), nextPageToken)
    #            nextPageToken = response.get("nextPageToken")
    #            replies = replies + response.get("items")
    #            i += 1

    #print(len(replies))  # Отображаем количество скачаных реплаев

    # Сохраняем комментарии и реплаи на них в файл csv
    print("Open csv file")
    with open('youtubecomments.csv', 'w',
              encoding="utf-8") as csv_file:  # конструкция with, чтобы файл закрылся автоматом после всех команд
        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL,
                            lineterminator='\r')  # использовал двойные кавычки и разделитель запятую, такой формат отлично открывается через LibreOffice Calc

        # Заголовки столбцов
        row = [
            'etag'
            , 'parentid'
            , 'id'
            , 'textDisplay'
            , 'textOriginal'
            , 'authorDisplayName'
            , 'authorProfileImageUrl'
            , 'authorChannelUrl'
            , 'authorChannelId'
            , 'likeCount'
            , 'publishedAt'
            , 'updatedAt'
        ]
        print("Start write in csv")
        writer.writerow(row)  # Записываем заголовки в файл

        # Сохраняем комментарии
        print("Write comments in csv")
        for line in items:
            topLevelComment = line.get("snippet").get("topLevelComment")
            # бывает, что у пользователя нет канала, поэтому для него отдельная конструкция
            if topLevelComment.get('snippet').get('authorChannelId') is not None:
                authorChannelId = topLevelComment.get('snippet').get('authorChannelId').get('value')
            else:
                authorChannelId = ''
            row = [
                topLevelComment.get('etag')
                , topLevelComment.get('id')
                , topLevelComment.get('id')
                , topLevelComment.get('snippet').get('textDisplay')
                , topLevelComment.get('snippet').get('textOriginal')
                , topLevelComment.get('snippet').get('authorDisplayName')
                , topLevelComment.get('snippet').get('authorProfileImageUrl')
                , topLevelComment.get('snippet').get('authorChannelUrl')
                , authorChannelId
                , topLevelComment.get('snippet').get('likeCount')
                , topLevelComment.get('snippet').get('publishedAt')
                , topLevelComment.get('snippet').get('updatedAt')
            ]
            writer.writerow(row)

        # Сохраняем реплаи
        #print("Write replies in csv")
        #for line in replies:
        #    # бывает, что у пользователя нет канала, поэтому для него отдельная конструкция
        #    if line.get('snippet').get('authorChannelId') is not None:
        #        authorChannelId = line.get('snippet').get('authorChannelId').get('value')
        #    else:
        #        authorChannelId = ''
        #    row = [
        #        line.get('etag')
        #        , line.get('snippet').get('parentId')
        #        , line.get('id')
        #        , line.get('snippet').get('textDisplay')
        #        , line.get('snippet').get('textOriginal')
        #        , line.get('snippet').get('authorDisplayName')
        #        , line.get('snippet').get('authorProfileImageUrl')
        #        , line.get('snippet').get('authorChannelUrl')
        #        , authorChannelId
        #        , line.get('snippet').get('likeCount')
        #        , line.get('snippet').get('publishedAt')
        #        , line.get('snippet').get('updatedAt')
        #    ]
        #    writer.writerow(row)

    print("done")


#if __name__ == "__main__":
#   main()