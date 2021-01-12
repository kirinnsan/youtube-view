from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


class ApiClient(object):

    def __init__(self, credential):
        self.service = build(YOUTUBE_API_SERVICE_NAME,
                             YOUTUBE_API_VERSION, credentials=credential)

    def get_videos_list(self, video_id):
        """
        YouTube動画IDに一致する動画情報を取得。
        idパラメータには、取得するリソースのYouTube動画IDをカンマ区切りリストの形式で指定。
        """
        try:
            result = self.service.videos().list(
                id=video_id,
                part="snippet,contentDetails,statistics"
            ).execute()
        except HttpError as err:
            print(f'action=get_videos_list error={err}')
            raise

        return result

    def get_youtube_channels_list(self):
        try:
            # 自身のチャンネルリストを取得。
            result = self.service.channels().list(
                mine=True,
                part="id,snippet,contentDetails"
            ).execute()
        except HttpError as err:
            print(f'action=get_youtube_channels_list error={err}')
            raise

        return result

    def get_youtube_playlists(self, list_id):
        # Call the Youtube API
        try:
            result = self.service.playlists().list(
                mine=True,
                part="id,snippet,status",
                maxResults=50
            ).execute()
        except HttpError as err:
            print(f'action=get_youtube_playlists error={err}')
            raise

        return result
