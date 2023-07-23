import os
from googleapiclient.discovery import build

class Video():

    """Класс для видео на ютубе"""

    def __init__(self, video_id: str):
        self.__video_id = video_id
        APY_KEY: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=APY_KEY)
        video = youtube.videos().list(id=self.__video_id, part='snippet,statistics').execute()
        try:
            #print(video)
            self.title = video['items'][0]['snippet']['title']
            self.url = f"https://www.youtube.com/watch?v={self.__video_id}"
            self.view_count = video['items'][0]['statistics']['viewCount']
            self.like_count = video['items'][0]['statistics']['likeCount']
        except:
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return self.title

# video = Video('AWX4JnAnjBE')
# print(video.title)
# print(video.url)
# print(video.view_count)
# print(video.like_count)

class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id