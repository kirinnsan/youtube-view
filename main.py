from datetime import datetime, timezone

import pandas as pd

import auth
from client import ApiClient
from util import convert_video_time_sec
from visualize import showChart

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/youtube']
YOUTUBE_VIDEO_BASE_URL = 'https://www.youtube.com/watch?v='


class WatchHistory(object):
    """視聴履歴を保持するクラス"""

    def __init__(self, title, title_url, date_time):
        self.title = title
        self.title_url = title_url
        self.date_time = date_time
        if isinstance(title_url, str):
            self.video_id = title_url.replace(YOUTUBE_VIDEO_BASE_URL, '')
        else:
            self.video_id = ''


class VideoInfo(object):
    """ビデオ情報を保持するクラス"""

    def __init__(self, id, title, categoryId, play_time_sec):
        self.id = id
        self.title = title
        self.categoryId = categoryId
        self.play_time_sec = play_time_sec


class HistoryGeneral(object):
    """履歴情報を管理するクラス"""

    def __init__(self, watchHistories: WatchHistory):
        self.__watch_history_list = [WatchHistory(
            w[0], w[1], w[2]) for w in watchHistories]
        self.__video_info_list = []

    def add_video_info(self, video_info: VideoInfo):
        self.video_info_list.append(video_info)

    @property
    def watch_history_list(self):
        return self.__watch_history_list

    @property
    def video_info_list(self):
        return self.__video_info_list

    def get_viewing_time(self):
        total_time_sec = 0
        for video in self.video_info_list:
            total_time_sec += video.play_time_sec
        return total_time_sec

    def statistics(self):
        result = []
        for video in self.video_info_list:
            video_id = video.id
            for watch_history in self.watch_history_list:
                if watch_history.video_id == video_id:
                    # TODO チャートで表示できる形にする
                    result.append({
                        'date_time': watch_history.date_time,
                        'time_sec': video.play_time_sec
                    })
        return result

    def aggregate(self, data_list):
        """日付毎にデータを集計"""
        df_agg = pd.DataFrame(data_list)
        print(df_agg)
        return df_agg


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

    result = df_range[['title', 'titleUrl', 'time']]
    result = result.values.tolist()

    return result


def create_video_id(data_list):
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
    watch_histroy = load_watch_history()

    history = HistoryGeneral(watch_histroy)

    video_id_list = create_video_id(watch_histroy)

    creds = auth.authenticate(SCOPES)
    client = ApiClient(creds)

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

    total_sec = history.get_viewing_time()
    viewing_time_by_day = history.statistics()
    result = history.aggregate(viewing_time_by_day)

    showChart(result)


if __name__ == '__main__':
    main()
