import time
from batch import check_all_pre_market_stocks
from trading_calendars import get_calendar
import pandas as pd
import datetime
from common import LifeLimitedList
from config import Config


def is_US_pre_market_hour(next_open, next_close):
    now = pd.Timestamp.now(tz="UTC").tz_convert("Asia/Shanghai")
    return next_close > now > next_open


def next_market_open_and_close():
    us_calendar = get_calendar('XNYS')
    now = pd.Timestamp.now(tz="UTC")
    next_open = us_calendar.next_open(now)
    next_open = next_open.tz_convert("Asia/Shanghai")
    next_close = next_open + datetime.timedelta(hours=6.5)
    return next_open, next_close


def next_pre_market_open_and_close():
    # Start running at 4:30 AM Eastern Time
    next_open, next_close = next_market_open_and_close()
    pre_market_open = next_open - datetime.timedelta(hours=5)
    pre_market_close = next_open
    return pre_market_open, pre_market_close


if __name__ == "__main__":
    gp = r"/home/ubuntu/data/market_watch_reports/intraday_signal.txt"
    life_limited_list = LifeLimitedList(Config.SignalLifeTime)
    next_open, next_close = next_market_open_and_close()
    next_pre_market_open, next_pre_market_close = next_pre_market_open_and_close()
    while True:
        time.sleep(1)
        if is_US_pre_market_hour(next_pre_market_open, next_pre_market_close):
            check_all_pre_market_stocks(gp, life_limited_list)
            time.sleep(Config.PremarketCheckInterval)
        else:
            next_pre_market_open, next_pre_market_close = next_pre_market_open_and_close()
