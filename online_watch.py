import time
from waffle.time import utils, constants
from batch import check_all_stocks
import pandas as pd


def is_valid_reporting_day():
    now = pd.Timestamp.now(tz="UTC").tz_convert("Asia/Shanghai")
    day_of_week = now.dayofweek

    if 1 <= day_of_week <= 5:
        return True
    else:
        return False


if __name__ == "__main__":
    while True:
        gp = r"/home/ubuntu/data/market_watch_reports/stock_signal_list.txt"
        time.sleep(constants.MINUTES)
        ct = utils.get_struct_stime()
        if ct.tm_hour == 6 and is_valid_reporting_day():
            check_all_stocks(gp)
            time.sleep(constants.HOURS + 1)

