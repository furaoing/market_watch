# -*- coding: utf-8 -*-
from finra_short_sell import construct_time_str, get_one_day_data
import logging


if __name__ == "__main__":
    data = [{'sell_time': '2018-10-01', 'ticker': u'IGC'}, {'sell_time': '2018-10-02', 'ticker': u'NBEV'}, {'sell_time': '2018-10-03', 'ticker': u'IGC'}, {'sell_time': '2018-11-01', 'ticker': u'VCYT'}, {'sell_time': '2018-12-12', 'ticker': u'BIMI'}, {'sell_time': '2018-12-20', 'ticker': u'MRIN'}, {'sell_time': '2019-01-09', 'ticker': u'CLPS'}, {'sell_time': '2019-01-10', 'ticker': u'PHUN'}, {'sell_time': '2019-01-11', 'ticker': u'ORGO'}, {'sell_time': '2019-01-11', 'ticker': u'LKCO'},
            {'sell_time': '2019-01-23', 'ticker': u'AVCO'}, {'sell_time': '2019-02-01', 'ticker': u'PHUN'},
            {'sell_time': '2019-03-12', 'ticker': u'GLBS'}, {'sell_time': '2019-03-27', 'ticker': u'HUNT'},
            {'sell_time': '2019-04-02', 'ticker': u'MXC'}, {'sell_time': '2019-05-30', 'ticker': u'SOLY'},
            {'sell_time': '2019-06-11', 'ticker': u'BYND'}, {'sell_time': '2019-06-13', 'ticker': u'AIM'},
            {'sell_time': '2019-07-01', 'ticker': u'MTC'}]
    logging.basicConfig(level=logging.INFO)

    for record in data:
        ticker = record.get("ticker")
        sell_time = record.get("sell_time")
        split_result = sell_time.split("-")
        year = int(split_result[0])
        month = int(split_result[1])
        day = int(split_result[2])
        date_str = construct_time_str(year, month, day)
        result = get_one_day_data(ticker, date_str)
        print(ticker)
        print(result)