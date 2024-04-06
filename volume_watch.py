import time
from batch import check_all_market_volume
from trading_calendars import get_calendar
import pandas as pd
import datetime
from common import LifeLimitedList
from config import Config


def is_US_market_hour(next_open, next_close):
    now = pd.Timestamp.now(tz="UTC").tz_convert("Asia/Shanghai")
    return next_close > now > next_open


def next_market_open_and_close():
    us_calendar = get_calendar('XNYS')
    now = pd.Timestamp.now(tz="UTC")
    next_open = us_calendar.next_open(now)
    next_open = next_open.tz_convert("Asia/Shanghai")
    next_close = next_open + datetime.timedelta(hours=6.5) - datetime.timedelta(hours=3)
    return next_open, next_close


if __name__ == "__main__":
    life_limited_list = LifeLimitedList(Config.SignalLifeTime)
    next_open, next_close = next_market_open_and_close()
    while True:
        gp = r"/home/ubuntu/data/market_watch_reports/intraday_signal.txt"
        time.sleep(1)
        if is_US_market_hour(next_open, next_close):
            check_all_market_volume(gp, life_limited_list)
        else:
            next_open, next_close = next_market_open_and_close()
