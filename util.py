import re

ZERO_SEC = 0


def convert_video_time_sec(duration):
    """
    ISO8601文字列としてフォーマットされた動画時間を秒単位で返す。
    例）
    PT23M54S
    23分、54秒
    P3Y6M4DT12H30M5S
    3年、6ヶ月、4日、12時間、30分、5秒

    Note:ISO8601について
        https://ja.wikipedia.org/wiki/ISO_8601
    """
    m = re.search('T.*', duration)
    if m is None:
        return ZERO_SEC

    time_duration_str = m.group().replace('T', '')

    result = re.split('[HMS]', time_duration_str)
    if result is None:
        raise Exception()

    # 空要素削除
    result = list(filter(None, result))

    sec = 0
    if len(result) == 3:
        sec = int(result[0]) * 3600 + int(result[1]) * 60 + int(result[2])
    elif len(result) == 2:
        sec = int(result[0]) * 60 + int(result[1])
    elif len(result) == 1:
        sec = int(result[0])

    return sec


if __name__ == "__main__":
    result = convert_video_time_sec('PT23M54S')
    print(result)
