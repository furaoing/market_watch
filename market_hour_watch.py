import time
from batch import check_all_intraday_stocks
from trading_calendars import get_calendar
import pandas as pd
from common import LifeLimitedList
from config import Config


def is_US_market_hour(next_open, next_close):
    now = pd.Timestamp.now(tz="UTC")
    return next_close > now > next_open


def next_market_open_and_close():
    us_calendar = get_calendar('XNYS')
    now = pd.Timestamp.now(tz="UTC")
    next_open = us_calendar.next_open(now)
    next_close = us_calendar.next_close(now)
    return next_open, next_close


if __name__ == "__main__":
    life_limited_list = LifeLimitedList(Config.SignalLifeTime)
    next_open, next_close = next_market_open_and_close()
    while True:
        gp = r"/home/ubuntu/data/market_watch_reports/intraday_signal.txt"
        time.sleep(1)
        if is_US_market_hour(next_open, next_close):
            check_all_intraday_stocks(gp, life_limited_list)
            time.sleep(Config.MarketCheckInterval)
        else:
            next_open, next_close = next_market_open_and_close()
