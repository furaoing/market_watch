from waffle.time import constants
from batch_load_previous_day_price import batch_load
import time
from trading_calendars import get_calendar
import pandas as pd
import datetime


def is_after_market_hour(next_open):
    now = pd.Timestamp.now(tz="UTC")
    # Start From 4:05 ET On Trading Day
    return now > next_open - datetime.timedelta(hours=5.4)


def next_market_open_and_close():
    us_calendar = get_calendar('XNYS')
    now = pd.Timestamp.now(tz="UTC")
    next_open = us_calendar.next_open(now)
    next_close = us_calendar.next_close(now)
    return next_open, next_close


if __name__ == "__main__":
    next_open, next_close = next_market_open_and_close()
    while True:
        time.sleep(1)
        if is_after_market_hour(next_open):
            batch_load()
            time.sleep(15*constants.HOURS)
            next_open, next_close = next_market_open_and_close()

