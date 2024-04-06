import time
import hashlib
import json
import os
from utils import get_tickers, ticker_lookup
from trading_calendars import get_calendar
import pandas as pd
import requests
from config import Config
import tushare as ts


def get_formated_time():
    struct_time = time.localtime()
    year = struct_time.tm_year
    month = struct_time.tm_mon
    day = struct_time.tm_mday
    hour = struct_time.tm_hour
    min = struct_time.tm_min
    sec = struct_time.tm_sec
    formated_time = str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(min) + ":" + str(sec)
    return formated_time


def generate_content_hash(item_list):
    content_cancate = ""
    for x in item_list:
        content_cancate = content_cancate + str(x)
    return hashlib.md5(content_cancate.encode("utf-8")).hexdigest()


def generate_sid():
    all_tickers = get_tickers()
    ticker_lookup_dict = ticker_lookup()
    dest_dir_path = "data"
    dest_f_path = os.path.join(dest_dir_path, "sid.jsonl")
    sid_start = 0
    sid_records = []

    for ticker_name in all_tickers:
        sid_start += 1
        stock_name = ticker_lookup_dict[ticker_name]
        sid_record = {"sid": sid_start, "ticker_name": ticker_name, "stock_name": stock_name, "effective_date": "2019-04-24"}
        sid_records.append(sid_record)

    with open(dest_f_path, "w", encoding="utf8", newline="\n") as f:
        for x in sid_records:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")


def get_time_integer(date_str):
    result = date_str.split("-")
    tmp_str = ""
    for x in result:
        tmp_str = tmp_str + x
    time_integer = int(tmp_str)
    return time_integer


class LifeLimitedList(object):
    def __init__(self, life_cycle):
        self.life_cycle = life_cycle
        self.container = []

    def _generate_data_point(self, obj):
        return {"obj": obj, "ts": time.time()}

    def add_obj(self, obj):
        data_point = self._generate_data_point(obj)
        self.container.append(data_point)

    def self_clean(self):
        current_ts = time.time()
        for data_point in self.container:
            ts = data_point["ts"]
            if current_ts - ts > self.life_cycle:
                self.container.remove(data_point)

    def get_all_obj(self):
        self.self_clean()
        all_obj = [x["obj"] for x in self.container]
        return all_obj

    def __contains__(self, x):
        all_obj = self.get_all_obj()
        if x in all_obj:
            return True
        else:
            return False

    def contains(self, x):
        return self.__contains__(x)


def generate_signal_msg(record):
    signals = record["signals"]
    ticker = record["ticker"]
    tmp = r"%s: %s" % ("|".join(signals), ticker)
    return tmp


def generate_short_records_msg(records):
    signal_msg_list = []
    for record in records:
        tmp = generate_signal_msg(record)
        signal_msg_list.append(tmp)
    notification_msg = "\n".join(signal_msg_list)
    return notification_msg


def filter_records_by_life_cycle(records, life_limited_list):
    new_records = []
    for record in records:
        signals = record["signals"]
        ticker = record["ticker"]
        non_repeat_signals = []
        for signal in signals:
            signal_ticker_hash = signal + "#" + ticker
            if signal_ticker_hash not in life_limited_list:
                life_limited_list.add_obj(signal_ticker_hash)
                non_repeat_signals.append(signal)

        if len(non_repeat_signals) > 0:
            new_record = dict()
            new_record["signals"] = non_repeat_signals
            new_record["ticker"] = ticker
            new_records.append(new_record)
    return new_records


class EndPoint(object):
    def __init__(self, baseURL, version, token):
        self.baseURL = baseURL
        self.token = token
        self.version = version
        self.prefix = "%s/%s" % (self.baseURL, self.version)

    def Price(self, symbol):
        url = self.prefix + "/stock/%s/price" % symbol + "?token=" + self.token
        return url

    def HistoryPrice(self, symbol, range):
        # range: 1m
        url = self.prefix + "/stock/%s/chart/%s" % (symbol, range) + "?token=" + self.token
        return url

    def OneDayPrice(self, symbol, date):
        # one day: 20190617
        url = self.prefix + "/stock/%s/chart/date/%s" % (symbol, date) + "?token=" + self.token + "&chartByDay=true"
        return url

    def PreviousDayPrice(self, symbol):
        # previous trading day
        url = self.prefix + "/stock/%s/previous" % symbol + "?token=" + self.token
        return url

    def Quote(self, symbol):
        # quote
        url = self.prefix + "/stock/%s/quote" % symbol + "?token=" + self.token
        return url

    def Stat(self, symbol, field):
        # shares outstanding
        url = self.prefix + "/stock/%s/stats/%s" % (symbol, field) + "?token=" + self.token
        return url

    def Earnings(self, symbol):
        # shares outstanding
        url = self.prefix + "/stock/%s/upcoming-earnings" % (symbol) + "?token=" + self.token
        return url

    def IntradayPrice(self, symbol, params=None):
        if params is None:
            params = {}
        params["token"] = self.token
        param_pairs = []
        for k, v in params.items():
            param_pairs.append("%s=%s" % (str(k), str(v)))
        param_str = "&".join(param_pairs)
        url = self.prefix + "/stock/%s/intraday-prices?%s" % (symbol, param_str)
        return url


def next_market_open_and_close_cntime():
    us_calendar = get_calendar('XNYS')
    now = pd.Timestamp.now(tz="UTC")
    next_open = us_calendar.next_open(now).tz_convert("Asia/Shanghai")
    next_close = us_calendar.next_close(now).tz_convert("Asia/Shanghai")
    return next_open, next_close


class GetFXRate(object):
    def __init__(self):
        base_url = "http://data.fixer.io/api/latest?access_key=%s&symbols=USD,CNY&format=1"
        self.request_url = base_url % Config.FIXER_KEY

    def get_cny_usd(self):
        r = requests.get(self.request_url)
        r.encoding = "utf8"
        obj = json.loads(r.text)
        USD_value = obj.get("rates").get("USD")
        CNY_value = obj.get("rates").get("CNY")
        return CNY_value/USD_value


class GetCNIndex(object):
    def __init__(self):
        pass

    def csi300(self):
        r = ts.get_realtime_quotes('hs300')
        previous = float(r.iloc[-1].get("pre_close"))
        today = float(r.iloc[-1].get("price"))
        return {"previous": previous, "today": today}


if __name__ == "__main__":
    # t = 5
    # x = "OK"
    # my_list = LifeLimitedList(t)
    # my_list.add_obj(x)
    # time.sleep(1)
    # print(my_list.contains(x))
    from config import APIConfig
    end_point = EndPoint(APIConfig.baseURL, APIConfig.version, APIConfig.secret_token)

    print(end_point.OneDayPrice("AAPL", "20190617"))