import requests
import json
import logging
from config import APIConfig
from utils import get_tickers, ticker_lookup
from network import Fetcher
import sys
import traceback
from constants import DataRequestType
from data_model import DataRequest, StockHistoryPrice
from database import MySQLUpdater

import hashlib


def get_time_integer(date_str):
    result = date_str.split("-")
    tmp_str = ""
    for x in result:
        tmp_str = tmp_str + x
    time_integer = int(tmp_str)
    return time_integer


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



def generate_content_hash(item_list):
    content_cancate = ""
    for x in item_list:
        content_cancate = content_cancate + str(x)
    return hashlib.md5(content_cancate.encode("utf-8")).hexdigest()



error_handler = logging.StreamHandler(sys.stderr)
error_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s/%(name)s, %(message)s"))
error_handler.setLevel(logging.ERROR)

info_handler = logging.StreamHandler(sys.stdout)
info_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s/%(name)s, %(message)s"))
info_handler.setLevel(logging.INFO)

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(error_handler)
root_logger.addHandler(info_handler)

right_tickers = []

def screen_tickers(price_history):
    adj_volume = []
    adj_close = []
    part_history = price_history[-4:]
    for record in part_history:
        adj_close.append(record.AdjClosePrice)
        adj_volume.append(record.AdjVolume)

    if len(price_history) == 0:
        return False

    average_volume = sum(adj_volume) / len(adj_volume)
    average_price = sum(adj_close) / len(adj_close)
    average_dollar_volume = average_volume * average_price
    if average_dollar_volume < 5000000 or average_price < 1:
        return False
    else:
        return True


def check_if_sequential_increase(price_history):
    adj_volume = []
    adj_close = []
    part_history = price_history[-4:]
    for record in part_history:
        adj_close.append(record.AdjClosePrice)
        adj_volume.append(record.AdjVolume)

    if len(price_history) == 0:
        return False

    average_volume = sum(adj_volume)/len(adj_volume)
    average_price = sum(adj_close)/len(adj_close)
    average_dollar_volume = average_volume * average_price
    if average_dollar_volume < 15000000 or average_price < 1:
        return False

    if_true = True
    for i in range(len(part_history)-1):
        if part_history[i+1].AdjClosePrice > part_history[i].AdjClosePrice and part_history[i+1].AdjClosePrice > part_history[i+1].AdjOpen \
                and part_history[i].AdjClosePrice > part_history[i].AdjOpen:
            if_true = if_true * True
        else:
            if_true = if_true * False
    if if_true:
        print(adj_close)
    return if_true


sequential_increase_tickers = []
def load_one_stock_helper(request_response, ticker_dict):
    try:
        history = []
        response_obj = request_response.result_obj
        # all ticker symbol upper cased
        ticker = request_response.symbol.upper()
        stock_name = ticker_dict[ticker]
        if len(response_obj) < 1:
            msg = "Response Contains No Data"
            root_logger.warning(msg)
            return 0

        for x in response_obj:
            open_price = x["uOpen"]
            adj_open_price = x["open"]
            high_price = x["uHigh"]
            adj_high_price = x["high"]
            low_price = x["uLow"]
            adj_low_price = x["low"]
            close_price = x["uClose"]
            adj_close_price = x["close"]
            volume = x["uVolume"]
            adj_volume = x["volume"]
            date = x["date"]

            hash_item_list = [ticker, stock_name, date]
            hash_str = generate_content_hash(hash_item_list)
            stock_record = StockHistoryPrice(Id=hash_str,
                                             TickerName=ticker,
                                             StockName=stock_name,
                                             Open=open_price,
                                             AdjOpen=adj_open_price,
                                             High=high_price,
                                             AdjHigh=adj_high_price,
                                             Low=low_price,
                                             AdjLow=adj_low_price,
                                             ClosePrice=close_price,
                                             AdjClosePrice=adj_close_price,
                                             Volume=volume,
                                             AdjVolume=adj_volume,
                                             DateFormated=date,
                                             DateInteger=get_time_integer(date))

            history.append(stock_record)
        if screen_tickers(history):
            right_tickers.append(ticker.lower())
        #if_sequential_increase = check_if_sequential_increase(history)
        #if if_sequential_increase:
            #sequential_increase_tickers.append(ticker)
            #print("Sequential Increase Ticker: %s" % ticker)

    except Exception:
        msg = "Response is: %s" % json.dumps(request_response.result_obj)
        root_logger.error(msg)
        raise Exception("Function: check_one_stock_helper, Exception !")


def load_one_stock(ticker):
    #mysql_updater = MySQLUpdater()
    ticker_dict = ticker_lookup()
    end_point = EndPoint(APIConfig.baseURL, APIConfig.version, APIConfig.secret_token)
    range = "5d"
    url = end_point.HistoryPrice(ticker, range)
    r = requests.get(url)
    response = r.text
    return load_one_stock_helper(json.loads(response), ticker_dict)


def load_batch_stocks(tickers):
    # mysql_updater = MySQLUpdater()
    ticker_dict = ticker_lookup()

    fetcher = Fetcher()
    end_point = EndPoint(APIConfig.baseURL, APIConfig.version, APIConfig.secret_token)
    range = "5d"

    tickers_list = list(tickers)
    tickers_list = tickers_list
    print("Ticker List Len %s" % str(len(tickers_list)))
    part_range = 100

    i = 0
    while i < len(tickers_list)-part_range-2:
        data_requests = []
        tickers_list_part = tickers_list[i:i+part_range]
        for ticker in tickers_list_part:
            url = end_point.HistoryPrice(ticker, range)
            data_request = DataRequest(ticker, url, DataRequestType.HistoryPrice)
            data_requests.append(data_request)
        fetcher.add_data_requests(data_requests)
        request_response_list = fetcher.fetch()

        for request_response in request_response_list:
            load_one_stock_helper(request_response, ticker_dict)
        print("Fetched and Processed: %s" % str(len(request_response_list)))
        i = i + part_range



def batch_load():
    all_tickers = get_tickers()
    try:
        load_batch_stocks(all_tickers)
    except Exception:
        root_logger.error(traceback.format_exc())


if __name__ == "__main__":
    batch_load()
    #print(sequential_increase_tickers)
    print(right_tickers)
    with open(r"data/ticker_universe.json", "w", encoding="utf-8") as f:
        f_content = json.dumps(right_tickers, ensure_ascii=False)
        f.write(f_content)

