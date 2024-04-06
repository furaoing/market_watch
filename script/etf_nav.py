# -*- coding: utf-8 -*-

import sys
sys.path.append('../')
from common import GetFXRate
from common import GetCNIndex
from datetime import date
import time
from market_watch_logger import root_logger
import sys


class ETF(object):
    def __init__(self):
        self.fx_fetcher = GetFXRate()


class CSI300(ETF):
    def __init__(self):
        super().__init__()
        self.cn_index = GetCNIndex()

    def get_nav(self, csi300=None):
        # NAV is determined at 4:00 PM EDT
        # 10 Sep 2019 18:00 UTC USD/CNY = 7.11261, ASHR NAV = USD 28.29, CSI300_index = 3959.2650
        usd_cny = self.fx_fetcher.get_cny_usd()

        try:
            csi300 = self.cn_index.csi300()
            today_close = csi300.get("today")
        except:
            root_logger.error("Fetching Data via Tushare Failed, Using Given CSI300 Index Value")
            if not csi300:
                root_logger.error("CSI300 Index Value Not Given, Process Terminated")
                sys.exit(1)
            else:
                today_close = csi300
        fee_rate_per_day = 0.0066/365
        current_nav_before_fee = ((7.11261 * 28.29)/usd_cny)*(today_close/3959.2650)

        date_reference = date(2019, 9, 10)
        current_gmt = time.gmtime()
        current_year, current_month, current_day = current_gmt.tm_year, current_gmt.tm_mon, current_gmt.tm_mday
        current_date = date(current_year, current_month, current_day)
        day_difference_time_delta = current_date - date_reference

        nav_after_estimated_fees = current_nav_before_fee * (1 - fee_rate_per_day*day_difference_time_delta.days)
        return nav_after_estimated_fees


if __name__ == "__main__":
    csi300 = CSI300()
    today_csi_300 = 3890.66
    result = csi300.get_nav(today_csi_300)
    print(result)