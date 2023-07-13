import os
import datetime

import isodate
from googleapiclient.discovery import build


class PlayList():
    def __init__(self, playlist_id: str):
        self.__playlist_id = playlist_id
        APY_KEY: str = os.getenv('API_KEY')
        self.__youtube = build('youtube', 'v3', developerKey=APY_KEY)
        playlist = self.__youtube.playlists().list(id=self.__playlist_id, part='snippet').execute()
        self.__title = playlist['items'][0]['snippet']['title']
        self.__url = f"https://www.youtube.com/playlist?list={self.__playlist_id}"
        self.__videos = self.__youtube.playlistItems().list(playlistId=self.__playlist_id,
                                                             part='contentDetails',
                                                             maxResults=50,
                                                             ).execute()

    @property
    def title(self):
        return self.__title

    @property
    def url(self):
        return self.__url

    @property
    def videos(self):
        return self.__videos

    @property
    def total_duration(self):
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.__videos['items']]
        video_response = self.__youtube.videos().list(part='contentDetails',
                                                      id=','.join(video_ids)
                                                      ).execute()
        total_duration = datetime.timedelta()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        video_ids = [video['contentDetails']['videoId'] for video in self.__videos['items']]
        video_response = self.__youtube.videos().list(part='statistics',
                                                      id=','.join(video_ids)).execute()
        max_likes = 0
        best_video_id = ''
        for video in video_response['items']:
            likes = int(video['statistics']['likeCount'])
            if likes > max_likes:
                max_likes = likes
                best_video_id = video['id']
        return f"https://youtu.be/{best_video_id}"