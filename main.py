from datetime import datetime, timezone

import pandas as pd

import auth
from client import ApiClient
from util import convert_video_time_sec

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/youtube']
YOUTUBE_VIDEO_BASE_URL = 'https://www.youtube.com/watch?v='


class WatchHisroty(object):
    def __inti__(self, title, title_url, date_time):
        self.title = title
        self.title_url = title_url
        self.data_time = date_time


class VideoInfo(object):
    def __init__(self, id, title, categoryId, play_time_sec):
        self.id = id
        self.title = title
        self.categoryId = categoryId
        self.play_time_sec = play_time_sec


class History(object):
    def __init__(self):
        self.__video_info_list = []

    def add_video_info(self, video_info):
        self.video_info_list.append(video_info)

    @property
    def video_info_list(self):
        return self.__video_info_list

    def get_viewing_time(self):
        total_time_sec = 0
        for video in self.video_info_list:
            total_time_sec += video.play_time_sec
        return total_time_sec

    # @video_info_list.setter
    # def video_info_list(self, video_info_list):
    #     self.__video_info_list = video_info_list


def load_watch_history():

    # Youtube履歴のjson読み込み
    df = pd.read_json('watch-history.json', encoding='utf-8')

    # timeカラムをdatetime型に変更
    df['time'] = pd.to_datetime(df['time'])

    # 今月視聴したデータ取得
    # today = datetime.today()
    # df_range = df[df['time'] > datetime(
    #     today.year, today.month, 1, tzinfo=timezone.utc)]
    # TODO 動作確認のため、2021年1月10日以降のデータを対象
    today = datetime.today()
    df_range = df[df['time'] > datetime(
        today.year, today.month, 10, tzinfo=timezone.utc)]

    result = df_range[['time', 'titleUrl']]
    time_and_video_url_list = result.values.tolist()

    return time_and_video_url_list


def create_video_id_list(data_list):
    video_id_list = []
    for data in data_list:
        video_url = data[1]
        # 型が文字列でない または ビデオのベースurlが含まれていない場合
        if not isinstance(video_url, str) or YOUTUBE_VIDEO_BASE_URL not in video_url:
            continue
        # ビデオIDパラメータを追加
        video_id_list.append(video_url.replace(YOUTUBE_VIDEO_BASE_URL, ''))

    return video_id_list


def main():
    # 再生履歴データ読み込み
    time_and_video_url_list = load_watch_history()

    video_id_list = create_video_id_list(time_and_video_url_list)

    creds = auth.authenticate(SCOPES)
    client = ApiClient(creds)

    history = History()

    # 再生履歴のビデオ情報を取得
    for index in range(0, len(video_id_list), 50):

        tmp = video_id_list[index:index + 50]
        video_id_list_str = ','.join(tmp)

        result = client.get_videos_list(video_id_list_str)

        video_items = result['items']

        # 動画情報を取得
        for video_item in video_items:
            id = video_item['id']
            title = video_item['snippet']['title']
            category_id = video_item['snippet']['categoryId']
            duration_sec = convert_video_time_sec(
                video_item['contentDetails']['duration'])
            # print(video_item)
            video_info = VideoInfo(id, title, category_id, duration_sec)

            history.add_video_info(video_info)

    print(history.get_viewing_time())


if __name__ == '__main__':
    main()
