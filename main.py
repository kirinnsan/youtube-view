from datetime import datetime, timezone

import pandas as pd

import auth
from client import ApiClient
from util import convert_video_time_sec

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/youtube']
YOUTUBE_VIDEO_BASE_URL = 'https://www.youtube.com/watch?v='


def get_watch_history():

    # Youtube履歴のjson読み込み
    df = pd.read_json('watch-history.json', encoding='utf-8')

    # print(df.head())
    # timeカラムをdatetime型に変更
    df['time'] = pd.to_datetime(df['time'])

    # 今月視聴したデータ取得
    today = datetime.today()
    df_range = df[df['time'] > datetime(
        today.year, today.month, 1, tzinfo=timezone.utc)]

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

    creds = auth.authenticate(SCOPES)
    client = ApiClient(creds)

    time_and_video_url_list = get_watch_history()

    video_id_list = create_video_id_list(time_and_video_url_list)

    # 再生履歴のビデオ情報を取得
    for index in range(0, len(video_id_list), 50):

        tmp = video_id_list[index:index + 50]
        video_id_list_str = ','.join(tmp)

        result = client.get_videos_list(video_id_list_str)

        video_items = result['items']

        # 各ビデオ情報を取得
        for video_item in video_items:
            title = video_item['snippet']['title']
            categoryId = video_item['snippet']['categoryId']
            duration = video_item['contentDetails']['duration']
            duration_sec = convert_video_time_sec(duration)
            # TODO
            print(video_item)


if __name__ == '__main__':
    main()
