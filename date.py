"""
日付クラス

Copyright (c) 2023 led-mirage
"""

import machine


# 日付クラス
class Date:
    # コンストラクタ
    def __init__(self, year=1, month=1, day=1):
        self.year = year
        self.month = month
        self.day = day

    # 減算
    def __sub__(self, other):
        days_in_self = self.days_since_epoch()
        days_in_other = other.days_since_epoch()
        return days_in_self - days_in_other

    # グレゴリウス暦１年１月１日からの経過日数を求める
    def days_since_epoch(self):
        return days_since_epoch(self.year, self.month, self.day)

    # テキスト化
    def text(self):
        return f"{self.year}年{self.month}月{self.day}日"

    @classmethod
    def today(cls):
        d = machine.RTC().datetime()
        return Date(d[0], d[1], d[2])


# グレゴリウス暦１年１月１日からの経過日数を求める
# 出典：https://ufcpp.net/study/algorithm/o_days.html
def days_since_epoch(y, m, d):
    # 1・2月 → 前年の13・14月
    if m <= 2:
        y -= 1
        m += 12

    dy = 365 * (y - 1)  # 経過年数×365日
    c = y // 100
    dl = (y >> 2) - c + (c >> 2)  # うるう年分
    dm = (m * 979 - 1033) >> 5  # 1月1日から m 月1日までの日数
    return dy + dl + dm + d - 1
