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
from common import generate_content_hash
from common import EndPoint
from common import get_time_integer


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


def load_one_stock_helper(request_response, ticker_dict, mysql_updater):
    try:
        response_obj = request_response.result_obj
        # all ticker symbol upper cased
        ticker = request_response.symbol.upper()
        stock_name = ticker_dict[ticker]
        if len(response_obj) < 1:
            msg = "Response Contains No Data"
            root_logger.warning(msg)

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

            has_record = mysql_updater.session.query(StockHistoryPrice).filter_by(Id=hash_str).first()
            if not has_record:
                mysql_updater.session.add(stock_record)
                mysql_updater.session.commit()

    except Exception:
        msg = "Response is: %s" % json.dumps(request_response.result_obj)
        root_logger.error(msg)
        raise Exception("Function: check_one_stock_helper, Exception !")


def load_one_stock(ticker):
    mysql_updater = MySQLUpdater()
    ticker_dict = ticker_lookup()
    end_point = EndPoint(APIConfig.baseURL, APIConfig.version, APIConfig.secret_token)
    range = "1m"
    url = end_point.HistoryPrice(ticker, range)
    r = requests.get(url)
    response = r.text
    return load_one_stock_helper(json.loads(response), ticker_dict, mysql_updater)


def load_batch_stocks(tickers):
    mysql_updater = MySQLUpdater()
    ticker_dict = ticker_lookup()

    data_requests = []
    fetcher = Fetcher()
    end_point = EndPoint(APIConfig.baseURL, APIConfig.version, APIConfig.secret_token)
    range = "1m"
    for ticker in tickers:
        url = end_point.HistoryPrice(ticker, range)
        data_request = DataRequest(ticker, url, DataRequestType.HistoryPrice)
        data_requests.append(data_request)
    fetcher.add_data_requests(data_requests)
    request_response_list = fetcher.fetch()

    for request_response in request_response_list:
        load_one_stock_helper(request_response, ticker_dict, mysql_updater)
    mysql_updater.clean_up()


def batch_load():
    all_tickers = get_tickers()
    try:
        load_batch_stocks(all_tickers)
    except Exception:
        root_logger.error(traceback.format_exc())


if __name__ == "__main__":
    batch_load()
