from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


class ApiClient(object):

    def __init__(self, credential):
        self.service = build(YOUTUBE_API_SERVICE_NAME,
                             YOUTUBE_API_VERSION, credentials=credential)

    def fetch_videos_list(self, video_id: str):
        """
        YouTube動画IDに一致する動画情報を取得。
        idパラメータは、カンマ区切りで複数指定可能。
        """
        try:
            result = self.service.videos().list(
                id=video_id,
                part="snippet,contentDetails,statistics"
            ).execute()
        except HttpError as err:
            print(f'action=fetch_videos_list error={err}')
            raise

        return result

    def fetch_video_categories_list(self):
        """
        ビデオカテゴリ情報を取得。

        Note:
            regionCodeに、ISO 3166-1 alpha-2 の国コードを指定すると、
            指定された国で使用できる動画カテゴリのリストを返す。
        """
        try:
            result = self.service.videoCategories().list(
                part="snippet",
                regionCode="JP"
            ).execute()
        except HttpError as err:
            print(f'action=fetch_video_categories_list error={err}')
            raise

        return result

    def fetch_youtube_channels_list(self):
        """自身のチャンネルリストを取得。"""
        try:
            result = self.service.channels().list(
                mine=True,
                part="id,snippet,contentDetails"
            ).execute()
        except HttpError as err:
            print(f'action=fetch_youtube_channels_list error={err}')
            raise

        return result

    def fetch_youtube_playlists_list(self):
        """自身の再生リストを取得。"""
        try:
            result = self.service.playlists().list(
                mine=True,
                part="id,snippet,status",
                maxResults=50
            ).execute()
        except HttpError as err:
            print(f'action=fetch_youtube_playlists_list error={err}')
            raise

        return result
