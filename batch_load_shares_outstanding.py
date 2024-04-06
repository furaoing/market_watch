import json
import logging
from config import APIConfig
from utils import get_tickers, ticker_lookup
from network import Fetcher
import sys
import traceback
from constants import DataRequestType
from data_model import DataRequest, StockSharesOutstanding
from database import MySQLUpdater
from common import generate_content_hash
from common import EndPoint


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


def load_one_stock_helper(request_response, ticker_dict, mysql_updater, f):
    try:
        response_obj = request_response.result_obj
        # all ticker symbol upper cased
        ticker = request_response.symbol.upper()
        stock_name = ticker_dict[ticker]
        if type(response_obj) is not int and type(response_obj) is not float:
            msg = "Response Contains Invalid Data"
            root_logger.warning(msg)
            return None

        shares_outstanding = int(response_obj)
        f.write(ticker + "," + str(shares_outstanding) + "\n")
        hash_item_list = [ticker, stock_name]
        hash_str = generate_content_hash(hash_item_list)
        stock_record = StockSharesOutstanding(Id=hash_str,
                                         TickerName=ticker,
                                         StockName=stock_name,
                                         SharesOutstanding=shares_outstanding)

        has_record = mysql_updater.session.query(StockSharesOutstanding).filter_by(Id=hash_str).first()
        if not has_record:
            mysql_updater.session.add(stock_record)
            mysql_updater.session.commit()

    except Exception:
        msg = "Response is: %s" % json.dumps(request_response.result_obj)
        root_logger.error(msg)
        raise Exception("Function: check_one_stock_helper, Exception !")


def load_batch_stocks(tickers, f):
    mysql_updater = MySQLUpdater()
    ticker_dict = ticker_lookup()
    field = "sharesOutstanding"

    data_requests = []
    fetcher = Fetcher()
    end_point = EndPoint(APIConfig.baseURL, APIConfig.version, APIConfig.secret_token)
    for ticker in tickers:
        url = end_point.Stat(ticker, field)
        data_request = DataRequest(ticker, url, DataRequestType.Stat)
        data_requests.append(data_request)
    fetcher.add_data_requests(data_requests)
    request_response_list = fetcher.fetch()

    for request_response in request_response_list:
        load_one_stock_helper(request_response, ticker_dict, mysql_updater, f)
    mysql_updater.clean_up()


def batch_load():
    f = open("outstanding_shares.txt", "w", encoding="utf8", newline="\n")
    f.write("ticker,shares" + "\n")
    all_tickers = get_tickers()
    try:
        load_batch_stocks(all_tickers, f)
    except Exception:
        root_logger.error(traceback.format_exc())
    f.close()


if __name__ == "__main__":
    batch_load()
